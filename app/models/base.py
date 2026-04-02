"""Declarative base and shared mixins for ORM models (MySQL-compatible)."""

from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.constants import validation as v


class Base(DeclarativeBase):
    """SQLAlchemy declarative base for all application models."""


class TimestampMixin:
    """created_at / updated_at columns aligned with project DB schema."""

    created_at: Mapped[datetime] = mapped_column(
        v.COL_CREATED_AT,
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        v.COL_UPDATED_AT,
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
