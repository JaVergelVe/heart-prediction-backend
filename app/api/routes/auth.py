from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.constants import auth as auth_c
from app.constants import http as http_c
from app.constants import messages as msg_c
from app.core.config import get_settings
from app.core.database import get_db
from app.core.timefmt import to_iso_z
from app.schemas.auth import LoginRequest, RegisterRequest
from app.services import auth_service

router = APIRouter(prefix=auth_c.ROUTER_PREFIX_AUTH, tags=[auth_c.ROUTER_TAG_AUTH])


@router.post(auth_c.ROUTE_REGISTER, status_code=http_c.HTTP_201_CREATED)
def register(
    body: RegisterRequest,
    db: Session = Depends(get_db),
) -> dict:
    user = auth_service.register_user(db, body)
    settings = get_settings()
    token = auth_service.create_access_token(user.id)
    return {
        msg_c.KEY_DATA: {
            msg_c.KEY_USER_ID: user.id,
            msg_c.KEY_EMAIL: user.email,
            msg_c.KEY_ACCESS_TOKEN: token,
            msg_c.KEY_TOKEN_TYPE: auth_c.TOKEN_TYPE_BEARER,
            msg_c.KEY_EXPIRES_IN: settings.access_token_expire_seconds,
            msg_c.KEY_CREATED_AT: to_iso_z(user.created_at),
        },
    }


@router.post(auth_c.ROUTE_LOGIN)
def login(
    body: LoginRequest,
    db: Session = Depends(get_db),
) -> dict:
    user = auth_service.authenticate_user(db, str(body.email), body.password)
    settings = get_settings()
    token = auth_service.create_access_token(user.id)
    last = user.last_login or datetime.now(timezone.utc)
    return {
        msg_c.KEY_DATA: {
            msg_c.KEY_USER_ID: user.id,
            msg_c.KEY_EMAIL: user.email,
            msg_c.KEY_ACCESS_TOKEN: token,
            msg_c.KEY_TOKEN_TYPE: auth_c.TOKEN_TYPE_BEARER,
            msg_c.KEY_EXPIRES_IN: settings.access_token_expire_seconds,
            msg_c.KEY_LAST_LOGIN: to_iso_z(last),
        },
    }
