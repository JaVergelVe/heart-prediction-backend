"""SHAP user-facing copy and feature label maps (aligned with frontend shap-display.constant.ts)."""

from typing import Final

from app.constants import prediction as pred_c
from app.constants import prediction_survey as ps

# Survey / profile labels (Spanish)
_LABEL_GENERAL_HEALTH: Final[str] = "Estado de salud general"
_LABEL_PHYSICAL_HEALTH_DAYS: Final[str] = "Días con mala salud física (último mes)"
_LABEL_MENTAL_HEALTH_DAYS: Final[str] = "Días con mala salud mental (último mes)"
_LABEL_LAST_CHECKUP: Final[str] = "Último chequeo médico"
_LABEL_PHYSICAL_ACTIVITIES: Final[str] = "Actividad física o ejercicio"
_LABEL_SLEEP_HOURS: Final[str] = "Horas de sueño en promedio (24 h)"
_LABEL_SMOKER_STATUS: Final[str] = "Estado de tabaquismo"
_LABEL_ECIGARETTE: Final[str] = "Uso de cigarrillos electrónicos"
_LABEL_ALCOHOL: Final[str] = "Consume alcohol"
_LABEL_CHEST_SCAN: Final[str] = "Alguna vez le hicieron TAC o radiografía de tórax"
_LABEL_HIV: Final[str] = "Se ha hecho prueba de VIH"
_LABEL_FLU_VAX: Final[str] = "Vacuna de gripe en los últimos 12 meses"
_LABEL_PNEUMO_VAX: Final[str] = "Alguna vez vacuna neumocócica"
_LABEL_TETANUS: Final[str] = "Vacuna antitetánica / Tdap en los últimos 10 años"
_LABEL_HIGH_RISK: Final[str] = "Alto riesgo de enfermedad grave el último año"
_LABEL_COVID: Final[str] = "Resultado COVID-19 conocido"
_LABEL_SEX: Final[str] = "Sexo biológico"
_LABEL_BIRTH_DATE: Final[str] = "Fecha de nacimiento"
_LABEL_HEIGHT: Final[str] = "Altura (metros)"
_LABEL_REMOVED_TEETH: Final[str] = "Dientes extraídos"
_LABEL_DIABETES: Final[str] = "Diabetes"
_LABEL_WEIGHT: Final[str] = "Peso (kg)"


def _norm_key(value: str) -> str:
    return value.strip().replace(" ", "_").replace("-", "_").lower()


def _map_labeled_options(options: tuple[tuple[str, str], ...]) -> dict[str, str]:
    return {_norm_key(value): label for value, label in options}


GENERAL_HEALTH_LABELS: Final[dict[str, str]] = _map_labeled_options(
    (
        (ps.GeneralHealth.EXCELLENT.value, "Excelente"),
        (ps.GeneralHealth.VERY_GOOD.value, "Muy buena"),
        (ps.GeneralHealth.GOOD.value, "Buena"),
        (ps.GeneralHealth.FAIR.value, "Regular"),
        (ps.GeneralHealth.POOR.value, "Mala"),
    )
)

SMOKER_STATUS_LABELS: Final[dict[str, str]] = _map_labeled_options(
    (
        (ps.SmokerStatus.NEVER_SMOKED.value, "Nunca fumó"),
        (ps.SmokerStatus.FORMER_SMOKER.value, "Exfumador"),
        (
            ps.SmokerStatus.CURRENT_SOME_DAYS.value,
            "Fumador actual: algunos días",
        ),
        (
            ps.SmokerStatus.CURRENT_EVERY_DAY.value,
            "Fumador actual: todos los días",
        ),
    )
)

ECIGARETTE_USAGE_LABELS: Final[dict[str, str]] = _map_labeled_options(
    (
        (ps.EcigaretteUsage.NEVER_USED_LIFE.value, "Nunca ha usado cigarrillos electrónicos"),
        (ps.EcigaretteUsage.NOT_AT_ALL_NOW.value, "Ahora mismo: no usa"),
        (ps.EcigaretteUsage.SOME_DAYS.value, "Algunos días"),
        (ps.EcigaretteUsage.EVERY_DAY.value, "Todos los días"),
    )
)

