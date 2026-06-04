
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException
from app.database import get_db
from app.api.deps import require_role
from app.models.uploaded_document import UploadedDocument
from datetime import datetime

router = APIRouter()


@router.get("")
async def list_documents(
    document_type: str = Query(None),
    is_verified: bool = Query(None),
    page: int = Query(1),
    per_page: int = Query(25),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    query = select(UploadedDocument)
    if document_type:
        query = query.where(UploadedDocument.document_type == document_type)
    if is_verified is not None:
        query = query.where(UploadedDocument.is_verified == is_verified)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()

    query = query.order_by(UploadedDocument.uploaded_at.desc()).offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)

    return {"data": result.scalars().all(), "meta": {"page": page, "per_page": per_page, "total": total}}


@router.get("/{document_id}")
async def get_document(
    document_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(UploadedDocument).where(UploadedDocument.id == document_id))
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(404, "Document not found")
    return {"data": doc}


@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(UploadedDocument).where(UploadedDocument.id == document_id))
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(404, "Document not found")
    await db.delete(doc)
    await db.flush()
    return {"message": "Document deleted"}


@router.patch("/{document_id}/verify")
async def verify_document(
    document_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(UploadedDocument).where(UploadedDocument.id == document_id))
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(404, "Document not found")
    doc.is_verified = True
    doc.verified_by = current_user.id
    doc.verified_at = datetime.utcnow()
    await db.flush()
    return {"message": "Document verified"}
