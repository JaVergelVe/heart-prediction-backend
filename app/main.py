from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api.routes import auth, health, users
from app.constants import auth as auth_c
from app.core.config import get_settings
from app.core.exceptions import APIError, api_error_handler, validation_error_handler

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.api_version,
    debug=settings.debug,
)

app.add_exception_handler(APIError, api_error_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)

app.include_router(health.router, prefix=auth_c.API_V1_PREFIX)
app.include_router(auth.router, prefix=auth_c.API_V1_PREFIX)
app.include_router(users.router, prefix=auth_c.API_V1_PREFIX)
