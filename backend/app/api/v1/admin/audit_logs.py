
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException
from app.database import get_db
from app.api.deps import require_role
from app.models.audit_log import AuditLog

router = APIRouter()


@router.get("")
async def list_audit_logs(
    page: int = Query(1),
    per_page: int = Query(25),
    action_category: str = Query(None),
    action: str = Query(None),
    user_role: str = Query(None),
    entity_type: str = Query(None),
    entity_id: int = Query(None),
    search: str = Query(None),
    date_from: str = Query(None),
    date_to: str = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    query = select(AuditLog).order_by(AuditLog.created_at.desc())

    if action_category:
        query = query.where(AuditLog.action_category == action_category)
    if action:
        query = query.where(AuditLog.action == action)
    if user_role:
        query = query.where(AuditLog.user_role == user_role)
    if entity_type:
        query = query.where(AuditLog.entity_type == entity_type)
    if entity_id:
        query = query.where(AuditLog.entity_id == entity_id)
    if search:
        query = query.where(AuditLog.description.ilike(f"%{search}%"))
    if date_from:
        query = query.where(AuditLog.created_at >= date_from)
    if date_to:
        query = query.where(AuditLog.created_at <= date_to)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()

    query = query.offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)

    return {"data": result.scalars().all(), "meta": {"page": page, "per_page": per_page, "total": total}}


@router.get("/{log_id}")
async def get_audit_log(
    log_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(AuditLog).where(AuditLog.id == log_id))
    log = result.scalar_one_or_none()
    if not log:
        raise HTTPException(404, "Audit log not found")
    return {"data": log}


@router.get("/meta/filters")
async def get_filter_options(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    # Distinct action categories
    cat_result = await db.execute(select(AuditLog.action_category).distinct())
    categories = [row[0] for row in cat_result if row[0]]

    # Distinct actions
    act_result = await db.execute(select(AuditLog.action).distinct())
    actions = [row[0] for row in act_result if row[0]]

    # Distinct entity types
    ent_result = await db.execute(select(AuditLog.entity_type).distinct())
    entity_types = [row[0] for row in ent_result if row[0]]

    return {
        "data": {
            "action_categories": sorted(categories),
            "actions": sorted(actions),
            "entity_types": sorted(entity_types),
            "user_roles": ["admin", "client", "accountant"],
        }
    }
