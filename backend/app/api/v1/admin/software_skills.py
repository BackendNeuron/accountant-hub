
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.database import get_db
from app.api.deps import require_role
from app.models.software_skill import SoftwareSkill
from app.schemas.software_skill import SoftwareSkillCreateRequest, SoftwareSkillUpdateRequest

router = APIRouter()


@router.get("")
async def list_software_skills(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(SoftwareSkill).order_by(SoftwareSkill.name))
    return {"data": result.scalars().all()}


@router.get("/{skill_id}")
async def get_software_skill(
    skill_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(SoftwareSkill).where(SoftwareSkill.id == skill_id))
    skill = result.scalar_one_or_none()
    if not skill:
        raise HTTPException(404, "Software skill not found")
    return {"data": skill}


@router.post("")
async def create_software_skill(
    request: SoftwareSkillCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    existing = await db.execute(select(SoftwareSkill).where(SoftwareSkill.name == request.name))
    if existing.scalar_one_or_none():
        raise HTTPException(409, "Software skill already exists")
    skill = SoftwareSkill(name=request.name, created_by=current_user.id)
    db.add(skill)
    await db.flush()
    return {"message": "Software skill created", "data": {"id": skill.id}}


@router.put("/{skill_id}")
async def update_software_skill(
    skill_id: int,
    request: SoftwareSkillUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(SoftwareSkill).where(SoftwareSkill.id == skill_id))
    skill = result.scalar_one_or_none()
    if not skill:
        raise HTTPException(404, "Software skill not found")
    for key, value in request.model_dump(exclude_none=True).items():
        setattr(skill, key, value)
    skill.updated_by = current_user.id
    await db.flush()
    return {"message": "Software skill updated"}


@router.delete("/{skill_id}")
async def delete_software_skill(
    skill_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(SoftwareSkill).where(SoftwareSkill.id == skill_id))
    skill = result.scalar_one_or_none()
    if not skill:
        raise HTTPException(404, "Software skill not found")
    await db.delete(skill)
    await db.flush()
    return {"message": "Software skill deleted"}
