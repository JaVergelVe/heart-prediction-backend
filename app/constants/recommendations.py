"""Thresholds and user-facing recommendation strings for prediction responses."""

from typing import Final

# --- Output limits ---
RECOMMENDATIONS_MAX_ITEMS: Final[int] = 8

# --- Lifestyle thresholds (aligned with clinical-style guidance; not diagnosis) ---
SLEEP_HOURS_LOW_THRESHOLD: Final[float] = 6.0
BMI_OVERWEIGHT_MIN: Final[float] = 25.0

# --- Risk-level anchors ---
MSG_REC_HIGH_RISK_MEDICAL: Final[str] = (
    "Su nivel de riesgo es alto. Consulte pronto a un profesional de salud para evaluación "
    "cardiovascular y seguimiento personalizado."
)
MSG_REC_MEDIUM_RISK_MONITOR: Final[str] = (
    "Su riesgo es moderado. Mantenga controles periódicos y comente estos resultados con su médico."
)
MSG_REC_LOW_RISK_MAINTAIN: Final[str] = (
    "Su riesgo estimado es bajo. Mantenga hábitos saludables y chequeos de rutina."
)

# --- Lifestyle (survey-driven) ---
MSG_REC_SLEEP_IMPROVE: Final[str] = (
    "Duerme menos de 6 horas en promedio: intente regular el sueño (7–9 h) y una hora de acostarse fija."
)
MSG_REC_EXERCISE: Final[str] = (
    "No reporta actividad física regular: incorpore movimiento moderado la mayoría de los días "
    "(caminar, bicicleta o similar), según su médico."
)
MSG_REC_QUIT_SMOKING: Final[str] = (
    "Fumar aumenta el riesgo cardiovascular: considere un plan para dejar de fumar con apoyo profesional."
)
MSG_REC_REDUCE_ECIG: Final[str] = (
    "Uso de cigarrillos electrónicos: considere reducir o dejar el consumo y consultar sobre opciones seguras."
)
MSG_REC_GENERAL_HEALTH_FAIR_POOR: Final[str] = (
    "Reporta salud general regular o mala: valore seguimiento médico y hábitos (dieta, sueño, actividad)."
)
MSG_REC_CHECKUP_OVERDUE: Final[str] = (
    "Hace tiempo sin chequeo médico: programe una evaluación preventiva."
)
MSG_REC_WEIGHT_BMI_ELEVATED: Final[str] = (
    "Su IMC está en sobrepeso u obesidad: un plan nutricional y de actividad puede ayudar; consúltelo con su médico."
)
MSG_REC_ALCOHOL_LIMIT: Final[str] = (
    "Consumo de alcohol reportado: discuta límites seguros con su profesional de salud."
)

# --- SHAP feature_name hints (substring match on model feature labels) ---
MSG_REC_SHAP_BMI: Final[str] = (
    "El modelo destaca el IMC: priorizar peso saludable con orientación médica y nutricional."
)
MSG_REC_SHAP_GENERAL_HEALTH: Final[str] = (
    "El modelo destaca la salud general: mejorar hábitos diarios y controles puede ser beneficioso."
)
MSG_REC_SHAP_SMOKING: Final[str] = (
    "El modelo destaca el tabaquismo: dejar de fumar es una de las medidas más efectivas para el corazón."
)
MSG_REC_SHAP_SLEEP: Final[str] = (
    "El modelo destaca el sueño: mejorar la higiene del sueño puede apoyar su salud cardiovascular."
)
MSG_REC_SHAP_ACTIVITY: Final[str] = (
    "El modelo destaca la actividad física: incrementar el movimiento regular suele reducir el riesgo."
)
