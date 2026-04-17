# PDF Script Details — Full Reference

## Imports & Page Setup

```python
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, ListFlowable, ListItem
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Page: A4, margins [25mm, 25mm, 20mm, 20mm]

# Vietnamese font setup
font_paths = [
    "/System/Library/Fonts/Helvetica.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
]
for fp in font_paths:
    if os.path.exists(fp):
        try:
            pdfmetrics.registerFont(TTFont("ViFont", fp))
            break
        except: continue
```

## Style Configuration (3 styles)

```yaml
corporate:
  title:    {fontName: "Helvetica-Bold", fontSize: 24, alignment: TA_CENTER, spaceAfter: 12mm}
  heading1: {fontName: "Helvetica-Bold", fontSize: 16, textColor: "#1a1a2e", spaceBefore: 8mm}
  heading2: {fontName: "Helvetica-Bold", fontSize: 13, textColor: "#16213e", spaceBefore: 6mm}
  body:     {fontName: "Helvetica", fontSize: 11, leading: 16, alignment: TA_JUSTIFY}
  table_header: {fontName: "Helvetica-Bold", fontSize: 10, textColor: "#FFFFFF", background: "#1a1a2e"}
  table_cell: {fontName: "Helvetica", fontSize: 10, padding: 6}

academic:
  title:    {fontName: "Helvetica-Bold", fontSize: 22, alignment: TA_CENTER}
  heading1: {fontName: "Helvetica-Bold", fontSize: 15, textColor: "#2C3E50"}
  body:     {fontName: "Helvetica", fontSize: 11, leading: 18, alignment: TA_JUSTIFY}

minimal:
  title:    {fontName: "Helvetica", fontSize: 28, alignment: TA_LEFT}
  heading1: {fontName: "Helvetica-Bold", fontSize: 14, textColor: "#111827"}
  body:     {fontName: "Helvetica", fontSize: 11, leading: 16}
```

## Markdown → PDF Conversion Rules

```yaml
CONVERSION:
  "# Title"      → Paragraph(text, styles["Title"])
  "## Heading"   → Paragraph(text, styles["Heading1"])
  "### Sub"      → Paragraph(text, styles["Heading2"])
  plain_text     → Paragraph(text, styles["BodyText"])
  "**bold**"     → "<b>bold</b>"   (reportlab XML markup)
  "*italic*"     → "<i>italic</i>"
  bullet_list    → ListFlowable with ListItem elements
  numbered_list  → ListFlowable with bulletType="1"
  tables         → Table flowable with TableStyle, alternating row colors
  code_blocks    → Paragraph with monospace font, gray background
  images         → Image(path, width, height) with auto-scale
  "---" or break → PageBreak()

CRITICAL:
  subscript:   Use "<sub>text</sub>" — NEVER Unicode subscript characters
  superscript: Use "<super>text</super>" — NEVER Unicode superscript characters
```

## Page Features

```yaml
PAGE_NUMBERS:
  position: bottom center
  format: "Trang {page_num} / {total_pages}"
  code: |
    def add_page_number(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 9)
        canvas.drawCentredString(A4[0]/2, 15*mm, f"Trang {canvas.getPageNumber()}")
        canvas.restoreState()

TABLE_OF_CONTENTS:
  condition: Document has 3+ H1/H2 headings
  position: After title page
  auto_generate: true

HEADER:
  content: Document title (abbreviated if long)
  position: top right
  font: Helvetica 8pt, gray
```

## Build & Verify

```python
doc = SimpleDocTemplate(output_path, pagesize=A4,
      leftMargin=25*mm, rightMargin=25*mm, topMargin=20*mm, bottomMargin=20*mm)
doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)

# Verify
import pypdf
reader = pypdf.PdfReader(output_path)
page_count = len(reader.pages)
```
