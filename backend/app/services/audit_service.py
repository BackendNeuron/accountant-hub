
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.models.audit_log import AuditLog


ALWAYS_LOG_ACTIONS = [
    "user.deactivated", "user.deleted", "user.restrictions_updated",
    "job.deleted", "bid.deleted", "content.updated", "content.published",
    "certification.deleted", "audit.toggle_changed",
]


class AuditService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def log(
        self,
        action: str,
        action_category: str,
        entity_type: str,
        entity_id: Optional[int] = None,
        user_id: Optional[int] = None,
        user_email: Optional[str] = None,
        user_role: Optional[str] = None,
        description: Optional[str] = None,
        old_values: Optional[dict] = None,
        new_values: Optional[dict] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        force_log: bool = False,
    ) -> Optional[AuditLog]:
        log_entry = AuditLog(
            user_id=user_id,
            user_email=user_email,
            user_role=user_role,
            action=action,
            action_category=action_category,
            entity_type=entity_type,
            entity_id=entity_id,
            description=description,
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        self.db.add(log_entry)
        await self.db.flush()
        return log_entry
