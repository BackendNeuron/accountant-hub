from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.api.deps import require_role, get_current_user
from app.services.client_service import ClientService
from app.services.audit_service import AuditService
from app.schemas.client import JobCreateRequest, JobUpdateRequest, JobStatusUpdateRequest
from app.models.user import User

router = APIRouter()


@router.post('')
async def create_job(
    request: JobCreateRequest,
    req: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role('client')),
):
    service = ClientService(db)
    job = await service.create_job(current_user, request.model_dump())

    audit = AuditService(db)
    await audit.log(
        action='job.created', action_category='job',
        entity_type='Job', entity_id=job.id,
        user_id=current_user.id, user_email=current_user.email,
        user_role=current_user.role,
        description=f'Job posted: {job.title}',
        new_values={'title': job.title, 'budget_min': str(job.budget_min), 'budget_max': str(job.budget_max)},
        ip_address=req.client.host if req.client else None,
    )
    return {'message': 'Job created successfully', 'data': {'id': job.id}}


@router.get('')
async def list_my_jobs(
    page: int = Query(1),
    per_page: int = Query(12),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role('client')),
):
    service = ClientService(db)
    jobs, total = await service.list_my_jobs(current_user.id, page, per_page)
    return {'data': jobs, 'meta': {'page': page, 'per_page': per_page, 'total': total}}


@router.get('/{job_id}')
async def get_my_job(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role('client')),
):
    service = ClientService(db)
    job = await service.get_my_job(job_id, current_user.id)
    return {'data': job}


@router.put('/{job_id}')
async def update_my_job(
    job_id: int,
    request: JobUpdateRequest,
    req: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role('client')),
):
    service = ClientService(db)
    job = await service.update_my_job(job_id, current_user.id, request.model_dump(exclude_none=True))

    audit = AuditService(db)
    await audit.log(
        action='job.updated', action_category='job',
        entity_type='Job', entity_id=job.id,
        user_id=current_user.id, user_email=current_user.email,
        user_role=current_user.role,
        description=f'Job updated: {job.title}',
        ip_address=req.client.host if req.client else None,
    )
    return {'message': 'Job updated successfully', 'data': job}


@router.patch('/{job_id}/status')
async def update_job_status(
    job_id: int,
    request: JobStatusUpdateRequest,
    req: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role('client')),
):
    service = ClientService(db)
    job = await service.update_job_status(job_id, current_user.id, request.status, request.closed_reason)

    audit = AuditService(db)
    await audit.log(
        action='job.status_changed', action_category='job',
        entity_type='Job', entity_id=job.id,
        user_id=current_user.id, user_email=current_user.email,
        user_role=current_user.role,
        description=f'Job #{job_id} status changed to {request.status}',
        new_values={'status': request.status},
        ip_address=req.client.host if req.client else None,
    )
    return {'message': f'Job {request.status}', 'data': {'id': job.id, 'status': job.status}}


@router.get('/{job_id}/bids')
async def get_job_bids(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role('client')),
):
    service = ClientService(db)
    bids = await service.get_job_bids(job_id, current_user.id)
    return {'data': bids}


@router.patch('/{job_id}/bids/{bid_id}/accept')
async def accept_bid(
    job_id: int,
    bid_id: int,
    req: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role('client')),
):
    service = ClientService(db)
    bid = await service.accept_bid(job_id, bid_id, current_user.id)

    audit = AuditService(db)
    await audit.log(
        action='bid.accepted', action_category='bid',
        entity_type='Bid', entity_id=bid.id,
        user_id=current_user.id, user_email=current_user.email,
        user_role=current_user.role,
        description=f'Bid #{bid.id} accepted for job #{job_id}',
        new_values={'status': 'accepted', 'job_closed': True},
        ip_address=req.client.host if req.client else None,
    )
    return {'message': 'Bid accepted - job is now closed', 'data': {'bid_id': bid.id, 'status': bid.status}}


@router.patch('/{job_id}/bids/{bid_id}/reject')
async def reject_bid(
    job_id: int,
    bid_id: int,
    req: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role('client')),
):
    service = ClientService(db)
    bid = await service.reject_bid(job_id, bid_id, current_user.id)

    audit = AuditService(db)
    await audit.log(
        action='bid.rejected', action_category='bid',
        entity_type='Bid', entity_id=bid.id,
        user_id=current_user.id, user_email=current_user.email,
        user_role=current_user.role,
        description=f'Bid #{bid.id} rejected for job #{job_id}',
        new_values={'status': 'rejected'},
        ip_address=req.client.host if req.client else None,
    )
    return {'message': 'Bid rejected', 'data': {'bid_id': bid.id, 'status': bid.status}}