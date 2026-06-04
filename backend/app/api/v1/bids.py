from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.api.deps import get_current_user, require_role
from app.schemas.bid import BidCreateRequest
from app.services.bid_service import BidService
from app.services.audit_service import AuditService

router = APIRouter()


@router.post("/{job_id}/bids")
async def submit_bid(
    job_id: int,
    request: BidCreateRequest,
    req: Request,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("accountant")),
):
    service = BidService(db)
    bid = await service.submit_bid(job_id, current_user, request.model_dump())
    
    audit = AuditService(db)
    await audit.log(
        action="bid.submitted", action_category="bid",
        entity_type="Bid", entity_id=bid.id,
        user_id=current_user.id, user_email=current_user.email,
        user_role=current_user.role,
        description=f"Bid of {bid.price} {bid.currency} submitted on job #{job_id}",
        new_values={"price": str(bid.price), "currency": bid.currency, "job_id": job_id},
        ip_address=req.client.host if req.client else None,
    )
    return {"message": "Bid submitted successfully", "data": {"id": bid.id, "status": bid.status}}


@router.get("/my-bids")
async def get_my_bids(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("accountant")),
):
    service = BidService(db)
    bids, total = await service.get_my_bids(current_user.id)
    return {"data": bids, "meta": {"total": total}}
