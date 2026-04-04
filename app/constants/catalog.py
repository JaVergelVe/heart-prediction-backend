"""Catalog API: allowed categorical values, field copy, and what-if variable metadata."""

from typing import Any, Final

from app.constants import arrays as arr_c
from app.constants import messages as msg_c
from app.constants import prediction as pred_c
from app.constants import prediction_survey as ps
from app.constants import validation as v

# --- Response keys (catalog payloads under `data`) ---
KEY_FIELD: Final[str] = "field"
KEY_DESCRIPTION: Final[str] = "description"
KEY_ALLOWED_VALUES: Final[str] = "allowed_values"
KEY_MODIFIABLE_VARIABLES: Final[str] = "modifiable_variables"
KEY_FIXED_VARIABLES: Final[str] = "fixed_variables"
KEY_NAME: Final[str] = "name"
KEY_TYPE: Final[str] = "type"
KEY_MIN: Final[str] = "min"
KEY_MAX: Final[str] = "max"
KEY_UNIT: Final[str] = "unit"

# --- Variable kinds for what-if catalog ---
TYPE_BOOLEAN: Final[str] = "boolean"
TYPE_CATEGORICAL: Final[str] = "categorical"
TYPE_INTEGER: Final[str] = "integer"
TYPE_NUMBER: Final[str] = "number"

UNIT_KG: Final[str] = "kg"
UNIT_DAYS: Final[str] = "days"
UNIT_HOURS: Final[str] = "hours"

# --- Ordered allowed values (single source per domain) ---
VALUES_GENERAL_HEALTH: Final[tuple[str, ...]] = tuple(m.value for m in ps.GeneralHealth)
VALUES_LAST_CHECKUP_TIME: Final[tuple[str, ...]] = tuple(m.value for m in ps.LastCheckupTime)
VALUES_SMOKER_STATUS: Final[tuple[str, ...]] = tuple(m.value for m in ps.SmokerStatus)
VALUES_ECIGARETTE_USAGE: Final[tuple[str, ...]] = tuple(m.value for m in ps.EcigaretteUsage)
VALUES_TETANUS_LAST_10_TDAP: Final[tuple[str, ...]] = tuple(m.value for m in ps.TetanusLast10Tdap)
VALUES_COVID_POS: Final[tuple[str, ...]] = tuple(m.value for m in ps.CovidPos)
VALUES_HAD_DIABETES: Final[tuple[str, ...]] = (
    arr_c.HAD_DIABETES_NO,
    arr_c.HAD_DIABETES_YES,
    arr_c.HAD_DIABETES_PRE_DIABETES,
    arr_c.HAD_DIABETES_PREGNANCY,
)
VALUES_REMOVED_TEETH: Final[tuple[str, ...]] = (
    arr_c.REMOVED_TEETH_NONE_OF_THEM,
    arr_c.REMOVED_TEETH_1_TO_5,
    arr_c.REMOVED_TEETH_6_OR_MORE_NOT_ALL,
    arr_c.REMOVED_TEETH_ALL,
)
VALUES_AGE_CATEGORY: Final[tuple[str, ...]] = tuple(
    b[arr_c.AGE_BRACKET_IDX_LABEL] for b in arr_c.AGE_BRACKETS
) + (arr_c.AGE_CATEGORY_80_OR_OLDER,)
VALUES_SEX: Final[tuple[str, ...]] = (arr_c.SEX_MALE, arr_c.SEX_FEMALE)

# --- Per-field catalog (GET /catalogs/{field}) ---
DESC_GENERAL_HEALTH: Final[str] = (
    "Autopercepción del estado general de salud (escala BRFSS)."
)
DESC_LAST_CHECKUP_TIME: Final[str] = "Tiempo transcurrido desde el último chequeo médico general."
DESC_SMOKER_STATUS: Final[str] = "Estado actual o histórico de consumo de tabaco."
DESC_ECIGARETTE_USAGE: Final[str] = "Uso de cigarrillos electrónicos o vaporizadores."
DESC_TETANUS_LAST_10_TDAP: Final[str] = (
    "Vacunación contra tétanos / Tdap en los últimos 10 años."
)
DESC_COVID_POS: Final[str] = "Resultado o historial de prueba de COVID-19."
DESC_HAD_DIABETES: Final[str] = (
    "Historial de diabetes o prediabetes (registro de perfil; no modificable en simulación)."
)
DESC_REMOVED_TEETH: Final[str] = (
    "Cantidad de dientes extraídos (registro de perfil; no modificable en simulación)."
)
DESC_AGE_CATEGORY: Final[str] = (
    "Franja etaria derivada de la fecha de nacimiento (solo lectura en predicción)."
)
DESC_SEX: Final[str] = "Sexo registrado en el perfil (no modificable en simulación)."

