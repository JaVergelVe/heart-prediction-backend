"""Simple rule-based recommendations for prediction responses (not persisted)."""

from __future__ import annotations

from typing import Any

from app.constants import messages as msg_c
from app.constants import prediction as pred_c
from app.constants import prediction_survey as ps
from app.constants import recommendations as rec_c
from app.models.prediction import Prediction


def _push(
    out: list[dict[str, Any]],
    text: str,
    category: str,
) -> None:
    if len(out) >= rec_c.RECOMMENDATION_MAX_ITEMS:
        return
    out.append(
        {
            msg_c.KEY_RECOMMENDATION_TEXT: text,
            msg_c.KEY_RECOMMENDATION_CATEGORY: category,
            msg_c.KEY_RECOMMENDATION_PRIORITY: len(out) + 1,
        }
    )


def build_recommendations_for_row(row: Prediction) -> list[dict[str, Any]]:
    """
    Build a small ordered list of recommendations from stored risk + survey fields.

    Deterministic, non-clinical guidance only; not a substitute for medical advice.
    """
    out: list[dict[str, Any]] = []

    rl = row.risk_level
    if rl == pred_c.RISK_LEVEL_HIGH:
        _push(out, rec_c.TEXT_RISK_HIGH, rec_c.REC_CATEGORY_MEDICAL)
    elif rl == pred_c.RISK_LEVEL_MEDIUM:
        _push(out, rec_c.TEXT_RISK_MEDIUM, rec_c.REC_CATEGORY_MEDICAL)
    elif rl == pred_c.RISK_LEVEL_LOW:
        _push(out, rec_c.TEXT_RISK_LOW, rec_c.REC_CATEGORY_LIFESTYLE)
    else:
        _push(out, rec_c.TEXT_RISK_UNKNOWN, rec_c.REC_CATEGORY_LIFESTYLE)

    ss = row.smoker_status
    if ss in (
        ps.SmokerStatus.CURRENT_SOME_DAYS.value,
        ps.SmokerStatus.CURRENT_EVERY_DAY.value,
    ):
        _push(out, rec_c.TEXT_SMOKING, rec_c.REC_CATEGORY_SUBSTANCE_USE)

    eu = row.ecigarette_usage
    if eu and eu != ps.EcigaretteUsage.NEVER_USED_LIFE.value:
        _push(out, rec_c.TEXT_ECIGARETTE, rec_c.REC_CATEGORY_SUBSTANCE_USE)

    if row.bmi is not None:
        b = float(row.bmi)
        if b >= rec_c.BMI_OBESE_MIN:
            _push(out, rec_c.TEXT_WEIGHT_OBESE, rec_c.REC_CATEGORY_NUTRITION)
        elif b >= rec_c.BMI_OVERWEIGHT_MIN:
            _push(out, rec_c.TEXT_WEIGHT_OVERWEIGHT, rec_c.REC_CATEGORY_NUTRITION)

    if row.physical_activities is False:
        _push(out, rec_c.TEXT_SEDENTARY, rec_c.REC_CATEGORY_PHYSICAL_ACTIVITY)

    if row.sleep_hours is not None:
        sf = float(row.sleep_hours)
        if sf > 0 and sf < rec_c.SLEEP_HOURS_SHORT_BELOW:
            _push(out, rec_c.TEXT_SHORT_SLEEP, rec_c.REC_CATEGORY_SLEEP)

    if row.alcohol_drinkers is True:
        _push(out, rec_c.TEXT_ALCOHOL, rec_c.REC_CATEGORY_LIFESTYLE)

    gh = row.general_health
    if gh in (ps.GeneralHealth.FAIR.value, ps.GeneralHealth.POOR.value):
        _push(out, rec_c.TEXT_GENERAL_HEALTH_POOR, rec_c.REC_CATEGORY_MEDICAL)

    lc = row.last_checkup_time
    if lc in (
        ps.LastCheckupTime.NEVER.value,
        ps.LastCheckupTime.FIVE_OR_MORE_YEARS_AGO.value,
    ):
        _push(out, rec_c.TEXT_CHECKUP_OVERDUE, rec_c.REC_CATEGORY_PREVENTIVE)

    return out
