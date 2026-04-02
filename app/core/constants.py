"""Centralized literals for health, auth, errors, and shared business rules."""

from typing import Final

# --- Health endpoint & database connectivity (API + DatabaseHealthStatus) ---
STATUS_HEALTHY: Final[str] = "healthy"
STATUS_UNHEALTHY: Final[str] = "unhealthy"
STATUS_NOT_CONFIGURED: Final[str] = "not_configured"
STATUS_CONNECTION_FAILED: Final[str] = "connection_failed"

# --- Auth (HTTP Bearer scheme + token payload / response) ---
AUTH_SCHEME_BEARER_LOWER: Final[str] = "bearer"
TOKEN_TYPE_BEARER: Final[str] = "Bearer"
DEFAULT_ACCESS_TOKEN_EXPIRE_SECONDS: Final[int] = 86400

# --- Risk levels & thresholds (API contracts / future predictions) ---
RISK_LEVEL_LOW: Final[str] = "Low"
RISK_LEVEL_MEDIUM: Final[str] = "Medium"
RISK_LEVEL_HIGH: Final[str] = "High"
# Probabilidad en %: Low si < 30; High si > 70; Medium entre 30 y 70 (inclusive).
RISK_PROBABILITY_LOW_MAX_EXCLUSIVE: Final[int] = 30
RISK_PROBABILITY_HIGH_MIN_EXCLUSIVE: Final[int] = 70

# --- API error codes ---
ERROR_CODE_VALIDATION: Final[str] = "VALIDATION_ERROR"
ERROR_CODE_INVALID_CREDENTIALS: Final[str] = "INVALID_CREDENTIALS"
ERROR_CODE_UNAUTHORIZED: Final[str] = "UNAUTHORIZED"
ERROR_CODE_INTERNAL: Final[str] = "INTERNAL_ERROR"

# --- Repeated API error / validation messages ---
MSG_VALIDATION_FAILED: Final[str] = "Error en validación de datos"
MSG_INVALID_CREDENTIALS: Final[str] = "Email o contraseña incorrectos"
MSG_TOKEN_INVALID_OR_EXPIRED: Final[str] = "Token inválido o expirado"
MSG_TOKEN_REQUIRED: Final[str] = "Token de acceso requerido"
MSG_VALIDATION_INVALID_INPUT: Final[str] = "Invalid input"

# --- Field-level validation (register / duplicate email) ---
FIELD_EMAIL: Final[str] = "email"
REASON_EMAIL_REGISTERED: Final[str] = "Email ya está registrado"

# --- Profile / medical defaults in responses ---
DEFAULT_HAD_DIABETES_DISPLAY: Final[str] = "No"
MSG_PROFILE_INCOMPLETE: Final[str] = "Perfil de usuario incompleto"

# --- Demographics (aligned with register schema; reuse for literals) ---
SEX_MALE: Final[str] = "Male"
SEX_FEMALE: Final[str] = "Female"
