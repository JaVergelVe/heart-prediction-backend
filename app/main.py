from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api.routes import auth, health, users
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

app.include_router(health.router, prefix="/v1")
app.include_router(auth.router, prefix="/v1")
app.include_router(users.router, prefix="/v1")
