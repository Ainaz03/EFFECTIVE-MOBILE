import time
import logging
import asyncio

from Async_parser.async_database import BaseModel, engine
from Async_parser.parser.main import async_main

logging.basicConfig(
    filename='parser.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)


async def init_db():
    """
    Асинхронно сбрасывает и пересоздаёт все таблицы.
    """
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    logging.info("БД очищена и структура пересоздана.")


async def runner():
    await init_db()

    start = time.perf_counter()
    await async_main()
    duration = time.perf_counter() - start
    logging.info(f"Асинхронный парсер завершился за {duration:.2f} сек.")
    print(f"Async time: {duration:.2f} sec")

    await engine.dispose()
    logging.info("Пул соединений закрыт.")


def main():
    asyncio.run(runner())


if __name__ == '__main__':
    main()
