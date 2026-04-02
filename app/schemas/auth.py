"""Request/response shapes for auth (aligned with docs/api-contracts.md)."""

from datetime import date
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, field_validator

SexLiteral = Literal["Male", "Female"]
RemovedTeethLiteral = Literal[
    "None of them",
    "1 to 5",
    "6 or more, but not all",
    "All",
]
HadDiabetesLiteral = Literal[
    "No",
    "Yes",
    "No, pre-diabetes or borderline diabetes",
    "Yes, but only during pregnancy (female)",
]


class RegisterProfileIn(BaseModel):
    sex: SexLiteral
    birth_date: date
    height_meters: float = Field(..., ge=0.5, le=2.5)
    removed_teeth: RemovedTeethLiteral

    @field_validator("birth_date")
    @classmethod
    def birth_date_age(cls, v: date) -> date:
        today = date.today()
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        if age < 18 or age > 120:
            raise ValueError("La edad debe estar entre 18 y 120 años")
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
    password: str = Field(..., min_length=8, max_length=128)
    profile: RegisterProfileIn
    medical_conditions: RegisterMedicalIn

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not any(c.isalpha() for c in v):
            raise ValueError("La contraseña debe incluir al menos una letra")
        if not any(c.isdigit() for c in v):
            raise ValueError("La contraseña debe incluir al menos un número")
        return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1, max_length=128)
