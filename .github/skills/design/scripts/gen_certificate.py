#!/usr/bin/env python3
"""Generate a professional certificate using reportlab Canvas.

Usage:
    python3 gen_certificate.py --name "Nguyễn Văn A" --title "Chứng Nhận Hoàn Thành" --output cert.pdf
    python3 gen_certificate.py --input data.json --output cert.pdf

JSON input format:
    {
        "name": "Recipient Name",
        "title": "Certificate of Completion",
        "subtitle": "has successfully completed the course",
        "course": "Advanced Data Analytics",
        "date": "April 17, 2026",
        "issuer": "InsightEngine Academy",
        "signature_name": "Director Name",
        "style": "formal|modern|elegant"
    }

Styles: formal (navy/gold, serif), modern (blue/white, sans), elegant (cream/dark, mixed)
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.units import mm, cm
    from reportlab.lib.colors import HexColor, white, black
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
except ImportError:
    print("Error: reportlab not installed. Run: pip3 install --user reportlab", file=sys.stderr)
    sys.exit(1)

FONT_DIR = Path(__file__).resolve().parent.parent / "canvas-fonts"

STYLES = {
    "formal": {
        "bg": "#FFFDF5", "border": "#1A365D", "accent": "#B8860B",
        "title_color": "#1A365D", "name_color": "#1A365D", "text_color": "#374151",
        "title_font": "Lora-Regular", "name_font": "Italiana-Regular",
        "body_font": "WorkSans-Regular",
    },
    "modern": {
        "bg": "#FFFFFF", "border": "#2563EB", "accent": "#2563EB",
        "title_color": "#1E3A5F", "name_color": "#2563EB", "text_color": "#4B5563",
        "title_font": "WorkSans-Bold", "name_font": "WorkSans-Bold",
        "body_font": "WorkSans-Regular",
    },
    "elegant": {
        "bg": "#FDF6E3", "border": "#5C4033", "accent": "#8B6914",
        "title_color": "#3C2415", "name_color": "#5C4033", "text_color": "#5C4033",
        "title_font": "CrimsonPro-Bold", "name_font": "Italiana-Regular",
        "body_font": "CrimsonPro-Regular",
    },
}


def register_fonts(style_config: dict):
    """Register required fonts."""
    for key in ("title_font", "name_font", "body_font"):
        font_name = style_config[key]
        ttf_path = FONT_DIR / f"{font_name}.ttf"
        if ttf_path.exists():
            try:
                pdfmetrics.registerFont(TTFont(font_name, str(ttf_path)))
            except Exception:
                pass


def safe_font(c, font_name: str, size: int):
    """Set font with Helvetica fallback."""
    try:
        c.setFont(font_name, size)
    except Exception:
        c.setFont("Helvetica", size)


def draw_certificate(c, width, height, data: dict, style_name: str):
    """Draw the certificate composition."""
    s = STYLES.get(style_name, STYLES["formal"])

    bg = HexColor(s["bg"])
    border = HexColor(s["border"])
    accent = HexColor(s["accent"])

    # Background
    c.setFillColor(bg)
    c.rect(0, 0, width, height, fill=1, stroke=0)

    # Decorative border (double line)
    margin = 15 * mm
    c.setStrokeColor(border)
    c.setLineWidth(3)
    c.rect(margin, margin, width - 2 * margin, height - 2 * margin, fill=0, stroke=1)
    c.setLineWidth(1)
    c.rect(margin + 4 * mm, margin + 4 * mm,
           width - 2 * margin - 8 * mm, height - 2 * margin - 8 * mm, fill=0, stroke=1)

    # Corner ornaments
    c.setFillColor(accent)
    corner_size = 8 * mm
    for x, y in [(margin + 4 * mm, height - margin - 4 * mm - corner_size),
                 (width - margin - 4 * mm - corner_size, height - margin - 4 * mm - corner_size),
                 (margin + 4 * mm, margin + 4 * mm),
                 (width - margin - 4 * mm - corner_size, margin + 4 * mm)]:
        c.rect(x, y, corner_size, corner_size, fill=1, stroke=0)

    # Title
    title = data.get("title", "CERTIFICATE")
    c.setFillColor(HexColor(s["title_color"]))
    safe_font(c, s["title_font"], 36)
    c.drawCentredString(width / 2, height - 55 * mm, title.upper())

    # Accent line under title
    c.setStrokeColor(accent)
    c.setLineWidth(2)
    line_w = 80 * mm
    c.line(width / 2 - line_w / 2, height - 60 * mm, width / 2 + line_w / 2, height - 60 * mm)

    # Subtitle
    subtitle = data.get("subtitle", "This certificate is presented to")
    c.setFillColor(HexColor(s["text_color"]))
    safe_font(c, s["body_font"], 14)
    c.drawCentredString(width / 2, height - 78 * mm, subtitle)

    # Recipient name
    name = data.get("name", "Recipient Name")
    c.setFillColor(HexColor(s["name_color"]))
    safe_font(c, s["name_font"], 42)
    c.drawCentredString(width / 2, height - 100 * mm, name)

    # Name underline
    c.setStrokeColor(accent)
    c.setLineWidth(1)
    name_w = max(c.stringWidth(name, s["name_font"], 42), 120 * mm)
    c.line(width / 2 - name_w / 2, height - 104 * mm, width / 2 + name_w / 2, height - 104 * mm)

    # Course/reason
    course = data.get("course", "")
    if course:
        c.setFillColor(HexColor(s["text_color"]))
        safe_font(c, s["body_font"], 14)
        c.drawCentredString(width / 2, height - 120 * mm, f"for completing: {course}")

    # Date
    date = data.get("date", "")
    if date:
        safe_font(c, s["body_font"], 12)
        c.setFillColor(HexColor(s["text_color"]))
        c.drawCentredString(width / 2, margin + 35 * mm, f"Date: {date}")

    # Issuer
    issuer = data.get("issuer", "")
    if issuer:
        safe_font(c, s["body_font"], 12)
        c.drawCentredString(width / 2, margin + 25 * mm, issuer)

    # Signature line
    sig_name = data.get("signature_name", "")
    if sig_name:
        sig_y = margin + 48 * mm
        c.setStrokeColor(HexColor(s["text_color"]))
        c.setLineWidth(0.5)
        c.line(width / 2 - 40 * mm, sig_y, width / 2 + 40 * mm, sig_y)
        safe_font(c, s["body_font"], 11)
        c.drawCentredString(width / 2, sig_y - 5 * mm, sig_name)


def main():
    parser = argparse.ArgumentParser(description="Generate a professional certificate (PDF)")
    parser.add_argument("--input", help="JSON data file")
    parser.add_argument("--name", default="Recipient Name")
    parser.add_argument("--title", default="CERTIFICATE OF COMPLETION")
    parser.add_argument("--subtitle", default="This certificate is presented to")
    parser.add_argument("--course", default="")
    parser.add_argument("--date", default="")
    parser.add_argument("--issuer", default="")
    parser.add_argument("--signature-name", default="")
    parser.add_argument("--style", choices=["formal", "modern", "elegant"], default="formal")
    parser.add_argument("--output", required=True, help="Output PDF path")
    args = parser.parse_args()

    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {"name": args.name, "title": args.title, "subtitle": args.subtitle,
                "course": args.course, "date": args.date, "issuer": args.issuer,
                "signature_name": args.signature_name}

    style = data.get("style", args.style)
    style_config = STYLES.get(style, STYLES["formal"])
    register_fonts(style_config)

    page_size = landscape(A4)
    width, height = page_size

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    c = canvas.Canvas(str(output_path), pagesize=page_size)
    draw_certificate(c, width, height, data, style)
    c.save()

    file_size = output_path.stat().st_size / 1024
    print(f"✅ Certificate saved: {output_path} ({file_size:.1f} KB, A4 landscape, style: {style})")


if __name__ == "__main__":
    main()
