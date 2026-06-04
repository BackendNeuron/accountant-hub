from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, cast, Date
from app.database import get_db
from app.api.deps import require_role
from app.models.user import User
from app.models.job import Job
from app.models.bid import Bid
from app.models.category import Category

router = APIRouter()


@router.get("/dashboard/stats")
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    total_users = (await db.execute(select(func.count(User.id)))).scalar()
    total_accountants = (await db.execute(select(func.count(User.id)).where(User.role == 'accountant'))).scalar()
    total_clients = (await db.execute(select(func.count(User.id)).where(User.role == 'client'))).scalar()
    total_admins = (await db.execute(select(func.count(User.id)).where(User.role == 'admin'))).scalar()
    
    total_jobs = (await db.execute(select(func.count(Job.id)))).scalar()
    open_jobs = (await db.execute(select(func.count(Job.id)).where(Job.status == 'open'))).scalar()
    closed_jobs = (await db.execute(select(func.count(Job.id)).where(Job.status == 'closed'))).scalar()
    
    total_bids = (await db.execute(select(func.count(Bid.id)))).scalar()
    pending_bids = (await db.execute(select(func.count(Bid.id)).where(Bid.status == 'pending'))).scalar()
    accepted_bids = (await db.execute(select(func.count(Bid.id)).where(Bid.status == 'accepted'))).scalar()
    rejected_bids = (await db.execute(select(func.count(Bid.id)).where(Bid.status == 'rejected'))).scalar()

    
    # Time-series: jobs posted per day (last 30 days)
    jobs_ts_result = await db.execute(
        select(
            cast(Job.posted_date, Date).label('date'),
            func.count(Job.id).label('count')
        )
        .group_by(cast(Job.posted_date, Date))
        .order_by(cast(Job.posted_date, Date).desc())
        .limit(30)
    )
    jobs_time_series = [{"date": str(row[0]), "count": row[1]} for row in jobs_ts_result.all()]

    # Time-series: bids submitted per day (last 30 days)
    bids_ts_result = await db.execute(
        select(
            cast(Bid.created_at, Date).label('date'),
            func.count(Bid.id).label('count')
        )
        .group_by(cast(Bid.created_at, Date))
        .order_by(cast(Bid.created_at, Date).desc())
        .limit(30)
    )
    bids_time_series = [{"date": str(row[0]), "count": row[1]} for row in bids_ts_result.all()]

    # Time-series: user registrations per day (last 30 days)
    users_ts_result = await db.execute(
        select(
            cast(User.created_at, Date).label('date'),
            func.count(User.id).label('count')
        )
        .group_by(cast(User.created_at, Date))
        .order_by(cast(User.created_at, Date).desc())
        .limit(30)
    )
    users_time_series = [{"date": str(row[0]), "count": row[1]} for row in users_ts_result.all()]

    # Top accountants by bid count
    top_accountants_result = await db.execute(
        select(User.name, func.count(Bid.id).label('bid_count'))
        .join(Bid, Bid.accountant_id == User.id)
        .where(User.role == 'accountant')
        .group_by(User.id, User.name)
        .order_by(func.count(Bid.id).desc())
        .limit(5)
    )
    top_accountants = [{"name": row[0], "bids": row[1]} for row in top_accountants_result.all()]

    # Jobs by category
    jobs_by_cat_result = await db.execute(
        select(Category.name, func.count(Job.id).label('count'))
        .join(Job, Job.category_id == Category.id)
        .group_by(Category.id, Category.name)
        .order_by(func.count(Job.id).desc())
    )
    jobs_by_category = [{"name": row[0], "count": row[1]} for row in jobs_by_cat_result.all()]

    return {
        "data": {
            "total_users": total_users,
            "users_by_role": {
                "admin": total_admins,
                "client": total_clients,
                "accountant": total_accountants,
            },
            "total_jobs": total_jobs,
            "jobs_by_status": {"open": open_jobs, "closed": closed_jobs},
            "total_bids": total_bids,
            "bids_by_status": {"pending": pending_bids, "accepted": accepted_bids, "rejected": rejected_bids},
            "jobs_time_series": jobs_time_series,
            "bids_time_series": bids_time_series,
            "users_time_series": users_time_series,
            "top_accountants": top_accountants,
            "jobs_by_category": jobs_by_category,
        }
    }
