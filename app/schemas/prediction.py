"""Request bodies for prediction endpoints."""

from pydantic import BaseModel, Field

from app.constants import prediction_survey as survey_c
from app.constants import validation as val_c
from app.schemas.auth import RegisterMedicalIn, RegisterProfileIn


class PredictionSurveyIn(BaseModel):
    """Health survey fields on `predictions` (optional; must match MySQL CHECK when sent)."""

    general_health: survey_c.GeneralHealth | None = None
    physical_health_days: int | None = Field(
        None,
        ge=val_c.PHYSICAL_MENTAL_HEALTH_DAYS_MIN,
        le=val_c.PHYSICAL_MENTAL_HEALTH_DAYS_MAX,
    )
    mental_health_days: int | None = Field(
        None,
        ge=val_c.PHYSICAL_MENTAL_HEALTH_DAYS_MIN,
        le=val_c.PHYSICAL_MENTAL_HEALTH_DAYS_MAX,
    )
    last_checkup_time: survey_c.LastCheckupTime | None = None
    physical_activities: bool | None = None
    sleep_hours: float | None = Field(None, ge=val_c.SLEEP_HOURS_MIN, le=val_c.SLEEP_HOURS_MAX)
    smoker_status: survey_c.SmokerStatus | None = None
    ecigarette_usage: survey_c.EcigaretteUsage | None = None
    alcohol_drinkers: bool | None = None
    chest_scan: bool | None = None
    hiv_testing: bool | None = None
    flu_vax_last_12: bool | None = None
    pneumo_vax_ever: bool | None = None
    tetanus_last_10_tdap: survey_c.TetanusLast10Tdap | None = None
    high_risk_last_year: bool | None = None
    covid_pos: survey_c.CovidPos | None = None


class AnonymousPredictionRequest(PredictionSurveyIn):
    """Anonymous prediction: full profile, medical block, vitals, and survey."""

    session_id: str = Field(..., min_length=1, max_length=val_c.DB_SESSION_ID_MAX_LEN)
    profile: RegisterProfileIn
    medical_conditions: RegisterMedicalIn
    weight_kilograms: float = Field(..., ge=val_c.WEIGHT_KG_MIN, le=val_c.WEIGHT_KG_MAX)


class AuthenticatedPredictionRequest(PredictionSurveyIn):
    """Authenticated prediction: weight and survey; profile/medical loaded server-side."""

    weight_kilograms: float = Field(..., ge=val_c.WEIGHT_KG_MIN, le=val_c.WEIGHT_KG_MAX)