LAST_CHECKUP_LABELS: Final[dict[str, str]] = _map_labeled_options(
    (
        (
            ps.LastCheckupTime.WITHIN_PAST_YEAR.value,
            "En el último año (menos de 12 meses)",
        ),
        (
            ps.LastCheckupTime.WITHIN_PAST_2_YEARS.value,
            "Entre 1 y 2 años",
        ),
        (
            ps.LastCheckupTime.WITHIN_PAST_5_YEARS.value,
            "Entre 2 y 5 años",
        ),
        (ps.LastCheckupTime.FIVE_OR_MORE_YEARS_AGO.value, "Hace 5 años o más"),
        (ps.LastCheckupTime.NEVER.value, "Nunca"),
    )
)

TETANUS_LABELS: Final[dict[str, str]] = _map_labeled_options(
    (
        (ps.TetanusLast10Tdap.YES_TDAP.value, "Sí, recibió Tdap"),
        (
            ps.TetanusLast10Tdap.YES_TETANUS_UNKNOWN_TYPE.value,
            "Sí, vacuna antitetánica (tipo no seguro)",
        ),
        (
            ps.TetanusLast10Tdap.YES_TETANUS_NOT_TDAP.value,
            "Sí, antitetánica pero no Tdap",
        ),
        (
            ps.TetanusLast10Tdap.NO_NOT_IN_10_YEARS.value,
            "No, ninguna en los últimos 10 años",
        ),
    )
)

COVID_POS_LABELS: Final[dict[str, str]] = _map_labeled_options(
    (
        (ps.CovidPos.YES.value, "Sí"),
        (ps.CovidPos.NO.value, "No"),
        (
            ps.CovidPos.HOME_TEST_POSITIVE.value,
            "Positivo en autotest en casa (sin profesional)",
        ),
    )
)

SHAP_COMPOUND_VALUE_LABELS: Final[dict[str, dict[str, str]]] = {
    "generalhealth": GENERAL_HEALTH_LABELS,
    "smokerstatus": SMOKER_STATUS_LABELS,
    "ecigaretteusage": ECIGARETTE_USAGE_LABELS,
    "lastcheckuptime": LAST_CHECKUP_LABELS,
    "tetanuslast10tdap": TETANUS_LABELS,
    "covidpos": COVID_POS_LABELS,
}

SHAP_COMPOUND_CATEGORY_PREFIX: Final[dict[str, str]] = {
    "generalhealth": _LABEL_GENERAL_HEALTH,
    "physicalhealthdays": _LABEL_PHYSICAL_HEALTH_DAYS,
    "mentalhealthdays": _LABEL_MENTAL_HEALTH_DAYS,
    "lastcheckuptime": _LABEL_LAST_CHECKUP,
    "physicalactivities": _LABEL_PHYSICAL_ACTIVITIES,
    "sleephours": _LABEL_SLEEP_HOURS,
    "smokerstatus": _LABEL_SMOKER_STATUS,
    "ecigaretteusage": _LABEL_ECIGARETTE,
    "alcoholdrinkers": _LABEL_ALCOHOL,
    "chestscan": _LABEL_CHEST_SCAN,
    "hivtesting": _LABEL_HIV,
    "fluvaxlast12": _LABEL_FLU_VAX,
    "pneumovaxever": _LABEL_PNEUMO_VAX,
    "tetanuslast10tdap": _LABEL_TETANUS,
    "highrisklastyear": _LABEL_HIGH_RISK,
    "covidpos": _LABEL_COVID,
    "agecategory": "Grupo de edad",
    "sex": _LABEL_SEX,
    "removedteeth": _LABEL_REMOVED_TEETH,
    "haddiabetes": _LABEL_DIABETES,
    "bmi": "Índice de masa corporal (IMC)",
    "weightkilograms": _LABEL_WEIGHT,
    "heightmeters": _LABEL_HEIGHT,
    "birthdate": _LABEL_BIRTH_DATE,
}

