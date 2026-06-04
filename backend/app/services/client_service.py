from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from fastapi import HTTPException
from datetime import datetime
from app.models.job import Job
from app.models.bid import Bid
from app.models.user import User


class ClientService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_job(self, client: User, job_data: dict) -> Job:
        job = Job(client_id=client.id, **job_data)
        self.db.add(job)
        await self.db.flush()
        return job

    async def list_my_jobs(self, client_id: int, page: int = 1, per_page: int = 12) -> tuple:
        query = select(Job).where(Job.client_id == client_id).order_by(Job.created_at.desc())
        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar()
        query = query.offset((page - 1) * per_page).limit(per_page)
        result = await self.db.execute(query)
        jobs = result.scalars().all()
        return jobs, total

    async def get_my_job(self, job_id: int, client_id: int) -> Job:
        result = await self.db.execute(
            select(Job).where(Job.id == job_id, Job.client_id == client_id)
        )
        job = result.scalar_one_or_none()
        if not job:
            raise HTTPException(404, "Job not found")
        return job

    async def update_my_job(self, job_id: int, client_id: int, update_data: dict) -> Job:
        job = await self.get_my_job(job_id, client_id)
        if job.status == "closed":
            raise HTTPException(400, "Cannot update a closed job")
        for key, value in update_data.items():
            if value is not None and hasattr(job, key):
                setattr(job, key, value)
        await self.db.flush()
        return job

    async def update_job_status(self, job_id: int, client_id: int, status: str, closed_reason: str = None) -> Job:
        job = await self.get_my_job(job_id, client_id)
        job.status = status
        if status == "closed" and closed_reason:
            job.closed_reason = closed_reason
        await self.db.flush()
        return job

    async def get_job_bids(self, job_id: int, client_id: int) -> list:
        await self.get_my_job(job_id, client_id)
        result = await self.db.execute(
            select(Bid).where(Bid.job_id == job_id).order_by(Bid.created_at.desc())
        )
        bids = result.scalars().all()
        
        from app.models.user import User
        for bid in bids:
            u_result = await self.db.execute(select(User).where(User.id == bid.accountant_id))
            user = u_result.scalar_one_or_none()
            bid.accountant_name = user.name if user else f'Accountant #{bid.accountant_id}'
        
        return bids

    async def accept_bid(self, job_id: int, bid_id: int, client_id: int) -> Bid:
        job = await self.get_my_job(job_id, client_id)
        if job.status != "open":
            raise HTTPException(400, "Job is not open")
        result = await self.db.execute(
            select(Bid).where(Bid.id == bid_id, Bid.job_id == job_id)
        )
        bid = result.scalar_one_or_none()
        if not bid:
            raise HTTPException(404, "Bid not found")
        if bid.status != "pending":
            raise HTTPException(400, f"Bid is already {bid.status}")
        bid.status = "accepted"
        bid.accepted_at = datetime.utcnow()
        job.status = "closed"
        job.closed_reason = "bid_accepted"
        await self.db.execute(
            update(Bid)
            .where(Bid.job_id == job_id, Bid.id != bid_id, Bid.status == "pending")
            .values(status="rejected", rejected_at=datetime.utcnow())
        )
        await self.db.flush()
        return bid

    async def reject_bid(self, job_id: int, bid_id: int, client_id: int) -> Bid:
        await self.get_my_job(job_id, client_id)
        result = await self.db.execute(
            select(Bid).where(Bid.id == bid_id, Bid.job_id == job_id)
        )
        bid = result.scalar_one_or_none()
        if not bid:
            raise HTTPException(404, "Bid not found")
        if bid.status != "pending":
            raise HTTPException(400, f"Bid is already {bid.status}")
        bid.status = "rejected"
        bid.rejected_at = datetime.utcnow()
        await self.db.flush()
        return bid