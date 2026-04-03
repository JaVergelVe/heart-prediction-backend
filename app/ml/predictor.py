"""Heart-risk inference: preprocess → MLP predict_proba → SHAP (single top feature)."""

from __future__ import annotations

import logging
from typing import Any

import numpy as np
import shap
from scipy import sparse
from app.constants import http as http_c
from app.constants import messages as msg_c
from app.constants import ml_inference as ml_c
from app.constants import validation as val_c
from app.core.exceptions import APIError
from app.ml.artifacts import load_ml_bundle
from app.ml.feature_row import build_training_row

logger = logging.getLogger(__name__)


class FeatureLayoutError(ValueError):
    """Preprocessed vector does not align with model / shap_background layout."""


def _to_dense2d(arr: Any) -> np.ndarray:
    if sparse.issparse(arr):
        return arr.toarray()
    out = np.asarray(arr, dtype=float)
    if out.ndim == 1:
        return out.reshape(1, -1)
    return out


def _ohe_feature_names(ohe: Any) -> list[str]:
    try:
        return list(ohe.get_feature_names_out(ml_c.ONE_HOT_FEATURE_NAMES))
    except Exception:
        return list(ohe.get_feature_names_out())


def _full_feature_names(bundle: Any) -> list[str]:
    if bundle.inference_feature_names is not None:
        return list(bundle.inference_feature_names)
    ohe = bundle.one_hot_encoder
    return (
        _ohe_feature_names(ohe)
        + list(ml_c.STANDARD_SCALE_FEATURE_NAMES)
        + list(ml_c.PASSTHROUGH_FEATURE_NAMES)
    )


def _feature_value_map(
    ohe_names: list[str],
    ohe_part: np.ndarray,
    num_part: np.ndarray,
    X_bin: np.ndarray,
) -> dict[str, float]:
    m: dict[str, float] = {}
    for i, name in enumerate(ohe_names):
        m[name] = float(ohe_part[0, i])
    for i, name in enumerate(ml_c.STANDARD_SCALE_FEATURE_NAMES):
        m[name] = float(num_part[0, i])
    for i, name in enumerate(ml_c.PASSTHROUGH_FEATURE_NAMES):
        m[name] = float(X_bin[0, i])
    return m


def _validate_feature_sets(
    value_map: dict[str, float],
    expected_order: tuple[str, ...],
) -> None:
    exp = set(expected_order)
    got = set(value_map.keys())
    if exp != got:
        missing = sorted(exp - got)
        extra = sorted(got - exp)
        raise FeatureLayoutError(
            f"Constructed features vs shap_background columns: "
            f"missing={missing[:20]}{'...' if len(missing) > 20 else ''} "
            f"extra={extra[:20]}{'...' if len(extra) > 20 else ''}"
        )


def _validate_width(X: np.ndarray, bundle: Any) -> None:
    n_bg = int(bundle.shap_background.shape[1])
    if int(X.shape[1]) != n_bg:
        raise FeatureLayoutError(
            f"Feature width {X.shape[1]} != shap_background width {n_bg}"
        )


def _build_X_matrix(row: dict[str, Any], bundle: Any) -> np.ndarray:
    ohe = bundle.one_hot_encoder
    scaler = bundle.standard_scaler
    X_cat = np.empty((1, len(ml_c.ONE_HOT_FEATURE_NAMES)), dtype=object)
    for j, name in enumerate(ml_c.ONE_HOT_FEATURE_NAMES):
        X_cat[0, j] = row[name]
    ohe_raw = ohe.transform(X_cat)
    ohe_part = _to_dense2d(ohe_raw)

    X_num = np.array(
        [[float(row[name]) for name in ml_c.STANDARD_SCALE_FEATURE_NAMES]],
        dtype=float,
    )
    num_part = scaler.transform(X_num)

    X_bin = np.array(
        [[float(row[name]) for name in ml_c.PASSTHROUGH_FEATURE_NAMES]],
        dtype=float,
    )

    ohe_names = _ohe_feature_names(ohe)
    expected = bundle.inference_feature_names

    if expected is None:
        X = np.hstack([ohe_part, num_part, X_bin])
        _validate_width(X, bundle)
        return X

    value_map = _feature_value_map(ohe_names, ohe_part, num_part, X_bin)
    _validate_feature_sets(value_map, expected)
    try:
        X = np.array([[value_map[name] for name in expected]], dtype=float)
    except KeyError as e:
        raise FeatureLayoutError(f"Missing feature column for layout: {e}") from e
    _validate_width(X, bundle)
    return X


def _predict_proba_matrix(model: Any, X: np.ndarray) -> np.ndarray:
    return model.predict_proba(X)


def _predicted_class_label(model: Any, proba_row: np.ndarray) -> str:
    idx = int(np.argmax(proba_row))
    classes = getattr(model, "classes_", None)
    if classes is not None and 0 <= idx < len(classes):
        return str(classes[idx])
    return str(idx)


