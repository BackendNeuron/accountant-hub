from sqlalchemy import Column, BigInteger, String, Text, Boolean, Integer, DECIMAL, Date, TIMESTAMP, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    client_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    category_id = Column(BigInteger, ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False, index=True)
    budget_min = Column(DECIMAL(12, 2), nullable=False, index=True)
    budget_max = Column(DECIMAL(12, 2), nullable=False, index=True)
    currency = Column(String(3), nullable=False, default="USD", index=True)
    pricing_model = Column(String(20), nullable=False, index=True)
    deadline = Column(Date, nullable=False, index=True)
    expected_delivery_time = Column(String(100), nullable=True)
    engagement_type = Column(String(20), nullable=False, default="one_time", index=True)
    jurisdiction = Column(String(100), nullable=True, index=True)
    accounting_standard = Column(String(50), nullable=True, index=True)
    required_certifications = Column(JSONB, nullable=True)
    required_software = Column(JSONB, nullable=True)
    required_skills = Column(JSONB, nullable=True)
    minimum_experience_years = Column(Integer, nullable=True)
    company_industry_context = Column(String(100), nullable=True)
    nda_required = Column(Boolean, nullable=False, default=False, index=True)
    status = Column(String(20), nullable=False, default="open", index=True)
    closed_reason = Column(String(50), nullable=True)
    posted_date = Column(Date, nullable=False, default=func.current_date(), index=True)
    bids_count = Column(Integer, nullable=False, default=0)
    bids_min_price = Column(DECIMAL(12, 2), nullable=True)
    bids_max_price = Column(DECIMAL(12, 2), nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    created_by = Column(BigInteger, nullable=True)
    updated_by = Column(BigInteger, nullable=True)

    __table_args__ = (
        CheckConstraint("budget_max >= budget_min", name="ck_budget_range"),
        CheckConstraint("deadline >= posted_date", name="ck_deadline_after_posted"),
        CheckConstraint("pricing_model IN ('fixed', 'hourly', 'retainer')", name="ck_pricing_model"),
        CheckConstraint("engagement_type IN ('one_time', 'recurring')", name="ck_engagement_type"),
        CheckConstraint("status IN ('open', 'closed')", name="ck_job_status"),
    )
