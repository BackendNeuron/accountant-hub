
from sqlalchemy import Column, BigInteger, String, Text, Boolean, Integer, DECIMAL, TIMESTAMP, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.database import Base


class Bid(Base):
    __tablename__ = "bids"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    job_id = Column(BigInteger, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True)
    accountant_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    price = Column(DECIMAL(12, 2), nullable=False)
    currency = Column(String(3), nullable=False)
    pricing_model = Column(String(20), nullable=False)
    includes_all_fees = Column(Boolean, nullable=False, default=True)
    additional_costs_description = Column(Text, nullable=True)
    estimated_hours = Column(Integer, nullable=True)
    number_of_entities = Column(Integer, nullable=True)
    delivery_time = Column(String(100), nullable=False)
    services_included = Column(JSONB, nullable=False)
    milestones = Column(JSONB, nullable=True)
    engagement_terms = Column(Text, nullable=True)
    proposal_letter = Column(Text, nullable=False)
    jurisdiction_confirmed = Column(Boolean, nullable=False, default=False)
    terms_accepted = Column(Boolean, nullable=False, default=False)
    status = Column(String(20), nullable=False, default="pending", index=True)
    accepted_at = Column(TIMESTAMP, nullable=True)
    rejected_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), index=True)
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    created_by = Column(BigInteger, nullable=True)
    updated_by = Column(BigInteger, nullable=True)

    __table_args__ = (
        UniqueConstraint("job_id", "accountant_id", name="uq_job_accountant_bid"),
        CheckConstraint("price > 0", name="ck_bid_price_positive"),
        CheckConstraint("pricing_model IN ('fixed', 'hourly', 'retainer')", name="ck_bid_pricing_model"),
        CheckConstraint("status IN ('pending', 'accepted', 'rejected')", name="ck_bid_status"),
    )
