import pytest
from unittest.mock import patch, AsyncMock

from httpx import AsyncClient, ASGITransport
from fastapi import status

from main import app
from routers.trading import router


@patch("backend.cache.redis_client.get", new_callable=AsyncMock)
@patch("backend.cache.redis_client.set", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_get_last_trading_dates(mock_redis_set, mock_redis_get):
    mock_redis_get.return_value = None

    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url='http://test') as ac:
        response = await ac.get(f'/trading/last_dates?count=5')
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 5



@patch("backend.cache.redis_client.get", new_callable=AsyncMock)
@patch("backend.cache.redis_client.set", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_get_dynamics(mock_redis_set, mock_redis_get):
    mock_redis_get.return_value = None

    params = {
        "start_date": "2023-01-01",
        "end_date": "2023-01-10",
        "oil_id": "BRN",
        "delivery_type_id": "FOB",
        "delivery_basis_id": "CIF"
    }

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/trading/dynamics", params=params)
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert isinstance(data, list)
        if data:
            item = data[0]
            assert "date" in item
            assert "oil_id" in item


@patch("backend.cache.redis_client.get", new_callable=AsyncMock)
@patch("backend.cache.redis_client.set", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_get_trading_results(mock_redis_set, mock_redis_get):
    mock_redis_get.return_value = None

    params = {
        "oil_id": "BRN",
        "delivery_type_id": "FOB",
        "delivery_basis_id": "CIF"
    }

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/trading/results", params=params)
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert isinstance(data, list)
        if data:
            item = data[0]
            assert "date" in item
            assert "oil_id" in item
