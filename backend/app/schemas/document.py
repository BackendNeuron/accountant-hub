
from typing import Optional
from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: int
    user_id: int
    document_type: str
    file_name: str
    file_url: str
    file_size: Optional[int] = None
    entity_type: Optional[str] = None
    entity_id: Optional[int] = None
    description: Optional[str] = None
    is_verified: bool
    uploaded_at: str

    class Config:
        from_attributes = True
