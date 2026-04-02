"""Demographic profile row (table `user_profiles`)."""

from datetime import date
import uuid

from sqlalchemy import Date, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.constants import validation as v
from app.models.base import Base, TimestampMixin


def _new_uuid_str() -> str:
    return str(uuid.uuid4())


class UserProfile(Base, TimestampMixin):
    __tablename__ = v.TABLE_USER_PROFILES

    id: Mapped[str] = mapped_column(
        String(v.DB_UUID_STR_LEN),
        primary_key=True,
        default=_new_uuid_str,
    )
    user_id: Mapped[str] = mapped_column(
        String(v.DB_UUID_STR_LEN),
        ForeignKey(v.FK_USERS_ID, ondelete=v.ON_DELETE_CASCADE),
        unique=True,
        nullable=False,
    )
    sex: Mapped[str | None] = mapped_column(String(v.DB_SEX_MAX_LEN))
    birth_date: Mapped[date | None] = mapped_column(Date)
    age_category: Mapped[str | None] = mapped_column(String(v.DB_AGE_CATEGORY_MAX_LEN))
    height_meters: Mapped[float | None] = mapped_column(
        Numeric(v.DB_HEIGHT_METERS_PRECISION, v.DB_HEIGHT_METERS_SCALE),
    )
    removed_teeth: Mapped[str | None] = mapped_column(String(v.DB_REMOVED_TEETH_MAX_LEN))
