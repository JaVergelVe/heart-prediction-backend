"""Rule-based cardiovascular lifestyle recommendations for prediction responses."""

from __future__ import annotations

from typing import Any

from app.constants import messages as msg_c
from app.constants import prediction as pred_c
from app.constants import prediction_survey as ps
from app.constants import recommendations as rec_c


def _append_unique(recs: list[str], seen: set[str], text: str) -> bool:
    """Append if new; return True if max items reached (caller should stop)."""
    if not text:
        return len(recs) >= rec_c.RECOMMENDATIONS_MAX_ITEMS
    if text in seen:
        return False
    seen.add(text)
    recs.append(text)
    return len(recs) >= rec_c.RECOMMENDATIONS_MAX_ITEMS


def _shap_substring_hints(feature_name: str) -> list[str]:
    f = feature_name.lower()
    out: list[str] = []
    if rec_c.SHAP_FEATURE_SUBSTRING_BMI in f:
        out.append(rec_c.MSG_REC_SHAP_BMI)
    if (
        rec_c.SHAP_FEATURE_SUBSTRING_GENERAL_HEALTH in f
        or rec_c.SHAP_FEATURE_SUBSTRING_GENERAL_HEALTH_SNAKE in f
    ):
        out.append(rec_c.MSG_REC_SHAP_GENERAL_HEALTH)
    if rec_c.SHAP_FEATURE_SUBSTRING_SMOKER in f or rec_c.SHAP_FEATURE_SUBSTRING_SMOKE in f:
        out.append(rec_c.MSG_REC_SHAP_SMOKING)
    if rec_c.SHAP_FEATURE_SUBSTRING_SLEEP in f:
        out.append(rec_c.MSG_REC_SHAP_SLEEP)
    if rec_c.SHAP_FEATURE_SUBSTRING_PHYSICAL in f and rec_c.SHAP_FEATURE_SUBSTRING_ACTIVIT in f:
        out.append(rec_c.MSG_REC_SHAP_ACTIVITY)
    return out


def build_prediction_recommendations(
    *,
    risk_level: str | None,
    survey: dict[str, Any],
    shap_explanation: dict[str, Any] | None,
    bmi: float | None,
) -> list[str]:
    """
    Build a short, ordered list of recommendation strings (no medical diagnosis).

    Uses risk_level, lifestyle fields in `survey`, optional BMI, and SHAP `feature_name` hints.
    """
    recs: list[str] = []
    seen: set[str] = set()

    rl = risk_level or ""
    if rl == pred_c.RISK_LEVEL_HIGH:
        if _append_unique(recs, seen, rec_c.MSG_REC_HIGH_RISK_MEDICAL):
            return recs[: rec_c.RECOMMENDATIONS_MAX_ITEMS]
    elif rl == pred_c.RISK_LEVEL_MEDIUM:
        if _append_unique(recs, seen, rec_c.MSG_REC_MEDIUM_RISK_MONITOR):
            return recs[: rec_c.RECOMMENDATIONS_MAX_ITEMS]
    elif rl == pred_c.RISK_LEVEL_LOW:
        if _append_unique(recs, seen, rec_c.MSG_REC_LOW_RISK_MAINTAIN):
            return recs[: rec_c.RECOMMENDATIONS_MAX_ITEMS]

    sleep = survey.get(msg_c.KEY_SLEEP_HOURS)
    if sleep is not None:
        try:
            if float(sleep) < rec_c.SLEEP_HOURS_LOW_THRESHOLD:
                if _append_unique(recs, seen, rec_c.MSG_REC_SLEEP_IMPROVE):
                    return recs[: rec_c.RECOMMENDATIONS_MAX_ITEMS]
        except (TypeError, ValueError):
            pass

    pa = survey.get(msg_c.KEY_PHYSICAL_ACTIVITIES)
    if pa is False:
        if _append_unique(recs, seen, rec_c.MSG_REC_EXERCISE):
            return recs[: rec_c.RECOMMENDATIONS_MAX_ITEMS]

    smoker = survey.get(msg_c.KEY_SMOKER_STATUS)
    if smoker in (
        ps.SmokerStatus.CURRENT_SOME_DAYS.value,
        ps.SmokerStatus.CURRENT_EVERY_DAY.value,
    ):
        if _append_unique(recs, seen, rec_c.MSG_REC_QUIT_SMOKING):
            return recs[: rec_c.RECOMMENDATIONS_MAX_ITEMS]

    ecig = survey.get(msg_c.KEY_ECIGARETTE_USAGE)
    if ecig is not None and ecig != ps.EcigaretteUsage.NEVER_USED_LIFE.value:
        if _append_unique(recs, seen, rec_c.MSG_REC_REDUCE_ECIG):
            return recs[: rec_c.RECOMMENDATIONS_MAX_ITEMS]

    gh = survey.get(msg_c.KEY_GENERAL_HEALTH)
    if gh in (ps.GeneralHealth.FAIR.value, ps.GeneralHealth.POOR.value):
        if _append_unique(recs, seen, rec_c.MSG_REC_GENERAL_HEALTH_FAIR_POOR):
            return recs[: rec_c.RECOMMENDATIONS_MAX_ITEMS]

    checkup = survey.get(msg_c.KEY_LAST_CHECKUP_TIME)
    if checkup in (
        ps.LastCheckupTime.NEVER.value,
        ps.LastCheckupTime.FIVE_OR_MORE_YEARS_AGO.value,
    ):
        if _append_unique(recs, seen, rec_c.MSG_REC_CHECKUP_OVERDUE):
            return recs[: rec_c.RECOMMENDATIONS_MAX_ITEMS]

    if bmi is not None and bmi >= rec_c.BMI_OVERWEIGHT_MIN:
        if _append_unique(recs, seen, rec_c.MSG_REC_WEIGHT_BMI_ELEVATED):
            return recs[: rec_c.RECOMMENDATIONS_MAX_ITEMS]

    if survey.get(msg_c.KEY_ALCOHOL_DRINKERS) is True:
        if _append_unique(recs, seen, rec_c.MSG_REC_ALCOHOL_LIMIT):
            return recs[: rec_c.RECOMMENDATIONS_MAX_ITEMS]

    if shap_explanation:
        fname = str(shap_explanation.get(msg_c.KEY_SHAP_FEATURE_NAME, ""))
        for hint in _shap_substring_hints(fname):
            if _append_unique(recs, seen, hint):
                return recs[: rec_c.RECOMMENDATIONS_MAX_ITEMS]

    return recs[: rec_c.RECOMMENDATIONS_MAX_ITEMS]
