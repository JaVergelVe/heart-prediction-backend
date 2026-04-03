"""Authentication, JWT, and auth route metadata."""

from typing import Final

# Bearer scheme / token type (API contract)
AUTH_SCHEME_BEARER_LOWER: Final[str] = "bearer"
TOKEN_TYPE_BEARER: Final[str] = "Bearer"

# JWT defaults (override via env / Settings)
JWT_ALGORITHM_DEFAULT: Final[str] = "HS256"
JWT_SECRET_KEY_DEV_PLACEHOLDER: Final[str] = "dev-only-change-with-JWT_SECRET_KEY"
ACCESS_TOKEN_EXPIRE_SECONDS_DEFAULT: Final[int] = 86400

# JWT registered claim names
JWT_CLAIM_SUB: Final[str] = "sub"
JWT_CLAIM_EXP: Final[str] = "exp"
JWT_CLAIM_IAT: Final[str] = "iat"

# API version prefix (routers)
API_V1_PREFIX: Final[str] = "/v1"

# Routers
ROUTER_PREFIX_AUTH: Final[str] = "/auth"
ROUTER_PREFIX_USERS: Final[str] = "/users"
ROUTER_PREFIX_PREDICTIONS: Final[str] = "/predictions"
ROUTER_TAG_AUTH: Final[str] = "auth"
ROUTER_TAG_USERS: Final[str] = "users"
ROUTER_TAG_PREDICTIONS: Final[str] = "predictions"

ROUTE_PREDICTIONS_ANONYMOUS: Final[str] = "/anonymous"

ROUTE_REGISTER: Final[str] = "/register"
ROUTE_LOGIN: Final[str] = "/login"
ROUTE_USERS_ME: Final[str] = "/me"
