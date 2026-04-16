---
name: tao-pdf
description: |
  Create professional PDF documents from synthesized content.
  Uses reportlab Platypus for complex layouts, Canvas for simple ones.
  Embeds fonts for Vietnamese character support.
  Use when user says "tạo file pdf", "xuất pdf", or "/tao-pdf".
argument-hint: "[content from bien-soan or direct text] [output path]"
---

# Tạo PDF — PDF Document Output Skill

Generates professionally formatted `.pdf` files with proper Vietnamese character support.

```yaml
MODE: Interactive (asks style) or Pipeline (from tong-hop)
LANGUAGE: Copilot responds in Vietnamese
INPUT: Structured Markdown from bien-soan or user text
OUTPUT: .pdf file saved to user-specified path
LIBRARIES: reportlab (Platypus + Canvas), pypdf
```

---

## Trigger Conditions

Use this skill when user:
- Says "tạo file pdf", "xuất pdf", "tạo file .pdf"
- Says "create pdf", "export to pdf"
- Uses command `/tao-pdf`
- Pipeline (tong-hop) routes content here for PDF output

---

## Pre-Flight Check

```yaml
PRE_FLIGHT:
  1. Check reportlab installed:
     command: python3 -c "from reportlab.platypus import SimpleDocTemplate" 2>&1
     if_fail: "Chạy: pip install --user reportlab"
     
  2. Check pypdf installed:
     command: python3 -c "import pypdf" 2>&1
     if_fail: "Chạy: pip install --user pypdf"
     
  3. Check content available:
     - From pipeline: content variable from bien-soan
     - From user: raw text or file path
     if_missing: Ask user for content or redirect to thu-thap + bien-soan
```

---

## Step 1: Analyze Content Structure

```yaml
ANALYZE:
  determine:
    - Document title and metadata
    - Number of sections and subsections
    - Tables present (need Table flowable)
    - Images to embed (need Image flowable)
    - Need for table of contents
    - Page orientation (portrait vs landscape)
    
  choose_approach:
    simple: Canvas API for single-page, minimal formatting
    complex: Platypus (SimpleDocTemplate) for multi-page with flowables
    default: Platypus (recommended for most cases)
```

---

## Step 2: Generate PDF Script

```yaml
SCRIPT_STRUCTURE:
  imports: |
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
    
  page_setup:
    pagesize: A4
    margins: [25*mm, 25*mm, 20*mm, 20*mm]  # left, right, top, bottom
    
  font_setup: |
    # Vietnamese font support — use system fonts
    # macOS: try Helvetica (built-in) or register a TTF with Vietnamese support
    # Fallback: DejaVuSans from reportlab bundled fonts
    import os
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
            except:
                continue
```

---

## Step 3: Style Configuration

```yaml
STYLES:
  title:
    fontName: Helvetica-Bold
    fontSize: 24
    spaceAfter: 12*mm
    alignment: TA_CENTER
    
  heading1:
    fontName: Helvetica-Bold
    fontSize: 16
    spaceBefore: 8*mm
    spaceAfter: 4*mm
    textColor: "#1a1a2e"
    
  heading2:
    fontName: Helvetica-Bold
    fontSize: 13
    spaceBefore: 6*mm
    spaceAfter: 3*mm
    textColor: "#16213e"
    
  body:
    fontName: Helvetica
    fontSize: 11
    leading: 16
    alignment: TA_JUSTIFY
    spaceAfter: 3*mm
    
  table_header:
    fontName: Helvetica-Bold
    fontSize: 10
    textColor: "#FFFFFF"
    background: "#1a1a2e"
    
  table_cell:
    fontName: Helvetica
    fontSize: 10
    padding: 6
```

---

## Step 4: Content Conversion Rules

```yaml
MARKDOWN_TO_PDF:
  headings:
    "# Title" -> Paragraph(text, styles["Title"])
    "## Heading" -> Paragraph(text, styles["Heading1"])  
    "### Subheading" -> Paragraph(text, styles["Heading2"])
    
  paragraphs:
    plain_text -> Paragraph(text, styles["BodyText"])
    
  bold_italic:
    "**bold**" -> "<b>bold</b>"
    "*italic*" -> "<i>italic</i>"
    # reportlab uses XML-like markup inside Paragraph
    
  lists:
    bullet_list -> ListFlowable with ListItem elements
    numbered_list -> ListFlowable with bulletType="1"
    
  tables:
    markdown_table -> Table flowable with TableStyle
    style: alternating row colors, header background
    
  code_blocks:
    fenced_code -> Paragraph with monospace font, gray background
    
  subscript_superscript:
    MUST use XML tags: "<sub>text</sub>" and "<super>text</super>"
    NEVER use Unicode subscript/superscript characters
    reason: reportlab XML tags render correctly; Unicode may not
    
  images:
    "![alt](path)" -> Image(path, width, height)
    auto_scale: fit within page margins
    
  page_breaks:
    "---" or explicit break -> PageBreak()
```

---

## Step 5: Page Numbering and TOC

```yaml
PAGE_FEATURES:
  page_numbers:
    position: bottom center
    format: "Trang {page_num} / {total_pages}"
    implementation: |
      def add_page_number(canvas, doc):
          page_num = canvas.getPageNumber()
          text = f"Trang {page_num}"
          canvas.saveState()
          canvas.setFont("Helvetica", 9)
          canvas.drawCentredString(A4[0]/2, 15*mm, text)
          canvas.restoreState()
          
  table_of_contents:
    condition: Document has 3+ H1/H2 headings
    position: After title page
    auto_generate: true
    
  header:
    content: Document title (abbreviated if long)
    position: top right
    font: Helvetica 8pt, gray
```

---

## Step 6: Save and Verify

```yaml
SAVE_AND_VERIFY:
  1_BUILD:
    command: |
      doc = SimpleDocTemplate(output_path, pagesize=A4, ...)
      doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
      
  2_VERIFY:
    script: |
      import pypdf
      reader = pypdf.PdfReader(output_path)
      page_count = len(reader.pages)
      sample_text = reader.pages[0].extract_text()[:200]
      
  3_REPORT:
    format: |
      File PDF created:
      - Path: {output_path}
      - Size: {file_size}
      - Pages: {page_count}
      - Content: {section_count} sections
```

---

## Error Handling

```yaml
ERRORS:
  font_error:
    detect: Vietnamese characters showing as boxes/question marks
    action: Try alternative font path, fallback to DejaVuSans
    message: "Font error for Vietnamese. Trying alternative..."
    
  image_error:
    detect: Image file not found or unsupported format
    action: Skip image, add placeholder text
    
  table_overflow:
    detect: Table wider than page
    action: Split columns or reduce font size
    
  memory_error:
    detect: Large document exceeds memory
    action: Process in chunks, merge with pypdf
```

---

## What This Skill Does NOT Do

- Does NOT read existing PDFs — that is thu-thap job
- Does NOT create charts — that is tao-hinh job (charts can be embedded as images)
- Does NOT synthesize content — that is bien-soan job
- Does NOT install dependencies — redirects to /cai-dat
