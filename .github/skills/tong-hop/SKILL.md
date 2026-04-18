---
name: tong-hop
description: |
  Main InsightEngine pipeline — analyzes user intent deeply, orchestrates all sub-skills end-to-end,
  and auto-reviews quality at every step. Before execution, expands user prompts into comprehensive
  dimensions and confirms analysis. After each step, reviews output quality — if insufficient, loops
  and retries with specific improvement instructions (max 2 retries). Default content depth is
  COMPREHENSIVE (expert-level, rich content) — not standard or brief.
  Handles any content task: research → synthesis → output in Word/Excel/PPT/PDF/HTML/chart format.
  Supports session resume via save_state.py and chained outputs (e.g., Excel data → chart → slide).
  Always use this skill whenever the user describes any content creation, reporting, or presentation
  task — even casual requests like "làm cái báo cáo", "tổng hợp giúp tôi", "tạo slide từ mấy cái
  file này", "search rồi tạo file", or simply describes what they need without naming a specific
  skill. Also triggers on resume requests: "tiếp tục", "resume", "tiếp tục từ", "/resume".
argument-hint: "[content request in Vietnamese or English]"
version: 1.3
compatibility:
  requires:
    - Python >= 3.10
    - All sub-skill dependencies (see cai-dat)
  tools:
    - run_in_terminal
    - read_file
    - fetch_webpage (for thu-thap)
    - vscode-websearchforcopilot_webSearch (for thu-thap)
---

# Tổng Hợp — InsightEngine Pipeline Orchestrator

**References:** `references/pipeline-ux.md` | `references/session-summary.md` | `references/output-chaining.md` | `references/auto-escalation.md` | `references/file-placement-rules.md` | `references/agent-context-schema.md` | `references/decision-maps.md` | `references/final-audit-rollback.md` | `references/conditional-skill-forge.md` | `references/public-skill-clone.md` | `references/agent-mode.md` | `references/request-analysis.md`
**Agents:** `agents/strategist.md` | `agents/advisory.md`
**State:** `tmp/.session-state.json` (written after each step via `scripts/save_state.py`)

---

## AGENT_MODE Feature Flag

```yaml
AGENT_MODE: true   # default — see references/agent-mode.md for full spec
# true:  strategist → dynamic workflow → tiered audit → advisory → final audit with rollback
# false: original static pipeline (Step 0 → Step 1 → ... → Step 4)
```

---
to a specialized sub-skill (thu-thap → bien-soan → tao-<format>).

**Three key quality mechanisms:**
1. **Request Deep Analysis (Step 1.5)**: Deeply analyze prompt, expand dimensions, confirm before executing
2. **Auto Quality Review (Step 4)**: Review after each sub-skill, retry if insufficient (max 2)
3. **Comprehensive by Default**: 5000-15000 words, expert-level. Only `standard` when user explicitly asks for brevity

All responses in Vietnamese. Pipeline presents plan, waits for approval, then executes with quality checks.

---

## Strict File Placement Rules (ENFORCED)

**Reference:** `references/file-placement-rules.md`

```yaml
FILE_RULES:
  /scripts:  All generated scripts (.py, .js) — NEVER in tmp/ or output/
  /tmp:      Temporary/intermediate files, session state, agent context
  /output:   All final deliverables (.docx, .xlsx, .pptx, .pdf, .html, .png)
  /input:    User-provided source files (read-only)

VALIDATION:
  when: Pipeline start (Step 0) + after each sub-skill (Step 4 quality loop)
  on_violation: Log warning → auto-move to correct directory → continue
  
SKILL_OUTPUT_MAP:
  tao-word → /output/*.docx    | tao-excel → /output/*.xlsx
  tao-slide → /output/*.pptx   | tao-pdf → /output/*.pdf
  tao-html → /output/*.html    | tao-hinh → /output/images/*.png
  thiet-ke → /output/*.png     | thu-thap → /tmp/raw_*.md
  bien-soan → /tmp/synthesized_*.md
```

---

## Step 0: Resume Check (run on every startup)

