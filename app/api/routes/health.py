from datetime import datetime, timezone

from fastapi import APIRouter

from app.core.config import get_settings
from app.core.database import DatabaseHealthStatus, check_database

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    """Liveness check with database state: not_configured, connection_failed, or healthy."""
    settings = get_settings()
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    db_health = check_database()
    db_status = db_health.value
    overall = (
        "healthy"
        if db_health is DatabaseHealthStatus.HEALTHY
        else "unhealthy"
    )
    return {
        "status": overall,
        "timestamp": now,
        "version": settings.api_version,
        "services": {
            "database": db_status,
            "ml_model": "not_configured",
        },
    }
