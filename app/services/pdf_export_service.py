"""Build PDF bytes for prediction export (simple ReportLab layout)."""

from __future__ import annotations

from io import BytesIO
from typing import Any
from xml.sax.saxutils import escape

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from app.constants import messages as msg_c
from app.constants import pdf_export as pdf_c
from app.constants import shap_display as sd_c
from app.utils import shap_display as shap_util


def build_export_filename(*, prediction_id: str, prediction_timestamp_iso: str | None) -> str:
    """Return a clear, filesystem-safe download filename."""
    ts = _timestamp_for_filename(prediction_timestamp_iso)
    return pdf_c.FILENAME_TEMPLATE.format(
        prefix=pdf_c.FILENAME_PREFIX,
        prediction_id=prediction_id,
        timestamp=ts,
    )


def _timestamp_for_filename(iso: str | None) -> str:
    if not iso:
        return pdf_c.FILENAME_TIMESTAMP_UNKNOWN
    out = iso.strip()
    for c in pdf_c.FILENAME_INVALID_CHARS:
        out = out.replace(c, "-")
    out = out.replace(" ", pdf_c.FILENAME_SPACE_REPLACEMENT)
    if len(out) > pdf_c.FILENAME_TIMESTAMP_MAX_LEN:
        out = out[: pdf_c.FILENAME_TIMESTAMP_MAX_LEN]
    return out


