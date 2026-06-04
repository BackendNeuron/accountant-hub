from fastapi import APIRouter, Depends, Request
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
            from app.models.accountant_certification import AccountantCertification
            from app.models.certification import Certification
            
            cert_result = await db.execute(
                select(AccountantCertification).where(
                    AccountantCertification.accountant_profile_id == profile.id
                )
            )
            acct_certs = cert_result.scalars().all()
            cert_names = []
            for ac in acct_certs:
                if ac.certification_id:
                    c_res = await db.execute(
                        select(Certification).where(Certification.id == ac.certification_id)
                    )
                    c = c_res.scalar_one_or_none()
                    if c:
                        cert_names.append(c.name)
                elif ac.custom_certification_name:
                    cert_names.append(ac.custom_certification_name)
            
            response["profile"] = {
                "bio": profile.bio,
                "years_of_experience": profile.years_of_experience,
                "hourly_rate": float(profile.hourly_rate) if profile.hourly_rate else None,
                "jurisdictions_served": profile.jurisdictions_served,
                "accounting_standards": profile.accounting_standards,
                "education_summary": profile.education_summary,
                "profile_completed": profile.profile_completed,
                "certifications": cert_names,
            }
            
            from app.models.accountant_software_skill import AccountantSoftwareSkill
            from app.models.software_skill import SoftwareSkill
            sw_result = await db.execute(
                select(AccountantSoftwareSkill).where(
                    AccountantSoftwareSkill.accountant_profile_id == profile.id
                )
            )
            acct_sw = sw_result.scalars().all()
            sw_names = []
            for ass in acct_sw:
                sw_res = await db.execute(
                    select(SoftwareSkill).where(SoftwareSkill.id == ass.software_skill_id)
                )
                sw = sw_res.scalar_one_or_none()
                if sw:
                    sw_names.append(sw.name)
            response["profile"]["software_skills"] = sw_names
            
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

@router.put("/certifications")
async def update_certifications(
    data: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "accountant":
        raise HTTPException(403, "Only accountants can update certifications")

    result = await db.execute(
        select(AccountantProfile).where(AccountantProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    if not profile:
        profile = AccountantProfile(user_id=current_user.id)
        db.add(profile)
        await db.flush()

    from app.models.accountant_certification import AccountantCertification
    from app.models.certification import Certification

    # Delete existing certifications
    await db.execute(
        select(AccountantCertification).where(
            AccountantCertification.accountant_profile_id == profile.id
        )
    )
    existing = (await db.execute(
        select(AccountantCertification).where(
            AccountantCertification.accountant_profile_id == profile.id
        )
    )).scalars().all()
    for cert in existing:
        await db.delete(cert)

    # Add new certifications
    cert_names = data.get("certifications", [])
    for name in cert_names:
        cert_result = await db.execute(
            select(Certification).where(Certification.name == name)
        )
        cert = cert_result.scalar_one_or_none()
        if cert:
            acc_cert = AccountantCertification(
                accountant_profile_id=profile.id,
                certification_id=cert.id,
            )
        else:
            acc_cert = AccountantCertification(
                accountant_profile_id=profile.id,
                custom_certification_name=name,
            )
        db.add(acc_cert)

    await db.flush()
    return {"message": "Certifications updated", "certifications": cert_names}

@router.put("/software-skills")
async def update_software_skills(
    data: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "accountant":
        raise HTTPException(403, "Only accountants can update software skills")

    result = await db.execute(
        select(AccountantProfile).where(AccountantProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    if not profile:
        profile = AccountantProfile(user_id=current_user.id)
        db.add(profile)
        await db.flush()

    from app.models.accountant_software_skill import AccountantSoftwareSkill
    from app.models.software_skill import SoftwareSkill

    existing = (await db.execute(
        select(AccountantSoftwareSkill).where(
            AccountantSoftwareSkill.accountant_profile_id == profile.id
        )
    )).scalars().all()
    for item in existing:
        await db.delete(item)

    skill_names = data.get("software_skills", [])
    for name in skill_names:
        sw_result = await db.execute(
            select(SoftwareSkill).where(SoftwareSkill.name == name)
        )
        sw = sw_result.scalar_one_or_none()
        if sw:
            acc_sw = AccountantSoftwareSkill(
                accountant_profile_id=profile.id,
                software_skill_id=sw.id,
            )
            db.add(acc_sw)

    await db.flush()
    return {"message": "Software skills updated", "software_skills": skill_names}

