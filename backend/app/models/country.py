
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base


class Country(Base):
    __tablename__ = "countries"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    country_name_ar = Column(String(255), nullable=True)
    country_name_en = Column(String(255), nullable=False)
    country_iso_code2 = Column(String(2), nullable=False, unique=True)
    country_iso_code3 = Column(String(3), nullable=False, unique=True)
    country_iso_numeric = Column(String(3), nullable=True)
    currency_name = Column(String(100), nullable=False)
    currency_iso_code = Column(String(3), nullable=False, index=True)
    currency_iso_number = Column(String(3), nullable=True)
    phone_code = Column(String(5), nullable=False)
    phone_digits_count = Column(Integer, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    created_by = Column(BigInteger, nullable=True)
    updated_by = Column(BigInteger, nullable=True)
