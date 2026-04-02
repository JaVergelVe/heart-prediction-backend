"""Risk labels, thresholds, and predictions table constraint metadata."""

from typing import Final

from app.constants import validation as v

RISK_LEVEL_LOW: Final[str] = "Low"
RISK_LEVEL_MEDIUM: Final[str] = "Medium"
RISK_LEVEL_HIGH: Final[str] = "High"

RISK_PROBABILITY_LOW_MAX_EXCLUSIVE: Final[int] = 30
RISK_PROBABILITY_HIGH_MIN_EXCLUSIVE: Final[int] = 70

PREDICTIONS_CHECK_NAME: Final[str] = "ck_predictions_user_or_session"
PREDICTIONS_CHECK_SQL: Final[str] = (
    f"({v.COL_USER_ID} IS NOT NULL AND {v.COL_SESSION_ID} IS NULL) OR "
    f"({v.COL_USER_ID} IS NULL AND {v.COL_SESSION_ID} IS NOT NULL)"
)

IX_PREDICTIONS_USER_ID: Final[str] = "ix_predictions_user_id"
IX_PREDICTIONS_PREDICTION_TIMESTAMP: Final[str] = "ix_predictions_prediction_timestamp"
IX_PREDICTIONS_SESSION_ID: Final[str] = "ix_predictions_session_id"