```bash
python3 scripts/save_state.py check
```

| Output | Action |
|--------|--------|
| `NO_STATE` or `COMPLETED` | Skip to Step 1 (normal start) |
| `IN_PROGRESS` + summary | Show summary to user in Vietnamese (see below), ask "⚡ Tiếp tục hay bắt đầu lại?" |

**If user says tiếp tục / resume / "1" / "tiếp":**
```bash
python3 scripts/save_state.py resume-plan
# Returns JSON list of pending steps
# Skip completed steps — execute ONLY pending steps (from Step 4)
```

**If user says bắt đầu lại / fresh / "2" / "mới":**
```bash
python3 scripts/save_state.py archive
# Then proceed from Step 1 as normal
```

**If no state file OR trigger was NOT a resume keyword:** skip to Step 1 silently.

---

## Step 1: Parse Request

1. Extract **input sources**: file paths, URLs, web-search topics, inline text
2. Determine **processing type**: synthesis (default) | translation | summary
3. Determine **output format**: word (default) | excel | slides | pdf | html
4. Detect **style**: corporate | academic | minimal | dark-modern | creative (see `references/pipeline-ux.md`)
5. Detect if request implies **chained outputs** (see `references/output-chaining.md`)
6. **Detect REQUEST_TYPE** — this fundamentally changes how the pipeline operates:
   ```yaml
   REQUEST_TYPE_DETECTION:
     research:
       # User wants knowledge synthesis — the traditional pipeline flow
       description: "Gather information about a topic → synthesize into a document"
       signals:
         - "tổng hợp về", "làm báo cáo về", "tìm hiểu về", "research about"
         - Request is about understanding a topic, trend, concept
         - Output is a document summarizing knowledge
       pipeline: thu-thap (search) → bien-soan (synthesize) → tao-<format>
       example: "Tổng hợp về xu hướng AI 2024-2026 thành báo cáo Word"

     data_collection:
       # User wants SPECIFIC ITEMS collected into structured output
       description: "Find specific entities (jobs, products, companies, courses) → extract structured fields → tabulate"
       signals:
         - "tìm tất cả", "tìm kiếm các", "liệt kê", "list all", "find all"
         - Request mentions specific fields to extract (tên, lương, URL, địa điểm...)
         - Output is Excel/table with rows = items, columns = fields
         - User wants individual item URLs (not search result pages)
         - Keywords: "job", "việc làm", "sản phẩm", "khóa học", "công ty", "apartment", "giá"
       pipeline: thu-thap (platform-specific search) → extract fields → tao-excel
       example: "Tìm tất cả job fresher JS ở HCM, tạo Excel có tên, lương, URL job"

     mixed:
       # User wants BOTH data collection AND analytical synthesis
       description: "Collect specific items → tabulate → AND analyze/present insights"
       signals:
         - Request has both "tìm tất cả X" AND "tổng hợp/phân tích/thuyết trình"
         - Multiple output formats (Excel + Slide, Excel + Word)
         - Analysis on top of collected data (ranking, recommendation, comparison)
       pipeline: thu-thap (platform search) → extract → tao-excel → bien-soan (analyze) → tao-<format>
       example: "Tìm jobs, tạo Excel tổng hợp, rồi tạo slide phân tích và xếp hạng"

   ```
7. **Extract REQUIRED_FIELDS** (for data_collection/mixed): scan user's prompt for specific
   output fields → create checklist for audit. Always auto-add `direct_url` and `source_platform`.
8. Detect if request needs **visual design**:
   - Poster, cover, certificate, invitation, banner, infographic → **thiet-ke**
   - Data charts → **tao-hinh** (chart) | AI images → **tao-hinh** (image)
   - **Dual routing**: one request can need BOTH (e.g., cover + charts + doc)
