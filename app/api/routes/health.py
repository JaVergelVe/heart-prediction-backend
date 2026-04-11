from datetime import datetime, timezone

from fastapi import APIRouter

from app.constants import health as health_c
from app.constants import messages as msg_c
from app.core.config import get_settings
from app.core.database import DatabaseHealthStatus, check_database
from app.ml.artifacts import load_ml_bundle

router = APIRouter(tags=[health_c.ROUTER_TAG_HEALTH])


@router.get(health_c.ROUTE_HEALTH)
def health() -> dict:
    """Liveness check with database state: not_configured, connection_failed, or healthy."""
    settings = get_settings()
    now = (
        datetime.now(timezone.utc)
        .isoformat()
        .replace(
            msg_c.ISO_DATETIME_UTC_OFFSET_LEGACY,
            msg_c.ISO_DATETIME_Z_SUFFIX,
        )
    )
    db_health = check_database()
    db_status = db_health.value

    try:
        load_ml_bundle()
        ml_status = health_c.STATUS_HEALTHY
    except Exception:
        ml_status = health_c.STATUS_NOT_CONFIGURED

    overall = (
        health_c.STATUS_HEALTHY
        if db_health is DatabaseHealthStatus.HEALTHY and ml_status == health_c.STATUS_HEALTHY
        else health_c.STATUS_UNHEALTHY
    )
    return {
        health_c.KEY_STATUS: overall,
        health_c.KEY_TIMESTAMP: now,
        health_c.KEY_VERSION: settings.api_version,
        health_c.KEY_SERVICES: {
            health_c.KEY_DATABASE: db_status,
            health_c.KEY_ML_MODEL: ml_status,
        },
    }
