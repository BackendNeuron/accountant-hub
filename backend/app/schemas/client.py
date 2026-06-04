from typing import Optional
from decimal import Decimal
from datetime import date
from pydantic import BaseModel, Field, field_validator


class JobCreateRequest(BaseModel):
    title: str = Field(..., min_length=5, max_length=255)
    description: str = Field(..., min_length=50)
    category_id: int
    budget_min: Decimal = Field(..., gt=0)
    budget_max: Decimal = Field(..., gt=0)
    currency: str = "USD"
    pricing_model: str = Field(..., pattern="^(fixed|hourly|retainer)$")
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

    @field_validator('deadline')
    @classmethod
    def deadline_must_be_future(cls, v):
        if v < date.today():
            raise ValueError('Deadline must be today or in the future')
        return v

    @field_validator('budget_max')
    @classmethod
    def budget_max_must_exceed_min(cls, v, info):
        if 'budget_min' in info.data and v < info.data['budget_min']:
            raise ValueError('Budget max must be greater than budget min')
        return v


class JobUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    budget_min: Optional[Decimal] = None
    budget_max: Optional[Decimal] = None
    currency: Optional[str] = None
    pricing_model: Optional[str] = None
    deadline: Optional[date] = None
    expected_delivery_time: Optional[str] = None
    engagement_type: Optional[str] = None
    jurisdiction: Optional[str] = None
    accounting_standard: Optional[str] = None
    required_certifications: Optional[list[str]] = None
    required_software: Optional[list[str]] = None
    required_skills: Optional[list[str]] = None
    minimum_experience_years: Optional[int] = None
    nda_required: Optional[bool] = None


class JobStatusUpdateRequest(BaseModel):
    status: str = Field(..., pattern="^(open|closed)$")
    closed_reason: Optional[str] = None