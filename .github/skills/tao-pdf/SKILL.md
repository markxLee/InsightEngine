---
name: tao-pdf
description: |
  Create professional PDF documents from synthesized content, with Vietnamese font support.
  Uses reportlab Platypus for complex multi-section layouts, Canvas for simple single-page PDFs.
  Always use this skill when the user wants a PDF output — even casual requests like "xuất PDF",
  "tạo file pdf", "lưu thành PDF để in", "tôi cần file pdf", or "cho tôi file không chỉnh sửa
  được" (read-only document implies PDF) — even without saying "/tao-pdf" or ".pdf".
argument-hint: "[content from bien-soan or direct text] [output path]"
version: 1.1
---

# Tạo PDF — PDF Document Output Skill

**References:** `references/pdf-script-details.md`

Generates professional PDF documents using reportlab. For complex multi-section documents
(the common case), use Platypus — it handles page breaks, headers, and flowing content
automatically. For simple single-page outputs (certificates, labels), the Canvas API is
more direct.

Vietnamese font support is critical for this skill's target audience — the skill registers
system fonts and falls back to DejaVuSans if needed.

All responses to the user are in Vietnamese.

---

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

## PDF Metadata & Bookmarks

Adding metadata makes PDF files searchable and professional — the title shows in browser tabs,
author shows in file properties, and bookmarks let readers jump between sections:

1. **Metadata**: set title, author, subject, and creation date via reportlab's `doc.title`,
   `doc.author`, `doc.subject` properties. These appear in File > Properties in PDF readers.
2. **Bookmarks**: for documents with 3+ sections, add PDF bookmarks (outlines) that mirror
   the heading structure. reportlab supports this via `doc.addOutlineEntry()` or by using
   `Paragraph` with `bookmarkName` parameter.
3. **Page numbers**: always include page numbers ("Trang X / Y") in the footer via
   `onFirstPage` and `onLaterPages` callbacks.

---

## Error Handling

Common issues and recovery strategies:
- **Font error**: Vietnamese characters render as boxes if the font lacks Vietnamese glyphs.
  Try system fonts first (`/System/Library/Fonts/` on macOS), fall back to DejaVuSans which
  has broad Unicode coverage.
- **Image error**: skip the image and add a placeholder text note ("[Hình ảnh không thể
  nhúng vào]"). Don't let one bad image crash the entire document.
- **Table overflow**: wide tables may not fit on A4. Reduce font size to 8pt first; if still
  too wide, split into multiple tables or switch to landscape orientation.
- **Memory error**: very large documents (100+ pages with images) may exhaust memory. Process
  in chunks using pypdf to merge partial PDFs.

---

## What This Skill Does NOT Do

- Does NOT read existing PDFs — that is thu-thap
- Does NOT create charts — that is tao-hinh
- Does NOT synthesize content — that is bien-soan
- Does NOT install dependencies — redirects to /cai-dat
