"""
Add certifications save endpoint
Run: python fix_certifications.py
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))

# Update profile.py to include certifications endpoint
with open(os.path.join(BASE, 'backend', 'app', 'api', 'v1', 'profile.py'), 'r', encoding='utf-8') as f:
    content = f.read()

# Add the certifications endpoint before the last line
cert_endpoint = """

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
"""

# Insert before the last line
content = content.rstrip() + cert_endpoint + "\n"

with open(os.path.join(BASE, 'backend', 'app', 'api', 'v1', 'profile.py'), 'w', encoding='utf-8') as f:
    f.write(content)

print("Added certifications endpoint to profile.py")