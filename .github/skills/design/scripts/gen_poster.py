#!/usr/bin/env python3
"""Generate a professional poster layout using reportlab Canvas.

Usage:
    python3 gen_poster.py --title "Event Title" --subtitle "April 2026" --output poster.pdf
    python3 gen_poster.py --title "Workshop" --subtitle "Details" --body "Description" --output poster.pdf --style modern
    python3 gen_poster.py --input data.json --output poster.pdf

JSON input format:
    {
        "title": "Event Title",
        "subtitle": "Date & Location",
        "body": "Description text (optional)",
        "footer": "Contact info (optional)",
        "style": "modern|classic|bold",
        "palette": {"bg": "#1A365D", "accent": "#E2B93B", "text": "#FFFFFF"}
    }

Styles: modern (geometric shapes), classic (elegant serif), bold (large type brutalist)
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A3, A4
    from reportlab.lib.units import mm, cm
    from reportlab.lib.colors import HexColor, white, black
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
except ImportError:
    print("Error: reportlab not installed. Run: pip3 install --user reportlab", file=sys.stderr)
    sys.exit(1)

FONT_DIR = Path(__file__).resolve().parent.parent / "canvas-fonts"

PALETTES = {
    "modern": {"bg": "#0F172A", "accent": "#38BDF8", "text": "#F8FAFC", "muted": "#64748B"},
    "classic": {"bg": "#FFFBEB", "accent": "#92400E", "text": "#1C1917", "muted": "#78716C"},
    "bold": {"bg": "#DC2626", "accent": "#FBBF24", "text": "#FFFFFF", "muted": "#FCA5A5"},
}

STYLE_FONTS = {
    "modern": {"title": "WorkSans-Bold", "body": "WorkSans-Regular", "accent": "GeistMono-Bold"},
    "classic": {"title": "Lora-Regular", "body": "Lora-Regular", "accent": "Italiana-Regular"},
    "bold": {"title": "BigShoulders-Bold", "body": "WorkSans-Regular", "accent": "WorkSans-Bold"},
}


def register_fonts(style: str):
    """Register required fonts for the given style."""
    fonts = STYLE_FONTS.get(style, STYLE_FONTS["modern"])
    for key, font_name in fonts.items():
        ttf_path = FONT_DIR / f"{font_name}.ttf"
        if ttf_path.exists():
            try:
                pdfmetrics.registerFont(TTFont(font_name, str(ttf_path)))
            except Exception:
                pass  # Already registered or fallback to Helvetica


def draw_poster(c, width, height, data: dict, style: str):
    """Draw the poster composition on the canvas."""
    palette = data.get("palette", PALETTES.get(style, PALETTES["modern"]))
    if isinstance(palette, dict):
        bg = HexColor(palette["bg"])
        accent = HexColor(palette["accent"])
        text_color = HexColor(palette["text"])
        muted = HexColor(palette.get("muted", palette["text"]))
    else:
        bg, accent, text_color, muted = HexColor("#0F172A"), HexColor("#38BDF8"), white, HexColor("#64748B")

    fonts = STYLE_FONTS.get(style, STYLE_FONTS["modern"])

    # Background
    c.setFillColor(bg)
    c.rect(0, 0, width, height, fill=1, stroke=0)

    # Accent geometric elements
    if style == "modern":
        c.setFillColor(accent)
        c.circle(width * 0.85, height * 0.82, 60 * mm, fill=1, stroke=0)
        c.setStrokeColor(accent)
        c.setLineWidth(2)
        c.line(30 * mm, height * 0.65, width - 30 * mm, height * 0.65)
    elif style == "classic":
        c.setStrokeColor(accent)
        c.setLineWidth(3)
        margin = 20 * mm
        c.rect(margin, margin, width - 2 * margin, height - 2 * margin, fill=0, stroke=1)
        c.rect(margin + 5 * mm, margin + 5 * mm,
               width - 2 * margin - 10 * mm, height - 2 * margin - 10 * mm, fill=0, stroke=1)
    elif style == "bold":
        c.setFillColor(accent)
        c.rect(0, height * 0.55, width, height * 0.35, fill=1, stroke=0)

    # Title
    title = data.get("title", "Title")
    title_font = fonts["title"]
    try:
        c.setFont(title_font, 48)
    except Exception:
        c.setFont("Helvetica-Bold", 48)

    if style == "bold":
        c.setFillColor(HexColor(palette["bg"]))
        c.drawCentredString(width / 2, height * 0.72, title)
    else:
        c.setFillColor(text_color)
        c.drawCentredString(width / 2, height * 0.58, title)

    # Subtitle
    subtitle = data.get("subtitle", "")
    if subtitle:
        try:
            c.setFont(fonts["accent"], 20)
        except Exception:
            c.setFont("Helvetica", 20)
        c.setFillColor(accent if style != "bold" else text_color)
        c.drawCentredString(width / 2, height * 0.50 if style != "bold" else height * 0.48, subtitle)

    # Body text
    body = data.get("body", "")
    if body:
        try:
            c.setFont(fonts["body"], 14)
        except Exception:
            c.setFont("Helvetica", 14)
        c.setFillColor(muted if style != "classic" else text_color)
        # Simple word wrap
        max_width = width - 60 * mm
        words = body.split()
        lines = []
        current_line = ""
        for word in words:
            test = f"{current_line} {word}".strip()
            if c.stringWidth(test, fonts.get("body", "Helvetica"), 14) < max_width:
                current_line = test
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)

        y = height * 0.38
        for line in lines[:8]:  # Max 8 lines
            c.drawCentredString(width / 2, y, line)
            y -= 20

    # Footer
    footer = data.get("footer", "")
    if footer:
        try:
            c.setFont(fonts["body"], 11)
        except Exception:
            c.setFont("Helvetica", 11)
        c.setFillColor(muted)
        c.drawCentredString(width / 2, 25 * mm, footer)


def main():
    parser = argparse.ArgumentParser(description="Generate a professional poster (PDF)")
    parser.add_argument("--input", help="JSON data file")
    parser.add_argument("--title", default="Poster Title")
    parser.add_argument("--subtitle", default="")
    parser.add_argument("--body", default="")
    parser.add_argument("--footer", default="")
    parser.add_argument("--style", choices=["modern", "classic", "bold"], default="modern")
    parser.add_argument("--size", choices=["A3", "A4"], default="A3")
    parser.add_argument("--output", required=True, help="Output PDF path")
    args = parser.parse_args()

    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {"title": args.title, "subtitle": args.subtitle,
                "body": args.body, "footer": args.footer}

    style = data.get("style", args.style)
    register_fonts(style)

    page_size = A3 if args.size == "A3" else A4
    width, height = page_size

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    c = canvas.Canvas(str(output_path), pagesize=page_size)
    draw_poster(c, width, height, data, style)
    c.save()

    file_size = output_path.stat().st_size / 1024
    print(f"✅ Poster saved: {output_path} ({file_size:.1f} KB, {args.size}, style: {style})")


if __name__ == "__main__":
    main()
