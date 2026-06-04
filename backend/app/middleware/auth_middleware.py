
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.security import decode_access_token
from app.config import settings


PUBLIC_PATHS = [
    "/", "/docs", "/openapi.json", "/redoc",
    "/api/v1/auth/register", "/api/v1/auth/login",
    "/api/v1/jobs", "/api/v1/categories", "/api/v1/certifications",
    "/api/v1/countries", "/api/v1/content",
]


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Allow public paths
        for public_path in PUBLIC_PATHS:
            if path.startswith(public_path):
                return await call_next(request)

        # Allow GET job detail
        if path.startswith("/api/v1/jobs/") and request.method == "GET":
            return await call_next(request)

        response = await call_next(request)
        return response
