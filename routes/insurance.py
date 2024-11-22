import logging

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dto.insurance import InsuranceResponse, InsuranceRequest
from middlewares.database import database
from models.tariffs import Tariff

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/insurance", tags=["insurance"])
async def post_insurance(
    data: InsuranceRequest,
    db: AsyncSession = Depends(database),
) -> InsuranceResponse:
    """Retrieves insurance price for the given cargo type and price."""
    stmt = select(Tariff).where(
        Tariff.date == data.date,
        Tariff.cargo_type == data.cargo_type,
    )
    try:
        tariff: Tariff | None = (await db.execute(stmt)).scalar()
    except Exception as e:
        logger.error("Unknown database error", exc_info=e)
        raise HTTPException(500)
    if tariff is None:
        raise HTTPException(404, detail=f"No tariff for date {data.date}")

    return InsuranceResponse(price=data.declared_value * tariff.rate)
