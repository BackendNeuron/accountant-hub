
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
