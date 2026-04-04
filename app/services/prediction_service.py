"""Create heart-risk predictions using the mock scorer and persist snapshots."""

import math
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import asc, desc, func, select
from sqlalchemy.orm import Session

from app.constants import http as http_c
from app.constants import messages as msg_c
from app.constants import prediction as pred_c
from app.constants import validation as val_c
from app.core.exceptions import APIError
from app.ml.predictor import predict_heart_risk
from app.models import MedicalConditions, Prediction, UserProfile
from app.schemas.prediction import (
    AnonymousPredictionRequest,
    AuthenticatedPredictionRequest,
    SimulationPatchRequest,
)
from app.services import pdf_export_service, recommendation_service


def compute_bmi(weight_kg: float, height_m: float) -> float:
    return round(weight_kg / (height_m**2), val_c.DB_BMI_SCALE)


def risk_level_from_probability(probability: float) -> str:
    if probability < pred_c.RISK_PROBABILITY_LOW_MAX_EXCLUSIVE:
        return pred_c.RISK_LEVEL_LOW
    if probability > pred_c.RISK_PROBABILITY_HIGH_MIN_EXCLUSIVE:
        return pred_c.RISK_LEVEL_HIGH
    return pred_c.RISK_LEVEL_MEDIUM


def _survey_fields_from_anonymous(body: AnonymousPredictionRequest) -> dict[str, Any]:
    return body.model_dump(
        mode="json",
        exclude={
            msg_c.KEY_SESSION_ID,
            msg_c.KEY_PROFILE,
            msg_c.KEY_MEDICAL_CONDITIONS,
            msg_c.KEY_WEIGHT_KILOGRAMS,
        },
    )


def _survey_fields_from_authenticated(body: AuthenticatedPredictionRequest) -> dict[str, Any]:
    return body.model_dump(
        mode="json",
        exclude={msg_c.KEY_WEIGHT_KILOGRAMS},
    )


def _coerce_survey_for_db_persist(survey: dict[str, Any]) -> dict[str, Any]:
    """Fill omitted optional fields with CHECK-compliant values (MySQL NOT NULL + chk_*)."""
    out = dict(survey)
    for key, default in pred_c.SURVEY_DB_DEFAULTS:
        if out.get(key) is None:
            out[key] = default
    return out


def _ensure_bmi_for_db(bmi: float) -> None:
    if not (pred_c.DB_BMI_CHECK_MIN <= bmi <= pred_c.DB_BMI_CHECK_MAX):
        raise APIError(
            http_c.HTTP_400_BAD_REQUEST,
            code=msg_c.ERROR_CODE_VALIDATION,
            message=msg_c.MSG_BMI_OUT_OF_DB_RANGE,
        )


def _profile_orm_to_dict(profile: UserProfile) -> dict[str, Any]:
    return {
        msg_c.KEY_SEX: profile.sex,
        msg_c.KEY_BIRTH_DATE: profile.birth_date.isoformat()
        if profile.birth_date
        else None,
        msg_c.KEY_AGE_CATEGORY: profile.age_category,
        msg_c.KEY_HEIGHT_METERS: float(profile.height_meters)
        if profile.height_meters is not None
        else None,
        msg_c.KEY_REMOVED_TEETH: profile.removed_teeth,
    }


def _medical_orm_to_dict(medical: MedicalConditions) -> dict[str, Any]:
    return {
        msg_c.KEY_HAD_ANGINA: medical.had_angina,
        msg_c.KEY_HAD_STROKE: medical.had_stroke,
        msg_c.KEY_HAD_ASTHMA: medical.had_asthma,
        msg_c.KEY_HAD_COPD: medical.had_copd,
        msg_c.KEY_HAD_SKIN_CANCER: medical.had_skin_cancer,
        msg_c.KEY_HAD_DEPRESSIVE_DISORDER: medical.had_depressive_disorder,
        msg_c.KEY_HAD_KIDNEY_DISEASE: medical.had_kidney_disease,
        msg_c.KEY_HAD_ARTHRITIS: medical.had_arthritis,
        msg_c.KEY_HAD_DIABETES: medical.had_diabetes,
        msg_c.KEY_DEAF_OR_HARD_OF_HEARING: medical.deaf_or_hard_of_hearing,
        msg_c.KEY_BLIND_OR_VISION_DIFFICULTY: medical.blind_or_vision_difficulty,
        msg_c.KEY_DIFFICULTY_CONCENTRATING: medical.difficulty_concentrating,
        msg_c.KEY_DIFFICULTY_WALKING: medical.difficulty_walking,
        msg_c.KEY_DIFFICULTY_DRESSING_BATHING: medical.difficulty_dressing_bathing,
        msg_c.KEY_DIFFICULTY_ERRANDS: medical.difficulty_errands,
    }


