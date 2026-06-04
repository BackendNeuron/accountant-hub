
from pydantic import BaseModel


class NDAAcceptRequest(BaseModel):
    agree: bool = True


class NDAResponse(BaseModel):
    message: str
    accepted: bool
    job_id: int
