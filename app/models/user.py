"""User authentication row (table `users`)."""

from datetime import datetime
import uuid

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.constants import validation as v
from app.models.base import Base, TimestampMixin


def _new_uuid_str() -> str:
    return str(uuid.uuid4())


class User(Base, TimestampMixin):
    __tablename__ = v.TABLE_USERS

    id: Mapped[str] = mapped_column(
        String(v.DB_UUID_STR_LEN),
        primary_key=True,
        default=_new_uuid_str,
    )
    email: Mapped[str] = mapped_column(String(v.DB_EMAIL_MAX_LEN), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(
        String(v.DB_PASSWORD_HASH_MAX_LEN),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=v.DEFAULT_USER_IS_ACTIVE,
    )
    last_login: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
