
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.services.audit_service import AuditService


class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        # Audit logging is handled at the service level for precise control
        return response
