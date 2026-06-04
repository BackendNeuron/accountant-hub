
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException
from app.database import get_db
from app.api.deps import require_role
from app.models.user import User
from app.schemas.user import UserUpdateRequest
from app.utils.security import hash_password
from pydantic import BaseModel

router = APIRouter()


class AdminCreateUserRequest(BaseModel):
    name: str
    email: str
    phone: str
    password: str
    role: str


@router.get("")
async def list_users(
    role: str = Query(None),
    is_active: bool = Query(None),
    search: str = Query(None),
    page: int = Query(1),
    per_page: int = Query(25),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    query = select(User)
    if role:
        query = query.where(User.role == role)
    if is_active is not None:
        query = query.where(User.is_active == is_active)
    if search:
        query = query.where(User.email.ilike(f"%{search}%") | User.name.ilike(f"%{search}%"))

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()

    query = query.order_by(User.created_at.desc()).offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)

    return {"data": result.scalars().all(), "meta": {"page": page, "per_page": per_page, "total": total}}


@router.get("/{user_id}")
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, "User not found")
    return {"data": user}


@router.post("")
async def create_user(
    request: AdminCreateUserRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    existing = await db.execute(select(User).where(User.email == request.email))
    if existing.scalar_one_or_none():
        raise HTTPException(409, "Email already registered")
    existing = await db.execute(select(User).where(User.phone == request.phone))
    if existing.scalar_one_or_none():
        raise HTTPException(409, "Phone already registered")

    user = User(
        name=request.name,
        email=request.email,
        phone=request.phone,
        password=hash_password(request.password),
        role=request.role,
        created_by=current_user.id,
    )
    db.add(user)
    await db.flush()
    return {"message": "User created", "data": {"id": user.id}}


@router.put("/{user_id}")
async def update_user(
    user_id: int,
    request: UserUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, "User not found")

    if request.name is not None:
        user.name = request.name
    if request.phone is not None:
        user.phone = request.phone
    if request.is_active is not None:
        user.is_active = request.is_active
    user.updated_by = current_user.id
    await db.flush()
    return {"message": "User updated", "data": {"id": user.id}}


@router.delete("/{user_id}")
async def deactivate_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, "User not found")
    if user.id == current_user.id:
        raise HTTPException(400, "Cannot deactivate yourself")
    user.is_active = False
    user.updated_by = current_user.id
    await db.flush()
    return {"message": "User deactivated"}

@router.patch("/{user_id}/activate")
async def activate_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, "User not found")
    user.is_active = True
    user.updated_by = current_user.id
    await db.flush()
    return {"message": "User activated"}

