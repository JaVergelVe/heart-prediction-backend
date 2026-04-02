from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.constants import DEFAULT_ACCESS_TOKEN_EXPIRE_SECONDS

# Resolve .env from the backend project root (directory that contains `app/`), not from CWD.
_BACKEND_ROOT = Path(__file__).resolve().parents[2]
_ENV_FILE = _BACKEND_ROOT / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Heart Attack Prediction API"
    debug: bool = False
    api_version: str = "1.0.0"
    database_url: str | None = None
    jwt_secret_key: str = "dev-only-change-with-JWT_SECRET_KEY"
    jwt_algorithm: str = "HS256"
    access_token_expire_seconds: int = DEFAULT_ACCESS_TOKEN_EXPIRE_SECONDS


@lru_cache
def get_settings() -> Settings:
    return Settings()
