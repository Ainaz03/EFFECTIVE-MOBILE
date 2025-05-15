from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Sync_parser.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
import logging

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

BaseModel = declarative_base()

try:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    logging.info(f"Успешно подключено к базе данных: {DB_NAME}")
except Exception as e:
    logging.error(f"Ошибка при подключении к базе данных: {e}")
    raise

Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

BaseModel.metadata.create_all(bind=engine)