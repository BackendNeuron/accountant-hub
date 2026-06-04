
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.api.deps import require_role, get_current_user
from app.services.match_service import MatchService
from app.models.user import User

router = APIRouter()


@router.get("/{job_id}/match-score")
async def get_match_score(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("accountant")),
):
    service = MatchService(db)
    result = await service.calculate_match(job_id, current_user)
    return {"data": result}
