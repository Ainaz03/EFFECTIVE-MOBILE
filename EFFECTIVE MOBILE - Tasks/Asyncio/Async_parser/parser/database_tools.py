from datetime import datetime
from Async_parser.models import ProcessedFile, SpimexTradingResult
from Async_parser.parser.logger import logger
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from urllib.parse import urlparse


async def is_file_already_processed(session, urlname: str) -> bool:
    clean = urlparse(urlname).path
    result = await session.execute(
        select(ProcessedFile).where(
            ProcessedFile.urlname == clean,
            ProcessedFile.isprocessed == True
        )
    )
    return result.scalars().first() is not None


async def save_processedfile_to_db(session, urlname: str, filename: str) -> None:
    try:
        clean = urlparse(urlname).path

        exists = await session.execute(
            select(ProcessedFile).where(ProcessedFile.filename == filename)
        )
        if exists.scalars().first() is None:
            new_file = ProcessedFile(
                filename=filename,
                urlname=clean,
                isprocessed=True,
                processed_on=datetime.utcnow()
            )
            session.add(new_file)
            await session.commit()
            logger.info(f"Файл {filename} успешно добавлен в processed_files.")
    except SQLAlchemyError as e:
        await session.rollback()
        logger.error(f"[Ошибка] Ошибка при добавлении файла в processed_files: {e}")
        raise


async def save_spimextradingresult_to_db(session, records: list) -> bool:
    if not records:
        logger.warning("Нет данных для сохранения.")
        return False

    try:
        await session.execute(
            SpimexTradingResult.__table__.insert(),
            records
        )
        await session.commit()
        logger.info("Данные успешно сохранены.")
        return True
    except SQLAlchemyError as e:
        await session.rollback()
        logger.error(f"[Ошибка] Ошибка сохранения в БД: {e}")
        raise
