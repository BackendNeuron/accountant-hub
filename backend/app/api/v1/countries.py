
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.country import Country

router = APIRouter()


@router.get("")
async def list_countries(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Country).where(Country.is_active == True)
    )
    return {"data": result.scalars().all()}
