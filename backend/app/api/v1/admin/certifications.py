
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.database import get_db
from app.api.deps import require_role
from app.models.certification import Certification
from app.schemas.certification import CertificationCreateRequest

router = APIRouter()


@router.get("")
async def list_certifications(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(Certification).order_by(Certification.name))
    return {"data": result.scalars().all()}


@router.get("/{cert_id}")
async def get_certification(
    cert_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(Certification).where(Certification.id == cert_id))
    cert = result.scalar_one_or_none()
    if not cert:
        raise HTTPException(404, "Certification not found")
    return {"data": cert}


@router.post("")
async def create_certification(
    request: CertificationCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    existing = await db.execute(select(Certification).where(Certification.name == request.name))
    if existing.scalar_one_or_none():
        raise HTTPException(409, "Certification already exists")
    cert = Certification(**request.model_dump(), created_by=current_user.id)
    db.add(cert)
    await db.flush()
    return {"message": "Certification created", "data": {"id": cert.id}}


@router.put("/{cert_id}")
async def update_certification(
    cert_id: int,
    request: CertificationCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(Certification).where(Certification.id == cert_id))
    cert = result.scalar_one_or_none()
    if not cert:
        raise HTTPException(404, "Certification not found")
    for key, value in request.model_dump(exclude_none=True).items():
        setattr(cert, key, value)
    cert.updated_by = current_user.id
    await db.flush()
    return {"message": "Certification updated"}


@router.delete("/{cert_id}")
async def delete_certification(
    cert_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(Certification).where(Certification.id == cert_id))
    cert = result.scalar_one_or_none()
    if not cert:
        raise HTTPException(404, "Certification not found")
    try:
        await db.delete(cert)
        await db.flush()
    except Exception:
        raise HTTPException(400, "Cannot delete this certification because it is assigned to accountants.")
    return {"message": "Certification deleted"}
