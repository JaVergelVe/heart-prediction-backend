"""Prediction lifecycle: anonymous, authenticated, history, detail, simulate, PDF."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.constants import auth as auth_c
from app.constants import http as http_c
from app.constants import messages as msg_c
from app.constants import pdf_export as pdf_c
from app.constants import prediction as pred_c
from app.services.prediction_service import compute_bmi
from tests.conftest import (
    anonymous_prediction_body,
    auth_headers,
    authenticated_prediction_body,
    make_predict_stub,
    prediction_count,
)


def _pred_base() -> str:
    return f"{auth_c.API_V1_PREFIX}{auth_c.ROUTER_PREFIX_PREDICTIONS}"


def test_anonymous_prediction_bmi_and_shap(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "app.services.prediction_service.predict_heart_risk",
        make_predict_stub(25.0),
    )
    body = anonymous_prediction_body()
    r = client.post(f"{_pred_base()}{auth_c.ROUTE_PREDICTIONS_ANONYMOUS}", json=body)
    assert r.status_code == http_c.HTTP_201_CREATED
    data = r.json()[msg_c.KEY_DATA]
    assert data[msg_c.KEY_BMI] == compute_bmi(80.0, 1.8)
    assert data[msg_c.KEY_RISK_LEVEL] == pred_c.RISK_LEVEL_LOW
    assert msg_c.KEY_SHAP_EXPLANATION in data
    assert isinstance(data[msg_c.KEY_SHAP_EXPLANATION], dict)
    assert msg_c.KEY_SHAP_FEATURE_NAME in data[msg_c.KEY_SHAP_EXPLANATION]


def test_authenticated_prediction_response_shape(
    client: TestClient,
    registered_user: dict,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "app.services.prediction_service.predict_heart_risk",
        make_predict_stub(72.0),
    )
    r = client.post(
        _pred_base(),
        json=authenticated_prediction_body(),
        headers=auth_headers(registered_user["token"]),
    )
    assert r.status_code == http_c.HTTP_201_CREATED
    data = r.json()[msg_c.KEY_DATA]
    assert data[msg_c.KEY_USER_ID] == registered_user["user_id"]
    assert data[msg_c.KEY_RISK_LEVEL] == pred_c.RISK_LEVEL_HIGH
    assert msg_c.KEY_SHAP_EXPLANATION in data
    assert msg_c.KEY_SHAP_TOP_FACTORS in data


def test_history_detail_pdf_simulate_no_extra_row(
    client: TestClient,
    db_session: Session,
    registered_user: dict,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "app.services.prediction_service.predict_heart_risk",
        make_predict_stub(40.0),
    )
    create = client.post(
        _pred_base(),
        json=authenticated_prediction_body(),
        headers=auth_headers(registered_user["token"]),
    )
    assert create.status_code == http_c.HTTP_201_CREATED
    pid = create.json()[msg_c.KEY_DATA][msg_c.KEY_PREDICTION_ID]

    hist = client.get(
        f"{_pred_base()}{auth_c.ROUTE_PREDICTIONS_HISTORY}",
        headers=auth_headers(registered_user["token"]),
    )
    assert hist.status_code == http_c.HTTP_200_OK
    hdata = hist.json()[msg_c.KEY_DATA]
    assert len(hdata[msg_c.KEY_PREDICTIONS]) >= 1
    assert hdata[msg_c.KEY_PAGINATION][msg_c.KEY_TOTAL] >= 1

    detail = client.get(
        f"{_pred_base()}/{pid}",
        headers=auth_headers(registered_user["token"]),
    )
    assert detail.status_code == http_c.HTTP_200_OK
    assert detail.json()[msg_c.KEY_DATA][msg_c.KEY_PREDICTION_ID] == pid

    n_before = prediction_count(db_session)
    sim = client.post(
        f"{_pred_base()}/{pid}/simulate",
        headers=auth_headers(registered_user["token"]),
        json={"sleep_hours": 7.0},
    )
    assert sim.status_code == http_c.HTTP_200_OK
    sdata = sim.json()[msg_c.KEY_DATA]
    assert msg_c.KEY_SIMULATED_PROBABILITY in sdata
    assert msg_c.KEY_CHANGED_FIELDS in sdata
    assert prediction_count(db_session) == n_before

    pdf = client.get(
        f"{_pred_base()}/{pid}/export/pdf",
        headers=auth_headers(registered_user["token"]),
    )
    assert pdf.status_code == http_c.HTTP_200_OK
    assert pdf.headers.get("content-type") == pdf_c.PDF_MEDIA_TYPE
    assert pdf.content[:4] == b"%PDF"


def test_simulate_rejects_non_modifiable_field(client: TestClient, registered_user: dict) -> None:
    create = client.post(
        _pred_base(),
        json=authenticated_prediction_body(),
        headers=auth_headers(registered_user["token"]),
    )
    pid = create.json()[msg_c.KEY_DATA][msg_c.KEY_PREDICTION_ID]
    r = client.post(
        f"{_pred_base()}/{pid}/simulate",
        headers=auth_headers(registered_user["token"]),
        json={"had_angina": True},
    )
    assert r.status_code == http_c.HTTP_400_BAD_REQUEST
    assert r.json()[msg_c.KEY_ERROR][msg_c.KEY_CODE] == msg_c.ERROR_CODE_INVALID_VARIABLE


def test_history_rejects_invalid_sort(client: TestClient, registered_user: dict) -> None:
    r = client.get(
        f"{_pred_base()}{auth_c.ROUTE_PREDICTIONS_HISTORY}?sort=not_a_field",
        headers=auth_headers(registered_user["token"]),
    )
    assert r.status_code == http_c.HTTP_400_BAD_REQUEST
