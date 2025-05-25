from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from backend.db import Base


class SpimexTradingResult(Base):
    __tablename__ = 'spimex_trading_results'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    exchange_product_id: Mapped[str] = mapped_column()
    exchange_product_name: Mapped[str] = mapped_column()
    oil_id: Mapped[str] = mapped_column()
    delivery_basis_id: Mapped[str] = mapped_column()
    delivery_basis_name: Mapped[str] = mapped_column()
    delivery_type_id: Mapped[str] = mapped_column()
    volume: Mapped[float] = mapped_column()
    total: Mapped[float] = mapped_column()
    count: Mapped[int] = mapped_column()
    date: Mapped[str] = mapped_column()
    created_on: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    updated_on: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=func.now(), nullable=False)
