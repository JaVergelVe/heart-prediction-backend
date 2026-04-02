"""Static categorical strings and age-bracket definitions."""

from typing import Final

from app.constants import validation as v

# --- Sex (register / API) ---
SEX_MALE: Final[str] = "Male"
SEX_FEMALE: Final[str] = "Female"

# --- Removed teeth (register / API) ---
REMOVED_TEETH_NONE_OF_THEM: Final[str] = "None of them"
REMOVED_TEETH_1_TO_5: Final[str] = "1 to 5"
REMOVED_TEETH_6_OR_MORE_NOT_ALL: Final[str] = "6 or more, but not all"
REMOVED_TEETH_ALL: Final[str] = "All"

# --- Had diabetes (register / API) ---
HAD_DIABETES_NO: Final[str] = "No"
HAD_DIABETES_YES: Final[str] = "Yes"
HAD_DIABETES_PRE_DIABETES: Final[str] = "No, pre-diabetes or borderline diabetes"
HAD_DIABETES_PREGNANCY: Final[str] = "Yes, but only during pregnancy (female)"

# --- Age category labels (BRFSS-style buckets) ---
AGE_CATEGORY_18_24: Final[str] = "Age 18 to 24"
AGE_CATEGORY_25_29: Final[str] = "Age 25 to 29"
AGE_CATEGORY_30_34: Final[str] = "Age 30 to 34"
AGE_CATEGORY_35_39: Final[str] = "Age 35 to 39"
AGE_CATEGORY_40_44: Final[str] = "Age 40 to 44"
AGE_CATEGORY_45_49: Final[str] = "Age 45 to 49"
AGE_CATEGORY_50_54: Final[str] = "Age 50 to 54"
AGE_CATEGORY_55_59: Final[str] = "Age 55 to 59"
AGE_CATEGORY_60_64: Final[str] = "Age 60 to 64"
AGE_CATEGORY_65_69: Final[str] = "Age 65 to 69"
AGE_CATEGORY_70_74: Final[str] = "Age 70 to 74"
AGE_CATEGORY_75_79: Final[str] = "Age 75 to 79"
AGE_CATEGORY_80_OR_OLDER: Final[str] = "Age 80 or older"

# --- Age bracket tuple indices: 0 = low age, 1 = high age, 2 = label ---
AGE_BRACKET_IDX_LOW: Final[int] = 0
AGE_BRACKET_IDX_HIGH: Final[int] = 1
AGE_BRACKET_IDX_LABEL: Final[int] = 2

AGE_THRESHOLD_SENIOR_YEARS: Final[int] = 80

# (low_inclusive, high_inclusive, label) — aligned with age_category_from_birth_date logic
AGE_BRACKETS: Final[tuple[tuple[int, int, str], ...]] = (
    (v.MIN_AGE_YEARS, 24, AGE_CATEGORY_18_24),
    (25, 29, AGE_CATEGORY_25_29),
    (30, 34, AGE_CATEGORY_30_34),
    (35, 39, AGE_CATEGORY_35_39),
    (40, 44, AGE_CATEGORY_40_44),
    (45, 49, AGE_CATEGORY_45_49),
    (50, 54, AGE_CATEGORY_50_54),
    (55, 59, AGE_CATEGORY_55_59),
    (60, 64, AGE_CATEGORY_60_64),
    (65, 69, AGE_CATEGORY_65_69),
    (70, 74, AGE_CATEGORY_70_74),
    (75, 79, AGE_CATEGORY_75_79),
)
