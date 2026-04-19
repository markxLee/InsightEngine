---
name: synthesize
description: |
  Content synthesis skill for InsightEngine — gathers, merges, and structures multi-source content
  into coherent documents. Called by the orchestrator orchestrator agent or directly via synthesize.
  Handles the core content pipeline: gather → compose → tao-[format] with auto quality review.
  Default content depth is COMPREHENSIVE (expert-level, rich content).
  Supports session resume via save_state.py and chained outputs (e.g., Excel data → chart → slide).
  NOTE: Orchestration (intent classification, routing) is handled by orchestrator agent.
  This skill focuses purely on content synthesis workflows.
argument-hint: "[content request in Vietnamese or English]"
version: 2.0
compatibility:
  requires:
    - Python >= 3.10
    - All sub-skill dependencies (see setup)
  tools:
    - run_in_terminal
    - read_file
    - fetch_webpage (for gather)
    - vscode-websearchforcopilot_webSearch (for gather)
---

# Tổng Hợp — Content Synthesis Skill

> **Role:** Pure content synthesis. Orchestration is handled by `orchestrator` agent.
> When user says `synthesize`, orchestrator intercepts, classifies as synthesis, and routes here.

**References:** `references/pipeline-ux.md` | `references/session-summary.md` | `references/output-chaining.md` | `references/auto-escalation.md` | `references/file-placement-rules.md` | `references/agent-context-schema.md` | `references/decision-maps.md` | `references/final-audit-rollback.md` | `references/conditional-skill-forge.md` | `references/public-skill-clone.md` | `references/agent-mode.md` | `references/request-analysis.md`
**Agents:** `.github/agents/auditor.agent.md` (quality gate)
**State:** `tmp/.session-state.json` (written after each step via `scripts/save_state.py`)

> **Note:** Orchestration agents (strategist, advisory) are called by orchestrator, not by this skill.
> This skill receives a pre-classified synthesis request and executes the content pipeline.

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
   - **research**: "tổng hợp về", "báo cáo", topic understanding → gather → compose → tao-\<format\>
   - **data_collection**: "tìm tất cả", "liệt kê", specific fields/entities → gather (platform) → gen-excel
   - **mixed**: both collection + analysis → gather → gen-excel → compose → tao-\<format\>
7. **Extract REQUIRED_FIELDS** (data_collection/mixed): scan prompt for fields, auto-add `direct_url` + `source_platform`.
8. **Visual design routing**: poster/cover/cert/banner → design | charts → gen-image | both possible.
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
  approved: ["ok", "đồng ý", "tiếp tục", "được", "yes"] → SET autonomy_mode=true → Proceed to Step 2
  modified: User adjusts → update analysis, re-present if major changes
  no_response: DO NOT PROCEED. The pipeline is paused until user confirms.
```

### 1.5.4: Autonomy Mode (MANDATORY after user approval)

```yaml
AUTONOMY_MODE:
  # Set when user confirms at Step 1.5. Persists for the entire pipeline run.
  activate_on: User response matching approved signals above
  
  WHEN_ACTIVE:
    - Execute ALL remaining steps (2→7) without stopping or asking
    - Auto-decide ALL technical choices: libraries, query strategy, platform order,
      file format details, retry counts, batch size
    - SUPPRESS all confirmation prompts between steps
    - SUPPRESS "Bạn có muốn tiếp tục?" style questions
    - Only 2 allowed interruptions:
        a. CONTENT ambiguity: scope or field is genuinely unclear from the request
           (max 1 clarifying question — ask it inline, proceed with best assumption if not answered)
           ⚠️ Classification guide: references/content-only-filter.md
        b. TOTAL failure: all retry attempts exhausted and data collection completely failed
    - Show periodic progress updates (non-interactive): "✅ Step 3 done — 45 items collected"
    
  CONTENT_VS_TECHNICAL:
    # Full classification: references/content-only-filter.md
    CONTENT (may ask once): which companies to include, output language, which provinces, data cutoff date
    TECHNICAL (never ask): which library, how many retries, confirm seed generation,
      approve each batch, confirm file format, confirm query strategy, install dependencies,
      step transitions ("Step 1 done, proceed?"), batch size, retry approval
      
  PROGRESS_FORMAT:
    each_step: "⚙️ {step_name}... ✅ done ({summary})"
    data_collection: "🔍 {source}: ✅ {count} items"
    file_generation: "📄 Đang tạo {file_type}..."
    completion: Single delivery summary message (see Step 7)
