"""Survey literals aligned with MySQL CHECK constraints on table `predictions`."""

from enum import Enum


class GeneralHealth(str, Enum):
    EXCELLENT = "Excellent"
    VERY_GOOD = "Very good"
    GOOD = "Good"
    FAIR = "Fair"
    POOR = "Poor"


class LastCheckupTime(str, Enum):
    WITHIN_PAST_YEAR = "Within past year (anytime less than 12 months ago)"
    WITHIN_PAST_2_YEARS = "Within past 2 years (1 year but less than 2 years ago)"
    WITHIN_PAST_5_YEARS = "Within past 5 years (2 years but less than 5 years ago)"
    FIVE_OR_MORE_YEARS_AGO = "5 or more years ago"
    NEVER = "Never"


class EcigaretteUsage(str, Enum):
    NEVER_USED_LIFE = "Never used e-cigarettes in my entire life"
    NOT_AT_ALL_NOW = "Not at all (right now)"
    SOME_DAYS = "Use them some days"
    EVERY_DAY = "Use them every day"


class SmokerStatus(str, Enum):
    NEVER_SMOKED = "Never smoked"
    FORMER_SMOKER = "Former smoker"
    CURRENT_SOME_DAYS = "Current smoker - now smokes some days"
    CURRENT_EVERY_DAY = "Current smoker - now smokes every day"


class CovidPos(str, Enum):
    YES = "Yes"
    NO = "No"
    HOME_TEST_POSITIVE = "Tested positive using home test without a health professional"


class TetanusLast10Tdap(str, Enum):
    YES_TDAP = "Yes, received Tdap"
    YES_TETANUS_UNKNOWN_TYPE = "Yes, received tetanus shot but not sure what type"
    YES_TETANUS_NOT_TDAP = "Yes, received tetanus shot, but not Tdap"
    NO_NOT_IN_10_YEARS = "No, did not receive any tetanus shot in the past 10 years"