SHAP_FEATURE_TITLE_MAP: Final[dict[str, str]] = {
    "had_angina": "Antecedentes de angina",
    "hadangina": "Antecedentes de angina",
    "had_stroke": "Antecedentes de accidente cerebrovascular",
    "hadstroke": "Antecedentes de accidente cerebrovascular",
    "had_asthma": "Antecedentes de asma",
    "hadasthma": "Antecedentes de asma",
    "had_copd": "Antecedentes de EPOC",
    "hadcopd": "Antecedentes de EPOC",
    "had_skin_cancer": "Antecedentes de cáncer de piel",
    "hadskincancer": "Antecedentes de cáncer de piel",
    "had_depressive_disorder": "Antecedentes de trastorno depresivo",
    "haddepressivedisorder": "Antecedentes de trastorno depresivo",
    "had_kidney_disease": "Antecedentes de enfermedad renal",
    "hadkidneydisease": "Antecedentes de enfermedad renal",
    "had_arthritis": "Antecedentes de artritis",
    "hadarthritis": "Antecedentes de artritis",
    "deaf_or_hard_of_hearing": "Sordera o dificultad auditiva",
    "deaforhardofhearing": "Sordera o dificultad auditiva",
    "blind_or_vision_difficulty": "Ceguera o dificultad visual",
    "blindorvisiondifficulty": "Ceguera o dificultad visual",
    "difficulty_concentrating": "Dificultad para concentrarse",
    "difficultyconcentrating": "Dificultad para concentrarse",
    "difficulty_walking": "Dificultad para caminar",
    "difficultywalking": "Dificultad para caminar",
    "difficulty_dressing_bathing": "Dificultad para vestirse o bañarse",
    "difficultydressingbathing": "Dificultad para vestirse o bañarse",
    "difficulty_errands": "Dificultad para hacer recados",
    "difficultyerrands": "Dificultad para hacer recados",
    "general_health": _LABEL_GENERAL_HEALTH,
    "generalhealth": _LABEL_GENERAL_HEALTH,
    "physical_health_days": _LABEL_PHYSICAL_HEALTH_DAYS,
    "physicalhealthdays": _LABEL_PHYSICAL_HEALTH_DAYS,
    "mental_health_days": _LABEL_MENTAL_HEALTH_DAYS,
    "mentalhealthdays": _LABEL_MENTAL_HEALTH_DAYS,
    "last_checkup_time": _LABEL_LAST_CHECKUP,
    "lastcheckuptime": _LABEL_LAST_CHECKUP,
    "physical_activities": _LABEL_PHYSICAL_ACTIVITIES,
    "physicalactivities": _LABEL_PHYSICAL_ACTIVITIES,
    "sleep_hours": _LABEL_SLEEP_HOURS,
    "sleephours": _LABEL_SLEEP_HOURS,
    "smoker_status": _LABEL_SMOKER_STATUS,
    "smokerstatus": _LABEL_SMOKER_STATUS,
    "ecigarette_usage": _LABEL_ECIGARETTE,
    "ecigaretteusage": _LABEL_ECIGARETTE,
    "alcohol_drinkers": _LABEL_ALCOHOL,
    "alcoholdrinkers": _LABEL_ALCOHOL,
    "chest_scan": _LABEL_CHEST_SCAN,
    "chestscan": _LABEL_CHEST_SCAN,
    "hiv_testing": _LABEL_HIV,
    "hivtesting": _LABEL_HIV,
    "flu_vax_last_12": _LABEL_FLU_VAX,
    "fluvaxlast12": _LABEL_FLU_VAX,
    "pneumo_vax_ever": _LABEL_PNEUMO_VAX,
    "pneumovaxever": _LABEL_PNEUMO_VAX,
    "tetanus_last_10_tdap": _LABEL_TETANUS,
    "tetanuslast10tdap": _LABEL_TETANUS,
    "high_risk_last_year": _LABEL_HIGH_RISK,
    "highrisklastyear": _LABEL_HIGH_RISK,
    "covid_pos": _LABEL_COVID,
    "covidpos": _LABEL_COVID,
    "weight_kilograms": _LABEL_WEIGHT,
    "weightkilograms": _LABEL_WEIGHT,
    "bmi": "Índice de masa corporal (IMC)",
    "sex": _LABEL_SEX,
    "birth_date": _LABEL_BIRTH_DATE,
    "birthdate": _LABEL_BIRTH_DATE,
    "height_meters": _LABEL_HEIGHT,
    "heightmeters": _LABEL_HEIGHT,
    "removed_teeth": _LABEL_REMOVED_TEETH,
    "removedteeth": _LABEL_REMOVED_TEETH,
    "had_diabetes": _LABEL_DIABETES,
    "haddiabetes": _LABEL_DIABETES,
    "age_category": "Grupo de edad",
    "agecategory": "Grupo de edad",
    "prediction_probability": "Probabilidad estimada por el modelo",
    "risk_level": "Nivel de riesgo informado",
}

