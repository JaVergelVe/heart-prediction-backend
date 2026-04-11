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

from app.constants import prediction as pred_c
from app.constants import validation as v
from app.models.base import Base


def _new_uuid_str() -> str:
    return str(uuid.uuid4())


class Prediction(Base):
    __tablename__ = v.TABLE_PREDICTIONS
    __table_args__ = (
        CheckConstraint(
            pred_c.PREDICTIONS_CHECK_SQL,
            name=pred_c.PREDICTIONS_CHECK_NAME,
        ),
        Index(pred_c.IX_PREDICTIONS_USER_ID, v.COL_USER_ID),
        Index(
            pred_c.IX_PREDICTIONS_PREDICTION_TIMESTAMP,
            v.COL_PREDICTION_TIMESTAMP,
        ),
        Index(pred_c.IX_PREDICTIONS_SESSION_ID, v.COL_SESSION_ID),
    )

    id: Mapped[str] = mapped_column(
        String(v.DB_UUID_STR_LEN),
        primary_key=True,
        default=_new_uuid_str,
    )
    user_id: Mapped[str | None] = mapped_column(
        String(v.DB_UUID_STR_LEN),
        ForeignKey(v.FK_USERS_ID, ondelete=v.ON_DELETE_CASCADE),
        nullable=True,
    )
    session_id: Mapped[str | None] = mapped_column(
        String(v.DB_SESSION_ID_MAX_LEN),
        nullable=True,
    )

    weight_kilograms: Mapped[float | None] = mapped_column(
        Numeric(v.DB_WEIGHT_KG_PRECISION, v.DB_WEIGHT_KG_SCALE),
    )
    bmi: Mapped[float | None] = mapped_column(
        Numeric(v.DB_BMI_PRECISION, v.DB_BMI_SCALE),
    )
    general_health: Mapped[str | None] = mapped_column(String(v.DB_GENERAL_HEALTH_MAX_LEN))
    physical_health_days: Mapped[int | None] = mapped_column(Integer)
    mental_health_days: Mapped[int | None] = mapped_column(Integer)
    last_checkup_time: Mapped[str | None] = mapped_column(String(v.DB_LAST_CHECKUP_MAX_LEN))
    physical_activities: Mapped[bool | None] = mapped_column(Boolean)
    sleep_hours: Mapped[float | None] = mapped_column(
        Numeric(v.DB_SLEEP_HOURS_PRECISION, v.DB_SLEEP_HOURS_SCALE),
    )
    smoker_status: Mapped[str | None] = mapped_column(String(v.DB_SMOKER_STATUS_MAX_LEN))
    ecigarette_usage: Mapped[str | None] = mapped_column(String(v.DB_ECIGARETTE_MAX_LEN))
    alcohol_drinkers: Mapped[bool | None] = mapped_column(Boolean)
    chest_scan: Mapped[bool | None] = mapped_column(Boolean)
    hiv_testing: Mapped[bool | None] = mapped_column(Boolean)
    flu_vax_last_12: Mapped[bool | None] = mapped_column(Boolean)
    pneumo_vax_ever: Mapped[bool | None] = mapped_column(Boolean)
    tetanus_last_10_tdap: Mapped[str | None] = mapped_column(String(v.DB_TETANUS_MAX_LEN))
    high_risk_last_year: Mapped[bool | None] = mapped_column(Boolean)
    covid_pos: Mapped[str | None] = mapped_column(String(v.DB_COVID_POS_MAX_LEN))

    prediction_probability: Mapped[float | None] = mapped_column(
        Numeric(v.DB_PREDICTION_PROB_PRECISION, v.DB_PREDICTION_PROB_SCALE),
    )
    risk_level: Mapped[str | None] = mapped_column(String(v.DB_RISK_LEVEL_MAX_LEN))
    model_version: Mapped[str | None] = mapped_column(String(v.DB_MODEL_VERSION_MAX_LEN))
    prediction_timestamp: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )
