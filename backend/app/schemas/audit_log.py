
from typing import Optional
from pydantic import BaseModel


class AuditLogResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    user_email: Optional[str] = None
    user_role: Optional[str] = None
    action: str
    action_category: str
    entity_type: str
    entity_id: Optional[int] = None
    description: Optional[str] = None
    old_values: Optional[dict] = None
    new_values: Optional[dict] = None
    ip_address: Optional[str] = None
    created_at: str

    class Config:
        from_attributes = True


class AuditLogFilterParams(BaseModel):
    action_category: Optional[str] = None
    action: Optional[str] = None
    user_role: Optional[str] = None
    entity_type: Optional[str] = None
    entity_id: Optional[int] = None
    search: Optional[str] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    page: int = 1
    per_page: int = 25
