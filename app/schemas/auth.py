"""Request/response shapes for auth (aligned with docs/api-contracts.md)."""

from datetime import date
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.constants import arrays as arr_c
from app.constants import messages as msg_c
from app.constants import validation as val_c

SexLiteral = Literal[arr_c.SEX_MALE, arr_c.SEX_FEMALE]
RemovedTeethLiteral = Literal[
    arr_c.REMOVED_TEETH_NONE_OF_THEM,
    arr_c.REMOVED_TEETH_1_TO_5,
    arr_c.REMOVED_TEETH_6_OR_MORE_NOT_ALL,
    arr_c.REMOVED_TEETH_ALL,
]
HadDiabetesLiteral = Literal[
    arr_c.HAD_DIABETES_NO,
    arr_c.HAD_DIABETES_YES,
    arr_c.HAD_DIABETES_PRE_DIABETES,
    arr_c.HAD_DIABETES_PREGNANCY,
]


class RegisterProfileIn(BaseModel):
    sex: SexLiteral
    birth_date: date
    height_meters: float = Field(..., ge=val_c.HEIGHT_METERS_MIN, le=val_c.HEIGHT_METERS_MAX)
    removed_teeth: RemovedTeethLiteral

    @field_validator("birth_date")
    @classmethod
    def birth_date_age(cls, v: date) -> date:
        today = date.today()
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        if age < val_c.MIN_AGE_YEARS or age > val_c.MAX_AGE_YEARS:
            raise ValueError(msg_c.MSG_BIRTH_DATE_AGE_RANGE)
        return v


class RegisterMedicalIn(BaseModel):
    had_angina: bool
    had_stroke: bool
    had_asthma: bool
    had_copd: bool
    had_skin_cancer: bool
    had_depressive_disorder: bool
    had_kidney_disease: bool
    had_arthritis: bool
    had_diabetes: HadDiabetesLiteral
    deaf_or_hard_of_hearing: bool
    blind_or_vision_difficulty: bool
    difficulty_concentrating: bool
    difficulty_walking: bool
    difficulty_dressing_bathing: bool
    difficulty_errands: bool


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(
        ...,
        min_length=val_c.MIN_PASSWORD_LENGTH,
        max_length=val_c.MAX_PASSWORD_LENGTH,
    )
    profile: RegisterProfileIn
    medical_conditions: RegisterMedicalIn

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not any(c.isalpha() for c in v):
            raise ValueError(msg_c.MSG_PASSWORD_NEED_LETTER)
        if not any(c.isdigit() for c in v):
            raise ValueError(msg_c.MSG_PASSWORD_NEED_DIGIT)
        return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(
        ...,
        min_length=val_c.MIN_LOGIN_PASSWORD_LENGTH,
        max_length=val_c.MAX_PASSWORD_LENGTH,
    )
