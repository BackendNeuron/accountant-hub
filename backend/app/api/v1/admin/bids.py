from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException
from app.database import get_db
from app.models.job import Job
from app.api.deps import require_role
from app.models.bid import Bid

router = APIRouter()


@router.get("")
async def list_bids(
    job_id: int = Query(None),
    accountant_id: int = Query(None),
    status: str = Query(None),
    page: int = Query(1),
    per_page: int = Query(25),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    query = select(Bid)
    if job_id:
        query = query.where(Bid.job_id == job_id)
    if accountant_id:
        query = query.where(Bid.accountant_id == accountant_id)
    if status:
        query = query.where(Bid.status == status)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()

    query = query.order_by(Bid.created_at.desc()).offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)

    return {"data": result.scalars().all(), "meta": {"page": page, "per_page": per_page, "total": total}}


@router.get("/{bid_id}")
async def get_bid(
    bid_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(Bid).where(Bid.id == bid_id))
    bid = result.scalar_one_or_none()
    if not bid:
        raise HTTPException(404, "Bid not found")
    return {"data": bid}


@router.delete("/{bid_id}")
async def delete_bid(
    bid_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(Bid).where(Bid.id == bid_id))
    bid = result.scalar_one_or_none()
    if not bid:
        raise HTTPException(404, "Bid not found")

    job_result = await db.execute(select(Job).where(Job.id == bid.job_id))
    job = job_result.scalar_one_or_none()
    if job:
        job.bids_count = max(0, (job.bids_count or 1) - 1)

    await db.delete(bid)
    await db.flush()
    return {"message": "Bid deleted"}
