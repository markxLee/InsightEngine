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
version: 1.4
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
**Agents:** `.github/skills/shared-agents/strategist.md` | `.github/skills/shared-agents/advisory.md` | `.github/skills/shared-agents/auditor.md` | `.github/skills/shared-agents/agent-protocol.md`
**State:** `tmp/.session-state.json` (written after each step via `scripts/save_state.py`)

---

## Shared Agent Architecture

```yaml
AGENT_MODE: always-on   # Shared agents are now canonical (Phase 8 migration)
# Pipeline always uses shared agent architecture:
#   1. Strategist agent → dynamic workflow (shared-agents/strategist.md)
#   2. Tiered audit at every step (shared-agents/auditor.md)
#   3. Advisory agent for decisions (shared-agents/advisory.md)
#   4. Calling protocol: shared-agents/agent-protocol.md
#
# Legacy inline agents (tong-hop/agents/) are ARCHIVED — do not use.
# Budget: strategist=1, advisory=max 2, auditor=max 5 per pipeline run.
```

---

**Quality mechanisms:** (1) Deep Analysis at Step 1.5 with HARD GATE, (2) Auto Quality Review after each sub-skill (max 2 retries), (3) Comprehensive by default (5000-15000 words). All Vietnamese. Shows plan → waits approval → executes.

**File rules** (`references/file-placement-rules.md`): scripts→`/scripts`, temp→`/tmp`, output→`/output`, input→`/input`. Validated at pipeline start + after each step.

---

## Step 0: Resume Check (run on every startup)

Run `python3 scripts/save_state.py check`.
- `NO_STATE`/`COMPLETED` → skip to Step 1
- `IN_PROGRESS` → show summary, ask "Tiếp tục hay bắt đầu lại?"
  - Tiếp tục: `save_state.py resume-plan` → skip completed steps
  - Bắt đầu lại: `save_state.py archive` → Step 1
- No state file or non-resume trigger: skip to Step 1 silently.

---

## Step 1: Parse Request

1. Extract **input sources**: file paths, URLs, web-search topics, inline text
2. Determine **processing type**: synthesis (default) | translation | summary
3. Determine **output format**: word (default) | excel | slides | pdf | html
4. Detect **style**: corporate | academic | minimal | dark-modern | creative (see `references/pipeline-ux.md`)
5. Detect if request implies **chained outputs** (see `references/output-chaining.md`)
6. **Detect REQUEST_TYPE** (details: `references/request-analysis.md`):
   - **research**: "tổng hợp về", "báo cáo", topic understanding → thu-thap → bien-soan → tao-\<format\>
   - **data_collection**: "tìm tất cả", "liệt kê", specific fields/entities → thu-thap (platform) → tao-excel
   - **mixed**: both collection + analysis → thu-thap → tao-excel → bien-soan → tao-\<format\>
7. **Extract REQUIRED_FIELDS** (data_collection/mixed): scan prompt for fields, auto-add `direct_url` + `source_platform`.
8. **Visual design routing**: poster/cover/cert/banner → thiet-ke | charts → tao-hinh | both possible.
9. **Research depth**: deep if 3+ dimensions, temporal range, comparison, exhaustive data; else standard.
10. **Content depth**: default `comprehensive` (5000-15000 words). Only `standard` if user says "tóm tắt"/"ngắn gọn".

---

## Step 1.5: Request Deep Analysis (CRITICAL — DO NOT SKIP)

> **Supplementary examples:** `references/request-analysis.md`

**YOU MUST EXECUTE THIS STEP.** Analyze the user's prompt deeply, expand implicit dimensions,
and present the analysis to the user. DO NOT proceed to Step 2 without completing this analysis.

### 1.5.1: Expand Dimensions (by REQUEST_TYPE)

⚠️ **Full protocol with examples: `references/request-analysis.md` — READ IT.**

**If `research`:** Expand 6 dimensions: CORE_QUESTION, IMPLICIT_SUBTOPICS, CONTEXT_DIMENSIONS, DATA_NEEDS, ANALYTICAL_ANGLES, SCOPE_BOUNDARIES.

**If `data_collection`/`mixed`:** Expand 6 fields: TARGET_ENTITIES, SEARCH_PLATFORMS (platform-specific, NOT generic Google), FILTER_CRITERIA, REQUIRED_FIELDS (+direct_url), SEARCH_QUERIES (site:X.com format), QUANTITY_EXPECTATION.

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

**After user approves**, print numbered step list. Update after each step:
`✅ {name} — {summary}` | `⏭️ {name} — {reason}` | `❌ {name} — {error}`

---

## Step 4: Execute Sub-Skills (with Auto Quality Review Loop)

**Update the step trace (Step 3.5) after EVERY sub-skill completes.**
For chained outputs and intermediate files, see `references/output-chaining.md`.

**CRITICAL: Every step now has an automatic quality review.** After each sub-skill completes,
the orchestrator reviews the output against quality criteria. If quality is insufficient, the
step is re-executed with specific improvement instructions. Maximum 2 retries per step —
if quality is still poor after 2 retries, proceed with a warning to the user.

