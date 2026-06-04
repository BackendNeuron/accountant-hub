
from typing import Optional
from pydantic import BaseModel


class PlatformContentResponse(BaseModel):
    key: str
    title: Optional[str] = None
    body: str
    content_type: str
    version: str

    class Config:
        from_attributes = True


class PlatformContentUpdateRequest(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    content_type: Optional[str] = None
