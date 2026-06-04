with open('app/services/job_service.py', 'r') as f:
    content = f.read()

# Add ClientProfile import
content = content.replace(
    'from app.models.bid import Bid',
    'from app.models.bid import Bid\nfrom app.models.client_profile import ClientProfile'
)

# Fix get_job_detail
content = content.replace(
    '''result = await self.db.execute(select(Job).where(Job.id == job_id))
        job = result.scalar_one_or_none()
        if not job:
            raise HTTPException(404, "Job not found")''',
    '''result = await self.db.execute(select(Job).where(Job.id == job_id))
        job = result.scalar_one_or_none()
        if not job:
            raise HTTPException(404, "Job not found")
        cp_result = await self.db.execute(
            select(ClientProfile).where(ClientProfile.user_id == job.client_id)
        )
        cp = cp_result.scalar_one_or_none()
        job.company_name = cp.company_name if cp else None'''
)

# Fix list_jobs
content = content.replace(
    '''result = await self.db.execute(query)
        jobs = result.scalars().all()
        return jobs, total''',
    '''result = await self.db.execute(query)
        jobs = result.scalars().all()
        for job in jobs:
            cp_result = await self.db.execute(
                select(ClientProfile).where(ClientProfile.user_id == job.client_id)
            )
            cp = cp_result.scalar_one_or_none()
            job.company_name = cp.company_name if cp else None
        return jobs, total'''
)

with open('app/services/job_service.py', 'w') as f:
    f.write(content)

print('Done - company names will now show on jobs')
