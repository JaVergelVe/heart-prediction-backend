"""User-friendly SHAP narratives (aligned with frontend shap-display.util.ts)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from app.constants import messages as msg_c
from app.constants import shap_display as sd_c

ShapImpactKind = Literal["increase", "decrease", "neutral", "unknown"]


@dataclass(frozen=True)
class ShapFeatureIdentity:
    base_key: str
    suffix: str | None
    numeric_value: float | None
    is_truthy: bool | None


@dataclass(frozen=True)
class ShapFactorUserView:
    friendly_title: str
    impact_kind: ShapImpactKind
    impact_label: str
    intensity_label: str | None
    primary_explanation: str
    narrative_extra: str | None


@dataclass(frozen=True)
class ShapExplanationUserView:
    friendly_title: str
    impact_kind: ShapImpactKind
    impact_label: str
    primary_explanation: str
    narrative_extra: str | None


HAD_MEDICAL_PREFIX = "had"
TRUTHY_SUFFIXES = frozenset({"true", "1", "yes", "si", "sí"})
FALSY_SUFFIXES = frozenset({"false", "0", "no"})
BOOLEAN_HEALTH_FEATURES = frozenset(
    {
        "physicalactivities",
        "alcoholdrinkers",
        "chestscan",
        "hivtesting",
        "fluvaxlast12",
        "pneumovaxever",
        "highrisklastyear",
        "deaforhardofhearing",
        "blindorvisiondifficulty",
        "difficultyconcentrating",
        "difficultywalking",
        "difficultydressingbathing",
        "difficultyerrands",
    }
)


def normalize_shap_token(raw: str) -> str:
    return (
        raw.strip()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("__", "_")
        .lower()
    )


def _camel_to_snake_key(value: str) -> str:
    text = value.strip().replace(" ", "_").replace("-", "_")
    out: list[str] = []
    for i, ch in enumerate(text):
        if ch.isupper() and i > 0 and (text[i - 1].islower() or text[i - 1].isdigit()):
            out.append("_")
        out.append(ch.lower())
    return "".join(out).replace("__", "_")


def _title_from_exact_or_snake(raw: str) -> str | None:
    normalized = normalize_shap_token(raw)
    if normalized in sd_c.SHAP_FEATURE_TITLE_MAP:
        return sd_c.SHAP_FEATURE_TITLE_MAP[normalized]
    snake = _camel_to_snake_key(raw)
    return sd_c.SHAP_FEATURE_TITLE_MAP.get(snake)


def _parse_numeric_suffix(suffix: str) -> float | None:
    try:
        return float(suffix.replace("_", "."))
    except ValueError:
        return None


def _resolve_boolean_from_suffix(suffix: str | None) -> bool | None:
    if suffix is None:
        return None
    token = normalize_shap_token(suffix)
    if token in TRUTHY_SUFFIXES:
        return True
    if token in FALSY_SUFFIXES:
        return False
    return None


def _resolve_boolean_from_value(value: float | None) -> bool | None:
    if value is None:
        return None
    if value == 1:
        return True
    if value == 0:
        return False
    return None


def parse_shap_feature_identity(
    feature_name: str | None,
    feature_value: float | None = None,
) -> ShapFeatureIdentity:
    normalized = normalize_shap_token(feature_name or "")
    value_from_field = float(feature_value) if feature_value is not None else None

    keys = sorted(sd_c.SHAP_COMPOUND_CATEGORY_PREFIX.keys(), key=len, reverse=True)
    for cat in keys:
        if normalized == cat:
            return ShapFeatureIdentity(
                base_key=cat,
                suffix=None,
                numeric_value=value_from_field,
                is_truthy=_resolve_boolean_from_value(value_from_field),
            )
        prefix = f"{cat}_"
        if normalized.startswith(prefix):
            suffix = normalized[len(prefix) :] or None
            suffix_bool = _resolve_boolean_from_suffix(suffix)
            value_bool = _resolve_boolean_from_value(value_from_field)
            return ShapFeatureIdentity(
                base_key=cat,
                suffix=suffix,
                numeric_value=value_from_field
                if value_from_field is not None
                else (_parse_numeric_suffix(suffix) if suffix else None),
                is_truthy=suffix_bool if suffix_bool is not None else value_bool,
            )

    return ShapFeatureIdentity(
        base_key=normalized,
        suffix=None,
        numeric_value=value_from_field,
        is_truthy=_resolve_boolean_from_value(value_from_field),
    )


def _is_had_medical_feature(base_key: str) -> bool:
    return base_key.startswith(HAD_MEDICAL_PREFIX) and base_key != "haddiabetes"


def _medical_condition_phrase(base_key: str) -> str | None:
    title = sd_c.SHAP_FEATURE_TITLE_MAP.get(base_key)
    if not title:
        return None
    lower = title.lower()
    prefix = "antecedentes de "
    if lower.startswith(prefix):
        return lower[len(prefix) :]
    return None


def _suffix_implies_non_smoker(suffix: str | None) -> bool:
    if not suffix:
        return False
    token = normalize_shap_token(suffix)
    return any(
        part in token
        for part in ("never", "nunca", "former", "exfum", "no")
    )


def _suffix_implies_current_smoker(suffix: str | None) -> bool:
    if not suffix:
        return False
    token = normalize_shap_token(suffix)
    return any(
        part in token
        for part in ("current", "actual", "every_day", "some_days")
    )


def _age_group_detail_label(suffix: str | None) -> str | None:
    if not suffix:
        return None
    return sd_c.SHAP_AGE_CATEGORY_SUFFIX_LABELS.get(suffix) or sd_c.SHAP_AGE_CATEGORY_SUFFIX_LABELS.get(
        normalize_shap_token(suffix)
    )


def _compound_value_label(base_key: str, suffix: str | None) -> str | None:
    if not suffix:
        return None
    table = sd_c.SHAP_COMPOUND_VALUE_LABELS.get(base_key)
    if not table:
        return None
    return table.get(suffix) or table.get(normalize_shap_token(suffix))


def _format_numeric_for_display(value: float) -> str:
    if float(value).is_integer():
        return str(int(value))
    text = f"{value:.1f}".rstrip("0").rstrip(".")
    return text


def classify_shap_direction(direction: str | None) -> ShapImpactKind:
    if direction is None or str(direction).strip() == "":
        return "unknown"
    token = normalize_shap_token(str(direction))
    mapped = sd_c.SHAP_DIRECTION_TO_KIND.get(token)
    if mapped:
        return mapped if mapped != "neutral" else "neutral"  # type: ignore[return-value]
    if "increase" in token and "risk" in token:
        return "increase"
    if "decrease" in token and "risk" in token:
        return "decrease"
    return "unknown"


def shap_impact_label(kind: ShapImpactKind) -> str:
    ui = sd_c.SHAP_DISPLAY_UI
    if kind == "increase":
        return str(ui["impactIncrease"])
    if kind == "decrease":
        return str(ui["impactDecrease"])
    if kind == "neutral":
        return str(ui["impactNeutral"])
    return str(ui["impactUnknown"])


def shap_primary_explanation(kind: ShapImpactKind) -> str:
    ui = sd_c.SHAP_DISPLAY_UI
    if kind == "increase":
        return str(ui["explanationIncrease"])
    if kind == "decrease":
        return str(ui["explanationDecrease"])
    return str(ui["explanationNeutral"])


def interpretation_looks_technical(text: str) -> bool:
    lowered = text.lower()
    hints = sd_c.SHAP_DISPLAY_UI["technicalInterpretationHints"]
    assert isinstance(hints, tuple)
    return any(hint in lowered for hint in hints)


def max_abs_shap_contribution(factors: list[dict[str, Any]]) -> float:
    maximum = 0.0
    for factor in factors:
        score = factor.get(msg_c.KEY_SHAP_CONTRIBUTION_SCORE)
        if score is None:
            continue
        try:
            absolute = abs(float(score))
        except (TypeError, ValueError):
            continue
        if absolute > maximum:
            maximum = absolute
    return maximum


def shap_relative_intensity_label(abs_score: float, batch_max_abs: float) -> str | None:
    if batch_max_abs <= 0 or abs_score <= 0:
        return None
    ratio = abs_score / batch_max_abs
    ui = sd_c.SHAP_DISPLAY_UI
    if ratio >= sd_c.SHAP_INTENSITY_RELATIVE_THRESHOLDS["high"]:
        return str(ui["intensityHigh"])
    if ratio >= sd_c.SHAP_INTENSITY_RELATIVE_THRESHOLDS["medium"]:
        return str(ui["intensityMedium"])
    return str(ui["intensityLow"])


def _compound_friendly_title(normalized_full: str) -> str | None:
    keys = sorted(sd_c.SHAP_COMPOUND_CATEGORY_PREFIX.keys(), key=len, reverse=True)
    for cat in keys:
        if normalized_full == cat:
            return sd_c.SHAP_COMPOUND_CATEGORY_PREFIX[cat]
        prefix = f"{cat}_"
        if not normalized_full.startswith(prefix):
            continue
        suffix = normalized_full[len(prefix) :]
        if not suffix:
            return sd_c.SHAP_COMPOUND_CATEGORY_PREFIX[cat]
        category_title = sd_c.SHAP_COMPOUND_CATEGORY_PREFIX[cat]
        value_table = sd_c.SHAP_COMPOUND_VALUE_LABELS.get(cat)
        if value_table and suffix in value_table:
            return f"{category_title}: {value_table[suffix]}"
        if cat == "agecategory":
            age_label = _age_group_detail_label(suffix)
            if age_label:
                return f"{category_title}: {age_label}"
        bool_label = sd_c.SHAP_BOOLEAN_VALUE_LABELS.get(suffix) or sd_c.SHAP_BOOLEAN_VALUE_LABELS.get(
            normalize_shap_token(suffix)
        )
        if bool_label:
            return f"{category_title}: {bool_label}"
        readable = suffix.replace("_", " ").strip()
        pretty = " ".join(word.capitalize() for word in readable.split())
        return f"{category_title}: {pretty}"
    return None


def shap_friendly_feature_title(feature_name: str | None) -> str:
    raw = (feature_name or "").strip()
    if not raw:
        return str(sd_c.SHAP_DISPLAY_UI["fallbackUnknownFeature"])
    exact = _title_from_exact_or_snake(raw)
    if exact:
        return exact
    normalized = normalize_shap_token(raw)
    compound = _compound_friendly_title(normalized)
    if compound:
        return compound
    readable = normalized.replace("_", " ").strip()
    if readable:
        return " ".join(word.capitalize() for word in readable.split())
    return str(sd_c.SHAP_DISPLAY_UI["fallbackUnknownFeature"])


def _narrative_for_had_medical(phrase: str, is_truthy: bool, kind: ShapImpactKind) -> str | None:
    if kind not in ("increase", "decrease"):
        return None
    if not is_truthy and kind == "decrease":
        return f"No presentar antecedentes de {phrase} contribuyó a reducir el riesgo estimado."
    if is_truthy and kind == "increase":
        return f"Presentar antecedentes de {phrase} se asoció con un mayor riesgo estimado."
    if not is_truthy and kind == "increase":
        return f"No presentar antecedentes de {phrase} se asoció con un mayor riesgo estimado."
    if is_truthy and kind == "decrease":
        return f"Presentar antecedentes de {phrase} contribuyó a reducir el riesgo estimado."
    return None


def _narrative_for_physical_activities(is_truthy: bool, kind: ShapImpactKind) -> str | None:
    if is_truthy and kind == "decrease":
        return "Realizar actividad física contribuyó a reducir el riesgo estimado."
    if not is_truthy and kind == "increase":
        return "No reportar actividad física se asoció con un mayor riesgo estimado."
    if is_truthy and kind == "increase":
        return "Reportar actividad física se asoció con un mayor riesgo estimado."
    if not is_truthy and kind == "decrease":
        return "No reportar actividad física contribuyó a reducir el riesgo estimado."
    return None


def _narrative_for_boolean_health_feature(
    base_key: str,
    is_truthy: bool,
    kind: ShapImpactKind,
) -> str | None:
    if base_key == "physicalactivities":
        return _narrative_for_physical_activities(is_truthy, kind)
    title = sd_c.SHAP_FEATURE_TITLE_MAP.get(base_key) or sd_c.SHAP_COMPOUND_CATEGORY_PREFIX.get(base_key)
    if not title:
        return None
    label = title.lower()
    if kind == "increase" and is_truthy:
        return f"Reportar {label} se asoció con un mayor riesgo estimado."
    if kind == "decrease" and not is_truthy:
        return f"No reportar {label} contribuyó a reducir el riesgo estimado."
    if kind == "increase" and not is_truthy:
        return f"No reportar {label} se asoció con un mayor riesgo estimado."
    if kind == "decrease" and is_truthy:
        return f"Reportar {label} contribuyó a reducir el riesgo estimado."
    return None


def build_contextual_shap_narrative(
    identity: ShapFeatureIdentity,
    kind: ShapImpactKind,
) -> tuple[str, str | None]:
    base_key = identity.base_key
    suffix = identity.suffix
    numeric_value = identity.numeric_value
    is_truthy = identity.is_truthy

    if base_key == "sleephours":
        detail = (
            f"En tu registro constan {_format_numeric_for_display(numeric_value)} horas de sueño en promedio."
            if numeric_value is not None
            else None
        )
        return (
            "La cantidad de horas de sueño registrada tuvo una influencia importante en el riesgo estimado.",
            detail,
        )

    if base_key == "agecategory":
        age_label = _age_group_detail_label(suffix)
        detail = (
            f"Corresponde al grupo de {age_label.replace('De ', '').lower()}."
            if age_label
            else None
        )
        if kind == "decrease":
            return ("Tu grupo de edad se asoció con un menor riesgo cardiovascular estimado.", detail)
        if kind == "increase":
            return ("Tu grupo de edad se asoció con un mayor riesgo cardiovascular estimado.", detail)

    if base_key == "smokerstatus":
        if _suffix_implies_non_smoker(suffix) and kind == "decrease":
            value_label = _compound_value_label(base_key, suffix)
            detail = f"Respuesta registrada: {value_label}." if value_label else None
            return ("El estado de no fumador contribuyó a reducir el riesgo estimado.", detail)
        if _suffix_implies_current_smoker(suffix) and kind == "increase":
            value_label = _compound_value_label(base_key, suffix)
            detail = f"Respuesta registrada: {value_label}." if value_label else None
            return ("El consumo actual de tabaco se asoció con un mayor riesgo estimado.", detail)
        if _suffix_implies_non_smoker(suffix) and kind == "increase":
            return (
                "El perfil de no fumador se asoció con un mayor riesgo estimado en esta estimación.",
                None,
            )
        if _suffix_implies_current_smoker(suffix) and kind == "decrease":
            return (
                "El consumo de tabaco registrado contribuyó a reducir el riesgo estimado en este cálculo.",
                None,
            )

    if base_key == "bmi" and numeric_value is not None:
        if numeric_value >= sd_c.SHAP_BMI_ELEVATED_THRESHOLD and kind == "increase":
            return (
                "Un IMC elevado se asoció con un mayor riesgo estimado.",
                f"IMC registrado: {_format_numeric_for_display(numeric_value)}.",
            )
        if numeric_value < sd_c.SHAP_BMI_ELEVATED_THRESHOLD and kind == "decrease":
            return (
                "Un IMC en rango no elevado contribuyó a reducir el riesgo estimado.",
                f"IMC registrado: {_format_numeric_for_display(numeric_value)}.",
            )
        if numeric_value >= sd_c.SHAP_BMI_ELEVATED_THRESHOLD and kind == "decrease":
            return (
                "El IMC registrado contribuyó a reducir el riesgo estimado en este cálculo.",
                f"IMC registrado: {_format_numeric_for_display(numeric_value)}.",
            )

    if is_truthy is not None:
        if _is_had_medical_feature(base_key):
            phrase = _medical_condition_phrase(base_key)
            if phrase:
                specific = _narrative_for_had_medical(phrase, is_truthy, kind)
                if specific:
                    return specific, None
        if base_key in BOOLEAN_HEALTH_FEATURES or base_key == "physicalactivities":
            specific = _narrative_for_boolean_health_feature(base_key, is_truthy, kind)
            if specific:
                return specific, None

    compound_label = _compound_value_label(base_key, suffix) if suffix else None
    if compound_label and kind in ("increase", "decrease"):
        category_title = sd_c.SHAP_COMPOUND_CATEGORY_PREFIX.get(base_key) or sd_c.SHAP_FEATURE_TITLE_MAP.get(
            base_key
        )
        if category_title:
            if kind == "increase":
                primary = f"{category_title} ({compound_label}) se asoció con un mayor riesgo estimado."
            else:
                primary = f"{category_title} ({compound_label}) se asoció con una reducción del riesgo estimado."
            return primary, None

    return shap_primary_explanation(kind), None


def _pick_narrative_extra(
    generated_detail: str | None,
    api_text: str | None,
    friendly_title: str,
    primary_explanation: str,
) -> str | None:
    if generated_detail and generated_detail != primary_explanation:
        return generated_detail
    interp = (api_text or "").strip()
    if (
        interp
        and not interpretation_looks_technical(interp)
        and interp not in (friendly_title, primary_explanation)
    ):
        return interp
    return None


def build_shap_explanation_user_view(explanation: dict[str, Any]) -> ShapExplanationUserView:
    friendly_title = shap_friendly_feature_title(explanation.get(msg_c.KEY_SHAP_FEATURE_NAME))
    impact_kind = classify_shap_direction(explanation.get(msg_c.KEY_SHAP_DIRECTION))
    impact_label = shap_impact_label(impact_kind)
    identity = parse_shap_feature_identity(explanation.get(msg_c.KEY_SHAP_FEATURE_NAME))
    primary_explanation, detail = build_contextual_shap_narrative(identity, impact_kind)
    message = explanation.get(msg_c.KEY_SHAP_MESSAGE)
    narrative_extra = _pick_narrative_extra(
        detail,
        str(message) if message is not None else None,
        friendly_title,
        primary_explanation,
    )
    return ShapExplanationUserView(
        friendly_title=friendly_title,
        impact_kind=impact_kind,
        impact_label=impact_label,
        primary_explanation=primary_explanation,
        narrative_extra=narrative_extra,
    )


def build_shap_factor_user_view(
    factor: dict[str, Any],
    batch_max_abs: float,
) -> ShapFactorUserView:
    friendly_title = shap_friendly_feature_title(factor.get(msg_c.KEY_SHAP_FEATURE_NAME))
    impact_kind = classify_shap_direction(factor.get(msg_c.KEY_SHAP_DIRECTION))
    impact_label = shap_impact_label(impact_kind)
    feature_value = factor.get(msg_c.KEY_SHAP_FEATURE_VALUE)
    numeric_value = float(feature_value) if feature_value is not None else None
    identity = parse_shap_feature_identity(
        factor.get(msg_c.KEY_SHAP_FEATURE_NAME),
        numeric_value,
    )
    primary_explanation, detail = build_contextual_shap_narrative(identity, impact_kind)
    interpretation = factor.get(msg_c.KEY_SHAP_INTERPRETATION)
    narrative_extra = _pick_narrative_extra(
        detail,
        str(interpretation) if interpretation is not None else None,
        friendly_title,
        primary_explanation,
    )
    contrib = factor.get(msg_c.KEY_SHAP_CONTRIBUTION_SCORE)
    abs_contrib = abs(float(contrib)) if contrib is not None else 0.0
    intensity_label = (
        shap_relative_intensity_label(abs_contrib, batch_max_abs) if abs_contrib > 0 else None
    )
    return ShapFactorUserView(
        friendly_title=friendly_title,
        impact_kind=impact_kind,
        impact_label=impact_label,
        intensity_label=intensity_label,
        primary_explanation=primary_explanation,
        narrative_extra=narrative_extra,
    )
