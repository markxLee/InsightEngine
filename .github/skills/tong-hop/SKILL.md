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
version: 1.2
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

**References:** `references/pipeline-ux.md` | `references/session-summary.md` | `references/output-chaining.md` | `references/auto-escalation.md` | `references/file-placement-rules.md` | `references/agent-context-schema.md` | `references/decision-maps.md`
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

   CRITICAL_DIFFERENCE:
     # Why this matters — the user's actual complaint:
     # "research" mode: searches broadly, synthesizes into prose → fine for reports
     # "data_collection" mode: must find INDIVIDUAL ITEMS with SPECIFIC URLs
     #   → NOT search result pages, NOT aggregator overview pages
     #   → Each row in output must link to a real, verifiable item page
     # "mixed" mode: data_collection FIRST, then research/analysis on collected data
   ```
7. **Extract REQUIRED_FIELDS** (for data_collection and mixed requests):
   ```yaml
   REQUIRED_FIELDS_EXTRACTION:
     # When request_type is data_collection or mixed, scan the user's prompt for
     # specific output fields they expect. This becomes a checklist for output audit.
     method: |
       Read the user's prompt and extract every mention of data they want:
       - Explicit: "tên job, lương, kinh nghiệm, URL" → fields: [name, salary, experience, url]
       - Implicit: "review công ty" → field: company_review
       - Inferred: job listing → always include: source_platform, direct_url
     
     output:
       required_fields:
         - field_name: "job_title"
           description: "Tên vị trí tuyển dụng"
           required: true
         - field_name: "direct_url"
           description: "URL trực tiếp đến trang job (KHÔNG phải search result)"
           required: true
           validation: "Must be a direct link to the job posting page, not a search/listing page"
         # ... extracted from user's prompt
     
     PASS_TO: thu-thap (for targeted extraction), bien-soan (for completeness check),
              output audit (for final validation)
   ```
8. Detect if request needs **visual design** (see routing table below):
   - Poster, cover page, certificate, invitation, banner, infographic layout → **thiet-ke**
   - Data charts (bar, line, pie, radar, scatter) → **tao-hinh** (chart mode)
   - AI-generated illustration, background, character → **tao-hinh** (image mode)
   - Keywords that signal thiet-ke: "poster", "bìa", "cover", "certificate", "bằng khen",
     "thiệp", "invitation", "banner", "infographic", "thiết kế", "design"
   - **Dual visual routing**: A single request can need BOTH thiet-ke AND tao-hinh.
     Example: "tạo báo cáo Word với bìa đẹp và biểu đồ" → thiet-ke (cover) + tao-hinh
     (charts) + tao-word (content). Detect both signals and route accordingly in Step 4.
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

**Behavior depends on REQUEST_TYPE detected in Step 1:**

#### For `research` requests — Expand analytical dimensions:

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

#### For `data_collection` or `mixed` requests — Expand collection strategy:

This is fundamentally different from research analysis. The user wants SPECIFIC ITEMS
collected, not knowledge synthesized. The analysis must focus on:

```yaml
DATA_COLLECTION_ANALYSIS:
  for_each_request:
    1. TARGET_ENTITIES: What specific items does the user want?
       - "Job listings", "apartments", "products", "courses", "companies"
       - Be precise: "fresher JavaScript jobs" not just "jobs"
    
    2. SEARCH_PLATFORMS: Where should we look for these items?
       # This is critical — generic Google search returns overview pages, NOT individual items.
       # Must identify platform-specific sources where individual items live.
       example_for_jobs:
         - ITViec.com (IT jobs Vietnam — most relevant)
         - TopCV.vn (general jobs Vietnam)
         - LinkedIn Jobs (remote + international)
         - VietnamWorks.com (established platform)
         - Glassdoor.com (reviews + jobs)
         - Indeed.com (broad reach)
       example_for_products:
         - Specific e-commerce platforms (Shopee, Tiki, Amazon)
       example_for_courses:
         - Udemy, Coursera, specific school websites
    
    3. FILTER_CRITERIA: What filters narrow the search?
       - Location: "HCM", "remote"
       - Experience: "fresher", "< 1 year"
       - Skills: "JavaScript", "Node.js", "React"
       - Salary range, company size, etc.
    
    4. REQUIRED_FIELDS: What data must be extracted per item?
       # Extract from user's prompt + add essential defaults
       user_explicit: [fields user mentioned directly]
       auto_added:
         - direct_url: "ALWAYS — link to the specific item page, never a search page"
         - source_platform: "Which platform/site this was found on"
       validation_rules:
         - direct_url must point to individual item (e.g., itviec.com/jobs/xyz NOT itviec.com/search?q=xyz)
         - Salary can be "Thương lượng" if not disclosed
    
    5. SEARCH_QUERIES: Generate platform-specific search queries
       # NOT generic Google queries — target specific platforms
       bad:  "fresher javascript developer ho chi minh"  ← returns Google search results
       good:
         - site:itviec.com fresher javascript developer ho chi minh
         - site:topCV.vn javascript fresher
         - site:linkedin.com/jobs javascript developer fresher vietnam remote
       # Also: navigate directly to platform search pages when possible
    
    6. SUPPLEMENTARY_RESEARCH: Additional context needed per item?
       - "review công ty" → need company review data from Glassdoor, ITViec reviews
       - "so sánh" → need comparison dimensions
    
    7. QUANTITY_EXPECTATION: How many items should we aim for?
       - "tất cả" → as many as feasible (20-50 for job search)
       - "top 10" → 10 items, ranked
       - No quantity specified → aim for 15-30 relevant items

  ANALYSIS_PRESENTATION_FORMAT: |
    🔍 **Phân tích yêu cầu thu thập dữ liệu:**

    **Đối tượng thu thập:** {target_entities}
    **Tiêu chí lọc:** {filter_criteria}
    
    📌 **Các nền tảng sẽ tìm kiếm:**
    1. {platform_1} — {why_relevant}
    2. {platform_2} — {why_relevant}
    ...
    
    📊 **Thông tin sẽ thu thập cho mỗi item:**
    | Field | Mô tả | Bắt buộc |
    |-------|--------|----------|
    | {field_1} | {desc} | ✅ |
    | {field_2} | {desc} | ✅ |
    | direct_url | Link trực tiếp tới job/item | ✅ |
    ...
    
    🔢 **Mục tiêu:** ~{target_quantity} items
    
    {if mixed: "📝 Sau khi thu thập, sẽ phân tích và tạo {analysis_output_format}"}
    
    👉 Bạn đồng ý với kế hoạch này không? Có muốn thêm/bớt trường dữ liệu nào?
