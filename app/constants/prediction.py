"""Risk labels, thresholds, and predictions table constraint metadata."""

from typing import Any, Final

from app.constants import messages as msg_c
from app.constants import prediction_survey as ps
from app.constants import validation as v

RISK_LEVEL_LOW: Final[str] = "Low"
RISK_LEVEL_MEDIUM: Final[str] = "Medium"
RISK_LEVEL_HIGH: Final[str] = "High"

RISK_PROBABILITY_LOW_MAX_EXCLUSIVE: Final[int] = 30
RISK_PROBABILITY_HIGH_MIN_EXCLUSIVE: Final[int] = 70

MOCK_MODEL_VERSION: Final[str] = "mock-1.0.0"

# Mock predictor: hash(features) → [0, MOCK_PREDICTOR_PROBABILITY_MODULO - 1]
MOCK_PREDICTOR_HEX_PREFIX_LEN: Final[int] = 8
MOCK_PREDICTOR_PROBABILITY_MODULO: Final[int] = 101
MOCK_PREDICTOR_PAYLOAD_ENCODING: Final[str] = "utf-8"

# MySQL `chk_bmi`
DB_BMI_CHECK_MIN: Final[int] = 10
DB_BMI_CHECK_MAX: Final[int] = 100

# When optional survey fields are omitted: NOT NULL + CHECK-compliant defaults (see `prediction_survey`).
PERSIST_DEFAULT_GENERAL_HEALTH: Final[str] = ps.GeneralHealth.GOOD.value
PERSIST_DEFAULT_LAST_CHECKUP_TIME: Final[str] = ps.LastCheckupTime.NEVER.value
PERSIST_DEFAULT_ECIGARETTE_USAGE: Final[str] = ps.EcigaretteUsage.NEVER_USED_LIFE.value
PERSIST_DEFAULT_SMOKER_STATUS: Final[str] = ps.SmokerStatus.NEVER_SMOKED.value
PERSIST_DEFAULT_COVID_POS: Final[str] = ps.CovidPos.NO.value
PERSIST_DEFAULT_TETANUS_LAST_10_TDAP: Final[str] = ps.TetanusLast10Tdap.NO_NOT_IN_10_YEARS.value
PERSIST_DEFAULT_BOOL: Final[bool] = False
PERSIST_DEFAULT_HEALTH_DAYS: Final[int] = 0
PERSIST_DEFAULT_SLEEP_HOURS: Final[float] = 0.0

# Order: key → default when value is missing or None (persist + ML coercion).
SURVEY_DB_DEFAULTS: Final[tuple[tuple[str, Any], ...]] = (
    (msg_c.KEY_GENERAL_HEALTH, PERSIST_DEFAULT_GENERAL_HEALTH),
    (msg_c.KEY_PHYSICAL_HEALTH_DAYS, PERSIST_DEFAULT_HEALTH_DAYS),
    (msg_c.KEY_MENTAL_HEALTH_DAYS, PERSIST_DEFAULT_HEALTH_DAYS),
    (msg_c.KEY_LAST_CHECKUP_TIME, PERSIST_DEFAULT_LAST_CHECKUP_TIME),
    (msg_c.KEY_PHYSICAL_ACTIVITIES, PERSIST_DEFAULT_BOOL),
    (msg_c.KEY_SLEEP_HOURS, PERSIST_DEFAULT_SLEEP_HOURS),
    (msg_c.KEY_SMOKER_STATUS, PERSIST_DEFAULT_SMOKER_STATUS),
    (msg_c.KEY_ECIGARETTE_USAGE, PERSIST_DEFAULT_ECIGARETTE_USAGE),
    (msg_c.KEY_ALCOHOL_DRINKERS, PERSIST_DEFAULT_BOOL),
    (msg_c.KEY_CHEST_SCAN, PERSIST_DEFAULT_BOOL),
    (msg_c.KEY_HIV_TESTING, PERSIST_DEFAULT_BOOL),
    (msg_c.KEY_FLU_VAX_LAST_12, PERSIST_DEFAULT_BOOL),
    (msg_c.KEY_PNEUMO_VAX_EVER, PERSIST_DEFAULT_BOOL),
    (msg_c.KEY_TETANUS_LAST_10_TDAP, PERSIST_DEFAULT_TETANUS_LAST_10_TDAP),
    (msg_c.KEY_HIGH_RISK_LAST_YEAR, PERSIST_DEFAULT_BOOL),
    (msg_c.KEY_COVID_POS, PERSIST_DEFAULT_COVID_POS),
)

PREDICTIONS_CHECK_NAME: Final[str] = "ck_predictions_user_or_session"
PREDICTIONS_CHECK_SQL: Final[str] = (
    f"({v.COL_USER_ID} IS NOT NULL AND {v.COL_SESSION_ID} IS NULL) OR "
    f"({v.COL_USER_ID} IS NULL AND {v.COL_SESSION_ID} IS NOT NULL)"
)

IX_PREDICTIONS_USER_ID: Final[str] = "ix_predictions_user_id"
IX_PREDICTIONS_PREDICTION_TIMESTAMP: Final[str] = "ix_predictions_prediction_timestamp"
IX_PREDICTIONS_SESSION_ID: Final[str] = "ix_predictions_session_id"
