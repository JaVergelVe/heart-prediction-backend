from datetime import datetime, timezone

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.core.timefmt import to_iso_z
from app.schemas.auth import LoginRequest, RegisterRequest
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    body: RegisterRequest,
    db: Session = Depends(get_db),
) -> dict:
    user = auth_service.register_user(db, body)
    settings = get_settings()
    token = auth_service.create_access_token(user.id)
    return {
        "data": {
            "user_id": user.id,
            "email": user.email,
            "access_token": token,
            "token_type": "Bearer",
            "expires_in": settings.access_token_expire_seconds,
            "created_at": to_iso_z(user.created_at),
        },
    }


@router.post("/login")
def login(
    body: LoginRequest,
    db: Session = Depends(get_db),
) -> dict:
    user = auth_service.authenticate_user(db, str(body.email), body.password)
    settings = get_settings()
    token = auth_service.create_access_token(user.id)
    last = user.last_login or datetime.now(timezone.utc)
    return {
        "data": {
            "user_id": user.id,
            "email": user.email,
            "access_token": token,
            "token_type": "Bearer",
            "expires_in": settings.access_token_expire_seconds,
            "last_login": to_iso_z(last),
        },
    }