def _require_profile_and_medical(
    db: Session, user_id: str
) -> tuple[UserProfile, MedicalConditions]:
    profile = db.scalars(select(UserProfile).where(UserProfile.user_id == user_id)).first()
    medical = db.scalars(
        select(MedicalConditions).where(MedicalConditions.user_id == user_id)
    ).first()
    if profile is None or medical is None:
        raise APIError(
            http_c.HTTP_400_BAD_REQUEST,
            code=msg_c.ERROR_CODE_PROFILE_INCOMPLETE,
            message=msg_c.MSG_PREDICTION_PROFILE_INCOMPLETE,
        )
    return profile, medical


def _require_height_meters(height: float | None) -> float:
    if height is None:
        raise APIError(
            http_c.HTTP_400_BAD_REQUEST,
            code=msg_c.ERROR_CODE_VALIDATION,
            message=msg_c.MSG_PREDICTION_HEIGHT_REQUIRED,
        )
    return height


def create_anonymous_prediction(db: Session, body: AnonymousPredictionRequest) -> dict[str, Any]:
    height = _require_height_meters(body.profile.height_meters)
    bmi = compute_bmi(body.weight_kilograms, height)
    _ensure_bmi_for_db(bmi)
    survey = _survey_fields_from_anonymous(body)
    survey_model = _coerce_survey_for_db_persist(dict(survey))
    features: dict[str, Any] = {
        msg_c.KEY_BMI: bmi,
        msg_c.KEY_WEIGHT_KILOGRAMS: body.weight_kilograms,
        msg_c.KEY_PROFILE: body.profile.model_dump(mode="json"),
        msg_c.KEY_MEDICAL_CONDITIONS: body.medical_conditions.model_dump(mode="json"),
        msg_c.KEY_SURVEY: survey_model,
    }
    ml_out = predict_heart_risk(features)
    probability = float(ml_out[msg_c.KEY_PREDICTION_PROBABILITY])
    risk = risk_level_from_probability(probability)

    row = Prediction(
        user_id=None,
        session_id=body.session_id,
        weight_kilograms=body.weight_kilograms,
        bmi=bmi,
        prediction_probability=probability,
        risk_level=risk,
        model_version=ml_out[msg_c.KEY_MODEL_VERSION],
        prediction_timestamp=datetime.now(timezone.utc),
        **survey_model,
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    recs = recommendation_service.build_prediction_recommendations(
        risk_level=risk,
        survey=survey_model,
        shap_explanation=ml_out[msg_c.KEY_SHAP_EXPLANATION],
        bmi=bmi,
    )
    return _prediction_to_response_dict(
        row,
        **{
            msg_c.KEY_PREDICTED_CLASS: ml_out[msg_c.KEY_PREDICTED_CLASS],
            msg_c.KEY_SHAP_EXPLANATION: ml_out[msg_c.KEY_SHAP_EXPLANATION],
            msg_c.KEY_RECOMMENDATIONS: recs,
        },
    )


def create_authenticated_prediction(
    db: Session, user_id: str, body: AuthenticatedPredictionRequest
) -> dict[str, Any]:
    profile, medical = _require_profile_and_medical(db, user_id)
    height = _require_height_meters(
        float(profile.height_meters) if profile.height_meters is not None else None
    )
    bmi = compute_bmi(body.weight_kilograms, height)
    _ensure_bmi_for_db(bmi)
    survey = _survey_fields_from_authenticated(body)
    survey_model = _coerce_survey_for_db_persist(dict(survey))
    features: dict[str, Any] = {
        msg_c.KEY_BMI: bmi,
        msg_c.KEY_WEIGHT_KILOGRAMS: body.weight_kilograms,
        msg_c.KEY_PROFILE: _profile_orm_to_dict(profile),
        msg_c.KEY_MEDICAL_CONDITIONS: _medical_orm_to_dict(medical),
        msg_c.KEY_SURVEY: survey_model,
    }
    ml_out = predict_heart_risk(features)
    probability = float(ml_out[msg_c.KEY_PREDICTION_PROBABILITY])
    risk = risk_level_from_probability(probability)

    row = Prediction(
        user_id=user_id,
        session_id=None,
        weight_kilograms=body.weight_kilograms,
        bmi=bmi,
        prediction_probability=probability,
        risk_level=risk,
        model_version=ml_out[msg_c.KEY_MODEL_VERSION],
        prediction_timestamp=datetime.now(timezone.utc),
        **survey_model,
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    recs = recommendation_service.build_prediction_recommendations(
        risk_level=risk,
        survey=survey_model,
        shap_explanation=ml_out[msg_c.KEY_SHAP_EXPLANATION],
        bmi=bmi,
    )
    return _prediction_to_response_dict(
        row,
        **{
            msg_c.KEY_PREDICTED_CLASS: ml_out[msg_c.KEY_PREDICTED_CLASS],
            msg_c.KEY_SHAP_EXPLANATION: ml_out[msg_c.KEY_SHAP_EXPLANATION],
            msg_c.KEY_RECOMMENDATIONS: recs,
        },
    )


def _survey_from_prediction_row(row: Prediction) -> dict[str, Any]:
    return {
        msg_c.KEY_GENERAL_HEALTH: row.general_health,
        msg_c.KEY_PHYSICAL_HEALTH_DAYS: row.physical_health_days,
        msg_c.KEY_MENTAL_HEALTH_DAYS: row.mental_health_days,
        msg_c.KEY_LAST_CHECKUP_TIME: row.last_checkup_time,
        msg_c.KEY_PHYSICAL_ACTIVITIES: row.physical_activities,
        msg_c.KEY_SLEEP_HOURS: float(row.sleep_hours) if row.sleep_hours is not None else None,
        msg_c.KEY_SMOKER_STATUS: row.smoker_status,
        msg_c.KEY_ECIGARETTE_USAGE: row.ecigarette_usage,
        msg_c.KEY_ALCOHOL_DRINKERS: row.alcohol_drinkers,
        msg_c.KEY_CHEST_SCAN: row.chest_scan,
        msg_c.KEY_HIV_TESTING: row.hiv_testing,
        msg_c.KEY_FLU_VAX_LAST_12: row.flu_vax_last_12,
        msg_c.KEY_PNEUMO_VAX_EVER: row.pneumo_vax_ever,
        msg_c.KEY_TETANUS_LAST_10_TDAP: row.tetanus_last_10_tdap,
        msg_c.KEY_HIGH_RISK_LAST_YEAR: row.high_risk_last_year,
        msg_c.KEY_COVID_POS: row.covid_pos,
    }


def _history_item_dict(row: Prediction) -> dict[str, Any]:
    ts = row.prediction_timestamp
    return {
        msg_c.KEY_PREDICTION_ID: row.id,
        msg_c.KEY_PREDICTION_PROBABILITY: float(row.prediction_probability)
        if row.prediction_probability is not None
        else None,
        msg_c.KEY_RISK_LEVEL: row.risk_level,
        msg_c.KEY_BMI: float(row.bmi) if row.bmi is not None else None,
        msg_c.KEY_WEIGHT_KILOGRAMS: float(row.weight_kilograms)
        if row.weight_kilograms is not None
        else None,
        msg_c.KEY_GENERAL_HEALTH: row.general_health,
        msg_c.KEY_PREDICTION_TIMESTAMP: ts.isoformat() if ts is not None else None,
    }


def list_prediction_history(
    db: Session,
    user_id: str,
    *,
    limit: int,
    offset: int,
    sort: str,
    order: str,
) -> dict[str, Any]:
    if sort != pred_c.HISTORY_SORT_PREDICTION_TIMESTAMP:
        raise APIError(
            http_c.HTTP_400_BAD_REQUEST,
            code=msg_c.ERROR_CODE_VALIDATION,
            message=msg_c.MSG_HISTORY_INVALID_SORT,
        )
    if order not in (pred_c.HISTORY_ORDER_DESC, pred_c.HISTORY_ORDER_ASC):
        raise APIError(
            http_c.HTTP_400_BAD_REQUEST,
            code=msg_c.ERROR_CODE_VALIDATION,
            message=msg_c.MSG_HISTORY_INVALID_ORDER,
        )

    base = select(Prediction).where(Prediction.user_id == user_id)
    count_q = select(func.count()).select_from(Prediction).where(Prediction.user_id == user_id)
    total = int(db.scalar(count_q) or 0)

    order_col = Prediction.prediction_timestamp
    ord_fn = desc if order == pred_c.HISTORY_ORDER_DESC else asc
    rows = db.scalars(
        base.order_by(ord_fn(order_col)).offset(offset).limit(limit)
    ).all()

    items = [_history_item_dict(r) for r in rows]
    has_more = offset + len(items) < total
    return {
        msg_c.KEY_PREDICTIONS: items,
        msg_c.KEY_PAGINATION: {
            msg_c.KEY_TOTAL: total,
            msg_c.KEY_LIMIT: limit,
            msg_c.KEY_OFFSET: offset,
            msg_c.KEY_HAS_MORE: has_more,
        },
    }


def get_prediction_detail(db: Session, user_id: str, prediction_id: str) -> dict[str, Any]:
    row = db.scalars(
        select(Prediction).where(
            Prediction.id == prediction_id,
            Prediction.user_id == user_id,
        )
    ).first()
    if row is None:
        raise APIError(
            http_c.HTTP_404_NOT_FOUND,
            code=msg_c.ERROR_CODE_PREDICTION_NOT_FOUND,
            message=msg_c.MSG_PREDICTION_NOT_FOUND,
        )

    profile = db.scalars(select(UserProfile).where(UserProfile.user_id == user_id)).first()
    medical = db.scalars(
        select(MedicalConditions).where(MedicalConditions.user_id == user_id)
    ).first()
    survey = _survey_from_prediction_row(row)

    if profile is None or medical is None:
        recs = recommendation_service.build_prediction_recommendations(
            risk_level=str(row.risk_level) if row.risk_level else None,
            survey=survey,
            shap_explanation=None,
            bmi=float(row.bmi) if row.bmi is not None else None,
        )
        return _prediction_to_response_dict(
            row,
            **{msg_c.KEY_RECOMMENDATIONS: recs},
        )

    if row.bmi is None or row.weight_kilograms is None:
        recs = recommendation_service.build_prediction_recommendations(
            risk_level=str(row.risk_level) if row.risk_level else None,
            survey=survey,
            shap_explanation=None,
            bmi=None,
        )
        return _prediction_to_response_dict(
            row,
            **{msg_c.KEY_RECOMMENDATIONS: recs},
        )

    features: dict[str, Any] = {
        msg_c.KEY_BMI: float(row.bmi),
        msg_c.KEY_WEIGHT_KILOGRAMS: float(row.weight_kilograms),
        msg_c.KEY_PROFILE: _profile_orm_to_dict(profile),
        msg_c.KEY_MEDICAL_CONDITIONS: _medical_orm_to_dict(medical),
        msg_c.KEY_SURVEY: survey,
    }
    ml_out = predict_heart_risk(features)
    recs = recommendation_service.build_prediction_recommendations(
        risk_level=str(row.risk_level) if row.risk_level else None,
        survey=survey,
        shap_explanation=ml_out[msg_c.KEY_SHAP_EXPLANATION],
        bmi=float(row.bmi),
    )
    return _prediction_to_response_dict(
        row,
        **{
            msg_c.KEY_PREDICTED_CLASS: ml_out[msg_c.KEY_PREDICTED_CLASS],
            msg_c.KEY_SHAP_EXPLANATION: ml_out[msg_c.KEY_SHAP_EXPLANATION],
            msg_c.KEY_RECOMMENDATIONS: recs,
        },
    )


def validate_simulation_request_keys(body: dict[str, Any]) -> None:
    for key in body:
        if key not in pred_c.SIMULATION_ALLOWED_FIELDS:
            raise APIError(
                http_c.HTTP_400_BAD_REQUEST,
                code=msg_c.ERROR_CODE_INVALID_VARIABLE,
                message=msg_c.MSG_SIMULATION_VARIABLE_NOT_MODIFIABLE,
                details={
                    msg_c.KEY_FIELD: key,
                    msg_c.KEY_REASON: msg_c.MSG_SIMULATION_REASON_FORBIDDEN,
                },
            )


def _values_differ(a: Any, b: Any) -> bool:
    if isinstance(a, bool) and isinstance(b, bool):
        return a != b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return not math.isclose(float(a), float(b), rel_tol=0.0, abs_tol=1e-4)
    return a != b


def simulate_what_if(
    db: Session, user_id: str, prediction_id: str, body: SimulationPatchRequest
) -> dict[str, Any]:
    row = db.scalars(
        select(Prediction).where(
            Prediction.id == prediction_id,
            Prediction.user_id == user_id,
        )
    ).first()
    if row is None:
        raise APIError(
            http_c.HTTP_404_NOT_FOUND,
            code=msg_c.ERROR_CODE_PREDICTION_NOT_FOUND,
            message=msg_c.MSG_PREDICTION_NOT_FOUND,
        )

    profile, medical = _require_profile_and_medical(db, user_id)
    height = _require_height_meters(
        float(profile.height_meters) if profile.height_meters is not None else None
    )

    if row.prediction_probability is None or row.weight_kilograms is None:
        raise APIError(
            http_c.HTTP_400_BAD_REQUEST,
            code=msg_c.ERROR_CODE_VALIDATION,
            message=msg_c.MSG_SIMULATION_BASELINE_INCOMPLETE,
        )

    original_probability = float(row.prediction_probability)
    original_risk = (
        str(row.risk_level)
        if row.risk_level is not None
        else risk_level_from_probability(original_probability)
    )

    baseline_weight = float(row.weight_kilograms)
    baseline_survey = _survey_from_prediction_row(row)

    patch_dict = body.model_dump(exclude_unset=True, exclude_none=True)
    merged_weight = patch_dict.get(msg_c.KEY_WEIGHT_KILOGRAMS, baseline_weight)
    survey_updates = {
        k: v for k, v in patch_dict.items() if k != msg_c.KEY_WEIGHT_KILOGRAMS
    }
    merged_survey = {**baseline_survey, **survey_updates}
    merged_survey_model = _coerce_survey_for_db_persist(dict(merged_survey))

    bmi_sim = compute_bmi(merged_weight, height)
    _ensure_bmi_for_db(bmi_sim)

    features: dict[str, Any] = {
        msg_c.KEY_BMI: bmi_sim,
        msg_c.KEY_WEIGHT_KILOGRAMS: merged_weight,
        msg_c.KEY_PROFILE: _profile_orm_to_dict(profile),
        msg_c.KEY_MEDICAL_CONDITIONS: _medical_orm_to_dict(medical),
        msg_c.KEY_SURVEY: merged_survey_model,
    }
    ml_out = predict_heart_risk(features)
    simulated_probability = float(ml_out[msg_c.KEY_PREDICTION_PROBABILITY])
    simulated_risk = risk_level_from_probability(simulated_probability)

    changed_fields: dict[str, Any] = {}
    if _values_differ(baseline_weight, merged_weight):
        changed_fields[msg_c.KEY_WEIGHT_KILOGRAMS] = {
            msg_c.KEY_ORIGINAL_VALUE: baseline_weight,
            msg_c.KEY_SIMULATED_VALUE: merged_weight,
        }
    for sk, bv in baseline_survey.items():
        mv = merged_survey[sk]
        if _values_differ(bv, mv):
            changed_fields[sk] = {
                msg_c.KEY_ORIGINAL_VALUE: bv,
                msg_c.KEY_SIMULATED_VALUE: mv,
            }

    return {
        msg_c.KEY_ORIGINAL_PROBABILITY: original_probability,
        msg_c.KEY_SIMULATED_PROBABILITY: simulated_probability,
        msg_c.KEY_ORIGINAL_RISK_LEVEL: original_risk,
        msg_c.KEY_SIMULATED_RISK_LEVEL: simulated_risk,
        msg_c.KEY_PROBABILITY_DIFFERENCE: round(
            simulated_probability - original_probability, val_c.DB_PREDICTION_PROB_SCALE
        ),
        msg_c.KEY_CHANGED_FIELDS: changed_fields,
        msg_c.KEY_SHAP_EXPLANATION: ml_out[msg_c.KEY_SHAP_EXPLANATION],
        msg_c.KEY_RECOMMENDATIONS: [],
    }


def _prediction_to_response_dict(row: Prediction, **extra: Any) -> dict[str, Any]:
    ts = row.prediction_timestamp
    out: dict[str, Any] = {
        msg_c.KEY_PREDICTION_ID: row.id,
        msg_c.KEY_USER_ID: row.user_id,
        msg_c.KEY_SESSION_ID: row.session_id,
        msg_c.KEY_WEIGHT_KILOGRAMS: float(row.weight_kilograms)
        if row.weight_kilograms is not None
        else None,
        msg_c.KEY_BMI: float(row.bmi) if row.bmi is not None else None,
        msg_c.KEY_GENERAL_HEALTH: row.general_health,
        msg_c.KEY_PHYSICAL_HEALTH_DAYS: row.physical_health_days,
        msg_c.KEY_MENTAL_HEALTH_DAYS: row.mental_health_days,
        msg_c.KEY_LAST_CHECKUP_TIME: row.last_checkup_time,
        msg_c.KEY_PHYSICAL_ACTIVITIES: row.physical_activities,
        msg_c.KEY_SLEEP_HOURS: float(row.sleep_hours) if row.sleep_hours is not None else None,
        msg_c.KEY_SMOKER_STATUS: row.smoker_status,
        msg_c.KEY_ECIGARETTE_USAGE: row.ecigarette_usage,
        msg_c.KEY_ALCOHOL_DRINKERS: row.alcohol_drinkers,
        msg_c.KEY_CHEST_SCAN: row.chest_scan,
        msg_c.KEY_HIV_TESTING: row.hiv_testing,
        msg_c.KEY_FLU_VAX_LAST_12: row.flu_vax_last_12,
        msg_c.KEY_PNEUMO_VAX_EVER: row.pneumo_vax_ever,
        msg_c.KEY_TETANUS_LAST_10_TDAP: row.tetanus_last_10_tdap,
        msg_c.KEY_HIGH_RISK_LAST_YEAR: row.high_risk_last_year,
        msg_c.KEY_COVID_POS: row.covid_pos,
        msg_c.KEY_PREDICTION_PROBABILITY: float(row.prediction_probability)
        if row.prediction_probability is not None
        else None,
        msg_c.KEY_RISK_LEVEL: row.risk_level,
        msg_c.KEY_MODEL_VERSION: row.model_version,
        msg_c.KEY_PREDICTION_TIMESTAMP: ts.isoformat() if ts is not None else None,
    }
    out.update(extra)
    if msg_c.KEY_RECOMMENDATIONS not in out:
        out[msg_c.KEY_RECOMMENDATIONS] = []
    return out


def export_prediction_pdf(db: Session, user_id: str, prediction_id: str) -> tuple[bytes, str]:
    """
    Build a PDF for an owned prediction (same data basis as GET /predictions/{id}).

    Returns (pdf_bytes, download_filename).
    """
    detail = get_prediction_detail(db, user_id, prediction_id)
    filename = pdf_export_service.build_export_filename(
        prediction_id=str(detail[msg_c.KEY_PREDICTION_ID]),
        prediction_timestamp_iso=detail.get(msg_c.KEY_PREDICTION_TIMESTAMP),
    )
    pdf_bytes = pdf_export_service.build_prediction_pdf_bytes(detail)
    return pdf_bytes, filename