```

---

## Step 2: Pre-flight Check

1. Run: `python3 scripts/check_deps.py --silent`
2. If exit 0 → continue to Step 3
3. If exit 1 → respond in Vietnamese: "⚠️ Một số thư viện chưa được cài đặt. Gõ setup để cài đặt tự động." — STOP

---

## Step 3: Present Execution Plan

Present the plan in Vietnamese with sources, processing, output format, and steps.

```yaml
ROUTING: # Choose based on Step 1 parse results
  single_output:    gather → compose → tao-<format>
  translation_only: gather → compose (translation mode)
  chained_output:   gather → compose → gen-excel → gen-image → gen-slide
  search_and_out:   gather (web search) → compose → tao-<format>
  design:           gather → compose → design (poster/cover/certificate/banner)
  data_collection:  gather (platform-specific) → extract → gen-excel → verify
  mixed_collection: gather → extract → gen-excel → compose → tao-<format> → verify
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
| gather | Read collected content | ≥5K chars (standard), ≥15K (deep) | Re-search with expanded queries |
| gather (DC) | Open 3 URLs with fetch_webpage | URLs are item pages, not search | Re-fetch from platform |
| compose | Read synthesized text | ≥300 words/section, ≥3 data points each | Re-synthesize with depth flag |
| gen-word | `read_file` the .docx (via markitdown) | ≥1000 words, all sections present | Re-generate |
| gen-excel | Read output rows + open 2 URLs | Data in cells, URLs work, formulas correct | Re-generate + re-fetch bad URLs |
| gen-slide | Read slide JSON/content | ≥8 slides, each has ≥3 bullet points with data | Re-generate |
| gen-pdf | Read content | Matches source, Vietnamese renders | Re-generate |
| gen-html | Read HTML source | All sections, reveal.js works, styles applied | Re-generate |

---

### 4.1: gather (with quality gate)

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
- **If research_depth = deep**: pass this flag so gather uses the Deep Research Protocol
  (query decomposition → multi-round search → gap analysis → targeted deep dives).
  Thu-thap will return content organized by research dimensions with coverage assessment.
- **If research_depth = standard**: single-query search as usual
- Output: combined Markdown text (with dimension headers if deep research)
- Report: "✅ Thu thập hoàn tất — {N} nguồn, {total_chars} ký tự"
- Save state: `python3 scripts/save_state.py update --step gather`

**⚠️ VERIFY (mandatory):** Read the collected content. For data_collection: open 3 URLs with
`fetch_webpage` — are they real item pages? Do titles match? If search/listing pages → re-fetch.

### 4.2: Analysis loop (ALWAYS — not just deep research)

After gather returns, **always** analyze the gathered content quality:
- Review each dimension from Step 1.5 analysis against collected data
- If compose identifies critical information gaps:
  - Generate specific follow-up queries targeting the gaps
  - Route back to gather for supplementary search
  - Maximum 2 supplementary rounds (up from 1)
- This loop ensures the synthesis is based on substantive data, not thin scraps

### 4.3: compose (with quality gate)

**Execute:**
- Input: Markdown from gather
- Options: `enrich: true` (always) | `include_notes: true` (if output = presentation)
- **content_depth**: pass the detected depth level (standard | comprehensive)
  - Default: `comprehensive` (produces 5000-15000 words — expert-level depth)
  - Only `standard` if user explicitly asked for brevity
- Output: structured Markdown content
- Report: "✅ Biên soạn hoàn tất — {sections} phần, {total_words} từ"
- Save state: `python3 scripts/save_state.py update --step compose`

**⚠️ VERIFY (mandatory):** Read the synthesized content. Count words per section. Are there
specific numbers, names, examples? If any section is < 200 words or purely generic → re-synthesize.

### 4.3b: Pre-Output URL Validation (data_collection/mixed ONLY — HARD GATE)

**Run BEFORE gen-excel generates the output file, NOT after.**

```bash
python3 scripts/validate_urls.py --urls "url1" "url2" ... --json
```

```yaml
URL_VALIDATION_GATE:
  1. Extract all collected direct_url values from gather output
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
- Mapping: word → gen-word | excel → gen-excel | slides → gen-slide | pdf → gen-pdf | html → gen-html
- Input: synthesized content from compose
- Output: final file
- Report: "✅ Xuất file hoàn tất — {path} ({size})"
- Save state: `python3 scripts/save_state.py update --step tao-<format> --output-file "<path>"`

**⚠️ VERIFY (mandatory):** `read_file` the output file. For Excel: are rows populated with real
data? Open 2 URLs — do pages match? For Word: ≥1000 words? For Slides: ≥8 slides with content?
For any format: if output is thin/empty/broken → re-generate. Do NOT move on just because script exited 0.

### 4.5: gen-image (conditional — if charts requested OR output is slides with data)
- Report: "✅ Tạo {N} biểu đồ hoàn tất"
- Save state: `python3 scripts/save_state.py update --step gen-image --output-file "<chart_path>"`

### 4.6: design (conditional — visual design: poster, cover, certificate, banner)
- Input: content + user design intent | Output: PNG/PDF | Save state after completion

### 4.7: Output Audit — verify (ALWAYS RUN — INTELLIGENCE-DRIVEN)

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
3. **Skip non-critical** — gen-image optional; deliver main doc without charts
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
| 1 | "Tổng hợp 3 file PDF thành báo cáo Word corporate" | Analysis → gather → compose → gen-word | output/bao-cao.docx (20pp) |
| 2 | "Search AI trends 2026, slide dark-modern" | Analysis → Expand 5 dims → gather (deep) → compose → gen-slide | output/ai-trends.pptx (22 slides) |
| 3 | "Excel sales_data.xlsx → chart → Word" | gather → compose → gen-image → gen-word | report + charts |
| 4 | "Tìm jobs fresher JS HCM, Excel + slide phân tích" | type=mixed → gather (platform) → gen-excel → compose → gen-slide → verify | xlsx + pptx |

---

## What This Skill Does NOT Do

- Does NOT generate content — delegates to sub-skills
- Does NOT install deps — redirects to setup
- Does NOT skip execution plan — always shows plan first
