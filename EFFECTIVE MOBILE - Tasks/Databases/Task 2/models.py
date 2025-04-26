from database import BaseModel
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func

class SpimexTradingResult(BaseModel):
    __tablename__ = "spimex_trading_results"

    id = Column(Integer, primary_key=True, index=True)
    exchange_product_id = Column(String, index=True)
    exchange_product_name = Column(String)
    oil_id = Column(String)
    delivery_basis_id = Column(String)
    delivery_basis_name = Column(String)
    delivery_type_id = Column(String)
    volume = Column(Float)
    total = Column(Float)
    count = Column(Integer)
    date = Column(String)
    created_on = Column(DateTime, default=func.now(), nullable=False)
    updated_on = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

class ProcessedFile(BaseModel):
    __tablename__ = 'processed_files'

    id = Column(Integer, primary_key=True)
    filename = Column(String, unique=True, nullable=False, index=True)  # добавлен индекс для улучшения производительности поиска
    urlname = Column(String, unique=True, nullable=False)
    processed_on = Column(DateTime, default=func.now(), nullable=False)
    isprocessed = Column(Boolean, nullable=False)