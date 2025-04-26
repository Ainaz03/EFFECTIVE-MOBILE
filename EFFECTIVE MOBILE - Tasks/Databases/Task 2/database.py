from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
import logging

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

BaseModel = declarative_base()

# Создание подключения к базе данных с обработкой ошибок
try:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    logging.info(f"Успешно подключено к базе данных: {DB_NAME}")
except Exception as e:
    logging.error(f"Ошибка при подключении к базе данных: {e}")
    raise  # Перебрасываем исключение, если подключение не удалось

Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Создание всех таблиц, если они еще не существуют
BaseModel.metadata.create_all(bind=engine)