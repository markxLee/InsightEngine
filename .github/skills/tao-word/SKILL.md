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
compatibility:
  requires:
    - Python >= 3.10
    - python-docx >= 1.1.0
  tools:
    - run_in_terminal
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

### Thin Content Guard (STRICT — reject and loop back)

Before generating the document, check if the input content is substantive enough for the
requested output. This is the last line of defense against thin output. A professionally
formatted document with shallow content is worse than no document — it makes the entire
pipeline look incompetent.

**Automatic rejection criteria (when called from pipeline):**
- **< 1000 words** for a multi-section report: REJECT. Do not generate. Signal back to
  tong-hop: "❌ Content quá mỏng ({word_count} từ) cho Word document. Cần biên soạn lại
  ở mức comprehensive." This triggers tong-hop's quality loop to re-run bien-soan.
- **< 500 words** for any document: REJECT. Same as above.
- **Sections with only 1-2 sentences**: Flag as thin. If more than 30% of sections are thin,
  REJECT the entire document and loop back.
- **No data/specifics**: If content is mostly generic text without numbers, examples, or
  specific data, warn: "⚠️ Nội dung thiếu số liệu cụ thể — file Word sẽ trông chung chung."

**When called standalone (not from pipeline):**
- Warn the user and suggest enrichment, but proceed if they insist
- "⚠️ Nội dung chỉ có ~{word_count} từ. Bạn muốn bổ sung thêm trước khi tạo file?"

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

Before converting Markdown to Word elements, analyze the content to make layout decisions
that improve readability. A Word document is not just a formatted text dump — it's a
reading experience. The same content can feel amateur or professional depending on how
it's laid out.

### Content Layout Intelligence

**1. Identify content types and choose optimal treatment:**

| Content pattern | Mechanical approach | Intelligent approach |
|---|---|---|
| Key finding or conclusion | Regular paragraph | **Callout box** — shaded background, slight indent, draws attention |
| Long list (10+ items) | One huge bullet list | **Split into categories** or use a table with 2-3 columns |
| Comparison of 2-3 options | Separate paragraphs | **Side-by-side table** with headers |
| Step-by-step process | Numbered list | **Numbered list + bold first phrase** per step for scannability |
| Statistics/key numbers | Inline in paragraph | **Pull out as bold highlight** or dedicated "Key Metrics" box |
| Dense technical content | Wall of text | **Break with subheadings** every 300-400 words |

**2. Page break intelligence:**
- Add page breaks before major H2 sections (chapter-like breaks) if document > 5 pages
- Never let a heading appear as the last line on a page (widow heading)
- Keep short sections (< 1/3 page) together with their content — don't let them float alone
- Tables that won't fit on the current page → start on next page

**3. Visual rhythm:**
- Alternate between text-heavy and visual elements (tables, charts, bullet lists)
- If the document has 5+ pages of continuous paragraphs, suggest breaking up with a summary
  table, callout box, or visual element
- White space matters — don't cram content. Adequate paragraph spacing (6pt before, 6pt after)
  gives the document room to breathe

### Map to Word Elements

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

### Step 4.5: Post-Generation Verification (MANDATORY)

```
╔══════════════════════════════════════════════════════════════════╗
║  🔴 DO NOT SKIP: Read the generated .docx BEFORE reporting     ║
║  Script exit code 0 does NOT mean quality is acceptable.       ║
╚══════════════════════════════════════════════════════════════════╝
```

1. **READ**: `read_file` the .docx output (markitdown or direct)
2. **COUNT**: total words, number of headings/sections
3. **CHECK**: Are paragraphs substantial? (not just 1-2 sentences per section)
4. **VERIFY**: All expected sections from the input are present in the output
5. **If thin** (< 1000 words for report, missing sections, or > 30% sections have < 100 words):
   → Fix the content JSON → re-generate (max 2 retries)
6. **If OK** → report:
   ```
   ✅ File Word đã tạo:
   📄 {output_path}  |  📏 {file_size}  |  🎨 {style}  |  📊 {N} phần
   Verified: {word_count} từ, {section_count} phần đầy đủ
   ```

---

## Examples

**Example 1 — Corporate report:**
Input: Synthesized Markdown with 5 sections, 3 tables, 2000 words
Output: corporate .docx, 10 pages, TOC, blue headers, formatted tables, 35 KB

**Example 2 — Academic paper:**
Input: Research content with citations, 4000 words, 8 sections
Output: academic .docx, Times New Roman, 18 pages, TOC, proper heading hierarchy, 45 KB

**Example 3 — Minimal memo:**
Input: Short summary, 500 words, 2 sections
Output: minimal .docx, clean layout, 4 pages, no TOC (< 3 headings), 12 KB

---

## Step 5: Shared Auditor Agent Call (Post-Generation)

```yaml
AUDITOR_GATE:
  when: After Step 4.5 verification passes
  how:
    1. READ .github/skills/shared-agents/auditor.md
    2. BUILD prompt with:
       user_request: original user request (from pipeline context or conversation)
       output_content: content read from generated .docx (markitdown or text)
       output_format: "word"
       required_fields: sections/topics user asked for
    3. CALL runSubagent(prompt=<built_prompt>, description="Audit Word output")
    4. PARSE response:
       IF VERDICT == PASS → deliver to user
       IF VERDICT == FAIL → re-generate with IMPROVEMENTS as guidance (max 2 retries)
  budget: Counts toward max 5 auditor calls per pipeline run
  skip_when: Standalone quick generation (user just wants a simple doc, no pipeline)
```

---

## What This Skill Does NOT Do

- Does NOT read input files — that's thu-thap
- Does NOT synthesize content — that's bien-soan
- Does NOT generate PDF/HTML/PPT — use respective tao-* skills
- Does NOT install dependencies — redirects to /cai-dat