### VERIFY-OR-LOOP Protocol (applies to EVERY sub-skill below)

```
╔══════════════════════════════════════════════════════════════════════════╗
║  🔴 AFTER EVERY SCRIPT/SUB-SKILL: YOU MUST READ THE ACTUAL OUTPUT     ║
║                                                                        ║
║  Script exit code 0 ≠ success. A script can "succeed" but produce:    ║
║  • Empty/thin content (500 words instead of 5000)                      ║
║  • Broken URLs (404, search pages, wrong items)                        ║
║  • Generic text (no names, numbers, dates, specifics)                  ║
║  • Missing sections (3 of 8 headings present)                          ║
║                                                                        ║
║  YOU MUST: read_file the output → CHECK content → LOOP if bad          ║
╚══════════════════════════════════════════════════════════════════════════╝
```

**After EVERY sub-skill completes, execute this sequence:**

1. **READ the output file** with `read_file` — not just the terminal log
2. **COUNT**: words, sections, rows, slides (depending on format)
3. **SAMPLE**: read 3-5 actual data points/paragraphs — are they specific or generic?
4. **VERIFY URLs** (if any): pick 2-3 URLs → `fetch_webpage` → is it the right page?
5. **JUDGE**: does output genuinely satisfy user's request? (not just "file exists")
6. **If quality fails** → re-run sub-skill with specific fix instructions (max 2 retries)
7. **If still fails after 2 retries** → report honestly to user, proceed with warning

**Minimum quality thresholds:**

| Sub-skill | Verify | Minimum | Fail action |
|-----------|--------|---------|-------------|
| thu-thap | Read collected content | ≥5K chars (standard), ≥15K (deep) | Re-search with expanded queries |
| thu-thap (DC) | Open 3 URLs with fetch_webpage | URLs are item pages, not search | Re-fetch from platform |
| bien-soan | Read synthesized text | ≥300 words/section, ≥3 data points each | Re-synthesize with depth flag |
| tao-word | `read_file` the .docx (via markitdown) | ≥1000 words, all sections present | Re-generate |
| tao-excel | Read output rows + open 2 URLs | Data in cells, URLs work, formulas correct | Re-generate + re-fetch bad URLs |
| tao-slide | Read slide JSON/content | ≥8 slides, each has ≥3 bullet points with data | Re-generate |
| tao-pdf | Read content | Matches source, Vietnamese renders | Re-generate |
| tao-html | Read HTML source | All sections, reveal.js works, styles applied | Re-generate |

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

**⚠️ VERIFY (mandatory):** Read the collected content. For data_collection: open 3 URLs with
`fetch_webpage` — are they real item pages? Do titles match? If search/listing pages → re-fetch.

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

**⚠️ VERIFY (mandatory):** Read the synthesized content. Count words per section. Are there
specific numbers, names, examples? If any section is < 200 words or purely generic → re-synthesize.

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

**⚠️ VERIFY (mandatory):** `read_file` the output file. For Excel: are rows populated with real
data? Open 2 URLs — do pages match? For Word: ≥1000 words? For Slides: ≥8 slides with content?
For any format: if output is thin/empty/broken → re-generate. Do NOT move on just because script exited 0.

### 4.5: tao-hinh (conditional — if charts requested OR output is slides with data)
- Report: "✅ Tạo {N} biểu đồ hoàn tất"
- Save state: `python3 scripts/save_state.py update --step tao-hinh --output-file "<chart_path>"`

### 4.6: thiet-ke (conditional — visual design: poster, cover, certificate, banner)
- Input: content + user design intent | Output: PNG/PDF | Save state after completion

### 4.7: Output Audit — kiem-tra (ALWAYS RUN — INTELLIGENCE-DRIVEN)

```
╔════════════════════════════════════════════════════════════════════╗
║  🔍 INTELLIGENCE AUDIT: READ output, OPEN URLs, COMPARE content  ║
║  Do NOT just run scripts. FETCH URLs with fetch_webpage.          ║
║  COMPARE reported data against what pages actually say.           ║
╚════════════════════════════════════════════════════════════════════╝
```

After ALL output files generated:
1. **READ** actual output content (not just file metadata)
2. **OPEN** URLs from output using `fetch_webpage` — verify they are real item pages
3. **COMPARE** output fields (title, salary, company) against actual page content
4. **REASON** about whether output genuinely matches user's request
5. For research: verify 5 key claims against sources

Inputs: `original_request`, `required_fields`, `expanded_analysis`, `output_files`.
On failure: report with evidence → specific re-fetch instructions → max 1 fix cycle.

---

## Error Recovery

1. **Retry once** — transient errors often resolve on retry
2. **Partial delivery** — save completed work if retry fails
3. **Skip non-critical** — tao-hinh optional; deliver main doc without charts
4. **Save state** before each step for resume | **Report clearly** — what failed, options

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

- Does NOT generate content — delegates to sub-skills
- Does NOT install deps — redirects to /cai-dat
- Does NOT skip execution plan — always shows plan first
