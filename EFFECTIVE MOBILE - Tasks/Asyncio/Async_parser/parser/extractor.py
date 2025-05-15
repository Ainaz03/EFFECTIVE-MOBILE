import re
from urllib.parse import urlparse

import aiohttp
from Async_parser.parser.constants import BASE_URL, FILE_URL_REGEX
from Async_parser.parser.database_tools import is_file_already_processed
from Async_parser.parser.logger import logger


def get_page_url(page_num: int) -> str:
    return BASE_URL if page_num == 1 else f"{BASE_URL}?page=page-{page_num}"


def normalize_url(url: str) -> str:
    """
    Обрезает все query-параметры и возвращает только путь.
    """
    parsed = urlparse(url)
    return parsed.path


def extract_file_urls(html: str) -> list[str]:
    matches = re.findall(FILE_URL_REGEX, html)
    raw = [m[0] if isinstance(m, tuple) else m for m in matches]
    return [normalize_url(u) for u in raw]


def extract_filename(file_url: str) -> str | None:
    m = re.search(r'oil_xls_(\d{14})\.xls', file_url)
    return m.group(0) if m else None


def is_file_from_2023_or_later(file_url: str) -> bool:
    m = re.search(r'oil_xls_(\d{14})\.xls', file_url)
    if not m:
        return False
    year = int(m.group(1)[:4])
    return year >= 2023


async def fetch_page_content(http_session: aiohttp.ClientSession, page_url: str) -> str | None:
    try:
        async with http_session.get(page_url) as resp:
            resp.raise_for_status()
            return await resp.text()
    except Exception as e:
        logger.error(f"Ошибка при загрузке страницы {page_url}: {e}")
        return None


async def find_new_excel_link_from_all_pages(db_session, http_session: aiohttp.ClientSession) -> str | bool:
    page_num = 1

    while True:
        page_url = get_page_url(page_num)
        html = await fetch_page_content(http_session, page_url)
        if not html:
            return False

        for file_url in extract_file_urls(html):
            if (is_file_from_2023_or_later(file_url)
                    and not await is_file_already_processed(db_session, file_url)):
                logger.info(f"Найдена новая ссылка: {file_url}")
                return file_url

        logger.info(f"Страница {page_num}: новых ссылок не найдено, продолжаем...")
        page_num += 1
