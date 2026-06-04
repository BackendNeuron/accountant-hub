
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
