
from typing import Optional
from pydantic import BaseModel


class SoftwareSkillResponse(BaseModel):
    id: int
    name: str
    is_active: bool

    class Config:
        from_attributes = True


class SoftwareSkillCreateRequest(BaseModel):
    name: str


class SoftwareSkillUpdateRequest(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None
