import pytest
from sqlalchemy import select
from models.spimextradingresult import SpimexTradingResult

from backend.db import get_db


@pytest.mark.asyncio
async def test_get_db():
    agen = get_db()
    async for db in agen:
        result = await db.execute(select(SpimexTradingResult))
        assert result is not None
        break