CATALOG_SUPPORTED_FIELDS: Final[frozenset[str]] = frozenset(
    {
        msg_c.KEY_GENERAL_HEALTH,
        msg_c.KEY_LAST_CHECKUP_TIME,
        msg_c.KEY_SMOKER_STATUS,
        msg_c.KEY_ECIGARETTE_USAGE,
        msg_c.KEY_TETANUS_LAST_10_TDAP,
        msg_c.KEY_COVID_POS,
        msg_c.KEY_HAD_DIABETES,
        msg_c.KEY_REMOVED_TEETH,
        msg_c.KEY_AGE_CATEGORY,
        msg_c.KEY_SEX,
    }
)

CATALOG_FIELD_DESCRIPTIONS: Final[dict[str, str]] = {
    msg_c.KEY_GENERAL_HEALTH: DESC_GENERAL_HEALTH,
    msg_c.KEY_LAST_CHECKUP_TIME: DESC_LAST_CHECKUP_TIME,
    msg_c.KEY_SMOKER_STATUS: DESC_SMOKER_STATUS,
    msg_c.KEY_ECIGARETTE_USAGE: DESC_ECIGARETTE_USAGE,
    msg_c.KEY_TETANUS_LAST_10_TDAP: DESC_TETANUS_LAST_10_TDAP,
    msg_c.KEY_COVID_POS: DESC_COVID_POS,
    msg_c.KEY_HAD_DIABETES: DESC_HAD_DIABETES,
    msg_c.KEY_REMOVED_TEETH: DESC_REMOVED_TEETH,
    msg_c.KEY_AGE_CATEGORY: DESC_AGE_CATEGORY,
    msg_c.KEY_SEX: DESC_SEX,
}

CATALOG_FIELD_ALLOWED_VALUES: Final[dict[str, tuple[str, ...]]] = {
    msg_c.KEY_GENERAL_HEALTH: VALUES_GENERAL_HEALTH,
    msg_c.KEY_LAST_CHECKUP_TIME: VALUES_LAST_CHECKUP_TIME,
    msg_c.KEY_SMOKER_STATUS: VALUES_SMOKER_STATUS,
    msg_c.KEY_ECIGARETTE_USAGE: VALUES_ECIGARETTE_USAGE,
    msg_c.KEY_TETANUS_LAST_10_TDAP: VALUES_TETANUS_LAST_10_TDAP,
    msg_c.KEY_COVID_POS: VALUES_COVID_POS,
    msg_c.KEY_HAD_DIABETES: VALUES_HAD_DIABETES,
    msg_c.KEY_REMOVED_TEETH: VALUES_REMOVED_TEETH,
    msg_c.KEY_AGE_CATEGORY: VALUES_AGE_CATEGORY,
    msg_c.KEY_SEX: VALUES_SEX,
}

# --- What-if: stable ordering (must match SIMULATION_ALLOWED_FIELDS) ---
MODIFIABLE_FIELDS_ORDER: Final[tuple[str, ...]] = (
    msg_c.KEY_WEIGHT_KILOGRAMS,
    msg_c.KEY_GENERAL_HEALTH,
    msg_c.KEY_PHYSICAL_HEALTH_DAYS,
    msg_c.KEY_MENTAL_HEALTH_DAYS,
    msg_c.KEY_LAST_CHECKUP_TIME,
    msg_c.KEY_PHYSICAL_ACTIVITIES,
    msg_c.KEY_SLEEP_HOURS,
    msg_c.KEY_SMOKER_STATUS,
    msg_c.KEY_ECIGARETTE_USAGE,
    msg_c.KEY_ALCOHOL_DRINKERS,
    msg_c.KEY_CHEST_SCAN,
    msg_c.KEY_HIV_TESTING,
    msg_c.KEY_FLU_VAX_LAST_12,
    msg_c.KEY_PNEUMO_VAX_EVER,
    msg_c.KEY_TETANUS_LAST_10_TDAP,
    msg_c.KEY_HIGH_RISK_LAST_YEAR,
    msg_c.KEY_COVID_POS,
)

