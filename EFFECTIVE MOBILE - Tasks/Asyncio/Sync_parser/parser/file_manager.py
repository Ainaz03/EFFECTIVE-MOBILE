import os
import urllib.request
from Sync_parser.parser.logger import logger
from Sync_parser.parser.extractor import extract_filename
from Sync_parser.parser.constants import BASE_BASE_URL

DOWNLOAD_DIR = "downloads"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)



def download_file_from_url(file_url: str) -> str:
    if file_url.startswith("/"):
        file_url = BASE_BASE_URL + file_url

    file_path = os.path.join(DOWNLOAD_DIR, extract_filename(file_url))
    
    try:
        urllib.request.urlretrieve(file_url, file_path)
        logger.info(f"Файл загружен: {file_path}")
        return file_path
    except Exception as e:
        logger.error(f"[Ошибка] Не удалось скачать файл {file_url}: {e}")
        raise


def is_file_exist(file_path: str) -> bool:
    if not os.path.exists(file_path):
        logger.error(f"Файл {file_path} не найден.")
        return False
    return True


def delete_file(file_path: str):
    try:
        os.remove(file_path)
        logger.info(f"Файл успешно удалён после обработки.")
    except Exception as e:
        logger.warning(f"Не удалось удалить файл: {e}")