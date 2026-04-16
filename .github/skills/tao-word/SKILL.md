---
name: tao-word
description: |
  Create professional Word (.docx) documents from synthesized content.
  Supports 3 template styles: corporate, academic, minimal.
  Uses python-docx with A4 page setup. Triggers on "tạo file word",
  "xuất word", "create word document", or "/tao-word".
argument-hint: "[content from bien-soan or direct text] [style: corporate|academic|minimal]"
---

# Tạo Word — Word Document Output Skill

Generates professionally formatted `.docx` files from structured Markdown content.

```yaml
MODE: Interactive (asks style) or Pipeline (style from tong-hop)
LANGUAGE: Copilot responds in Vietnamese
INPUT: Structured Markdown from bien-soan or user text
OUTPUT: .docx file saved to user-specified path
LIBRARY: python-docx
```

---

## Trigger Conditions

Use this skill when user:
- Says "tạo file word", "xuất word", "tạo tài liệu word", "tạo file .docx"
- Says "create word document", "export to word"
- Uses command `/tao-word`
- Pipeline (tong-hop) routes content here for Word output

---

## Script Architecture (US-4.3.3)

```yaml
CLI_SCRIPT:
  path: scripts/gen_docx.py
  purpose: Reusable CLI tool for generating .docx from JSON data
  usage: |
    python3 scripts/gen_docx.py --input data.json --output report.docx --style corporate
  
  args:
    --input: Path to JSON file with content data (required)
    --output: Output .docx file path (required)
    --style: corporate | academic | minimal (default: corporate)
  
  json_format: |
    {
      "title": "Document Title",
      "author": "Author Name",
      "date": "2026-04-16",
      "sections": [
        {"type": "heading", "level": 1, "text": "Section Title"},
        {"type": "text", "text": "Paragraph content"},
        {"type": "bullets", "heading": "Optional Heading", "items": ["Item 1", "Item 2"]},
        {"type": "table", "heading": "Table Title", "headers": ["Col1", "Col2"], "rows": [["a", "b"]]},
        {"type": "quote", "text": "Quote text", "author": "Attribution"}
      ]
    }
  
  output: Prints "✅ Saved: <path> (<size> KB, <N> sections, style: <style>)"

COPILOT_WORKFLOW:
  1. Prepare content as JSON (from bien-soan output or user text)
  2. Save JSON to tmp file
  3. Run: python3 .github/skills/tao-word/scripts/gen_docx.py --input data.json --output output.docx --style <style>
  4. Verify output exists
  5. Report file path + size
```

---

## Pre-Flight Check

```yaml
PRE_FLIGHT:
  1. Check python-docx installed:
     command: python3 -c "import docx" 2>&1
     if_fail: "Chạy: pip install --user python-docx"
     
  2. Check content available:
     - From pipeline: content variable from bien-soan
     - From user: raw text or file path
     if_missing: Ask user for content or redirect to thu-thap + bien-soan
     
  3. Determine style:
     - If user specified: use that style
     - If pipeline: use inferred style from tong-hop
     - If neither: ask user to choose (corporate / academic / minimal)
     
  4. Determine output path:
     - If user specified: use that path
     - Default: ./<document-title>.docx in current working directory
```

---

## Step 1: Parse Content Structure

```yaml
PARSE:
  from_markdown:
    - H1 → Document title
    - H2 → Section headings (Heading 1 in Word)
    - H3 → Subsection headings (Heading 2 in Word)
    - H4 → Sub-subsection (Heading 3 in Word)
    - Paragraphs → Normal text
    - Bullet lists → Bullet list style
    - Numbered lists → Numbered list style
    - Tables → Word tables with headers
    - Bold/italic → Corresponding text runs
    - Blockquotes → Indented italic paragraphs
    - Images (if paths provided) → Inline images
    
  extract:
    - title: First H1 or user-provided title
    - sections: Array of {heading, level, content}
    - metadata: date, author (if provided)
```

---

## Step 2: Generate Python Script

