from pydantic import BaseModel, ConfigDict
from datetime import date, datetime


class TradingResult(BaseModel):
    id:               int
    exchange_product_id:   str
    exchange_product_name: str
    oil_id:           str
    delivery_basis_id:     str
    delivery_basis_name:   str
    delivery_type_id:      str
    volume:           float
    total:            float
    count:            int
    date:             date
    created_on:       datetime
    updated_on:       datetime

    model_config = ConfigDict(from_attributes=True)
