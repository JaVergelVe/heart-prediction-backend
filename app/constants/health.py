"""Health check responses and DB ping."""

from typing import Final

# Overall / service status values (also used by DatabaseHealthStatus enum values)
STATUS_HEALTHY: Final[str] = "healthy"
STATUS_UNHEALTHY: Final[str] = "unhealthy"
STATUS_NOT_CONFIGURED: Final[str] = "not_configured"
STATUS_CONNECTION_FAILED: Final[str] = "connection_failed"

# JSON keys — GET /v1/health
KEY_STATUS: Final[str] = "status"
KEY_TIMESTAMP: Final[str] = "timestamp"
KEY_VERSION: Final[str] = "version"
KEY_SERVICES: Final[str] = "services"
KEY_DATABASE: Final[str] = "database"
KEY_ML_MODEL: Final[str] = "ml_model"

# Router
ROUTER_TAG_HEALTH: Final[str] = "health"
ROUTE_HEALTH: Final[str] = "/health"

# SQL executed for connectivity check
SQL_HEALTH_CHECK: Final[str] = "SELECT 1"
