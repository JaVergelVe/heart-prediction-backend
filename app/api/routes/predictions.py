from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.constants import auth as auth_c
from app.constants import http as http_c
from app.constants import messages as msg_c
from app.core.database import get_db
from app.models import User
from app.schemas.prediction import AnonymousPredictionRequest, AuthenticatedPredictionRequest
from app.services import prediction_service

router = APIRouter(prefix=auth_c.ROUTER_PREFIX_PREDICTIONS, tags=[auth_c.ROUTER_TAG_PREDICTIONS])


@router.post(auth_c.ROUTE_PREDICTIONS_ANONYMOUS, status_code=http_c.HTTP_201_CREATED)
def predict_anonymous(
    body: AnonymousPredictionRequest,
    db: Annotated[Session, Depends(get_db)],
) -> dict:
    return {msg_c.KEY_DATA: prediction_service.create_anonymous_prediction(db, body)}


@router.post("", status_code=http_c.HTTP_201_CREATED)
def predict_authenticated(
    body: AuthenticatedPredictionRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> dict:
    return {
        msg_c.KEY_DATA: prediction_service.create_authenticated_prediction(
            db, current_user.id, body
        ),
    }
