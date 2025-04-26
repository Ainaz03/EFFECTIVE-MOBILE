from database import engine, BaseModel
from models import *

# Создание всех таблиц в базе данных
BaseModel.metadata.create_all(bind=engine)

print("Таблицы успешно созданы!")