from fastapi import APIRouter, Depends, Query
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.api.deps import get_optional_user
from app.services.job_service import JobService
from app.models.user import User

router = APIRouter()


@router.get("")
async def list_jobs(
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    budget_min: Optional[str] = Query(None),
    budget_max: Optional[str] = Query(None),
    currency: Optional[str] = Query(None),
    pricing_model: Optional[str] = Query(None),
    jurisdiction: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    sort: Optional[str] = Query("newest"),
    page: int = Query(1),
    per_page: int = Query(12),
    db: AsyncSession = Depends(get_db),
):
    bmin = float(budget_min) if budget_min and budget_min.strip() else None
    bmax = float(budget_max) if budget_max and budget_max.strip() else None
    
    service = JobService(db)
    filters = {
        "search": search if search and search.strip() else None,
        "category": category if category and category.strip() else None,
        "budget_min": bmin,
        "budget_max": bmax,
        "currency": currency if currency and currency.strip() else None,
        "pricing_model": pricing_model if pricing_model and pricing_model.strip() else None,
        "jurisdiction": jurisdiction if jurisdiction and jurisdiction.strip() else None,
        "status": status if status and status.strip() else None,
        "sort": sort if sort and sort.strip() else "newest",
        "page": page,
        "per_page": per_page,
    }
    jobs, total = await service.list_jobs(filters)
    return {
        "data": jobs,
        "meta": {"current_page": page, "per_page": per_page, "total": total}
    }


@router.get("/{job_id}")
async def get_job_detail(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_optional_user),
):
    service = JobService(db)
    return await service.get_job_detail(job_id, current_user)
