
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.database import get_db
from app.api.deps import get_current_user
from app.services.file_service import FileService
from app.models.uploaded_document import UploadedDocument
from app.models.user import User
from sqlalchemy import select

router = APIRouter()


@router.post("/documents")
async def upload_document(
    file: UploadFile = File(...),
    document_type: str = "other",
    entity_type: str = None,
    entity_id: int = None,
    description: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    file_data = await FileService.save_upload(file)
    document = UploadedDocument(
        user_id=current_user.id,
        document_type=document_type,
        file_name=file_data["file_name"],
        file_url=file_data["file_url"],
        file_size=file_data["file_size"],
        file_type=file_data["file_type"],
        entity_type=entity_type,
        entity_id=entity_id,
        description=description,
    )
    db.add(document)
    await db.flush()
    return {"message": "Document uploaded successfully", "data": {"id": document.id, "file_url": document.file_url}}


@router.get("/documents")
async def list_my_documents(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(UploadedDocument).where(UploadedDocument.user_id == current_user.id).order_by(UploadedDocument.uploaded_at.desc())
    )
    documents = result.scalars().all()
    return {"data": documents}


@router.delete("/documents/{document_id}")
async def delete_document(
    document_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(UploadedDocument).where(UploadedDocument.id == document_id, UploadedDocument.user_id == current_user.id)
    )
    document = result.scalar_one_or_none()
    if not document:
        raise HTTPException(404, "Document not found")
    await db.delete(document)
    await db.flush()
    return {"message": "Document deleted successfully"}
