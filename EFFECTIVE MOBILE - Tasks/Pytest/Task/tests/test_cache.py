import pytest
from datetime import datetime
import backend.cache as cache_mod

@pytest.mark.parametrize("now, expected_delta", [
    (
        datetime(2025, 5, 28, 13, 0),
        datetime(2025, 5, 28, 14, 11) - datetime(2025, 5, 28, 13, 0)
    ),
    (
        datetime(2025, 5, 28, 14, 11),
        datetime(2025, 5, 29, 14, 11) - datetime(2025, 5, 28, 14, 11)
    ),
    (
        datetime(2025, 5, 28, 15, 0),
        datetime(2025, 5, 29, 14, 11) - datetime(2025, 5, 28, 15, 0)
    ),
])
def test_seconds_until_reset(monkeypatch, now, expected_delta):
    class FakeDateTime(datetime):
        @classmethod
        def now(cls, tz=None):
            return now

    monkeypatch.setattr(cache_mod, "datetime", FakeDateTime)

    secs = cache_mod.seconds_until_reset()
    assert isinstance(secs, int)
    assert secs == int(expected_delta.total_seconds())