9. **Detect research complexity** — classify as standard or deep research:
   ```yaml
   DEEP_RESEARCH_SIGNALS:
     # If ANY of these are true → set research_depth: deep for thu-thap
     - Request has 3+ distinct information dimensions (e.g., "models + benchmarks + timeline + classification")
     - Request spans a temporal range ("từ 2024 đến nay", "qua các năm")
     - Request asks for comparison, classification, or taxonomy ("phân loại", "so sánh", "classify")
     - Request demands exhaustive data ("tất cả", "toàn bộ", "comprehensive", "đầy đủ")
     - Request requires data aggregation ("tổng hợp điểm", "benchmark scores", "collect all")
     - Request involves multi-step reasoning (connecting info from multiple domains)
   
   STANDARD_SEARCH:
     - Single topic, single question ("tìm kiếm về X")
     - Quick overview request
     - Specific URLs or files provided
   ```
   When deep research is detected, the execution plan must reflect this (see Step 3).
10. **Detect content depth** — default is `comprehensive` (5000-15000 words, expert-level).
   Only use `standard` when user explicitly asks for brevity ("tóm tắt", "ngắn gọn", "brief").
   Pass `content_depth` to bien-soan.

---

## Step 1.5: Request Deep Analysis (CRITICAL — DO NOT SKIP)

> **Supplementary examples:** `references/request-analysis.md`

**YOU MUST EXECUTE THIS STEP.** Analyze the user's prompt deeply, expand implicit dimensions,
and present the analysis to the user. DO NOT proceed to Step 2 without completing this analysis.

### 1.5.1: Expand Dimensions (by REQUEST_TYPE)

**If `research` request — Expand analytical dimensions:**

```yaml
DIMENSION_EXPANSION:
  1. CORE_QUESTION: What is the user literally asking for?
  2. IMPLICIT_SUBTOPICS: What sub-topics must be covered to make this useful?
     # "AI trends" → current state, key players, breakthroughs, market data, risks, predictions
  3. CONTEXT_DIMENSIONS: Audience? Decisions supported? Technical level?
  4. DATA_NEEDS: Numbers, statistics, comparisons, timelines, case studies
  5. ANALYTICAL_ANGLES: Comparisons, trend analysis, SWOT, recommendations
  6. SCOPE_BOUNDARIES: What should NOT be included? (to stay focused)
```

**If `data_collection` or `mixed` request — Expand collection strategy:**

```yaml
DATA_COLLECTION_ANALYSIS:
  1. TARGET_ENTITIES: What specific items? ("fresher JavaScript jobs" not just "jobs")
  2. SEARCH_PLATFORMS: Where should we look?
     # MUST identify platform-specific sources. Generic Google returns overview pages, NOT items.
     # Jobs: ITViec.com, TopCV.vn, LinkedIn Jobs, VietnamWorks, Glassdoor
     # Products: Shopee, Tiki, Amazon | Courses: Udemy, Coursera
  3. FILTER_CRITERIA: Location, experience, skills, salary range, etc.
  4. REQUIRED_FIELDS: Fields from user prompt + auto-add direct_url, source_platform
     # direct_url = link to SPECIFIC ITEM PAGE, NEVER a search page
  5. SEARCH_QUERIES: Generate platform-specific queries
     # BAD:  "fresher javascript developer HCM" (generic Google)
     # GOOD: site:itviec.com fresher javascript developer ho chi minh
  6. QUANTITY_EXPECTATION: "tất cả" → 20-50 | "top 10" → 10 | unspecified → 15-30
```

### 1.5.2: Present Analysis to User (MANDATORY — HARD GATE)

```
╔══════════════════════════════════════════════════════════════╗
║  🛑 HARD GATE: YOU MUST STOP HERE AND WAIT FOR USER INPUT  ║
║  Do NOT proceed to Step 2, 3, or 4.                        ║
║  Do NOT skip this step. Do NOT summarize and continue.      ║
║  SHOW the analysis below. WAIT for user response.           ║
╚══════════════════════════════════════════════════════════════╝
```

Display the analysis output in Vietnamese. The format depends on REQUEST_TYPE:

