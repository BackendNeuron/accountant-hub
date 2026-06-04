from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.auth import RegisterRequest, LoginRequest
from app.services.auth_service import AuthService
from app.services.audit_service import AuditService

router = APIRouter()


@router.post("/register")
async def register(request: RegisterRequest, req: Request, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    user = await service.register(
        name=request.name, email=request.email, phone=request.phone,
        password=request.password, role=request.role,
    )
    audit = AuditService(db)
    await audit.log(
        action="user.registered", action_category="authentication",
        entity_type="User", entity_id=user.id,
        user_id=user.id, user_email=user.email, user_role=user.role,
        description=f"User {user.email} registered as {user.role}",
        new_values={"name": user.name, "email": user.email, "role": user.role},
        ip_address=req.client.host if req.client else None,
    )
    return {"message": "Registration successful", "user_id": user.id}


@router.post("/login")
async def login(request: LoginRequest, req: Request, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    result = await service.login(request.email, request.password)
    
    audit = AuditService(db)
    await audit.log(
        action="user.login", action_category="authentication",
        entity_type="User", entity_id=result["user"]["id"],
        user_id=result["user"]["id"], user_email=result["user"]["email"],
        user_role=result["user"]["role"],
        description=f"User {result['user']['email']} logged in",
        ip_address=req.client.host if req.client else None,
    )
    return result
