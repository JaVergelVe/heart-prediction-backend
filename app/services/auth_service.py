"""Password hashing, JWT, register/login orchestration."""

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.constants import auth as auth_c
from app.constants import http as http_c
from app.constants import messages as msg_c
from app.constants import validation as val_c
from app.core.config import get_settings
from app.core.exceptions import APIError
from app.models import MedicalConditions, User, UserProfile
from app.schemas.auth import RegisterRequest
from app.services.age_category import age_category_from_birth_date


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(
            plain.encode("utf-8"),
            password_hash.encode("utf-8"),
        )
    except ValueError:
        return False


def create_access_token(user_id: str) -> str:
    settings = get_settings()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(seconds=settings.access_token_expire_seconds)
    payload = {
        auth_c.JWT_CLAIM_SUB: user_id,
        auth_c.JWT_CLAIM_EXP: expire,
        auth_c.JWT_CLAIM_IAT: now,
    }
    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> str:
    settings = get_settings()
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
    except jwt.PyJWTError:
        raise APIError(
            http_c.HTTP_401_UNAUTHORIZED,
            code=msg_c.ERROR_CODE_UNAUTHORIZED,
            message=msg_c.MSG_TOKEN_INVALID_OR_EXPIRED,
        ) from None
    sub = payload.get(auth_c.JWT_CLAIM_SUB)
    if not isinstance(sub, str) or not sub.strip():
        raise APIError(
            http_c.HTTP_401_UNAUTHORIZED,
            code=msg_c.ERROR_CODE_UNAUTHORIZED,
            message=msg_c.MSG_TOKEN_INVALID_OR_EXPIRED,
        )
    return sub


def get_user_by_email(db: Session, email: str) -> User | None:
    normalized = email.strip().lower()
    return db.scalars(select(User).where(User.email == normalized)).first()


def register_user(db: Session, body: RegisterRequest) -> User:
    if get_user_by_email(db, str(body.email)) is not None:
        raise APIError(
            http_c.HTTP_400_BAD_REQUEST,
            code=msg_c.ERROR_CODE_VALIDATION,
            message=msg_c.MSG_VALIDATION_FAILED,
            details={
                msg_c.KEY_FIELD: msg_c.FIELD_EMAIL,
                msg_c.KEY_REASON: msg_c.REASON_EMAIL_REGISTERED,
            },
        )

    user = User(
        email=str(body.email).lower(),
        password_hash=hash_password(body.password),
        is_active=val_c.DEFAULT_USER_IS_ACTIVE,
    )
    db.add(user)

    try:
        db.flush()
        prof = body.profile
        age_cat = age_category_from_birth_date(prof.birth_date)
        profile = UserProfile(
            user_id=user.id,
            sex=prof.sex,
            birth_date=prof.birth_date,
            age_category=age_cat,
            height_meters=prof.height_meters,
            removed_teeth=prof.removed_teeth,
        )
        mc = body.medical_conditions
        medical = MedicalConditions(
            user_id=user.id,
            had_angina=mc.had_angina,
            had_stroke=mc.had_stroke,
            had_asthma=mc.had_asthma,
            had_copd=mc.had_copd,
            had_skin_cancer=mc.had_skin_cancer,
            had_depressive_disorder=mc.had_depressive_disorder,
            had_kidney_disease=mc.had_kidney_disease,
            had_arthritis=mc.had_arthritis,
            had_diabetes=mc.had_diabetes,
            deaf_or_hard_of_hearing=mc.deaf_or_hard_of_hearing,
            blind_or_vision_difficulty=mc.blind_or_vision_difficulty,
            difficulty_concentrating=mc.difficulty_concentrating,
            difficulty_walking=mc.difficulty_walking,
            difficulty_dressing_bathing=mc.difficulty_dressing_bathing,
            difficulty_errands=mc.difficulty_errands,
        )
        db.add(profile)
        db.add(medical)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise APIError(
            http_c.HTTP_400_BAD_REQUEST,
            code=msg_c.ERROR_CODE_VALIDATION,
            message=msg_c.MSG_VALIDATION_FAILED,
            details={
                msg_c.KEY_FIELD: msg_c.FIELD_EMAIL,
                msg_c.KEY_REASON: msg_c.REASON_EMAIL_REGISTERED,
            },
        ) from None

    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User:
    user = get_user_by_email(db, email.lower())
    if user is None or not verify_password(password, user.password_hash):
        raise APIError(
            http_c.HTTP_401_UNAUTHORIZED,
            code=msg_c.ERROR_CODE_INVALID_CREDENTIALS,
            message=msg_c.MSG_INVALID_CREDENTIALS,
        )
    if not user.is_active:
        raise APIError(
            http_c.HTTP_401_UNAUTHORIZED,
            code=msg_c.ERROR_CODE_INVALID_CREDENTIALS,
            message=msg_c.MSG_INVALID_CREDENTIALS,
        )
    user.last_login = datetime.now(timezone.utc)
    db.commit()
    db.refresh(user)
    return user
