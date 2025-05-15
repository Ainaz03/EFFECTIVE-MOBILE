import re
import urllib.request
import time
from Sync_parser.parser.constants import BASE_URL, FILE_URL_REGEX
from Sync_parser.parser.database_tools import is_file_already_processed
from Sync_parser.parser.logger import logger
from urllib.parse import urlparse

def find_new_excel_link_from_all_pages(session):
    page_num = 1

    while True:
        page_url = get_page_url(page_num)
        html = fetch_page_content(page_url)
        if not html:
            logger.error(f"Ошибка при загрузке {page_url}")
            return False

        file_urls = extract_file_urls(html)
        if not file_urls:
            logger.info("Нет больше XLS ссылок.")
            return False

        for file_url in file_urls:
            if is_file_from_2023_or_later(file_url) and not is_file_already_processed(session, file_url):
                logger.info(f"Найдена новая ссылка: {file_url}")
                return file_url

        page_num += 1


def get_page_url(page_num: int) -> str:
    return BASE_URL if page_num == 1 else f"{BASE_URL}?page=page-{page_num}"


def fetch_page_content(page_url: str) -> str:
    try:
        with urllib.request.urlopen(page_url) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        return None


def extract_file_urls(html: str) -> list:
    matches = re.findall(FILE_URL_REGEX, html)
    urls = [clean_url(m[0]) if isinstance(m, tuple) else clean_url(m) for m in matches]
    return urls


def clean_url(url: str) -> str:
    parsed_url = urlparse(url)
    return parsed_url.path


def extract_filename(file_url: str) -> str:
    filename_match = re.search(r'oil_xls_\d{14}\.xls', file_url)
    if filename_match:
        return filename_match.group(0)
    return None


def is_file_from_2023_or_later(file_url: str) -> bool:
    match = re.search(r'oil_xls_(\d{14})\.xls', file_url)
    if not match:
        return False

    date_str = match.group(1)
    year = int(date_str[:4])

    return year >= 2023
