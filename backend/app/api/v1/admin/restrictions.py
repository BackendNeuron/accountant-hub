
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.database import get_db
from app.api.deps import require_role
from app.models.user import User
from pydantic import BaseModel
from typing import Optional


class RestrictionsUpdate(BaseModel):
    can_submit_bids: Optional[bool] = True
    can_view_jobs: Optional[bool] = True
    can_view_nda_jobs: Optional[bool] = True
    can_upload_documents: Optional[bool] = True
    can_edit_profile: Optional[bool] = True
    can_login: Optional[bool] = True
    restricted_reason: Optional[str] = None


class AuditToggleUpdate(BaseModel):
    audit_enabled: bool


router = APIRouter()


@router.get("/me/audit-toggle")
async def get_audit_toggle(current_user = Depends(require_role("admin"))):
    return {"audit_enabled": current_user.audit_enabled}


@router.patch("/me/audit-toggle")
async def toggle_audit(
    request: AuditToggleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    current_user.audit_enabled = request.audit_enabled
    await db.flush()
    return {"message": "Audit logging updated", "audit_enabled": current_user.audit_enabled}


@router.get("/users/{user_id}/restrictions")
async def get_restrictions(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, "User not found")
    return {"user_id": user.id, "restrictions": user.restrictions}


@router.patch("/users/{user_id}/restrictions")
async def set_restrictions(
    user_id: int,
    request: RestrictionsUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, "User not found")

    from datetime import datetime
    user.restrictions = {
        "can_submit_bids": request.can_submit_bids,
        "can_view_jobs": request.can_view_jobs,
        "can_view_nda_jobs": request.can_view_nda_jobs,
        "can_upload_documents": request.can_upload_documents,
        "can_edit_profile": request.can_edit_profile,
        "can_login": request.can_login,
        "restricted_reason": request.restricted_reason,
        "restricted_at": datetime.utcnow().isoformat(),
        "restricted_by": current_user.id,
    }
    await db.flush()
    return {"message": "Restrictions updated", "user_id": user.id, "restrictions": user.restrictions}


@router.delete("/users/{user_id}/restrictions")
async def remove_restrictions(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, "User not found")
    user.restrictions = None
    await db.flush()
    return {"message": "Restrictions removed", "user_id": user.id}
