import asyncio
import logging
from Async_parser.parser.extractor import find_new_excel_link_from_all_pages, extract_filename
from Async_parser.parser.file_manager import download_file_from_url
from Async_parser.parser.file_processor import process_file
from Async_parser.parser.database_tools import save_processedfile_to_db
from Async_parser.async_database import async_session
import aiohttp

logging.basicConfig(
    filename='parser.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)


async def find_and_process_new_file():
    async with async_session() as session:
        async with aiohttp.ClientSession() as http:
            new_url = await find_new_excel_link_from_all_pages(session, http)
            if not new_url:
                return False

            filename = extract_filename(new_url)
            if not filename:
                return False

            path = await download_file_from_url(new_url)
            if not path:
                return False

            ok = await process_file(session, filename)
            if ok:
                await save_processedfile_to_db(session, new_url, filename)
                logging.info(f"Файл {filename} успешно обработан.")
                return True
    return False


async def async_main():
    logging.info("Запуск асинхронного парсера...")
    while True:
        if not await find_and_process_new_file():
            logging.info("Новых файлов не найдено. Завершение.")
            break
        logging.info("Обработан файл — продолжаем проверку...")


if __name__ == '__main__':
    asyncio.run(async_main())
