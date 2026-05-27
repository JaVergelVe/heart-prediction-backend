"""PDF export: labels, disclaimer, filename pattern, and HTTP metadata."""

from typing import Final

from app.constants import messages as msg_c

# --- HTTP ---
PDF_MEDIA_TYPE: Final[str] = "application/pdf"
CONTENT_DISPOSITION_ATTACHMENT: Final[str] = 'attachment; filename="{filename}"'
OPENAPI_RESPONSE_200_DESCRIPTION: Final[str] = "PDF file download"

# --- Filename (clear, filesystem-safe) ---
FILENAME_PREFIX: Final[str] = "heart-risk-prediction"
FILENAME_TIMESTAMP_UNKNOWN: Final[str] = "unknown-timestamp"
FILENAME_TEMPLATE: Final[str] = "{prefix}_{prediction_id}_{timestamp}.pdf"
FILENAME_INVALID_CHARS: Final[str] = '<>:"/\\|?*'
FILENAME_SPACE_REPLACEMENT: Final[str] = "_"
FILENAME_TIMESTAMP_MAX_LEN: Final[int] = 180

# --- ReportLab layout (simple, fixed) ---
PDF_PAGE_MARGIN_INCHES: Final[float] = 0.75
PDF_TITLE_BOTTOM_SPACER_INCHES: Final[float] = 0.1
PDF_FONT_TITLE: Final[int] = 14
PDF_FONT_TITLE_LEADING: Final[int] = 18
PDF_FONT_TITLE_SPACE_AFTER: Final[int] = 14
PDF_FONT_H2: Final[int] = 12
PDF_FONT_H2_LEADING: Final[int] = 15
PDF_FONT_H2_SPACE_BEFORE: Final[int] = 10
PDF_FONT_H2_SPACE_AFTER: Final[int] = 8
PDF_FONT_BODY: Final[int] = 10
PDF_FONT_BODY_LEADING: Final[int] = 16
PDF_FONT_BODY_SPACE_AFTER: Final[int] = 10
PDF_FONT_DISCLAIMER: Final[int] = 9
PDF_FONT_DISCLAIMER_LEADING: Final[int] = 14
PDF_FONT_DISCLAIMER_SPACE_AFTER: Final[int] = 10
PDF_PARAGRAPH_STYLE_NAME_TITLE: Final[str] = "pdf_title"
PDF_PARAGRAPH_STYLE_NAME_H2: Final[str] = "pdf_h2"
PDF_PARAGRAPH_STYLE_NAME_BODY: Final[str] = "pdf_body"
PDF_PARAGRAPH_STYLE_NAME_SMALL: Final[str] = "pdf_small"

# --- Line / value templates ---
PDF_LINE_LABEL_VALUE: Final[str] = "{label}: {value}"
PDF_LINE_PROBABILITY: Final[str] = "{label}: {value}{unit}"
PDF_LINE_RECOMMENDATION_ITEM: Final[str] = "{index}. {text}"
PDF_FLOAT_ZERO_DISPLAY: Final[str] = "0"
PDF_FLOAT_DECIMALS: Final[int] = 4
PDF_FLOAT_RSTRIP_TRAILING_ZERO: Final[str] = "0"
PDF_FLOAT_RSTRIP_TRAILING_DOT: Final[str] = "."
PDF_PROBABILITY_DECIMALS: Final[int] = 2

# --- Document ---
PDF_TITLE: Final[str] = "Informe de predicción de riesgo cardiovascular"
PDF_SECTION_SUMMARY: Final[str] = "Resumen"
PDF_SECTION_INPUT_DATA: Final[str] = "Datos de entrada relevantes"
PDF_SECTION_SHAP: Final[str] = "Factores que influyeron en la estimación"
PDF_SECTION_SHAP_MAIN: Final[str] = "Factor con mayor influencia"
PDF_SECTION_SHAP_FACTORS: Final[str] = "Otros factores destacados"
PDF_SECTION_RECOMMENDATIONS: Final[str] = "Recomendaciones"
PDF_RECOMMENDATIONS_EMPTY: Final[str] = "No hay recomendaciones generadas para este resultado."
PDF_SECTION_DISCLAIMER: Final[str] = "Aviso legal"

