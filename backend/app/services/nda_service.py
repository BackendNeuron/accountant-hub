from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.job import Job
from app.models.nda_acceptance import NDAAcceptance
from app.models.user import User


class NDAService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def accept_nda(self, job_id: int, user: User, ip_address: str = None) -> NDAAcceptance:
        result = await self.db.execute(select(Job).where(Job.id == job_id))
        job = result.scalar_one_or_none()
        if not job:
            raise HTTPException(404, 'Job not found')
        if not job.nda_required:
            raise HTTPException(400, 'This job does not require an NDA')

        existing_result = await self.db.execute(
            select(NDAAcceptance).where(
                NDAAcceptance.job_id == job_id,
                NDAAcceptance.user_id == user.id
            )
        )
        existing = existing_result.scalar_one_or_none()
        if existing:
            return existing

        nda = NDAAcceptance(
            user_id=user.id,
            job_id=job_id,
            ip_address=ip_address,
        )
        self.db.add(nda)
        await self.db.flush()
        return nda

    async def has_accepted_nda(self, job_id: int, user_id: int) -> bool:
        result = await self.db.execute(
            select(NDAAcceptance).where(
                NDAAcceptance.job_id == job_id,
                NDAAcceptance.user_id == user_id
            )
        )
        return result.scalar_one_or_none() is not None
