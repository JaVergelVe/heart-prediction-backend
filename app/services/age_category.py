"""Derive BRFSS-style age bucket label from birth date (aligned with API examples)."""

from datetime import date


def age_category_from_birth_date(birth: date, *, today: date | None = None) -> str:
    ref = today or date.today()
    age = ref.year - birth.year - ((ref.month, ref.day) < (birth.month, birth.day))
    if age >= 80:
        return "Age 80 or older"
    brackets: list[tuple[int, int, str]] = [
        (18, 24, "Age 18 to 24"),
        (25, 29, "Age 25 to 29"),
        (30, 34, "Age 30 to 34"),
        (35, 39, "Age 35 to 39"),
        (40, 44, "Age 40 to 44"),
        (45, 49, "Age 45 to 49"),
        (50, 54, "Age 50 to 54"),
        (55, 59, "Age 55 to 59"),
        (60, 64, "Age 60 to 64"),
        (65, 69, "Age 65 to 69"),
        (70, 74, "Age 70 to 74"),
        (75, 79, "Age 75 to 79"),
    ]
    for lo, hi, label in brackets:
        if lo <= age <= hi:
            return label
    return "Age 80 or older"
