
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.database import get_db
from app.models.platform_content import PlatformContent

router = APIRouter()


@router.get("/{key}")
async def get_content(key: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(PlatformContent).where(
            PlatformContent.key == key,
            PlatformContent.is_active == True
        )
    )
    content = result.scalar_one_or_none()
    if not content:
        raise HTTPException(404, "Content not found")
    return {"data": content}
