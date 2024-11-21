import datetime

from pydantic import BaseModel, Field

from models.tariffs import CargoType

__all__ = (
    "MINIMAL_RATE",
    "CargoRate",
    "CreateTariffRequest",
    "UpdateTariffRequest",
    "TariffResponse",
)

MINIMAL_RATE: float = 0.00001


class CargoRate(BaseModel):
    cargo_type: CargoType
    rate: float = Field(..., ge=MINIMAL_RATE)


class CreateTariffRequest(BaseModel):
    cargo_type: CargoType
    rate: float = Field(..., ge=MINIMAL_RATE)
    date: datetime.date = Field(default_factory=datetime.date.today)


class UpdateTariffRequest(BaseModel):
    cargo_type: CargoType | None = None
    rate: float | None = Field(None, ge=MINIMAL_RATE)


class TariffResponse(BaseModel):
    id: int
    cargo_type: CargoType
    date: datetime.date
    rate: float = Field(..., ge=MINIMAL_RATE)
