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
version: 1.1
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

**References:** `references/pipeline-ux.md` | `references/session-summary.md` | `references/output-chaining.md`
**State:** `tmp/.session-state.json` (written after each step via `scripts/save_state.py`)

This is the central orchestrator — it never generates content itself, but delegates each phase
to a specialized sub-skill (thu-thap → bien-soan → tao-<format>). This separation matters because
each sub-skill has deep domain expertise (e.g., tao-slide knows about 10 pptxgenjs templates),
and the orchestrator focuses solely on planning, routing, quality control, and error recovery.

**Three key mechanisms that drive quality:**
1. **Request Deep Analysis (Step 1.5)**: Before executing, deeply analyze the user's prompt,
   expand implicit dimensions, and confirm the expanded scope with the user. This prevents
   executing in the wrong direction.
2. **Auto Quality Review Loop (Step 4)**: After every sub-skill step, automatically review
   output quality against specific criteria. If quality is insufficient, loop back with
   targeted improvement instructions. Max 2 retries per step.
3. **Comprehensive by Default**: Default content depth is `comprehensive` (expert-level,
   5000-15000 words). Only downgrade to `standard` when user explicitly asks for brevity.
   The #1 user complaint is thin, shallow output — this default eliminates it.

All responses to the user are in Vietnamese. The pipeline presents an execution plan, waits for
approval, then executes step-by-step with progress reporting and quality checks.

---

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
6. Detect if request needs **visual design** (see routing table below):
   - Poster, cover page, certificate, invitation, banner, infographic layout → **thiet-ke**
   - Data charts (bar, line, pie, radar, scatter) → **tao-hinh** (chart mode)
   - AI-generated illustration, background, character → **tao-hinh** (image mode)
   - Keywords that signal thiet-ke: "poster", "bìa", "cover", "certificate", "bằng khen",
     "thiệp", "invitation", "banner", "infographic", "thiết kế", "design"
7. **Detect research complexity** — classify as standard or deep research:
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
8. **Detect content depth** — how rich should the output be?
   ```yaml
   CONTENT_DEPTH_SIGNALS:
     standard:
       # ONLY when user EXPLICITLY asks for brevity — never assume this
       - "tóm tắt", "tóm lược", "ngắn gọn", "brief", "quick", "overview"
       - "just the key points", "chỉ cần ý chính"
       - Output format is email or memo (inherently short)
     
     comprehensive:
       # DEFAULT — this is the new normal for ALL requests
       # The single biggest user complaint is thin output. Users who invest time
       # in a pipeline request deserve rich, expert-level content by default.
       # Any request that doesn't explicitly ask for brevity gets comprehensive.
       - "tổng hợp", "làm báo cáo", "tạo tài liệu", "viết về"
       - "search rồi tạo file", "tạo slide", "tạo word"
       - Most web search + output requests
       - research_depth was "deep" (auto-upgrade)
       - User specifies a long document type (whitepaper, research report, thesis)
       - "chi tiết", "đầy đủ", "comprehensive", "chuyên sâu", "thật kỹ"
       - "phân tích sâu", "deep analysis", "viết thật chi tiết"
   ```
   Pass `content_depth` to bien-soan. **Default is `comprehensive`** — not `standard` or
   `enriched`. The most common complaint is thin, shallow output. Users who go through a
   multi-step pipeline expect expert-level, substantive content — not a surface-level summary.
   Only downgrade to `standard` when user explicitly asks for brevity.

---

## Step 1.5: Request Deep Analysis (CRITICAL — DO NOT SKIP)

The difference between mediocre and excellent output starts here. Most user prompts are
underspecified — the user has a rich mental model of what they want but only types a short
sentence. This step bridges that gap by analyzing the request deeply, expanding implicit
dimensions, and confirming with the user before execution.

**Why this matters:** Without this step, a request like "làm báo cáo về AI" gets parsed as
"search AI → write report" which produces generic content. With deep analysis, it becomes
"search AI applications in [user's domain], trends 2024-2026, key players, market size,
risks, and opportunities → write analytical report with data tables and recommendations."

