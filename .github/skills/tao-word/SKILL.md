---
name: tao-word
description: |
  Create professional Word (.docx) documents with 3 template styles: corporate, academic, minimal.
  Uses python-docx with A4 page setup. Supports tables, headings, TOC, and custom formatting.
  Always use this skill when the user wants any Word or .docx output — even casual requests like
  "lưu vào file word", "tạo tài liệu", "làm cái báo cáo word", "export text ra file", or
  "cho tôi file để gửi sếp" where a Word document is clearly the right format, even without
  saying "/tao-word" or ".docx".
argument-hint: "[content from bien-soan or direct text] [style: corporate|academic|minimal]"
version: 1.1
---

# Tạo Word — Word Document Output Skill

**References:** `references/word-styles-rules.md`

Generates professional `.docx` files from structured content. The skill uses python-docx with
A4 page setup. Three things regularly cause bugs with python-docx and must be avoided:
- Table column widths: use `WidthType.DXA` (twips), never `WidthType.PERCENTAGE` (it silently
  produces broken layouts in most Word versions)
- Line breaks: create a separate `Paragraph` object for each line, never use `\n` inside a
  `TextRun` (it renders as a literal newline character, not a paragraph break)
- Images: always constrain to `max_width=Inches(6)` to avoid overflow on A4

All responses to the user are in Vietnamese.

---

---

## Step 1: Pre-flight Check

1. Check: `python3 -c "import docx"` → if fail: "Chạy: pip install --user python-docx"
2. Confirm content available (pipeline or ask user)
3. Determine style (user-specified, pipeline-inferred, or ask user: corporate / academic / minimal)
4. Determine output path (default: `./<title>.docx`)

---

## Step 2: Use CLI Script (Recommended)

```yaml
SCRIPT: scripts/gen_docx.py
USAGE: python3 scripts/gen_docx.py --input data.json --output report.docx --style corporate
STYLES: corporate (default) | academic | minimal
JSON_FORMAT: |
  {
    "title": "...", "author": "...", "date": "2026-04-16",
    "sections": [
      {"type": "heading", "level": 1, "text": "Section Title"},
      {"type": "text", "text": "Paragraph content"},
      {"type": "bullets", "heading": "Optional", "items": ["Item 1", "Item 2"]},
      {"type": "table", "heading": "Table", "headers": ["Col1","Col2"], "rows": [["a","b"]]},
      {"type": "quote", "text": "Quote", "author": "Attribution"}
    ]
  }
OUTPUT: Prints "✅ Saved: <path> (<size> KB, <N> sections, style: <style>)"
```

---

## Step 3: Parse Content

Map Markdown to Word elements:
- H1 → Document title; H2 → Heading 1; H3 → Heading 2; H4 → Heading 3
- Paragraphs → Normal; Bullet lists → Bullet style; Numbered lists → List Number
- Tables → Word tables; Bold/italic → Text runs; Blockquotes → Indented italic
- Images (if paths provided) → Inline images (max 6" width, preserve aspect ratio)
  - Position images after their associated paragraph, with a caption below if provided
  - For charts from tao-hinh: embed the PNG at full column width for readability

For style specs (fonts, colors, visual elements): `references/word-styles-rules.md`
For critical rules (tables DXA, lists, images, line breaks): `references/word-styles-rules.md`

---

## Step 3.5: Table of Contents (if 3+ headings)

Documents with 3 or more headings benefit from a table of contents — it helps readers navigate
and looks professional for formal reports.

1. Insert TOC field after the title page (before first H2):
   ```python
   from docx.oxml.ns import qn
   paragraph = doc.add_paragraph()
   run = paragraph.add_run()
   fldChar = OxmlElement('w:fldChar')
   fldChar.set(qn('w:fldCharType'), 'begin')
   run._r.append(fldChar)
   instrText = OxmlElement('w:instrText')
   instrText.set(qn('xml:space'), 'preserve')
   instrText.text = 'TOC \\o "1-3" \\h \\z \\u'
   run2 = paragraph.add_run()
   run2._r.append(instrText)
   fldChar2 = OxmlElement('w:fldChar')
   fldChar2.set(qn('w:fldCharType'), 'end')
   run3 = paragraph.add_run()
   run3._r.append(fldChar2)
   ```
2. The TOC will auto-populate when the user opens the file in Word and presses Ctrl+A, F9
3. Add a note in the report: "Mục lục sẽ tự động cập nhật khi mở file trong Word"

---

## Step 4: Execute & Report

1. Prepare JSON → save to tmp file
2. Run: `python3 .github/skills/tao-word/scripts/gen_docx.py --input <json> --output <path> --style <style>`
3. On error: read traceback, fix script, retry (max 2)
4. Report:
   ```
   ✅ File Word đã tạo:
   📄 {output_path}  |  📏 {file_size}  |  🎨 {style}  |  📊 {N} phần
   ```

---

## What This Skill Does NOT Do

- Does NOT read input files — that's thu-thap
- Does NOT synthesize content — that's bien-soan
- Does NOT generate PDF/HTML/PPT — use respective tao-* skills
- Does NOT install dependencies — redirects to /cai-dat
