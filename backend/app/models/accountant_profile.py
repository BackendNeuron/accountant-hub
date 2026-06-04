
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
