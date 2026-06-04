
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.database import get_db
from app.api.deps import require_role
from app.models.platform_content import PlatformContent
from app.schemas.platform_content import PlatformContentUpdateRequest
from datetime import datetime

router = APIRouter()


@router.get("")
async def list_content(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(PlatformContent).order_by(PlatformContent.key))
    return {"data": result.scalars().all()}


@router.get("/{content_id}")
async def get_content(
    content_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(PlatformContent).where(PlatformContent.id == content_id))
    content = result.scalar_one_or_none()
    if not content:
        raise HTTPException(404, "Content not found")
    return {"data": content}


@router.put("/{content_id}")
async def update_content(
    content_id: int,
    request: PlatformContentUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(PlatformContent).where(PlatformContent.id == content_id))
    content = result.scalar_one_or_none()
    if not content:
        raise HTTPException(404, "Content not found")
    for key, value in request.model_dump(exclude_none=True).items():
        setattr(content, key, value)
    content.updated_by = current_user.id
    content.published_at = datetime.utcnow()
    await db.flush()
    return {"message": "Content updated"}
