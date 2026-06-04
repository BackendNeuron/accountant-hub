from fastapi import APIRouter
from app.api.v1 import auth, jobs, bids, categories, certifications, countries, content, profile
from app.api.v1 import nda, match, documents, client_jobs, accountants
from app.api.v1.admin.router import admin_router

api_v1_router = APIRouter()

# Public
api_v1_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_v1_router.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
api_v1_router.include_router(categories.router, prefix="/categories", tags=["Categories"])
api_v1_router.include_router(certifications.router, prefix="/certifications", tags=["Certifications"])
api_v1_router.include_router(countries.router, prefix="/countries", tags=["Countries"])
api_v1_router.include_router(content.router, prefix="/content", tags=["Content"])

# Accountant
api_v1_router.include_router(nda.router, prefix="/jobs", tags=["NDA"])
api_v1_router.include_router(bids.router, prefix="/jobs", tags=["Bids"])
api_v1_router.include_router(bids.router, prefix="", tags=["My Bids"])
api_v1_router.include_router(match.router, prefix="/jobs", tags=["Match"])
api_v1_router.include_router(profile.router, prefix="/my-profile", tags=["Profile"])
api_v1_router.include_router(documents.router, prefix="/my-profile", tags=["Documents"])

# Client
api_v1_router.include_router(client_jobs.router, prefix="/my-jobs", tags=["My Jobs"])
api_v1_router.include_router(accountants.router, prefix="/accountants", tags=["Accountants"])

# Admin
api_v1_router.include_router(admin_router, prefix="/admin", tags=["Admin"])
