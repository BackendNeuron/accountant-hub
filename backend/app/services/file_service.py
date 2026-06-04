
import os
import uuid
from fastapi import UploadFile, HTTPException
from app.config import settings


ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx", ".png", ".jpg", ".jpeg"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


class FileService:
    @staticmethod
    async def save_upload(upload_file: UploadFile, subdirectory: str = "documents") -> dict:
        ext = os.path.splitext(upload_file.filename or "")[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(400, f"File type {ext} not allowed")

        contents = await upload_file.read()
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(400, "File size exceeds 10MB limit")

        unique_name = f"{uuid.uuid4()}{ext}"
        upload_dir = os.path.join(settings.UPLOAD_DIR, subdirectory)
        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, unique_name)
        with open(file_path, "wb") as f:
            f.write(contents)

        return {
            "file_name": upload_file.filename,
            "file_url": f"/{upload_dir}/{unique_name}",
            "file_size": len(contents),
            "file_type": upload_file.content_type or ext,
        }