### 1.5.1: Expand Request Dimensions

For the user's request, identify ALL implicit dimensions:

```yaml
DIMENSION_EXPANSION:
  for_each_request:
    1. CORE_QUESTION: What is the user literally asking for?
    2. IMPLICIT_SUBTOPICS: What sub-topics must be covered to make this useful?
       - A report about "AI trends" implicitly needs: current state, key players,
         recent breakthroughs, market data, risks/challenges, future predictions
    3. CONTEXT_DIMENSIONS: What context makes this actionable?
       - Who is the audience? (infer from style/format if not stated)
       - What decisions will this support?
       - What level of technical detail is appropriate?
    4. DATA_NEEDS: What specific data would make this credible?
       - Numbers, statistics, comparisons, timelines, case studies
    5. ANALYTICAL_ANGLES: What analysis would add genuine value?
       - Comparisons, trend analysis, SWOT, recommendations, implications
    6. SCOPE_BOUNDARIES: What should NOT be included? (to stay focused)
```

### 1.5.2: Present Analysis for User Confirmation

Present the expanded analysis to the user BEFORE creating the execution plan:

```yaml
ANALYSIS_FORMAT: |
  🔍 **Phân tích yêu cầu:**

  **Yêu cầu gốc:** {original_request}

  **Phân tích mở rộng:**
  Tôi hiểu bạn cần {core_interpretation}. Để tạo nội dung thật sự chất lượng,
  tôi đề xuất mở rộng phạm vi như sau:

  📌 **Các khía cạnh sẽ bao gồm:**
  1. {dimension_1} — {why_this_matters}
  2. {dimension_2} — {why_this_matters}
  3. {dimension_3} — {why_this_matters}
  ...

  📊 **Dữ liệu sẽ thu thập:**
  - {data_need_1}
  - {data_need_2}
  - {data_need_3}

  🎯 **Góc phân tích:**
  - {analytical_angle_1}
  - {analytical_angle_2}

  ⚠️ **Sẽ KHÔNG bao gồm:** {scope_boundaries}

  **Đầu ra:** {format} kiểu {style}, dự kiến {estimated_length}

  👉 Bạn đồng ý với phân tích này không? Có muốn thêm/bớt khía cạnh nào?

USER_RESPONSE_HANDLING:
  approved: Proceed to Step 2 with expanded dimensions
  modified: Adjust dimensions based on feedback, re-present if major changes
  simplified: Respect user's wish to narrow scope, but keep content_depth comprehensive
```

**Important:** This step may feel like it slows the pipeline down, but it prevents the much
worse outcome of executing in the wrong direction and producing irrelevant content. A 30-second
confirmation saves 5 minutes of wasted generation.

---

## Step 2: Pre-flight Check

1. Run: `python3 scripts/check_deps.py --silent`
2. If exit 0 → continue to Step 3
3. If exit 1 → respond in Vietnamese: "⚠️ Một số thư viện chưa được cài đặt. Gõ /cai-dat để cài đặt tự động." — STOP

---

## Step 3: Present Execution Plan

