"""ML artifact names, training column layout, and SHAP / inference literals."""

from pathlib import Path
from typing import Final

# --- Layout under app/ml/ ---
ML_MODELS_SUBDIR_NAME: Final[str] = "models"
ML_ARTIFACT_MODEL: Final[str] = "best_mlp_model.joblib"
ML_ARTIFACT_ONE_HOT_ENCODER: Final[str] = "one_hot_encoder.joblib"
ML_ARTIFACT_STANDARD_SCALER: Final[str] = "standard_scaler.joblib"
ML_ARTIFACT_LABEL_ENCODER: Final[str] = "label_encoder.joblib"
ML_ARTIFACT_SHAP_BACKGROUND: Final[str] = "shap_background.joblib"

# Bump when retraining / swapping artifacts (also persisted as model_version).
ML_MODEL_VERSION: Final[str] = "mlp-brfss-1.0.0"

# Trained column names (PascalCase) — must match the notebook / training export.
COL_GENERAL_HEALTH: Final[str] = "GeneralHealth"
COL_LAST_CHECKUP_TIME: Final[str] = "LastCheckupTime"
COL_REMOVED_TEETH: Final[str] = "RemovedTeeth"
COL_HAD_DIABETES: Final[str] = "HadDiabetes"
COL_SMOKER_STATUS: Final[str] = "SmokerStatus"
COL_ECIGARETTE_USAGE: Final[str] = "ECigaretteUsage"
COL_AGE_CATEGORY: Final[str] = "AgeCategory"
COL_TETANUS_LAST_10_TDAP: Final[str] = "TetanusLast10Tdap"
COL_COVID_POS: Final[str] = "CovidPos"

ONE_HOT_FEATURE_NAMES: Final[tuple[str, ...]] = (
    COL_GENERAL_HEALTH,
    COL_LAST_CHECKUP_TIME,
    COL_REMOVED_TEETH,
    COL_HAD_DIABETES,
    COL_SMOKER_STATUS,
    COL_ECIGARETTE_USAGE,
    COL_AGE_CATEGORY,
    COL_TETANUS_LAST_10_TDAP,
    COL_COVID_POS,
)

COL_PHYSICAL_HEALTH_DAYS: Final[str] = "PhysicalHealthDays"
COL_MENTAL_HEALTH_DAYS: Final[str] = "MentalHealthDays"
COL_SLEEP_HOURS: Final[str] = "SleepHours"
COL_HEIGHT_IN_METERS: Final[str] = "HeightInMeters"
COL_WEIGHT_IN_KILOGRAMS: Final[str] = "WeightInKilograms"
COL_BMI: Final[str] = "BMI"

STANDARD_SCALE_FEATURE_NAMES: Final[tuple[str, ...]] = (
    COL_PHYSICAL_HEALTH_DAYS,
    COL_MENTAL_HEALTH_DAYS,
    COL_SLEEP_HOURS,
    COL_HEIGHT_IN_METERS,
    COL_WEIGHT_IN_KILOGRAMS,
    COL_BMI,
)

COL_SEX: Final[str] = "Sex"
COL_PHYSICAL_ACTIVITIES: Final[str] = "PhysicalActivities"
COL_HAD_ANGINA: Final[str] = "HadAngina"
COL_HAD_STROKE: Final[str] = "HadStroke"
COL_HAD_ASTHMA: Final[str] = "HadAsthma"
COL_HAD_COPD: Final[str] = "HadCOPD"
COL_HAD_SKIN_CANCER: Final[str] = "HadSkinCancer"
COL_HAD_DEPRESSIVE_DISORDER: Final[str] = "HadDepressiveDisorder"
COL_HAD_KIDNEY_DISEASE: Final[str] = "HadKidneyDisease"
COL_HAD_ARTHRITIS: Final[str] = "HadArthritis"
COL_DEAF_OR_HARD_OF_HEARING: Final[str] = "DeafOrHardOfHearing"
COL_BLIND_OR_VISION_DIFFICULTY: Final[str] = "BlindOrVisionDifficulty"
COL_DIFFICULTY_CONCENTRATING: Final[str] = "DifficultyConcentrating"
COL_DIFFICULTY_WALKING: Final[str] = "DifficultyWalking"
COL_DIFFICULTY_DRESSING_BATHING: Final[str] = "DifficultyDressingBathing"
COL_DIFFICULTY_ERRANDS: Final[str] = "DifficultyErrands"
COL_ALCOHOL_DRINKERS: Final[str] = "AlcoholDrinkers"
COL_CHEST_SCAN: Final[str] = "ChestScan"
COL_HIV_TESTING: Final[str] = "HIVTesting"
COL_FLU_VAX_LAST_12: Final[str] = "FluVaxLast12"
COL_PNEUMO_VAX_EVER: Final[str] = "PneumoVaxEver"
COL_HIGH_RISK_LAST_YEAR: Final[str] = "HighRiskLastYear"

