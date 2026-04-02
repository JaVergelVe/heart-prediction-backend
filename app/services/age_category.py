"""Derive BRFSS-style age bucket label from birth date (aligned with API examples)."""

from datetime import date

from app.constants import arrays as arr_c


def age_category_from_birth_date(birth: date, *, today: date | None = None) -> str:
    ref = today or date.today()
    age = ref.year - birth.year - ((ref.month, ref.day) < (birth.month, birth.day))
    if age >= arr_c.AGE_THRESHOLD_SENIOR_YEARS:
        return arr_c.AGE_CATEGORY_80_OR_OLDER
    for bracket in arr_c.AGE_BRACKETS:
        lo = bracket[arr_c.AGE_BRACKET_IDX_LOW]
        hi = bracket[arr_c.AGE_BRACKET_IDX_HIGH]
        label = bracket[arr_c.AGE_BRACKET_IDX_LABEL]
        if lo <= age <= hi:
            return label
    return arr_c.AGE_CATEGORY_80_OR_OLDER
