from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from Async_parser.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
import logging

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

BaseModel = declarative_base()


try:
    engine = create_async_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
    logging.info(f"Успешно подключено к базе данных: {DB_NAME}")
except Exception as e:
    logging.error(f"Ошибка при подключении к базе данных: {e}")
    raise


async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