DESC_MOD_WEIGHT: Final[str] = "Peso corporal usado para calcular el IMC en la simulación."
DESC_MOD_GENERAL_HEALTH: Final[str] = "Autopercepción del estado general de salud."
DESC_MOD_PHYSICAL_HEALTH_DAYS: Final[str] = (
    "Días en los que la salud física no fue buena (últimos 30 días)."
)
DESC_MOD_MENTAL_HEALTH_DAYS: Final[str] = (
    "Días en los que la salud mental no fue buena (últimos 30 días)."
)
DESC_MOD_LAST_CHECKUP: Final[str] = "Tiempo desde el último chequeo médico general."
DESC_MOD_PHYSICAL_ACTIVITIES: Final[str] = (
    "Actividad física en el tiempo libre en la última semana."
)
DESC_MOD_SLEEP_HOURS: Final[str] = "Horas de sueño en un día típico."
DESC_MOD_SMOKER: Final[str] = "Estado de tabaquismo."
DESC_MOD_ECIG: Final[str] = "Uso de cigarrillos electrónicos."
DESC_MOD_ALCOHOL: Final[str] = "Consumo de alcohol."
DESC_MOD_CHEST_SCAN: Final[str] = "Antecedente de tomografía o radiografía de tórax."
DESC_MOD_HIV: Final[str] = "Prueba de VIH alguna vez."
DESC_MOD_FLU: Final[str] = "Vacuna contra la gripe en los últimos 12 meses."
DESC_MOD_PNEUMO: Final[str] = "Vacuna neumocócica alguna vez."
DESC_MOD_TETANUS: Final[str] = "Vacuna de tétanos / Tdap en los últimos 10 años."
DESC_MOD_HIGH_RISK: Final[str] = "Condiciones de alto riesgo para enfermedad grave (último año)."
DESC_MOD_COVID: Final[str] = "Resultado o historial de COVID-19."