```yaml
PLAN_FORMAT: |
  📋 Kế hoạch thực hiện:

  **Nguồn dữ liệu:** [list each source]
  **Xử lý:** [synthesis | translation | summary]
  **Đầu ra:** [format + style]

  **Các bước:**
  1. Thu thập nội dung từ [sources]
  2. Biên soạn và tổng hợp
  3. Xuất [format] kiểu [style]
  ⏱️ Ước tính: ~{total_time}

  Bạn đồng ý với kế hoạch này không?

DEEP_RESEARCH_PLAN_FORMAT: |
  📋 Kế hoạch thực hiện:

  **Loại yêu cầu:** 🔬 Nghiên cứu chuyên sâu (Deep Research)
  **Hướng tìm kiếm:** {N} hướng nghiên cứu (sẽ tìm kiếm nhiều vòng)
  **Đầu ra:** [format + style]

  **Các hướng nghiên cứu:**
  1. {dimension_1}
  2. {dimension_2}
  ...

  **Các bước:**
  1. 🔬 Phân tách yêu cầu thành {N} hướng nghiên cứu
  2. 🔍 Vòng 1: Tìm kiếm rộng ({N} queries)
  3. 📊 Phân tích gaps và tìm kiếm bổ sung (2-3 vòng)
  4. 📝 Biên soạn và tổng hợp kết quả
  5. 📄 Xuất {format} kiểu {style}
  ⏱️ Ước tính: ~{total_time} (nghiên cứu sâu cần thêm thời gian)

  Bạn đồng ý với kế hoạch này không?

ROUTING:
  single_output:    thu-thap → bien-soan → tao-<format>
  translation_only: thu-thap → bien-soan (translation mode)
  chained_output:   thu-thap → bien-soan → tao-excel → tao-hinh → tao-slide
  search_and_out:   thu-thap (web search) → bien-soan → tao-<format>
  design_output:    thu-thap → bien-soan → thiet-ke (poster/cover/certificate/banner)
  design_chained:   thu-thap → bien-soan → thiet-ke (cover) + tao-<format> (content)
```

After user approves plan, initialize session state:
```bash
python3 scripts/save_state.py init \
  --request "<original user request>" \
  --plan '{"input_sources":[...],"processing_type":"...","output_format":"...","style":"..."}'
```

---

## Step 4: Execute Sub-Skills (with Auto Quality Review Loop)

Show progress before and after each step (format: see `references/pipeline-ux.md`).
For chained outputs and intermediate files, see `references/output-chaining.md`.

**CRITICAL: Every step now has an automatic quality review.** After each sub-skill completes,
the orchestrator reviews the output against quality criteria. If quality is insufficient, the
step is re-executed with specific improvement instructions. Maximum 2 retries per step —
if quality is still poor after 2 retries, proceed with a warning to the user.

### Auto Quality Review Protocol

```yaml
QUALITY_REVIEW_LOOP:
  after_each_step:
    1. Sub-skill produces output
    2. Orchestrator reviews output against QUALITY_CRITERIA for that step
    3. IF passes → proceed to next step
    4. IF fails → generate IMPROVEMENT_INSTRUCTIONS, re-execute step
    5. Maximum 2 retries per step
    6. After max retries, proceed with warning: "⚠️ Chất lượng bước {step} chưa
       đạt mức tối ưu. Tiếp tục với kết quả hiện tại — bạn có thể yêu cầu
       chỉnh sửa sau."

  REVIEW_MINDSET: |
    Review like a demanding expert reader, not a lenient validator. Ask:
    - Would I be proud to submit this to my boss?
    - Does this teach me something I didn't already know?
    - Are the claims backed by specific evidence, or are they vague platitudes?
    - Would a competing tool produce better output from the same inputs?
```

---

### 4.1: thu-thap (with quality gate)

**Execute:**
- Input: sources from user request + expanded dimensions from Step 1.5
- **If research_depth = deep**: pass this flag so thu-thap uses the Deep Research Protocol
  (query decomposition → multi-round search → gap analysis → targeted deep dives).
  Thu-thap will return content organized by research dimensions with coverage assessment.
- **If research_depth = standard**: single-query search as usual
- Output: combined Markdown text (with dimension headers if deep research)
- Report: "✅ Thu thập hoàn tất — {N} nguồn, {total_chars} ký tự"
- Save state: `python3 scripts/save_state.py update --step thu-thap`

