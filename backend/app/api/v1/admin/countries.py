
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.database import get_db
from app.api.deps import require_role
from app.models.country import Country
from pydantic import BaseModel
from typing import Optional


class CountryCreateRequest(BaseModel):
    country_name_ar: Optional[str] = None
    country_name_en: str
    country_iso_code2: str
    country_iso_code3: str
    country_iso_numeric: Optional[str] = None
    currency_name: str
    currency_iso_code: str
    currency_iso_number: Optional[str] = None
    phone_code: str
    phone_digits_count: Optional[int] = None


class CountryUpdateRequest(BaseModel):
    country_name_ar: Optional[str] = None
    country_name_en: Optional[str] = None
    currency_name: Optional[str] = None
    currency_iso_code: Optional[str] = None
    phone_code: Optional[str] = None
    phone_digits_count: Optional[int] = None
    is_active: Optional[bool] = None


router = APIRouter()


@router.get("")
async def list_countries(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(Country).order_by(Country.country_name_en))
    return {"data": result.scalars().all()}


@router.get("/{country_id}")
async def get_country(
    country_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(Country).where(Country.id == country_id))
    country = result.scalar_one_or_none()
    if not country:
        raise HTTPException(404, "Country not found")
    return {"data": country}


@router.post("")
async def create_country(
    request: CountryCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    existing = await db.execute(select(Country).where(Country.country_iso_code2 == request.country_iso_code2))
    if existing.scalar_one_or_none():
        raise HTTPException(409, "Country code already exists")
    country = Country(**request.model_dump(), created_by=current_user.id)
    db.add(country)
    await db.flush()
    return {"message": "Country created", "data": {"id": country.id}}


@router.put("/{country_id}")
async def update_country(
    country_id: int,
    request: CountryUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(Country).where(Country.id == country_id))
    country = result.scalar_one_or_none()
    if not country:
        raise HTTPException(404, "Country not found")
    for key, value in request.model_dump(exclude_none=True).items():
        setattr(country, key, value)
    country.updated_by = current_user.id
    await db.flush()
    return {"message": "Country updated"}


@router.delete("/{country_id}")
async def delete_country(
    country_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(Country).where(Country.id == country_id))
    country = result.scalar_one_or_none()
    if not country:
        raise HTTPException(404, "Country not found")
    await db.delete(country)
    await db.flush()
    return {"message": "Country deleted"}
