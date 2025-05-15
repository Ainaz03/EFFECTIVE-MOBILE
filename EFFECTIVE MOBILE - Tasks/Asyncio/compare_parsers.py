import time
import asyncio
import logging

from Sync_parser.sync_database import BaseModel, engine as syncengine
from Sync_parser.parser.main import find_and_process_new_file as sync_find_file

from Async_parser.async_database import BaseModel as AsyncBaseModel, engine as asyncengine
from Async_parser.parser.main import find_and_process_new_file as async_find_file


# ---------------- Инициализация БД ----------------

def init_db_sync():
    try:
        logging.info("[SYNC] Инициализация БД...")
        BaseModel.metadata.drop_all(bind=syncengine)
        BaseModel.metadata.create_all(bind=syncengine)
        logging.info("[SYNC] БД инициализирована.")
    except Exception as e:
        logging.error(f"[SYNC][Ошибка] {e}")
        raise

async def init_db_async():
    try:
        logging.info("[ASYNC] Инициализация БД...")
        async with asyncengine.begin() as conn:
            await conn.run_sync(AsyncBaseModel.metadata.drop_all)
            await conn.run_sync(AsyncBaseModel.metadata.create_all)
        logging.info("[ASYNC] БД инициализирована.")
    except Exception as e:
        logging.error(f"[ASYNC][Ошибка] {e}")
        raise


# ---------------- Парсинг ----------------

def run_sync(n_files=10):
    print("[SYNC] Очистка базы данных...")
    init_db_sync()

    results = []
    print(f"[SYNC] Обработка {n_files} файлов...")

    for i in range(n_files):
        start = time.perf_counter()
        processed = sync_find_file()
        end = time.perf_counter()

        if not processed:
            print(f"[SYNC] Недостаточно новых файлов, обработано: {i}")
            break

        duration = end - start
        results.append(duration)
        print(f"[SYNC] Файл {i+1} обработан за {duration:.2f} сек.")

    return results

async def run_async(n_files=10):
    print("[ASYNC] Очистка базы данных...")
    await init_db_async()

    results = []
    print(f"[ASYNC] Обработка {n_files} файлов...")

    for i in range(n_files):
        start = time.perf_counter()
        processed = await async_find_file()
        end = time.perf_counter()

        if not processed:
            print(f"[ASYNC] Недостаточно новых файлов, обработано: {i}")
            break

        duration = end - start
        results.append(duration)
        print(f"[ASYNC] Файл {i+1} обработан за {duration:.2f} сек.")

    return results


# ---------------- Запись результатов ----------------

def write_results(sync_times, async_times, output_file='comparison_results.txt'):
    max_len = max(len(sync_times), len(async_times))
    lines = []

    lines.append("+----------------------+------------+------------+")
    lines.append("|     Файл №           |   SYNC     |   ASYNC    |")
    lines.append("+----------------------+------------+------------+")

    for i in range(max_len):
        s = f"{sync_times[i]:.2f} сек" if i < len(sync_times) else "-"
        a = f"{async_times[i]:.2f} сек" if i < len(async_times) else "-"
        lines.append(f"| Файл {i+1:<14} | {s:<10} | {a:<10} |")

    lines.append("+----------------------+------------+------------+")

    total_sync = sum(sync_times)
    total_async = sum(async_times)
    lines.append(f"| ИТОГО                | {total_sync:.2f} сек | {total_async:.2f} сек |")
    lines.append("+----------------------+----------------------+----------------------+")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\nРезультаты сравнения сохранены в {output_file}")


# ---------------- Точка входа ----------------

def main():
    n_files = 10
    sync_times = run_sync(n_files=n_files)
    async_times = asyncio.run(run_async(n_files=n_files))
    write_results(sync_times, async_times)


if __name__ == '__main__':
    main()
