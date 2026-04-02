"""Prediction request/snapshot and model outputs (table `predictions`)."""

from datetime import datetime
import uuid

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


def _new_uuid_str() -> str:
    return str(uuid.uuid4())


class Prediction(Base):
    __tablename__ = "predictions"
    __table_args__ = (
        CheckConstraint(
            "(user_id IS NOT NULL AND session_id IS NULL) OR "
            "(user_id IS NULL AND session_id IS NOT NULL)",
            name="ck_predictions_user_or_session",
        ),
        Index("ix_predictions_user_id", "user_id"),
        Index("ix_predictions_prediction_timestamp", "prediction_timestamp"),
        Index("ix_predictions_session_id", "session_id"),
    )

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=_new_uuid_str,
    )
    user_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
    )
    session_id: Mapped[str | None] = mapped_column(String(64), nullable=True)

    weight_kilograms: Mapped[float | None] = mapped_column(Numeric(5, 2))
    bmi: Mapped[float | None] = mapped_column(Numeric(5, 2))
    general_health: Mapped[str | None] = mapped_column(String(20))
    physical_health_days: Mapped[int | None] = mapped_column(Integer)
    mental_health_days: Mapped[int | None] = mapped_column(Integer)
    last_checkup_time: Mapped[str | None] = mapped_column(String(100))
    physical_activities: Mapped[bool | None] = mapped_column(Boolean)
    sleep_hours: Mapped[float | None] = mapped_column(Numeric(3, 1))
    smoker_status: Mapped[str | None] = mapped_column(String(80))
    ecigarette_usage: Mapped[str | None] = mapped_column(String(100))
    alcohol_drinkers: Mapped[bool | None] = mapped_column(Boolean)
    chest_scan: Mapped[bool | None] = mapped_column(Boolean)
    hiv_testing: Mapped[bool | None] = mapped_column(Boolean)
    flu_vax_last_12: Mapped[bool | None] = mapped_column(Boolean)
    pneumo_vax_ever: Mapped[bool | None] = mapped_column(Boolean)
    tetanus_last_10_tdap: Mapped[str | None] = mapped_column(String(100))
    high_risk_last_year: Mapped[bool | None] = mapped_column(Boolean)
    covid_pos: Mapped[str | None] = mapped_column(String(100))

    prediction_probability: Mapped[float | None] = mapped_column(Numeric(5, 2))
    risk_level: Mapped[str | None] = mapped_column(String(10))
    model_version: Mapped[str | None] = mapped_column(String(50))
    prediction_timestamp: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )
