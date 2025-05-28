from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import json

from backend.cache import redis_client, seconds_until_reset
from backend.db import get_db
from models.spimextradingresult import SpimexTradingResult
from schemas.tradingdate import TradingDate
from schemas.tradingresult import TradingResult

router = APIRouter(prefix='/trading', tags=['Трейдинг'])

@router.get('/last_dates', response_model=List[TradingDate],
    summary="Список последних торговых дат")
async def get_last_trading_dates(
    db: Annotated[AsyncSession, Depends(get_db)],
    # Обязательный параметр: без count не поймём, сколько дат вернуть
    count: Annotated[int, Query(..., gt=0, description="Количество дат (>0)")]):

    cache_key = f"last_dates:{count}"
    cached = await redis_client.get(cache_key)
    if cached:
        return [TradingDate(**item) for item in json.loads(cached)]

    stmt = (
        select(SpimexTradingResult.date)
        .distinct()
        .order_by(SpimexTradingResult.date.desc())
        .limit(count)
    )
    result = await db.execute(stmt)
    dates = result.scalars().all()
    payload = [ {"date": d} for d in dates ]

    await redis_client.set(cache_key, json.dumps(payload), ex=seconds_until_reset())

    return [TradingDate(**item) for item in payload]


@router.get('/dynamics', response_model=List[TradingResult],
    summary="Динамика торгов за период"
)
async def get_dynamics(
    db: Annotated[AsyncSession, Depends(get_db)],
    # Параметры start_date и end_date — обязательны, иначе непонятен период
    start_date: Annotated[str, Query(..., description="Дата начала YYYY-MM-DD")],
    end_date:   Annotated[str, Query(..., description="Дата конца YYYY-MM-DD")],
    # Остальные параметры — опциональны, т.к. фильтрация по ним нужна только при запросе конкретных выборок
    oil_id: Optional[str]           = Query(None, description="Код нефти"),
    delivery_type_id: Optional[str] = Query(None, description="Тип поставки"),
    delivery_basis_id: Optional[str]= Query(None, description="Условие поставки"),
):
    cache_key = f"dynamics:{start_date}:{end_date}:{oil_id or ''}:{delivery_type_id or ''}:{delivery_basis_id or ''}"
    cached = await redis_client.get(cache_key)
    if cached:
        return [TradingResult(**item) for item in json.loads(cached)]

    stmt = select(SpimexTradingResult).where(
        SpimexTradingResult.date >= start_date,
        SpimexTradingResult.date <= end_date
    )
    if oil_id:
        stmt = stmt.where(SpimexTradingResult.oil_id == oil_id)
    if delivery_type_id:
        stmt = stmt.where(SpimexTradingResult.delivery_type_id == delivery_type_id)
    if delivery_basis_id:
        stmt = stmt.where(SpimexTradingResult.delivery_basis_id == delivery_basis_id)

    stmt = stmt.order_by(SpimexTradingResult.date.asc())
    result = await db.execute(stmt)
    records = result.scalars().all()

    payload = [r.__dict__ for r in records]

    await redis_client.set(cache_key, json.dumps(payload), ex=seconds_until_reset())

    return [TradingResult(**item) for item in payload]


@router.get('/results', response_model=List[TradingResult],
    summary="Последние торговые результаты"
)
async def get_trading_results(
    db: Annotated[AsyncSession, Depends(get_db)],
    # Здесь всё опционально: если нет фильтров — отдаём все данные
    oil_id: Optional[str]           = Query(None, description="Код нефти"),
    delivery_type_id: Optional[str] = Query(None, description="Тип поставки"),
    delivery_basis_id: Optional[str]= Query(None, description="Условие поставки"),
):
    cache_key = f"results:{oil_id or ''}:{delivery_type_id or ''}:{delivery_basis_id or ''}"
    cached = await redis_client.get(cache_key)
    if cached:
        return [TradingResult(**item) for item in json.loads(cached)]

    stmt = select(SpimexTradingResult)
    if oil_id:
        stmt = stmt.where(SpimexTradingResult.oil_id == oil_id)
    if delivery_type_id:
        stmt = stmt.where(SpimexTradingResult.delivery_type_id == delivery_type_id)
    if delivery_basis_id:
        stmt = stmt.where(SpimexTradingResult.delivery_basis_id == delivery_basis_id)

    stmt = stmt.order_by(SpimexTradingResult.date.desc())
    result = await db.execute(stmt)
    records = result.scalars().all()

    payload = [r.__dict__ for r in records]

    await redis_client.set(cache_key, json.dumps(payload), ex=seconds_until_reset())

    return [TradingResult(**item) for item in payload]
