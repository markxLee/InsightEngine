#!/usr/bin/env python3
"""Generate a professional PDF document from JSON content data.

Usage:
    python3 gen_pdf.py --input content.json --output report.pdf --style corporate
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.colors import HexColor, white
    from reportlab.lib.units import cm, mm
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        PageBreak, HRFlowable
    )
except ImportError:
    print("Error: reportlab not installed. Run: pip3 install reportlab", file=sys.stderr)
    sys.exit(1)

STYLES = {
    "corporate": {
        "heading_color": "#1A365D",
        "accent_color": "#3182CE",
        "text_color": "#2D3748",
        "font_heading": "Helvetica-Bold",
        "font_body": "Helvetica",
        "table_header_bg": "#1A365D",
        "table_stripe_bg": "#EBF5FB",
    },
    "academic": {
        "heading_color": "#1A202C",
        "accent_color": "#744210",
        "text_color": "#1A202C",
        "font_heading": "Times-Bold",
        "font_body": "Times-Roman",
        "table_header_bg": "#744210",
        "table_stripe_bg": "#FFF8E1",
    },
    "minimal": {
        "heading_color": "#111827",
        "accent_color": "#059669",
        "text_color": "#374151",
        "font_heading": "Helvetica-Bold",
        "font_body": "Helvetica",
        "table_header_bg": "#059669",
        "table_stripe_bg": "#F0FDF4",
    },
}


def build_styles(style_name):
    """Build reportlab ParagraphStyles from style config."""
    s = STYLES.get(style_name, STYLES["corporate"])
    base = getSampleStyleSheet()

    styles = {
        "title": ParagraphStyle(
            "CustomTitle", parent=base["Title"],
            fontName=s["font_heading"], fontSize=22,
            textColor=HexColor(s["heading_color"]),
            alignment=TA_CENTER, spaceAfter=6,
        ),
        "h1": ParagraphStyle(
            "CustomH1", parent=base["Heading1"],
            fontName=s["font_heading"], fontSize=16,
            textColor=HexColor(s["heading_color"]),
            spaceBefore=12, spaceAfter=6,
        ),
        "h2": ParagraphStyle(
            "CustomH2", parent=base["Heading2"],
            fontName=s["font_heading"], fontSize=13,
            textColor=HexColor(s["accent_color"]),
            spaceBefore=8, spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "CustomBody", parent=base["Normal"],
            fontName=s["font_body"], fontSize=11,
            textColor=HexColor(s["text_color"]),
            alignment=TA_JUSTIFY, spaceAfter=4,
            leading=15,
        ),
        "bullet": ParagraphStyle(
            "CustomBullet", parent=base["Normal"],
            fontName=s["font_body"], fontSize=11,
            textColor=HexColor(s["text_color"]),
            leftIndent=20, bulletIndent=10,
            spaceAfter=2, leading=14,
        ),
        "quote": ParagraphStyle(
            "CustomQuote", parent=base["Normal"],
            fontName=s["font_body"], fontSize=11,
            textColor=HexColor(s["accent_color"]),
            leftIndent=30, rightIndent=30,
            spaceAfter=6, leading=14,
        ),
        "meta": ParagraphStyle(
            "CustomMeta", parent=base["Normal"],
            fontName=s["font_body"], fontSize=10,
            textColor=HexColor(s["accent_color"]),
            alignment=TA_CENTER, spaceAfter=12,
        ),
    }
    return styles, s


def build_table(headers, rows, style_config):
    """Build a styled Table flowable."""
    table_data = [headers] + [[str(c) for c in row] for row in rows]
    table = Table(table_data, repeatRows=1)

    header_bg = HexColor(style_config["table_header_bg"])
    stripe_bg = HexColor(style_config["table_stripe_bg"])

    table_style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), header_bg),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#B0BEC5")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ])

    # Stripe alternate rows
    for i in range(1, len(table_data)):
        if i % 2 == 0:
            table_style.add("BACKGROUND", (0, i), (-1, i), stripe_bg)

    table.setStyle(table_style)
    return table


def generate_pdf(data, style_name):
    """Generate PDF content as a list of flowables."""
    styles, style_config = build_styles(style_name)
    story = []

    # Title
    title = data.get("title", "Document")
    story.append(Paragraph(title, styles["title"]))

    # Author / date
    author = data.get("author", "")
    date = data.get("date", "")
    if author or date:
        meta = " | ".join(filter(None, [author, date]))
        story.append(Paragraph(meta, styles["meta"]))

    story.append(HRFlowable(width="80%", thickness=1,
                             color=HexColor(style_config["accent_color"])))
    story.append(Spacer(1, 12))

    # Process sections
    for section in data.get("sections", []):
        section_type = section.get("type", "text")

        if section_type == "heading":
            level = section.get("level", 1)
            style_key = "h1" if level <= 1 else "h2"
            story.append(Paragraph(section.get("text", ""), styles[style_key]))

        elif section_type == "text":
            story.append(Paragraph(section.get("text", ""), styles["body"]))

        elif section_type == "bullets":
            heading = section.get("heading", "")
            if heading:
                story.append(Paragraph(heading, styles["h2"]))
            for item in section.get("items", []):
                story.append(Paragraph(f"• {item}", styles["bullet"]))
            story.append(Spacer(1, 4))

        elif section_type == "table":
            heading = section.get("heading", "")
            if heading:
                story.append(Paragraph(heading, styles["h2"]))
            table = build_table(section.get("headers", []),
                                section.get("rows", []), style_config)
            story.append(table)
            story.append(Spacer(1, 8))

        elif section_type == "quote":
            text = section.get("text", "")
            author_q = section.get("author", "")
            quote_text = f'<i>"{text}"</i>'
            if author_q:
                quote_text += f"<br/>— {author_q}"
            story.append(Paragraph(quote_text, styles["quote"]))

        elif section_type == "page_break":
            story.append(PageBreak())

    return story


def main():
    parser = argparse.ArgumentParser(
        description="Generate professional PDF document from JSON data")
    parser.add_argument("--input", required=True, help="Path to JSON file with content data")
    parser.add_argument("--output", required=True, help="Output .pdf file path")
    parser.add_argument("--style", choices=list(STYLES.keys()), default="corporate",
                        help="Document style (default: corporate)")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(output_path), pagesize=A4,
        topMargin=2.5 * cm, bottomMargin=2.5 * cm,
        leftMargin=2.5 * cm, rightMargin=2.5 * cm,
    )

    story = generate_pdf(data, args.style)
    doc.build(story)

    size_kb = output_path.stat().st_size / 1024
    section_count = len(data.get("sections", []))
    print(f"✅ Saved: {output_path} ({size_kb:.1f} KB, {section_count} sections, style: {args.style})")


if __name__ == "__main__":
    main()
