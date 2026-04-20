---
name: gen-slide
description: |
  Create professional PowerPoint (.pptx) presentations from synthesized content.
  Two engines: Quick mode (pptxgenjs, 10 templates) for pipeline tasks, and Pro mode
  (ppt-master SVG→PPTX) for consulting-grade output with native DrawingML shapes,
  20+ layout templates, 50+ chart templates, and 6700+ icons.
  Colors must be hex without # prefix (pptxgenjs format requirement).
  Always use this skill when the user wants a PowerPoint, deck, or .pptx file — even casual
  requests like "làm bài thuyết trình", "tạo slide", "tôi cần deck để present", "xuất ra
  PowerPoint", "cho tôi file pptx", "tạo bài slide chuyên nghiệp" — even without saying
  "gen-slide". Use Pro mode when user says "slide chuyên nghiệp", "consulting-grade",
  "slide đẹp thật sự", "dùng ppt-master", or has source docs (PDF/DOCX/URL) to convert.
argument-hint: "[content] [mode: quick|pro] [template: corporate-blue|...|mckinsey|google-style|...]"
version: 2.0
compatibility:
  requires:
    - Node.js >= 18
    - pptxgenjs (npm install -g pptxgenjs)
  optional:
    - Python 3.10+ with ppt-master requirements (for Pro mode)
  tools:
    - run_in_terminal
---

# Tạo Slide — PowerPoint Output Skill

**References:** `references/template-styles.md` | `references/pro-mode.md`

**Governance:** Read and follow `.github/RULE.md` — it overrides all instructions below.

**Quality loop (RULE-2):** After generating slides, self-review + auditor gate (>80/100).
Pivot strategies: 1) different layout template, 2) different content density, 3) switch engine.

Two engines — **Pro là mặc định** cho mọi bài thuyết trình mới:

| Mode | Engine | Khi nào dùng |
|------|--------|-------------|
| **Pro** (mặc định) | ppt-master SVG→PPTX | Mọi bài thuyết trình mới — native DrawingML, consulting-grade |
| **Quick** | pptxgenjs (Node.js) | Chỉ khi user yêu cầu rõ ràng "simple", "nhanh", "prototype" |

## Mode Selection

```
User request →
  ├─ Pipeline call từ synthesize HOẶC bất kỳ yêu cầu tạo slide?
  │   → Pro mode (MẶC ĐỊNH)
  │   Đọc `references/pro-mode.md`
  │
  ├─ User nói rõ "slide đơn giản" / "quick" / "nhanh" / "prototype"?
  │   → Quick mode
  │   Tiếp tục đọc bên dưới
  │
  └─ User nói "tạo slide đơn giản" / "5 slides nhanh" / "prototype deck"?
      → Quick mode
```

Pro mode: đọc `references/pro-mode.md`.
Quick mode: tiếp tục đọc bên dưới.

All responses to the user are in Vietnamese.

---

## Step 0: State Read-Back (RULE-13)

Call `save_state.py read-context gen-slide` as FIRST action before any processing. Check `relevant_artifacts[]` for upstream outputs to incorporate.

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
     python3 scripts/save_state.py update --step gen-slide --status completed \
       --data '{"artifacts_injected": ["path1"], "artifacts_available_but_skipped": ["path2"]}'
```

---

## Quick Mode (pptxgenjs)

pptxgenjs produces good visual output with proper support for gradients, shadows, and modern
slide layouts. Colors must be hex strings **without** the `#` prefix (e.g., `"1F4E79"` not
`"#1F4E79"`). The `#` prefix causes silent rendering errors.

---

## Available Templates (Quick Mode)

```yaml
LIGHT:
  corporate-blue:    "Professional navy/blue — business reports"
  corporate-red:     "Bold red — executive summaries, annual reports"
  academic-serif:    "Scholarly serif — research, lectures, thesis"
  minimal-white:     "Clean whitespace — product demos, pitches"
  minimal-gray:      "Soft gray — internal memos, team updates"
  creative-gradient: "Purple-amber — marketing, launch events"
  creative-warm:     "Earthy warm — non-profit, community events"
  tech-modern:       "Teal/blue — product launches, SaaS demos"

DARK:
  dark-gradient:     "Indigo/cyan — tech conferences, engineering"
  dark-neon:         "Neon cyan/magenta — gaming, hackathons"

STYLE_ALIASES:
  corporate → corporate-blue  |  academic → academic-serif
  minimal → minimal-white     |  dark-modern → dark-gradient
  creative → creative-gradient
```

Full color/font specs: `references/template-styles.md`

---

## Step 1: Pre-flight Check

1. Check pptxgenjs: `node -e "require('pptxgenjs')"` → if fail: "Chạy: npm install -g pptxgenjs"
2. Confirm content available; if missing: redirect to gather + compose
3. Determine style (user-specified, pipeline-inferred, or ask)
4. Determine output path (default: `./<title>.pptx`)

### Template-First Protocol (US-13.4.1 / US-13.4.3)

