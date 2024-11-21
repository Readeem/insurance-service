import datetime

from pydantic import BaseModel, Field

from models import CargoType

__all__ = (
    "InsuranceRequest",
    "InsuranceResponse",
)


class InsuranceRequest(BaseModel):
    cargo_type: CargoType
    declared_value: float
    date: datetime.date = Field(default_factory=datetime.date.today)
    # timezone: datetime.timezone | None = None


class InsuranceResponse(BaseModel):
    price: float
