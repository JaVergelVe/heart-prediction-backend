"""Unit tests for user-friendly SHAP display and PDF export content."""

from __future__ import annotations

from app.constants import messages as msg_c
from app.constants import ml_inference as ml_c
from app.constants import prediction as pred_c
from app.services import pdf_export_service
from app.utils import shap_display as shap_util


def test_shap_explanation_user_view_for_bmi_uses_friendly_spanish() -> None:
    explanation = {
        msg_c.KEY_SHAP_FEATURE_NAME: "BMI",
        msg_c.KEY_SHAP_IMPACT_SCORE: 0.12,
        msg_c.KEY_SHAP_DIRECTION: ml_c.SHAP_DIRECTION_INCREASES_RISK,
        msg_c.KEY_SHAP_MESSAGE: (
            '"BMI" es el factor con mayor contribución SHAP en esta predicción; '
            "empuja la probabilidad de la clase positiva hacia arriba."
        ),
    }
    view = shap_util.build_shap_explanation_user_view(explanation)
    assert view.friendly_title == "Índice de masa corporal (IMC)"
    assert view.impact_label == "Aumenta el riesgo"
    assert "IMC elevado" in view.primary_explanation or "aumento del riesgo" in view.primary_explanation
    assert "clase positiva" not in view.primary_explanation
    assert view.narrative_extra is None or "clase positiva" not in view.narrative_extra


def test_shap_factor_user_view_ignores_technical_interpretation() -> None:
    factor = {
        msg_c.KEY_SHAP_FEATURE_NAME: "physicalactivities_1",
        msg_c.KEY_SHAP_FEATURE_VALUE: 1.0,
        msg_c.KEY_SHAP_CONTRIBUTION_SCORE: -0.08,
        msg_c.KEY_SHAP_RANK: 2,
        msg_c.KEY_SHAP_DIRECTION: ml_c.SHAP_DIRECTION_DECREASES_RISK,
        msg_c.KEY_SHAP_INTERPRETATION: (
            'Rango 2: "physicalactivities_1" (valor en el vector de entrada del modelo: 1.0) '
            "reduce la contribución hacia la clase positiva; valor SHAP -0.08."
        ),
    }
    view = shap_util.build_shap_factor_user_view(factor, batch_max_abs=0.12)
    assert view.friendly_title.startswith("Actividad física")
    assert view.impact_label == "Disminuye el riesgo"
    assert "actividad física" in view.primary_explanation.lower()
    assert view.narrative_extra is None or "vector de entrada" not in view.narrative_extra


def test_pdf_builds_with_user_friendly_shap_sections() -> None:
    detail = {
        msg_c.KEY_PREDICTION_PROBABILITY: 35.59,
        msg_c.KEY_RISK_LEVEL: pred_c.RISK_LEVEL_MEDIUM,
        msg_c.KEY_PREDICTION_TIMESTAMP: "2026-05-18T21:50:55",
        msg_c.KEY_GENERAL_HEALTH: "Good",
        msg_c.KEY_SMOKER_STATUS: "Never smoked",
        msg_c.KEY_SHAP_EXPLANATION: {
            msg_c.KEY_SHAP_FEATURE_NAME: "BMI",
            msg_c.KEY_SHAP_IMPACT_SCORE: 0.12,
            msg_c.KEY_SHAP_DIRECTION: ml_c.SHAP_DIRECTION_INCREASES_RISK,
            msg_c.KEY_SHAP_MESSAGE: ml_c.MSG_SHAP_INCREASES.format(feature="BMI"),
        },
        msg_c.KEY_SHAP_TOP_FACTORS: [],
        msg_c.KEY_RECOMMENDATIONS: [],
    }
    pdf_bytes = pdf_export_service.build_prediction_pdf_bytes(detail)
    assert pdf_bytes.startswith(b"%PDF")
    assert len(pdf_bytes) > 500


def test_pdf_value_formatters_use_spanish_labels() -> None:
    assert pdf_export_service._format_risk_level(pred_c.RISK_LEVEL_MEDIUM) == "Medio"
    assert (
        pdf_export_service._format_input_value(msg_c.KEY_GENERAL_HEALTH, "Good") == "Buena"
    )
    assert (
        pdf_export_service._format_input_value(msg_c.KEY_SMOKER_STATUS, "Never smoked")
        == "Nunca fumó"
    )