**For research:**
```
🔍 Phân tích yêu cầu:
Yêu cầu gốc: {original_request}
Tôi đề xuất mở rộng phạm vi:
📌 Các khía cạnh: 1. {dim_1} 2. {dim_2} ...
📊 Dữ liệu sẽ thu thập: {data_needs}
🎯 Góc phân tích: {analytical_angles}
⚠️ Không bao gồm: {scope_boundaries}
Đầu ra: {format} kiểu {style}, độ sâu: {content_depth}
👉 Bạn đồng ý? Muốn thêm/bớt khía cạnh nào?
```

**For data_collection/mixed:**
```
🔍 Phân tích yêu cầu thu thập dữ liệu:
Đối tượng: {target_entities} | Tiêu chí lọc: {filters}
📌 Nền tảng sẽ tìm: 1. {platform_1} 2. {platform_2} ...
📊 Thông tin/item: {field_1}, {field_2}, ..., direct_url
🔢 Mục tiêu: ~{quantity} items
{if mixed: "📝 Sau đó sẽ phân tích và tạo {analysis_format}"}
👉 Bạn đồng ý? Muốn thêm/bớt trường nào?
```

**Analysis MUST include:** request_type, detected dimensions/fields, planned steps, content_depth.
**Then STOP. WAIT. Do not generate any further output until user responds.**

### 1.5.3: Handle User Response (ONLY after user replies)

```yaml
USER_RESPONSE:
  approved: ["ok", "đồng ý", "tiếp tục", "được", "yes"] → Proceed to Step 2
  modified: User adjusts → update analysis, re-present if major changes
  no_response: DO NOT PROCEED. The pipeline is paused until user confirms.
```

---

## Step 2: Pre-flight Check

1. Run: `python3 scripts/check_deps.py --silent`
2. If exit 0 → continue to Step 3
3. If exit 1 → respond in Vietnamese: "⚠️ Một số thư viện chưa được cài đặt. Gõ /cai-dat để cài đặt tự động." — STOP

---

## Step 3: Present Execution Plan

Present the plan in Vietnamese with sources, processing, output format, and steps.

```yaml
ROUTING: # Choose based on Step 1 parse results
  single_output:    thu-thap → bien-soan → tao-<format>
  translation_only: thu-thap → bien-soan (translation mode)
  chained_output:   thu-thap → bien-soan → tao-excel → tao-hinh → tao-slide
  search_and_out:   thu-thap (web search) → bien-soan → tao-<format>
  design:           thu-thap → bien-soan → thiet-ke (poster/cover/certificate/banner)
  data_collection:  thu-thap (platform-specific) → extract → tao-excel → kiem-tra
  mixed_collection: thu-thap → extract → tao-excel → bien-soan → tao-<format> → kiem-tra
```

After user approves, save state: `python3 scripts/save_state.py save '<json>'`

### Step 3.5: Print Pipeline Step Trace (MANDATORY)

**Immediately after user approves the plan**, print the numbered step list. This trace MUST
be visible throughout execution — update each step as it completes.

```
📋 Pipeline steps:
  1. ⬜ Phân tích yêu cầu (Step 1.5)
  2. ⬜ Thu thập dữ liệu
  3. ⬜ Biên soạn nội dung
  4. ⬜ Xuất file {format}
  5. ⬜ Kiểm tra đầu ra
```

Adapt steps to match the actual routing. After each step, print updated trace:
- Completed: `✅ {step_name} — {one-line summary}` (e.g., "✅ Thu thập — 12 nguồn, 25K ký tự")
- Skipped: `⏭️ {step_name} — {reason}` (e.g., "⏭️ Biểu đồ — không có dữ liệu số")
- Failed: `❌ {step_name} — {error}` (e.g., "❌ Thu thập URL — timeout sau 3 lần thử")

---

## Step 4: Execute Sub-Skills (with Auto Quality Review Loop)

**Update the step trace (Step 3.5) after EVERY sub-skill completes.**
For chained outputs and intermediate files, see `references/output-chaining.md`.

**CRITICAL: Every step now has an automatic quality review.** After each sub-skill completes,
the orchestrator reviews the output against quality criteria. If quality is insufficient, the
step is re-executed with specific improvement instructions. Maximum 2 retries per step —
if quality is still poor after 2 retries, proceed with a warning to the user.

