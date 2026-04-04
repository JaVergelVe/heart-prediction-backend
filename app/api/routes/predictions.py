from typing import Annotated

from fastapi import APIRouter, Body, Depends, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.constants import auth as auth_c
from app.constants import http as http_c
from app.constants import messages as msg_c
from app.constants import pdf_export as pdf_c
from app.constants import prediction as pred_c
from app.core.database import get_db
from app.models import User
from app.schemas.prediction import (
    AnonymousPredictionRequest,
    AuthenticatedPredictionRequest,
    SimulationPatchRequest,
)
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


@router.get(auth_c.ROUTE_PREDICTIONS_HISTORY)
def list_prediction_history(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    limit: Annotated[
        int,
        Query(
            ge=pred_c.HISTORY_QUERY_LIMIT_GE_MIN,
            le=pred_c.HISTORY_LIMIT_MAX,
            description=pred_c.QUERY_DESC_HISTORY_LIMIT,
        ),
    ] = pred_c.HISTORY_LIMIT_DEFAULT,
    offset: Annotated[
        int,
        Query(ge=pred_c.HISTORY_QUERY_OFFSET_GE_MIN, description=pred_c.QUERY_DESC_HISTORY_OFFSET),
    ] = pred_c.HISTORY_OFFSET_DEFAULT,
    sort: Annotated[str, Query(description=pred_c.QUERY_DESC_HISTORY_SORT)] = (
        pred_c.HISTORY_SORT_PREDICTION_TIMESTAMP
    ),
    order: Annotated[str, Query(description=pred_c.QUERY_DESC_HISTORY_ORDER)] = (
        pred_c.HISTORY_ORDER_DESC
    ),
) -> dict:
    return {
        msg_c.KEY_DATA: prediction_service.list_prediction_history(
            db,
            current_user.id,
            limit=limit,
            offset=offset,
            sort=sort,
            order=order,
        ),
    }


@router.post(auth_c.ROUTE_PREDICTIONS_SIMULATE)
def simulate_prediction_what_if(
    prediction_id: str,
    body: Annotated[dict, Body()],
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> dict:
    prediction_service.validate_simulation_request_keys(body)
    patch = SimulationPatchRequest.model_validate(body)
    return {
        msg_c.KEY_DATA: prediction_service.simulate_what_if(
            db, current_user.id, prediction_id, patch
        ),
    }


@router.get(
    auth_c.ROUTE_PREDICTIONS_EXPORT_PDF,
    response_class=Response,
    responses={
        http_c.HTTP_200_OK: {
            "content": {"application/pdf": {}},
            "description": "PDF file download",
        },
    },
)
def export_prediction_pdf(
    prediction_id: str,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Response:
    pdf_bytes, filename = prediction_service.export_prediction_pdf(
        db, current_user.id, prediction_id
    )
    headers = {
        "Content-Disposition": pdf_c.CONTENT_DISPOSITION_ATTACHMENT.format(filename=filename),
    }
    return Response(content=pdf_bytes, media_type=pdf_c.PDF_MEDIA_TYPE, headers=headers)


@router.get(auth_c.ROUTE_PREDICTIONS_DETAIL)
def get_prediction_detail(
    prediction_id: str,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> dict:
    return {
        msg_c.KEY_DATA: prediction_service.get_prediction_detail(
            db, current_user.id, prediction_id
        ),
    }
