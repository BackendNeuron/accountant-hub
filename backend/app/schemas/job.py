
from typing import Optional
from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field


class JobFilterParams(BaseModel):
    search: Optional[str] = None
    category: Optional[str] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    currency: Optional[str] = None
    pricing_model: Optional[str] = None
    jurisdiction: Optional[str] = None
    accounting_standard: Optional[str] = None
    certification: Optional[str] = None
    software: Optional[str] = None
    engagement_type: Optional[str] = None
    nda_required: Optional[bool] = None
    status: Optional[str] = "open"
    sort: Optional[str] = "newest"
    page: int = 1
    per_page: int = 12


class JobCreateRequest(BaseModel):
    title: str = Field(..., min_length=5, max_length=255)
    description: str = Field(..., min_length=50)
    category_id: int
    budget_min: Decimal
    budget_max: Decimal
    currency: str = "USD"
    pricing_model: str = "fixed"
    deadline: date
    expected_delivery_time: Optional[str] = None
    engagement_type: str = "one_time"
    jurisdiction: Optional[str] = None
    accounting_standard: Optional[str] = None
    required_certifications: Optional[list[str]] = None
    required_software: Optional[list[str]] = None
    required_skills: Optional[list[str]] = None
    minimum_experience_years: Optional[int] = None
    company_industry_context: Optional[str] = None
    nda_required: bool = False


class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    client_id: int
    company_name: Optional[str] = None
    category: Optional[dict] = None
    budget_min: Decimal
    budget_max: Decimal
    currency: str
    pricing_model: str
    deadline: date
    engagement_type: str
    jurisdiction: Optional[str] = None
    accounting_standard: Optional[str] = None
    required_certifications: Optional[list] = None
    required_software: Optional[list] = None
    required_skills: Optional[list] = None
    nda_required: bool
    status: str
    bids_count: int
    bids_min_price: Optional[Decimal] = None
    bids_max_price: Optional[Decimal] = None
    posted_date: date
    current_user_bid: Optional[dict] = None

    class Config:
        from_attributes = True
