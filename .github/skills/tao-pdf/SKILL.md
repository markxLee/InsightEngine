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

**References:** `references/pdf-script-details.md`

```yaml
MODE: Interactive (asks style) or Pipeline (from tong-hop)
LANGUAGE: Copilot responds in Vietnamese
INPUT: Structured Markdown from bien-soan or user text
OUTPUT: .pdf file
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

## Step 1: Pre-flight Check

1. Check: `python3 -c "from reportlab.platypus import SimpleDocTemplate"` → if fail: "pip install --user reportlab"
2. Check: `python3 -c "import pypdf"` → if fail: "pip install --user pypdf"
3. Confirm content available (pipeline or ask user)

---

## Step 2: Use CLI Script (Recommended)

```yaml
SCRIPT: scripts/gen_pdf.py
USAGE: python3 scripts/gen_pdf.py --input content.json --output report.pdf --style corporate
STYLES: corporate (default) | academic | minimal
JSON_FORMAT: |
  {
    "title": "...", "author": "...", "date": "2026-04-16",
    "sections": [
      {"type": "heading", "level": 1, "text": "Section Title"},
      {"type": "text", "text": "Paragraph content"},
      {"type": "bullets", "heading": "List", "items": ["Item 1", "Item 2"]},
      {"type": "table", "heading": "Table", "headers": ["Col1","Col2"], "rows": [["a","b"]]},
      {"type": "quote", "text": "Quote", "author": "Attribution"},
      {"type": "page_break"}
    ]
  }
OUTPUT: Prints "✅ Saved: <path> (<size> KB, <N> sections, style: <style>)"
```

---

## Step 3: Analyze Content

1. Determine document complexity: simple (Canvas API) vs complex multi-page (Platypus — default)
2. Check for: tables, images to embed, need for table of contents (3+ headings), page orientation
3. Register Vietnamese font from system (see `references/pdf-script-details.md`)

---

## Step 4: Convert Content & Build

1. Convert Markdown → reportlab flowables (Paragraph, Table, Image, ListFlowable, PageBreak)
2. Critical: use `<sub>` / `<super>` XML tags — NEVER Unicode subscript/superscript characters
3. Build document: `doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)`
4. For full import/style/conversion specs: `references/pdf-script-details.md`

---

## Step 5: Verify & Report

1. Verify with pypdf: `len(reader.pages)` and sample text extraction
2. Report:
   ```
   ✅ File PDF:
   - Đường dẫn: {output_path}
   - Kích thước: {file_size}
   - Số trang: {page_count}
   - Số phần: {section_count}
   ```

---

## Error Handling

```yaml
ERRORS:
  font_error: Try alternative font path; fallback to DejaVuSans
  image_error: Skip image, add placeholder text
  table_overflow: Split columns or reduce font size
  memory_error: Process in chunks, merge with pypdf
```

---

## What This Skill Does NOT Do

- Does NOT read existing PDFs — that is thu-thap
- Does NOT create charts — that is tao-hinh
- Does NOT synthesize content — that is bien-soan
- Does NOT install dependencies — redirects to /cai-dat