PDF_LABEL_PROBABILITY: Final[str] = "Probabilidad estimada"
PDF_LABEL_RISK_LEVEL: Final[str] = "Nivel de riesgo"
PDF_LABEL_PREDICTION_TIMESTAMP: Final[str] = "Fecha y hora de la predicción"

PDF_LABEL_SHAP_IMPACT: Final[str] = "Impacto"
PDF_LABEL_SHAP_MORE_DETAIL: Final[str] = "Más detalle"
PDF_SHAP_NOT_AVAILABLE: Final[str] = (
    "No se pudo incluir la explicación de factores (perfil incompleto o datos insuficientes)."
)

PDF_LINE_SHAP_FACTOR_RANK: Final[str] = "#{rank} {title}"

PDF_VALUE_NOT_AVAILABLE: Final[str] = "—"
PDF_VALUE_YES: Final[str] = "Sí"
PDF_VALUE_NO: Final[str] = "No"

PDF_PROBABILITY_UNIT: Final[str] = "%"

# --- Input field labels (aligned with prediction detail keys) ---
PDF_LABEL_INPUT_WEIGHT_KG: Final[str] = "Peso (kg)"
PDF_LABEL_INPUT_BMI: Final[str] = "IMC"
PDF_LABEL_INPUT_GENERAL_HEALTH: Final[str] = "Salud general"
PDF_LABEL_INPUT_PHYSICAL_HEALTH_DAYS: Final[str] = (
    "Días con salud física no óptima (último mes)"
)
PDF_LABEL_INPUT_MENTAL_HEALTH_DAYS: Final[str] = (
    "Días con salud mental no óptima (último mes)"
)
PDF_LABEL_INPUT_LAST_CHECKUP: Final[str] = "Último chequeo médico"
PDF_LABEL_INPUT_PHYSICAL_ACTIVITIES: Final[str] = "Actividad física"
PDF_LABEL_INPUT_SLEEP_HOURS: Final[str] = "Horas de sueño (promedio)"
PDF_LABEL_INPUT_SMOKER_STATUS: Final[str] = "Estado de tabaquismo"
PDF_LABEL_INPUT_ECIGARETTE: Final[str] = "Uso de cigarrillo electrónico"
PDF_LABEL_INPUT_ALCOHOL: Final[str] = "Consumo de alcohol"
PDF_LABEL_INPUT_CHEST_SCAN: Final[str] = "Estudio de tórax (CT)"
PDF_LABEL_INPUT_HIV: Final[str] = "Prueba de VIH"
PDF_LABEL_INPUT_FLU_VAX: Final[str] = "Vacuna contra la gripe (últimos 12 meses)"
PDF_LABEL_INPUT_PNEUMO_VAX: Final[str] = "Vacuna neumocócica (alguna vez)"
PDF_LABEL_INPUT_TETANUS: Final[str] = "Vacuna Tdap / tétanos (últimos 10 años)"
PDF_LABEL_INPUT_HIGH_RISK_YEAR: Final[str] = "Alto riesgo de enfermedad (último año)"
PDF_LABEL_INPUT_COVID: Final[str] = "COVID-19 positivo (autorreporte)"

PDF_SURVEY_VALUE_LABELS: Final[dict[str, dict[str, str]]] = {
    msg_c.KEY_GENERAL_HEALTH: {
        "Excellent": "Excelente",
        "Very good": "Muy buena",
        "Good": "Buena",
        "Fair": "Regular",
        "Poor": "Mala",
    },
    msg_c.KEY_LAST_CHECKUP_TIME: {
        "Within past year (anytime less than 12 months ago)": "En el último año (menos de 12 meses)",
        "Within past 2 years (1 year but less than 2 years ago)": "Entre 1 y 2 años",
        "Within past 5 years (2 years but less than 5 years ago)": "Entre 2 y 5 años",
        "5 or more years ago": "Hace 5 años o más",
        "Never": "Nunca",
    },
    msg_c.KEY_SMOKER_STATUS: {
        "Never smoked": "Nunca fumó",
        "Former smoker": "Exfumador",
        "Current smoker - now smokes some days": "Fumador actual: algunos días",
        "Current smoker - now smokes every day": "Fumador actual: todos los días",
    },
    msg_c.KEY_ECIGARETTE_USAGE: {
        "Never used e-cigarettes in my entire life": "Nunca ha usado cigarrillos electrónicos",
        "Not at all (right now)": "Ahora mismo: no usa",
        "Use them some days": "Algunos días",
        "Use them every day": "Todos los días",
    },
    msg_c.KEY_TETANUS_LAST_10_TDAP: {
        "Yes, received Tdap": "Sí, recibió Tdap",
        "Yes, received tetanus shot but not sure what type": "Sí, vacuna antitetánica (tipo no seguro)",
        "Yes, received tetanus shot, but not Tdap": "Sí, antitetánica pero no Tdap",
        "No, did not receive any tetanus shot in the past 10 years": "No, ninguna en los últimos 10 años",
    },
    msg_c.KEY_COVID_POS: {
        "Yes": "Sí",
        "No": "No",
        "Tested positive using home test without a health professional": (
            "Positivo en autotest en casa (sin profesional)"
        ),
    },
}

