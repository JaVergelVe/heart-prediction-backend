"""Map API feature bundle (survey + profile + medical + vitals) to training column names."""

from __future__ import annotations

from datetime import date
from typing import Any

from app.constants import arrays as arr_c
from app.constants import messages as msg_c
from app.constants import ml_inference as ml_c
from app.services.age_category import age_category_from_birth_date


def _bool_to_float(v: Any) -> float:
    return 1.0 if bool(v) else 0.0


def _sex_to_float(sex: str) -> float:
    if sex == arr_c.SEX_MALE:
        return ml_c.SEX_ENCODED_MALE
    return ml_c.SEX_ENCODED_FEMALE


def _resolve_age_category(profile: dict[str, Any]) -> str:
    ac = profile.get(msg_c.KEY_AGE_CATEGORY)
    if ac:
        return str(ac)
    bd_raw = profile.get(msg_c.KEY_BIRTH_DATE)
    if bd_raw is None:
        raise ValueError("age_category or birth_date required for AgeCategory")
    if isinstance(bd_raw, date):
        bd = bd_raw
    else:
        bd = date.fromisoformat(str(bd_raw))
    return age_category_from_birth_date(bd)


def build_training_row(features: dict[str, Any]) -> dict[str, Any]:
    """
    Build a single-row dict keyed by PascalCase training columns.

    `features` must include BMI, weight_kilograms, profile, medical_conditions, survey
    (survey should already be coercion-aligned with persistence defaults).
    """
    profile = features[msg_c.KEY_PROFILE]
    survey = features[msg_c.KEY_SURVEY]
    medical = features[msg_c.KEY_MEDICAL_CONDITIONS]
    bmi = float(features[msg_c.KEY_BMI])
    weight_kg = float(features[msg_c.KEY_WEIGHT_KILOGRAMS])
    height_m = float(profile[msg_c.KEY_HEIGHT_METERS])

    row: dict[str, Any] = {
        ml_c.COL_GENERAL_HEALTH: survey[msg_c.KEY_GENERAL_HEALTH],
        ml_c.COL_LAST_CHECKUP_TIME: survey[msg_c.KEY_LAST_CHECKUP_TIME],
        ml_c.COL_REMOVED_TEETH: profile[msg_c.KEY_REMOVED_TEETH],
        ml_c.COL_HAD_DIABETES: medical[msg_c.KEY_HAD_DIABETES],
        ml_c.COL_SMOKER_STATUS: survey[msg_c.KEY_SMOKER_STATUS],
        ml_c.COL_ECIGARETTE_USAGE: survey[msg_c.KEY_ECIGARETTE_USAGE],
        ml_c.COL_AGE_CATEGORY: _resolve_age_category(profile),
        ml_c.COL_TETANUS_LAST_10_TDAP: survey[msg_c.KEY_TETANUS_LAST_10_TDAP],
        ml_c.COL_COVID_POS: survey[msg_c.KEY_COVID_POS],
        ml_c.COL_PHYSICAL_HEALTH_DAYS: int(survey[msg_c.KEY_PHYSICAL_HEALTH_DAYS]),
        ml_c.COL_MENTAL_HEALTH_DAYS: int(survey[msg_c.KEY_MENTAL_HEALTH_DAYS]),
        ml_c.COL_SLEEP_HOURS: float(survey[msg_c.KEY_SLEEP_HOURS]),
        ml_c.COL_HEIGHT_IN_METERS: height_m,
        ml_c.COL_WEIGHT_IN_KILOGRAMS: weight_kg,
        ml_c.COL_BMI: bmi,
        ml_c.COL_SEX: _sex_to_float(str(profile[msg_c.KEY_SEX])),
        ml_c.COL_PHYSICAL_ACTIVITIES: _bool_to_float(survey[msg_c.KEY_PHYSICAL_ACTIVITIES]),
        ml_c.COL_HAD_ANGINA: _bool_to_float(medical[msg_c.KEY_HAD_ANGINA]),
        ml_c.COL_HAD_STROKE: _bool_to_float(medical[msg_c.KEY_HAD_STROKE]),
        ml_c.COL_HAD_ASTHMA: _bool_to_float(medical[msg_c.KEY_HAD_ASTHMA]),
        ml_c.COL_HAD_COPD: _bool_to_float(medical[msg_c.KEY_HAD_COPD]),
        ml_c.COL_HAD_SKIN_CANCER: _bool_to_float(medical[msg_c.KEY_HAD_SKIN_CANCER]),
        ml_c.COL_HAD_DEPRESSIVE_DISORDER: _bool_to_float(
            medical[msg_c.KEY_HAD_DEPRESSIVE_DISORDER]
        ),
        ml_c.COL_HAD_KIDNEY_DISEASE: _bool_to_float(medical[msg_c.KEY_HAD_KIDNEY_DISEASE]),
        ml_c.COL_HAD_ARTHRITIS: _bool_to_float(medical[msg_c.KEY_HAD_ARTHRITIS]),
        ml_c.COL_DEAF_OR_HARD_OF_HEARING: _bool_to_float(
            medical[msg_c.KEY_DEAF_OR_HARD_OF_HEARING]
        ),
        ml_c.COL_BLIND_OR_VISION_DIFFICULTY: _bool_to_float(
            medical[msg_c.KEY_BLIND_OR_VISION_DIFFICULTY]
        ),
        ml_c.COL_DIFFICULTY_CONCENTRATING: _bool_to_float(
            medical[msg_c.KEY_DIFFICULTY_CONCENTRATING]
        ),
        ml_c.COL_DIFFICULTY_WALKING: _bool_to_float(medical[msg_c.KEY_DIFFICULTY_WALKING]),
        ml_c.COL_DIFFICULTY_DRESSING_BATHING: _bool_to_float(
            medical[msg_c.KEY_DIFFICULTY_DRESSING_BATHING]
        ),
        ml_c.COL_DIFFICULTY_ERRANDS: _bool_to_float(medical[msg_c.KEY_DIFFICULTY_ERRANDS]),
        ml_c.COL_ALCOHOL_DRINKERS: _bool_to_float(survey[msg_c.KEY_ALCOHOL_DRINKERS]),
        ml_c.COL_CHEST_SCAN: _bool_to_float(survey[msg_c.KEY_CHEST_SCAN]),
        ml_c.COL_HIV_TESTING: _bool_to_float(survey[msg_c.KEY_HIV_TESTING]),
        ml_c.COL_FLU_VAX_LAST_12: _bool_to_float(survey[msg_c.KEY_FLU_VAX_LAST_12]),
        ml_c.COL_PNEUMO_VAX_EVER: _bool_to_float(survey[msg_c.KEY_PNEUMO_VAX_EVER]),
        ml_c.COL_HIGH_RISK_LAST_YEAR: _bool_to_float(survey[msg_c.KEY_HIGH_RISK_LAST_YEAR]),
    }
    return row
