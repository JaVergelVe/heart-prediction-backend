from datetime import datetime, timezone

from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    """Liveness check. DB/ML status will be wired in later phases."""
    settings = get_settings()
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return {
        "status": "healthy",
        "timestamp": now,
        "version": settings.api_version,
        "services": {
            "database": "not_configured",
            "ml_model": "not_configured",
        },
    }
