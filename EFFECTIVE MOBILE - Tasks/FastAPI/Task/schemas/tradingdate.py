from pydantic import BaseModel, ConfigDict
from datetime import date


class TradingDate(BaseModel):
    date: date

    model_config = ConfigDict(from_attributes=True)
