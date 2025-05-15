import time
import logging
from Sync_parser.parser.main import find_and_process_new_file
from Sync_parser.sync_database import BaseModel, engine

logging.basicConfig(
    filename='parser.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

def initialize_database():
    try:
        BaseModel.metadata.create_all(bind=engine)
        logging.info("База данных и таблицы успешно инициализированы.")
    except Exception as e:
        logging.error(f"Ошибка при инициализации базы данных: {e}")
        raise

def main():
    logging.info("Запуск парсера...")

    initialize_database()

    while True:
        process = find_and_process_new_file()

        if not process:
            logging.info("Новых файлов не найдено. Завершение работы.")
            break

        logging.info("Обнаружен и обработан новый файл. Повторная проверка...")

if __name__ == '__main__':
    main()