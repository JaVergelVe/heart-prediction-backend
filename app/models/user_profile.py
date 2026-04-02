"""Demographic profile row (table `user_profiles`)."""

from datetime import date
import uuid

from sqlalchemy import Date, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


def _new_uuid_str() -> str:
    return str(uuid.uuid4())


class UserProfile(Base, TimestampMixin):
    __tablename__ = "user_profiles"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=_new_uuid_str,
    )
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    sex: Mapped[str | None] = mapped_column(String(10))
    birth_date: Mapped[date | None] = mapped_column(Date)
    age_category: Mapped[str | None] = mapped_column(String(64))
    height_meters: Mapped[float | None] = mapped_column(Numeric(4, 2))
    removed_teeth: Mapped[str | None] = mapped_column(String(64))
