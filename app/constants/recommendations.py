"""Rule-based heart-risk recommendation labels, thresholds, and copy."""

from typing import Final

# --- Limits ---
RECOMMENDATION_MAX_ITEMS: Final[int] = 5

# --- WHO-style BMI cutoffs (modifiable risk messaging) ---
BMI_OVERWEIGHT_MIN: Final[float] = 25.0
BMI_OBESE_MIN: Final[float] = 30.0

# --- Sleep (hours/night): flag short sleep only if value is present and > 0 ---
SLEEP_HOURS_SHORT_BELOW: Final[float] = 7.0

# --- Response item: category values (aligned with docs/api-contracts examples) ---
REC_CATEGORY_MEDICAL: Final[str] = "Medical Consultation"
REC_CATEGORY_LIFESTYLE: Final[str] = "Lifestyle"
REC_CATEGORY_NUTRITION: Final[str] = "Nutrition"
REC_CATEGORY_PHYSICAL_ACTIVITY: Final[str] = "Physical Activity"
REC_CATEGORY_SLEEP: Final[str] = "Sleep"
REC_CATEGORY_PREVENTIVE: Final[str] = "Preventive Care"
REC_CATEGORY_SUBSTANCE_USE: Final[str] = "Substance Use"

# --- Rule text (Spanish; deterministic, non-clinical guidance) ---
TEXT_RISK_HIGH: Final[str] = (
    "Su nivel de riesgo estimado es alto. Consulte pronto a un profesional de salud "
    "para una evaluación cardiovascular y un plan personalizado."
)
TEXT_RISK_MEDIUM: Final[str] = (
    "Su nivel de riesgo estimado es moderado. Conviene revisar hábitos con un "
    "profesional de salud y seguimiento periódico."
)
TEXT_RISK_LOW: Final[str] = (
    "Su nivel de riesgo estimado es bajo. Mantenga hábitos saludables y controles de rutina."
)
TEXT_RISK_UNKNOWN: Final[str] = (
    "Revise periódicamente su salud cardiovascular con un profesional de salud."
)

TEXT_SMOKING: Final[str] = (
    "Dejar de fumar o reducir el tabaco es una de las medidas más efectivas para "
    "proteger el corazón; busque apoyo médico para un plan de cesación."
)
TEXT_ECIGARETTE: Final[str] = (
    "Reducir o eliminar el uso de cigarrillos electrónicos puede beneficiar su salud "
    "cardiovascular; consulte opciones con su equipo de salud."
)
TEXT_WEIGHT_OBESE: Final[str] = (
    "Un IMC elevado aumenta la carga cardiovascular. Un plan de alimentación y actividad "
    "física supervisado puede ayudar a reducir peso de forma segura."
)
TEXT_WEIGHT_OVERWEIGHT: Final[str] = (
    "Un IMC en sobrepeso puede contribuir al riesgo. Pequeños cambios sostenibles en dieta "
    "y ejercicio suelen ayudar; considere orientación profesional."
)
TEXT_SEDENTARY: Final[str] = (
    "Aumentar gradualmente la actividad física regular (según su médico) mejora la salud "
    "cardiovascular y el control de peso."
)
TEXT_SHORT_SLEEP: Final[str] = (
    "Dormir poco se asocia a peor salud cardiovascular. Intente higiene del sueño y "
    "coméntelo con un profesional si persiste el insomnio."
)
TEXT_ALCOHOL: Final[str] = (
    "Si consume alcohol, moderar la ingesta puede reducir factores de riesgo; "
    "siga las indicaciones de su equipo de salud."
)
TEXT_GENERAL_HEALTH_POOR: Final[str] = (
    "Un estado de salud general débil merece atención: coordine una evaluación para "
    "identificar causas tratables."
)
TEXT_CHECKUP_OVERDUE: Final[str] = (
    "Programar un chequeo médico periódico ayuda a detectar factores de riesgo a tiempo."
)
