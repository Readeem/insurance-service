import datetime
import logging
from collections.abc import Sequence

from fastapi import APIRouter, HTTPException
from fastapi.params import Query, Depends
from pydantic import RootModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from dto.tariffs import TariffResponse, CreateTariffRequest, UpdateTariffRequest, CargoRate
from middlewares.database import database
from models import Tariff

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/tariffs", tags=["tariffs"])
async def create_tariff(
    data: CreateTariffRequest,
    db: AsyncSession = Depends(database),
) -> TariffResponse:
    """Create a new tariff."""
    # models can be initialized with keyword arguments but pycharm complains
    # noinspection PyArgumentList
    new_tariff = Tariff(
        cargo_type=data.cargo_type,
        rate=data.rate,
        date=data.date,
    )
    db.add(new_tariff)

    try:
        await db.commit()
    except IntegrityError:
        raise HTTPException(400, detail="Tariff with such date and type already exists")

    await db.refresh(new_tariff)

    return TariffResponse(
        id=new_tariff.id,
        cargo_type=new_tariff.cargo_type,
        date=new_tariff.date,
        rate=new_tariff.rate,
    )


@router.post("/tariffs/batch", tags=["tariffs"])
async def create_tariffs_batch(
    data: RootModel[dict[datetime.date, list[CargoRate]]],
    db: AsyncSession = Depends(database),
) -> None:
    """Create a new tariffs with batch data request."""
    for date, tariffs in data.root.items():
        for tariff in tariffs:
            # noinspection PyArgumentList
            db.add(
                Tariff(
                    cargo_type=tariff.cargo_type,
                    rate=tariff.rate,
                    date=date,
                )
            )
    try:
        await db.commit()
    except IntegrityError:
        raise HTTPException(400, detail="Some tariffs must not be already present")


@router.get("/tariffs", tags=["tariffs"])
async def get_tariffs(
    db: AsyncSession = Depends(database),
    limit: int = Query(50),
    offset: int = Query(0),
) -> list[TariffResponse]:
    """Retrieve all available tariffs."""
    stmt = select(Tariff).limit(limit).offset(offset)
    try:
        results: Sequence[Tariff] = (await db.execute(stmt)).scalars().all()
    except Exception as e:
        logger.error("Unknown database error", exc_info=e)
        raise HTTPException(500)

    return [
        TariffResponse(
            id=tariff.id,
            cargo_type=tariff.cargo_type,
            date=tariff.date,
            rate=tariff.rate,
        )
        for tariff in results
    ]


@router.get("/tariffs/{id}", tags=["tariffs"])
async def get_tariff(
    id: int,
    db: AsyncSession = Depends(database),
) -> TariffResponse:
    """Retrieve a specific tariff."""
    stmt = select(Tariff).where(Tariff.id == id)
    try:
        tariff: Tariff | None = (await db.execute(stmt)).scalar()
    except Exception as e:
        logger.error("Unknown database error", exc_info=e)
        raise HTTPException(500)

    if tariff is None:
        raise HTTPException(404, detail=f"Tariff with id {id} not found")

    return TariffResponse(
        id=tariff.id,
        cargo_type=tariff.cargo_type,
        date=tariff.date,
        rate=tariff.rate,
    )


@router.patch("/tariffs/{id}", tags=["tariffs"])
async def update_tariff(
    id: int,
    data: UpdateTariffRequest,
    db: AsyncSession = Depends(database),
) -> TariffResponse:
    """Update a specific tariff."""
    if data.cargo_type is None and data.rate is None:
        raise HTTPException(400, detail="At least one of 'cargo_type' and 'rate' are required")

    stmt = select(Tariff).where(Tariff.id == id)
    try:
        tariff: Tariff | None = (await db.execute(stmt)).scalar()
    except Exception as e:
        logger.error("Unknown database error", exc_info=e)
        raise HTTPException(500)

    if tariff is None:
        raise HTTPException(404, detail=f"Tariff with id {id} not found")

    if data.cargo_type is not None:
        tariff.cargo_type = data.cargo_type
    if data.rate is not None:
        tariff.rate = data.rate

    await db.commit()

    return TariffResponse(
        id=tariff.id,
        cargo_type=tariff.cargo_type,
        date=tariff.date,
        rate=tariff.rate,
    )


@router.delete("/tariffs/{id}", tags=["tariffs"])
async def delete_tariff(
    id: int,
    db: AsyncSession = Depends(database),
) -> TariffResponse:
    """Delete a specific tariff."""
    stmt = select(Tariff).where(Tariff.id == id)
    try:
        tariff: Tariff | None = (await db.execute(stmt)).scalar()
    except Exception as e:
        logger.error("Unknown database error", exc_info=e)
        raise HTTPException(500)

    if tariff is None:
        raise HTTPException(404, detail=f"Tariff with id {id} not found")

    await db.delete(tariff)
    await db.commit()

    return TariffResponse(
        id=tariff.id,
        cargo_type=tariff.cargo_type,
        date=tariff.date,
        rate=tariff.rate,
    )
