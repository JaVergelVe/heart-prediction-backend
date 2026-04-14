"""Catalog and health endpoints (mostly stateless)."""

from fastapi.testclient import TestClient

from app.constants import auth as auth_c
from app.constants import catalog as cat_c
from app.constants import health as health_c
from app.constants import http as http_c
from app.constants import messages as msg_c


def test_catalog_field_and_modifiable(client: TestClient) -> None:
    base = f"{auth_c.API_V1_PREFIX}{auth_c.ROUTER_PREFIX_CATALOGS}"
    r = client.get(f"{base}/{msg_c.KEY_GENERAL_HEALTH}")
    assert r.status_code == http_c.HTTP_200_OK
    data = r.json()[msg_c.KEY_DATA]
    assert data[cat_c.KEY_FIELD] == msg_c.KEY_GENERAL_HEALTH
    assert cat_c.KEY_ALLOWED_VALUES in data

    m = client.get(f"{base}{auth_c.ROUTE_CATALOGS_MODIFIABLE_VARIABLES}")
    assert m.status_code == http_c.HTTP_200_OK
    payload = m.json()[msg_c.KEY_DATA]
    assert cat_c.KEY_MODIFIABLE_VARIABLES in payload
    assert cat_c.KEY_FIXED_VARIABLES in payload
    assert len(payload[cat_c.KEY_MODIFIABLE_VARIABLES]) >= 1


def test_catalog_unknown_field_404(client: TestClient) -> None:
    base = f"{auth_c.API_V1_PREFIX}{auth_c.ROUTER_PREFIX_CATALOGS}"
    r = client.get(f"{base}/not_a_real_catalog_field_xyz")
    assert r.status_code == http_c.HTTP_404_NOT_FOUND
    assert r.json()[msg_c.KEY_ERROR][msg_c.KEY_CODE] == msg_c.ERROR_CODE_CATALOG_FIELD_NOT_SUPPORTED


def test_cors_preflight_allows_configured_dev_origin(client: TestClient) -> None:
    r = client.options(
        f"{auth_c.API_V1_PREFIX}{health_c.ROUTE_HEALTH}",
        headers={
            "Origin": "http://localhost:4200",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert r.status_code == http_c.HTTP_200_OK
    assert r.headers.get("access-control-allow-origin") == "http://localhost:4200"


def test_health_reports_database(client: TestClient) -> None:
    r = client.get(f"{auth_c.API_V1_PREFIX}{health_c.ROUTE_HEALTH}")
    assert r.status_code == http_c.HTTP_200_OK
    body = r.json()
    assert health_c.KEY_STATUS in body
    assert body[health_c.KEY_STATUS] in (health_c.STATUS_HEALTHY, health_c.STATUS_UNHEALTHY)
    assert body[health_c.KEY_SERVICES][health_c.KEY_DATABASE] in (
        health_c.STATUS_HEALTHY,
        health_c.STATUS_NOT_CONFIGURED,
        health_c.STATUS_CONNECTION_FAILED,
    )
    assert body[health_c.KEY_SERVICES][health_c.KEY_ML_MODEL] == health_c.STATUS_NOT_CONFIGURED
