"""Assemble /users/me payload from ORM rows."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.constants import http as http_c
from app.constants import messages as msg_c
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
            http_c.HTTP_500_INTERNAL_SERVER_ERROR,
            code=msg_c.ERROR_CODE_INTERNAL,
            message=msg_c.MSG_PROFILE_INCOMPLETE,
        )

    height = profile.height_meters
    height_out = float(height) if height is not None else None

    return {
        msg_c.KEY_USER_ID: user.id,
        msg_c.KEY_EMAIL: user.email,
        msg_c.KEY_PROFILE: {
            msg_c.KEY_SEX: profile.sex,
            msg_c.KEY_BIRTH_DATE: profile.birth_date.isoformat()
            if profile.birth_date
            else None,
            msg_c.KEY_AGE_CATEGORY: profile.age_category,
            msg_c.KEY_HEIGHT_METERS: height_out,
            msg_c.KEY_REMOVED_TEETH: profile.removed_teeth,
            msg_c.KEY_CREATED_AT: to_iso_z(profile.created_at),
            msg_c.KEY_UPDATED_AT: to_iso_z(profile.updated_at),
        },
        msg_c.KEY_MEDICAL_CONDITIONS: {
            msg_c.KEY_HAD_ANGINA: bool(medical.had_angina),
            msg_c.KEY_HAD_STROKE: bool(medical.had_stroke),
            msg_c.KEY_HAD_ASTHMA: bool(medical.had_asthma),
            msg_c.KEY_HAD_COPD: bool(medical.had_copd),
            msg_c.KEY_HAD_SKIN_CANCER: bool(medical.had_skin_cancer),
            msg_c.KEY_HAD_DEPRESSIVE_DISORDER: bool(medical.had_depressive_disorder),
            msg_c.KEY_HAD_KIDNEY_DISEASE: bool(medical.had_kidney_disease),
            msg_c.KEY_HAD_ARTHRITIS: bool(medical.had_arthritis),
            msg_c.KEY_HAD_DIABETES: medical.had_diabetes
            or msg_c.DEFAULT_HAD_DIABETES_DISPLAY,
            msg_c.KEY_DEAF_OR_HARD_OF_HEARING: bool(medical.deaf_or_hard_of_hearing),
            msg_c.KEY_BLIND_OR_VISION_DIFFICULTY: bool(medical.blind_or_vision_difficulty),
            msg_c.KEY_DIFFICULTY_CONCENTRATING: bool(medical.difficulty_concentrating),
            msg_c.KEY_DIFFICULTY_WALKING: bool(medical.difficulty_walking),
            msg_c.KEY_DIFFICULTY_DRESSING_BATHING: bool(
                medical.difficulty_dressing_bathing
            ),
            msg_c.KEY_DIFFICULTY_ERRANDS: bool(medical.difficulty_errands),
            msg_c.KEY_UPDATED_AT: to_iso_z(medical.updated_at),
        },
    }
