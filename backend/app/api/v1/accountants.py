from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.database import get_db
from app.api.deps import require_role, get_current_user
from app.models.user import User
from app.models.accountant_profile import AccountantProfile
from app.models.accountant_certification import AccountantCertification
from app.models.certification import Certification
from app.models.accountant_software_skill import AccountantSoftwareSkill
from app.models.software_skill import SoftwareSkill
from app.models.bid import Bid
from app.models.job import Job

router = APIRouter()


@router.get("/{accountant_id}/profile")
async def get_accountant_profile(
    accountant_id: int,
    job_id: int = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("client")),
):
    # Verify the job belongs to this client
    job_result = await db.execute(
        select(Job).where(Job.id == job_id, Job.client_id == current_user.id)
    )
    job = job_result.scalar_one_or_none()
    if not job:
        raise HTTPException(403, "You can only view profiles of accountants who bid on your jobs")

    # Verify this accountant bid on this job
    bid_result = await db.execute(
        select(Bid).where(Bid.job_id == job_id, Bid.accountant_id == accountant_id)
    )
    bid = bid_result.scalar_one_or_none()
    if not bid:
        raise HTTPException(403, "This accountant has not submitted a bid on your job")

    # Get accountant user info
    user_result = await db.execute(select(User).where(User.id == accountant_id))
    accountant = user_result.scalar_one_or_none()
    if not accountant:
        raise HTTPException(404, "Accountant not found")

    # Get profile
    profile_result = await db.execute(
        select(AccountantProfile).where(AccountantProfile.user_id == accountant_id)
    )
    profile = profile_result.scalar_one_or_none()

    # Get certifications
    certs = []
    if profile:
        cert_result = await db.execute(
            select(AccountantCertification).where(
                AccountantCertification.accountant_profile_id == profile.id
            )
        )
        for ac in cert_result.scalars().all():
            if ac.certification_id:
                c = (await db.execute(select(Certification).where(Certification.id == ac.certification_id))).scalar_one_or_none()
                certs.append({"name": c.name if c else "Unknown", "custom": False})
            elif ac.custom_certification_name:
                certs.append({"name": ac.custom_certification_name, "custom": True})

    # Get software skills
    software = []
    if profile:
        sw_result = await db.execute(
            select(AccountantSoftwareSkill).where(
                AccountantSoftwareSkill.accountant_profile_id == profile.id
            )
        )
        for ass in sw_result.scalars().all():
            s = (await db.execute(select(SoftwareSkill).where(SoftwareSkill.id == ass.software_skill_id))).scalar_one_or_none()
            if s:
                software.append(s.name)

    return {
        "data": {
            "name": accountant.name,
            "email": accountant.email,
            "bio": profile.bio if profile else None,
            "years_of_experience": profile.years_of_experience if profile else None,
            "hourly_rate": float(profile.hourly_rate) if profile and profile.hourly_rate else None,
            "jurisdictions_served": profile.jurisdictions_served if profile else [],
            "accounting_standards": profile.accounting_standards if profile else [],
            "certifications": certs,
            "software_skills": software,
            "bid_price": str(bid.price),
            "bid_delivery": bid.delivery_time,
        }
    }
