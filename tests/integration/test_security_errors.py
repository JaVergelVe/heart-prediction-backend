"""Validation envelope, auth failures, and cross-user isolation (404)."""

import uuid

from fastapi.testclient import TestClient

from app.constants import auth as auth_c
from app.constants import http as http_c
from app.constants import messages as msg_c
from tests.conftest import auth_headers, register_body


def test_missing_token_401(client: TestClient) -> None:
    r = client.get(f"{auth_c.API_V1_PREFIX}{auth_c.ROUTER_PREFIX_USERS}{auth_c.ROUTE_USERS_ME}")
    assert r.status_code == http_c.HTTP_401_UNAUTHORIZED
    err = r.json()[msg_c.KEY_ERROR]
    assert err[msg_c.KEY_CODE] == msg_c.ERROR_CODE_UNAUTHORIZED


def test_invalid_token_401(client: TestClient) -> None:
    r = client.get(
        f"{auth_c.API_V1_PREFIX}{auth_c.ROUTER_PREFIX_USERS}{auth_c.ROUTE_USERS_ME}",
        headers=auth_headers("not-a-valid-jwt"),
    )
    assert r.status_code == http_c.HTTP_401_UNAUTHORIZED


def test_profile_update_empty_body_validation(client: TestClient, registered_user: dict) -> None:
    r = client.put(
        f"{auth_c.API_V1_PREFIX}{auth_c.ROUTER_PREFIX_USERS}{auth_c.ROUTE_USERS_ME_PROFILE}",
        headers=auth_headers(registered_user["token"]),
        json={},
    )
    assert r.status_code == http_c.HTTP_400_BAD_REQUEST
    assert r.json()[msg_c.KEY_ERROR][msg_c.KEY_CODE] == msg_c.ERROR_CODE_VALIDATION


def test_validation_envelope_bad_email(client: TestClient) -> None:
    payload = register_body()
    payload["email"] = "not-an-email"
    r = client.post(
        f"{auth_c.API_V1_PREFIX}{auth_c.ROUTER_PREFIX_AUTH}{auth_c.ROUTE_REGISTER}",
        json=payload,
    )
    assert r.status_code == http_c.HTTP_400_BAD_REQUEST
    err = r.json()[msg_c.KEY_ERROR]
    assert err[msg_c.KEY_CODE] == msg_c.ERROR_CODE_VALIDATION


def test_prediction_not_found_404(client: TestClient, registered_user: dict) -> None:
    pid = str(uuid.uuid4())
    r = client.get(
        f"{auth_c.API_V1_PREFIX}{auth_c.ROUTER_PREFIX_PREDICTIONS}/{pid}",
        headers=auth_headers(registered_user["token"]),
    )
    assert r.status_code == http_c.HTTP_404_NOT_FOUND
    assert r.json()[msg_c.KEY_ERROR][msg_c.KEY_CODE] == msg_c.ERROR_CODE_PREDICTION_NOT_FOUND


def test_user_cannot_read_other_users_prediction(
    client: TestClient,
    registered_user: dict,
    second_registered_user: dict,
) -> None:
    pred_base = f"{auth_c.API_V1_PREFIX}{auth_c.ROUTER_PREFIX_PREDICTIONS}"
    create = client.post(
        pred_base,
        json={"weight_kilograms": 70.0},
        headers=auth_headers(second_registered_user["token"]),
    )
    assert create.status_code == http_c.HTTP_201_CREATED
    pid = create.json()[msg_c.KEY_DATA][msg_c.KEY_PREDICTION_ID]

    stolen = client.get(
        f"{pred_base}/{pid}",
        headers=auth_headers(registered_user["token"]),
    )
    assert stolen.status_code == http_c.HTTP_404_NOT_FOUND
