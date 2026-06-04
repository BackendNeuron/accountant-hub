content = """from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from fastapi import HTTPException
from app.models.job import Job
from app.models.bid import Bid


class JobService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_jobs(self, filters: dict) -> tuple:
        query = select(Job)

        status = filters.get('status')
        if status and status.strip():
            query = query.where(Job.status == status.strip())

        search = filters.get('search')
        if search and search.strip():
            search_term = '%' + search.strip() + '%'
            query = query.where(
                or_(Job.title.ilike(search_term), Job.description.ilike(search_term))
            )

        category = filters.get('category')
        if category and str(category).strip():
            query = query.where(Job.category_id == int(category))

        pricing = filters.get('pricing_model')
        if pricing and pricing.strip():
            query = query.where(Job.pricing_model == pricing.strip())

        jurisdiction = filters.get('jurisdiction')
        if jurisdiction and jurisdiction.strip():
            query = query.where(Job.jurisdiction == jurisdiction.strip())

        budget_min = filters.get('budget_min')
        if budget_min and str(budget_min).strip():
            query = query.where(Job.budget_max >= float(budget_min))

        budget_max = filters.get('budget_max')
        if budget_max and str(budget_max).strip():
            query = query.where(Job.budget_min <= float(budget_max))

        sort_map = {
            'newest': Job.posted_date.desc(),
            'budget_high': Job.budget_max.desc(),
            'budget_low': Job.budget_min.asc(),
            'bids': Job.bids_count.desc(),
            'deadline': Job.deadline.asc(),
        }
        sort_by = sort_map.get(filters.get('sort'), Job.posted_date.desc())
        query = query.order_by(sort_by)

        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar()

        page = int(filters.get('page', 1))
        per_page = int(filters.get('per_page', 12))
        query = query.offset((page - 1) * per_page).limit(per_page)

        result = await self.db.execute(query)
        jobs = result.scalars().all()
        return jobs, total

    async def get_job_detail(self, job_id: int) -> dict:
        result = await self.db.execute(select(Job).where(Job.id == job_id))
        job = result.scalar_one_or_none()
        if not job:
            raise HTTPException(404, 'Job not found')
        return {'job': job, 'current_user_bid': None}
"""
with open('app/services/job_service.py', 'w') as f:
    f.write(content)
print('DONE')