### Auto Quality Review Protocol

After each sub-skill step, review output against quality criteria (see `references/quality-gates.md`
for full criteria). If quality fails, re-execute with improvement instructions. Max 2 retries.

---

### 4.1: thu-thap (with quality gate)

**Execute:**
- Input: sources from user request + expanded dimensions from Step 1.5
- **If request_type = data_collection or mixed**: pass `mode: data_collection` with:
  - `required_fields`: list of fields to extract per item
  - `search_platforms`: platform-specific search targets from Step 1.5
  - `filter_criteria`: filters (location, experience level, etc.)
  - Thu-thap must search PLATFORM-SPECIFIC (e.g., site:itviec.com) not generic Google
  - Thu-thap must fetch INDIVIDUAL ITEM PAGES, not search result pages
  - Thu-thap must extract structured data fields from each page
  - See `references/data-collection-mode.md` for detailed protocol
- **If research_depth = deep**: pass this flag so thu-thap uses the Deep Research Protocol
  (query decomposition → multi-round search → gap analysis → targeted deep dives).
  Thu-thap will return content organized by research dimensions with coverage assessment.
- **If research_depth = standard**: single-query search as usual
- Output: combined Markdown text (with dimension headers if deep research)
- Report: "✅ Thu thập hoàn tất — {N} nguồn, {total_chars} ký tự"
- Save state: `python3 scripts/save_state.py update --step thu-thap`

**Quality Gate — THU-THAP:** See `references/quality-gates.md` for full criteria.
Key checks: volume (≥5K chars standard, ≥15K deep), coverage of all dimensions, source diversity,
specificity. For data_collection: URL specificity (no search links), field extraction completeness,
item quantity vs target.

### 4.2: Analysis loop (ALWAYS — not just deep research)

After thu-thap returns, **always** analyze the gathered content quality:
- Review each dimension from Step 1.5 analysis against collected data
- If bien-soan identifies critical information gaps:
  - Generate specific follow-up queries targeting the gaps
  - Route back to thu-thap for supplementary search
  - Maximum 2 supplementary rounds (up from 1)
- This loop ensures the synthesis is based on substantive data, not thin scraps

### 4.3: bien-soan (with quality gate)

**Execute:**
- Input: Markdown from thu-thap
- Options: `enrich: true` (always) | `include_notes: true` (if output = presentation)
- **content_depth**: pass the detected depth level (standard | comprehensive)
  - Default: `comprehensive` (produces 5000-15000 words — expert-level depth)
  - Only `standard` if user explicitly asked for brevity
- Output: structured Markdown content
- Report: "✅ Biên soạn hoàn tất — {sections} phần, {total_words} từ"
- Save state: `python3 scripts/save_state.py update --step bien-soan`

**Quality Gate — BIEN-SOAN (MOST CRITICAL):** See `references/quality-gates.md`.
Key checks: depth (≥300 words/section comprehensive), specificity (≥3 data points/section),
structure (H2/H3 hierarchy, tables, takeaways), analytical depth (insights, not just facts).

### 4.3b: Pre-Output URL Validation (data_collection/mixed ONLY — HARD GATE)

**Run BEFORE tao-excel generates the output file, NOT after.**

```bash
python3 scripts/validate_urls.py --urls "url1" "url2" ... --json
```

```yaml
URL_VALIDATION_GATE:
  1. Extract all collected direct_url values from thu-thap output
  2. Run validate_urls.py → classify each as DIRECT/SEARCH/LISTING/AMBIGUOUS
  3. For SEARCH or LISTING URLs:
     a. Auto re-fetch: search for specific item on the same platform
     b. Replace invalid URL with valid item page URL
  4. After re-fetch, re-validate remaining URLs
  5. Report: "🔗 URL validation: {valid}/{total} URLs verified as direct links"
  6. IF >50% URLs still invalid after re-fetch:
     ⚠️ STOP — ask user: "Chỉ {X}% URLs là link trực tiếp. Bạn muốn tiếp tục hay tìm lại?"
  7. Flag remaining invalid URLs with ⚠️ in Excel output
```

