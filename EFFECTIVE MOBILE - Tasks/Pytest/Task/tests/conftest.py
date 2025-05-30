import sys, os
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch

from main import app


@pytest.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture
def fake_redis():
    with patch("backend.cache.redis_client.get", new_callable=AsyncMock) as mock_get, \
         patch("backend.cache.redis_client.set", new_callable=AsyncMock) as mock_set:
        mock_get.return_value = None
        yield mock_get, mock_set
