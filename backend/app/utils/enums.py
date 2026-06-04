
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
