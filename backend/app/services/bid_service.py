from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException
from datetime import date
from app.models.job import Job
from app.models.bid import Bid
from app.models.user import User


class BidService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def submit_bid(self, job_id: int, accountant: User, bid_data: dict) -> Bid:
        result = await self.db.execute(select(Job).where(Job.id == job_id))
        job = result.scalar_one_or_none()
        if not job:
            raise HTTPException(404, "Job not found")
        if job.status != "open":
            raise HTTPException(400, "This job is closed and no longer accepting bids")
        if job.deadline and job.deadline < date.today():
            raise HTTPException(400, "The deadline for this job has passed")
        if accountant.restrictions:
            r = accountant.restrictions
            if r.get("can_submit_bids") == False:
                raise HTTPException(403, r.get("restricted_reason", "Your account has restricted bidding"))
        existing = await self.db.execute(
            select(Bid).where(Bid.job_id == job_id, Bid.accountant_id == accountant.id)
        )
        if existing.scalar_one_or_none():
            raise HTTPException(409, "You have already submitted a bid for this job")
        bid = Bid(
            job_id=job_id, accountant_id=accountant.id,
            currency=job.currency, **bid_data
        )
        self.db.add(bid)
        job.bids_count = (job.bids_count or 0) + 1
        if job.bids_min_price is None or bid_data["price"] < job.bids_min_price:
            job.bids_min_price = bid_data["price"]
        if job.bids_max_price is None or bid_data["price"] > job.bids_max_price:
            job.bids_max_price = bid_data["price"]
        await self.db.flush()
        return bid

    async def get_my_bids(self, accountant_id: int, page: int = 1, per_page: int = 12) -> tuple:
        query = select(Bid).where(
            Bid.accountant_id == accountant_id
        ).order_by(Bid.created_at.desc())
        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar()
        query = query.offset((page - 1) * per_page).limit(per_page)
        result = await self.db.execute(query)
        bids = result.scalars().all()
        return bids, total