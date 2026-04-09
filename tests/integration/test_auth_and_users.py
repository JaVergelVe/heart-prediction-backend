"""Auth and authenticated user profile endpoints."""

from fastapi.testclient import TestClient

from app.constants import auth as auth_c
from app.constants import http as http_c
from app.constants import messages as msg_c
from tests.conftest import auth_headers, register_body


def _url(*parts: str) -> str:
    return f"{auth_c.API_V1_PREFIX}{''.join(parts)}"


def test_register_login_me_profile_medical(
    client: TestClient,
    registered_user: dict,
) -> None:
    login = client.post(
        _url(auth_c.ROUTER_PREFIX_AUTH, auth_c.ROUTE_LOGIN),
        json={"email": registered_user["email"], "password": registered_user["password"]},
    )
    assert login.status_code == http_c.HTTP_200_OK
    token = login.json()[msg_c.KEY_DATA][msg_c.KEY_ACCESS_TOKEN]

    me = client.get(
        _url(auth_c.ROUTER_PREFIX_USERS, auth_c.ROUTE_USERS_ME),
        headers=auth_headers(token),
    )
    assert me.status_code == http_c.HTTP_200_OK
    body = me.json()[msg_c.KEY_DATA]
    assert body[msg_c.KEY_USER_ID] == registered_user["user_id"]
    assert body[msg_c.KEY_EMAIL] == registered_user["email"]
    assert msg_c.KEY_PROFILE in body
    assert msg_c.KEY_MEDICAL_CONDITIONS in body

    prof = client.put(
        _url(auth_c.ROUTER_PREFIX_USERS, auth_c.ROUTE_USERS_ME_PROFILE),
        headers=auth_headers(token),
        json={"height_meters": 1.82},
    )
    assert prof.status_code == http_c.HTTP_200_OK
    assert prof.json()[msg_c.KEY_DATA][msg_c.KEY_PROFILE][msg_c.KEY_HEIGHT_METERS] == 1.82

    med = client.put(
        _url(auth_c.ROUTER_PREFIX_USERS, auth_c.ROUTE_USERS_ME_MEDICAL_CONDITIONS),
        headers=auth_headers(token),
        json={"had_asthma": True},
    )
    assert med.status_code == http_c.HTTP_200_OK
    assert med.json()[msg_c.KEY_DATA][msg_c.KEY_MEDICAL_CONDITIONS]["had_asthma"] is True


def test_register_duplicate_email_400(client: TestClient) -> None:
    payload = register_body()
    assert client.post(
        _url(auth_c.ROUTER_PREFIX_AUTH, auth_c.ROUTE_REGISTER),
        json=payload,
    ).status_code == http_c.HTTP_201_CREATED
    dup = client.post(
        _url(auth_c.ROUTER_PREFIX_AUTH, auth_c.ROUTE_REGISTER),
        json=payload,
    )
    assert dup.status_code == http_c.HTTP_400_BAD_REQUEST
    err = dup.json()[msg_c.KEY_ERROR]
    assert err[msg_c.KEY_CODE] == msg_c.ERROR_CODE_VALIDATION


def test_login_invalid_credentials_401(client: TestClient, registered_user: dict) -> None:
    r = client.post(
        _url(auth_c.ROUTER_PREFIX_AUTH, auth_c.ROUTE_LOGIN),
        json={"email": registered_user["email"], "password": "wrong-password1"},
    )
    assert r.status_code == http_c.HTTP_401_UNAUTHORIZED
    assert r.json()[msg_c.KEY_ERROR][msg_c.KEY_CODE] == msg_c.ERROR_CODE_INVALID_CREDENTIALS
