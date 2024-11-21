from datetime import datetime
from enum import Enum

from sqlalchemy import Enum as ORMEnum, Column, Integer, Float, Date, UniqueConstraint
from sqlalchemy.orm import Mapped

from .base import Base

__all__ = (
    "CargoType",
    "Tariff",
)


class CargoType(Enum):
    other = "Other"
    glass = "Glass"


class Tariff(Base):
    __tablename__ = "tariffs"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cargo_type: Mapped[CargoType] = Column(ORMEnum(CargoType), nullable=False)
    date: Mapped[datetime.date] = Column(Date, nullable=False)
    rate: Mapped[float] = Column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint('cargo_type', 'date', name='_cargo_type_date_uc'),
    )
