
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
