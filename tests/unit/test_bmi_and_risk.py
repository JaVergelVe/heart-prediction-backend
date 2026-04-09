"""Unit checks for BMI rounding and risk thresholds (no HTTP)."""

from app.constants import prediction as pred_c
from app.constants import validation as val_c
from app.services.prediction_service import compute_bmi, risk_level_from_probability


def test_compute_bmi_matches_service_rounding() -> None:
    # 80 kg, 1.8 m → 80 / 3.24
    assert compute_bmi(80.0, 1.8) == round(80.0 / (1.8**2), val_c.DB_BMI_SCALE)


def test_risk_level_low_medium_high() -> None:
    assert risk_level_from_probability(29.9) == pred_c.RISK_LEVEL_LOW
    assert risk_level_from_probability(30.0) == pred_c.RISK_LEVEL_MEDIUM
    assert risk_level_from_probability(50.0) == pred_c.RISK_LEVEL_MEDIUM
    assert risk_level_from_probability(70.0) == pred_c.RISK_LEVEL_MEDIUM
    assert risk_level_from_probability(70.1) == pred_c.RISK_LEVEL_HIGH
