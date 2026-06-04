"""
Fix all backend services - Phase III
Run: python fix_services.py
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))

FILES = {}

FILES['app/services/bid_service.py'] = '''from sqlalchemy.ext.asyncio import AsyncSession
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
'''

FILES['app/services/client_service.py'] = '''from sqlalchemy.ext.asyncio import AsyncSession
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
        return result.scalars().all()

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
'''

FILES['app/services/job_service.py'] = '''from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from fastapi import HTTPException
from app.models.job import Job
from app.models.category import Category
from app.models.bid import Bid


class JobService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_jobs(self, filters: dict) -> tuple:
        query = select(Job)

        status = filters.get("status")
        if status and status.strip():
            query = query.where(Job.status == status.strip())

        search = filters.get("search")
        if search and search.strip():
            s = "%" + search.strip() + "%"
            query = query.where(
                or_(Job.title.ilike(s), Job.description.ilike(s))
            )

        category_slug = filters.get("category")
        if category_slug and category_slug.strip():
            cat_res = await self.db.execute(
                select(Category.id).where(Category.slug == category_slug.strip())
            )
            cat_id = cat_res.scalar_one_or_none()
            if cat_id:
                query = query.where(Job.category_id == cat_id)
            else:
                query = query.where(Job.category_id == -1)

        pricing = filters.get("pricing_model")
        if pricing and pricing.strip():
            query = query.where(Job.pricing_model == pricing.strip())

        jurisdiction = filters.get("jurisdiction")
        if jurisdiction and jurisdiction.strip():
            query = query.where(Job.jurisdiction == jurisdiction.strip())

        budget_min = filters.get("budget_min")
        if budget_min and str(budget_min).strip():
            query = query.where(Job.budget_max >= float(budget_min))

        budget_max = filters.get("budget_max")
        if budget_max and str(budget_max).strip():
            query = query.where(Job.budget_min <= float(budget_max))

        sort_map = {
            "newest": Job.posted_date.desc(),
            "budget_high": Job.budget_max.desc(),
            "budget_low": Job.budget_min.asc(),
            "bids": Job.bids_count.desc(),
            "deadline": Job.deadline.asc(),
        }
        sort_by = sort_map.get(filters.get("sort"), Job.posted_date.desc())
        query = query.order_by(sort_by)

        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar()

        page = int(filters.get("page", 1))
        per_page = int(filters.get("per_page", 12))
        query = query.offset((page - 1) * per_page).limit(per_page)

        result = await self.db.execute(query)
        jobs = result.scalars().all()
        return jobs, total

    async def get_job_detail(self, job_id: int) -> dict:
        result = await self.db.execute(select(Job).where(Job.id == job_id))
        job = result.scalar_one_or_none()
        if not job:
            raise HTTPException(404, "Job not found")
        return {"job": job, "current_user_bid": None}
'''

FILES['app/api/v1/profile.py'] = '''from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.accountant_profile import AccountantProfile
from app.models.client_profile import ClientProfile
from app.services.audit_service import AuditService

router = APIRouter()


@router.get("")
async def get_my_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    response = {
        "id": current_user.id, "name": current_user.name,
        "email": current_user.email, "phone": current_user.phone,
        "role": current_user.role, "is_active": current_user.is_active,
    }
    if current_user.role == "accountant":
        result = await db.execute(
            select(AccountantProfile).where(AccountantProfile.user_id == current_user.id)
        )
        profile = result.scalar_one_or_none()
        if profile:
            response["profile"] = {
                "bio": profile.bio,
                "years_of_experience": profile.years_of_experience,
                "hourly_rate": float(profile.hourly_rate) if profile.hourly_rate else None,
                "jurisdictions_served": profile.jurisdictions_served,
                "accounting_standards": profile.accounting_standards,
                "education_summary": profile.education_summary,
                "profile_completed": profile.profile_completed,
            }
    elif current_user.role == "client":
        result = await db.execute(
            select(ClientProfile).where(ClientProfile.user_id == current_user.id)
        )
        profile = result.scalar_one_or_none()
        if profile:
            response["profile"] = {
                "company_name": profile.company_name,
                "company_industry": profile.company_industry,
                "company_size": profile.company_size,
                "company_description": profile.company_description,
                "website": profile.website,
                "country_id": profile.country_id,
                "city": profile.city,
                "profile_completed": profile.profile_completed,
            }
    return {"data": response}


@router.put("")
async def update_my_profile(
    update_data: dict,
    req: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == "accountant":
        result = await db.execute(
            select(AccountantProfile).where(AccountantProfile.user_id == current_user.id)
        )
        profile = result.scalar_one_or_none()
        if not profile:
            profile = AccountantProfile(user_id=current_user.id)
            db.add(profile)

        if "bio" in update_data and update_data["bio"] is not None:
            profile.bio = str(update_data["bio"])
        if "years_of_experience" in update_data and update_data["years_of_experience"] is not None:
            profile.years_of_experience = int(update_data["years_of_experience"])
        if "hourly_rate" in update_data and update_data["hourly_rate"] is not None:
            profile.hourly_rate = float(update_data["hourly_rate"])
        if "jurisdictions_served" in update_data:
            profile.jurisdictions_served = update_data["jurisdictions_served"]
        if "accounting_standards" in update_data:
            profile.accounting_standards = update_data["accounting_standards"]
        if "education_summary" in update_data and update_data["education_summary"] is not None:
            profile.education_summary = str(update_data["education_summary"])
        profile.profile_completed = True

    elif current_user.role == "client":
        result = await db.execute(
            select(ClientProfile).where(ClientProfile.user_id == current_user.id)
        )
        profile = result.scalar_one_or_none()
        if not profile:
            profile = ClientProfile(
                user_id=current_user.id,
                company_name=update_data.get("company_name", ""),
            )
            db.add(profile)

        if "company_name" in update_data and update_data["company_name"] is not None:
            profile.company_name = str(update_data["company_name"])
        if "company_industry" in update_data:
            profile.company_industry = update_data["company_industry"]
        if "company_size" in update_data:
            profile.company_size = update_data["company_size"]
        if "company_description" in update_data:
            profile.company_description = update_data["company_description"]
        if "website" in update_data:
            profile.website = update_data["website"]
        if "country_id" in update_data and update_data["country_id"] is not None:
            profile.country_id = int(update_data["country_id"])
        if "city" in update_data:
            profile.city = update_data["city"]
        profile.profile_completed = True

    audit = AuditService(db)
    await audit.log(
        action="profile.updated",
        action_category="profile",
        entity_type="User",
        entity_id=current_user.id,
        user_id=current_user.id,
        user_email=current_user.email,
        user_role=current_user.role,
        description="Profile updated",
        ip_address=req.client.host if req.client else None,
    )
    await db.flush()
    return {"message": "Profile updated successfully"}
'''

if __name__ == "__main__":
    os.chdir(BASE)
    for path, content in FILES.items():
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content.strip())
        print(f"✅ Fixed: {path}")
    print("\n🎉 All 4 files fixed. Restart: uvicorn app.main:app --reload")