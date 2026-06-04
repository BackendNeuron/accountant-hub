
from typing import Optional
from pydantic import BaseModel


class RestrictionsUpdate(BaseModel):
    can_submit_bids: Optional[bool] = True
    can_view_jobs: Optional[bool] = True
    can_view_nda_jobs: Optional[bool] = True
    can_upload_documents: Optional[bool] = True
    can_edit_profile: Optional[bool] = True
    can_login: Optional[bool] = True
    restricted_reason: Optional[str] = None


class AuditToggleUpdate(BaseModel):
    audit_enabled: bool
