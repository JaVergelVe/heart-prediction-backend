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

# --- Prediction (response + internal feature bundle keys) ---
KEY_SURVEY: Final[str] = "survey"
KEY_PREDICTION_ID: Final[str] = "prediction_id"
KEY_SESSION_ID: Final[str] = "session_id"
KEY_WEIGHT_KILOGRAMS: Final[str] = "weight_kilograms"
KEY_BMI: Final[str] = "bmi"
KEY_PREDICTION_PROBABILITY: Final[str] = "prediction_probability"
KEY_RISK_LEVEL: Final[str] = "risk_level"
KEY_MODEL_VERSION: Final[str] = "model_version"
KEY_PREDICTION_TIMESTAMP: Final[str] = "prediction_timestamp"
KEY_GENERAL_HEALTH: Final[str] = "general_health"
KEY_PHYSICAL_HEALTH_DAYS: Final[str] = "physical_health_days"
KEY_MENTAL_HEALTH_DAYS: Final[str] = "mental_health_days"
KEY_LAST_CHECKUP_TIME: Final[str] = "last_checkup_time"
KEY_PHYSICAL_ACTIVITIES: Final[str] = "physical_activities"
KEY_SLEEP_HOURS: Final[str] = "sleep_hours"
KEY_SMOKER_STATUS: Final[str] = "smoker_status"
KEY_ECIGARETTE_USAGE: Final[str] = "ecigarette_usage"
KEY_ALCOHOL_DRINKERS: Final[str] = "alcohol_drinkers"
KEY_CHEST_SCAN: Final[str] = "chest_scan"
KEY_HIV_TESTING: Final[str] = "hiv_testing"
KEY_FLU_VAX_LAST_12: Final[str] = "flu_vax_last_12"
KEY_PNEUMO_VAX_EVER: Final[str] = "pneumo_vax_ever"
KEY_TETANUS_LAST_10_TDAP: Final[str] = "tetanus_last_10_tdap"
KEY_HIGH_RISK_LAST_YEAR: Final[str] = "high_risk_last_year"
KEY_COVID_POS: Final[str] = "covid_pos"
KEY_PREDICTED_CLASS: Final[str] = "predicted_class"
KEY_SHAP_EXPLANATION: Final[str] = "shap_explanation"
KEY_SHAP_FEATURE_NAME: Final[str] = "feature_name"
KEY_SHAP_IMPACT_SCORE: Final[str] = "impact_score"
KEY_SHAP_DIRECTION: Final[str] = "direction"
KEY_SHAP_MESSAGE: Final[str] = "message"

# --- Paginated lists (predictions history) ---
KEY_PREDICTIONS: Final[str] = "predictions"
KEY_PAGINATION: Final[str] = "pagination"
KEY_TOTAL: Final[str] = "total"
KEY_LIMIT: Final[str] = "limit"
KEY_OFFSET: Final[str] = "offset"
KEY_HAS_MORE: Final[str] = "has_more"

# --- Error codes ---
ERROR_CODE_VALIDATION: Final[str] = "VALIDATION_ERROR"
ERROR_CODE_INVALID_CREDENTIALS: Final[str] = "INVALID_CREDENTIALS"
ERROR_CODE_UNAUTHORIZED: Final[str] = "UNAUTHORIZED"
ERROR_CODE_INTERNAL: Final[str] = "INTERNAL_ERROR"
ERROR_CODE_PROFILE_INCOMPLETE: Final[str] = "PROFILE_INCOMPLETE"
ERROR_CODE_PREDICTION_NOT_FOUND: Final[str] = "PREDICTION_NOT_FOUND"
ERROR_CODE_INVALID_VARIABLE: Final[str] = "INVALID_VARIABLE"
ERROR_CODE_CATALOG_FIELD_NOT_SUPPORTED: Final[str] = "CATALOG_FIELD_NOT_SUPPORTED"

# --- What-if simulation (response keys) ---
KEY_ORIGINAL_PROBABILITY: Final[str] = "original_probability"
KEY_SIMULATED_PROBABILITY: Final[str] = "simulated_probability"
KEY_ORIGINAL_RISK_LEVEL: Final[str] = "original_risk_level"
KEY_SIMULATED_RISK_LEVEL: Final[str] = "simulated_risk_level"
KEY_PROBABILITY_DIFFERENCE: Final[str] = "probability_difference"
KEY_CHANGED_FIELDS: Final[str] = "changed_fields"
KEY_RECOMMENDATIONS: Final[str] = "recommendations"
KEY_ORIGINAL_VALUE: Final[str] = "original"
KEY_SIMULATED_VALUE: Final[str] = "simulated"

# --- Human-readable messages ---
MSG_VALIDATION_FAILED: Final[str] = "Error en validación de datos"
MSG_INVALID_CREDENTIALS: Final[str] = "Email o contraseña incorrectos"
MSG_TOKEN_INVALID_OR_EXPIRED: Final[str] = "Token inválido o expirado"
MSG_TOKEN_REQUIRED: Final[str] = "Token de acceso requerido"
MSG_VALIDATION_INVALID_INPUT: Final[str] = "Invalid input"
MSG_PROFILE_INCOMPLETE: Final[str] = "Perfil de usuario incompleto"
MSG_PREDICTION_PROFILE_INCOMPLETE: Final[str] = (
    "Se requiere perfil y condiciones médicas completas para generar una predicción"
)
MSG_PREDICTION_HEIGHT_REQUIRED: Final[str] = (
    "Se requiere altura en metros en el perfil para calcular el IMC"
)
MSG_BMI_OUT_OF_DB_RANGE: Final[str] = (
    "El IMC calculado debe estar entre 10 y 100 según las reglas de la base de datos"
)
MSG_PREDICTION_NOT_FOUND: Final[str] = "Predicción no encontrada"
MSG_SIMULATION_VARIABLE_NOT_MODIFIABLE: Final[str] = "Variable no modificable"
MSG_SIMULATION_REASON_FORBIDDEN: Final[str] = (
    "Las variables demográficas y condiciones médicas crónicas no pueden modificarse en simulaciones"
)
MSG_SIMULATION_BASELINE_INCOMPLETE: Final[str] = (
    "La predicción base no tiene los datos necesarios para simular"
)
MSG_CATALOG_FIELD_NOT_SUPPORTED: Final[str] = "Campo de catálogo no soportado"
MSG_CATALOG_UNSUPPORTED_FIELD_REASON: Final[str] = (
    "El campo no figura en el catálogo de valores permitidos."
)
MSG_HISTORY_INVALID_SORT: Final[str] = "Campo de ordenamiento no válido"
MSG_HISTORY_INVALID_ORDER: Final[str] = "Orden debe ser asc o desc"
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
