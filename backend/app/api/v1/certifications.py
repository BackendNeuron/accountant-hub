
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.certification import Certification

router = APIRouter()


@router.get("")
async def list_certifications(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Certification).where(Certification.is_active == True)
    )
    return {"data": result.scalars().all()}
