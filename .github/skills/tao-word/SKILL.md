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

**References:** `references/word-styles-rules.md`

```yaml
MODE: Interactive (asks style) or Pipeline (style from tong-hop)
LANGUAGE: Copilot responds in Vietnamese
INPUT: Structured Markdown from bien-soan or user text
OUTPUT: .docx file (A4, 1" margins)
LIBRARY: python-docx
CRITICAL: Use WidthType.DXA for tables (never PERCENTAGE), separate Paragraph for each line (never \n in TextRun)
```

---

## Trigger Conditions

Use this skill when user:
- Says "tạo file word", "xuất word", "tạo tài liệu word", "tạo file .docx"
- Says "create word document", "export to word"
- Uses command `/tao-word`
- Pipeline (tong-hop) routes content here for Word output

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
- Images (if paths provided) → Inline images (max 6" width)

For style specs (fonts, colors, visual elements): `references/word-styles-rules.md`
For critical rules (tables DXA, lists, images, line breaks): `references/word-styles-rules.md`

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
