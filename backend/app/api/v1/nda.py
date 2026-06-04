from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.api.deps import require_role, get_current_user
from app.services.nda_service import NDAService
from app.services.audit_service import AuditService
from app.models.user import User

router = APIRouter()


@router.post('/{job_id}/accept-nda')
async def accept_nda(
    job_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role('accountant')),
):
    service = NDAService(db)
    ip_address = request.client.host if request.client else None
    nda = await service.accept_nda(job_id, current_user, ip_address)

    audit = AuditService(db)
    await audit.log(
        action='nda.accepted', action_category='nda',
        entity_type='NDAAcceptance', entity_id=nda.id,
        user_id=current_user.id, user_email=current_user.email,
        user_role=current_user.role,
        description=f'NDA accepted for job #{job_id}',
        ip_address=ip_address,
    )
    return {'message': 'NDA accepted successfully', 'accepted': True, 'job_id': job_id}