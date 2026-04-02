"""User-facing messages, log templates, and JSON envelope / field keys."""

from typing import Final

# --- Error envelope (docs/api-contracts.md shape) ---
KEY_ERROR: Final[str] = "error"
KEY_CODE: Final[str] = "code"
KEY_MESSAGE: Final[str] = "message"
KEY_DETAILS: Final[str] = "details"
KEY_FIELD: Final[str] = "field"
KEY_REASON: Final[str] = "reason"

# --- Success envelope ---
KEY_DATA: Final[str] = "data"

# --- Auth response / user payload keys ---
KEY_USER_ID: Final[str] = "user_id"
KEY_EMAIL: Final[str] = "email"
KEY_ACCESS_TOKEN: Final[str] = "access_token"
KEY_TOKEN_TYPE: Final[str] = "token_type"
KEY_EXPIRES_IN: Final[str] = "expires_in"
KEY_CREATED_AT: Final[str] = "created_at"
KEY_LAST_LOGIN: Final[str] = "last_login"

# --- Profile keys ---
KEY_PROFILE: Final[str] = "profile"
KEY_SEX: Final[str] = "sex"
KEY_BIRTH_DATE: Final[str] = "birth_date"
KEY_AGE_CATEGORY: Final[str] = "age_category"
KEY_HEIGHT_METERS: Final[str] = "height_meters"
KEY_REMOVED_TEETH: Final[str] = "removed_teeth"
KEY_UPDATED_AT: Final[str] = "updated_at"

# --- Medical conditions block ---
KEY_MEDICAL_CONDITIONS: Final[str] = "medical_conditions"
KEY_HAD_ANGINA: Final[str] = "had_angina"
KEY_HAD_STROKE: Final[str] = "had_stroke"
KEY_HAD_ASTHMA: Final[str] = "had_asthma"
KEY_HAD_COPD: Final[str] = "had_copd"
KEY_HAD_SKIN_CANCER: Final[str] = "had_skin_cancer"
KEY_HAD_DEPRESSIVE_DISORDER: Final[str] = "had_depressive_disorder"
KEY_HAD_KIDNEY_DISEASE: Final[str] = "had_kidney_disease"
KEY_HAD_ARTHRITIS: Final[str] = "had_arthritis"
KEY_HAD_DIABETES: Final[str] = "had_diabetes"
KEY_DEAF_OR_HARD_OF_HEARING: Final[str] = "deaf_or_hard_of_hearing"
KEY_BLIND_OR_VISION_DIFFICULTY: Final[str] = "blind_or_vision_difficulty"
KEY_DIFFICULTY_CONCENTRATING: Final[str] = "difficulty_concentrating"
KEY_DIFFICULTY_WALKING: Final[str] = "difficulty_walking"
KEY_DIFFICULTY_DRESSING_BATHING: Final[str] = "difficulty_dressing_bathing"
KEY_DIFFICULTY_ERRANDS: Final[str] = "difficulty_errands"

# --- Error codes ---
ERROR_CODE_VALIDATION: Final[str] = "VALIDATION_ERROR"
ERROR_CODE_INVALID_CREDENTIALS: Final[str] = "INVALID_CREDENTIALS"
ERROR_CODE_UNAUTHORIZED: Final[str] = "UNAUTHORIZED"
ERROR_CODE_INTERNAL: Final[str] = "INTERNAL_ERROR"

# --- Human-readable messages ---
MSG_VALIDATION_FAILED: Final[str] = "Error en validación de datos"
MSG_INVALID_CREDENTIALS: Final[str] = "Email o contraseña incorrectos"
MSG_TOKEN_INVALID_OR_EXPIRED: Final[str] = "Token inválido o expirado"
MSG_TOKEN_REQUIRED: Final[str] = "Token de acceso requerido"
MSG_VALIDATION_INVALID_INPUT: Final[str] = "Invalid input"
MSG_PROFILE_INCOMPLETE: Final[str] = "Perfil de usuario incompleto"
MSG_BIRTH_DATE_AGE_RANGE: Final[str] = "La edad debe estar entre 18 y 120 años"
MSG_PASSWORD_NEED_LETTER: Final[str] = "La contraseña debe incluir al menos una letra"
MSG_PASSWORD_NEED_DIGIT: Final[str] = "La contraseña debe incluir al menos un número"

# --- Field / reason strings (validation & duplicate email) ---
FIELD_EMAIL: Final[str] = "email"
FIELD_BODY: Final[str] = "body"
REASON_EMAIL_REGISTERED: Final[str] = "Email ya está registrado"

# --- Defaults in JSON responses ---
DEFAULT_HAD_DIABETES_DISPLAY: Final[str] = "No"

# --- HTTP / infrastructure messages ---
HTTP_DETAIL_DATABASE_NOT_CONFIGURED: Final[str] = "Database not configured"

# --- Logging (database health) ---
LOG_DB_HEALTH_CHECK_FAIL: Final[str] = "Database health check failed: %s"

# --- ISO-8601 UTC formatting (timefmt helper) ---
ISO_DATETIME_UTC_OFFSET_LEGACY: Final[str] = "+00:00"
ISO_DATETIME_Z_SUFFIX: Final[str] = "Z"
