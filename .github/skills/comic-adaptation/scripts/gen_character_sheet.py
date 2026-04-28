#!/usr/bin/env python3
"""Generate a character prototype sheet PDF for comic adaptation.

Usage:
    python3 gen_character_sheet.py --input characters.json --output output/sheet.pdf
    python3 gen_character_sheet.py --input characters.json --output output/sheet.pdf --title "My Comic"

Input JSON format:
    {
        "title": "Comic Title",
        "subtitle": "Anime adaptation character prototype sheet",
        "characters": [
            {
                "name": "Character Name",
                "role": "Story role description",
                "archetype": "shonen_hero",
                "palette": ["#C11F2C", "#E2BF54", "#1F4E8C", "#F8EBCF"],
                "accent": "#E2BF54",
                "skin": "#E7C7A8",
                "hair_color": "#1A1822",
                "eye_style": "hero",
                "hair_shape": "long_flow",
                "notes": [
                    "Silhouette note...",
                    "Expression note...",
                    "Pose note..."
                ]
            }
        ]
    }

Archetypes (hair_shape): short_spike, long_flow, bun, topknot, crown, helmet, ponytail, short_neat
Eye styles: wide, hero, warm, sharp, slit
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from reportlab.lib.colors import HexColor, black, white
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.units import mm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen import canvas
except ImportError:
    print("Error: reportlab not installed. Run: pip install reportlab", file=sys.stderr)
    sys.exit(1)

# Resolve font directory relative to the skill tree
FONT_DIR = Path(__file__).resolve().parent.parent.parent / "design" / "canvas-fonts"


# ---------------------------------------------------------------------------
# Font helpers
# ---------------------------------------------------------------------------

def register_fonts() -> None:
    for name in ("WorkSans-Bold", "WorkSans-Regular", "Lora-Bold", "Lora-Regular"):
        path = FONT_DIR / f"{name}.ttf"
        if path.exists():
            try:
                pdfmetrics.registerFont(TTFont(name, str(path)))
            except Exception:
                pass


def set_font(c: canvas.Canvas, name: str, size: int) -> None:
    try:
        c.setFont(name, size)
    except Exception:
        c.setFont("Helvetica-Bold" if "Bold" in name else "Helvetica", size)


def wrap_text(c: canvas.Canvas, text: str, font: str, size: int, max_w: float) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        test = f"{cur} {w}".strip()
        if c.stringWidth(test, font, size) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------------------
# Drawing primitives
# ---------------------------------------------------------------------------

def draw_swatch_row(c: canvas.Canvas, x: float, y: float, swatches: list[str]) -> None:
    size = 6 * mm
    gap = 2.5 * mm
    for i, color in enumerate(swatches):
        c.setFillColor(HexColor(color))
        c.roundRect(x + i * (size + gap), y, size, size, 1.5 * mm, fill=1, stroke=0)


def draw_eye_pair(c: canvas.Canvas, cx: float, ey: float, style: str) -> None:
    """Draw anime-style eye pair based on archetype."""
    if style == "wide":
        c.setFillColor(black)
        c.ellipse(cx - 5 * mm, ey - 2.2 * mm, cx - 1.5 * mm, ey + 1.6 * mm, fill=1, stroke=0)
        c.ellipse(cx + 1.5 * mm, ey - 2.2 * mm, cx + 5 * mm, ey + 1.6 * mm, fill=1, stroke=0)
        c.setFillColor(white)
        c.circle(cx - 3.7 * mm, ey, 0.8 * mm, fill=1, stroke=0)
        c.circle(cx + 3.7 * mm, ey, 0.8 * mm, fill=1, stroke=0)
    elif style == "hero":
        c.setFillColor(black)
        c.ellipse(cx - 4.6 * mm, ey - 1.8 * mm, cx - 1.2 * mm, ey + 1.2 * mm, fill=1, stroke=0)
        c.ellipse(cx + 1.2 * mm, ey - 1.8 * mm, cx + 4.6 * mm, ey + 1.2 * mm, fill=1, stroke=0)
        c.setFillColor(white)
        c.circle(cx - 3.1 * mm, ey + 0.1 * mm, 0.7 * mm, fill=1, stroke=0)
        c.circle(cx + 3.1 * mm, ey + 0.1 * mm, 0.7 * mm, fill=1, stroke=0)
    elif style == "warm":
        c.setFillColor(black)
        c.ellipse(cx - 4.2 * mm, ey - 1.4 * mm, cx - 1.8 * mm, ey + 1.2 * mm, fill=1, stroke=0)
        c.ellipse(cx + 1.8 * mm, ey - 1.4 * mm, cx + 4.2 * mm, ey + 1.2 * mm, fill=1, stroke=0)
        c.setFillColor(white)
        c.circle(cx - 3.2 * mm, ey + 0.1 * mm, 0.55 * mm, fill=1, stroke=0)
        c.circle(cx + 3.2 * mm, ey + 0.1 * mm, 0.55 * mm, fill=1, stroke=0)
    elif style in ("sharp", "slit"):
        c.setFillColor(black)
        c.setStrokeColor(black)
        c.setLineWidth(1.4)
        c.line(cx - 5 * mm, ey + 0.8 * mm, cx - 1.5 * mm, ey + 1.9 * mm)
        c.line(cx + 1.5 * mm, ey + 1.9 * mm, cx + 5 * mm, ey + 0.8 * mm)
        c.line(cx - 4.6 * mm, ey - 0.2 * mm, cx - 1.2 * mm, ey - 0.2 * mm)
        c.line(cx + 1.2 * mm, ey - 0.2 * mm, cx + 4.6 * mm, ey - 0.2 * mm)
        c.setFillColor(white)
        c.circle(cx - 2.7 * mm, ey + 0.3 * mm, 0.45 * mm, fill=1, stroke=0)
        c.circle(cx + 2.7 * mm, ey + 0.3 * mm, 0.45 * mm, fill=1, stroke=0)
    else:
        c.setFillColor(black)
        c.circle(cx - 3 * mm, ey, 1 * mm, fill=1, stroke=0)
        c.circle(cx + 3 * mm, ey, 1 * mm, fill=1, stroke=0)


def draw_head(c: canvas.Canvas, cx: float, by: float, skin: str, hair: str, shape: str) -> None:
    """Draw stylized head + hair silhouette."""
    # Face circle
    c.setFillColor(HexColor(skin))
    c.circle(cx, by + 20 * mm, 10 * mm, fill=1, stroke=0)

    # Hair
    c.setFillColor(HexColor(hair))
    if shape == "short_spike":
        c.circle(cx, by + 24 * mm, 12 * mm, fill=1, stroke=0)
        c.setStrokeColor(HexColor(hair))
        c.setLineWidth(2.2)
        c.line(cx - 8 * mm, by + 31 * mm, cx - 3 * mm, by + 39 * mm)
        c.line(cx - 1 * mm, by + 31.5 * mm, cx + 2 * mm, by + 41 * mm)
        c.line(cx + 6 * mm, by + 29 * mm, cx + 10 * mm, by + 37 * mm)
    elif shape == "long_flow":
        c.circle(cx, by + 25 * mm, 13 * mm, fill=1, stroke=0)
        c.setStrokeColor(HexColor(hair))
        c.setLineWidth(3.2)
        c.line(cx + 8 * mm, by + 18 * mm, cx + 17 * mm, by + 7 * mm)
        c.line(cx + 9 * mm, by + 23 * mm, cx + 19 * mm, by + 18 * mm)
        c.line(cx - 6 * mm, by + 22 * mm, cx - 2 * mm, by + 33 * mm)
    elif shape == "bun":
        c.circle(cx, by + 23 * mm, 11 * mm, fill=1, stroke=0)
        c.circle(cx + 2 * mm, by + 34 * mm, 4 * mm, fill=1, stroke=0)
    elif shape == "topknot":
        c.circle(cx, by + 23 * mm, 11 * mm, fill=1, stroke=0)
        c.circle(cx, by + 36 * mm, 4 * mm, fill=1, stroke=0)
    elif shape == "crown":
        c.circle(cx, by + 24 * mm, 11 * mm, fill=1, stroke=0)
        c.setFillColor(HexColor("#C8A95D"))
        c.rect(cx - 10 * mm, by + 34 * mm, 20 * mm, 4 * mm, fill=1, stroke=0)
    elif shape == "helmet":
        c.circle(cx, by + 23 * mm, 11 * mm, fill=1, stroke=0)
        c.setFillColor(HexColor("#7A7F87"))
        c.rect(cx - 11 * mm, by + 24 * mm, 22 * mm, 12 * mm, fill=0, stroke=1)
    elif shape == "ponytail":
        c.circle(cx, by + 23 * mm, 11 * mm, fill=1, stroke=0)
        c.setStrokeColor(HexColor(hair))
        c.setLineWidth(3)
        c.line(cx + 5 * mm, by + 20 * mm, cx + 14 * mm, by + 10 * mm)
    elif shape == "short_neat":
        c.circle(cx, by + 23 * mm, 11.5 * mm, fill=1, stroke=0)
    else:
        c.circle(cx, by + 24 * mm, 12 * mm, fill=1, stroke=0)


def draw_mouth(c: canvas.Canvas, cx: float, by: float, eye_style: str) -> None:
    """Draw a small mouth matching the character tone."""
    c.setStrokeColor(black)
    c.setLineWidth(0.9)
    if eye_style in ("wide", "warm"):
        c.arc(cx - 2.5 * mm, by + 16.5 * mm, cx + 2.5 * mm, by + 20 * mm, 210, 320)
    elif eye_style == "hero":
        c.line(cx - 2.4 * mm, by + 17.1 * mm, cx + 2.4 * mm, by + 17.1 * mm)
    else:
        c.line(cx - 2.6 * mm, by + 17.0 * mm, cx + 2.6 * mm, by + 17.0 * mm)


# ---------------------------------------------------------------------------
# Card rendering
# ---------------------------------------------------------------------------

def draw_card(c: canvas.Canvas, x: float, y: float, w: float, h: float, char: dict) -> None:
    accent = char.get("accent", "#555555")

    # Card background
    c.setFillColor(HexColor("#FFF9F0"))
    c.roundRect(x, y, w, h, 6 * mm, fill=1, stroke=0)
    c.setStrokeColor(HexColor(accent))
    c.setLineWidth(2)
    c.roundRect(x, y, w, h, 6 * mm, fill=0, stroke=1)

    # Header band
    c.setFillColor(HexColor(accent))
    c.roundRect(x, y + h - 16 * mm, w, 16 * mm, 6 * mm, fill=1, stroke=0)

    set_font(c, "WorkSans-Bold", 14)
    c.setFillColor(white)
    c.drawString(x + 8 * mm, y + h - 11 * mm, char["name"])

    set_font(c, "WorkSans-Regular", 8.5)
    c.drawString(x + 8 * mm, y + h - 15 * mm, char.get("role", ""))

    # Portrait
    cx = x + 23 * mm
    by = y + 13 * mm
    skin = char.get("skin", "#E7C7A8")
    hair_color = char.get("hair_color", "#1A1822")
    hair_shape = char.get("hair_shape", "short_neat")
    eye_style = char.get("eye_style", "hero")

    draw_head(c, cx, by, skin, hair_color, hair_shape)

    # Body silhouette
    palette = char.get("palette", ["#555555", "#777777", "#333333", "#EEEEEE"])
    c.setFillColor(HexColor(palette[0]))
    c.roundRect(cx - 11 * mm, y + 9 * mm, 22 * mm, 12 * mm, 4 * mm, fill=1, stroke=0)
    if len(palette) > 2:
        c.setFillColor(HexColor(palette[2]))
        c.rect(cx - 13 * mm, y + 11 * mm, 26 * mm, 5 * mm, fill=1, stroke=0)

    # Eyes + mouth
    draw_eye_pair(c, cx, by + 20.3 * mm, eye_style)
    draw_mouth(c, cx, by, eye_style)

    # Palette swatches
    draw_swatch_row(c, x + 48 * mm, y + h - 28 * mm, palette[:5])
    set_font(c, "WorkSans-Bold", 8.5)
    c.setFillColor(HexColor(accent))
    c.drawString(x + 48 * mm, y + h - 20 * mm, "Màu chủ đạo")

    # Notes
    tx = x + 48 * mm
    ty = y + h - 33 * mm
    set_font(c, "WorkSans-Regular", 8.8)
    c.setFillColor(HexColor("#2E2A39"))
    for note in char.get("notes", []):
        wrapped = wrap_text(c, note, "WorkSans-Regular", 8.8, w - 55 * mm)
        for line in wrapped:
            c.drawString(tx, ty, f"• {line}" if line == wrapped[0] else f"  {line}")
            ty -= 4.8 * mm
        ty -= 1.1 * mm

    # Archetype badge
    archetype = char.get("archetype", "")
    if archetype:
        c.setFillColor(HexColor("#FAF3E6"))
        c.roundRect(x + 8 * mm, y + 7 * mm, 31 * mm, 7 * mm, 2.5 * mm, fill=1, stroke=0)
        set_font(c, "WorkSans-Bold", 7.2)
        c.setFillColor(HexColor(accent))
        label = archetype.upper().replace("_", " ")
        c.drawCentredString(x + 23.5 * mm, y + 9.1 * mm, label)


# ---------------------------------------------------------------------------
# Page layout
# ---------------------------------------------------------------------------

def build_pdf(data: dict, output_path: Path) -> None:
    register_fonts()
    characters = data.get("characters", [])
    title = data.get("title", "Character Prototype Sheet")
    subtitle = data.get("subtitle", "Anime adaptation — reference for comic pages")

    width, height = landscape(A4)
    c = canvas.Canvas(str(output_path), pagesize=(width, height))

    cards_per_page = 6
    card_w = 88 * mm
    card_h = 74 * mm
    gap_x = 8 * mm
    gap_y = 8 * mm
    start_x = 14 * mm

    for page_idx in range(0, len(characters), cards_per_page):
        page_chars = characters[page_idx : page_idx + cards_per_page]

        # Background
        c.setFillColor(HexColor("#F3E9DA"))
        c.rect(0, 0, width, height, fill=1, stroke=0)

        # Decorative diagonals
        c.setFillColor(HexColor("#E7D7BC"))
        c.saveState()
        c.translate(width * 0.78, height * 0.42)
        c.rotate(-18)
        c.rect(-25 * mm, -70 * mm, 50 * mm, 140 * mm, fill=1, stroke=0)
        c.restoreState()

        c.setFillColor(HexColor("#DCC5A2"))
        c.saveState()
        c.translate(width * 0.18, height * 0.72)
        c.rotate(22)
        c.rect(-18 * mm, -55 * mm, 36 * mm, 110 * mm, fill=1, stroke=0)
        c.restoreState()

        # Header
        c.setFillColor(HexColor("#2B2230"))
        c.rect(0, height - 28 * mm, width, 28 * mm, fill=1, stroke=0)
        c.setFillColor(HexColor("#D9B24C"))
        c.rect(0, height - 30 * mm, width, 2 * mm, fill=1, stroke=0)

        set_font(c, "WorkSans-Bold", 24)
        c.setFillColor(white)
        c.drawString(14 * mm, height - 18 * mm, title.upper())
        set_font(c, "WorkSans-Regular", 10)
        c.setFillColor(HexColor("#F1E6D1"))
        c.drawString(14 * mm, height - 23 * mm, subtitle)

        page_label = f"Page {page_idx // cards_per_page + 1}"
        set_font(c, "WorkSans-Regular", 8.8)
        c.drawRightString(width - 14 * mm, height - 18 * mm, page_label)

        # Card positions (3 cols × 2 rows)
        positions = [
            (start_x + col * (card_w + gap_x), height - 28 * mm - gap_y - card_h - row * (card_h + gap_y))
            for row in range(2)
            for col in range(3)
        ]

        for char, (px, py) in zip(page_chars, positions):
            draw_card(c, px, py, card_w, card_h, char)

        # Footer
        set_font(c, "WorkSans-Regular", 8)
        c.setFillColor(HexColor("#5B4A3B"))
        c.drawString(14 * mm, 6 * mm,
                      "Keep proportions, palette, and emotional tone consistent across comic pages.")

        c.showPage()

    c.save()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate character prototype sheet PDF")
    parser.add_argument("--input", required=True, help="JSON file with character data")
    parser.add_argument("--output", required=True, help="Output PDF path")
    parser.add_argument("--title", help="Override title from JSON")
    parser.add_argument("--subtitle", help="Override subtitle from JSON")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    if args.title:
        data["title"] = args.title
    if args.subtitle:
        data["subtitle"] = args.subtitle

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    build_pdf(data, output_path)
    size_kb = round(output_path.stat().st_size / 1024, 1)
    print(f"{output_path} {size_kb} KB")


if __name__ == "__main__":
    main()