```yaml
SCRIPT:
  location: scripts/ (ephemeral, generated per task)
  template: |
    Copilot generates a python-docx script with:
    1. Import statements
    2. Style configuration (from references/)
    3. Page setup (A4)
    4. Content population
    5. Save and report
    
  CRITICAL_RULES:
    page_setup:
      - A4: width = Inches(8.27), height = Inches(11.69)
      - Margins: 1 inch all sides (Inches(1))
      
    tables:
      - ALWAYS use WidthType.DXA (never PERCENTAGE)
      - Set both table width AND individual cell widths
      - Cell widths must sum to table width
      - A4 content width with 1" margins: 9026 DXA (6.27 inches × 1440)
      
    lists:
      - Use docx numbering config with LevelFormat.BULLET
      - NEVER use Unicode bullet characters (•, ▪, etc.)
      
    images:
      - Always set explicit width: add_picture(path, width=Inches(x))
      - Max width: 6 inches (within margins)
      
    line_breaks:
      - Use separate Paragraph objects
      - NEVER use \n inside TextRun
      
    page_breaks:
      - Must be inside a Paragraph: paragraph.add_run().add_break(WD_BREAK.PAGE)
```

---

## Step 3: Apply Style

```yaml
STYLES:
  selection:
    - User chooses: "corporate", "academic", or "minimal"
    - Pipeline infers: formal/business → corporate, research/paper → academic, simple → minimal
    
  corporate:
    description: Professional blue theme, bold headings, company-style
    reference: references/style-corporate.md
    fonts:
      heading: Calibri, bold
      body: Calibri
    colors:
      primary: "1F4E79"    # Dark blue
      accent: "2E75B6"     # Medium blue
      text: "333333"       # Dark gray
    features:
      - Colored heading bars (blue left border)
      - Table header row with blue background
      - Bold section numbers
      - Footer with page numbers
      
  academic:
    description: Serif fonts, footnote-friendly, research paper style
    reference: references/style-academic.md
    fonts:
      heading: Georgia, bold
      body: Times New Roman
    colors:
      primary: "2C3E50"    # Dark navy
      accent: "7F8C8D"     # Gray
      text: "2C3E50"       # Dark navy
    features:
      - Serif typography throughout
      - Generous line spacing (1.5)
      - Table of contents friendly headings
      - Footnote support
      - Indented first paragraphs
      
  minimal:
    description: Clean, modern, lots of whitespace
    reference: references/style-minimal.md
    fonts:
      heading: Helvetica Neue or Arial
      body: Helvetica Neue or Arial
    colors:
      primary: "1A1A1A"    # Near black
      accent: "666666"     # Medium gray
      text: "333333"       # Dark gray
    features:
      - Thin horizontal rules between sections
      - Large heading sizes, light weight
      - Extra spacing between elements
      - Minimal table borders (top/bottom only)
```

---

## Step 4: Execute Script

```yaml
EXECUTE:
  1. Write script to scripts/gen_word_<timestamp>.py
  2. Run via run_in_terminal:
     command: python3 scripts/gen_word_<timestamp>.py --output "<path>" --style "<style>"
  3. Check exit code:
     - 0: Success → read output path and size
     - Non-zero: Read error → fix script → retry (max 2 retries)
  4. Report to user:
     format: |
       ✅ File Word đã tạo thành công:
       📄 Đường dẫn: {output_path}
       📏 Kích thước: {file_size}
       🎨 Style: {style_name}
       📊 Nội dung: {N} phần, {M} bảng, {P} hình ảnh
```

---

## Step 5: Quality Checks

```yaml
QA:
  automated:
    - File exists and size > 0
    - No python-docx errors in output
    - All sections present in document
    
  manual_offer:
    - "Bạn muốn xem trước nội dung không?" (offer to read back key sections)
    - "Cần chỉnh sửa gì không?" (offer to modify and regenerate)
    
  common_issues:
    tables_too_wide: Check total DXA ≤ 9026 for A4
    missing_fonts: Fallback to Arial if custom font unavailable
    images_not_found: Skip with warning, note missing image paths
    encoding_issues: Ensure UTF-8 for Vietnamese text
```

---

## Script Template Reference

```python
# Template structure — Copilot generates full script based on this pattern
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.shared import OxmlElement, qn
import os, sys

def create_document(content, style, output_path):
    doc = Document()
    
    # Page setup — A4
    section = doc.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)
    
    # Apply style-specific formatting...
    # Add content from parsed Markdown...
    
    doc.save(output_path)
    size = os.path.getsize(output_path)
    print(f"✅ Saved: {output_path} ({size:,} bytes)")

if __name__ == "__main__":
    # Parse CLI args and run
    pass
```

---

## What This Skill Does NOT Do

- Does NOT read input files — that's thu-thap's job
- Does NOT synthesize content — that's bien-soan's job
- Does NOT generate PDF/HTML/PPT — use respective tao-* skills
- Does NOT install dependencies — redirects to /cai-dat
- Does NOT handle Excel data — that's tao-excel's job