When structured_requirements available with content_requirements:
```bash
# Step 0a: Create structural placeholder
python3 scripts/create_placeholder.py slide output/<filename>.pptx \
  --slide-titles '["Title 1","Title 2","Title 3"]'

# Step 0b: Call auditor with audit_mode: structural to verify slide structure

# Step 3+ (US-13.4.3): slide fill mode is not yet implemented in create_placeholder.py
# Use direct generation with gen_pptx.py — placeholder serves as structural reference only
```

### Thin Content Guard (STRICT — reject and loop back)

A presentation with only bullet-point titles and no substance looks amateurish. This is the
last line of defense against thin output. Better to loop back and enrich content than to
deliver a deck that embarrasses the user.

**Automatic rejection criteria (when called from pipeline):**
- **< 500 words** for a multi-section presentation: REJECT. Do not generate. Signal back to
  synthesize: "❌ Content quá mỏng ({word_count} từ) cho presentation. Cần biên soạn lại
  ở mức comprehensive." This triggers synthesize's quality loop to re-run compose.
- **Sections with only 1 bullet or 1 sentence**: these will produce nearly-empty slides.
  If more than 40% of sections are this thin, REJECT and loop back.
- **All sections are surface-level** (no data, no examples, no specifics): REJECT. A
  presentation without concrete content wastes the audience's time.
- **No speaker notes content**: For comprehensive content, compose should provide enough
  material for both slides AND speaker notes. If content is only enough for slide text,
  it's too thin.

**When called standalone:**
- Warn: "⚠️ Nội dung chỉ có ~{word_count} từ. Bài thuyết trình sẽ khá mỏng. Bạn muốn
  bổ sung thêm không?"
- Proceed if user insists

---

## Step 2: Plan Slide Structure

Before mapping content mechanically to slides, analyze the content to make intelligent
presentation decisions. A good presentation tells a story — it doesn't just dump information
onto slides. This analysis step is what separates a "slide deck" from a "presentation."

### Narrative Analysis

Read the synthesized content and identify the **narrative arc**:

```yaml
NARRATIVE_PATTERNS:
  problem_solution:
    structure: "Situation → Problem → Analysis → Solution → Results"
    slide_design: "Open with compelling problem statement, build tension, resolve"
    best_for: "Business proposals, project pitches, case studies"
  
  timeline_journey:
    structure: "Past → Present → Future (or chronological events)"
    slide_design: "Visual timeline flow, milestone highlights"
    best_for: "Progress reports, history overviews, roadmaps"
  
  comparison:
    structure: "Option A vs Option B (or multi-option)"
    slide_design: "Side-by-side layouts, comparison tables, pros/cons"
    best_for: "Decision reports, market analysis, product comparisons"
  
  deep_dive:
    structure: "Overview → Detail 1 → Detail 2 → ... → Synthesis"
    slide_design: "Start broad, zoom in per topic, end with big picture"
    best_for: "Research presentations, technical deep-dives, training"
  
  data_story:
    structure: "Key Insight → Supporting Data → Implications → Action"
    slide_design: "Lead with the conclusion, then show evidence"
    best_for: "Analytics reports, quarterly reviews, KPI dashboards"
```

### Audience & Density Calibration

Think about who will see this presentation — it changes everything about slide density:
- **Executive audience**: fewer slides, more white space, 1 key takeaway per slide, big
  numbers and conclusions up front, skip methodology details
- **Technical audience**: can handle denser slides, include methodology and data tables,
  more content per slide is acceptable
- **General/mixed audience**: balance — use progressive disclosure (simple slide → detail
  slide for those who want to dig in)

Default to the content context when the user doesn't specify audience. A quarterly business
report implies executive; a research paper implies technical; a workshop implies general.

### Content-to-Slide Intelligence

For each piece of content, decide the optimal slide treatment:

| Content type | Bad (mechanical) | Good (intelligent) |
|---|---|---|
| 10 bullet points | 1 slide with 10 bullets | 2-3 slides, grouped by theme |
| Raw data table | Full table on one slide | Key insight as headline + simplified table |
| Long paragraph | Text dump slide | Extract 1 key message + supporting visual |
| Statistics/numbers | Buried in text | "Big number" highlight slide |
| Process/steps | Numbered list | Step-by-step with visual flow |
| Before/after | Two separate slides | Side-by-side comparison slide |

### Engagement Techniques

Weave these into the structure naturally (not forced):
- **Opening hook**: start with a question, surprising stat, or bold statement — not a
  table of contents (TOC slides are rarely engaging)
- **Data highlights**: when you have a striking number, give it its own "big number" slide
  (e.g., huge "47%" centered with a one-line explanation)
- **Breathing slides**: between dense sections, add a section divider or visual-only slide
  so the audience can reset
- **Strong close**: end with a clear call-to-action or key takeaway, not just "Thank you"

Report the analysis:
```
🎯 Phân tích nội dung:
- Narrative: {pattern} (ví dụ: problem → solution)
- Đối tượng: {audience_type}
- Mật độ: {density_recommendation}
- Kỹ thuật: {engagement_notes}
- Đề xuất: {N} slides (thay vì {M} nếu làm cơ học)
```

### Map to Slides

### Map to Slides

