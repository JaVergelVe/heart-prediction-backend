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
    for c in '<>:"/\\|?*':
        out = out.replace(c, "-")
    out = out.replace(" ", "_")
    if len(out) > 180:
        out = out[:180]
    return out


def _p(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(escape(text), style)


def _format_value(val: Any) -> str:
    if val is None:
        return pdf_c.PDF_VALUE_NOT_AVAILABLE
    if isinstance(val, bool):
        return pdf_c.PDF_VALUE_YES if val else pdf_c.PDF_VALUE_NO
    if isinstance(val, float):
        s = f"{val:.4f}".rstrip("0").rstrip(".")
        return s if s else "0"
    return str(val)


def build_prediction_pdf_bytes(detail: dict[str, Any]) -> bytes:
    """Render prediction detail dict (same shape as GET /predictions/{id}) as PDF bytes."""
    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=letter,
        leftMargin=inch * 0.75,
        rightMargin=inch * 0.75,
        topMargin=inch * 0.75,
        bottomMargin=inch * 0.75,
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "title",
        parent=styles["Title"],
        fontSize=14,
        leading=18,
        spaceAfter=14,
    )
    h2 = ParagraphStyle(
        "h2",
        parent=styles["Heading2"],
        fontSize=12,
        leading=15,
        spaceBefore=10,
        spaceAfter=8,
    )
    body = ParagraphStyle(
        "body",
        parent=styles["Normal"],
        fontSize=10,
        leading=13,
        spaceAfter=6,
    )
    small = ParagraphStyle(
        "small",
        parent=styles["Normal"],
        fontSize=9,
        leading=12,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
    )

    story: list[Any] = []
    story.append(_p(pdf_c.PDF_TITLE, title_style))
    story.append(Spacer(1, 0.1 * inch))

    story.append(_p(pdf_c.PDF_SECTION_SUMMARY, h2))
    prob = detail.get(msg_c.KEY_PREDICTION_PROBABILITY)
    prob_line = (
        f"{pdf_c.PDF_LABEL_PROBABILITY}: {pdf_c.PDF_VALUE_NOT_AVAILABLE}"
        if prob is None
        else f"{pdf_c.PDF_LABEL_PROBABILITY}: {float(prob):.2f}{pdf_c.PDF_PROBABILITY_UNIT}"
    )
    story.append(_p(prob_line, body))
    rl = detail.get(msg_c.KEY_RISK_LEVEL)
    story.append(
        _p(
            f"{pdf_c.PDF_LABEL_RISK_LEVEL}: {_format_value(rl)}",
            body,
        )
    )
    ts = detail.get(msg_c.KEY_PREDICTION_TIMESTAMP)
    story.append(
        _p(
            f"{pdf_c.PDF_LABEL_PREDICTION_TIMESTAMP}: {_format_value(ts)}",
            body,
        )
    )

    story.append(_p(pdf_c.PDF_SECTION_INPUT_DATA, h2))
    for key, label in pdf_c.PDF_INPUT_FIELDS:
        val = detail.get(key)
        story.append(_p(f"{label}: {_format_value(val)}", body))

    story.append(_p(pdf_c.PDF_SECTION_SHAP, h2))
    shap = detail.get(msg_c.KEY_SHAP_EXPLANATION)
    if isinstance(shap, dict) and shap:
        story.append(
            _p(
                f"{pdf_c.PDF_LABEL_SHAP_FEATURE}: {_format_value(shap.get(msg_c.KEY_SHAP_FEATURE_NAME))}",
                body,
            )
        )
        story.append(
            _p(
                f"{pdf_c.PDF_LABEL_SHAP_IMPACT}: {_format_value(shap.get(msg_c.KEY_SHAP_IMPACT_SCORE))}",
                body,
            )
        )
        story.append(
            _p(
                f"{pdf_c.PDF_LABEL_SHAP_DIRECTION}: {_format_value(shap.get(msg_c.KEY_SHAP_DIRECTION))}",
                body,
            )
        )
        story.append(
            _p(
                f"{pdf_c.PDF_LABEL_SHAP_MESSAGE}: {_format_value(shap.get(msg_c.KEY_SHAP_MESSAGE))}",
                body,
            )
        )
    else:
        story.append(_p(pdf_c.PDF_SHAP_NOT_AVAILABLE, body))

    story.append(_p(pdf_c.PDF_SECTION_RECOMMENDATIONS, h2))
    recs = detail.get(msg_c.KEY_RECOMMENDATIONS) or []
    if isinstance(recs, list) and recs:
        for i, item in enumerate(recs, start=1):
            line = f"{i}. {_format_value(item)}"
            story.append(_p(line, body))
    else:
        story.append(_p(pdf_c.PDF_RECOMMENDATIONS_EMPTY, body))

    story.append(_p(pdf_c.PDF_SECTION_DISCLAIMER, h2))
    for para in pdf_c.PDF_DISCLAIMER_PARAGRAPHS:
        story.append(_p(para, small))

    doc.build(story)
    return buf.getvalue()
