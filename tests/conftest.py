"""Test configuration: environment must be set before importing `app`."""

from __future__ import annotations

import os
import uuid
from typing import Any

# Force SQLite and a stable JWT secret so tests do not depend on local .env / RDS.
os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
os.environ["JWT_SECRET_KEY"] = "pytest-jwt-secret-key-at-least-32-bytes-long!"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from app.constants import arrays as arr_c
from app.constants import auth as auth_c
from app.constants import messages as msg_c
from app.constants import ml_inference as ml_c
from app.core.database import SessionLocal, engine, get_db
from app.main import app
from app.models import MedicalConditions, Prediction, User, UserProfile
from app.models.base import Base


Base.metadata.create_all(bind=engine)


def make_predict_stub(probability: float):
    def stub(_features: dict[str, Any]) -> dict[str, Any]:
        return {
            msg_c.KEY_PREDICTION_PROBABILITY: probability,
            msg_c.KEY_PREDICTED_CLASS: "0",
            msg_c.KEY_MODEL_VERSION: ml_c.ML_MODEL_VERSION,
            msg_c.KEY_SHAP_EXPLANATION: {
                msg_c.KEY_SHAP_FEATURE_NAME: "BMI",
                msg_c.KEY_SHAP_IMPACT_SCORE: 0.5,
                msg_c.KEY_SHAP_DIRECTION: ml_c.SHAP_DIRECTION_INCREASES_RISK,
                msg_c.KEY_SHAP_MESSAGE: "test",
            },
            msg_c.KEY_SHAP_TOP_FACTORS: [],
        }

    return stub


@pytest.fixture(autouse=True)
def _stub_predict_heart_risk(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "app.services.prediction_service.predict_heart_risk",
        make_predict_stub(45.0),
    )


def _wipe_db(session: Session) -> None:
    session.execute(delete(Prediction))
    session.execute(delete(UserProfile))
    session.execute(delete(MedicalConditions))
    session.execute(delete(User))
    session.commit()


@pytest.fixture
def db_session() -> Session:
    s = SessionLocal()
    yield s
    _wipe_db(s)
    s.close()


@pytest.fixture
def client(db_session: Session) -> TestClient:
    def override_db() -> Any:
        yield db_session

    app.dependency_overrides[get_db] = override_db
    with TestClient(app) as tc:
        yield tc
    app.dependency_overrides.clear()


def register_body(*, email: str | None = None, password: str = "testpass1") -> dict[str, Any]:
    em = email or f"u_{uuid.uuid4().hex[:12]}@example.com"
    return {
        "email": em,
        "password": password,
        "profile": {
            "sex": arr_c.SEX_MALE,
            "birth_date": "1990-06-15",
            "height_meters": 1.8,
            "removed_teeth": arr_c.REMOVED_TEETH_NONE_OF_THEM,
        },
        "medical_conditions": {
            "had_angina": False,
            "had_stroke": False,
            "had_asthma": False,
            "had_copd": False,
            "had_skin_cancer": False,
            "had_depressive_disorder": False,
            "had_kidney_disease": False,
            "had_arthritis": False,
            "had_diabetes": arr_c.HAD_DIABETES_NO,
            "deaf_or_hard_of_hearing": False,
            "blind_or_vision_difficulty": False,
            "difficulty_concentrating": False,
            "difficulty_walking": False,
            "difficulty_dressing_bathing": False,
            "difficulty_errands": False,
        },
    }


def anonymous_prediction_body(*, session_id: str | None = None) -> dict[str, Any]:
    sid = session_id or f"sess-{uuid.uuid4().hex[:16]}"
    base = register_body()
    return {
        "session_id": sid,
        "profile": base["profile"],
        "medical_conditions": base["medical_conditions"],
        "weight_kilograms": 80.0,
    }


def authenticated_prediction_body() -> dict[str, Any]:
    return {"weight_kilograms": 75.0}


def auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def registered_user(client: TestClient) -> dict[str, Any]:
    payload = register_body()
    r = client.post(
        f"{auth_c.API_V1_PREFIX}{auth_c.ROUTER_PREFIX_AUTH}{auth_c.ROUTE_REGISTER}",
        json=payload,
    )
    assert r.status_code == 201, r.text
    data = r.json()[msg_c.KEY_DATA]
    return {
        "email": payload["email"],
        "password": payload["password"],
        "user_id": data[msg_c.KEY_USER_ID],
        "token": data[msg_c.KEY_ACCESS_TOKEN],
    }


@pytest.fixture
def second_registered_user(client: TestClient) -> dict[str, Any]:
    payload = register_body()
    r = client.post(
        f"{auth_c.API_V1_PREFIX}{auth_c.ROUTER_PREFIX_AUTH}{auth_c.ROUTE_REGISTER}",
        json=payload,
    )
    assert r.status_code == 201, r.text
    data = r.json()[msg_c.KEY_DATA]
    return {
        "email": payload["email"],
        "password": payload["password"],
        "user_id": data[msg_c.KEY_USER_ID],
        "token": data[msg_c.KEY_ACCESS_TOKEN],
    }


def prediction_count(session: Session) -> int:
    return int(session.scalar(select(func.count()).select_from(Prediction)) or 0)
