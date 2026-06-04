
from typing import Optional
from pydantic import BaseModel


class CountryResponse(BaseModel):
    id: int
    country_name_en: str
    country_name_ar: Optional[str] = None
    country_iso_code2: str
    currency_iso_code: str
    phone_code: str
    phone_digits_count: Optional[int] = None

    class Config:
        from_attributes = True
