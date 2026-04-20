---
name: gen-pdf
description: |
  Create professional PDF documents from synthesized content, with Vietnamese font support.
  Uses reportlab Platypus for complex multi-section layouts, Canvas for simple single-page PDFs.
  Always use this skill when the user wants a PDF output — even casual requests like "xuất PDF",
  "tạo file pdf", "lưu thành PDF để in", "tôi cần file pdf", or "cho tôi file không chỉnh sửa
  được" (read-only document implies PDF) — even without saying "gen-pdf" or ".pdf".
argument-hint: "[content from compose or direct text] [output path]"
version: 1.1
compatibility:
  requires:
    - Python >= 3.10
    - reportlab >= 4.1.0
    - pypdf >= 4.0.0
  tools:
    - run_in_terminal
---

# Tạo PDF — PDF Document Output Skill

**References:** `references/pdf-script-details.md`

**Governance:** Read and follow `.github/RULE.md` — it overrides all instructions below.

**Quality loop (RULE-2):** After generating the PDF, self-review + auditor gate (>80/100).
Pivot strategies: 1) different layout engine, 2) restructure page layout, 3) adjust content flow.

Generates professional PDF documents using reportlab. For complex multi-section documents
(the common case), use Platypus — it handles page breaks, headers, and flowing content
automatically. For simple single-page outputs (certificates, labels), the Canvas API is
more direct.

Vietnamese font support is critical for this skill's target audience — the skill registers
system fonts and falls back to DejaVuSans if needed.

All responses to the user are in Vietnamese.

---

---

## Step 0: State Read-Back (RULE-13)

Call `save_state.py read-context gen-pdf` as FIRST action before any processing. Check `relevant_artifacts[]` for upstream outputs to incorporate.

---

## Step 0.5: Artifact Evidence Injection (US-18.3.2)

After read-context, check `relevant_artifacts[]` for evidence to enrich the output document.
This is ADDITIVE — it does not replace compose output, only enriches it with supporting material.

```yaml
EVIDENCE_INJECTION:
  1. Parse `relevant_artifacts[]` from read-context
  2. For each artifact with `retention: keep` AND `quality_score >= 60`:
     - type `chart` or `image` → embed or reference in document where topically relevant
     - type `data_table` or `excel_data` → extract key rows/figures for inline tables
     - type `search_results` → use as source citations
     - type `gathered_content` → extract supporting quotes or data points
  3. Injection rules:
     - Place evidence NEAR the section it supports (not in a separate appendix)
     - Add brief caption or attribution: "(Nguồn: {artifact_summary})"
     - Do NOT inject if it would disrupt document flow — quality over completeness
  4. Log usage to state for auditor verification:
     python3 scripts/save_state.py update --step gen-pdf --status completed \
       --data '{"artifacts_injected": ["path1"], "artifacts_available_but_skipped": ["path2"]}'
```

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

### Thin Content Guard (STRICT — reject and loop back)

PDF is often the final delivery format — it goes to bosses, clients, or gets printed. A thin
PDF is worse than a thin Word doc because the recipient can't easily fix it.

**Automatic rejection criteria (when called from pipeline):**
- **< 1000 words** for a multi-section report PDF: REJECT. Signal back to synthesize:
  "❌ Content quá mỏng ({word_count} từ) cho PDF. Cần biên soạn lại ở mức comprehensive."
- **< 500 words** for any PDF: REJECT (unless it's a single-page certificate/label).
- **Sections without substance**: If more than 30% of sections have only 1-2 sentences, REJECT.

**When called standalone:** warn the user and suggest enrichment.

### Content Intelligence for PDF

PDF is often the final delivery format — the user sends it to a boss, prints it, or attaches
it to an email. Unlike Word, the recipient can't easily edit it, so the layout must be right
the first time. Analyze the content before building:

**1. Layout decisions based on content:**
- Wide tables (6+ columns) → switch to landscape orientation for that page, or reduce font
  size to 8pt. Don't let tables overflow and get silently clipped
- Heavy data content (multiple tables, charts) → use 2-column layout for narrative text
  between data elements to avoid the "wall of tables" problem
- Short document (< 2 pages) with formal purpose → Canvas API with careful positioning
  gives a more polished result than Platypus flow layout

**2. Visual hierarchy emphasis:**
- Identify the 2-3 most important findings/conclusions in the content
- Render them with visual emphasis: slightly larger font, colored left border bar, or
  shaded background box — so they stand out when someone skims the PDF
- Section titles should have consistent visual treatment (color, size, spacing) that creates
  a clear hierarchy when scrolling through the document

**3. Print-awareness:**
- PDFs are frequently printed. Ensure adequate margins (≥ 20mm all sides)
- Avoid light gray text or very thin lines that disappear on lower-quality printers
- Images and charts at ≥ 150 dpi for print quality
- If the document will be bound (reports, theses), add extra inner margin (gutter: 10mm)

---

## Step 4: Convert Content & Build

1. Convert Markdown → reportlab flowables (Paragraph, Table, Image, ListFlowable, PageBreak)
2. Critical: use `<sub>` / `<super>` XML tags — NEVER Unicode subscript/superscript characters
3. Build document: `doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)`
4. For full import/style/conversion specs: `references/pdf-script-details.md`

---

## Step 5: Verify & Report

1. Verify with pypdf: `len(reader.pages)` and sample text extraction
2. **READ BACK (mandatory)**: Extract text from 2-3 pages with pypdf — verify content is present,
   Vietnamese renders correctly (not garbled), and sections match input. If empty/broken → re-generate.
3. Report:
   ```
   ✅ File PDF:
   - Đường dẫn: {output_path}  |  📏 {file_size}  |  📄 {page_count} trang
   Verified: text extracted ✓, sections present ✓
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

## Examples

**Example 1 — Multi-section report:**
Input: Synthesized content, 8 sections, 3000 words, 2 tables
Output: corporate PDF, 12 pages, TOC bookmarks, page numbers, Vietnamese fonts, 85 KB

**Example 2 — Simple one-page summary:**
Input: Short executive summary, 300 words
Output: Minimal PDF, 1 page, Canvas API, clean layout, 15 KB

**Example 3 — Report with embedded charts:**
Input: Content + 3 chart PNGs from gen-image
Output: PDF with inline images, captions, proper page breaks, 250 KB

---

## Step 5: Shared Auditor Agent Call (Post-Generation)

```yaml
AUDITOR_GATE:
  when: After PDF generation and verification
  how:
    1. READ .github/agents/auditor.agent.md
    2. BUILD prompt with:
       user_request: original user request
       output_content: text content from generated PDF (via markitdown or source text)
       output_format: "pdf"
       required_fields: sections/topics user asked for
       structured_requirements: from `python3 scripts/save_state.py check-requirements` (if available)
    3. CALL runSubagent(agentName="auditor", prompt=<built_prompt>, description="Audit PDF output")
    4. PARSE response:
       IF VERDICT == PASS → return to orchestrator
       IF VERDICT == FAIL → re-generate with IMPROVEMENTS guidance (max 2 retries)
  budget: Counts toward max 5 auditor calls per pipeline run
  skip_when: Standalone quick generation
```

---

## Step 6: Artifact Registration (RULE-13)

Call `save_state.py register-artifact --step gen-pdf --path <file> --type draft_output --summary "<text>"` for every file created in `tmp/` or `output/`.

---

## What This Skill Does NOT Do

- Does NOT read existing PDFs — that is gather
- Does NOT create charts — that is gen-image
- Does NOT synthesize content — that is compose
- Does NOT install dependencies — redirects to setup
