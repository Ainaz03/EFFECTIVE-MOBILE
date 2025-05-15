import os
from urllib.parse import urljoin

import aiofiles
import aiohttp
from Async_parser.parser.constants import BASE_BASE_URL, DOWNLOAD_DIR
from Async_parser.parser.extractor import extract_filename
from Async_parser.parser.logger import logger

os.makedirs(DOWNLOAD_DIR, exist_ok=True)


async def download_file_from_url(file_url: str) -> str:
    if file_url.startswith("/"):
        file_url = urljoin(BASE_BASE_URL, file_url)

    filename = extract_filename(file_url)
    if not filename:
        raise ValueError(f"Не удалось извлечь имя файла из URL {file_url}")

    file_path = os.path.join(DOWNLOAD_DIR, filename)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(file_url) as resp:
                resp.raise_for_status()
                async with aiofiles.open(file_path, "wb") as f:
                    async for chunk in resp.content.iter_chunked(1024):
                        await f.write(chunk)

        logger.info(f"Файл загружен: {file_path}")
        return file_path

    except Exception as e:
        logger.error(f"[Ошибка] Не удалось скачать файл {file_url}: {e}")
        raise


def is_file_exist(file_path: str) -> bool:
    exists = os.path.exists(file_path)
    if not exists:
        logger.error(f"Файл {file_path} не найден.")
    return exists


def delete_file(file_path: str):
    try:
        os.remove(file_path)
        logger.info(f"Файл успешно удалён после обработки.")
    except Exception as e:
        logger.warning(f"Не удалось удалить файл: {e}")
