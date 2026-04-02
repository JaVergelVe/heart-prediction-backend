"""Chronic medical conditions row (table `medical_conditions`)."""

import uuid

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


def _new_uuid_str() -> str:
    return str(uuid.uuid4())


class MedicalConditions(Base, TimestampMixin):
    __tablename__ = "medical_conditions"

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
    had_angina: Mapped[bool | None] = mapped_column(Boolean)
    had_stroke: Mapped[bool | None] = mapped_column(Boolean)
    had_asthma: Mapped[bool | None] = mapped_column(Boolean)
    had_copd: Mapped[bool | None] = mapped_column(Boolean)
    had_skin_cancer: Mapped[bool | None] = mapped_column(Boolean)
    had_depressive_disorder: Mapped[bool | None] = mapped_column(Boolean)
    had_kidney_disease: Mapped[bool | None] = mapped_column(Boolean)
    had_arthritis: Mapped[bool | None] = mapped_column(Boolean)
    had_diabetes: Mapped[str | None] = mapped_column(String(100))
    deaf_or_hard_of_hearing: Mapped[bool | None] = mapped_column(Boolean)
    blind_or_vision_difficulty: Mapped[bool | None] = mapped_column(Boolean)
    difficulty_concentrating: Mapped[bool | None] = mapped_column(Boolean)
    difficulty_walking: Mapped[bool | None] = mapped_column(Boolean)
    difficulty_dressing_bathing: Mapped[bool | None] = mapped_column(Boolean)
    difficulty_errands: Mapped[bool | None] = mapped_column(Boolean)
