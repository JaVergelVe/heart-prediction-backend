import logging
from collections.abc import Generator
from enum import Enum

from fastapi import HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from app.constants import health as health_c
from app.constants import http as http_c
from app.constants import messages as msg_c
from app.core.config import get_settings

logger = logging.getLogger(__name__)

# Health responses use only DatabaseHealthStatus values — never raw exceptions or connection strings.


class DatabaseHealthStatus(str, Enum):
    """Reportable database states (safe for clients; no credentials or exception text)."""

    NOT_CONFIGURED = health_c.STATUS_NOT_CONFIGURED
    CONNECTION_FAILED = health_c.STATUS_CONNECTION_FAILED
    HEALTHY = health_c.STATUS_HEALTHY


_settings = get_settings()

if _settings.database_url:
    engine = create_engine(_settings.database_url, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
    engine = None
    SessionLocal = None


def check_database() -> DatabaseHealthStatus:
    """Run SELECT 1; classify missing URL vs connection errors vs success."""
    if engine is None:
        return DatabaseHealthStatus.NOT_CONFIGURED
    try:
        with engine.connect() as conn:
            conn.execute(text(health_c.SQL_HEALTH_CHECK))
        return DatabaseHealthStatus.HEALTHY
    except Exception as exc:
        # Log exception class only — avoids leaking host, user, or message details to logs/API.
        logger.warning(
            msg_c.LOG_DB_HEALTH_CHECK_FAIL,
            type(exc).__name__,
            exc_info=False,
        )
        return DatabaseHealthStatus.CONNECTION_FAILED


def get_db() -> Generator[Session, None, None]:
    if SessionLocal is None:
        raise HTTPException(
            status_code=http_c.HTTP_503_SERVICE_UNAVAILABLE,
            detail=msg_c.HTTP_DETAIL_DATABASE_NOT_CONFIGURED,
        )
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
