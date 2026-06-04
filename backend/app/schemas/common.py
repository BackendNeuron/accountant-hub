
from typing import TypeVar, Generic, Optional
from pydantic import BaseModel

T = TypeVar("T")


class PaginationParams(BaseModel):
    page: int = 1
    per_page: int = 12


class PaginatedResponse(BaseModel, Generic[T]):
    data: list[T]
    meta: dict


class MessageResponse(BaseModel):
    message: str
    detail: Optional[str] = None