**Quality Gate — THU-THAP:**
```yaml
THU_THAP_QUALITY_CRITERIA:
  volume_check:
    # Is there enough raw material to produce rich output?
    minimum_chars: 5000  # For standard requests
    minimum_chars_deep: 15000  # For deep research requests
    fail_action: "Thu thập chưa đủ dữ liệu. Tìm kiếm bổ sung với queries mở rộng."

  coverage_check:
    # Do the collected sources cover ALL dimensions from Step 1.5?
    method: Check each expanded dimension from analysis against collected content
    fail_if: Any major dimension has < 500 chars of relevant content
    fail_action: "Thiếu dữ liệu về {missing_dimensions}. Tìm kiếm bổ sung."

  diversity_check:
    # Are sources diverse enough? (not all from one website)
    minimum_unique_sources: 3  # For web search requests
    fail_action: "Nguồn dữ liệu quá tập trung. Tìm thêm từ nguồn khác."

  specificity_check:
    # Does content contain specific data (numbers, names, dates)?
    method: Scan for numeric data, proper nouns, dates in collected content
    fail_if: Content is mostly generic descriptions without specifics
    fail_action: "Nội dung thu thập quá chung chung, thiếu số liệu cụ thể. Tìm nguồn có data."
```

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

**Quality Gate — BIEN-SOAN (MOST CRITICAL):**
```yaml
BIEN_SOAN_QUALITY_CRITERIA:
  depth_check:
    # Is the content genuinely substantive?
    method: Read through the synthesized output and evaluate
    fail_if_any:
      - Average section length < 300 words (comprehensive) or < 200 words (standard)
      - More than 30% of sentences are generic (no specific data/examples)
      - Sections that just restate source content without analysis
      - Missing analytical paragraphs (what the facts mean, implications)
    fail_action: |
      "Nội dung biên soạn chưa đủ sâu. Cần bổ sung:
      - Thêm số liệu cụ thể và ví dụ cho các phần: {weak_sections}
      - Thêm phân tích (implications, trends) cho: {sections_without_analysis}
      - Mở rộng các phần quá ngắn: {short_sections}"

  specificity_check:
    # Does output contain concrete, verifiable information?
    method: Count specific data points (numbers, names, dates, examples, case studies)
    minimum_per_section: 3  # At least 3 specific data points per major section
    fail_action: "Nội dung quá chung chung. Cần thêm số liệu cụ thể, ví dụ, case study."

  structure_check:
    # Is the document well-organized?
    fail_if_any:
      - No H2/H3 hierarchy (flat structure)
      - Sections longer than 2000 words without sub-headings
      - No comparison tables where comparison data exists
      - No key takeaways at end of major sections
    fail_action: "Cấu trúc cần cải thiện: {specific_structural_issues}"

  analytical_depth_check:
    # Does the content go beyond facts to provide genuine insights?
    method: Check for analysis paragraphs, implications, trend identification, recommendations
    fail_if: More than half of sections are purely factual with no analysis
    fail_action: "Thiếu phân tích chuyên sâu. Mỗi phần cần có đoạn phân tích: xu hướng,
    ý nghĩa, khuyến nghị — không chỉ liệt kê sự kiện."
```

### 4.4: tao-\<format\> (with quality gate)

**Execute:**
- Mapping: word → tao-word | excel → tao-excel | slides → tao-slide | pdf → tao-pdf | html → tao-html
- Input: synthesized content from bien-soan
- Output: final file
- Report: "✅ Xuất file hoàn tất — {path} ({size})"
- Save state: `python3 scripts/save_state.py update --step tao-<format> --output-file "<path>"`

**Quality Gate — OUTPUT:**
```yaml
OUTPUT_QUALITY_CRITERIA:
  completeness_check:
    # Did the output skill include ALL sections from bien-soan?
    method: Compare section count in input vs output
    fail_if: Output is missing sections or has significantly truncated content
    fail_action: "File đầu ra thiếu nội dung. Kiểm tra lại các phần: {missing_sections}"

  formatting_check:
    # Is the formatting professional?
    fail_if_any:
      - Tables with broken layouts
      - Missing headings or inconsistent hierarchy
      - Images overflowing margins
      - Empty pages or sections
    fail_action: "Lỗi format: {specific_issues}. Tạo lại file."

  size_sanity_check:
    # Is file size reasonable for the content volume?
    # A 10-page report shouldn't be 2KB (probably empty)
    minimum_size_kb:
      docx: 15
      pptx: 50
      pdf: 20
      html: 5
    fail_action: "File quá nhỏ — có thể thiếu nội dung. Kiểm tra lại."
```

