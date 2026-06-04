
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field


class BidCreateRequest(BaseModel):
    price: Decimal = Field(..., gt=0)
    pricing_model: str = Field(..., pattern="^(fixed|hourly|retainer)$")
    includes_all_fees: bool = True
    additional_costs_description: Optional[str] = None
    estimated_hours: Optional[int] = None
    number_of_entities: Optional[int] = None
    delivery_time: str = Field(..., min_length=2, max_length=100)
    services_included: list[str]
    milestones: Optional[list[dict]] = None
    engagement_terms: Optional[str] = None
    proposal_letter: str = Field(..., min_length=50)
    jurisdiction_confirmed: bool = False
    terms_accepted: bool = False


class BidResponse(BaseModel):
    id: int
    job_id: int
    accountant_id: int
    price: Decimal
    currency: str
    pricing_model: str
    delivery_time: str
    proposal_letter: str
    status: str
    created_at: str

    class Config:
        from_attributes = True