Map content to slide types using the narrative analysis above:
- H1 → title slide; H2 → section divider; H3 → content slide title
- Bullet lists → content bullets (max 6/slide); Tables → table slide; Images → image slide
- Key data points → highlight/callout slide; Auto-add closing slide with call-to-action

**Content overflow**: when a section has more than 6 bullet points, split across multiple
slides (e.g., "Key Findings (1/2)" and "Key Findings (2/2)"). Long paragraphs should be
condensed to bullets — slides are visual aids, not documents. Aim for 15-25 slides total;
more than 30 slides usually means content needs more aggressive condensation.

Present plan to user (interactive):
```
📊 Kế hoạch slide ({N} slides):
1. Title: "{title}"
2. Section: "{section_1}"
3. Content: "{point_1}" (bullets)
...
Bạn muốn điều chỉnh gì không?
```

---

## Step 3: Prepare Data & Run Script

1. Prepare content as JSON → save to `tmp/{timestamp}_slides.json`
2. Select template from STYLE_ALIASES or user-specified name
3. Run script:
   ```
   node .github/skills/gen-slide/scripts/<template>.js --input <json> --output <output.pptx>
   ```
4. JSON format:
   ```json
   {
     "title": "...",
     "slides": [
       {"type": "title", "title": "...", "subtitle": "..."},
       {"type": "section", "title": "..."},
       {"type": "content", "title": "...", "bullets": ["..."], "notes": "Talking points"},
       {"type": "two-column", "title": "...", "left": ["..."], "right": ["..."]},
       {"type": "table", "title": "...", "headers": ["Col1"], "rows": [["a"]]},
       {"type": "image", "title": "...", "image_path": "..."},
       {"type": "quote", "text": "...", "author": "..."},
       {"type": "closing", "title": "Cảm ơn!", "subtitle": "Questions?"}
     ]
   }
   ```
5. Notes field: optional on any slide → written as PowerPoint speaker notes (View → Notes)
6. Auto-generate notes when synthesize sets `include_notes: true` (compose provides notes)

---

## Step 4: Post-Generation Verification & Report

```
╔══════════════════════════════════════════════════════════════════╗
║  🔴 DO NOT SKIP: Read the generated .pptx BEFORE reporting     ║
║  A "successful" script can produce slides with no real content. ║
╚══════════════════════════════════════════════════════════════════╝
```

1. Check exit code; on error: read traceback, fix data, retry (max 2)
2. **READ**: `read_file` the .pptx (via markitdown) or re-read the input JSON
3. **COUNT**: slides generated, bullets per slide, total words across all slides
4. **CHECK DEPTH**: Each content slide should have ≥ 3 bullet points with specific data/examples.
   Slides with only a title and 1 generic bullet = THIN → re-generate with richer content.
5. **CHECK COVERAGE**: Compare slide topics vs input sections — any section missing?
6. **If thin/missing** → enrich the JSON data → re-run script (max 2 retries)
7. Clean up tmp JSON file
8. Report:
   ```
   ✅ File PowerPoint đã tạo:
   📄 {output_path}  |  📏 {file_size}  |  🎨 {style}  |  📊 {slide_count} slides
   Verified: {total_words} từ across slides, {thin_count} thin slides fixed
   ```

---

## Examples

**Example 1 — Business presentation:**
Input: Quarterly report content, 6 sections, with data tables
Output: corporate-blue .pptx, 20 slides (title + 6 sections + closing), speaker notes, 180 KB

**Example 2 — Tech conference deck:**
Input: Product launch content with code samples and screenshots
Output: dark-gradient .pptx, 15 slides, code slides with syntax, image slides, 250 KB

**Example 3 — Academic lecture:**
Input: Research findings, 8 sections, bullet-heavy content (needs splitting)
Output: academic-serif .pptx, 25 slides (long sections split across 2-3 slides), 150 KB

---

## Step 5: Shared Auditor Agent Call (Post-Generation)

```yaml
AUDITOR_GATE:
  when: After slide generation and verification
  how:
    1. READ .github/agents/auditor.agent.md
    2. BUILD prompt with:
       user_request: original user request
       output_content: slide titles + content summaries from .pptx
       output_format: "slides"
       required_fields: topics/sections user wanted
       structured_requirements: from `python3 scripts/save_state.py check-requirements` (if available)
    3. CALL runSubagent(agentName="auditor", prompt=<built_prompt>, description="Audit Slide output")
    4. PARSE response:
       IF VERDICT == PASS → return to orchestrator
       IF VERDICT == FAIL → re-generate slides with IMPROVEMENTS guidance (max 2 retries)
  budget: Counts toward max 5 auditor calls per pipeline run
  skip_when: Standalone quick generation
```

---

## Step 6: Artifact Registration (RULE-13)

Call `save_state.py register-artifact --step gen-slide --path <file> --type draft_output --summary "<text>"` for every file created in `tmp/` or `output/`.

---

## What This Skill Does NOT Do

- Does NOT read input files — that's gather
- Does NOT synthesize content — that's compose
- Does NOT generate Word/PDF/HTML — use respective gen-* skills
- Does NOT install dependencies — redirects to setup
- Does NOT generate chart images — that's gen-image (receives chart PNGs as input)
