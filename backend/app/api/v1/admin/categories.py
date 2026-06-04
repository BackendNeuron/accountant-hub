
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.database import get_db
from app.api.deps import require_role
from app.models.category import Category
from app.schemas.category import CategoryCreateRequest

router = APIRouter()


@router.get("")
async def list_categories(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(Category).order_by(Category.sort_order))
    return {"data": result.scalars().all()}


@router.get("/{category_id}")
async def get_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(404, "Category not found")
    return {"data": category}


@router.post("")
async def create_category(
    request: CategoryCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    existing = await db.execute(select(Category).where(Category.slug == request.slug))
    if existing.scalar_one_or_none():
        raise HTTPException(409, "Slug already exists")
    category = Category(**request.model_dump(), created_by=current_user.id)
    db.add(category)
    await db.flush()
    return {"message": "Category created", "data": {"id": category.id}}


@router.put("/{category_id}")
async def update_category(
    category_id: int,
    request: CategoryCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(404, "Category not found")
    for key, value in request.model_dump(exclude_none=True).items():
        setattr(category, key, value)
    category.updated_by = current_user.id
    await db.flush()
    return {"message": "Category updated"}


@router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(404, "Category not found")
    try:
        await db.delete(category)
        await db.flush()
    except Exception:
        raise HTTPException(400, 'Cannot delete this category because it has jobs assigned to it. Reassign those jobs first.')
    return {"message": "Category deleted"}
