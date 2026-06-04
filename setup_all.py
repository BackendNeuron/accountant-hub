"""
Accountant Hub - Master Setup Script
Run: python setup_all.py
Creates all project files and verifies them for syntax errors.
"""
import os
import sys
import py_compile
import traceback

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ERRORS = []


def write_file(filepath: str, content: str):
    """Write content to a file, creating directories if needed."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✅ Created: {os.path.relpath(filepath, BASE_DIR)}")


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


def create_core_files():
    """Step 1: Create core configuration and utility files."""
    print("\n" + "="*60)
    print("STEP 1: Core Files (config.py, enums.py, security.py, etc.)")
    print("="*60)

    # config.py
    write_file("app/config.py", CONFIG_PY)
    verify_file("app/config.py")

    # utils/__init__.py
    write_file("app/utils/__init__.py", "")
    verify_file("app/utils/__init__.py")

    # utils/enums.py
    write_file("app/utils/enums.py", ENUMS_PY)
    verify_file("app/utils/enums.py")

    # utils/security.py
    write_file("app/utils/security.py", SECURITY_PY)
    verify_file("app/utils/security.py")

    # utils/validators.py
    write_file("app/utils/validators.py", VALIDATORS_PY)
    verify_file("app/utils/validators.py")


def create_database_files():
    """Step 2: Create database.py and models."""
    print("\n" + "="*60)
    print("STEP 2: Database & Models")
    print("="*60)

    # database.py
    write_file("app/database.py", DATABASE_PY)
    verify_file("app/database.py")

    # models/__init__.py
    write_file("app/models/__init__.py", MODELS_INIT_PY)
    verify_file("app/models/__init__.py")

    # All models
    models = [
        ("user.py", USER_MODEL_PY),
        ("client_profile.py", CLIENT_PROFILE_MODEL_PY),
        ("accountant_profile.py", ACCOUNTANT_PROFILE_MODEL_PY),
        ("certification.py", CERTIFICATION_MODEL_PY),
        ("accountant_certification.py", ACCOUNTANT_CERTIFICATION_MODEL_PY),
        ("software_skill.py", SOFTWARE_SKILL_MODEL_PY),
        ("accountant_software_skill.py", ACCOUNTANT_SOFTWARE_SKILL_MODEL_PY),
        ("category.py", CATEGORY_MODEL_PY),
        ("job.py", JOB_MODEL_PY),
        ("bid.py", BID_MODEL_PY),
        ("nda_acceptance.py", NDA_ACCEPTANCE_MODEL_PY),
        ("job_attachment.py", JOB_ATTACHMENT_MODEL_PY),
        ("uploaded_document.py", UPLOADED_DOCUMENT_MODEL_PY),
        ("country.py", COUNTRY_MODEL_PY),
        ("platform_content.py", PLATFORM_CONTENT_MODEL_PY),
        ("audit_log.py", AUDIT_LOG_MODEL_PY),
        ("password_reset_token.py", PASSWORD_RESET_TOKEN_MODEL_PY),
    ]
    for filename, content in models:
        write_file(f"app/models/{filename}", content)
        verify_file(f"app/models/{filename}")


def create_schema_files():
    """Step 3: Create Pydantic schemas."""
    print("\n" + "="*60)
    print("STEP 3: Pydantic Schemas")
    print("="*60)

    # schemas/__init__.py
    write_file("app/schemas/__init__.py", "")
    verify_file("app/schemas/__init__.py")

    schemas = [
        ("common.py", COMMON_SCHEMA_PY),
        ("auth.py", AUTH_SCHEMA_PY),
        ("user.py", USER_SCHEMA_PY),
        ("job.py", JOB_SCHEMA_PY),
        ("bid.py", BID_SCHEMA_PY),
        ("category.py", CATEGORY_SCHEMA_PY),
        ("certification.py", CERTIFICATION_SCHEMA_PY),
        ("country.py", COUNTRY_SCHEMA_PY),
        ("document.py", DOCUMENT_SCHEMA_PY),
        ("platform_content.py", PLATFORM_CONTENT_SCHEMA_PY),
        ("audit_log.py", AUDIT_LOG_SCHEMA_PY),
    ]
    for filename, content in schemas:
        write_file(f"app/schemas/{filename}", content)
        verify_file(f"app/schemas/{filename}")


def create_service_files():
    """Step 4: Create service layer."""
    print("\n" + "="*60)
    print("STEP 4: Service Layer")
    print("="*60)

    write_file("app/services/__init__.py", "")
    verify_file("app/services/__init__.py")

    services = [
        ("auth_service.py", AUTH_SERVICE_PY),
        ("job_service.py", JOB_SERVICE_PY),
        ("bid_service.py", BID_SERVICE_PY),
        ("match_service.py", MATCH_SERVICE_PY),
        ("audit_service.py", AUDIT_SERVICE_PY),
        ("file_service.py", FILE_SERVICE_PY),
    ]
    for filename, content in services:
        write_file(f"app/services/{filename}", content)
        verify_file(f"app/services/{filename}")


def create_api_files():
    """Step 5: Create API routes."""
    print("\n" + "="*60)
    print("STEP 5: API Routes")
    print("="*60)

    # api/__init__.py
    write_file("app/api/__init__.py", "")
    verify_file("app/api/__init__.py")

    # api/deps.py
    write_file("app/api/deps.py", DEPS_PY)
    verify_file("app/api/deps.py")

    # api/v1/__init__.py
    write_file("app/api/v1/__init__.py", "")
    verify_file("app/api/v1/__init__.py")

    # api/v1/router.py
    write_file("app/api/v1/router.py", V1_ROUTER_PY)
    verify_file("app/api/v1/router.py")

    # Public routes
    v1_routes = [
        ("auth.py", AUTH_ROUTES_PY),
        ("jobs.py", JOBS_ROUTES_PY),
        ("bids.py", BIDS_ROUTES_PY),
        ("categories.py", CATEGORIES_ROUTES_PY),
        ("certifications.py", CERTIFICATIONS_ROUTES_PY),
        ("countries.py", COUNTRIES_ROUTES_PY),
        ("content.py", CONTENT_ROUTES_PY),
        ("profile.py", PROFILE_ROUTES_PY),
    ]
    for filename, content in v1_routes:
        write_file(f"app/api/v1/{filename}", content)
        verify_file(f"app/api/v1/{filename}")

    # Admin routes
    write_file("app/api/v1/admin/__init__.py", "")
    verify_file("app/api/v1/admin/__init__.py")

    write_file("app/api/v1/admin/router.py", ADMIN_ROUTER_PY)
    verify_file("app/api/v1/admin/router.py")

    admin_routes = [
        ("dashboard.py", ADMIN_DASHBOARD_PY),
        ("users.py", ADMIN_USERS_PY),
        ("jobs.py", ADMIN_JOBS_PY),
        ("bids.py", ADMIN_BIDS_PY),
        ("categories.py", ADMIN_CATEGORIES_PY),
        ("certifications.py", ADMIN_CERTIFICATIONS_PY),
        ("software_skills.py", ADMIN_SOFTWARE_SKILLS_PY),
        ("countries.py", ADMIN_COUNTRIES_PY),
        ("documents.py", ADMIN_DOCUMENTS_PY),
        ("content.py", ADMIN_CONTENT_PY),
        ("audit_logs.py", ADMIN_AUDIT_LOGS_PY),
        ("restrictions.py", ADMIN_RESTRICTIONS_PY),
    ]
    for filename, content in admin_routes:
        write_file(f"app/api/v1/admin/{filename}", content)
        verify_file(f"app/api/v1/admin/{filename}")


def create_middleware_files():
    """Step 6: Create middleware."""
    print("\n" + "="*60)
    print("STEP 6: Middleware")
    print("="*60)

    write_file("app/middleware/__init__.py", "")
    verify_file("app/middleware/__init__.py")

    write_file("app/middleware/auth_middleware.py", AUTH_MIDDLEWARE_PY)
    verify_file("app/middleware/auth_middleware.py")

    write_file("app/middleware/audit_middleware.py", AUDIT_MIDDLEWARE_PY)
    verify_file("app/middleware/audit_middleware.py")


def create_main_file():
    """Step 7: Create main.py."""
    print("\n" + "="*60)
    print("STEP 7: Main Application Entry Point")
    print("="*60)

    write_file("app/main.py", MAIN_PY)
    verify_file("app/main.py")

    write_file("app/__init__.py", "")
    verify_file("app/__init__.py")


def print_summary():
    """Print final summary."""
    print("\n" + "="*60)
    if ERRORS:
        print(f"❌ COMPLETED WITH {len(ERRORS)} ERROR(S):")
        for filepath, error in ERRORS:
            print(f"   - {filepath}: {error}")
    else:
        print("✅ ALL FILES CREATED AND VERIFIED SUCCESSFULLY!")
    print("="*60)
    print(f"\nTotal files created in: {BASE_DIR}")
    print("Next steps:")
    print("  1. pip install -r requirements.txt")
    print("  2. Create PostgreSQL database: 'accountant_hub'")
    print("  3. Run migration: psql -U postgres -d accountant_hub -f migrations/001_initial_schema.sql")
    print("  4. Run: uvicorn app.main:app --reload")


# ============================================================
# FILE CONTENTS - All actual code for each file
# ============================================================

CONFIG_PY = '''
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/accountant_hub"
    SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440
    UPLOAD_DIR: str = "uploads"
    APP_ENV: str = "development"
    APP_NAME: str = "Accountant Hub API"
    APP_VERSION: str = "1.0.0"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
'''

ENUMS_PY = '''
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    CLIENT = "client"
    ACCOUNTANT = "accountant"


class JobStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"


class BidStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class PricingModel(str, Enum):
    FIXED = "fixed"
    HOURLY = "hourly"
    RETAINER = "retainer"


class EngagementType(str, Enum):
    ONE_TIME = "one_time"
    RECURRING = "recurring"


class DocumentType(str, Enum):
    CV = "cv"
    CERTIFICATE_PROOF = "certificate_proof"
    BUSINESS_LICENSE = "business_license"
    PORTFOLIO = "portfolio"
    ENGAGEMENT_LETTER = "engagement_letter"
    OTHER = "other"


class AuditActionCategory(str, Enum):
    AUTHENTICATION = "authentication"
    PROFILE = "profile"
    JOB = "job"
    BID = "bid"
    NDA = "nda"
    DOCUMENT = "document"
    ADMIN = "admin"
    CONTENT = "content"
'''

SECURITY_PY = '''
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    user_id: int,
    role: str,
    expires_delta: Optional[timedelta] = None
) -> str:
    to_encode = {
        "sub": str(user_id),
        "role": role,
        "iat": datetime.utcnow(),
    }
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
'''

VALIDATORS_PY = '''
import re
from typing import Optional


def validate_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_phone(phone: str, expected_digits: Optional[int] = None) -> bool:
    digits_only = re.sub(r"\\D", "", phone)
    if expected_digits:
        return len(digits_only) == expected_digits
    return 7 <= len(digits_only) <= 15


def validate_password_strength(password: str) -> tuple[bool, str]:
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r"\\d", password):
        return False, "Password must contain at least one number"
    return True, "Password is strong"
'''

DATABASE_PY = '''
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False, pool_size=10, max_overflow=20)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
'''

MODELS_INIT_PY = '''
from app.database import Base
from app.models.user import User
from app.models.country import Country
from app.models.client_profile import ClientProfile
from app.models.accountant_profile import AccountantProfile
from app.models.certification import Certification
from app.models.accountant_certification import AccountantCertification
from app.models.software_skill import SoftwareSkill
from app.models.accountant_software_skill import AccountantSoftwareSkill
from app.models.category import Category
from app.models.job import Job
from app.models.bid import Bid
from app.models.nda_acceptance import NDAAcceptance
from app.models.job_attachment import JobAttachment
from app.models.uploaded_document import UploadedDocument
from app.models.platform_content import PlatformContent
from app.models.audit_log import AuditLog
from app.models.password_reset_token import PasswordResetToken

__all__ = [
    "Base", "User", "Country", "ClientProfile", "AccountantProfile",
    "Certification", "AccountantCertification", "SoftwareSkill",
    "AccountantSoftwareSkill", "Category", "Job", "Bid", "NDAAcceptance",
    "JobAttachment", "UploadedDocument", "PlatformContent", "AuditLog",
    "PasswordResetToken",
]
'''

USER_MODEL_PY = '''
from sqlalchemy import Column, BigInteger, String, Boolean, TIMESTAMP, CheckConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    phone = Column(String(30), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, index=True)
    email_verified_at = Column(TIMESTAMP, nullable=True)
    phone_verified_at = Column(TIMESTAMP, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    terms_accepted_at = Column(TIMESTAMP, nullable=True)
    terms_version = Column(String(20), nullable=True)
    last_login_at = Column(TIMESTAMP, nullable=True)
    last_login_ip = Column(String(45), nullable=True)
    restrictions = Column(JSONB, nullable=True, default=None)
    audit_enabled = Column(Boolean, nullable=False, default=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    created_by = Column(BigInteger, nullable=True)
    updated_by = Column(BigInteger, nullable=True)

    __table_args__ = (
        CheckConstraint("role IN ('admin', 'client', 'accountant')", name="ck_users_role"),
    )
'''

COUNTRY_MODEL_PY = '''
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base


class Country(Base):
    __tablename__ = "countries"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    country_name_ar = Column(String(255), nullable=True)
    country_name_en = Column(String(255), nullable=False)
    country_iso_code2 = Column(String(2), nullable=False, unique=True)
    country_iso_code3 = Column(String(3), nullable=False, unique=True)
    country_iso_numeric = Column(String(3), nullable=True)
    currency_name = Column(String(100), nullable=False)
    currency_iso_code = Column(String(3), nullable=False, index=True)
    currency_iso_number = Column(String(3), nullable=True)
    phone_code = Column(String(5), nullable=False)
    phone_digits_count = Column(Integer, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    created_by = Column(BigInteger, nullable=True)
    updated_by = Column(BigInteger, nullable=True)
'''

CLIENT_PROFILE_MODEL_PY = '''
from sqlalchemy import Column, BigInteger, String, Text, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class ClientProfile(Base):
    __tablename__ = "client_profiles"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    company_name = Column(String(255), nullable=False)
    company_industry = Column(String(100), nullable=True, index=True)
    company_size = Column(String(50), nullable=True)
    company_description = Column(Text, nullable=True)
    website = Column(String(255), nullable=True)
    country_id = Column(BigInteger, ForeignKey("countries.id"), nullable=True, index=True)
    city = Column(String(100), nullable=True)
    logo_url = Column(String(500), nullable=True)
    preferred_currency = Column(String(3), nullable=False, default="USD")
    profile_completed = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    created_by = Column(BigInteger, nullable=True)
    updated_by = Column(BigInteger, nullable=True)
'''

ACCOUNTANT_PROFILE_MODEL_PY = '''
from sqlalchemy import Column, BigInteger, String, Text, Boolean, Integer, DECIMAL, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.database import Base


class AccountantProfile(Base):
    __tablename__ = "accountant_profiles"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    bio = Column(Text, nullable=True)
    years_of_experience = Column(Integer, nullable=True, index=True)
    hourly_rate = Column(DECIMAL(10, 2), nullable=True)
    hourly_rate_currency = Column(String(3), nullable=False, default="USD")
    jurisdictions_served = Column(JSONB, nullable=True)
    accounting_standards = Column(JSONB, nullable=True)
    education_summary = Column(Text, nullable=True)
    identity_verified = Column(Boolean, nullable=False, default=False)
    profile_completed = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    created_by = Column(BigInteger, nullable=True)
    updated_by = Column(BigInteger, nullable=True)
'''

CERTIFICATION_MODEL_PY = '''
from sqlalchemy import Column, BigInteger, String, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base


class Certification(Base):
    __tablename__ = "certifications"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    issuing_body = Column(String(255), nullable=True)
    region = Column(String(50), nullable=True, index=True)
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    created_by = Column(BigInteger, nullable=True)
    updated_by = Column(BigInteger, nullable=True)
'''

ACCOUNTANT_CERTIFICATION_MODEL_PY = '''
from sqlalchemy import Column, BigInteger, String, Date, TIMESTAMP, ForeignKey, CheckConstraint
from sqlalchemy.sql import func
from app.database import Base


class AccountantCertification(Base):
    __tablename__ = "accountant_certifications"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    accountant_profile_id = Column(BigInteger, ForeignKey("accountant_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    certification_id = Column(BigInteger, ForeignKey("certifications.id", ondelete="SET NULL"), nullable=True, index=True)
    custom_certification_name = Column(String(255), nullable=True)
    license_number = Column(String(100), nullable=True)
    issued_date = Column(Date, nullable=True)
    expiry_date = Column(Date, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    created_by = Column(BigInteger, nullable=True)
    updated_by = Column(BigInteger, nullable=True)

    __table_args__ = (
        CheckConstraint(
            "certification_id IS NOT NULL OR custom_certification_name IS NOT NULL",
            name="ck_certification_or_custom"
        ),
    )
'''

SOFTWARE_SKILL_MODEL_PY = '''
from sqlalchemy import Column, BigInteger, String, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base


class SoftwareSkill(Base):
    __tablename__ = "software_skills"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    created_by = Column(BigInteger, nullable=True)
    updated_by = Column(BigInteger, nullable=True)
'''

ACCOUNTANT_SOFTWARE_SKILL_MODEL_PY = '''
from sqlalchemy import Column, BigInteger, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class AccountantSoftwareSkill(Base):
    __tablename__ = "accountant_software_skills"

    accountant_profile_id = Column(BigInteger, ForeignKey("accountant_profiles.id", ondelete="CASCADE"), primary_key=True)
    software_skill_id = Column(BigInteger, ForeignKey("software_skills.id", ondelete="CASCADE"), primary_key=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
'''

CATEGORY_MODEL_PY = '''
from sqlalchemy import Column, BigInteger, String, Text, Boolean, Integer, TIMESTAMP, ForeignKey, CheckConstraint
from sqlalchemy.sql import func
from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    parent_id = Column(BigInteger, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, index=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    sort_order = Column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    created_by = Column(BigInteger, nullable=True)
    updated_by = Column(BigInteger, nullable=True)

    __table_args__ = (
        CheckConstraint("id != parent_id", name="ck_category_not_self_parent"),
    )
'''

JOB_MODEL_PY = '''
from sqlalchemy import Column, BigInteger, String, Text, Boolean, Integer, DECIMAL, Date, TIMESTAMP, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    client_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    category_id = Column(BigInteger, ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False, index=True)
    budget_min = Column(DECIMAL(12, 2), nullable=False, index=True)
    budget_max = Column(DECIMAL(12, 2), nullable=False, index=True)
    currency = Column(String(3), nullable=False, default="USD", index=True)
    pricing_model = Column(String(20), nullable=False, index=True)
    deadline = Column(Date, nullable=False, index=True)
    expected_delivery_time = Column(String(100), nullable=True)
    engagement_type = Column(String(20), nullable=False, default="one_time", index=True)
    jurisdiction = Column(String(100), nullable=True, index=True)
    accounting_standard = Column(String(50), nullable=True, index=True)
    required_certifications = Column(JSONB, nullable=True)
    required_software = Column(JSONB, nullable=True)
    required_skills = Column(JSONB, nullable=True)
    minimum_experience_years = Column(Integer, nullable=True)
    company_industry_context = Column(String(100), nullable=True)
    nda_required = Column(Boolean, nullable=False, default=False, index=True)
    status = Column(String(20), nullable=False, default="open", index=True)
    closed_reason = Column(String(50), nullable=True)
    posted_date = Column(Date, nullable=False, default=func.current_date(), index=True)
    bids_count = Column(Integer, nullable=False, default=0)
    bids_min_price = Column(DECIMAL(12, 2), nullable=True)
    bids_max_price = Column(DECIMAL(12, 2), nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    created_by = Column(BigInteger, nullable=True)
    updated_by = Column(BigInteger, nullable=True)

    __table_args__ = (
        CheckConstraint("budget_max >= budget_min", name="ck_budget_range"),
        CheckConstraint("deadline >= posted_date", name="ck_deadline_after_posted"),
        CheckConstraint("pricing_model IN ('fixed', 'hourly', 'retainer')", name="ck_pricing_model"),
        CheckConstraint("engagement_type IN ('one_time', 'recurring')", name="ck_engagement_type"),
        CheckConstraint("status IN ('open', 'closed')", name="ck_job_status"),
    )
'''

BID_MODEL_PY = '''
from sqlalchemy import Column, BigInteger, String, Text, Boolean, Integer, DECIMAL, TIMESTAMP, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.database import Base


class Bid(Base):
    __tablename__ = "bids"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    job_id = Column(BigInteger, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True)
    accountant_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    price = Column(DECIMAL(12, 2), nullable=False)
    currency = Column(String(3), nullable=False)
    pricing_model = Column(String(20), nullable=False)
    includes_all_fees = Column(Boolean, nullable=False, default=True)
    additional_costs_description = Column(Text, nullable=True)
    estimated_hours = Column(Integer, nullable=True)
    number_of_entities = Column(Integer, nullable=True)
    delivery_time = Column(String(100), nullable=False)
    services_included = Column(JSONB, nullable=False)
    milestones = Column(JSONB, nullable=True)
    engagement_terms = Column(Text, nullable=True)
    proposal_letter = Column(Text, nullable=False)
    jurisdiction_confirmed = Column(Boolean, nullable=False, default=False)
    terms_accepted = Column(Boolean, nullable=False, default=False)
    status = Column(String(20), nullable=False, default="pending", index=True)
    accepted_at = Column(TIMESTAMP, nullable=True)
    rejected_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), index=True)
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    created_by = Column(BigInteger, nullable=True)
    updated_by = Column(BigInteger, nullable=True)

    __table_args__ = (
        UniqueConstraint("job_id", "accountant_id", name="uq_job_accountant_bid"),
        CheckConstraint("price > 0", name="ck_bid_price_positive"),
        CheckConstraint("pricing_model IN ('fixed', 'hourly', 'retainer')", name="ck_bid_pricing_model"),
        CheckConstraint("status IN ('pending', 'accepted', 'rejected')", name="ck_bid_status"),
    )
'''

NDA_ACCEPTANCE_MODEL_PY = '''
from sqlalchemy import Column, BigInteger, String, TIMESTAMP, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from app.database import Base


class NDAAcceptance(Base):
    __tablename__ = "nda_acceptances"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    job_id = Column(BigInteger, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True)
    content_version = Column(String(20), nullable=True)
    ip_address = Column(String(45), nullable=True)
    accepted_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "job_id", name="uq_user_job_nda"),
    )
'''

JOB_ATTACHMENT_MODEL_PY = '''
from sqlalchemy import Column, BigInteger, String, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class JobAttachment(Base):
    __tablename__ = "job_attachments"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    job_id = Column(BigInteger, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True)
    file_name = Column(String(255), nullable=False)
    file_url = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=True)
    file_type = Column(String(50), nullable=True)
    uploaded_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    created_by = Column(BigInteger, nullable=True)
'''

UPLOADED_DOCUMENT_MODEL_PY = '''
from sqlalchemy import Column, BigInteger, String, Text, Boolean, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class UploadedDocument(Base):
    __tablename__ = "uploaded_documents"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    document_type = Column(String(50), nullable=False, index=True)
    file_name = Column(String(255), nullable=False)
    file_url = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=True)
    file_type = Column(String(50), nullable=True)
    entity_type = Column(String(50), nullable=True, index=True)
    entity_id = Column(BigInteger, nullable=True)
    description = Column(Text, nullable=True)
    is_verified = Column(Boolean, nullable=False, default=False)
    verified_by = Column(BigInteger, ForeignKey("users.id"), nullable=True)
    verified_at = Column(TIMESTAMP, nullable=True)
    uploaded_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    created_by = Column(BigInteger, nullable=True)
    updated_by = Column(BigInteger, nullable=True)
'''

PLATFORM_CONTENT_MODEL_PY = '''
from sqlalchemy import Column, BigInteger, String, Text, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base


class PlatformContent(Base):
    __tablename__ = "platform_content"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    key = Column(String(100), nullable=False, unique=True, index=True)
    title = Column(String(255), nullable=True)
    body = Column(Text, nullable=False)
    content_type = Column(String(50), nullable=False, default="text")
    version = Column(String(20), nullable=False, default="1.0")
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    published_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    created_by = Column(BigInteger, nullable=True)
    updated_by = Column(BigInteger, nullable=True)
'''

AUDIT_LOG_MODEL_PY = '''
from sqlalchemy import Column, BigInteger, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    user_email = Column(String(255), nullable=True)
    user_role = Column(String(20), nullable=True)
    action = Column(String(100), nullable=False, index=True)
    action_category = Column(String(50), nullable=False, index=True)
    entity_type = Column(String(50), nullable=False, index=True)
    entity_id = Column(BigInteger, nullable=True)
    description = Column(Text, nullable=True)
    old_values = Column(JSONB, nullable=True)
    new_values = Column(JSONB, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), index=True)
'''

PASSWORD_RESET_TOKEN_MODEL_PY = '''
from sqlalchemy import Column, BigInteger, String, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, index=True)
    token = Column(String(255), nullable=False, index=True)
    expires_at = Column(TIMESTAMP, nullable=False, index=True)
    used = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
'''

# Schemas
COMMON_SCHEMA_PY = '''
from typing import TypeVar, Generic, Optional
from pydantic import BaseModel

T = TypeVar("T")


class PaginationParams(BaseModel):
    page: int = 1
    per_page: int = 12


class PaginatedResponse(BaseModel, Generic[T]):
    data: list[T]
    meta: dict


class MessageResponse(BaseModel):
    message: str
    detail: Optional[str] = None
'''

AUTH_SCHEMA_PY = '''
from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr
    phone: str = Field(..., min_length=7, max_length=30)
    password: str = Field(..., min_length=8, max_length=100)
    role: str = Field(..., pattern="^(accountant|client)$")


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict
'''

USER_SCHEMA_PY = '''
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    role: str
    is_active: bool
    restrictions: Optional[dict] = None
    audit_enabled: bool = True

    class Config:
        from_attributes = True


class UserUpdateRequest(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None
'''

JOB_SCHEMA_PY = '''
from typing import Optional
from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field


class JobFilterParams(BaseModel):
    search: Optional[str] = None
    category: Optional[str] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    currency: Optional[str] = None
    pricing_model: Optional[str] = None
    jurisdiction: Optional[str] = None
    accounting_standard: Optional[str] = None
    certification: Optional[str] = None
    software: Optional[str] = None
    engagement_type: Optional[str] = None
    nda_required: Optional[bool] = None
    status: Optional[str] = "open"
    sort: Optional[str] = "newest"
    page: int = 1
    per_page: int = 12


class JobCreateRequest(BaseModel):
    title: str = Field(..., min_length=5, max_length=255)
    description: str = Field(..., min_length=50)
    category_id: int
    budget_min: Decimal
    budget_max: Decimal
    currency: str = "USD"
    pricing_model: str = "fixed"
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


class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    client_id: int
    company_name: Optional[str] = None
    category: Optional[dict] = None
    budget_min: Decimal
    budget_max: Decimal
    currency: str
    pricing_model: str
    deadline: date
    engagement_type: str
    jurisdiction: Optional[str] = None
    accounting_standard: Optional[str] = None
    required_certifications: Optional[list] = None
    required_software: Optional[list] = None
    required_skills: Optional[list] = None
    nda_required: bool
    status: str
    bids_count: int
    bids_min_price: Optional[Decimal] = None
    bids_max_price: Optional[Decimal] = None
    posted_date: date
    current_user_bid: Optional[dict] = None

    class Config:
        from_attributes = True
'''

BID_SCHEMA_PY = '''
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field


class BidCreateRequest(BaseModel):
    price: Decimal = Field(..., gt=0)
    pricing_model: str = Field(..., pattern="^(fixed|hourly|retainer)$")
    includes_all_fees: bool = True
    additional_costs_description: Optional[str] = None
    estimated_hours: Optional[int] = None
    number_of_entities: Optional[int] = None
    delivery_time: str = Field(..., min_length=2, max_length=100)
    services_included: list[str]
    milestones: Optional[list[dict]] = None
    engagement_terms: Optional[str] = None
    proposal_letter: str = Field(..., min_length=50)
    jurisdiction_confirmed: bool = False
    terms_accepted: bool = False


class BidResponse(BaseModel):
    id: int
    job_id: int
    accountant_id: int
    price: Decimal
    currency: str
    pricing_model: str
    delivery_time: str
    proposal_letter: str
    status: str
    created_at: str

    class Config:
        from_attributes = True
'''

CATEGORY_SCHEMA_PY = '''
from typing import Optional
from pydantic import BaseModel


class CategoryResponse(BaseModel):
    id: int
    name: str
    slug: str
    parent_id: Optional[int] = None
    description: Optional[str] = None
    children: list["CategoryResponse"] = []

    class Config:
        from_attributes = True


class CategoryCreateRequest(BaseModel):
    name: str
    slug: str
    parent_id: Optional[int] = None
    description: Optional[str] = None
    sort_order: int = 0
'''

CERTIFICATION_SCHEMA_PY = '''
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
'''

COUNTRY_SCHEMA_PY = '''
from typing import Optional
from pydantic import BaseModel


class CountryResponse(BaseModel):
    id: int
    country_name_en: str
    country_name_ar: Optional[str] = None
    country_iso_code2: str
    currency_iso_code: str
    phone_code: str
    phone_digits_count: Optional[int] = None

    class Config:
        from_attributes = True
'''

DOCUMENT_SCHEMA_PY = '''
from typing import Optional
from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: int
    user_id: int
    document_type: str
    file_name: str
    file_url: str
    file_size: Optional[int] = None
    entity_type: Optional[str] = None
    entity_id: Optional[int] = None
    description: Optional[str] = None
    is_verified: bool
    uploaded_at: str

    class Config:
        from_attributes = True
'''

PLATFORM_CONTENT_SCHEMA_PY = '''
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
'''

AUDIT_LOG_SCHEMA_PY = '''
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
'''

# Services
AUTH_SERVICE_PY = '''
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.user import User
from app.utils.security import hash_password, verify_password, create_access_token
from app.utils.validators import validate_email


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register(self, name: str, email: str, phone: str, password: str, role: str) -> User:
        result = await self.db.execute(select(User).where(User.email == email))
        if result.scalar_one_or_none():
            raise HTTPException(409, "Email already registered")

        result = await self.db.execute(select(User).where(User.phone == phone))
        if result.scalar_one_or_none():
            raise HTTPException(409, "Phone already registered")

        user = User(
            name=name,
            email=email,
            phone=phone,
            password=hash_password(password),
            role=role,
        )
        self.db.add(user)
        await self.db.flush()
        return user

    async def login(self, email: str, password: str) -> dict:
        result = await self.db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        if not user or not verify_password(password, user.password):
            raise HTTPException(401, "Invalid email or password")

        if not user.is_active:
            raise HTTPException(403, "Account is deactivated")

        token = create_access_token(user.id, user.role)
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
            }
        }
'''

JOB_SERVICE_PY = '''
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from sqlalchemy.orm import joinedload
from fastapi import HTTPException
from app.models.job import Job
from app.models.user import User
from app.models.bid import Bid


class JobService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_jobs(self, filters: dict, current_user: User = None) -> tuple[list[Job], int]:
        query = select(Job).options(
            joinedload(Job.client).joinedload(User.client_profile),
            joinedload(Job.category),
        )

        if filters.get("status"):
            query = query.where(Job.status == filters["status"])
        else:
            query = query.where(Job.status == "open")

        if filters.get("search"):
            search_term = f"%{filters['search']}%"
            query = query.where(
                or_(Job.title.ilike(search_term), Job.description.ilike(search_term))
            )

        if filters.get("category"):
            query = query.where(Job.category.has(slug=filters["category"]))

        if filters.get("pricing_model"):
            query = query.where(Job.pricing_model == filters["pricing_model"])

        if filters.get("jurisdiction"):
            query = query.where(Job.jurisdiction == filters["jurisdiction"])

        if filters.get("budget_min"):
            query = query.where(Job.budget_max >= float(filters["budget_min"]))

        if filters.get("budget_max"):
            query = query.where(Job.budget_min <= float(filters["budget_max"]))

        # Sort
        sort_map = {
            "newest": Job.posted_date.desc(),
            "budget_high": Job.budget_max.desc(),
            "budget_low": Job.budget_min.asc(),
            "bids": Job.bids_count.desc(),
            "deadline": Job.deadline.asc(),
        }
        sort_by = sort_map.get(filters.get("sort"), Job.posted_date.desc())
        query = query.order_by(sort_by)

        # Count
        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar()

        # Paginate
        page = int(filters.get("page", 1))
        per_page = int(filters.get("per_page", 12))
        query = query.offset((page - 1) * per_page).limit(per_page)

        result = await self.db.execute(query)
        jobs = result.unique().scalars().all()

        return jobs, total

    async def get_job_detail(self, job_id: int, current_user: User = None) -> dict:
        result = await self.db.execute(
            select(Job)
            .options(
                joinedload(Job.client).joinedload(User.client_profile),
                joinedload(Job.category),
            )
            .where(Job.id == job_id)
        )
        job = result.unique().scalar_one_or_none()

        if not job:
            raise HTTPException(404, "Job not found")

        current_user_bid = None
        if current_user and current_user.role == "accountant":
            bid_result = await self.db.execute(
                select(Bid).where(Bid.job_id == job_id, Bid.accountant_id == current_user.id)
            )
            bid = bid_result.scalar_one_or_none()
            if bid:
                current_user_bid = {
                    "id": bid.id,
                    "price": str(bid.price),
                    "status": bid.status,
                    "submitted_at": str(bid.created_at),
                }

        return {
            "job": job,
            "current_user_bid": current_user_bid,
        }
'''

BID_SERVICE_PY = '''
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
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

        if job.deadline and job.deadline < func.current_date():
            raise HTTPException(400, "The deadline for this job has passed")

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

        # Update denormalized counters
        job.bids_count = (job.bids_count or 0) + 1
        if job.bids_min_price is None or bid_data["price"] < job.bids_min_price:
            job.bids_min_price = bid_data["price"]
        if job.bids_max_price is None or bid_data["price"] > job.bids_max_price:
            job.bids_max_price = bid_data["price"]

        await self.db.flush()
        return bid

    async def get_my_bids(self, accountant_id: int) -> list[Bid]:
        result = await self.db.execute(
            select(Bid).where(Bid.accountant_id == accountant_id).order_by(Bid.created_at.desc())
        )
        return result.scalars().all()
'''

MATCH_SERVICE_PY = '''
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.job import Job
from app.models.user import User
from app.models.accountant_profile import AccountantProfile


class MatchService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def calculate_match(self, job_id: int, accountant: User) -> dict:
        result = await self.db.execute(select(Job).where(Job.id == job_id))
        job = result.scalar_one_or_none()

        if not job or accountant.role != "accountant":
            return {"score": 0, "matched": [], "missing": [], "warnings": []}

        profile_result = await self.db.execute(
            select(AccountantProfile).where(AccountantProfile.user_id == accountant.id)
        )
        profile = profile_result.scalar_one_or_none()

        if not profile:
            return {"score": 0, "matched": [], "missing": ["Complete your profile"], "warnings": ["Profile incomplete"]}

        matched = []
        missing = []
        warnings = []

        # Check certifications
        if job.required_certifications:
            # Simplified — would check accountant_certifications in production
            pass

        # Check software
        if job.required_software:
            pass

        # Check jurisdiction
        if job.jurisdiction and profile.jurisdictions_served:
            if job.jurisdiction in profile.jurisdictions_served:
                matched.append(f"Jurisdiction: {job.jurisdiction}")
            else:
                missing.append(f"Jurisdiction: {job.jurisdiction}")
                warnings.append("This job requires a jurisdiction not in your profile")

        total_checks = len(matched) + len(missing)
        score = round((len(matched) / total_checks * 100)) if total_checks > 0 else 0

        return {
            "score": score,
            "matched": matched,
            "missing": missing,
            "warnings": warnings,
        }
'''

AUDIT_SERVICE_PY = '''
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
'''

FILE_SERVICE_PY = '''
import os
import uuid
from fastapi import UploadFile, HTTPException
from app.config import settings


ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx", ".png", ".jpg", ".jpeg"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


class FileService:
    @staticmethod
    async def save_upload(upload_file: UploadFile, subdirectory: str = "documents") -> dict:
        ext = os.path.splitext(upload_file.filename or "")[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(400, f"File type {ext} not allowed")

        contents = await upload_file.read()
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(400, "File size exceeds 10MB limit")

        unique_name = f"{uuid.uuid4()}{ext}"
        upload_dir = os.path.join(settings.UPLOAD_DIR, subdirectory)
        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, unique_name)
        with open(file_path, "wb") as f:
            f.write(contents)

        return {
            "file_name": upload_file.filename,
            "file_url": f"/{upload_dir}/{unique_name}",
            "file_size": len(contents),
            "file_type": upload_file.content_type or ext,
        }
'''

# API Routes
DEPS_PY = '''
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.user import User
from app.utils.security import decode_access_token

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    token = credentials.credentials
    try:
        payload = decode_access_token(token)
        user_id = int(payload.get("sub"))
    except Exception:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or expired token")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user or not user.is_active:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User not found or inactive")
    return user


def require_role(*roles: str):
    async def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Insufficient permissions")
        return current_user
    return role_checker


async def get_optional_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User | None:
    try:
        return await get_current_user(credentials, db)
    except HTTPException:
        return None
'''

V1_ROUTER_PY = '''
from fastapi import APIRouter
from app.api.v1 import auth, jobs, bids, categories, certifications, countries, content, profile
from app.api.v1.admin.router import admin_router

api_v1_router = APIRouter()

api_v1_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_v1_router.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
api_v1_router.include_router(bids.router, prefix="/jobs", tags=["Bids"])
api_v1_router.include_router(categories.router, prefix="/categories", tags=["Categories"])
api_v1_router.include_router(certifications.router, prefix="/certifications", tags=["Certifications"])
api_v1_router.include_router(countries.router, prefix="/countries", tags=["Countries"])
api_v1_router.include_router(content.router, prefix="/content", tags=["Content"])
api_v1_router.include_router(profile.router, prefix="/my-profile", tags=["Profile"])
api_v1_router.include_router(admin_router, prefix="/admin", tags=["Admin"])
'''

AUTH_ROUTES_PY = '''
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.auth import RegisterRequest, LoginRequest
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register")
async def register(request: RegisterRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    user = await service.register(
        name=request.name,
        email=request.email,
        phone=request.phone,
        password=request.password,
        role=request.role,
    )
    return {"message": "Registration successful", "user_id": user.id}


@router.post("/login")
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.login(request.email, request.password)
'''

JOBS_ROUTES_PY = '''
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.api.deps import get_optional_user
from app.services.job_service import JobService

router = APIRouter()


@router.get("")
async def list_jobs(
    search: str = Query(None),
    category: str = Query(None),
    budget_min: float = Query(None),
    budget_max: float = Query(None),
    currency: str = Query(None),
    pricing_model: str = Query(None),
    jurisdiction: str = Query(None),
    status: str = Query("open"),
    sort: str = Query("newest"),
    page: int = Query(1),
    per_page: int = Query(12),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_optional_user),
):
    service = JobService(db)
    filters = {
        "search": search, "category": category, "budget_min": budget_min,
        "budget_max": budget_max, "currency": currency, "pricing_model": pricing_model,
        "jurisdiction": jurisdiction, "status": status, "sort": sort,
        "page": page, "per_page": per_page,
    }
    jobs, total = await service.list_jobs(filters)
    return {
        "data": jobs,
        "meta": {"current_page": page, "per_page": per_page, "total": total}
    }


@router.get("/{job_id}")
async def get_job_detail(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_optional_user),
):
    service = JobService(db)
    return await service.get_job_detail(job_id, current_user)
'''

BIDS_ROUTES_PY = '''
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.api.deps import get_current_user, require_role
from app.schemas.bid import BidCreateRequest
from app.services.bid_service import BidService

router = APIRouter()


@router.post("/{job_id}/bids")
async def submit_bid(
    job_id: int,
    request: BidCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("accountant")),
):
    service = BidService(db)
    bid = await service.submit_bid(job_id, current_user, request.model_dump())
    return {"message": "Bid submitted successfully", "data": {"id": bid.id, "status": bid.status}}


@router.get("/my-bids")
async def get_my_bids(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("accountant")),
):
    service = BidService(db)
    bids = await service.get_my_bids(current_user.id)
    return {"data": bids}
'''

CATEGORIES_ROUTES_PY = '''
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.category import Category

router = APIRouter()


@router.get("")
async def list_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Category).where(Category.is_active == True).order_by(Category.sort_order)
    )
    categories = result.scalars().all()
    return {"data": categories}
'''

CERTIFICATIONS_ROUTES_PY = '''
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.certification import Certification

router = APIRouter()


@router.get("")
async def list_certifications(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Certification).where(Certification.is_active == True)
    )
    return {"data": result.scalars().all()}
'''

COUNTRIES_ROUTES_PY = '''
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.country import Country

router = APIRouter()


@router.get("")
async def list_countries(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Country).where(Country.is_active == True)
    )
    return {"data": result.scalars().all()}
'''

CONTENT_ROUTES_PY = '''
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.database import get_db
from app.models.platform_content import PlatformContent

router = APIRouter()


@router.get("/{key}")
async def get_content(key: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(PlatformContent).where(
            PlatformContent.key == key,
            PlatformContent.is_active == True
        )
    )
    content = result.scalar_one_or_none()
    if not content:
        raise HTTPException(404, "Content not found")
    return {"data": content}
'''

PROFILE_ROUTES_PY = '''
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.api.deps import get_current_user, require_role

router = APIRouter()


@router.get("")
async def get_my_profile(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    return {"data": current_user}
'''

# Admin Routes
ADMIN_ROUTER_PY = '''
from fastapi import APIRouter
from app.api.v1.admin import (
    dashboard, users, jobs, bids, categories, certifications,
    software_skills, countries, documents, content, audit_logs, restrictions,
)

admin_router = APIRouter()

admin_router.include_router(dashboard.router, tags=["Admin - Dashboard"])
admin_router.include_router(users.router, tags=["Admin - Users"])
admin_router.include_router(jobs.router, tags=["Admin - Jobs"])
admin_router.include_router(bids.router, tags=["Admin - Bids"])
admin_router.include_router(categories.router, tags=["Admin - Categories"])
admin_router.include_router(certifications.router, tags=["Admin - Certifications"])
admin_router.include_router(software_skills.router, tags=["Admin - Software Skills"])
admin_router.include_router(countries.router, tags=["Admin - Countries"])
admin_router.include_router(documents.router, tags=["Admin - Documents"])
admin_router.include_router(content.router, tags=["Admin - Content"])
admin_router.include_router(audit_logs.router, tags=["Admin - Audit Logs"])
admin_router.include_router(restrictions.router, tags=["Admin - Restrictions"])
'''

ADMIN_DASHBOARD_PY = '''
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.api.deps import require_role
from app.models.user import User
from app.models.job import Job
from app.models.bid import Bid

router = APIRouter()


@router.get("/dashboard/stats")
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    total_users = (await db.execute(select(func.count(User.id)))).scalar()
    total_jobs = (await db.execute(select(func.count(Job.id)))).scalar()
    total_bids = (await db.execute(select(func.count(Bid.id)))).scalar()

    return {
        "data": {
            "total_users": total_users,
            "total_jobs": total_jobs,
            "total_bids": total_bids,
        }
    }
'''

ADMIN_USERS_PY = '''
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.api.deps import require_role
from app.models.user import User

router = APIRouter()


@router.get("/users")
async def list_users(
    role: str = Query(None),
    page: int = Query(1),
    per_page: int = Query(25),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    query = select(User)
    if role:
        query = query.where(User.role == role)

    total = (await db.execute(select(func.count()).select_from(query.subquery()))).scalar()
    query = query.offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)

    return {
        "data": result.scalars().all(),
        "meta": {"page": page, "per_page": per_page, "total": total}
    }
'''

ADMIN_JOBS_PY = '''
from fastapi import APIRouter, Depends
from app.api.deps import require_role

router = APIRouter()


@router.get("/jobs")
async def list_jobs(current_user = Depends(require_role("admin"))):
    return {"data": [], "message": "Admin jobs management"}
'''

ADMIN_BIDS_PY = '''
from fastapi import APIRouter, Depends
from app.api.deps import require_role

router = APIRouter()


@router.get("/bids")
async def list_bids(current_user = Depends(require_role("admin"))):
    return {"data": [], "message": "Admin bids management"}
'''

ADMIN_CATEGORIES_PY = '''
from fastapi import APIRouter, Depends
from app.api.deps import require_role

router = APIRouter()


@router.get("/categories")
async def list_categories(current_user = Depends(require_role("admin"))):
    return {"data": [], "message": "Admin categories management"}
'''

ADMIN_CERTIFICATIONS_PY = '''
from fastapi import APIRouter, Depends
from app.api.deps import require_role

router = APIRouter()


@router.get("/certifications")
async def list_certifications(current_user = Depends(require_role("admin"))):
    return {"data": [], "message": "Admin certifications management"}
'''

ADMIN_SOFTWARE_SKILLS_PY = '''
from fastapi import APIRouter, Depends
from app.api.deps import require_role

router = APIRouter()


@router.get("/software-skills")
async def list_software_skills(current_user = Depends(require_role("admin"))):
    return {"data": [], "message": "Admin software skills management"}
'''

ADMIN_COUNTRIES_PY = '''
from fastapi import APIRouter, Depends
from app.api.deps import require_role

router = APIRouter()


@router.get("/countries")
async def list_countries(current_user = Depends(require_role("admin"))):
    return {"data": [], "message": "Admin countries management"}
'''

ADMIN_DOCUMENTS_PY = '''
from fastapi import APIRouter, Depends
from app.api.deps import require_role

router = APIRouter()


@router.get("/documents")
async def list_documents(current_user = Depends(require_role("admin"))):
    return {"data": [], "message": "Admin documents management"}
'''

ADMIN_CONTENT_PY = '''
from fastapi import APIRouter, Depends
from app.api.deps import require_role

router = APIRouter()


@router.get("/content")
async def list_content(current_user = Depends(require_role("admin"))):
    return {"data": [], "message": "Admin content management"}
'''

ADMIN_AUDIT_LOGS_PY = '''
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.api.deps import require_role
from app.models.audit_log import AuditLog

router = APIRouter()


@router.get("/audit-logs")
async def list_audit_logs(
    page: int = Query(1),
    per_page: int = Query(25),
    action_category: str = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    query = select(AuditLog).order_by(AuditLog.created_at.desc())
    if action_category:
        query = query.where(AuditLog.action_category == action_category)

    total = (await db.execute(select(func.count()).select_from(query.subquery()))).scalar()
    query = query.offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)

    return {
        "data": result.scalars().all(),
        "meta": {"page": page, "per_page": per_page, "total": total}
    }
'''

ADMIN_RESTRICTIONS_PY = '''
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.database import get_db
from app.api.deps import require_role
from app.models.user import User
from pydantic import BaseModel
from typing import Optional


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


router = APIRouter()


@router.get("/me/audit-toggle")
async def get_audit_toggle(current_user = Depends(require_role("admin"))):
    return {"audit_enabled": current_user.audit_enabled}


@router.patch("/me/audit-toggle")
async def toggle_audit(
    request: AuditToggleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    current_user.audit_enabled = request.audit_enabled
    await db.flush()
    return {"message": "Audit logging updated", "audit_enabled": current_user.audit_enabled}


@router.get("/users/{user_id}/restrictions")
async def get_restrictions(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, "User not found")
    return {"user_id": user.id, "restrictions": user.restrictions}


@router.patch("/users/{user_id}/restrictions")
async def set_restrictions(
    user_id: int,
    request: RestrictionsUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, "User not found")

    from datetime import datetime
    user.restrictions = {
        "can_submit_bids": request.can_submit_bids,
        "can_view_jobs": request.can_view_jobs,
        "can_view_nda_jobs": request.can_view_nda_jobs,
        "can_upload_documents": request.can_upload_documents,
        "can_edit_profile": request.can_edit_profile,
        "can_login": request.can_login,
        "restricted_reason": request.restricted_reason,
        "restricted_at": datetime.utcnow().isoformat(),
        "restricted_by": current_user.id,
    }
    await db.flush()
    return {"message": "Restrictions updated", "user_id": user.id, "restrictions": user.restrictions}


@router.delete("/users/{user_id}/restrictions")
async def remove_restrictions(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, "User not found")
    user.restrictions = None
    await db.flush()
    return {"message": "Restrictions removed", "user_id": user.id}
'''

# Middleware
AUTH_MIDDLEWARE_PY = '''
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.security import decode_access_token
from app.config import settings


PUBLIC_PATHS = [
    "/", "/docs", "/openapi.json", "/redoc",
    "/api/v1/auth/register", "/api/v1/auth/login",
    "/api/v1/jobs", "/api/v1/categories", "/api/v1/certifications",
    "/api/v1/countries", "/api/v1/content",
]


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Allow public paths
        for public_path in PUBLIC_PATHS:
            if path.startswith(public_path):
                return await call_next(request)

        # Allow GET job detail
        if path.startswith("/api/v1/jobs/") and request.method == "GET":
            return await call_next(request)

        response = await call_next(request)
        return response
'''

AUDIT_MIDDLEWARE_PY = '''
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.services.audit_service import AuditService


class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        # Audit logging is handled at the service level for precise control
        return response
'''

MAIN_PY = '''
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.v1.router import api_v1_router
from app.middleware.auth_middleware import AuthMiddleware

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs" if settings.APP_ENV == "development" else None,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(api_v1_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
'''


# ============================================================
# RUN SETUP
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("ACCOUNTANT HUB - BACKEND SETUP")
    print("=" * 60)

    os.chdir(BASE_DIR)

    create_core_files()
    create_database_files()
    create_schema_files()
    create_service_files()
    create_api_files()
    create_middleware_files()
    create_main_file()

    print_summary()