# Binary / numeric passthrough block order (strict; concat after OHE + scaled columns).
PASSTHROUGH_FEATURE_NAMES: Final[tuple[str, ...]] = (
    COL_SEX,
    COL_PHYSICAL_ACTIVITIES,
    COL_HAD_ANGINA,
    COL_HAD_STROKE,
    COL_HAD_ASTHMA,
    COL_HAD_COPD,
    COL_HAD_SKIN_CANCER,
    COL_HAD_DEPRESSIVE_DISORDER,
    COL_HAD_KIDNEY_DISEASE,
    COL_HAD_ARTHRITIS,
    COL_DEAF_OR_HARD_OF_HEARING,
    COL_BLIND_OR_VISION_DIFFICULTY,
    COL_DIFFICULTY_CONCENTRATING,
    COL_DIFFICULTY_WALKING,
    COL_DIFFICULTY_DRESSING_BATHING,
    COL_DIFFICULTY_ERRANDS,
    COL_ALCOHOL_DRINKERS,
    COL_CHEST_SCAN,
    COL_HIV_TESTING,
    COL_FLU_VAX_LAST_12,
    COL_PNEUMO_VAX_EVER,
    COL_HIGH_RISK_LAST_YEAR,
)

# Training used Female=0, Male=1 for Sex (adjust if your notebook differs).
SEX_ENCODED_FEMALE: Final[float] = 0.0
SEX_ENCODED_MALE: Final[float] = 1.0

# Binary classification: probability scale and positive-class index (adjust if labels inverted).
POSITIVE_CLASS_PROB_INDEX: Final[int] = 1

# SHAP (KernelExplainer)
SHAP_KERNEL_NSAMPLES: Final[int] = 80
SHAP_BACKGROUND_MAX_ROWS: Final[int] = 200
SHAP_IMPACT_DECIMALS: Final[int] = 6

SHAP_DIRECTION_INCREASES_RISK: Final[str] = "increases_risk"
SHAP_DIRECTION_DECREASES_RISK: Final[str] = "decreases_risk"

MSG_SHAP_INCREASES: Final[str] = (
    '"{feature}" es el factor con mayor contribución SHAP en esta predicción; '
    "empuja la probabilidad de la clase positiva hacia arriba."
)
MSG_SHAP_DECREASES: Final[str] = (
    '"{feature}" es el factor con mayor contribución SHAP en esta predicción; '
    "empuja la probabilidad de la clase positiva hacia abajo."
)

ERROR_ML_ARTIFACTS_MISSING: Final[str] = (
    "Los artefactos del modelo no están disponibles en el servidor (ruta ML configurada)."
)
ERROR_ML_INFERENCE_FAILED: Final[str] = "Error al ejecutar la inferencia del modelo de riesgo."

ERROR_ML_FEATURE_LAYOUT_MISMATCH: Final[str] = (
    "El vector de características no coincide con el orden esperado del modelo "
    "(revisar shap_background con columnas o artefactos de preprocesado)."
)

MSG_SHAP_FALLBACK: Final[str] = (
    "No se pudo calcular SHAP para esta solicitud; se omitió la explicación detallada."
)

# Resolver: app/ml/models (or ML_MODELS_DIR env — see artifacts module)
def default_models_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "ml" / ML_MODELS_SUBDIR_NAME
