from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.constants import auth as auth_c
from app.constants import messages as msg_c
from app.core.database import get_db
from app.models import User
from app.services import user_service

router = APIRouter(prefix=auth_c.ROUTER_PREFIX_USERS, tags=[auth_c.ROUTER_TAG_USERS])


@router.get(auth_c.ROUTE_USERS_ME)
def read_me(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> dict:
    return {msg_c.KEY_DATA: user_service.build_me_data(db, current_user)}
