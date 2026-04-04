"""PDF export: labels, disclaimer, filename pattern, and HTTP metadata."""

from typing import Final

from app.constants import messages as msg_c

# --- HTTP ---
PDF_MEDIA_TYPE: Final[str] = "application/pdf"
CONTENT_DISPOSITION_ATTACHMENT: Final[str] = 'attachment; filename="{filename}"'

# --- Filename (clear, filesystem-safe) ---
FILENAME_PREFIX: Final[str] = "heart-risk-prediction"
FILENAME_TIMESTAMP_UNKNOWN: Final[str] = "unknown-timestamp"
FILENAME_TEMPLATE: Final[str] = "{prefix}_{prediction_id}_{timestamp}.pdf"

# --- Document ---
PDF_TITLE: Final[str] = "Informe de predicción de riesgo cardiovascular"
PDF_SECTION_SUMMARY: Final[str] = "Resumen"
PDF_SECTION_INPUT_DATA: Final[str] = "Datos de entrada relevantes"
PDF_SECTION_SHAP: Final[str] = "Explicación SHAP (principal)"
PDF_SECTION_RECOMMENDATIONS: Final[str] = "Recomendaciones"
PDF_RECOMMENDATIONS_EMPTY: Final[str] = "No hay recomendaciones generadas para este resultado."
PDF_SECTION_DISCLAIMER: Final[str] = "Aviso legal"

PDF_LABEL_PROBABILITY: Final[str] = "Probabilidad estimada"
PDF_LABEL_RISK_LEVEL: Final[str] = "Nivel de riesgo"
PDF_LABEL_PREDICTION_TIMESTAMP: Final[str] = "Fecha y hora de la predicción"

PDF_LABEL_SHAP_FEATURE: Final[str] = "Variable con mayor impacto"
PDF_LABEL_SHAP_IMPACT: Final[str] = "Magnitud del impacto (valor absoluto)"
PDF_LABEL_SHAP_DIRECTION: Final[str] = "Dirección respecto al riesgo"
PDF_LABEL_SHAP_MESSAGE: Final[str] = "Mensaje"
PDF_SHAP_NOT_AVAILABLE: Final[str] = (
    "No se pudo incluir la explicación SHAP (perfil incompleto o datos insuficientes)."
)

PDF_VALUE_NOT_AVAILABLE: Final[str] = "—"
PDF_VALUE_YES: Final[str] = "Sí"
PDF_VALUE_NO: Final[str] = "No"

PDF_PROBABILITY_UNIT: Final[str] = "%"

# --- Input field labels (aligned with prediction detail keys) ---
PDF_INPUT_FIELDS: Final[tuple[tuple[str, str], ...]] = (
    (msg_c.KEY_WEIGHT_KILOGRAMS, "Peso (kg)"),
    (msg_c.KEY_BMI, "IMC"),
    (msg_c.KEY_GENERAL_HEALTH, "Salud general"),
    (msg_c.KEY_PHYSICAL_HEALTH_DAYS, "Días con salud física no óptima (último mes)"),
    (msg_c.KEY_MENTAL_HEALTH_DAYS, "Días con salud mental no óptima (último mes)"),
    (msg_c.KEY_LAST_CHECKUP_TIME, "Último chequeo médico"),
    (msg_c.KEY_PHYSICAL_ACTIVITIES, "Actividad física"),
    (msg_c.KEY_SLEEP_HOURS, "Horas de sueño (promedio)"),
    (msg_c.KEY_SMOKER_STATUS, "Estado de tabaquismo"),
    (msg_c.KEY_ECIGARETTE_USAGE, "Uso de cigarrillo electrónico"),
    (msg_c.KEY_ALCOHOL_DRINKERS, "Consumo de alcohol"),
    (msg_c.KEY_CHEST_SCAN, "Estudio de tórax (CT)"),
    (msg_c.KEY_HIV_TESTING, "Prueba de VIH"),
    (msg_c.KEY_FLU_VAX_LAST_12, "Vacuna contra la gripe (últimos 12 meses)"),
    (msg_c.KEY_PNEUMO_VAX_EVER, "Vacuna neumocócica (alguna vez)"),
    (msg_c.KEY_TETANUS_LAST_10_TDAP, "Vacuna Tdap / tétanos (últimos 10 años)"),
    (msg_c.KEY_HIGH_RISK_LAST_YEAR, "Alto riesgo de enfermedad (último año)"),
    (msg_c.KEY_COVID_POS, "COVID-19 positivo (autorreporte)"),
)

PDF_DISCLAIMER_PARAGRAPHS: Final[tuple[str, ...]] = (
    (
        "Este documento es generado automáticamente con fines informativos y educativos. "
        "No constituye diagnóstico médico, consejo clínico ni sustituye la evaluación "
        "de un profesional de la salud."
    ),
    (
        "Los resultados se basan en un modelo estadístico y en los datos proporcionados; "
        "pueden ser incompletos o estar sujetos a error. Ante síntomas, antecedentes "
        "personales o dudas sobre su salud cardiovascular, consulte a su médico."
    ),
)
