with open('app/api/v1/profile.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_get = '"certifications": cert_names,\n            }'
new_get = '''"certifications": cert_names,
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
            '''

content = content.replace(old_get.strip(), new_get.strip())

sw_endpoint = '''

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
'''

content = content.rstrip() + sw_endpoint + '\n'

with open('app/api/v1/profile.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done')