MODIFIABLE_VARIABLE_SPECS: Final[dict[str, dict[str, Any]]] = {
    msg_c.KEY_WEIGHT_KILOGRAMS: {
        KEY_TYPE: TYPE_NUMBER,
        KEY_MIN: v.WEIGHT_KG_MIN,
        KEY_MAX: v.WEIGHT_KG_MAX,
        KEY_UNIT: UNIT_KG,
        KEY_DESCRIPTION: DESC_MOD_WEIGHT,
    },
    msg_c.KEY_GENERAL_HEALTH: {
        KEY_TYPE: TYPE_CATEGORICAL,
        KEY_ALLOWED_VALUES: list(VALUES_GENERAL_HEALTH),
        KEY_DESCRIPTION: DESC_MOD_GENERAL_HEALTH,
    },
    msg_c.KEY_PHYSICAL_HEALTH_DAYS: {
        KEY_TYPE: TYPE_INTEGER,
        KEY_MIN: v.PHYSICAL_MENTAL_HEALTH_DAYS_MIN,
        KEY_MAX: v.PHYSICAL_MENTAL_HEALTH_DAYS_MAX,
        KEY_UNIT: UNIT_DAYS,
        KEY_DESCRIPTION: DESC_MOD_PHYSICAL_HEALTH_DAYS,
    },
    msg_c.KEY_MENTAL_HEALTH_DAYS: {
        KEY_TYPE: TYPE_INTEGER,
        KEY_MIN: v.PHYSICAL_MENTAL_HEALTH_DAYS_MIN,
        KEY_MAX: v.PHYSICAL_MENTAL_HEALTH_DAYS_MAX,
        KEY_UNIT: UNIT_DAYS,
        KEY_DESCRIPTION: DESC_MOD_MENTAL_HEALTH_DAYS,
    },
    msg_c.KEY_LAST_CHECKUP_TIME: {
        KEY_TYPE: TYPE_CATEGORICAL,
        KEY_ALLOWED_VALUES: list(VALUES_LAST_CHECKUP_TIME),
        KEY_DESCRIPTION: DESC_MOD_LAST_CHECKUP,
    },
    msg_c.KEY_PHYSICAL_ACTIVITIES: {
        KEY_TYPE: TYPE_BOOLEAN,
        KEY_ALLOWED_VALUES: [True, False],
        KEY_DESCRIPTION: DESC_MOD_PHYSICAL_ACTIVITIES,
    },
    msg_c.KEY_SLEEP_HOURS: {
        KEY_TYPE: TYPE_NUMBER,
        KEY_MIN: v.SLEEP_HOURS_MIN,
        KEY_MAX: v.SLEEP_HOURS_MAX,
        KEY_UNIT: UNIT_HOURS,
        KEY_DESCRIPTION: DESC_MOD_SLEEP_HOURS,
    },
    msg_c.KEY_SMOKER_STATUS: {
        KEY_TYPE: TYPE_CATEGORICAL,
        KEY_ALLOWED_VALUES: list(VALUES_SMOKER_STATUS),
        KEY_DESCRIPTION: DESC_MOD_SMOKER,
    },
    msg_c.KEY_ECIGARETTE_USAGE: {
        KEY_TYPE: TYPE_CATEGORICAL,
        KEY_ALLOWED_VALUES: list(VALUES_ECIGARETTE_USAGE),
        KEY_DESCRIPTION: DESC_MOD_ECIG,
    },
    msg_c.KEY_ALCOHOL_DRINKERS: {
        KEY_TYPE: TYPE_BOOLEAN,
        KEY_ALLOWED_VALUES: [True, False],
        KEY_DESCRIPTION: DESC_MOD_ALCOHOL,
    },
    msg_c.KEY_CHEST_SCAN: {
        KEY_TYPE: TYPE_BOOLEAN,
        KEY_ALLOWED_VALUES: [True, False],
        KEY_DESCRIPTION: DESC_MOD_CHEST_SCAN,
    },
    msg_c.KEY_HIV_TESTING: {
        KEY_TYPE: TYPE_BOOLEAN,
        KEY_ALLOWED_VALUES: [True, False],
        KEY_DESCRIPTION: DESC_MOD_HIV,
    },
    msg_c.KEY_FLU_VAX_LAST_12: {
        KEY_TYPE: TYPE_BOOLEAN,
        KEY_ALLOWED_VALUES: [True, False],
        KEY_DESCRIPTION: DESC_MOD_FLU,
    },
    msg_c.KEY_PNEUMO_VAX_EVER: {
        KEY_TYPE: TYPE_BOOLEAN,
        KEY_ALLOWED_VALUES: [True, False],
        KEY_DESCRIPTION: DESC_MOD_PNEUMO,
    },
    msg_c.KEY_TETANUS_LAST_10_TDAP: {
        KEY_TYPE: TYPE_CATEGORICAL,
        KEY_ALLOWED_VALUES: list(VALUES_TETANUS_LAST_10_TDAP),
        KEY_DESCRIPTION: DESC_MOD_TETANUS,
    },
    msg_c.KEY_HIGH_RISK_LAST_YEAR: {
        KEY_TYPE: TYPE_BOOLEAN,
        KEY_ALLOWED_VALUES: [True, False],
        KEY_DESCRIPTION: DESC_MOD_HIGH_RISK,
    },
    msg_c.KEY_COVID_POS: {
        KEY_TYPE: TYPE_CATEGORICAL,
        KEY_ALLOWED_VALUES: list(VALUES_COVID_POS),
        KEY_DESCRIPTION: DESC_MOD_COVID,
    },
}

