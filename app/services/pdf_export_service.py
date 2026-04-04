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
    for c in pdf_c.FILENAME_INVALID_CHARS:
        out = out.replace(c, "-")
    out = out.replace(" ", pdf_c.FILENAME_SPACE_REPLACEMENT)
    if len(out) > pdf_c.FILENAME_TIMESTAMP_MAX_LEN:
        out = out[: pdf_c.FILENAME_TIMESTAMP_MAX_LEN]
    return out


def _p(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(escape(text), style)


def _format_value(val: Any) -> str:
    if val is None:
        return pdf_c.PDF_VALUE_NOT_AVAILABLE
    if isinstance(val, bool):
        return pdf_c.PDF_VALUE_YES if val else pdf_c.PDF_VALUE_NO
    if isinstance(val, float):
        fmt = f"{{:.{pdf_c.PDF_FLOAT_DECIMALS}f}}"
        s = fmt.format(val).rstrip(pdf_c.PDF_FLOAT_RSTRIP_TRAILING_ZERO).rstrip(
            pdf_c.PDF_FLOAT_RSTRIP_TRAILING_DOT
        )
        return s if s else pdf_c.PDF_FLOAT_ZERO_DISPLAY
    return str(val)


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
                value=_format_value(rl),
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
                pdf_c.PDF_LINE_LABEL_VALUE.format(label=label, value=_format_value(val)),
                body,
            )
        )

    story.append(_p(pdf_c.PDF_SECTION_SHAP, h2))
    shap = detail.get(msg_c.KEY_SHAP_EXPLANATION)
    if isinstance(shap, dict) and shap:
        story.append(
            _p(
                pdf_c.PDF_LINE_LABEL_VALUE.format(
                    label=pdf_c.PDF_LABEL_SHAP_FEATURE,
                    value=_format_value(shap.get(msg_c.KEY_SHAP_FEATURE_NAME)),
                ),
                body,
            )
        )
        story.append(
            _p(
                pdf_c.PDF_LINE_LABEL_VALUE.format(
                    label=pdf_c.PDF_LABEL_SHAP_IMPACT,
                    value=_format_value(shap.get(msg_c.KEY_SHAP_IMPACT_SCORE)),
                ),
                body,
            )
        )
        story.append(
            _p(
                pdf_c.PDF_LINE_LABEL_VALUE.format(
                    label=pdf_c.PDF_LABEL_SHAP_DIRECTION,
                    value=_format_value(shap.get(msg_c.KEY_SHAP_DIRECTION)),
                ),
                body,
            )
        )
        story.append(
            _p(
                pdf_c.PDF_LINE_LABEL_VALUE.format(
                    label=pdf_c.PDF_LABEL_SHAP_MESSAGE,
                    value=_format_value(shap.get(msg_c.KEY_SHAP_MESSAGE)),
                ),
                body,
            )
        )
    else:
        story.append(_p(pdf_c.PDF_SHAP_NOT_AVAILABLE, body))

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