### 4.5: tao-hinh (conditional — if charts requested OR output is slides with data)
- Report: "✅ Tạo {N} biểu đồ hoàn tất"
- Save state: `python3 scripts/save_state.py update --step tao-hinh --output-file "<chart_path>"`

### 4.6: thiet-ke (conditional — if visual design requested: poster, cover, certificate, etc.)
- Input: content from bien-soan (titles, key phrases) + user design intent
- Output: PNG or PDF visual composition
- Route here instead of tao-hinh when the user wants a **designed composition** with
  typography and layout (poster, cover page, certificate, invitation, banner, infographic)
  rather than a data chart or AI-generated image
- Report: "✅ Thiết kế hoàn tất — {path} ({size})"
- Save state: `python3 scripts/save_state.py update --step thiet-ke --output-file "<path>"`

---

## Error Recovery

Pipeline steps can fail (network timeout in thu-thap, missing font in tao-pdf, etc.).
Without recovery, the entire pipeline stops and the user loses all progress. These rules
ensure graceful degradation:

1. **Retry once** — if a sub-skill fails, retry the same step once. Transient errors (network,
   file locks) often resolve on retry.
2. **Partial delivery** — if retry also fails, save whatever was completed so far. For example,
   if thu-thap succeeded but bien-soan fails, offer the raw collected content to the user:
   "⚠️ Biên soạn gặp lỗi. Tôi đã lưu nội dung thu thập tại tmp/collected_content.md — bạn muốn thử lại hay dùng nội dung thô?"
3. **Skip non-critical steps** — tao-hinh (charts) is often optional. If it fails, deliver
   the main document without charts and note what's missing.
4. **Save state before each step** — this way, if the pipeline crashes mid-way, the user can
   resume from the last completed step via session resume (Step 0).
5. **Report clearly** — on any failure, tell the user what step failed, what error occurred,
   and what options they have (retry / skip / manual fix).

When called from pipeline, sub-skills skip their own pre-flight checks (tong-hop already ran
`check_deps.py` in Step 2). This avoids redundant checks that slow down execution.

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

**Example 1:**
Input: "Tổng hợp 3 file PDF trong thư mục input/ thành báo cáo Word kiểu corporate"
Flow: Request Analysis → Expand (xác nhận scope) → thu-thap (đọc 3 PDF + quality check) → bien-soan (comprehensive synthesis + self-review) → tao-word (thin content guard → corporate .docx)
Output: output/bao-cao.docx (20 trang, 55 KB — comprehensive default)

**Example 2:**
Input: "Search Google về AI trends 2026, rồi làm slide thuyết trình dark-modern"
Flow: Request Analysis → Expand 5 dimensions (trends, players, market, risks, predictions) → confirm → thu-thap (deep search 5 queries + gap analysis + supplementary) → bien-soan (comprehensive + self-review loop) → tao-slide (thin content guard → dark-gradient .pptx)
Output: output/ai-trends-2026.pptx (22 slides — rich content from expanded research)

**Example 3:**
Input: "Đọc file Excel sales_data.xlsx, tạo biểu đồ bar chart rồi nhúng vào Word report"
Flow: Request Analysis → thu-thap (đọc xlsx) → bien-soan → tao-hinh (bar chart PNG) → tao-word (embed chart)
Output: 2 files output — comprehensive report with embedded charts

---

## What This Skill Does NOT Do

- Does NOT generate content itself — delegates to sub-skills
- Does NOT install dependencies — redirects to /cai-dat
- Does NOT process files directly — uses thu-thap
- Does NOT skip the execution plan — always shows plan first
