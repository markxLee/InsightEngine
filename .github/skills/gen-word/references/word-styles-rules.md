# Word Style Specs & Script Rules — Full Reference

## Style Specifications

### corporate

```yaml
fonts: {heading: "Calibri Bold", body: "Calibri"}
colors:
  primary: "1F4E79"  # Dark blue
  accent:  "2E75B6"  # Medium blue
  text:    "333333"  # Dark gray
features:
  - Colored heading bars (blue left border)
  - Table header row with blue background
  - Bold section numbers
  - Footer with page numbers
```

### academic

```yaml
fonts: {heading: "Georgia Bold", body: "Times New Roman"}
colors:
  primary: "2C3E50"  # Dark navy
  accent:  "7F8C8D"  # Gray
  text:    "2C3E50"
features:
  - Serif typography throughout
  - Line spacing: 1.5
  - Table of contents friendly headings
  - Indented first paragraphs
```

### minimal

```yaml
fonts: {heading: "Arial", body: "Arial"}
colors:
  primary: "1A1A1A"  # Near black
  accent:  "666666"  # Medium gray
  text:    "333333"
features:
  - Thin horizontal rules between sections
  - Extra spacing between elements
  - Minimal table borders (top/bottom only)
```

---

## Critical python-docx Rules

```yaml
PAGE_SETUP:
  A4: width = Inches(8.27), height = Inches(11.69)
  Margins: Inches(1) all sides
  A4_content_width_DXA: 9026  # (8.27 - 2) * 1440

TABLES:
  - ALWAYS use WidthType.DXA — NEVER WidthType.PERCENTAGE
  - Set both table width AND individual cell widths
  - Cell widths must sum to table width
  - Total DXA for A4 with 1" margins: max 9026

LISTS:
  - Use docx numbering config with LevelFormat.BULLET
  - NEVER use Unicode bullet characters (•, ▪, etc.)

IMAGES:
  - Always set explicit width: doc.add_picture(path, width=Inches(x))
  - Max width: 6 inches (to fit within margins)

LINE_BREAKS:
  - Use separate Paragraph objects for each paragraph
  - NEVER use "\n" inside a TextRun

PAGE_BREAKS:
  - Must be inside a Paragraph:
    paragraph.add_run().add_break(WD_BREAK.PAGE)
```

---

## Script Template

```python
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

def create_document(content, style, output_path):
    doc = Document()
    section = doc.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    for attr in ['top_margin', 'bottom_margin', 'left_margin', 'right_margin']:
        setattr(section, attr, Inches(1))

    # Apply style formatting, populate sections, add tables, images...

    doc.save(output_path)
    size = os.path.getsize(output_path)
    print(f"✅ Saved: {output_path} ({size:,} bytes)")

# Parse CLI args: --input data.json --output report.docx --style corporate
```