```

### 1.5.2: Present Analysis for User Confirmation

**For `research` requests** — present expanded research dimensions:

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
  dual_visual:      thu-thap → bien-soan → thiet-ke (cover/design) + tao-hinh (charts) + tao-<format>
  data_collection:  thu-thap (platform-specific) → extract fields → tao-excel → kiem-tra (audit)
  mixed_collection: thu-thap (platform-specific) → extract → tao-excel → bien-soan (analyze) → tao-<format> → kiem-tra
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

### 4.6: thiet-ke (conditional — if visual design requested: poster, cover, certificate, etc.)
- Input: content from bien-soan (titles, key phrases) + user design intent
- Output: PNG or PDF visual composition
- Route here instead of tao-hinh when the user wants a **designed composition** with
  typography and layout (poster, cover page, certificate, invitation, banner, infographic)
  rather than a data chart or AI-generated image
- Report: "✅ Thiết kế hoàn tất — {path} ({size})"
- Save state: `python3 scripts/save_state.py update --step thiet-ke --output-file "<path>"`

### 4.7: Output Audit — kiem-tra (ALWAYS RUN)

**This step closes the #1 gap in the previous pipeline: outputs that are well-formatted
but don't actually match what the user asked for.**

After ALL output files are generated, run the audit sub-skill (kiem-tra) to verify the
output against the user's original request. Full audit criteria: `references/quality-gates.md`.

**Inputs to kiem-tra:**
- `original_request`: User's full original prompt (verbatim)
- `required_fields`: From Step 1 extraction (if data_collection/mixed)
- `expanded_analysis`: From Step 1.5 (dimensions or collection plan)
- `output_files`: Generated file paths
- `output_content`: Content that was put into the files

**Key checks:**
- Requirement coverage: every user requirement ✅/⚠️/❌
- For data_collection: URL quality (direct links, not search pages), field completeness, quantity
- Specificity: sample 5 claims — are they specific or vague?

**On failure:** Report specifics → propose remediation → re-run if approved (max 1 fix cycle).
**On pass:** Report coverage stats → proceed to final report.

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

**Example 4 (data_collection — the job search case):**
Input: "Tìm tất cả job fresher JS ở HCM, tạo Excel có tên, lương, URL job, rồi tạo slide phân tích"
Flow:
  1. Step 1: request_type = mixed (data_collection + analysis)
  2. Step 1.5: Identify platforms (ITViec, TopCV, LinkedIn), required fields (job_title, salary,
     experience, skills, location, direct_url, company_review_url), target ~20-30 items
  3. Step 4.1: thu-thap searches PLATFORM-SPECIFIC (site:itviec.com fresher javascript HCM, etc.)
     → fetches INDIVIDUAL JOB PAGES (not search result pages) → extracts structured fields
  4. Step 4.4: tao-excel with structured job data (each row = 1 job, columns = required fields)
  5. Step 4.3: bien-soan analyzes jobs → rankings, recommendations, company comparisons
  6. Step 4.4b: tao-slide with analysis content
  7. Step 4.7: kiem-tra audits — checks URLs are direct job links, fields complete, quantity met
Output: job-search.xlsx (30 jobs with direct URLs) + job-analysis.pptx (analysis & recommendations)

---

## What This Skill Does NOT Do

- Does NOT generate content itself — delegates to sub-skills
- Does NOT install dependencies — redirects to /cai-dat
- Does NOT process files directly — uses thu-thap
- Does NOT skip the execution plan — always shows plan first
