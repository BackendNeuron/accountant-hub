
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
