import pytest
from datetime import date, datetime, timedelta
from pydantic import ValidationError

from schemas.tradingdate import TradingDate
from schemas.tradingresult import TradingResult


def test_tradingdate_valid():
    td = TradingDate(date=date(2025, 5, 28))
    assert isinstance(td.date, date)
    assert td.date == date(2025, 5, 28)


@pytest.mark.parametrize("bad", [
    {},
    {"date": "not-a-date"},
    {"date": 123},
])
def test_tradingdate_invalid(bad):
    with pytest.raises(ValidationError):
        TradingDate(**bad)


def make_valid_trading_result():
    return {
        "id": 1,
        "exchange_product_id": "A692BLL005A",
        "exchange_product_name": "Бензин",
        "oil_id": "A692",
        "delivery_basis_id": "BLL",
        "delivery_basis_name": "Basis Name",
        "delivery_type_id": "A",
        "volume": 123.45,
        "total": 6789.01,
        "count": 5,
        "date": date(2025, 5, 28),
        "created_on": datetime(2025, 5, 28, 12, 0, 0),
        "updated_on": datetime(2025, 5, 28, 13, 0, 0),
    }


def test_tradingresult_valid():
    data = make_valid_trading_result()
    tr = TradingResult(**data)

    assert tr.id == data["id"]
    assert tr.exchange_product_id == data["exchange_product_id"]
    assert tr.volume == data["volume"]
    assert isinstance(tr.date, date)
    assert isinstance(tr.created_on, datetime)
    assert isinstance(tr.updated_on, datetime)


@pytest.mark.parametrize("field,value", [
    ("id", None),
    ("exchange_product_id", 123),
    ("volume", "abc"),
    ("date", "2025-13-01"),
    ("created_on", "bad-date"),
    ("updated_on", None),
])
def test_tradingresult_invalid_types(field, value):
    data = make_valid_trading_result()
    data[field] = value
    with pytest.raises(ValidationError):
        TradingResult(**data)


def test_tradingresult_date_order():
    data = make_valid_trading_result()

    data["created_on"] = datetime.combine(data["date"] + timedelta(days=2), datetime.min.time())

    tr = TradingResult(**data)
    assert tr.created_on.date() > tr.date