def _top_shap_explanation(
    bundle: Any,
    X: np.ndarray,
    feature_names: list[str],
) -> dict[str, Any]:
    bg = bundle.shap_background
    if bg.ndim != 2:
        raise ValueError("shap_background must be 2D")
    n_bg = min(bg.shape[0], ml_c.SHAP_BACKGROUND_MAX_ROWS)
    bg_use = np.asarray(bg[:n_bg], dtype=float)

    model = bundle.model

    def model_positive_proba(z: np.ndarray) -> np.ndarray:
        p = _predict_proba_matrix(model, z)
        return p[:, ml_c.POSITIVE_CLASS_PROB_INDEX]

    explainer = shap.KernelExplainer(model_positive_proba, bg_use)
    sv = explainer.shap_values(X, nsamples=ml_c.SHAP_KERNEL_NSAMPLES)
    arr = np.asarray(sv)
    vec = np.ravel(arr[0]) if arr.ndim >= 2 else np.ravel(arr)
    if vec.shape[0] != len(feature_names):
        raise ValueError("SHAP vector length does not match feature name list")
    idx = int(np.argmax(np.abs(vec)))
    raw = float(vec[idx])
    impact = abs(raw)
    direction = (
        ml_c.SHAP_DIRECTION_INCREASES_RISK
        if raw >= 0
        else ml_c.SHAP_DIRECTION_DECREASES_RISK
    )
    fname = feature_names[idx]
    msg = (
        ml_c.MSG_SHAP_INCREASES.format(feature=fname)
        if raw >= 0
        else ml_c.MSG_SHAP_DECREASES.format(feature=fname)
    )
    return {
        msg_c.KEY_SHAP_FEATURE_NAME: fname,
        msg_c.KEY_SHAP_IMPACT_SCORE: round(impact, ml_c.SHAP_IMPACT_DECIMALS),
        msg_c.KEY_SHAP_DIRECTION: direction,
        msg_c.KEY_SHAP_MESSAGE: msg,
    }


def predict_heart_risk(features: dict[str, Any]) -> dict[str, Any]:
    """
    Run trained MLP on the feature bundle used by prediction_service.

    Returns keys aligned with msg_c / persistence: probability 0–100, predicted_class,
    model_version, shap_explanation (single dict).
    """
    try:
        bundle = load_ml_bundle()
    except FileNotFoundError as e:
        raise APIError(
            http_c.HTTP_503_SERVICE_UNAVAILABLE,
            code=msg_c.ERROR_CODE_INTERNAL,
            message=ml_c.ERROR_ML_ARTIFACTS_MISSING,
            details={"reason": str(e)},
        ) from e
    except Exception as e:
        logger.exception("ML artifact load failed")
        raise APIError(
            http_c.HTTP_500_INTERNAL_SERVER_ERROR,
            code=msg_c.ERROR_CODE_INTERNAL,
            message=ml_c.ERROR_ML_INFERENCE_FAILED,
            details={"reason": str(e)},
        ) from e

    try:
        row = build_training_row(features)
        X = _build_X_matrix(row, bundle)
        model = bundle.model
        if hasattr(model, "n_features_in_") and int(model.n_features_in_) != X.shape[1]:
            raise FeatureLayoutError(
                f"Feature width mismatch: model expects {model.n_features_in_}, got {X.shape[1]}"
            )
        proba = _predict_proba_matrix(model, X)[0]
        p_pos = float(proba[ml_c.POSITIVE_CLASS_PROB_INDEX])
        probability_100 = round(p_pos * 100.0, val_c.DB_PREDICTION_PROB_SCALE)
        pred_label = _predicted_class_label(model, proba)

        names = _full_feature_names(bundle)
        if len(names) != X.shape[1]:
            raise FeatureLayoutError("Feature name list width does not match X")
        try:
            shap_explanation = _top_shap_explanation(bundle, X, names)
        except Exception as e:
            logger.warning("SHAP explanation failed: %s", e)
            shap_explanation = {
                msg_c.KEY_SHAP_FEATURE_NAME: names[0] if names else "unknown",
                msg_c.KEY_SHAP_IMPACT_SCORE: 0.0,
                msg_c.KEY_SHAP_DIRECTION: ml_c.SHAP_DIRECTION_INCREASES_RISK,
                msg_c.KEY_SHAP_MESSAGE: ml_c.MSG_SHAP_FALLBACK,
            }
    except APIError:
        raise
    except FeatureLayoutError as e:
        logger.warning("ML feature layout validation failed: %s", e)
        raise APIError(
            http_c.HTTP_500_INTERNAL_SERVER_ERROR,
            code=msg_c.ERROR_CODE_INTERNAL,
            message=ml_c.ERROR_ML_FEATURE_LAYOUT_MISMATCH,
            details={"reason": str(e)},
        ) from e
    except Exception as e:
        logger.exception("ML inference failed")
        raise APIError(
            http_c.HTTP_500_INTERNAL_SERVER_ERROR,
            code=msg_c.ERROR_CODE_INTERNAL,
            message=ml_c.ERROR_ML_INFERENCE_FAILED,
            details={"reason": str(e)},
        ) from e

    return {
        msg_c.KEY_PREDICTION_PROBABILITY: probability_100,
        msg_c.KEY_PREDICTED_CLASS: pred_label,
        msg_c.KEY_MODEL_VERSION: ml_c.ML_MODEL_VERSION,
        msg_c.KEY_SHAP_EXPLANATION: shap_explanation,
    }


def predict_risk_probability(features: dict[str, Any]) -> float:
    """Backward-compatible alias: return probability 0–100 only."""
    return float(predict_heart_risk(features)[msg_c.KEY_PREDICTION_PROBABILITY])
