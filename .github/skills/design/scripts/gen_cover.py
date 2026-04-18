#!/usr/bin/env python3
"""Generate a professional report cover page using reportlab Canvas.

Usage:
    python3 gen_cover.py --title "Annual Report 2026" --author "Team Name" --output cover.pdf
    python3 gen_cover.py --input data.json --output cover.pdf

JSON input format:
    {
        "title": "Report Title",
        "subtitle": "Optional subtitle",
        "author": "Author or Organization",
        "date": "April 2026",
        "logo_path": "path/to/logo.png (optional)",
        "style": "corporate|academic|creative"
    }

Styles: corporate (navy/white, clean), academic (sepia/serif), creative (gradient/bold)
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm, cm
    from reportlab.lib.colors import HexColor, white, black
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
except ImportError:
    print("Error: reportlab not installed. Run: pip3 install --user reportlab", file=sys.stderr)
    sys.exit(1)

FONT_DIR = Path(__file__).resolve().parent.parent / "canvas-fonts"

STYLES = {
    "corporate": {
        "bg_top": "#1A365D", "bg_bottom": "#FFFFFF", "accent": "#3182CE",
        "title_color": "#FFFFFF", "subtitle_color": "#A0C4E8",
        "author_color": "#1A365D", "date_color": "#6B7280",
        "title_font": "WorkSans-Bold", "body_font": "WorkSans-Regular",
        "split_ratio": 0.55,
    },
    "academic": {
        "bg_top": "#F5F0E8", "bg_bottom": "#F5F0E8", "accent": "#8B4513",
        "title_color": "#2D1B0E", "subtitle_color": "#6B4423",
        "author_color": "#2D1B0E", "date_color": "#8B7355",
        "title_font": "Lora-Regular", "body_font": "Lora-Regular",
        "split_ratio": 0.0,
    },
    "creative": {
        "bg_top": "#4C1D95", "bg_bottom": "#1E1B4B", "accent": "#F59E0B",
        "title_color": "#FFFFFF", "subtitle_color": "#C4B5FD",
        "author_color": "#E0E7FF", "date_color": "#A5B4FC",
        "title_font": "WorkSans-Bold", "body_font": "WorkSans-Regular",
        "split_ratio": 1.0,
    },
}


def register_fonts(style_config: dict):
    """Register required fonts."""
    for key in ("title_font", "body_font"):
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
        fallback = "Helvetica-Bold" if "Bold" in font_name else "Helvetica"
        c.setFont(fallback, size)


def draw_cover(c, width, height, data: dict, style_name: str):
    """Draw the cover page."""
    s = STYLES.get(style_name, STYLES["corporate"])
    split = s["split_ratio"]

    # Background
    if split > 0:
        # Top section (colored)
        c.setFillColor(HexColor(s["bg_top"]))
        c.rect(0, height * (1 - split), width, height * split, fill=1, stroke=0)
        # Bottom section
        c.setFillColor(HexColor(s["bg_bottom"]))
        c.rect(0, 0, width, height * (1 - split), fill=1, stroke=0)
    else:
        # Full page single color (academic)
        c.setFillColor(HexColor(s["bg_top"]))
        c.rect(0, 0, width, height, fill=1, stroke=0)

    # Accent bar
    accent = HexColor(s["accent"])
    if style_name == "corporate":
        c.setFillColor(accent)
        c.rect(0, height * (1 - split) - 3 * mm, width, 3 * mm, fill=1, stroke=0)
    elif style_name == "academic":
        c.setStrokeColor(accent)
        c.setLineWidth(2)
        margin = 25 * mm
        c.line(margin, height * 0.55, width - margin, height * 0.55)
        c.line(margin, height * 0.53, width - margin, height * 0.53)
    elif style_name == "creative":
        c.setFillColor(accent)
        c.circle(width * 0.8, height * 0.75, 40 * mm, fill=1, stroke=0)
        c.setFillColor(HexColor(s["bg_top"]))
        c.circle(width * 0.8, height * 0.75, 30 * mm, fill=1, stroke=0)

    # Title
    title = data.get("title", "Report Title")
    c.setFillColor(HexColor(s["title_color"]))
    safe_font(c, s["title_font"], 36)

    # Word wrap title
    max_w = width - 60 * mm
    words = title.split()
    lines = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip()
        if c.stringWidth(test, s["title_font"], 36) < max_w:
            current = test
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)

    if style_name == "academic":
        title_y = height * 0.70
    else:
        title_y = height * 0.75

    for line in lines:
        if style_name == "academic":
            c.drawCentredString(width / 2, title_y, line)
        else:
            c.drawString(30 * mm, title_y, line)
        title_y -= 42

    # Subtitle
    subtitle = data.get("subtitle", "")
    if subtitle:
        c.setFillColor(HexColor(s["subtitle_color"]))
        safe_font(c, s["body_font"], 18)
        sub_y = title_y - 10
        if style_name == "academic":
            c.drawCentredString(width / 2, sub_y, subtitle)
        else:
            c.drawString(30 * mm, sub_y, subtitle)

    # Author
    author = data.get("author", "")
    if author:
        c.setFillColor(HexColor(s["author_color"]))
        safe_font(c, s["body_font"], 16)
        if style_name == "corporate":
            c.drawString(30 * mm, height * 0.30, author)
        elif style_name == "academic":
            c.drawCentredString(width / 2, height * 0.40, author)
        else:
            c.drawString(30 * mm, height * 0.15, author)

    # Date
    date = data.get("date", "")
    if date:
        c.setFillColor(HexColor(s["date_color"]))
        safe_font(c, s["body_font"], 13)
        if style_name == "academic":
            c.drawCentredString(width / 2, height * 0.35, date)
        else:
            c.drawString(30 * mm, 25 * mm, date)

    # Logo
    logo_path = data.get("logo_path", "")
    if logo_path and Path(logo_path).exists():
        try:
            c.drawImage(logo_path, width - 55 * mm, 20 * mm, width=30 * mm,
                        preserveAspectRatio=True, mask="auto")
        except Exception:
            pass  # Skip if logo fails


def main():
    parser = argparse.ArgumentParser(description="Generate a report cover page (PDF)")
    parser.add_argument("--input", help="JSON data file")
    parser.add_argument("--title", default="Report Title")
    parser.add_argument("--subtitle", default="")
    parser.add_argument("--author", default="")
    parser.add_argument("--date", default="")
    parser.add_argument("--style", choices=["corporate", "academic", "creative"], default="corporate")
    parser.add_argument("--output", required=True, help="Output PDF path")
    args = parser.parse_args()

    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {"title": args.title, "subtitle": args.subtitle,
                "author": args.author, "date": args.date}

    style = data.get("style", args.style)
    style_config = STYLES.get(style, STYLES["corporate"])
    register_fonts(style_config)

    width, height = A4

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    c = canvas.Canvas(str(output_path), pagesize=A4)
    draw_cover(c, width, height, data, style)
    c.save()

    file_size = output_path.stat().st_size / 1024
    print(f"✅ Cover saved: {output_path} ({file_size:.1f} KB, A4, style: {style})")


if __name__ == "__main__":
    main()
