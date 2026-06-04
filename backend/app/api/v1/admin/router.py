from fastapi import APIRouter
from app.api.v1.admin import (
    dashboard, users, jobs, bids, categories, certifications,
    software_skills, countries, documents, content, audit_logs, restrictions,
)

admin_router = APIRouter()

admin_router.include_router(dashboard.router, tags=["Admin - Dashboard"])
admin_router.include_router(users.router, prefix="/users", tags=["Admin - Users"])
admin_router.include_router(jobs.router, prefix="/jobs", tags=["Admin - Jobs"])
admin_router.include_router(bids.router, prefix="/bids", tags=["Admin - Bids"])
admin_router.include_router(categories.router, prefix="/categories", tags=["Admin - Categories"])
admin_router.include_router(certifications.router, prefix="/certifications", tags=["Admin - Certifications"])
admin_router.include_router(software_skills.router, prefix="/software-skills", tags=["Admin - Software Skills"])
admin_router.include_router(countries.router, prefix="/countries", tags=["Admin - Countries"])
admin_router.include_router(documents.router, prefix="/documents", tags=["Admin - Documents"])
admin_router.include_router(content.router, prefix="/content", tags=["Admin - Content"])
admin_router.include_router(audit_logs.router, prefix="/audit-logs", tags=["Admin - Audit Logs"])
admin_router.include_router(restrictions.router, prefix="", tags=["Admin - Restrictions"])
