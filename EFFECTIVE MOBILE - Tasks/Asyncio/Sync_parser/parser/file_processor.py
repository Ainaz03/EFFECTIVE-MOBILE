import os
import pandas as pd
from Sync_parser.parser.logger import logger
from Sync_parser.parser.file_manager import is_file_exist, delete_file
from datetime import datetime
from Sync_parser.parser.database_tools import save_spimextradingresult_to_db

DOWNLOAD_DIR = "downloads"

def process_file(session, file_name: str) -> bool:
    file_path = os.path.join(DOWNLOAD_DIR, file_name)

    if not is_file_exist(file_path):
        return False

    try:
        df = read_excel_file(file_path)
        if df is None:
            return False

        df = clean_dataframe(df)
        if df.empty:
            return False

        if not validate_dataframe(df):
            return False

        records = transform_to_records(df)

        if not save_spimextradingresult_to_db(session, records):
            return False

        return True

    except Exception as e:
        handle_processing_error(session, file_name, e)
        return False

    finally:
        delete_file(file_path)



def read_excel_file(file_path: str) -> pd.DataFrame:
    try:
        df = pd.read_excel(file_path, sheet_name=0)
        start_index = df.apply(lambda row: row.astype(str).str.contains("Единица измерения: Метрическая тонна", na=False).any(), axis=1)
        
        if start_index.any():
            start_index_row = start_index.idxmax() + 1
            df = df.iloc[start_index_row:]
            df.columns = df.iloc[0]
            df = df[1:]

        return df
    except Exception as e:
        logger.error(f"[Ошибка] Ошибка при чтении файла {file_path}: {e}")
        return None


def validate_dataframe(df: pd.DataFrame) -> bool:
    if 'Объем Договоров, руб.' not in df.columns:
        logger.warning(f"Столбец 'Объем Договоров, руб.' не найден.")
        return False
    return True


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.replace('\n', ' ').str.strip()

    if 'Количество Договоров, шт.' not in df.columns:
        logger.warning(f"Столбец 'Количество Договоров, шт.' не найден в данных.")
        return df

    df['Количество Договоров, шт.'] = pd.to_numeric(df['Количество Договоров, шт.'], errors='coerce')

    if 'Обьем Договоров, руб.' in df.columns:
        df['Объем Договоров, руб.'] = df['Обьем Договоров, руб.']
        df = df.drop(columns=['Обьем Договоров, руб.'])

    if 'Объем Договоров, руб.' not in df.columns:
        logger.warning(f"Столбец 'Объем Договоров, руб.' не найден в данных.")
        return df

    df = df[df['Количество Договоров, шт.'] > 0]

    return df


def transform_to_records(df: pd.DataFrame) -> list:
    records = []
    for _, row in df.iterrows():
        code = row['Код Инструмента']
        if isinstance(code, str) and len(code) >= 7:
            records.append({
                'exchange_product_id': code,
                'exchange_product_name': row['Наименование Инструмента'],
                'delivery_basis_name': row['Базис поставки'],
                'volume': row['Объем Договоров в единицах измерения'],
                'total': row['Объем Договоров, руб.'],
                'count': row['Количество Договоров, шт.'],
                'oil_id': code[:4],
                'delivery_basis_id': code[4:7],
                'delivery_type_id': code[-1],
                'date': datetime.utcnow().strftime("%Y-%m-%d"),
                'created_on': datetime.utcnow(),
                'updated_on': datetime.utcnow()
            })
    return records


def handle_processing_error(session, filename, error):
    session.rollback()
    logger.exception(f"[Ошибка] Ошибка обработки файла {filename}: {error}")