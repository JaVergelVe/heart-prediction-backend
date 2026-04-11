"""Thread-safe lazy loading of joblib ML artifacts."""

from __future__ import annotations

import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import numpy as np

from app.constants import ml_inference as ml_c
from app.core.config import get_settings


def _shap_background_to_array_and_names(
    raw: Any,
) -> tuple[np.ndarray, tuple[str, ...] | None]:
    """
    Prefer pandas DataFrame columns as canonical feature order (matches training / SHAP).
    Plain ndarray → values only; order follows manual hstack in predictor.
    """
    if hasattr(raw, "columns") and hasattr(raw, "to_numpy"):
        cols = tuple(str(c) for c in raw.columns)
        arr = np.asarray(raw.to_numpy(dtype=float), dtype=float)
        return arr, cols
    arr = np.asarray(raw, dtype=float)
    if arr.ndim != 2:
        raise ValueError("shap_background must be 2-dimensional")
    return arr, None


@dataclass(frozen=True)
class MLArtifactBundle:
    """Loaded sklearn / SHAP resources (paths resolved at load time)."""

    model: Any
    one_hot_encoder: Any
    standard_scaler: Any
    label_encoder: Any
    shap_background: np.ndarray
    inference_feature_names: tuple[str, ...] | None
    models_dir: Path


_lock = threading.Lock()
_bundle: MLArtifactBundle | None = None


def _resolve_models_dir() -> Path:
    settings = get_settings()
    if getattr(settings, "ml_models_dir", None):
        return Path(settings.ml_models_dir).resolve()
    return ml_c.default_models_dir()


def _require_file(path: Path) -> None:
    if not path.is_file():
        raise FileNotFoundError(str(path))


def _load_impl() -> MLArtifactBundle:
    root = _resolve_models_dir()
    p_model = root / ml_c.ML_ARTIFACT_MODEL
    p_ohe = root / ml_c.ML_ARTIFACT_ONE_HOT_ENCODER
    p_scaler = root / ml_c.ML_ARTIFACT_STANDARD_SCALER
    p_le = root / ml_c.ML_ARTIFACT_LABEL_ENCODER
    p_bg = root / ml_c.ML_ARTIFACT_SHAP_BACKGROUND
    for p in (p_model, p_ohe, p_scaler, p_le, p_bg):
        _require_file(p)
    model = joblib.load(p_model)
    ohe = joblib.load(p_ohe)
    scaler = joblib.load(p_scaler)
    label_enc = joblib.load(p_le)
    bg_raw = joblib.load(p_bg)
    bg, inf_names = _shap_background_to_array_and_names(bg_raw)
    n_feat = int(bg.shape[1])
    n_model = getattr(model, "n_features_in_", None)
    if n_model is not None and int(n_model) != n_feat:
        raise ValueError(
            f"Model n_features_in_ ({n_model}) != shap_background columns ({n_feat})"
        )
    return MLArtifactBundle(
        model=model,
        one_hot_encoder=ohe,
        standard_scaler=scaler,
        label_encoder=label_enc,
        shap_background=bg,
        inference_feature_names=inf_names,
        models_dir=root,
    )


def load_ml_bundle() -> MLArtifactBundle:
    """Return cached bundle, loading from disk on first use."""
    global _bundle
    with _lock:
        if _bundle is None:
            _bundle = _load_impl()
        return _bundle
