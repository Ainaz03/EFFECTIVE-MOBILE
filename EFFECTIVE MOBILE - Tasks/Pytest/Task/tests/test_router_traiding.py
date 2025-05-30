import pytest
from unittest.mock import patch, AsyncMock

from httpx import AsyncClient, ASGITransport
from fastapi import status

from main import app
from routers.trading import router


@pytest.mark.asyncio
async def test_get_last_trading_dates(async_client, fake_redis):
    response = await async_client.get('/trading/last_dates?count=5')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 5


@pytest.mark.asyncio
async def test_get_dynamics(async_client, fake_redis):
    params = {
        "start_date": "2023-01-01",
        "end_date": "2023-01-10",
        "oil_id": "BRN",
        "delivery_type_id": "FOB",
        "delivery_basis_id": "CIF"
    }

    response = await async_client.get("/trading/dynamics", params=params)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert isinstance(data, list)
    if data:
        item = data[0]
        assert "date" in item
        assert "oil_id" in item


@pytest.mark.asyncio
async def test_get_trading_results(async_client, fake_redis):
    params = {
        "oil_id": "BRN",
        "delivery_type_id": "FOB",
        "delivery_basis_id": "CIF"
    }

    response = await async_client.get("/trading/results", params=params)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert isinstance(data, list)
    if data:
        item = data[0]
        assert "date" in item
        assert "oil_id" in item
