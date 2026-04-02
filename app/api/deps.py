from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.constants import (
    AUTH_SCHEME_BEARER_LOWER,
    ERROR_CODE_UNAUTHORIZED,
    MSG_TOKEN_INVALID_OR_EXPIRED,
    MSG_TOKEN_REQUIRED,
)
from app.core.database import get_db
from app.core.exceptions import APIError
from app.models import User
from app.services.auth_service import decode_access_token

_bearer = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(_bearer),
    ],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    if credentials is None or credentials.scheme.lower() != AUTH_SCHEME_BEARER_LOWER:
        raise APIError(
            401,
            code=ERROR_CODE_UNAUTHORIZED,
            message=MSG_TOKEN_REQUIRED,
        )
    user_id = decode_access_token(credentials.credentials)
    user = db.scalars(select(User).where(User.id == user_id)).first()
    if user is None or not user.is_active:
        raise APIError(
            401,
            code=ERROR_CODE_UNAUTHORIZED,
            message=MSG_TOKEN_INVALID_OR_EXPIRED,
        )
    return user
