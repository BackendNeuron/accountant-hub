
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
