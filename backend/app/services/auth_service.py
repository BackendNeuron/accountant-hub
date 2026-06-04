
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.user import User
from app.utils.security import hash_password, verify_password, create_access_token
from app.utils.validators import validate_email


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register(self, name: str, email: str, phone: str, password: str, role: str) -> User:
        result = await self.db.execute(select(User).where(User.email == email))
        if result.scalar_one_or_none():
            raise HTTPException(409, "Email already registered")

        result = await self.db.execute(select(User).where(User.phone == phone))
        if result.scalar_one_or_none():
            raise HTTPException(409, "Phone already registered")

        user = User(
            name=name,
            email=email,
            phone=phone,
            password=hash_password(password),
            role=role,
        )
        self.db.add(user)
        await self.db.flush()
        return user

    async def login(self, email: str, password: str) -> dict:
        result = await self.db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        if not user or not verify_password(password, user.password):
            raise HTTPException(401, "Invalid email or password")

        if not user.is_active:
            raise HTTPException(403, "Account is deactivated")

        token = create_access_token(user.id, user.role)
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
            }
        }