def _p(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(escape(text), style)


def _format_float(val: float) -> str:
    fmt = f"{{:.{pdf_c.PDF_FLOAT_DECIMALS}f}}"
    s = fmt.format(val).rstrip(pdf_c.PDF_FLOAT_RSTRIP_TRAILING_ZERO).rstrip(
        pdf_c.PDF_FLOAT_RSTRIP_TRAILING_DOT
    )
    return s if s else pdf_c.PDF_FLOAT_ZERO_DISPLAY


def _format_risk_level(value: Any) -> str:
    if value is None:
        return pdf_c.PDF_VALUE_NOT_AVAILABLE
    text = str(value).strip()
    if not text:
        return pdf_c.PDF_VALUE_NOT_AVAILABLE
    return sd_c.RISK_LEVEL_DISPLAY_LABELS.get(text, text)


def _format_input_value(field_key: str, val: Any) -> str:
    if val is None:
        return pdf_c.PDF_VALUE_NOT_AVAILABLE
    if isinstance(val, bool):
        return pdf_c.PDF_VALUE_YES if val else pdf_c.PDF_VALUE_NO
    if isinstance(val, float):
        return _format_float(val)
    if isinstance(val, int):
        return str(val)
    text = str(val).strip()
    if not text:
        return pdf_c.PDF_VALUE_NOT_AVAILABLE
    field_labels = pdf_c.PDF_SURVEY_VALUE_LABELS.get(field_key)
    if field_labels and text in field_labels:
        return field_labels[text]
    return text


def _format_value(val: Any) -> str:
    if val is None:
        return pdf_c.PDF_VALUE_NOT_AVAILABLE
    if isinstance(val, bool):
        return pdf_c.PDF_VALUE_YES if val else pdf_c.PDF_VALUE_NO
    if isinstance(val, float):
        return _format_float(val)
    return str(val)


def _append_shap_factor_block(
    story: list[Any],
    *,
    title: str,
    impact_label: str,
    primary_explanation: str,
    narrative_extra: str | None,
    intensity_label: str | None,
    body: ParagraphStyle,
    factor_title: ParagraphStyle,
) -> None:
    story.append(_p(title, factor_title))
    story.append(
        _p(
            pdf_c.PDF_LINE_LABEL_VALUE.format(
                label=pdf_c.PDF_LABEL_SHAP_IMPACT,
                value=impact_label,
            ),
            body,
        )
    )
    if intensity_label:
        story.append(_p(intensity_label, body))
    story.append(_p(primary_explanation, body))
    if narrative_extra:
        story.append(
            _p(
                f"{pdf_c.PDF_LABEL_SHAP_MORE_DETAIL}: {narrative_extra}",
                body,
            )
        )


def _append_shap_sections(
    story: list[Any],
    detail: dict[str, Any],
    *,
    h2: ParagraphStyle,
    h3: ParagraphStyle,
    body: ParagraphStyle,
    small: ParagraphStyle,
) -> None:
    story.append(_p(pdf_c.PDF_SECTION_SHAP, h2))
    story.append(_p(str(sd_c.SHAP_DISPLAY_UI["sectionDisclaimer"]), small))

    shap = detail.get(msg_c.KEY_SHAP_EXPLANATION)
    top_factors = detail.get(msg_c.KEY_SHAP_TOP_FACTORS) or []
    if not isinstance(top_factors, list):
        top_factors = []

    has_main = isinstance(shap, dict) and bool(shap)
    has_factors = bool(top_factors)

    if not has_main and not has_factors:
        story.append(_p(pdf_c.PDF_SHAP_NOT_AVAILABLE, body))
        return

    if has_main:
        view = shap_util.build_shap_explanation_user_view(shap)
        story.append(_p(pdf_c.PDF_SECTION_SHAP_MAIN, h3))
        _append_shap_factor_block(
            story,
            title=view.friendly_title,
            impact_label=view.impact_label,
            primary_explanation=view.primary_explanation,
            narrative_extra=view.narrative_extra,
            intensity_label=None,
            body=body,
            factor_title=h3,
        )

    if has_factors:
        story.append(_p(pdf_c.PDF_SECTION_SHAP_FACTORS, h3))
        batch_max = shap_util.max_abs_shap_contribution(top_factors)
        for factor in top_factors:
            if not isinstance(factor, dict):
                continue
            view = shap_util.build_shap_factor_user_view(factor, batch_max)
            rank = factor.get(msg_c.KEY_SHAP_RANK)
            if rank is not None:
                title = pdf_c.PDF_LINE_SHAP_FACTOR_RANK.format(
                    rank=rank,
                    title=view.friendly_title,
                )
            else:
                title = view.friendly_title
            _append_shap_factor_block(
                story,
                title=title,
                impact_label=view.impact_label,
                primary_explanation=view.primary_explanation,
                narrative_extra=view.narrative_extra,
                intensity_label=view.intensity_label,
                body=body,
                factor_title=h3,
            )


def build_prediction_pdf_bytes(detail: dict[str, Any]) -> bytes:
    """Render prediction detail dict (same shape as GET /predictions/{id}) as PDF bytes."""
    buf = BytesIO()
    margin = inch * pdf_c.PDF_PAGE_MARGIN_INCHES
    doc = SimpleDocTemplate(
        buf,
        pagesize=letter,
        leftMargin=margin,
        rightMargin=margin,
        topMargin=margin,
        bottomMargin=margin,
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        pdf_c.PDF_PARAGRAPH_STYLE_NAME_TITLE,
        parent=styles["Title"],
        fontSize=pdf_c.PDF_FONT_TITLE,
        leading=pdf_c.PDF_FONT_TITLE_LEADING,
        spaceAfter=pdf_c.PDF_FONT_TITLE_SPACE_AFTER,
    )
    h2 = ParagraphStyle(
        pdf_c.PDF_PARAGRAPH_STYLE_NAME_H2,
        parent=styles["Heading2"],
        fontSize=pdf_c.PDF_FONT_H2,
        leading=pdf_c.PDF_FONT_H2_LEADING,
        spaceBefore=pdf_c.PDF_FONT_H2_SPACE_BEFORE,
        spaceAfter=pdf_c.PDF_FONT_H2_SPACE_AFTER,
    )
    h3 = ParagraphStyle(
        "pdf_h3",
        parent=styles["Heading3"],
        fontSize=pdf_c.PDF_FONT_H2 - 1,
        leading=pdf_c.PDF_FONT_H2_LEADING,
        spaceBefore=6,
        spaceAfter=4,
    )
    body = ParagraphStyle(
        pdf_c.PDF_PARAGRAPH_STYLE_NAME_BODY,
        parent=styles["Normal"],
        fontSize=pdf_c.PDF_FONT_BODY,
        leading=pdf_c.PDF_FONT_BODY_LEADING,
        spaceAfter=pdf_c.PDF_FONT_BODY_SPACE_AFTER,
    )
    small = ParagraphStyle(
        pdf_c.PDF_PARAGRAPH_STYLE_NAME_SMALL,
        parent=styles["Normal"],
        fontSize=pdf_c.PDF_FONT_DISCLAIMER,
        leading=pdf_c.PDF_FONT_DISCLAIMER_LEADING,
        alignment=TA_JUSTIFY,
        spaceAfter=pdf_c.PDF_FONT_DISCLAIMER_SPACE_AFTER,
    )

    story: list[Any] = []
    story.append(_p(pdf_c.PDF_TITLE, title_style))
    story.append(Spacer(1, pdf_c.PDF_TITLE_BOTTOM_SPACER_INCHES * inch))

    story.append(_p(pdf_c.PDF_SECTION_SUMMARY, h2))
    prob = detail.get(msg_c.KEY_PREDICTION_PROBABILITY)
    if prob is None:
        prob_line = pdf_c.PDF_LINE_LABEL_VALUE.format(
            label=pdf_c.PDF_LABEL_PROBABILITY,
            value=pdf_c.PDF_VALUE_NOT_AVAILABLE,
        )
    else:
        prob_fmt = f"{{:.{pdf_c.PDF_PROBABILITY_DECIMALS}f}}"
        prob_line = pdf_c.PDF_LINE_PROBABILITY.format(
            label=pdf_c.PDF_LABEL_PROBABILITY,
            value=prob_fmt.format(float(prob)),
            unit=pdf_c.PDF_PROBABILITY_UNIT,
        )
    story.append(_p(prob_line, body))
    rl = detail.get(msg_c.KEY_RISK_LEVEL)
    story.append(
        _p(
            pdf_c.PDF_LINE_LABEL_VALUE.format(
                label=pdf_c.PDF_LABEL_RISK_LEVEL,
                value=_format_risk_level(rl),
            ),
            body,
        )
    )
    ts = detail.get(msg_c.KEY_PREDICTION_TIMESTAMP)
    story.append(
        _p(
            pdf_c.PDF_LINE_LABEL_VALUE.format(
                label=pdf_c.PDF_LABEL_PREDICTION_TIMESTAMP,
                value=_format_value(ts),
            ),
            body,
        )
    )

    story.append(_p(pdf_c.PDF_SECTION_INPUT_DATA, h2))
    for key, label in pdf_c.PDF_INPUT_FIELDS:
        val = detail.get(key)
        story.append(
            _p(
                pdf_c.PDF_LINE_LABEL_VALUE.format(
                    label=label,
                    value=_format_input_value(key, val),
                ),
                body,
            )
        )

    _append_shap_sections(story, detail, h2=h2, h3=h3, body=body, small=small)

    story.append(_p(pdf_c.PDF_SECTION_RECOMMENDATIONS, h2))
    recs = detail.get(msg_c.KEY_RECOMMENDATIONS) or []
    if isinstance(recs, list) and recs:
        for i, item in enumerate(recs, start=1):
            line = pdf_c.PDF_LINE_RECOMMENDATION_ITEM.format(
                index=i,
                text=_format_value(item),
            )
            story.append(_p(line, body))
    else:
        story.append(_p(pdf_c.PDF_RECOMMENDATIONS_EMPTY, body))

    story.append(_p(pdf_c.PDF_SECTION_DISCLAIMER, h2))
    for para in pdf_c.PDF_DISCLAIMER_PARAGRAPHS:
        story.append(_p(para, small))

    doc.build(story)
    return buf.getvalue()
