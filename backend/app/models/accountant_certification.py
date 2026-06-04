
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
