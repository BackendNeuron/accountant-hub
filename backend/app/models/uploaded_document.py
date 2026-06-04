
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
