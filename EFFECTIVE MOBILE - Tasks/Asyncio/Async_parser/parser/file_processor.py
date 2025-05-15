import os
import pandas as pd
from datetime import datetime
import asyncio

from Async_parser.parser.constants import DOWNLOAD_DIR
from Async_parser.parser.logger import logger
from Async_parser.parser.file_manager import is_file_exist, delete_file
from Async_parser.parser.database_tools import save_spimextradingresult_to_db


async def process_file(session, file_name: str) -> bool:
    file_path = os.path.join(DOWNLOAD_DIR, file_name)

    if not is_file_exist(file_path):
        return False

    try:
        df = await asyncio.to_thread(read_excel_file, file_path)
        if df is None or df.empty:
            return False

        df = await asyncio.to_thread(clean_dataframe, df)
        if df.empty:
            return False

        valid = await asyncio.to_thread(validate_dataframe, df)
        if not valid:
            return False

        records = await asyncio.to_thread(transform_to_records, df)
        if not records:
            return False

        if not await save_spimextradingresult_to_db(session, records):
            return False

        return True

    except Exception as e:
        await handle_processing_error(session, file_name, e)
        return False

    finally:
        delete_file(file_path)


def read_excel_file(file_path: str) -> pd.DataFrame | None:
    try:
        df = pd.read_excel(file_path, sheet_name=0)
        start_index = df.apply(
            lambda row: row.astype(str)
                           .str.contains("Единица измерения: Метрическая тонна", na=False)
                           .any(),
            axis=1
        )
        if start_index.any():
            first = start_index.idxmax() + 1
            df = df.iloc[first:]
            df.columns = df.iloc[0]
            df = df[1:]
        return df
    except Exception as e:
        logger.error(f"[Ошибка] Ошибка при чтении файла {file_path}: {e}")
        return None


def validate_dataframe(df: pd.DataFrame) -> bool:
    if 'Объем Договоров, руб.' not in df.columns:
        logger.warning("Столбец 'Объем Договоров, руб.' не найден.")
        return False
    return True


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.str.replace('\n', ' ').str.strip()

    for col in ['Количество Договоров, шт.', 'Объем Договоров в единицах измерения', 'Объем Договоров, руб.']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    if 'Обьем Договоров, руб.' in df.columns:
        df['Объем Договоров, руб.'] = df.pop('Обьем Договоров, руб.')

    if 'Количество Договоров, шт.' in df.columns:
        df = df[df['Количество Договоров, шт.'] > 0]

    return df.dropna(subset=['Объем Договоров в единицах измерения', 'Объем Договоров, руб.', 'Количество Договоров, шт.'])


def transform_to_records(df: pd.DataFrame) -> list[dict]:
    records = []
    now = datetime.utcnow()
    for _, row in df.iterrows():
        code = row.get('Код Инструмента')
        try:
            volume = float(row.get('Объем Договоров в единицах измерения'))
            total = float(row.get('Объем Договоров, руб.'))
            count = int(row.get('Количество Договоров, шт.'))
        except Exception:
            logger.warning(f"Невозможно преобразовать числовые поля в строке: {row.to_dict()}")
            continue

        if not isinstance(code, str) or len(code) < 7:
            continue

        records.append({
            'exchange_product_id': code,
            'exchange_product_name': row.get('Наименование Инструмента'),
            'delivery_basis_name': row.get('Базис поставки'),
            'volume': volume,
            'total': total,
            'count': count,
            'oil_id': code[:4],
            'delivery_basis_id': code[4:7],
            'delivery_type_id': code[-1],
            'date': now.strftime("%Y-%m-%d"),
            'created_on': now,
            'updated_on': now
        })
    return records


async def handle_processing_error(session, filename: str, error: Exception):
    await session.rollback()
    logger.exception(f"[Ошибка] Ошибка обработки файла {filename}: {error}")
