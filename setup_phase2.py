"""
Accountant Hub - Setup Phase II
Completes all missing endpoints, services, and logic
Run: python setup_phase2.py
"""
import os
import sys
import py_compile
import traceback

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ERRORS = []
CREATED = []
MODIFIED = []


def write_file(filepath: str, content: str):
    """Write content to a file, creating directories if needed."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    existed = os.path.exists(filepath)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    if existed:
        MODIFIED.append(filepath)
    else:
        CREATED.append(filepath)
    print(f"  {'🔧' if existed else '✅'} {'Updated' if existed else 'Created'}: {os.path.relpath(filepath, BASE_DIR)}")


def verify_file(filepath: str):
    """Try to compile a Python file to check for syntax errors."""
    try:
        py_compile.compile(filepath, doraise=True)
        print(f"  ✅ Verified: {os.path.relpath(filepath, BASE_DIR)}")
        return True
    except py_compile.PyCompileError as e:
        print(f"  ❌ SYNTAX ERROR in {os.path.relpath(filepath, BASE_DIR)}: {e}")
        ERRORS.append((filepath, str(e)))
        return False


def create_missing_services():
    """Step 1: Create missing services."""
    print("\n" + "="*60)
    print("STEP 1: Missing Services (ClientService)")
    print("="*60)

    write_file("app/services/client_service.py", CLIENT_SERVICE_PY)
    verify_file("app/services/client_service.py")

    write_file("app/services/nda_service.py", NDA_SERVICE_PY)
    verify_file("app/services/nda_service.py")

    # Update match_service with full logic
    write_file("app/services/match_service.py", MATCH_SERVICE_FULL_PY)
    verify_file("app/services/match_service.py")

    # Update bid_service with accept/reject
    write_file("app/services/bid_service.py", BID_SERVICE_FULL_PY)
    verify_file("app/services/bid_service.py")


def create_missing_schemas():
    """Step 2: Create missing schemas."""
    print("\n" + "="*60)
    print("STEP 2: Missing Schemas")
    print("="*60)

    write_file("app/schemas/client.py", CLIENT_SCHEMA_PY)
    verify_file("app/schemas/client.py")

    write_file("app/schemas/nda.py", NDA_SCHEMA_PY)
    verify_file("app/schemas/nda.py")

    write_file("app/schemas/restrictions.py", RESTRICTIONS_SCHEMA_PY)
    verify_file("app/schemas/restrictions.py")

    write_file("app/schemas/software_skill.py", SOFTWARE_SKILL_SCHEMA_PY)
    verify_file("app/schemas/software_skill.py")


def create_accountant_endpoints():
    """Step 3: Missing accountant endpoints."""
    print("\n" + "="*60)
    print("STEP 3: Missing Accountant Endpoints")
    print("="*60)

    write_file("app/api/v1/nda.py", NDA_ROUTES_PY)
    verify_file("app/api/v1/nda.py")

    write_file("app/api/v1/match.py", MATCH_ROUTES_PY)
    verify_file("app/api/v1/match.py")

    write_file("app/api/v1/documents.py", DOCUMENTS_ROUTES_PY)
    verify_file("app/api/v1/documents.py")

    # Update profile.py with full CRUD
    write_file("app/api/v1/profile.py", PROFILE_FULL_PY)
    verify_file("app/api/v1/profile.py")


def create_client_endpoints():
    """Step 4: Create client routes."""
    print("\n" + "="*60)
    print("STEP 4: Client Routes (my-jobs, accept/reject bids)")
    print("="*60)

    write_file("app/api/v1/client_jobs.py", CLIENT_JOBS_ROUTES_PY)
    verify_file("app/api/v1/client_jobs.py")


def fill_admin_crud():
    """Step 5: Fill all admin CRUD stubs with real logic."""
    print("\n" + "="*60)
    print("STEP 5: Admin CRUD - Full Implementations")
    print("="*60)

    write_file("app/api/v1/admin/users.py", ADMIN_USERS_FULL_PY)
    verify_file("app/api/v1/admin/users.py")

    write_file("app/api/v1/admin/jobs.py", ADMIN_JOBS_FULL_PY)
    verify_file("app/api/v1/admin/jobs.py")

    write_file("app/api/v1/admin/bids.py", ADMIN_BIDS_FULL_PY)
    verify_file("app/api/v1/admin/bids.py")

    write_file("app/api/v1/admin/categories.py", ADMIN_CATEGORIES_FULL_PY)
    verify_file("app/api/v1/admin/categories.py")

    write_file("app/api/v1/admin/certifications.py", ADMIN_CERTIFICATIONS_FULL_PY)
    verify_file("app/api/v1/admin/certifications.py")

    write_file("app/api/v1/admin/software_skills.py", ADMIN_SOFTWARE_SKILLS_FULL_PY)
    verify_file("app/api/v1/admin/software_skills.py")

    write_file("app/api/v1/admin/countries.py", ADMIN_COUNTRIES_FULL_PY)
    verify_file("app/api/v1/admin/countries.py")

    write_file("app/api/v1/admin/documents.py", ADMIN_DOCUMENTS_FULL_PY)
    verify_file("app/api/v1/admin/documents.py")

    write_file("app/api/v1/admin/content.py", ADMIN_CONTENT_FULL_PY)
    verify_file("app/api/v1/admin/content.py")

    write_file("app/api/v1/admin/audit_logs.py", ADMIN_AUDIT_LOGS_FULL_PY)
    verify_file("app/api/v1/admin/audit_logs.py")


def update_router():
    """Step 6: Update v1 router with new routes."""
    print("\n" + "="*60)
    print("STEP 6: Update API Router")
    print("="*60)

    write_file("app/api/v1/router.py", V1_ROUTER_FULL_PY)
    verify_file("app/api/v1/router.py")


def create_migration():
    """Step 7: Create the full SQL migration file."""
    print("\n" + "="*60)
    print("STEP 7: Full Database Migration SQL")
    print("="*60)

    write_file("migrations/001_initial_schema.sql", MIGRATION_SQL)
    print(f"  ✅ Created: migrations/001_initial_schema.sql")


def print_summary():
    """Print final summary."""
    print("\n" + "="*60)
    print("PHASE II SETUP COMPLETE")
    print("="*60)

    if CREATED:
        print(f"\n📁 {len(CREATED)} new files created:")
        for f in CREATED:
            print(f"   + {os.path.relpath(f, BASE_DIR)}")

    if MODIFIED:
        print(f"\n🔧 {len(MODIFIED)} files updated:")
        for f in MODIFIED:
            print(f"   ~ {os.path.relpath(f, BASE_DIR)}")

    if ERRORS:
        print(f"\n❌ {len(ERRORS)} SYNTAX ERROR(S):")
        for filepath, error in ERRORS:
            print(f"   - {os.path.relpath(filepath, BASE_DIR)}: {error}")
    else:
        print(f"\n✅ ALL FILES VERIFIED — NO SYNTAX ERRORS")

    print(f"\nNext steps:")
    print(f"  1. Create DB: psql -U postgres -c \"CREATE DATABASE accountant_hub;\"")
    print(f"  2. Run migration: psql -U postgres -d accountant_hub -f migrations/001_initial_schema.sql")
    print(f"  3. Run seeders: python seeders/seed_all.py")
    print(f"  4. Start server: uvicorn app.main:app --reload")
    print("="*60)


# ============================================================
# MISSING SERVICES
# ============================================================

CLIENT_SERVICE_PY = '''
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from fastapi import HTTPException
from app.models.job import Job
from app.models.bid import Bid
from app.models.user import User
from app.models.client_profile import ClientProfile
from sqlalchemy.orm import joinedload


class ClientService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_job(self, client: User, job_data: dict) -> Job:
        job = Job(client_id=client.id, **job_data)
        self.db.add(job)
        await self.db.flush()
        return job

    async def list_my_jobs(self, client_id: int, page: int = 1, per_page: int = 12) -> tuple[list[Job], int]:
        query = select(Job).where(Job.client_id == client_id).options(
            joinedload(Job.category)
        ).order_by(Job.created_at.desc())

        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar()

        query = query.offset((page - 1) * per_page).limit(per_page)
        result = await self.db.execute(query)
        jobs = result.unique().scalars().all()

        return jobs, total

    async def get_my_job(self, job_id: int, client_id: int) -> Job:
        result = await self.db.execute(
            select(Job)
            .options(joinedload(Job.category), joinedload(Job.client).joinedload(User.client_profile))
            .where(Job.id == job_id, Job.client_id == client_id)
        )
        job = result.unique().scalar_one_or_none()
        if not job:
            raise HTTPException(404, "Job not found")
        return job

    async def update_my_job(self, job_id: int, client_id: int, update_data: dict) -> Job:
        job = await self.get_my_job(job_id, client_id)
        if job.status == "closed":
            raise HTTPException(400, "Cannot update a closed job")
        for key, value in update_data.items():
            if value is not None and hasattr(job, key):
                setattr(job, key, value)
        await self.db.flush()
        return job

    async def update_job_status(self, job_id: int, client_id: int, status: str, closed_reason: str = None) -> Job:
        job = await self.get_my_job(job_id, client_id)
        job.status = status
        if status == "closed" and closed_reason:
            job.closed_reason = closed_reason
        await self.db.flush()
        return job

    async def get_job_bids(self, job_id: int, client_id: int) -> list[Bid]:
        job = await self.get_my_job(job_id, client_id)
        result = await self.db.execute(
            select(Bid)
            .options(joinedload(Bid.accountant))
            .where(Bid.job_id == job_id)
            .order_by(Bid.created_at.desc())
        )
        return result.unique().scalars().all()

    async def accept_bid(self, job_id: int, bid_id: int, client_id: int) -> Bid:
        job = await self.get_my_job(job_id, client_id)
        if job.status != "open":
            raise HTTPException(400, "Job is not open")

        result = await self.db.execute(
            select(Bid).where(Bid.id == bid_id, Bid.job_id == job_id)
        )
        bid = result.scalar_one_or_none()
        if not bid:
            raise HTTPException(404, "Bid not found")
        if bid.status != "pending":
            raise HTTPException(400, f"Bid is already {bid.status}")

        from datetime import datetime
        bid.status = "accepted"
        bid.accepted_at = datetime.utcnow()

        # Close the job
        job.status = "closed"
        job.closed_reason = "bid_accepted"

        # Reject all other pending bids
        await self.db.execute(
            update(Bid)
            .where(Bid.job_id == job_id, Bid.id != bid_id, Bid.status == "pending")
            .values(status="rejected", rejected_at=datetime.utcnow())
        )

        await self.db.flush()
        return bid

    async def reject_bid(self, job_id: int, bid_id: int, client_id: int) -> Bid:
        job = await self.get_my_job(job_id, client_id)
        result = await self.db.execute(
            select(Bid).where(Bid.id == bid_id, Bid.job_id == job_id)
        )
        bid = result.scalar_one_or_none()
        if not bid:
            raise HTTPException(404, "Bid not found")
        if bid.status != "pending":
            raise HTTPException(400, f"Bid is already {bid.status}")

        from datetime import datetime
        bid.status = "rejected"
        bid.rejected_at = datetime.utcnow()
        await self.db.flush()
        return bid
'''

NDA_SERVICE_PY = '''
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.job import Job
from app.models.nda_acceptance import NDAAcceptance
from app.models.user import User


class NDAService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def accept_nda(self, job_id: int, user: User, ip_address: str = None) -> NDAAcceptance:
        result = await self.db.execute(select(Job).where(Job.id == job_id))
        job = result.scalar_one_or_none()
        if not job:
            raise HTTPException(404, "Job not found")
        if not job.nda_required:
            raise HTTPException(400, "This job does not require an NDA")

        existing = await self.db.execute(
            select(NDAAcceptance).where(
                NDAAcceptance.job_id == job_id,
                NDAAcceptance.user_id == user.id
            )
        )
        if existing.scalar_one_or_none():
            return existing.scalar_one()

        nda = NDAAcceptance(
            user_id=user.id,
            job_id=job_id,
            ip_address=ip_address,
        )
        self.db.add(nda)
        await self.db.flush()
        return nda

    async def has_accepted_nda(self, job_id: int, user_id: int) -> bool:
        result = await self.db.execute(
            select(NDAAcceptance).where(
                NDAAcceptance.job_id == job_id,
                NDAAcceptance.user_id == user_id
            )
        )
        return result.scalar_one_or_none() is not None
'''

MATCH_SERVICE_FULL_PY = '''
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.models.job import Job
from app.models.user import User
from app.models.accountant_profile import AccountantProfile
from app.models.accountant_certification import AccountantCertification
from app.models.certification import Certification
from app.models.accountant_software_skill import AccountantSoftwareSkill
from app.models.software_skill import SoftwareSkill


class MatchService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def calculate_match(self, job_id: int, accountant: User) -> dict:
        result = await self.db.execute(select(Job).where(Job.id == job_id))
        job = result.scalar_one_or_none()

        if not job or accountant.role != "accountant":
            return {"score": 0, "matched": [], "missing": [], "warnings": []}

        profile_result = await self.db.execute(
            select(AccountantProfile)
            .options(
                joinedload(AccountantProfile.certifications).joinedload(AccountantCertification.certification),
                joinedload(AccountantProfile.software_skills).joinedload(AccountantSoftwareSkill.software_skill),
            )
            .where(AccountantProfile.user_id == accountant.id)
        )
        profile = profile_result.unique().scalar_one_or_none()

        if not profile:
            return {
                "score": 0,
                "matched": [],
                "missing": ["Complete your profile to see match scores"],
                "warnings": ["Profile incomplete — complete it to increase your chances"],
            }

        matched = []
        missing = []
        warnings = []
        total_checks = 0

        # Check certifications
        if job.required_certifications and len(job.required_certifications) > 0:
            total_checks += len(job.required_certifications)
            accountant_cert_names = []
            if profile.certifications:
                from datetime import date
                for ac in profile.certifications:
                    cert_name = ac.certification.name if ac.certification else ac.custom_certification_name
                    if cert_name:
                        # Check expiry
                        if ac.expiry_date and ac.expiry_date < date.today():
                            warnings.append(f"Certification '{cert_name}' is expired")
                            continue
                        if ac.expiry_date and (ac.expiry_date - date.today()).days <= 30:
                            warnings.append(f"Certification '{cert_name}' expires soon")
                        accountant_cert_names.append(cert_name)

            for req_cert in job.required_certifications:
                if req_cert in accountant_cert_names:
                    matched.append(f"Certification: {req_cert}")
                else:
                    missing.append(f"Certification: {req_cert}")

        # Check software skills
        if job.required_software and len(job.required_software) > 0:
            total_checks += len(job.required_software)
            accountant_software_names = []
            if profile.software_skills:
                for ass in profile.software_skills:
                    if ass.software_skill:
                        accountant_software_names.append(ass.software_skill.name)

            for req_sw in job.required_software:
                if req_sw in accountant_software_names:
                    matched.append(f"Software: {req_sw}")
                else:
                    missing.append(f"Software: {req_sw}")

        # Check jurisdiction
        if job.jurisdiction:
            total_checks += 1
            if profile.jurisdictions_served and job.jurisdiction in profile.jurisdictions_served:
                matched.append(f"Jurisdiction: {job.jurisdiction}")
            else:
                missing.append(f"Jurisdiction: {job.jurisdiction}")
                warnings.append(f"This job requires {job.jurisdiction} jurisdiction — not in your profile")

        # Check accounting standard
        if job.accounting_standard:
            total_checks += 1
            if profile.accounting_standards and job.accounting_standard in profile.accounting_standards:
                matched.append(f"Standard: {job.accounting_standard}")
            else:
                missing.append(f"Standard: {job.accounting_standard}")

        # Check experience
        if job.minimum_experience_years:
            total_checks += 1
            if profile.years_of_experience and profile.years_of_experience >= job.minimum_experience_years:
                matched.append(f"Experience: {profile.years_of_experience} years (requires {job.minimum_experience_years})")
            else:
                missing.append(f"Experience: Requires {job.minimum_experience_years}+ years")

        score = round((len(matched) / total_checks * 100)) if total_checks > 0 else 100

        return {
            "score": score,
            "matched": matched,
            "missing": missing,
            "warnings": warnings,
        }
'''

BID_SERVICE_FULL_PY = '''
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from fastapi import HTTPException
from datetime import date
from app.models.job import Job
from app.models.bid import Bid
from app.models.user import User


class BidService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def submit_bid(self, job_id: int, accountant: User, bid_data: dict) -> Bid:
        result = await self.db.execute(select(Job).where(Job.id == job_id))
        job = result.scalar_one_or_none()

        if not job:
            raise HTTPException(404, "Job not found")

        if job.status != "open":
            raise HTTPException(400, "This job is closed and no longer accepting bids")

        if job.deadline and job.deadline < date.today():
            raise HTTPException(400, "The deadline for this job has passed")

        # Check restrictions
        if accountant.restrictions:
            restrictions = accountant.restrictions
            if restrictions.get("can_submit_bids") == False:
                reason = restrictions.get("restricted_reason", "Your account has restricted bidding")
                raise HTTPException(403, reason)

        existing = await self.db.execute(
            select(Bid).where(Bid.job_id == job_id, Bid.accountant_id == accountant.id)
        )
        if existing.scalar_one_or_none():
            raise HTTPException(409, "You have already submitted a bid for this job")

        bid = Bid(
            job_id=job_id,
            accountant_id=accountant.id,
            currency=job.currency,
            **bid_data
        )
        self.db.add(bid)

        job.bids_count = (job.bids_count or 0) + 1
        if job.bids_min_price is None or bid_data["price"] < job.bids_min_price:
            job.bids_min_price = bid_data["price"]
        if job.bids_max_price is None or bid_data["price"] > job.bids_max_price:
            job.bids_max_price = bid_data["price"]

        await self.db.flush()
        return bid

    async def get_my_bids(self, accountant_id: int, page: int = 1, per_page: int = 12) -> tuple[list[Bid], int]:
        query = select(Bid).options(
            joinedload(Bid.job)
        ).where(Bid.accountant_id == accountant_id).order_by(Bid.created_at.desc())

        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar()

        query = query.offset((page - 1) * per_page).limit(per_page)
        result = await self.db.execute(query)
        bids = result.unique().scalars().all()

        return bids, total
'''

# ============================================================
# MISSING SCHEMAS
# ============================================================

CLIENT_SCHEMA_PY = '''
from typing import Optional
from decimal import Decimal
from datetime import date
from pydantic import BaseModel, Field


class JobCreateRequest(BaseModel):
    title: str = Field(..., min_length=5, max_length=255)
    description: str = Field(..., min_length=50)
    category_id: int
    budget_min: Decimal = Field(..., gt=0)
    budget_max: Decimal = Field(..., gt=0)
    currency: str = "USD"
    pricing_model: str = Field(..., pattern="^(fixed|hourly|retainer)$")
    deadline: date
    expected_delivery_time: Optional[str] = None
    engagement_type: str = "one_time"
    jurisdiction: Optional[str] = None
    accounting_standard: Optional[str] = None
    required_certifications: Optional[list[str]] = None
    required_software: Optional[list[str]] = None
    required_skills: Optional[list[str]] = None
    minimum_experience_years: Optional[int] = None
    company_industry_context: Optional[str] = None
    nda_required: bool = False


class JobUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    budget_min: Optional[Decimal] = None
    budget_max: Optional[Decimal] = None
    currency: Optional[str] = None
    pricing_model: Optional[str] = None
    deadline: Optional[date] = None
    expected_delivery_time: Optional[str] = None
    engagement_type: Optional[str] = None
    jurisdiction: Optional[str] = None
    accounting_standard: Optional[str] = None
    required_certifications: Optional[list[str]] = None
    required_software: Optional[list[str]] = None
    required_skills: Optional[list[str]] = None
    minimum_experience_years: Optional[int] = None
    nda_required: Optional[bool] = None


class JobStatusUpdateRequest(BaseModel):
    status: str = Field(..., pattern="^(open|closed)$")
    closed_reason: Optional[str] = None
'''

NDA_SCHEMA_PY = '''
from pydantic import BaseModel


class NDAAcceptRequest(BaseModel):
    agree: bool = True


class NDAResponse(BaseModel):
    message: str
    accepted: bool
    job_id: int
'''

RESTRICTIONS_SCHEMA_PY = '''
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
'''

SOFTWARE_SKILL_SCHEMA_PY = '''
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
'''

# ============================================================
# MISSING ACCOUNTANT ENDPOINTS
# ============================================================

NDA_ROUTES_PY = '''
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.api.deps import require_role, get_current_user
from app.services.nda_service import NDAService
from app.models.user import User

router = APIRouter()


@router.post("/{job_id}/accept-nda")
async def accept_nda(
    job_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("accountant")),
):
    service = NDAService(db)
    ip_address = request.client.host if request.client else None
    nda = await service.accept_nda(job_id, current_user, ip_address)
    return {
        "message": "NDA accepted successfully",
        "accepted": True,
        "job_id": job_id,
    }
'''

MATCH_ROUTES_PY = '''
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.api.deps import require_role, get_current_user
from app.services.match_service import MatchService
from app.models.user import User

router = APIRouter()


@router.get("/{job_id}/match-score")
async def get_match_score(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("accountant")),
):
    service = MatchService(db)
    result = await service.calculate_match(job_id, current_user)
    return {"data": result}
'''

DOCUMENTS_ROUTES_PY = '''
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.database import get_db
from app.api.deps import get_current_user
from app.services.file_service import FileService
from app.models.uploaded_document import UploadedDocument
from app.models.user import User
from sqlalchemy import select

router = APIRouter()


@router.post("/documents")
async def upload_document(
    file: UploadFile = File(...),
    document_type: str = "other",
    entity_type: str = None,
    entity_id: int = None,
    description: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    file_data = await FileService.save_upload(file)
    document = UploadedDocument(
        user_id=current_user.id,
        document_type=document_type,
        file_name=file_data["file_name"],
        file_url=file_data["file_url"],
        file_size=file_data["file_size"],
        file_type=file_data["file_type"],
        entity_type=entity_type,
        entity_id=entity_id,
        description=description,
    )
    db.add(document)
    await db.flush()
    return {"message": "Document uploaded successfully", "data": {"id": document.id, "file_url": document.file_url}}


@router.get("/documents")
async def list_my_documents(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(UploadedDocument).where(UploadedDocument.user_id == current_user.id).order_by(UploadedDocument.uploaded_at.desc())
    )
    documents = result.scalars().all()
    return {"data": documents}


@router.delete("/documents/{document_id}")
async def delete_document(
    document_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(UploadedDocument).where(UploadedDocument.id == document_id, UploadedDocument.user_id == current_user.id)
    )
    document = result.scalar_one_or_none()
    if not document:
        raise HTTPException(404, "Document not found")
    await db.delete(document)
    await db.flush()
    return {"message": "Document deleted successfully"}
'''

PROFILE_FULL_PY = '''
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.accountant_profile import AccountantProfile
from app.models.client_profile import ClientProfile
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class AccountantProfileUpdate(BaseModel):
    bio: Optional[str] = None
    years_of_experience: Optional[int] = None
    hourly_rate: Optional[float] = None
    jurisdictions_served: Optional[list[str]] = None
    accounting_standards: Optional[list[str]] = None
    education_summary: Optional[str] = None


class ClientProfileUpdate(BaseModel):
    company_name: Optional[str] = None
    company_industry: Optional[str] = None
    company_size: Optional[str] = None
    company_description: Optional[str] = None
    website: Optional[str] = None
    country_id: Optional[int] = None
    city: Optional[str] = None


@router.get("")
async def get_my_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    response = {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "phone": current_user.phone,
        "role": current_user.role,
        "is_active": current_user.is_active,
    }

    if current_user.role == "accountant":
        result = await db.execute(
            select(AccountantProfile).where(AccountantProfile.user_id == current_user.id)
        )
        profile = result.scalar_one_or_none()
        if profile:
            response["profile"] = profile

    elif current_user.role == "client":
        result = await db.execute(
            select(ClientProfile).where(ClientProfile.user_id == current_user.id)
        )
        profile = result.scalar_one_or_none()
        if profile:
            response["profile"] = profile

    return {"data": response}


@router.put("")
async def update_my_profile(
    update_data: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == "accountant":
        result = await db.execute(
            select(AccountantProfile).where(AccountantProfile.user_id == current_user.id)
        )
        profile = result.scalar_one_or_none()
        if not profile:
            profile = AccountantProfile(user_id=current_user.id)
            db.add(profile)

        allowed_fields = ["bio", "years_of_experience", "hourly_rate", "jurisdictions_served", "accounting_standards", "education_summary"]
        for key, value in update_data.items():
            if key in allowed_fields and value is not None:
                setattr(profile, key, value)
        profile.profile_completed = True

    elif current_user.role == "client":
        result = await db.execute(
            select(ClientProfile).where(ClientProfile.user_id == current_user.id)
        )
        profile = result.scalar_one_or_none()
        if not profile:
            profile = ClientProfile(user_id=current_user.id)
            db.add(profile)

        allowed_fields = ["company_name", "company_industry", "company_size", "company_description", "website", "country_id", "city"]
        for key, value in update_data.items():
            if key in allowed_fields and value is not None:
                setattr(profile, key, value)
        profile.profile_completed = True

    await db.flush()
    return {"message": "Profile updated successfully"}
'''

# ============================================================
# CLIENT ROUTES
# ============================================================

CLIENT_JOBS_ROUTES_PY = '''
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.api.deps import require_role, get_current_user
from app.services.client_service import ClientService
from app.schemas.client import JobCreateRequest, JobUpdateRequest, JobStatusUpdateRequest
from app.models.user import User

router = APIRouter()


@router.post("")
async def create_job(
    request: JobCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("client")),
):
    service = ClientService(db)
    job = await service.create_job(current_user, request.model_dump())
    return {"message": "Job created successfully", "data": {"id": job.id}}


@router.get("")
async def list_my_jobs(
    page: int = Query(1),
    per_page: int = Query(12),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("client")),
):
    service = ClientService(db)
    jobs, total = await service.list_my_jobs(current_user.id, page, per_page)
    return {"data": jobs, "meta": {"page": page, "per_page": per_page, "total": total}}


@router.get("/{job_id}")
async def get_my_job(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("client")),
):
    service = ClientService(db)
    job = await service.get_my_job(job_id, current_user.id)
    return {"data": job}


@router.put("/{job_id}")
async def update_my_job(
    job_id: int,
    request: JobUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("client")),
):
    service = ClientService(db)
    job = await service.update_my_job(job_id, current_user.id, request.model_dump(exclude_none=True))
    return {"message": "Job updated successfully", "data": job}


@router.patch("/{job_id}/status")
async def update_job_status(
    job_id: int,
    request: JobStatusUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("client")),
):
    service = ClientService(db)
    job = await service.update_job_status(job_id, current_user.id, request.status, request.closed_reason)
    return {"message": f"Job {request.status}", "data": {"id": job.id, "status": job.status}}


@router.get("/{job_id}/bids")
async def get_job_bids(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("client")),
):
    service = ClientService(db)
    bids = await service.get_job_bids(job_id, current_user.id)
    return {"data": bids}


@router.patch("/{job_id}/bids/{bid_id}/accept")
async def accept_bid(
    job_id: int,
    bid_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("client")),
):
    service = ClientService(db)
    bid = await service.accept_bid(job_id, bid_id, current_user.id)
    return {"message": "Bid accepted — job is now closed", "data": {"bid_id": bid.id, "status": bid.status}}


@router.patch("/{job_id}/bids/{bid_id}/reject")
async def reject_bid(
    job_id: int,
    bid_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("client")),
):
    service = ClientService(db)
    bid = await service.reject_bid(job_id, bid_id, current_user.id)
    return {"message": "Bid rejected", "data": {"bid_id": bid.id, "status": bid.status}}
'''

# ============================================================
# ADMIN CRUD - FULL IMPLEMENTATIONS
# ============================================================

ADMIN_USERS_FULL_PY = '''
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException
from app.database import get_db
from app.api.deps import require_role
from app.models.user import User
from app.schemas.user import UserUpdateRequest
from app.utils.security import hash_password
from pydantic import BaseModel

router = APIRouter()


class AdminCreateUserRequest(BaseModel):
    name: str
    email: str
    phone: str
    password: str
    role: str


@router.get("")
async def list_users(
    role: str = Query(None),
    is_active: bool = Query(None),
    search: str = Query(None),
    page: int = Query(1),
    per_page: int = Query(25),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    query = select(User)
    if role:
        query = query.where(User.role == role)
    if is_active is not None:
        query = query.where(User.is_active == is_active)
    if search:
        query = query.where(User.email.ilike(f"%{search}%") | User.name.ilike(f"%{search}%"))

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()

    query = query.order_by(User.created_at.desc()).offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)

    return {"data": result.scalars().all(), "meta": {"page": page, "per_page": per_page, "total": total}}


@router.get("/{user_id}")
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, "User not found")
    return {"data": user}


@router.post("")
async def create_user(
    request: AdminCreateUserRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    existing = await db.execute(select(User).where(User.email == request.email))
    if existing.scalar_one_or_none():
        raise HTTPException(409, "Email already registered")
    existing = await db.execute(select(User).where(User.phone == request.phone))
    if existing.scalar_one_or_none():
        raise HTTPException(409, "Phone already registered")

    user = User(
        name=request.name,
        email=request.email,
        phone=request.phone,
        password=hash_password(request.password),
        role=request.role,
        created_by=current_user.id,
    )
    db.add(user)
    await db.flush()
    return {"message": "User created", "data": {"id": user.id}}


@router.put("/{user_id}")
async def update_user(
    user_id: int,
    request: UserUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, "User not found")

    if request.name is not None:
        user.name = request.name
    if request.phone is not None:
        user.phone = request.phone
    if request.is_active is not None:
        user.is_active = request.is_active
    user.updated_by = current_user.id
    await db.flush()
    return {"message": "User updated", "data": {"id": user.id}}


@router.delete("/{user_id}")
async def deactivate_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, "User not found")
    if user.id == current_user.id:
        raise HTTPException(400, "Cannot deactivate yourself")
    user.is_active = False
    user.updated_by = current_user.id
    await db.flush()
    return {"message": "User deactivated"}
'''

ADMIN_JOBS_FULL_PY = '''
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from fastapi import HTTPException
from app.database import get_db
from app.api.deps import require_role
from app.models.job import Job
from app.models.user import User

router = APIRouter()


@router.get("")
async def list_jobs(
    status: str = Query(None),
    client_id: int = Query(None),
    category_id: int = Query(None),
    page: int = Query(1),
    per_page: int = Query(25),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    query = select(Job).options(joinedload(Job.client), joinedload(Job.category))
    if status:
        query = query.where(Job.status == status)
    if client_id:
        query = query.where(Job.client_id == client_id)
    if category_id:
        query = query.where(Job.category_id == category_id)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()

    query = query.order_by(Job.created_at.desc()).offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)

    return {"data": result.unique().scalars().all(), "meta": {"page": page, "per_page": per_page, "total": total}}


@router.get("/{job_id}")
async def get_job(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(
        select(Job).options(joinedload(Job.client), joinedload(Job.category)).where(Job.id == job_id)
    )
    job = result.unique().scalar_one_or_none()
    if not job:
        raise HTTPException(404, "Job not found")
    return {"data": job}


@router.delete("/{job_id}")
async def delete_job(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(404, "Job not found")
    await db.delete(job)
    await db.flush()
    return {"message": "Job deleted"}


@router.patch("/{job_id}/status")
async def update_job_status(
    job_id: int,
    status: str = Query(..., pattern="^(open|closed)$"),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(404, "Job not found")
    job.status = status
    if status == "closed":
        job.closed_reason = "admin_closed"
    await db.flush()
    return {"message": f"Job {status}"}
'''

ADMIN_BIDS_FULL_PY = '''
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from fastapi import HTTPException
from app.database import get_db
from app.api.deps import require_role
from app.models.bid import Bid

router = APIRouter()


@router.get("")
async def list_bids(
    job_id: int = Query(None),
    accountant_id: int = Query(None),
    status: str = Query(None),
    page: int = Query(1),
    per_page: int = Query(25),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    query = select(Bid).options(joinedload(Bid.job), joinedload(Bid.accountant))
    if job_id:
        query = query.where(Bid.job_id == job_id)
    if accountant_id:
        query = query.where(Bid.accountant_id == accountant_id)
    if status:
        query = query.where(Bid.status == status)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()

    query = query.order_by(Bid.created_at.desc()).offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)

    return {"data": result.unique().scalars().all(), "meta": {"page": page, "per_page": per_page, "total": total}}


@router.get("/{bid_id}")
async def get_bid(
    bid_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(
        select(Bid).options(joinedload(Bid.job), joinedload(Bid.accountant)).where(Bid.id == bid_id)
    )
    bid = result.unique().scalar_one_or_none()
    if not bid:
        raise HTTPException(404, "Bid not found")
    return {"data": bid}


@router.delete("/{bid_id}")
async def delete_bid(
    bid_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(Bid).where(Bid.id == bid_id))
    bid = result.scalar_one_or_none()
    if not bid:
        raise HTTPException(404, "Bid not found")

    # Update job denormalized count
    job = bid.job
    if job:
        job.bids_count = max(0, (job.bids_count or 1) - 1)

    await db.delete(bid)
    await db.flush()
    return {"message": "Bid deleted"}
'''

ADMIN_CATEGORIES_FULL_PY = '''
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.database import get_db
from app.api.deps import require_role
from app.models.category import Category
from app.schemas.category import CategoryCreateRequest

router = APIRouter()


@router.get("")
async def list_categories(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(Category).order_by(Category.sort_order))
    return {"data": result.scalars().all()}


@router.get("/{category_id}")
async def get_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(404, "Category not found")
    return {"data": category}


@router.post("")
async def create_category(
    request: CategoryCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    existing = await db.execute(select(Category).where(Category.slug == request.slug))
    if existing.scalar_one_or_none():
        raise HTTPException(409, "Slug already exists")
    category = Category(**request.model_dump(), created_by=current_user.id)
    db.add(category)
    await db.flush()
    return {"message": "Category created", "data": {"id": category.id}}


@router.put("/{category_id}")
async def update_category(
    category_id: int,
    request: CategoryCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(404, "Category not found")
    for key, value in request.model_dump(exclude_none=True).items():
        setattr(category, key, value)
    category.updated_by = current_user.id
    await db.flush()
    return {"message": "Category updated"}


@router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(404, "Category not found")
    await db.delete(category)
    await db.flush()
    return {"message": "Category deleted"}
'''

ADMIN_CERTIFICATIONS_FULL_PY = '''
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.database import get_db
from app.api.deps import require_role
from app.models.certification import Certification
from app.schemas.certification import CertificationCreateRequest

router = APIRouter()


@router.get("")
async def list_certifications(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(Certification).order_by(Certification.name))
    return {"data": result.scalars().all()}


@router.get("/{cert_id}")
async def get_certification(
    cert_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(Certification).where(Certification.id == cert_id))
    cert = result.scalar_one_or_none()
    if not cert:
        raise HTTPException(404, "Certification not found")
    return {"data": cert}


@router.post("")
async def create_certification(
    request: CertificationCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    existing = await db.execute(select(Certification).where(Certification.name == request.name))
    if existing.scalar_one_or_none():
        raise HTTPException(409, "Certification already exists")
    cert = Certification(**request.model_dump(), created_by=current_user.id)
    db.add(cert)
    await db.flush()
    return {"message": "Certification created", "data": {"id": cert.id}}


@router.put("/{cert_id}")
async def update_certification(
    cert_id: int,
    request: CertificationCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(Certification).where(Certification.id == cert_id))
    cert = result.scalar_one_or_none()
    if not cert:
        raise HTTPException(404, "Certification not found")
    for key, value in request.model_dump(exclude_none=True).items():
        setattr(cert, key, value)
    cert.updated_by = current_user.id
    await db.flush()
    return {"message": "Certification updated"}


@router.delete("/{cert_id}")
async def delete_certification(
    cert_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(Certification).where(Certification.id == cert_id))
    cert = result.scalar_one_or_none()
    if not cert:
        raise HTTPException(404, "Certification not found")
    await db.delete(cert)
    await db.flush()
    return {"message": "Certification deleted"}
'''

ADMIN_SOFTWARE_SKILLS_FULL_PY = '''
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.database import get_db
from app.api.deps import require_role
from app.models.software_skill import SoftwareSkill
from app.schemas.software_skill import SoftwareSkillCreateRequest, SoftwareSkillUpdateRequest

router = APIRouter()


@router.get("")
async def list_software_skills(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(SoftwareSkill).order_by(SoftwareSkill.name))
    return {"data": result.scalars().all()}


@router.get("/{skill_id}")
async def get_software_skill(
    skill_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(SoftwareSkill).where(SoftwareSkill.id == skill_id))
    skill = result.scalar_one_or_none()
    if not skill:
        raise HTTPException(404, "Software skill not found")
    return {"data": skill}


@router.post("")
async def create_software_skill(
    request: SoftwareSkillCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    existing = await db.execute(select(SoftwareSkill).where(SoftwareSkill.name == request.name))
    if existing.scalar_one_or_none():
        raise HTTPException(409, "Software skill already exists")
    skill = SoftwareSkill(name=request.name, created_by=current_user.id)
    db.add(skill)
    await db.flush()
    return {"message": "Software skill created", "data": {"id": skill.id}}


@router.put("/{skill_id}")
async def update_software_skill(
    skill_id: int,
    request: SoftwareSkillUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(SoftwareSkill).where(SoftwareSkill.id == skill_id))
    skill = result.scalar_one_or_none()
    if not skill:
        raise HTTPException(404, "Software skill not found")
    for key, value in request.model_dump(exclude_none=True).items():
        setattr(skill, key, value)
    skill.updated_by = current_user.id
    await db.flush()
    return {"message": "Software skill updated"}


@router.delete("/{skill_id}")
async def delete_software_skill(
    skill_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(SoftwareSkill).where(SoftwareSkill.id == skill_id))
    skill = result.scalar_one_or_none()
    if not skill:
        raise HTTPException(404, "Software skill not found")
    await db.delete(skill)
    await db.flush()
    return {"message": "Software skill deleted"}
'''

ADMIN_COUNTRIES_FULL_PY = '''
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.database import get_db
from app.api.deps import require_role
from app.models.country import Country
from pydantic import BaseModel
from typing import Optional


class CountryCreateRequest(BaseModel):
    country_name_ar: Optional[str] = None
    country_name_en: str
    country_iso_code2: str
    country_iso_code3: str
    country_iso_numeric: Optional[str] = None
    currency_name: str
    currency_iso_code: str
    currency_iso_number: Optional[str] = None
    phone_code: str
    phone_digits_count: Optional[int] = None


class CountryUpdateRequest(BaseModel):
    country_name_ar: Optional[str] = None
    country_name_en: Optional[str] = None
    currency_name: Optional[str] = None
    currency_iso_code: Optional[str] = None
    phone_code: Optional[str] = None
    phone_digits_count: Optional[int] = None
    is_active: Optional[bool] = None


router = APIRouter()


@router.get("")
async def list_countries(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(Country).order_by(Country.country_name_en))
    return {"data": result.scalars().all()}


@router.get("/{country_id}")
async def get_country(
    country_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(Country).where(Country.id == country_id))
    country = result.scalar_one_or_none()
    if not country:
        raise HTTPException(404, "Country not found")
    return {"data": country}


@router.post("")
async def create_country(
    request: CountryCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    existing = await db.execute(select(Country).where(Country.country_iso_code2 == request.country_iso_code2))
    if existing.scalar_one_or_none():
        raise HTTPException(409, "Country code already exists")
    country = Country(**request.model_dump(), created_by=current_user.id)
    db.add(country)
    await db.flush()
    return {"message": "Country created", "data": {"id": country.id}}


@router.put("/{country_id}")
async def update_country(
    country_id: int,
    request: CountryUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(Country).where(Country.id == country_id))
    country = result.scalar_one_or_none()
    if not country:
        raise HTTPException(404, "Country not found")
    for key, value in request.model_dump(exclude_none=True).items():
        setattr(country, key, value)
    country.updated_by = current_user.id
    await db.flush()
    return {"message": "Country updated"}


@router.delete("/{country_id}")
async def delete_country(
    country_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(Country).where(Country.id == country_id))
    country = result.scalar_one_or_none()
    if not country:
        raise HTTPException(404, "Country not found")
    await db.delete(country)
    await db.flush()
    return {"message": "Country deleted"}
'''

ADMIN_DOCUMENTS_FULL_PY = '''
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException
from app.database import get_db
from app.api.deps import require_role
from app.models.uploaded_document import UploadedDocument
from datetime import datetime

router = APIRouter()


@router.get("")
async def list_documents(
    document_type: str = Query(None),
    is_verified: bool = Query(None),
    page: int = Query(1),
    per_page: int = Query(25),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    query = select(UploadedDocument)
    if document_type:
        query = query.where(UploadedDocument.document_type == document_type)
    if is_verified is not None:
        query = query.where(UploadedDocument.is_verified == is_verified)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()

    query = query.order_by(UploadedDocument.uploaded_at.desc()).offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)

    return {"data": result.scalars().all(), "meta": {"page": page, "per_page": per_page, "total": total}}


@router.get("/{document_id}")
async def get_document(
    document_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(UploadedDocument).where(UploadedDocument.id == document_id))
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(404, "Document not found")
    return {"data": doc}


@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(UploadedDocument).where(UploadedDocument.id == document_id))
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(404, "Document not found")
    await db.delete(doc)
    await db.flush()
    return {"message": "Document deleted"}


@router.patch("/{document_id}/verify")
async def verify_document(
    document_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(UploadedDocument).where(UploadedDocument.id == document_id))
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(404, "Document not found")
    doc.is_verified = True
    doc.verified_by = current_user.id
    doc.verified_at = datetime.utcnow()
    await db.flush()
    return {"message": "Document verified"}
'''

ADMIN_CONTENT_FULL_PY = '''
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.database import get_db
from app.api.deps import require_role
from app.models.platform_content import PlatformContent
from app.schemas.platform_content import PlatformContentUpdateRequest
from datetime import datetime

router = APIRouter()


@router.get("")
async def list_content(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(PlatformContent).order_by(PlatformContent.key))
    return {"data": result.scalars().all()}


@router.get("/{content_id}")
async def get_content(
    content_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(PlatformContent).where(PlatformContent.id == content_id))
    content = result.scalar_one_or_none()
    if not content:
        raise HTTPException(404, "Content not found")
    return {"data": content}


@router.put("/{content_id}")
async def update_content(
    content_id: int,
    request: PlatformContentUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(PlatformContent).where(PlatformContent.id == content_id))
    content = result.scalar_one_or_none()
    if not content:
        raise HTTPException(404, "Content not found")
    for key, value in request.model_dump(exclude_none=True).items():
        setattr(content, key, value)
    content.updated_by = current_user.id
    content.published_at = datetime.utcnow()
    await db.flush()
    return {"message": "Content updated"}
'''

ADMIN_AUDIT_LOGS_FULL_PY = '''
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException
from app.database import get_db
from app.api.deps import require_role
from app.models.audit_log import AuditLog

router = APIRouter()


@router.get("")
async def list_audit_logs(
    page: int = Query(1),
    per_page: int = Query(25),
    action_category: str = Query(None),
    action: str = Query(None),
    user_role: str = Query(None),
    entity_type: str = Query(None),
    entity_id: int = Query(None),
    search: str = Query(None),
    date_from: str = Query(None),
    date_to: str = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    query = select(AuditLog).order_by(AuditLog.created_at.desc())

    if action_category:
        query = query.where(AuditLog.action_category == action_category)
    if action:
        query = query.where(AuditLog.action == action)
    if user_role:
        query = query.where(AuditLog.user_role == user_role)
    if entity_type:
        query = query.where(AuditLog.entity_type == entity_type)
    if entity_id:
        query = query.where(AuditLog.entity_id == entity_id)
    if search:
        query = query.where(AuditLog.description.ilike(f"%{search}%"))
    if date_from:
        query = query.where(AuditLog.created_at >= date_from)
    if date_to:
        query = query.where(AuditLog.created_at <= date_to)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()

    query = query.offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)

    return {"data": result.scalars().all(), "meta": {"page": page, "per_page": per_page, "total": total}}


@router.get("/{log_id}")
async def get_audit_log(
    log_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(AuditLog).where(AuditLog.id == log_id))
    log = result.scalar_one_or_none()
    if not log:
        raise HTTPException(404, "Audit log not found")
    return {"data": log}


@router.get("/meta/filters")
async def get_filter_options(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    # Distinct action categories
    cat_result = await db.execute(select(AuditLog.action_category).distinct())
    categories = [row[0] for row in cat_result if row[0]]

    # Distinct actions
    act_result = await db.execute(select(AuditLog.action).distinct())
    actions = [row[0] for row in act_result if row[0]]

    # Distinct entity types
    ent_result = await db.execute(select(AuditLog.entity_type).distinct())
    entity_types = [row[0] for row in ent_result if row[0]]

    return {
        "data": {
            "action_categories": sorted(categories),
            "actions": sorted(actions),
            "entity_types": sorted(entity_types),
            "user_roles": ["admin", "client", "accountant"],
        }
    }
'''

# ============================================================
# UPDATED ROUTER
# ============================================================

V1_ROUTER_FULL_PY = '''
from fastapi import APIRouter
from app.api.v1 import auth, jobs, bids, categories, certifications, countries, content, profile
from app.api.v1 import nda, match, documents, client_jobs
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
api_v1_router.include_router(match.router, prefix="/jobs", tags=["Match"])
api_v1_router.include_router(bids.router, prefix="", tags=["My Bids"])
api_v1_router.include_router(profile.router, prefix="/my-profile", tags=["Profile"])
api_v1_router.include_router(documents.router, prefix="/my-profile", tags=["Documents"])

# Client
api_v1_router.include_router(client_jobs.router, prefix="/my-jobs", tags=["My Jobs"])
# Clients also use profile and documents routes

# Admin
api_v1_router.include_router(admin_router, prefix="/admin", tags=["Admin"])
'''

# ============================================================
# MIGRATION SQL
# ============================================================

MIGRATION_SQL = '''
-- =============================================
-- Accountant Hub — Complete Database Schema
-- Run: psql -U postgres -d accountant_hub -f 001_initial_schema.sql
-- =============================================

-- 01. users
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(30) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'client', 'accountant')),
    email_verified_at TIMESTAMP NULL,
    phone_verified_at TIMESTAMP NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    terms_accepted_at TIMESTAMP NULL,
    terms_version VARCHAR(20) NULL,
    last_login_at TIMESTAMP NULL,
    last_login_ip VARCHAR(45) NULL,
    restrictions JSONB NULL DEFAULT NULL,
    audit_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by BIGINT NULL REFERENCES users(id),
    updated_by BIGINT NULL REFERENCES users(id)
);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_is_active ON users(is_active);

-- 02. countries
CREATE TABLE countries (
    id BIGSERIAL PRIMARY KEY,
    country_name_ar VARCHAR(255) NULL,
    country_name_en VARCHAR(255) NOT NULL,
    country_iso_code2 VARCHAR(2) NOT NULL UNIQUE,
    country_iso_code3 VARCHAR(3) NOT NULL UNIQUE,
    country_iso_numeric VARCHAR(3) NULL,
    currency_name VARCHAR(100) NOT NULL,
    currency_iso_code VARCHAR(3) NOT NULL,
    currency_iso_number VARCHAR(3) NULL,
    phone_code VARCHAR(5) NOT NULL,
    phone_digits_count INTEGER NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by BIGINT NULL REFERENCES users(id),
    updated_by BIGINT NULL REFERENCES users(id)
);
CREATE INDEX idx_countries_currency ON countries(currency_iso_code);
CREATE INDEX idx_countries_is_active ON countries(is_active);

-- 03. client_profiles
CREATE TABLE client_profiles (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    company_name VARCHAR(255) NOT NULL,
    company_industry VARCHAR(100) NULL,
    company_size VARCHAR(50) NULL,
    company_description TEXT NULL,
    website VARCHAR(255) NULL,
    country_id BIGINT NULL REFERENCES countries(id),
    city VARCHAR(100) NULL,
    logo_url VARCHAR(500) NULL,
    preferred_currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    profile_completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by BIGINT NULL REFERENCES users(id),
    updated_by BIGINT NULL REFERENCES users(id)
);
CREATE INDEX idx_client_profiles_industry ON client_profiles(company_industry);
CREATE INDEX idx_client_profiles_country ON client_profiles(country_id);

-- 04. accountant_profiles
CREATE TABLE accountant_profiles (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    bio TEXT NULL,
    years_of_experience INTEGER NULL,
    hourly_rate DECIMAL(10,2) NULL,
    hourly_rate_currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    jurisdictions_served JSONB NULL,
    accounting_standards JSONB NULL,
    education_summary TEXT NULL,
    identity_verified BOOLEAN NOT NULL DEFAULT FALSE,
    profile_completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by BIGINT NULL REFERENCES users(id),
    updated_by BIGINT NULL REFERENCES users(id)
);
CREATE INDEX idx_accountant_profiles_experience ON accountant_profiles(years_of_experience);
CREATE INDEX idx_accountant_profiles_jurisdictions ON accountant_profiles USING GIN(jurisdictions_served);
CREATE INDEX idx_accountant_profiles_standards ON accountant_profiles USING GIN(accounting_standards);

-- 05. certifications
CREATE TABLE certifications (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    issuing_body VARCHAR(255) NULL,
    region VARCHAR(50) NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by BIGINT NULL REFERENCES users(id),
    updated_by BIGINT NULL REFERENCES users(id)
);
CREATE INDEX idx_certifications_region ON certifications(region);
CREATE INDEX idx_certifications_is_active ON certifications(is_active);

-- 06. accountant_certifications
CREATE TABLE accountant_certifications (
    id BIGSERIAL PRIMARY KEY,
    accountant_profile_id BIGINT NOT NULL REFERENCES accountant_profiles(id) ON DELETE CASCADE,
    certification_id BIGINT NULL REFERENCES certifications(id) ON DELETE SET NULL,
    custom_certification_name VARCHAR(255) NULL,
    license_number VARCHAR(100) NULL,
    issued_date DATE NULL,
    expiry_date DATE NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by BIGINT NULL REFERENCES users(id),
    updated_by BIGINT NULL REFERENCES users(id),
    CONSTRAINT ck_certification_or_custom CHECK (certification_id IS NOT NULL OR custom_certification_name IS NOT NULL)
);
CREATE INDEX idx_acct_cert_profile ON accountant_certifications(accountant_profile_id);
CREATE INDEX idx_acct_cert_cert ON accountant_certifications(certification_id);

-- 07. software_skills
CREATE TABLE software_skills (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by BIGINT NULL REFERENCES users(id),
    updated_by BIGINT NULL REFERENCES users(id)
);
CREATE INDEX idx_software_skills_is_active ON software_skills(is_active);

-- 08. accountant_software_skills
CREATE TABLE accountant_software_skills (
    accountant_profile_id BIGINT NOT NULL REFERENCES accountant_profiles(id) ON DELETE CASCADE,
    software_skill_id BIGINT NOT NULL REFERENCES software_skills(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (accountant_profile_id, software_skill_id)
);

-- 09. categories
CREATE TABLE categories (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE,
    parent_id BIGINT NULL REFERENCES categories(id) ON DELETE SET NULL,
    description TEXT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    sort_order INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by BIGINT NULL REFERENCES users(id),
    updated_by BIGINT NULL REFERENCES users(id),
    CONSTRAINT ck_category_not_self_parent CHECK (id != parent_id)
);
CREATE INDEX idx_categories_parent ON categories(parent_id);
CREATE INDEX idx_categories_is_active ON categories(is_active);
CREATE INDEX idx_categories_sort ON categories(sort_order);

-- 10. jobs
CREATE TABLE jobs (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    client_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category_id BIGINT NOT NULL REFERENCES categories(id) ON DELETE RESTRICT,
    budget_min DECIMAL(12,2) NOT NULL,
    budget_max DECIMAL(12,2) NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    pricing_model VARCHAR(20) NOT NULL CHECK (pricing_model IN ('fixed', 'hourly', 'retainer')),
    deadline DATE NOT NULL,
    expected_delivery_time VARCHAR(100) NULL,
    engagement_type VARCHAR(20) NOT NULL DEFAULT 'one_time' CHECK (engagement_type IN ('one_time', 'recurring')),
    jurisdiction VARCHAR(100) NULL,
    accounting_standard VARCHAR(50) NULL,
    required_certifications JSONB NULL,
    required_software JSONB NULL,
    required_skills JSONB NULL,
    minimum_experience_years INTEGER NULL,
    company_industry_context VARCHAR(100) NULL,
    nda_required BOOLEAN NOT NULL DEFAULT FALSE,
    status VARCHAR(20) NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'closed')),
    closed_reason VARCHAR(50) NULL,
    posted_date DATE NOT NULL DEFAULT CURRENT_DATE,
    bids_count INTEGER NOT NULL DEFAULT 0,
    bids_min_price DECIMAL(12,2) NULL,
    bids_max_price DECIMAL(12,2) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by BIGINT NULL REFERENCES users(id),
    updated_by BIGINT NULL REFERENCES users(id),
    CONSTRAINT ck_budget_range CHECK (budget_max >= budget_min),
    CONSTRAINT ck_deadline_after_posted CHECK (deadline >= posted_date)
);
CREATE INDEX idx_jobs_client ON jobs(client_id);
CREATE INDEX idx_jobs_category ON jobs(category_id);
CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_pricing ON jobs(pricing_model);
CREATE INDEX idx_jobs_jurisdiction ON jobs(jurisdiction);
CREATE INDEX idx_jobs_standard ON jobs(accounting_standard);
CREATE INDEX idx_jobs_engagement ON jobs(engagement_type);
CREATE INDEX idx_jobs_nda ON jobs(nda_required);
CREATE INDEX idx_jobs_deadline ON jobs(deadline);
CREATE INDEX idx_jobs_posted ON jobs(posted_date);
CREATE INDEX idx_jobs_budget_min ON jobs(budget_min);
CREATE INDEX idx_jobs_budget_max ON jobs(budget_max);
CREATE INDEX idx_jobs_currency ON jobs(currency);
CREATE INDEX idx_jobs_certs ON jobs USING GIN(required_certifications);
CREATE INDEX idx_jobs_software ON jobs USING GIN(required_software);
CREATE INDEX idx_jobs_skills ON jobs USING GIN(required_skills);

-- 11. bids
CREATE TABLE bids (
    id BIGSERIAL PRIMARY KEY,
    job_id BIGINT NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    accountant_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    price DECIMAL(12,2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    pricing_model VARCHAR(20) NOT NULL CHECK (pricing_model IN ('fixed', 'hourly', 'retainer')),
    includes_all_fees BOOLEAN NOT NULL DEFAULT TRUE,
    additional_costs_description TEXT NULL,
    estimated_hours INTEGER NULL,
    number_of_entities INTEGER NULL,
    delivery_time VARCHAR(100) NOT NULL,
    services_included JSONB NOT NULL,
    milestones JSONB NULL,
    engagement_terms TEXT NULL,
    proposal_letter TEXT NOT NULL,
    jurisdiction_confirmed BOOLEAN NOT NULL DEFAULT FALSE,
    terms_accepted BOOLEAN NOT NULL DEFAULT FALSE,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'rejected')),
    accepted_at TIMESTAMP NULL,
    rejected_at TIMESTAMP NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by BIGINT NULL REFERENCES users(id),
    updated_by BIGINT NULL REFERENCES users(id),
    CONSTRAINT uq_job_accountant_bid UNIQUE (job_id, accountant_id),
    CONSTRAINT ck_bid_price_positive CHECK (price > 0)
);
CREATE INDEX idx_bids_job ON bids(job_id);
CREATE INDEX idx_bids_accountant ON bids(accountant_id);
CREATE INDEX idx_bids_status ON bids(status);
CREATE INDEX idx_bids_created ON bids(created_at);
CREATE INDEX idx_bids_services ON bids USING GIN(services_included);

-- 12. nda_acceptances
CREATE TABLE nda_acceptances (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    job_id BIGINT NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    content_version VARCHAR(20) NULL,
    ip_address VARCHAR(45) NULL,
    accepted_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_user_job_nda UNIQUE (user_id, job_id)
);
CREATE INDEX idx_nda_user ON nda_acceptances(user_id);
CREATE INDEX idx_nda_job ON nda_acceptances(job_id);

-- 13. job_attachments
CREATE TABLE job_attachments (
    id BIGSERIAL PRIMARY KEY,
    job_id BIGINT NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    file_name VARCHAR(255) NOT NULL,
    file_url VARCHAR(500) NOT NULL,
    file_size INTEGER NULL,
    file_type VARCHAR(50) NULL,
    uploaded_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by BIGINT NULL REFERENCES users(id)
);
CREATE INDEX idx_job_attachments_job ON job_attachments(job_id);

-- 14. uploaded_documents
CREATE TABLE uploaded_documents (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    document_type VARCHAR(50) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_url VARCHAR(500) NOT NULL,
    file_size INTEGER NULL,
    file_type VARCHAR(50) NULL,
    entity_type VARCHAR(50) NULL,
    entity_id BIGINT NULL,
    description TEXT NULL,
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,
    verified_by BIGINT NULL REFERENCES users(id),
    verified_at TIMESTAMP NULL,
    uploaded_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by BIGINT NULL REFERENCES users(id),
    updated_by BIGINT NULL REFERENCES users(id)
);
CREATE INDEX idx_uploaded_docs_user ON uploaded_documents(user_id);
CREATE INDEX idx_uploaded_docs_entity ON uploaded_documents(entity_type, entity_id);
CREATE INDEX idx_uploaded_docs_type ON uploaded_documents(document_type);

-- 15. platform_content
CREATE TABLE platform_content (
    id BIGSERIAL PRIMARY KEY,
    key VARCHAR(100) NOT NULL UNIQUE,
    title VARCHAR(255) NULL,
    body TEXT NOT NULL,
    content_type VARCHAR(50) NOT NULL DEFAULT 'text',
    version VARCHAR(20) NOT NULL DEFAULT '1.0',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    published_at TIMESTAMP NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by BIGINT NULL REFERENCES users(id),
    updated_by BIGINT NULL REFERENCES users(id)
);
CREATE INDEX idx_platform_content_key ON platform_content(key);
CREATE INDEX idx_platform_content_active ON platform_content(is_active);

-- 16. audit_logs
CREATE TABLE audit_logs (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NULL REFERENCES users(id) ON DELETE SET NULL,
    user_email VARCHAR(255) NULL,
    user_role VARCHAR(20) NULL,
    action VARCHAR(100) NOT NULL,
    action_category VARCHAR(50) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id BIGINT NULL,
    description TEXT NULL,
    old_values JSONB NULL,
    new_values JSONB NULL,
    ip_address VARCHAR(45) NULL,
    user_agent TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_audit_logs_user ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_category ON audit_logs(action_category);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_entity ON audit_logs(entity_type, entity_id);
CREATE INDEX idx_audit_logs_created ON audit_logs(created_at);

-- 17. password_reset_tokens
CREATE TABLE password_reset_tokens (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    token VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    used BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_password_reset_email ON password_reset_tokens(email);
CREATE INDEX idx_password_reset_token ON password_reset_tokens(token);
CREATE INDEX idx_password_reset_expires ON password_reset_tokens(expires_at);
'''


# ============================================================
# RUN SETUP
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("ACCOUNTANT HUB - PHASE II SETUP")
    print("Completing all missing endpoints & services")
    print("=" * 60)

    os.chdir(BASE_DIR)

    create_missing_services()
    create_missing_schemas()
    create_accountant_endpoints()
    create_client_endpoints()
    fill_admin_crud()
    update_router()
    create_migration()

    print_summary()