### 4.4: tao-\<format\> (with quality gate)

**Execute:**
- Mapping: word → tao-word | excel → tao-excel | slides → tao-slide | pdf → tao-pdf | html → tao-html
- Input: synthesized content from bien-soan
- Output: final file
- Report: "✅ Xuất file hoàn tất — {path} ({size})"
- Save state: `python3 scripts/save_state.py update --step tao-<format> --output-file "<path>"`

**Quality Gate — OUTPUT:** See `references/quality-gates.md`.
Key checks: completeness (all sections present), formatting (no broken tables/headings),
size sanity (docx ≥15KB, pptx ≥50KB, pdf ≥20KB, html ≥5KB).

### 4.5: tao-hinh (conditional — if charts requested OR output is slides with data)
- Report: "✅ Tạo {N} biểu đồ hoàn tất"
- Save state: `python3 scripts/save_state.py update --step tao-hinh --output-file "<chart_path>"`

### 4.6: thiet-ke (conditional — visual design: poster, cover, certificate, banner)
- Input: content + user design intent | Output: PNG/PDF | Save state after completion

### 4.7: Output Audit — kiem-tra (ALWAYS RUN)

After ALL output files generated, run kiem-tra to verify against user's original request.
Inputs: `original_request`, `required_fields`, `expanded_analysis`, `output_files`.
Checks: requirement coverage, URL quality (data_collection), specificity (5-claim sample).
On failure: report → propose fix → re-run (max 1 cycle). On pass: proceed to final report.

---

## Error Recovery

1. **Retry once** — transient errors often resolve on retry
2. **Partial delivery** — if retry fails, save completed work, offer to user
3. **Skip non-critical** — tao-hinh is optional; deliver main doc without charts if it fails
4. **Save state before each step** — enables resume from last completed step
5. **Report clearly** — tell user what failed, what error, what options (retry/skip/fix)

Sub-skills skip their own pre-flight checks when called from pipeline (tong-hop already ran check_deps.py).

---

## Step 5: Final Report

```yaml
FINAL_REPORT:
  format: |
    🎉 Hoàn tất! Kết quả:

    📄 File đầu ra:
    - {file_path} ({file_size})

    ⏱️ Các bước đã thực hiện:
    1. ✅ Thu thập: {source_count} nguồn
    2. ✅ Biên soạn: {word_count} từ
    3. ✅ Xuất {format}: {file_path}

    💡 Bạn muốn chỉnh sửa gì không?
```

After reporting, mark pipeline complete:
```bash
python3 scripts/save_state.py complete
```

---

## Step 6: Session Summary & View Suggestions

After every completed pipeline run:
1. Append session entry to `output/session-summary.md`
2. Show how to open the output file(s)

See `references/session-summary.md` for full format and view suggestion specs.

---

## Examples

| # | Input | Flow | Output |
|---|-------|------|--------|
| 1 | "Tổng hợp 3 file PDF thành báo cáo Word corporate" | Analysis → thu-thap → bien-soan → tao-word | output/bao-cao.docx (20pp) |
| 2 | "Search AI trends 2026, slide dark-modern" | Analysis → Expand 5 dims → thu-thap (deep) → bien-soan → tao-slide | output/ai-trends.pptx (22 slides) |
| 3 | "Excel sales_data.xlsx → chart → Word" | thu-thap → bien-soan → tao-hinh → tao-word | report + charts |
| 4 | "Tìm jobs fresher JS HCM, Excel + slide phân tích" | type=mixed → thu-thap (platform) → tao-excel → bien-soan → tao-slide → kiem-tra | xlsx + pptx |

---

## What This Skill Does NOT Do

- Does NOT generate content itself — delegates to sub-skills
- Does NOT install dependencies — redirects to /cai-dat
- Does NOT process files directly — uses thu-thap
- Does NOT skip the execution plan — always shows plan first
