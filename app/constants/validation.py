"""API validation limits, defaults, and SQLAlchemy / schema numeric & name literals."""

from typing import Final

# --- Application defaults (Settings) ---
APP_NAME_DEFAULT: Final[str] = "Heart Attack Prediction API"
API_VERSION_DEFAULT: Final[str] = "1.0.0"
DEBUG_DEFAULT: Final[bool] = False

# --- Register / login validation ---
MIN_AGE_YEARS: Final[int] = 18
MAX_AGE_YEARS: Final[int] = 120
MIN_PASSWORD_LENGTH: Final[int] = 8
MAX_PASSWORD_LENGTH: Final[int] = 128
MIN_LOGIN_PASSWORD_LENGTH: Final[int] = 1
HEIGHT_METERS_MIN: Final[float] = 0.5
HEIGHT_METERS_MAX: Final[float] = 2.5

# --- Prediction input (survey / vitals) ---
WEIGHT_KG_MIN: Final[float] = 20.0
WEIGHT_KG_MAX: Final[float] = 300.0
PHYSICAL_MENTAL_HEALTH_DAYS_MIN: Final[int] = 0
PHYSICAL_MENTAL_HEALTH_DAYS_MAX: Final[int] = 30
SLEEP_HOURS_MIN: Final[float] = 0.0
SLEEP_HOURS_MAX: Final[float] = 24.0

# --- User row ---
DEFAULT_USER_IS_ACTIVE: Final[bool] = True

# --- Table names ---
TABLE_USERS: Final[str] = "users"
TABLE_USER_PROFILES: Final[str] = "user_profiles"
TABLE_MEDICAL_CONDITIONS: Final[str] = "medical_conditions"
TABLE_PREDICTIONS: Final[str] = "predictions"

# --- Column names (FK / PK / common) ---
COL_ID: Final[str] = "id"
COL_USER_ID: Final[str] = "user_id"
COL_SESSION_ID: Final[str] = "session_id"
COL_EMAIL: Final[str] = "email"
COL_PASSWORD_HASH: Final[str] = "password_hash"
COL_IS_ACTIVE: Final[str] = "is_active"
COL_LAST_LOGIN: Final[str] = "last_login"
COL_SEX: Final[str] = "sex"
COL_BIRTH_DATE: Final[str] = "birth_date"
COL_AGE_CATEGORY: Final[str] = "age_category"
COL_HEIGHT_METERS: Final[str] = "height_meters"
COL_REMOVED_TEETH: Final[str] = "removed_teeth"
COL_HAD_DIABETES: Final[str] = "had_diabetes"
COL_PREDICTION_TIMESTAMP: Final[str] = "prediction_timestamp"
COL_CREATED_AT: Final[str] = "created_at"
COL_UPDATED_AT: Final[str] = "updated_at"

# --- FK targets ---
FK_USERS_ID: Final[str] = f"{TABLE_USERS}.{COL_ID}"

# --- ON DELETE ---
ON_DELETE_CASCADE: Final[str] = "CASCADE"

# --- String / numeric column specs (SQLAlchemy) ---
DB_UUID_STR_LEN: Final[int] = 36
DB_EMAIL_MAX_LEN: Final[int] = 255
DB_PASSWORD_HASH_MAX_LEN: Final[int] = 255
DB_SEX_MAX_LEN: Final[int] = 10
DB_AGE_CATEGORY_MAX_LEN: Final[int] = 64
DB_REMOVED_TEETH_MAX_LEN: Final[int] = 64
DB_HEIGHT_METERS_PRECISION: Final[int] = 4
DB_HEIGHT_METERS_SCALE: Final[int] = 2
DB_HAD_DIABETES_MAX_LEN: Final[int] = 100

DB_WEIGHT_KG_PRECISION: Final[int] = 5
DB_WEIGHT_KG_SCALE: Final[int] = 2
DB_BMI_PRECISION: Final[int] = 5
DB_BMI_SCALE: Final[int] = 2
DB_GENERAL_HEALTH_MAX_LEN: Final[int] = 20
DB_LAST_CHECKUP_MAX_LEN: Final[int] = 100
DB_SMOKER_STATUS_MAX_LEN: Final[int] = 50
DB_ECIGARETTE_MAX_LEN: Final[int] = 100
DB_TETANUS_MAX_LEN: Final[int] = 100
DB_COVID_POS_MAX_LEN: Final[int] = 100
DB_RISK_LEVEL_MAX_LEN: Final[int] = 10
DB_MODEL_VERSION_MAX_LEN: Final[int] = 50
DB_SESSION_ID_MAX_LEN: Final[int] = 255
DB_SLEEP_HOURS_PRECISION: Final[int] = 3
DB_SLEEP_HOURS_SCALE: Final[int] = 1
DB_PREDICTION_PROB_PRECISION: Final[int] = 5
DB_PREDICTION_PROB_SCALE: Final[int] = 2
