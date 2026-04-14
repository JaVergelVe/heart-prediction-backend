from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.constants import auth as auth_c
from app.constants import validation as val_c

# Resolve .env from the backend project root (directory that contains `app/`), not from CWD.
_BACKEND_ROOT = Path(__file__).resolve().parents[2]
_ENV_FILE = _BACKEND_ROOT / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = val_c.APP_NAME_DEFAULT
    debug: bool = val_c.DEBUG_DEFAULT
    api_version: str = val_c.API_VERSION_DEFAULT
    database_url: str | None = None
    ml_models_dir: str | None = None
    jwt_secret_key: str = auth_c.JWT_SECRET_KEY_DEV_PLACEHOLDER
    jwt_algorithm: str = auth_c.JWT_ALGORITHM_DEFAULT
    access_token_expire_seconds: int = auth_c.ACCESS_TOKEN_EXPIRE_SECONDS_DEFAULT
    cors_origins: str = val_c.CORS_ORIGINS_DEFAULT

    def cors_allowed_origins(self) -> list[str]:
        return [part.strip() for part in self.cors_origins.split(",") if part.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
