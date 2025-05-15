from datetime import datetime
from Sync_parser.models import ProcessedFile, SpimexTradingResult
from Sync_parser.parser.logger import logger

def is_file_already_processed(session, urlname: str) -> bool:
    return session.query(ProcessedFile).filter_by(urlname=urlname, isprocessed=True).first() is not None


def save_processedfile_to_db(session, urlname: str, filename: str) -> None:
    try:
        if not session.query(ProcessedFile).filter_by(filename=filename).first():
            new_file = ProcessedFile(
                filename=filename,
                urlname=urlname,
                isprocessed=True,
                processed_on=datetime.utcnow()
            )
            session.add(new_file)
            session.commit()
            logger.info(f"Файл {filename} успешно добавлен в processed_files.")
        
    except Exception as e:
        session.rollback()
        logger.error(f"[Ошибка] Ошибка при добавлении файла в processed_files: {e}")
        raise


def save_spimextradingresult_to_db(session, records: list) -> bool:
    if records:
        try:
            session.bulk_insert_mappings(SpimexTradingResult, records)
            session.commit()
            logger.info(f"Данные успешно сохранены.")
            return True
        except Exception as e:
            session.rollback()
            logger.error(f"[Ошибка] Ошибка сохранения в БД: {e}")
            raise
    else:
        logger.warning(f"Нет данных для сохранения.")
        return False
