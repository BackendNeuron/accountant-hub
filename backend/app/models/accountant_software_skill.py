
from sqlalchemy import Column, BigInteger, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class AccountantSoftwareSkill(Base):
    __tablename__ = "accountant_software_skills"

    accountant_profile_id = Column(BigInteger, ForeignKey("accountant_profiles.id", ondelete="CASCADE"), primary_key=True)
    software_skill_id = Column(BigInteger, ForeignKey("software_skills.id", ondelete="CASCADE"), primary_key=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