SHAP_DIRECTION_TO_KIND: Final[dict[str, str]] = {
    "increases_risk": "increase",
    "increase_risk": "increase",
    "increased_risk": "increase",
    "increase": "increase",
    "higher_risk": "increase",
    "higher": "increase",
    "positive": "increase",
    "pos": "increase",
    "up": "increase",
    "decreases_risk": "decrease",
    "decrease_risk": "decrease",
    "decreased_risk": "decrease",
    "decrease": "decrease",
    "lower_risk": "decrease",
    "lower": "decrease",
    "negative": "decrease",
    "neg": "decrease",
    "down": "decrease",
    "neutral": "neutral",
    "no_effect": "neutral",
    "none": "neutral",
    "unchanged": "neutral",
}

SHAP_BOOLEAN_VALUE_LABELS: Final[dict[str, str]] = {
    "true": "Sí",
    "false": "No",
    "1": "Sí",
    "0": "No",
    "yes": "Sí",
    "no": "No",
}

SHAP_AGE_CATEGORY_SUFFIX_LABELS: Final[dict[str, str]] = {
    "age_18_to_24": "De 18 a 24 años",
    "age_25_to_29": "De 25 a 29 años",
    "age_30_to_34": "De 30 a 34 años",
    "age_35_to_39": "De 35 a 39 años",
    "age_40_to_44": "De 40 a 44 años",
    "age_45_to_49": "De 45 a 49 años",
    "age_50_to_54": "De 50 a 54 años",
    "age_55_to_59": "De 55 a 59 años",
    "age_60_to_64": "De 60 a 64 años",
    "age_65_to_69": "De 65 a 69 años",
    "age_70_to_74": "De 70 a 74 años",
    "age_75_to_79": "De 75 a 79 años",
    "age_80_or_older": "80 años o más",
    "age_18_24": "De 18 a 24 años",
    "age_25_29": "De 25 a 29 años",
    "age_30_34": "De 30 a 34 años",
    "age_35_39": "De 35 a 39 años",
    "age_40_44": "De 40 a 44 años",
    "age_45_49": "De 45 a 49 años",
    "age_50_54": "De 50 a 54 años",
    "age_55_59": "De 55 a 59 años",
    "age_60_64": "De 60 a 64 años",
    "age_65_69": "De 65 a 69 años",
    "age_70_74": "De 70 a 74 años",
    "age_75_79": "De 75 a 79 años",
}

SHAP_INTENSITY_RELATIVE_THRESHOLDS: Final[dict[str, float]] = {
    "high": 0.66,
    "medium": 0.33,
}

SHAP_BMI_ELEVATED_THRESHOLD: Final[float] = 25.0

SHAP_DISPLAY_UI: Final[dict[str, str | tuple[str, ...] | dict[str, str]]] = {
    "fallbackUnknownFeature": "Factor de salud",
    "impactIncrease": "Aumenta el riesgo",
    "impactDecrease": "Disminuye el riesgo",
    "impactNeutral": "Efecto neutro",
    "impactUnknown": "Impacto no clasificado",
    "intensityHigh": "Intensidad: alta",
    "intensityMedium": "Intensidad: media",
    "intensityLow": "Intensidad: baja",
    "sectionDisclaimer": (
        "Estas explicaciones indican qué variables influyeron más en la estimación del modelo. "
        "No constituyen un diagnóstico médico."
    ),
    "explanationIncrease": "Este factor se asoció con un aumento del riesgo estimado.",
    "explanationDecrease": "Este factor se asoció con una reducción del riesgo estimado.",
    "explanationNeutral": (
        "Este factor tuvo un efecto moderado o equilibrado en la estimación. "
        "El resultado depende del conjunto de tus respuestas."
    ),
    "moreContextHeading": "Más detalle",
    "technicalInterpretationHints": (
        "input vector",
        "feature vector",
        "vector de entrada",
        "vector del modelo",
        "vector de entrada del modelo",
        "shap value",
        "valor shap",
        "model input",
        "increases_risk",
        "decreases_risk",
        "increase_risk",
        "decrease_risk",
        "clase positiva",
        "positive class",
        "empuja",
        "empuja la estimación",
        "probabilidad hacia",
        "numpy",
        "tensor",
        "baseline",
        "rango 1:",
        "rango 2:",
        "valor en el vector",
        "no es un diagnóstico",
        "no constituyen un diagnóstico",
    ),
}

RISK_LEVEL_DISPLAY_LABELS: Final[dict[str, str]] = {
    pred_c.RISK_LEVEL_LOW: "Bajo",
    pred_c.RISK_LEVEL_MEDIUM: "Medio",
    pred_c.RISK_LEVEL_HIGH: "Alto",
}
