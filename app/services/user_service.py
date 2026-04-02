"""Assemble /users/me payload from ORM rows."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.constants import (
    DEFAULT_HAD_DIABETES_DISPLAY,
    ERROR_CODE_INTERNAL,
    MSG_PROFILE_INCOMPLETE,
)
from app.core.exceptions import APIError
from app.core.timefmt import to_iso_z
from app.models import MedicalConditions, User, UserProfile


def build_me_data(db: Session, user: User) -> dict:
    profile = db.scalars(select(UserProfile).where(UserProfile.user_id == user.id)).first()
    medical = db.scalars(
        select(MedicalConditions).where(MedicalConditions.user_id == user.id)
    ).first()
    if profile is None or medical is None:
        raise APIError(
            500,
            code=ERROR_CODE_INTERNAL,
            message=MSG_PROFILE_INCOMPLETE,
        )

    height = profile.height_meters
    height_out = float(height) if height is not None else None

    return {
        "user_id": user.id,
        "email": user.email,
        "profile": {
            "sex": profile.sex,
            "birth_date": profile.birth_date.isoformat() if profile.birth_date else None,
            "age_category": profile.age_category,
            "height_meters": height_out,
            "removed_teeth": profile.removed_teeth,
            "created_at": to_iso_z(profile.created_at),
            "updated_at": to_iso_z(profile.updated_at),
        },
        "medical_conditions": {
            "had_angina": bool(medical.had_angina),
            "had_stroke": bool(medical.had_stroke),
            "had_asthma": bool(medical.had_asthma),
            "had_copd": bool(medical.had_copd),
            "had_skin_cancer": bool(medical.had_skin_cancer),
            "had_depressive_disorder": bool(medical.had_depressive_disorder),
            "had_kidney_disease": bool(medical.had_kidney_disease),
            "had_arthritis": bool(medical.had_arthritis),
            "had_diabetes": medical.had_diabetes or DEFAULT_HAD_DIABETES_DISPLAY,
            "deaf_or_hard_of_hearing": bool(medical.deaf_or_hard_of_hearing),
            "blind_or_vision_difficulty": bool(medical.blind_or_vision_difficulty),
            "difficulty_concentrating": bool(medical.difficulty_concentrating),
            "difficulty_walking": bool(medical.difficulty_walking),
            "difficulty_dressing_bathing": bool(medical.difficulty_dressing_bathing),
            "difficulty_errands": bool(medical.difficulty_errands),
            "updated_at": to_iso_z(medical.updated_at),
        },
    }
