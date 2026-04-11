"""Request bodies for authenticated user profile / medical updates."""

from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.constants import messages as msg_c
from app.constants import validation as val_c
from app.schemas.auth import HadDiabetesLiteral, RemovedTeethLiteral


class UserProfileUpdateRequest(BaseModel):
    """Partial profile update: only columns present on `user_profiles` and editable post-registration."""

    model_config = ConfigDict(extra="forbid")

    height_meters: float | None = Field(
        default=None,
        ge=val_c.HEIGHT_METERS_MIN,
        le=val_c.HEIGHT_METERS_MAX,
    )
    removed_teeth: RemovedTeethLiteral | None = None

    @model_validator(mode="after")
    def at_least_one_meaningful_field(self) -> Self:
        payload = self.model_dump(exclude_unset=True, exclude_none=True)
        if not payload:
            raise ValueError(msg_c.MSG_UPDATE_REQUIRES_ONE_FIELD)
        return self


class MedicalConditionsUpdateRequest(BaseModel):
    """Partial update for `medical_conditions` rows; omit keys you do not want to change."""

    model_config = ConfigDict(extra="forbid")

    had_angina: bool | None = None
    had_stroke: bool | None = None
    had_asthma: bool | None = None
    had_copd: bool | None = None
    had_skin_cancer: bool | None = None
    had_depressive_disorder: bool | None = None
    had_kidney_disease: bool | None = None
    had_arthritis: bool | None = None
    had_diabetes: HadDiabetesLiteral | None = None
    deaf_or_hard_of_hearing: bool | None = None
    blind_or_vision_difficulty: bool | None = None
    difficulty_concentrating: bool | None = None
    difficulty_walking: bool | None = None
    difficulty_dressing_bathing: bool | None = None
    difficulty_errands: bool | None = None

    @model_validator(mode="after")
    def at_least_one_meaningful_field(self) -> Self:
        payload = self.model_dump(exclude_unset=True, exclude_none=True)
        if not payload:
            raise ValueError(msg_c.MSG_UPDATE_REQUIRES_ONE_FIELD)
        return self
