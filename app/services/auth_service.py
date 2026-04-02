"""Password hashing, JWT, register/login orchestration."""

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

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
        "sub": user_id,
        "exp": expire,
        "iat": now,
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
            401,
            code="UNAUTHORIZED",
            message="Token inválido o expirado",
        ) from None
    sub = payload.get("sub")
    if not isinstance(sub, str):
        raise APIError(401, code="UNAUTHORIZED", message="Token inválido o expirado")
    return sub


def get_user_by_email(db: Session, email: str) -> User | None:
    normalized = email.strip().lower()
    return db.scalars(select(User).where(User.email == normalized)).first()


def register_user(db: Session, body: RegisterRequest) -> User:
    if get_user_by_email(db, str(body.email)) is not None:
        raise APIError(
            400,
            code="VALIDATION_ERROR",
            message="Error en validación de datos",
            details={"field": "email", "reason": "Email ya está registrado"},
        )

    user = User(
        email=str(body.email).lower(),
        password_hash=hash_password(body.password),
        is_active=True,
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
            400,
            code="VALIDATION_ERROR",
            message="Error en validación de datos",
            details={"field": "email", "reason": "Email ya está registrado"},
        ) from None

    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User:
    user = get_user_by_email(db, email.lower())
    if user is None or not verify_password(password, user.password_hash):
        raise APIError(
            401,
            code="INVALID_CREDENTIALS",
            message="Email o contraseña incorrectos",
        )
    if not user.is_active:
        raise APIError(
            401,
            code="INVALID_CREDENTIALS",
            message="Email o contraseña incorrectos",
        )
    user.last_login = datetime.now(timezone.utc)
    db.commit()
    db.refresh(user)
    return user
