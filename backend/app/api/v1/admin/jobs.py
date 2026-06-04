from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException
from app.database import get_db
from app.api.deps import require_role
from app.models.job import Job

router = APIRouter()


@router.get("")
async def list_jobs(
    status: str = Query(None),
    client_id: int = Query(None),
    category_id: int = Query(None),
    page: int = Query(1),
    per_page: int = Query(25),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    query = select(Job)
    if status:
        query = query.where(Job.status == status)
    if client_id:
        query = query.where(Job.client_id == client_id)
    if category_id:
        query = query.where(Job.category_id == category_id)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()

    query = query.order_by(Job.created_at.desc()).offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)

    return {"data": result.scalars().all(), "meta": {"page": page, "per_page": per_page, "total": total}}


@router.get("/{job_id}")
async def get_job(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(404, "Job not found")
    return {"data": job}


@router.delete("/{job_id}")
async def delete_job(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(404, "Job not found")
    await db.delete(job)
    await db.flush()
    return {"message": "Job deleted"}


@router.patch("/{job_id}/status")
async def update_job_status(
    job_id: int,
    status: str = Query(..., pattern="^(open|closed)$"),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(404, "Job not found")
    job.status = status
    if status == "closed":
        job.closed_reason = "admin_closed"
    await db.flush()
    return {"message": f"Job {status}"}
