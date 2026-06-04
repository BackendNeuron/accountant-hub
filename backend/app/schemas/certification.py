
from typing import Optional
from pydantic import BaseModel


class CertificationResponse(BaseModel):
    id: int
    name: str
    issuing_body: Optional[str] = None
    region: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True


class CertificationCreateRequest(BaseModel):
    name: str
    issuing_body: Optional[str] = None
    region: Optional[str] = None