PDF_INPUT_FIELDS: Final[tuple[tuple[str, str], ...]] = (
    (msg_c.KEY_WEIGHT_KILOGRAMS, PDF_LABEL_INPUT_WEIGHT_KG),
    (msg_c.KEY_BMI, PDF_LABEL_INPUT_BMI),
    (msg_c.KEY_GENERAL_HEALTH, PDF_LABEL_INPUT_GENERAL_HEALTH),
    (msg_c.KEY_PHYSICAL_HEALTH_DAYS, PDF_LABEL_INPUT_PHYSICAL_HEALTH_DAYS),
    (msg_c.KEY_MENTAL_HEALTH_DAYS, PDF_LABEL_INPUT_MENTAL_HEALTH_DAYS),
    (msg_c.KEY_LAST_CHECKUP_TIME, PDF_LABEL_INPUT_LAST_CHECKUP),
    (msg_c.KEY_PHYSICAL_ACTIVITIES, PDF_LABEL_INPUT_PHYSICAL_ACTIVITIES),
    (msg_c.KEY_SLEEP_HOURS, PDF_LABEL_INPUT_SLEEP_HOURS),
    (msg_c.KEY_SMOKER_STATUS, PDF_LABEL_INPUT_SMOKER_STATUS),
    (msg_c.KEY_ECIGARETTE_USAGE, PDF_LABEL_INPUT_ECIGARETTE),
    (msg_c.KEY_ALCOHOL_DRINKERS, PDF_LABEL_INPUT_ALCOHOL),
    (msg_c.KEY_CHEST_SCAN, PDF_LABEL_INPUT_CHEST_SCAN),
    (msg_c.KEY_HIV_TESTING, PDF_LABEL_INPUT_HIV),
    (msg_c.KEY_FLU_VAX_LAST_12, PDF_LABEL_INPUT_FLU_VAX),
    (msg_c.KEY_PNEUMO_VAX_EVER, PDF_LABEL_INPUT_PNEUMO_VAX),
    (msg_c.KEY_TETANUS_LAST_10_TDAP, PDF_LABEL_INPUT_TETANUS),
    (msg_c.KEY_HIGH_RISK_LAST_YEAR, PDF_LABEL_INPUT_HIGH_RISK_YEAR),
    (msg_c.KEY_COVID_POS, PDF_LABEL_INPUT_COVID),
)

PDF_DISCLAIMER_PARAGRAPH_1: Final[str] = (
    "Este documento es generado automáticamente con fines informativos y educativos. "
    "No constituye diagnóstico médico, consejo clínico ni sustituye la evaluación "
    "de un profesional de la salud."
)
PDF_DISCLAIMER_PARAGRAPH_2: Final[str] = (
    "Los resultados se basan en un modelo estadístico y en los datos proporcionados; "
    "pueden ser incompletos o estar sujetos a error. Ante síntomas, antecedentes "
    "personales o dudas sobre su salud cardiovascular, consulte a su médico."
)

PDF_DISCLAIMER_PARAGRAPHS: Final[tuple[str, ...]] = (
    PDF_DISCLAIMER_PARAGRAPH_1,
    PDF_DISCLAIMER_PARAGRAPH_2,
)
