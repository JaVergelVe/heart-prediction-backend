from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, catalogs, health, predictions, users
from app.constants import auth as auth_c
from app.constants import validation as val_c
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins(),
    allow_credentials=True,
    allow_methods=list(val_c.CORS_ALLOW_METHODS),
    allow_headers=list(val_c.CORS_ALLOW_HEADERS),
    expose_headers=list(val_c.CORS_EXPOSE_HEADERS),
)

app.include_router(health.router, prefix=auth_c.API_V1_PREFIX)
app.include_router(auth.router, prefix=auth_c.API_V1_PREFIX)
app.include_router(users.router, prefix=auth_c.API_V1_PREFIX)
app.include_router(predictions.router, prefix=auth_c.API_V1_PREFIX)
app.include_router(catalogs.router, prefix=auth_c.API_V1_PREFIX)