# --- Fixed in what-if (profile + chronic conditions); aligned with simulation rules ---
DESC_FIXED_SEX: Final[str] = "Sexo del perfil; no se modifica en la simulación."
DESC_FIXED_BIRTH_DATE: Final[str] = "Fecha de nacimiento; no se modifica en la simulación."
DESC_FIXED_AGE_CATEGORY: Final[str] = "Franja etaria derivada; no se modifica en la simulación."
DESC_FIXED_HEIGHT: Final[str] = "Altura en metros del perfil; no se modifica en la simulación."
DESC_FIXED_REMOVED_TEETH: Final[str] = "Dientes extraídos (perfil); no se modifica en la simulación."
DESC_FIXED_HAD_ANGINA: Final[str] = "Antecedente de angina; no modificable en simulación."
DESC_FIXED_HAD_STROKE: Final[str] = "Antecedente de accidente cerebrovascular; no modificable en simulación."
DESC_FIXED_HAD_ASTHMA: Final[str] = "Antecedente de asma; no modificable en simulación."
DESC_FIXED_HAD_COPD: Final[str] = "Antecedente de EPOC; no modificable en simulación."
DESC_FIXED_HAD_SKIN_CANCER: Final[str] = "Antecedente de cáncer de piel; no modificable en simulación."
DESC_FIXED_HAD_DEPRESSIVE: Final[str] = (
    "Antecedente de trastorno depresivo; no modificable en simulación."
)
DESC_FIXED_HAD_KIDNEY: Final[str] = "Antecedente de enfermedad renal; no modificable en simulación."
DESC_FIXED_HAD_ARTHRITIS: Final[str] = "Antecedente de artritis; no modificable en simulación."
DESC_FIXED_HAD_DIABETES: Final[str] = "Antecedente de diabetes; no modificable en simulación."
DESC_FIXED_DEAF: Final[str] = "Dificultad auditiva; no modificable en simulación."
DESC_FIXED_BLIND: Final[str] = "Dificultad visual; no modificable en simulación."
DESC_FIXED_CONCENTRATING: Final[str] = "Dificultad para concentrarse; no modificable en simulación."
DESC_FIXED_WALKING: Final[str] = "Dificultad para caminar; no modificable en simulación."
DESC_FIXED_DRESSING: Final[str] = "Dificultad para vestirse o bañarse; no modificable en simulación."
DESC_FIXED_ERRANDS: Final[str] = "Dificultad para hacer mandados sola/o; no modificable en simulación."

FIXED_VARIABLE_ENTRIES: Final[tuple[tuple[str, str], ...]] = (
    (msg_c.KEY_SEX, DESC_FIXED_SEX),
    (msg_c.KEY_BIRTH_DATE, DESC_FIXED_BIRTH_DATE),
    (msg_c.KEY_AGE_CATEGORY, DESC_FIXED_AGE_CATEGORY),
    (msg_c.KEY_HEIGHT_METERS, DESC_FIXED_HEIGHT),
    (msg_c.KEY_REMOVED_TEETH, DESC_FIXED_REMOVED_TEETH),
    (msg_c.KEY_HAD_ANGINA, DESC_FIXED_HAD_ANGINA),
    (msg_c.KEY_HAD_STROKE, DESC_FIXED_HAD_STROKE),
    (msg_c.KEY_HAD_ASTHMA, DESC_FIXED_HAD_ASTHMA),
    (msg_c.KEY_HAD_COPD, DESC_FIXED_HAD_COPD),
    (msg_c.KEY_HAD_SKIN_CANCER, DESC_FIXED_HAD_SKIN_CANCER),
    (msg_c.KEY_HAD_DEPRESSIVE_DISORDER, DESC_FIXED_HAD_DEPRESSIVE),
    (msg_c.KEY_HAD_KIDNEY_DISEASE, DESC_FIXED_HAD_KIDNEY),
    (msg_c.KEY_HAD_ARTHRITIS, DESC_FIXED_HAD_ARTHRITIS),
    (msg_c.KEY_HAD_DIABETES, DESC_FIXED_HAD_DIABETES),
    (msg_c.KEY_DEAF_OR_HARD_OF_HEARING, DESC_FIXED_DEAF),
    (msg_c.KEY_BLIND_OR_VISION_DIFFICULTY, DESC_FIXED_BLIND),
    (msg_c.KEY_DIFFICULTY_CONCENTRATING, DESC_FIXED_CONCENTRATING),
    (msg_c.KEY_DIFFICULTY_WALKING, DESC_FIXED_WALKING),
    (msg_c.KEY_DIFFICULTY_DRESSING_BATHING, DESC_FIXED_DRESSING),
    (msg_c.KEY_DIFFICULTY_ERRANDS, DESC_FIXED_ERRANDS),
)


def assert_modifiable_order_matches_simulation() -> None:
    """Runtime guard: catalog order and prediction simulation allowlist must stay aligned."""
    assert frozenset(MODIFIABLE_FIELDS_ORDER) == pred_c.SIMULATION_ALLOWED_FIELDS
    assert len(MODIFIABLE_FIELDS_ORDER) == len(pred_c.SIMULATION_ALLOWED_FIELDS)


assert_modifiable_order_matches_simulation()
