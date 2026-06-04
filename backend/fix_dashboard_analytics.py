with open('app/api/v1/admin/dashboard.py', 'r') as f:
    content = f.read()

# Add new imports
content = content.replace(
    'from sqlalchemy import select, func',
    'from sqlalchemy import select, func, cast, Date'
)

# Add new queries before the return statement
old_return = '''return {
        "data": {'''

new_queries = '''
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
        "data": {'''

content = content.replace(old_return, new_queries)

# Add new fields to the response
old_close = '''            "total_bids": total_bids,
            "bids_by_status": {"pending": pending_bids, "accepted": accepted_bids, "rejected": rejected_bids},
        }'''

new_close = '''            "total_bids": total_bids,
            "bids_by_status": {"pending": pending_bids, "accepted": accepted_bids, "rejected": rejected_bids},
            "jobs_time_series": jobs_time_series,
            "bids_time_series": bids_time_series,
            "users_time_series": users_time_series,
            "top_accountants": top_accountants,
            "jobs_by_category": jobs_by_category,
        }'''

content = content.replace(old_close, new_close)

# Add missing imports
content = content.replace(
    'from app.models.user import User\nfrom app.models.job import Job\nfrom app.models.bid import Bid',
    'from app.models.user import User\nfrom app.models.job import Job\nfrom app.models.bid import Bid\nfrom app.models.category import Category'
)

with open('app/api/v1/admin/dashboard.py', 'w') as f:
    f.write(content)

print('Dashboard enhanced with time-series analytics')
