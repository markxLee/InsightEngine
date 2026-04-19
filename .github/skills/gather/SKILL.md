---
name: gather
description: |
  Gather content from any source: local files (docx/xlsx/pdf/pptx/txt), URLs, and web search.
  Uses markitdown as primary reader with format-specific fallbacks for garbled output.
  Web search via vscode-websearchforcopilot_webSearch for online research.
  3-tier URL fetching: fetch_webpage → httpx → Playwright stealth mode (for bot-protected sites).
  Auto-reviews gathered content quality: checks volume, coverage, specificity, and source diversity.
  If content is insufficient, automatically expands search queries and does additional rounds.
  Always use this skill when the user mentions any file to read, URL to fetch, or topic to search
  online — even casual requests like "đọc file này", "lấy thông tin từ trang web đó", "tìm hiểu
  về X", "search Google giúp tôi", or when a file path or URL is dropped into the chat, even
  without saying "gather". For bot-protected sites (Cloudflare, CAPTCHA walls, JS-heavy SPAs),
  automatically escalates to Playwright with anti-detection stealth mode.
argument-hint: "[file paths or URLs]"
version: 1.3
compatibility:
  requires:
    - Python >= 3.10
    - markitdown[all]
    - httpx, beautifulsoup4 (URL fallback)
    - playwright (bot-protected URL fallback)
  tools:
    - run_in_terminal
    - fetch_webpage (primary URL reader)
    - vscode-websearchforcopilot_webSearch (web search)
---

# Thu Thập — Content Gathering Skill

**References:** `references/code-patterns.md` | `references/web-search-enrichment.md` | `references/deep-research.md` | `references/playwright-stealth.md` | `references/data-collection.md`

This skill reads content from any source — local files, URLs, or web search — and returns
clean Markdown text. It runs in two contexts: standalone (user asks to read something) or as
the first step in the synthesize pipeline. The key design choice is "markitdown first, fallback
second" — markitdown handles most formats well, and format-specific readers only kick in when
markitdown produces garbled or empty output.

**Quality-driven gathering:** After collecting content, this skill auto-reviews what was gathered
against the request dimensions. If the content is too thin, lacks specifics, or doesn't cover
all requested topics, it automatically expands search queries and does additional fetch rounds
(max 2 supplementary rounds). The goal is to ensure compose receives enough raw material to
produce rich, expert-level output — not scraps that force shallow synthesis.

**Three search modes:**
- **Standard**: single-query search for simple requests (default)
- **Deep Research**: multi-round iterative search for complex research requests — decomposes
  the query into dimensions, searches broadly, analyzes gaps, then searches deeper.
  See `references/deep-research.md` for the full protocol.
- **Data Collection**: platform-specific search for structured item collection — finds individual
  items (jobs, products, courses) on specific platforms, fetches item detail pages, and extracts
  structured fields. See `references/data-collection.md` for the full protocol.

All responses to the user are in Vietnamese.

---

---

## Supported Formats

```yaml
LOCAL_FILES:
  primary_reader: markitdown
  supported: .docx, .xlsx, .pdf, .pptx, .txt, .md, .csv, .html, .jpg, .png

URLS:
  tier_1: Copilot fetch_webpage tool (fast, no overhead)
  tier_2: httpx + beautifulsoup4 (fallback for fetch_webpage failures)
  tier_3: Playwright stealth mode (for bot-protected sites — Cloudflare, CAPTCHA, JS-heavy SPAs)

BOT_PROTECTED_SITES:
  detection_signals:
    - HTTP 403/429 from tier 1 or tier 2
    - Empty/garbled content despite valid URL
    - "Just a moment", "Checking your browser", "Verify you are human"
    - Cloudflare challenge page, CAPTCHA walls
    - JavaScript-rendered content (SPA) returning empty HTML
  escalation: Automatic — if tier 1+2 fail or return < 50 chars, try Playwright
  script: scripts/playwright_fetch.py

WEB_SEARCH:
  tool: vscode-websearchforcopilot_webSearch
  trigger: No files/URLs provided OR user says "tìm kiếm về..."
  see: references/web-search-enrichment.md
```

---

## Step 1: Detect Research Depth

Before doing anything, classify the request's **research complexity**:

```yaml
COMPLEXITY_SIGNALS:
  deep_research:
    # ANY of these signals → use deep research mode
    - Multiple information dimensions: user asks for several categories of info
      ("models + benchmarks + classification + timelines")
    - Temporal range: "từ 2024 đến nay", "over the past 3 years", "trends over time"
    - Comparison/classification: "classify", "compare", "phân loại", "so sánh"
    - Exhaustive intent: "tất cả", "comprehensive", "đầy đủ", "chi tiết", "toàn bộ"
    - Data aggregation: "tổng hợp điểm benchmark", "list all", "collect all data points"
    - Multi-step reasoning: answer requires connecting info from different sources
    - Explicit: synthesize passes research_depth: deep

  standard_search:
    # Simple requests → single-query search (existing Step 3 workflow)
    - Single topic, single question
    - User asks for a quick overview, not exhaustive data
    - File reading only (no web search needed)
    - User provides specific URLs to fetch

  data_collection:
    # User wants SPECIFIC ITEMS collected with structured fields
    # This is NOT research — it's entity discovery + field extraction
    - synthesize passes mode: data_collection
    - User wants items: jobs, products, courses, apartments, companies
    - User specifies output fields: "tên, lương, URL, kinh nghiệm"
    - Needs platform-specific search, not generic Google
    - Must return individual item URLs, not search result pages

  source_discovery_needed:
    # BEFORE data collection: does the pipeline know which sources actually exist?
    # Trigger source discovery (SD-0) when ALL of the following are true:
    #   1. Mode is data_collection
    #   2. Item type requires "soft knowledge" sources (review platforms, job boards,
    #      local directories, company profiles, regional marketplaces)
    #   3. No explicit source list was provided by the user or orchestrator
    # "Soft knowledge" = sources that vary by country/domain and may have changed
    #   since model training. Contrast with "hard knowledge" sources (LinkedIn, Amazon,
    #   GitHub, YouTube) which are universally known and stable.
    examples:
      - "danh sách đánh giá công ty Việt Nam" → review platforms are soft knowledge
      - "tin tuyển dụng ở Malaysia" → job boards in Malaysia are soft knowledge
      - "nền tảng ecommerce Thái Lan" → regional marketplaces are soft knowledge
    NOT_triggered_for:
      - LinkedIn, Shopee, Amazon, GitHub — globally known, model knowledge reliable
      - User provides explicit URLs → skip discovery, go directly to DC-0

RESULT:
  deep → follow Deep Research Protocol below (replaces Steps 3-4 for web search)
  standard → follow standard Steps 1-4 as before
  data_collection → check source_discovery_needed FIRST → if yes: run SD-0 → then DC-0
  data_collection → if source_discovery NOT needed: proceed directly to DC-0
```

---

## Data Collection Protocol (when mode = data_collection)

> **Advanced examples:** `references/data-collection.md`

When synthesize passes `mode: data_collection`, the workflow changes fundamentally.
**Key principle: every item in output MUST have a direct_url to its detail page.**
A search result URL or listing page URL is NEVER acceptable as a final output URL.

### SD-0: Source Discovery (MANDATORY when source_discovery_needed = true)

Before any data collection step when soft-knowledge sources are involved, the pipeline MUST
discover currently active sources for that domain + country. **Never assume model training
knowledge is current.** Even well-known local platforms change over time — new sites launch,
old ones shut down, regional names vary.

**Trigger check (runs at start of data_collection mode):**
```yaml
TRIGGER_SD0:
  condition: |
    mode == data_collection
    AND item_type involves soft-knowledge sources
    AND no explicit source_list provided by user/orchestrator
  soft_knowledge_signals:
    - "công ty", "đánh giá công ty", "review công ty"  → company review platforms
    - "việc làm" + country (not global platform)        → regional job boards
    - "ecommerce" + non-global region                   → regional marketplaces
    - "nền tảng", "trang web", "sites" + domain+country → platform discovery
  skip_SD0_when:
    - User/orchestrator provides explicit URL list → proceed to DC-0 directly
    - Item type targets universal platforms (LinkedIn, Shopee, Amazon, GitHub, etc.)
```

**SD-0 Execution Steps:**

1. **Extract discovery context** from the user request:
   ```yaml
   domain: "<what category of platform>" # e.g., "company review", "job board", "marketplace"
   country: "<target country>"           # e.g., "Vietnam", "Malaysia", "Thailand"
   year: "<current year>"               # e.g., "2026" (always current year — freshness signal)
   ```

2. **Construct ≥2 discovery search queries** (in English for better coverage):
   ```yaml
   query_templates:
     primary:   "{domain} sites {country} {year}"     # e.g., "company review sites Vietnam 2026"
     secondary: "best {domain} platforms {country}"    # e.g., "best job boards Vietnam"
     tertiary:  "{country} {domain} website list"      # e.g., "Vietnam company review website list"
   ```
   Execute ALL queries. Use English query even if user request was in Vietnamese.

3. **Parse results into candidate source list:**
   For each result, extract:
   ```yaml
   candidate_source:
     name: "<platform display name>"    # e.g., "ITViec"
     url: "<homepage or root URL>"      # e.g., "https://itviec.com"
     source_type: "<category>"          # review_platform | job_board | directory | aggregator | news
     description: "<one-line summary>"  # From search snippet
     discovery_query: "<which query found this>"
   ```
   Deduplicate by domain. Ignore news articles or non-platform results.

4. **Minimum threshold check:**
   ```yaml
   IF len(candidate_sources) < 3:
     → Run one additional search with a broader or alternative query
     → If still < 3 after one additional round:
         Log: "⚠️ SD-0: Chỉ tìm được {N} nguồn — tiếp tục với kết quả hiện có"
         → Proceed to US-14.1.2 (classification) with available candidates
   ```

5. **Save to session state** and **report (non-technical):**
   ```yaml
   session_state:
     sd0_candidates: [<list of candidate_source objects>]
     sd0_complete: true
   ```
   Report format (jargon shield applies):
   ```
   🔍 Tìm kiếm nguồn dữ liệu cho {domain} tại {country}...
   → Đã tìm thấy {N} nền tảng/trang web phù hợp:
      • {name_1} ({url_domain_1}) — {source_type_1}
      • {name_2} ({url_domain_2}) — {source_type_2}
      • {name_3} ({url_domain_3}) — {source_type_3}
      ...
   → Đang kiểm tra từng nguồn... (see US-14.2.1)
   ```

**What SD-0 does NOT do:**
- Does NOT ask user to choose sources — fully autonomous
- Does NOT test accessibility (that's US-14.2.1 / SD-1)
- Does NOT rank sources (that's US-14.2.2 / SD-2)
- Does NOT present plan (that's US-14.3.1 / SD-3)

**Budget:** SD-0 consumes ≤3 web search calls. Counts toward overall gather budget.

→ After SD-0 completes: pass `sd0_candidates` to **SD-0.5** (classification below).

---

### SD-0.5: Source Classification (runs immediately after SD-0)

After source discovery produces a candidate list, classify each source by **data type** and
assign a preliminary **reliability tier** based on domain heuristics. Classification informs
which accessibility-test strategy to apply in SD-1 (US-14.2.1).

**Classification steps:**

1. **Classify by data type** (one of the following):
   ```yaml
   source_types:
     review_platform: "Site where users leave company/product/service reviews"
     job_board: "Site listing job openings with apply flow"
     directory: "Structured listing of companies, products, or services"
     aggregator: "Re-publishes listings from multiple sources"
     news: "Primarily publishes articles — NOT a platform (exclude from collection)"
   ```
   Assignment heuristics:
   - Domain contains "review", "rating", "đánh giá", "review" in URL/name → `review_platform`
   - Domain contains "job", "career", "việc", "tuyển" in URL/name → `job_board`
   - Domain has category navigation, filters, entity listing → `directory`
   - Domain republishes from other sources without original data → `aggregator`
   - Domain is primarily a news/blog site → `news` → **exclude from candidate list**

2. **Assign preliminary reliability tier** (Tier 1/2/3) based on heuristics:
   ```yaml
   tier_heuristics:
     Tier_1:  # Score 60+ expected — likely primary source
       - National/regional platform established ≥3 years (check domain age if possible)
       - Has dedicated mobile app (mentioned in search snippets)
       - In top 3 results for all discovery queries
       - High volume signals (">X reviews", ">X listings" in snippet)
     Tier_2:  # Score 30-59 expected — may need Playwright fallback
       - Regional niche platform
       - Appears in only 1 of 2 discovery queries
       - No strong volume signals
       - Domain age unknown
     Tier_3:  # Score <30 expected — likely to be skipped
       - Very low profile (only 1 mention total)
       - Appears to be a news site or aggregator
       - Domain not clearly related to the target type
   ```

3. **Exclude `news`-type sources** from the candidate list entirely (add to `excluded_sources`).

4. **Save classification to session state:**
   ```yaml
   session_state:
     sd0_candidates: [
       { name, url, source_type, description, discovery_query, preliminary_tier }
     ]
     sd0_excluded: [  # news/aggregator sources removed
       { name, url, reason }
     ]
     sd05_complete: true
   ```

5. **Report (non-technical, user-friendly):**
   ```
   📋 Phân loại {N} nguồn:
     Tier 1 (chính): {count} — {names}
     Tier 2 (dự phòng): {count} — {names}
     Tier 3 (xác minh thêm): {count} — {names}
     Loại bỏ (tin tức/blog): {count} — {names}
   → Đang kiểm tra khả năng truy cập từng nguồn...
   ```

**What SD-0.5 does NOT do:**
- Does NOT fetch any URLs (that's SD-1)
- Does NOT compute final scores (that's SD-2)
- Does NOT confirm with user — fully autonomous

→ After SD-0.5 completes: pass classified + tiered candidates to **SD-1** (accessibility testing).

---

### SD-1: Per-Source Accessibility Test (US-14.2.1)

After classification produces a tiered candidate list, test each source for actual accessibility
and data availability. This replaces the assumption that a discovered source is automatically
usable — bot-protection, login walls, or structural changes can make a source inaccessible.

**Test execution per candidate source:**

1. **Attempt fetch using 3-tier fallback** (same as Step 4 standard fetch):
   - Tier 1: `fetch_webpage` on homepage or main category page
   - Tier 2: httpx + BeautifulSoup if Tier 1 fails/returns < 50 chars
   - Tier 3: Playwright stealth mode if bot-detection signals detected
   
   > Tier 2 sources (preliminary Tier 2 from SD-0.5) → skip directly to Playwright

2. **Check response for accessibility signals:**
   ```yaml
   ACCESSIBILITY_CHECKS:
     status_ok:
       pass: HTTP 200 or equivalent (content received)
       fail: 403, 404, 429, empty body
     not_bot_protected:
       fail_signals:
         - "Checking your browser", "Just a moment" (Cloudflare)
         - "Please log in", "Sign in to continue" (login wall)
         - "Subscribe to read" (paywall)
         - Empty body despite valid URL
     data_present:
       pass: Response contains recognizable entity listings (jobs, reviews, companies)
       check: Look for list elements, repeated card patterns, tabular data
       fail: Only static marketing copy or homepage hero content
   ```

3. **Auto-escalate to Playwright on bot-detection** (never give up without Playwright):
   ```yaml
   AUTO_ESCALATE:
     trigger: Tier 1 or Tier 2 returns bot-detection signals OR < 50 chars
     action: Immediately try Playwright stealth mode
     script: python3 .github/skills/gather/scripts/playwright_fetch.py "{url}" --wait 3
     max_wait: 8s
   ```

4. **Log test result per source:**
   ```yaml
   test_result:
     source_name: "<name>"
     url: "<url>"
     fetch_tier_used: 1 | 2 | 3  # Which tier succeeded
     playwright_needed: true | false
     accessible: true | false
     data_present: true | false
     fail_reason: "<reason if failed>"  # e.g., "login wall", "Cloudflare block", "empty content"
   ```

5. **Save results to session state:**
   ```yaml
   session_state:
     sd1_test_results: [ { test_result objects } ]
     sd1_complete: true
   ```

6. **Report (non-technical):**
   ```
   🔍 Kiểm tra {N} nguồn dữ liệu:
     ✅ {name_1} — truy cập được, có dữ liệu
     ✅ {name_2} — truy cập được (cần browser đặc biệt), có dữ liệu
     ⚠️ {name_3} — truy cập được nhưng cần đăng nhập
     ❌ {name_4} — không truy cập được ({friendly_reason})
   → Đang tính điểm độ tin cậy...
   ```
   Jargon shield: "browser đặc biệt" instead of "Playwright", "không truy cập được" instead
   of "403 Forbidden", "cần đăng nhập" instead of "login wall/paywall"

**What SD-1 does NOT do:**
- Does NOT compute final reliability score (that's SD-2 / US-14.2.2)
- Does NOT present source plan (that's SD-3 / US-14.3.1)
- Does NOT start data collection

→ After SD-1 completes: pass `sd1_test_results` to **SD-2** (reliability scoring).

---

### SD-2: Source Reliability Scoring & Ranking (US-14.2.2)

After accessibility testing, compute a **final reliability score (0-100)** for each accessible
source and rank them. This score determines which sources are used in collection, which need
special handling (Playwright), and which to skip.

**Scoring formula (100 points total):**

```yaml
RELIABILITY_SCORE:
  accessibility_status:        # 40 points max
    accessible_no_playwright:  40   # Tier 1 fetch worked without Playwright
    accessible_with_playwright: 28  # Required Playwright but accessible
    login_wall_no_account: 0        # Inaccessible — exclude
    failed_all_tiers: 0             # Inaccessible — exclude

  data_completeness_sample:    # 40 points max
    # Based on data seen during SD-1 fetch — can we observe entity listings?
    rich_structured_data: 40       # Clear listings with multiple fields (title, company, etc.)
    basic_structured_data: 24      # Some structured data but sparse fields
    unstructured_content: 12       # Readable text but no clear item listings
    no_data_visible: 0             # No relevant data detected — exclude

  preliminary_tier_bonus:      # 20 points max
    Tier_1_preliminary: 20     # Was marked Tier 1 in SD-0.5
    Tier_2_preliminary: 10     # Was marked Tier 2 in SD-0.5
    Tier_3_preliminary: 0      # Was marked Tier 3 in SD-0.5
```

**Tier assignment from final score:**
```yaml
TIER_FROM_SCORE:
  Tier_1_final:  score >= 60   # Primary source — direct collection
  Tier_2_final:  30 <= score < 60  # Fallback source — Playwright collection
  Tier_3_final:  score < 30    # Skip unless NO Tier 1 or 2 available
```

**Fallback rule (no Tier 1 or 2 sources):**
```yaml
IF count(Tier_1_final) + count(Tier_2_final) == 0:
  → Check if any Tier 3 sources have score > 0
  → If yes: promote best Tier 3 to Tier 2, log: "⚠️ Chỉ có nguồn Tier 3 — thử với dữ liệu hạn chế"
  → If all score == 0: EXIT collection for this domain, report failure to SD-3
```

**Save ranked list to session state:**
```yaml
session_state:
  sd2_ranked_sources: [  # Sorted by score DESC
    {
      name, url, source_type,
      final_score: 0-100,
      final_tier: 1|2|3,
      playwright_needed: true|false,
      included: true|false,  # false if score == 0
      score_breakdown: { accessibility: N, data: M, tier_bonus: K }
    }
  ]
  sd2_collection_viable: true|false  # false if no Tier 1 or 2
  sd2_complete: true
```

**Report (non-technical):**
```
📊 Đánh giá độ tin cậy {N} nguồn:
  Tier 1 (ưu tiên cao): {count} nguồn
    • {name_1} — điểm {score_1}/100
    • {name_2} — điểm {score_2}/100
  Tier 2 (dự phòng): {count} nguồn
    • {name_3} — điểm {score_3}/100
  Bỏ qua (điểm thấp/không truy cập): {count} nguồn
→ Chuẩn bị kế hoạch thu thập dữ liệu...
```

**What SD-2 does NOT do:**
- Does NOT present plan to user (that's SD-3 / US-14.3.1)
- Does NOT start data collection

→ After SD-2 completes: pass `sd2_ranked_sources` to **SD-3** (verified source plan).

---

### SD-3: Verified Source Plan Output (US-14.3.1)

After scoring and ranking sources, present the **verified source plan** to the user as
factual INFORMATION — not a question. The user should see what was found, understand the
plan, and have the option to override if desired. The pipeline then **auto-proceeds** to
data collection without waiting for explicit user confirmation.

**Key design principle:** This is a status update, not a decision request. The pipeline
has already done the work (discovery + testing + scoring). The user is informed, not blocked.

**SD-3 Execution:**

1. **Check viability** from SD-2 results:
   ```yaml
   IF sd2_collection_viable == false:
     → Present failure message (see Failure Format below)
     → STOP collection, return empty result to synthesize
     → Do NOT proceed to data collection
   ```

2. **Format and present the verified source plan (auto-proceed):**

   **Success format (Tier 1 or 2 sources available):**
   ```
   📋 Kế hoạch thu thập dữ liệu cho {domain} tại {country}:
   
   ✅ Nguồn chính (sẽ dùng trước):
     • {name_1} ({domain_1}) — {source_type}
     • {name_2} ({domain_2}) — {source_type}
   
   ⚠️ Nguồn dự phòng (dùng nếu nguồn chính không đủ):
     • {name_3} ({domain_3}) — cần trình duyệt đặc biệt
   
   ❌ Đã bỏ qua ({skip_count} nguồn):
     • {name_4} — {friendly_reason}
   
   → Bắt đầu thu thập từ {total_active} nguồn...
   ```

   **Failure format (no viable sources):**
   ```
   ❌ Không tìm được nguồn dữ liệu phù hợp cho {domain} tại {country}.
   
   Đã kiểm tra {total_tested} nguồn — tất cả không truy cập được hoặc không có dữ liệu.
   
   Bạn có thể:
   • Cung cấp URL trực tiếp của nền tảng bạn muốn dùng
   • Thay đổi phạm vi tìm kiếm (ví dụ: dùng nền tảng quốc tế như LinkedIn, Glassdoor)
   ```

3. **Handle user override (if user responds before pipeline proceeds):**
   ```yaml
   IF user provides feedback within a few seconds of the plan display:
     - "thêm {site}" → add site to SD-1 candidates and re-test it, then re-run SD-3
     - "bỏ {site}" → exclude that source from plan
     - "dùng {site} thôi" → restrict to that source only
     - No response → auto-proceed immediately after presenting the plan
   ```

4. **Save plan to session state and proceed to data collection:**
   ```yaml
   session_state:
     sd3_source_plan:
       tier1_sources: [{ name, url, source_type }]
       tier2_sources: [{ name, url, source_type, playwright_needed: true }]
       viable: true | false
     sd3_complete: true
   ```

5. **Proceed immediately to SD-4 / DC-0 data collection** using `sd3_source_plan.tier1_sources`
   as the verified source list (replaces model-assumed sources in DC-0).

**Jargon shield rules for this section:**
- "trình duyệt đặc biệt" not "Playwright"
- "không truy cập được" not "HTTP 403 / blocked"
- "nguồn dự phòng" not "Tier 2"
- "nguồn chính" not "Tier 1"

**What SD-3 does NOT do:**
- Does NOT ask "which sources do you want to use?" (that's the old broken behavior)
- Does NOT wait indefinitely for user response — auto-proceeds
- Does NOT start data collection (that's SD-4 / DC-0)

→ After SD-3: auto-proceed to **DC-0** (per-step search planning) with verified source list.

> **Note on SD-4 (verify-retry loop):** Once data collection begins (DC-0 → DC-7), the SD-4
> verify-retry loop wraps EACH source's collection. See **SD-4** section below for the full
> per-source retry protocol that runs during data collection.

---

### DC-0: Per-Step Search Planning (MANDATORY for complex data collection)

Before any search step, call the **strategist agent** to generate a specialized search sub-flow
tailored to the item type and target sources. This replaces flat "search Google → get results"
for complex data-collection requests (sales leads, job listings, products, company profiles).

> **Note:** If SD-0 ran (source_discovery_needed = true), the `sd0_candidates` list from SD-0
> replaces the "potential_sources" field below — use discovered sources, not model assumptions.

**When to trigger DC-0:**
- User wants specific items: jobs, products, leads, companies, listings, candidates
- Item count ≥ 5 AND specific output fields are requested
- synthesize passes `mode: data_collection`

**Budget:** ≤1 strategist call per search step, max 2 per gather execution.
These calls count toward the orchestrator's total strategist budget (max 5/pipeline).
If budget exhausted → skip DC-0, proceed directly to DC-1 using best-effort queries.

**Call strategist with this structured context:**
```yaml
strategist_call:
  task: generate_search_sub_flow
  context:
    item_type: "<what user wants: jobs|leads|products|courses|companies>"
    potential_sources: ["<platform_1>", "<platform_2>", ...]  # Known relevant platforms
    desired_quantity: <N>
    required_fields: ["<field_1>", "<field_2>", ...]
    user_request_summary: "<one-sentence description>"
    filters: { location: "...", level: "...", salary: "..." }  # If specified
```

**Expected sub-flow output from strategist (minimum 4 ordered steps):**
1. **source-plan** — Rank target platforms by relevance; identify primary and fallback sources
2. **site-search** — Construct `site:{source}.com` queries for each platform; capture item URLs
3. **dom-explore** — If site-search returns thin results (< 3 items), fetch source homepage,
   extract DOM structure (nav links, search inputs, URL patterns) to find internal search paths
   *(see `references/dom-exploration.md` for implementation; requires US-11.2.1+)*
4. **internal-search** — Use the source platform's own search tool (discovered via dom-explore
   or known URL patterns) to perform a more targeted query inside the platform

Execute each step in sequence. Each step's output feeds into the next.
If a step fails after 1 retry → continue to the next step with available data.
If the overall sub-flow fails after 2 full attempts → trigger DC-6 (Adaptive Flow Advisor).

**Budget tracking (session state):**
```yaml
session_state:
  strategist_calls_used: 0   # Increment after each DC-0 call
  strategist_calls_max: 3    # Per pipeline run — HARD STOP
```

Report after DC-0:
```
🗺️ Search sub-flow generated (strategist call {N}/3):
  1. source-plan: {platform list}
  2. site-search: {query templates}
  3. dom-explore: {trigger condition}
  4. internal-search: {search endpoint or approach}
Đang thực hiện sub-flow...
```

### DC-1: Platform-Specific Search (MANDATORY — DO NOT USE GENERIC GOOGLE)

⚠️ **Advanced examples: `references/data-collection.md`**

**Generic Google returns overview articles, NOT item pages. You MUST use site-specific search:**
- Primary: `site:itviec.com fresher javascript HCM 2026` (via web search tool)
- Supplementary: fetch platform search URL directly

**URL pattern — listing vs item page (critical distinction):**

| Platform | Listing (Phase 1 only) | Item page (required) |
|----------|----------------------|---------------------|
| ITViec | itviec.com/it-jobs?query=... | itviec.com/it-jobs/title-at-company-123 |
| TopCV | topcv.vn/tim-viec-lam-... | topcv.vn/viec-lam/title-123456 |
| LinkedIn | linkedin.com/jobs/search/... | linkedin.com/jobs/view/1234567 |
| VietnamWorks | vietnamworks.com/tim-viec/... | vietnamworks.com/viec-lam/title-123 |
| Shopee | shopee.vn/search?keyword=... | shopee.vn/product-name-i.123.456 |

Steps: construct `site:{platform}` search → collect item URLs → deduplicate.

### DC-2: Two-Phase Fetch — Discover URLs, Then Extract Fields

**Phase 1:** Discover item URLs from search results/listing pages.
**Phase 2:** Fetch each item detail page → extract fields:

| Field | Look for |
|-------|----------|
| job_title | First \<h1\>, page title |
| company | "at {company}", employer section |
| salary | "Lương:", numbers + "triệu" \| "Thương lượng" |
| experience | "Kinh nghiệm:", normalize to "< 1 năm" etc. |
| skills | "Yêu cầu:", tech lists → comma-separated |
| location | "Địa điểm:", city or "Remote" |
| direct_url | THE URL FETCHED (item page) — NEVER search/listing |

Validate URL is item page (has ID/slug, not ?q= or /search?). If field missing → "Không rõ".

**⚠️ DC-2 Inline/Popup Detection Rule (MANDATORY):**

Some sources display item details inline (expandable card, popup, JS-rendered modal)
rather than navigating to a separate detail page. These sources will show listing URLs
for every item — which are NEVER acceptable as final output URLs.

**Detection signals:**
- All anchor tags in results point back to the listing page (same URL + hash `#item-id`)
- Items use `data-id` attributes instead of `href` links
- Clicking an item triggers a modal/popup rather than page navigation
- All result URLs match `?q=` or `#results` pattern

**When inline/popup source detected:**
```bash
# Extract canonical URLs using detail_url_extractor.py
python3 .github/skills/gather/scripts/detail_url_extractor.py \
  "{listing_url}" \
  --item-selector "{css_selector_for_item_cards}" \
  --limit 20

# For JS-rendered items requiring click-to-navigate
python3 .github/skills/gather/scripts/detail_url_extractor.py \
  "{listing_url}" \
  --click-and-capture \
  --item-selector ".job-card, .item-card" \
  --limit 10
```

The extractor:
1. Tries `<link rel="canonical">`, `og:url`, `data-url` attributes from each item's HTML
2. Falls back to clicking the item and capturing URL after navigation (Playwright)
3. **Rejects** any URL matching listing-page patterns (`?q=`, `?page=`, `#results`, `/search?`)
4. Logs rejected URLs for traceability

**Hard rule — enforce before adding any item to output:**
```yaml
URL_VALIDATION:
  FORBIDDEN_PATTERNS:
    - URL contains "?page=", "?q=", "?query=", "#results", "#search"
    - URL matches listing page format (/jobs?, /search?, /browse?)
    - URL is identical to the search/listing page URL
  REQUIRED:
    - URL has a unique ID or slug: /jobs/title-at-company-12345
    - URL is fetchable and returns item-specific content
  ON_VALIDATION_FAIL:
    - Log: "⚠️ Rejected listing URL: {url} — not an item detail page"
    - Run detail_url_extractor.py to find canonical
    - If canonical not found → mark item as "URL not available", do NOT use listing URL
```

### DC-2.5: DOM Exploration (triggered when DC-1 returns thin results)

If after running DC-1 (and the site-search step from DC-0's sub-flow) the result is
**fewer than 3 quality item URLs**, automatically trigger DOM exploration:

```yaml
THIN_RESULT_THRESHOLD: 3  # Item URLs below this count → trigger DOM exploration

TRIGGER_CONDITION:
  - DC-1 search returned < 3 valid item URLs for this source, OR
  - All results are listing/search pages (no item-page URLs), OR
  - Site returned only homepage or generic pages
```

**DOM Exploration Steps:**

1. **Fetch source homepage** (or known category page) using standard 3-tier fallback:
   ```bash
   python3 .github/skills/gather/scripts/dom_explorer.py "{source_url}" --extract nav,search,links
   ```
   Use `--use-playwright` if Tier 1+2 return empty content.

2. **Extract structure** — the script returns JSON with:
   - `nav_links`: Category/section links on the site
   - `search_forms`: Form action URL + input field names
   - `url_patterns`: Item URL format (e.g., `/jobs/{SLUG}` or `/products/{ID}`)
   - `api_hints`: API endpoint patterns found in inline JS

3. **Choose strategy based on results:**
   ```yaml
   if search_forms found:
     strategy: Construct search URL from form action + inputs
     example: "https://source.com/search?q={keyword}&type=jobs"
     
   elif nav_links found:
     strategy: Fetch the most relevant category page directly
     example: "https://source.com/it-jobs?query={keyword}"
     
   elif url_patterns found:
     strategy: Use pattern to validate/find item URLs in fetched listing
     example: Filter hrefs matching "/jobs/{SLUG}-{ID}"
     
   else:
     strategy: Skip source, move to next platform or trigger DC-6
   ```

4. **Re-run search** using the discovered strategy — feed results back to DC-2 Phase 1.

4a. **If search form found — execute internal search directly** (DC-2.5 extension):
   ```bash
   # GET-based search form (most common)
   python3 .github/skills/gather/scripts/internal_search.py \
     "{form_action_url}" --query "{keyword}" --method GET

   # POST-based search form
   python3 .github/skills/gather/scripts/internal_search.py \
     "{form_action_url}" --query "{keyword}" --method POST \
     --fields '{"type": "jobs", "location": "{city}"}'

   # For JS-rendered results (SPA search — requires Playwright)
   python3 .github/skills/gather/scripts/internal_search.py \
     "{form_action_url}" --query "{keyword}" --use-playwright
   ```
   Script extracts item URLs from search results page, returns structured JSON
   with `{url, title, snippet}` per item. Validate: item URLs must have ID/slug,
   not search/listing page patterns. If 0 items returned → fall back to DC-1 strategies.

5. **Report:**
   ```
   🔍 DOM exploration: {source_domain}
     - Nav links: {N} found
     - Search form: {found/not found} → {action_url}
     - URL pattern: {example_pattern}
     - Strategy chosen: {A/B/C}
   → Re-searching with improved query...
   ```

**Full reference:** `references/dom-exploration.md`
**Known platform patterns:** See the "Known Platform Search Patterns" table in that file.

### DC-3: Company/Entity Research (if supplementary data requested)

When user requests additional context per item (e.g., company reviews):
1. Deduplicate entities (group items by company/brand)
2. For each unique entity, search for supplementary data
3. Attach supplementary data to relevant items

### DC-4: Structured Output

Return collected items as structured data (not prose):
```markdown
## Collected Items: {entity_type}
### Item 1
- **{field_1}**: {value}
- **{field_2}**: {value}
- **direct_url**: {specific_item_url}
- **source_platform**: {platform}

### Item 2
...
```

### DC-5: Quality Check for Data Collection

Check 4 criteria: (1) URL specificity — no search/listing URLs, re-fetch if found; (2) Field completeness — >70% items have each required field; (3) Quantity — ≥50% of target; (4) Filter accuracy — items match user criteria. Fail any → re-fetch/expand.

Full spec: `references/deep-research.md`

### DC-6: Adaptive Flow Advisor (triggered after 2 failed sub-flow attempts)

When a search sub-flow for a specific source **fails 2 times** (insufficient items after
DC-0 sub-flow execution + 1 retry, or DC-2.5 DOM exploration also returns no usable
structure), call the **advisory agent** for alternative approaches before giving up.

```yaml
TRIGGER_CONDITION:
  - Sub-flow attempted: 2 times for this source/step
  - Both attempts produced: < threshold items (< 3 for that source)
  - DOM exploration also failed (DC-2.5 returned no usable structure)

BUDGET:
  advisory_calls_max: 2 per pipeline run  # HARD STOP
  # If budget exhausted → log "Advisory budget exhausted" and proceed with available items
```

**Call advisory agent with this context:**
```yaml
advisory_call:
  task: propose_alternative_search_flow
  context:
    item_type: "<what was being searched>"
    attempted_sources: ["<source_1> — {reason_failed}", "<source_2> — {reason_failed}"]
    current_results_count: <N>  # Items found so far
    target_quantity: <M>         # Original target
    gap_count: <M - N>           # Still needed
    failed_queries: ["<query_1>", "<query_2>"]
    search_approach_tried: ["site:search", "dom-exploration", "direct-fetch"]
```

**Advisory agent returns 2-3 alternatives, each with:**
```yaml
alternative:
  name: "<short name>"
  description: "<how to execute>"
  example: "<concrete example URL or query>"
  pros: ["<pro_1>"]
  cons: ["<con_1>"]
```

**After receiving alternatives:**
- Store alternatives in session state for DC-6 Step 2 (US-11.4.2) — user presentation
- If user has already selected → execute the chosen alternative immediately
- If first encounter → PAUSE and present to user (see DC-7 below)
- Budget tracking: increment `advisory_calls_used`

Report:
```
⚠️ Search sub-flow thất bại sau 2 lần thử cho {source_domain}
  Đã thử: {attempt_summary}
  Kết quả hiện tại: {N}/{M} items
→ Gọi advisory agent để đề xuất phương án thay thế...
```

### DC-7: User-Facing Flow Alternatives Presentation

After DC-6 calls the advisory agent, present alternatives to the user before retrying.  
**Reference:** `.github/skills/gather/references/adaptive-flow.md`

**Step 1 — Check session state first:**
```yaml
IF session_state["adaptive_flow"]["per_source"][source]["user_choice"] IS NOT NULL:
  → Skip presentation; use stored choice directly (do NOT ask again)
```

**Step 2 — Present numbered alternatives:**
```
⚡ Không tìm được đủ {item_type} từ {source_domain} sau 2 lần thử.

Tôi đã thử:
• Lần 1: {search_approach_1} → {result_count_1} kết quả
• Lần 2: {search_approach_2} → {result_count_2} kết quả

Advisory agent đề xuất {N} phương án thay thế:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**Phương án 1: {alternative_1.name}**
{alternative_1.description}
Ví dụ: {alternative_1.example}
✅ {alternative_1.pros[0]} | ⚠️ {alternative_1.cons[0]}

**Phương án 2: {alternative_2.name}**
{alternative_2.description}
Ví dụ: {alternative_2.example}
✅ {alternative_2.pros[0]} | ⚠️ {alternative_2.cons[0]}

**Phương án 3: Tiếp tục với {collected_count} items đã có**
Bỏ qua {source_domain}, xử lý kết quả hiện có.
✅ Không mất thêm thời gian | ⚠️ Output thiếu ~{gap_count} items
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Nhập 1, 2, hoặc 3 để chọn — hoặc mô tả hướng dẫn khác:
```

**Step 3 — Handle user response:**

| User input | Action |
|-----------|--------|
| `"1"` / `"phương án 1"` | Execute `alternative_1` from advisory result |
| `"2"` / `"phương án 2"` | Execute `alternative_2` from advisory result |
| `"3"` / `"tiếp tục"` | Accept current partial results, move on |
| Freeform text | Use as custom guidance: construct new query/approach |
| No response (context full) | Default to `alternative_1`; note: "Đã tự động chọn phương án 1" |

**Step 4 — Save choice to session state:**
```yaml
# MANDATORY — prevents repeating the same question
session_state["adaptive_flow"]["per_source"][source]["user_choice"] = user_input
session_state["adaptive_flow"]["per_source"][source]["chosen_alternative"] = resolved_alternative
```

**Step 5 — Execute chosen alternative:**
- `alternative_1` / `alternative_2`: Run as a new search sub-flow (DC-1 / DC-2 / DC-2.5)
- `alternative_3` / "tiếp tục": Mark source as `resolved: true`, proceed with items collected
- Freeform: Treat as a natural language instruction for a single additional attempt

---

### SD-4: Verify-Retry Data Collection Loop (US-14.4.1)

The SD-4 loop **wraps each source's data collection** when using verified sources from SD-3.
Instead of blindly fetching and returning whatever was collected, SD-4 checks quality after
each source fetch, and retries with adjusted strategy if quality is insufficient.

**This loop runs FOR EACH source in `sd3_source_plan.tier1_sources + tier2_sources`:**

```yaml
LOOP (per source):
  max_retries_per_source: 2  # Max retry attempts before marking source as failed
  
  attempt: 1...(1 + max_retries_per_source):
    1. FETCH data from source (using DC-1 / DC-2 approach)
    
    2. QUALITY CHECK — evaluate collected data:
       minimum_records:
         pass: ≥3 items/entities collected from this source
         fail: 0-2 items (clearly insufficient)
       field_coverage:
         pass: >50% of required fields present across items
         fail: ≤50% — fields mostly empty or "Không rõ"
       url_validity:
         pass: All direct_urls are item-page URLs (not listing/search pages)
         fail: Any URL matches forbidden patterns (?q=, /search?, listing-page format)
       
    3. IF quality_check PASS:
       → Mark source as: succeeded: true, items: [collected_items]
       → Break loop (move to next source)
       
    4. IF quality_check FAIL AND attempt < max_retries:
       → Determine retry strategy:
         if insufficient_records AND attempt == 1: retry_strategy = modified_search_query
         if insufficient_records AND attempt == 2: retry_strategy = different_url_pattern
         if playwright_needed AND not_yet_used: retry_strategy = playwright_escalation
         if bad_urls AND detail_extractor_not_tried: retry_strategy = run_detail_extractor
       → LOG: "⚠️ Nguồn {name} — kết quả không đủ ({reason}). Đang thử lại..."
       → RETRY with adjusted strategy
       
    5. IF quality_check FAIL AND attempt > max_retries:
       → Mark source as: failed: true, reason: "<why_failed>", items: []
       → LOG: "❌ Nguồn {name} — không thu thập được sau {N} lần thử ({reason})"
       → Break loop (move to next source)
```

**After all sources processed:**

```yaml
POST_LOOP:
  total_sources: <N>
  succeeded_sources: [ { name, items_count, items } ]
  failed_sources: [ { name, reason } ]
  
  IF len(succeeded_sources) == 0:
    → Report total failure with details
    → Return empty result (do NOT fabricate)
    
  ELSE:
    → Combine all items from succeeded sources
    → Present summary (non-technical, friendly):
      ```
      ✅ Thu thập hoàn tất:
        Thành công: {N} nguồn ({total_items} kết quả)
          • {name_1}: {count_1} {entity_type}
          • {name_2}: {count_2} {entity_type}
        
        ❌ Không thu thập được: {M} nguồn
          • {name_3}: {friendly_reason_3}
      
      → Tổng cộng: {total_items} {entity_type} từ {N} nguồn
      ```
    → Pass combined items to compose for synthesis
```

**SD-4 does NOT:**
- Stop the pipeline because one source failed (partial results are always acceptable)
- Ask user whether to continue after a source fails
- Fabricate data to meet quantity targets

**Budget impact:** Each retry counts as additional fetch calls. SD-4 max adds
`count(sources) * max_retries * avg_fetch_calls` to total gather budget.

---

### DR-1: Query Decomposition

1. Read the full request and identify every distinct information dimension
2. For each dimension, generate 1-2 specific search queries
3. Use English queries for technical topics (better results)
4. Include year/date qualifiers, entity names, specific terms
5. Report:
   ```
   🔬 Phân tích yêu cầu nghiên cứu:
   Tôi đã chia thành {N} hướng tìm kiếm:
   1. {dimension_1} → query: "{query_1}"
   2. {dimension_2} → query: "{query_2}"
   ...
   ```

### DR-2: Round 1 — Broad Search

1. Execute `vscode-websearchforcopilot_webSearch` for ALL dimensions
2. For each dimension, select 2-3 most relevant URLs (prefer authoritative sources)
3. Fetch via `fetch_webpage`, tag content with dimension and source
4. Report: "🔍 Vòng 1: {M} nguồn đã thu thập — đang phân tích gaps..."

### DR-3: Gap Analysis (THE CRITICAL STEP)

After Round 1, **read and analyze** what you've collected:

1. For each dimension: is the content adequate? (< 500 chars relevant content = gap)
2. Are there missing specifics? (mentions benchmarks exist but no actual numbers = gap)
3. Temporal coverage complete? (asked for 2024-2026 but only have 2024 data = gap)
4. Emerging topics? (results reveal important related info user didn't ask about)
5. Entity coverage? (found 20 models but benchmark data for only 5 = gap)

Generate follow-up queries for each gap (more specific than Round 1).

Report:
```
📊 Phân tích gaps:
- ✅ Đủ dữ liệu: {covered_dimensions}
- ⚠️ Cần bổ sung: {gap_list_with_reasons}
Đang tìm kiếm bổ sung...
```

### DR-4: Round 2+ — Targeted Deep Dives

1. Search for gaps with specific, targeted queries
2. Fewer URLs per query (1-2, targeting exactly what's missing)
3. After Round 2, do another gap analysis
4. If critical gaps remain and haven't hit limits → Round 3

**Depth limits (hard stops):**
- Maximum **3 rounds** (Round 1 broad + Round 2 targeted + Round 3 final)
- Maximum **15 total URL fetches** across all rounds
- Stop early if next round would add < 10% new content
- Report honestly if some dimensions couldn't be fully covered

### DR-5: Consolidate

Combine all content with dimension headers and coverage assessment:
```markdown
## Research Summary
### Dimensions Covered
1. {dim_1}: {coverage} — {N} sources
2. {dim_2}: {coverage} — {M} sources
### Gaps Remaining
- {honest_assessment_of_unfilled_gaps}
---
{combined_content_organized_by_dimension}
```

---

## Step 2: Identify Sources

1. Extract file paths from user request (absolute or relative)
2. Extract URLs (http:// or https://)
3. Detect if web search is needed (no specific sources given)
4. Validate: check each file exists and format is supported; validate URL format
5. Report:
   ```
   📂 Nguồn dữ liệu:
   - File: {N} file ({formats})
   - URL: {M} đường dẫn
   - Tìm kiếm web: "{query}" → {K} kết quả
   ```

---

## Step 3: Read Local Files

For each file:
1. Check file size first — skip files larger than 50 MB with a warning (large files exhaust
   context and slow processing; the user can split them or provide specific pages/sheets)
2. Try markitdown first (see `references/code-patterns.md`)
3. If output < 100 chars → use format-specific fallback reader
4. Report: "  ✅ {filename} — {char_count} ký tự ({format})"
5. On error: "  ❌ {filename} — Lỗi: {error_message}" → skip file, continue with others

---

## Step 4: Fetch URL Content (Standard Mode — 3-Tier Fallback)

For each URL, try tiers in order — escalate on failure:

### Tier 1: fetch_webpage (fastest, default)
1. Use `fetch_webpage` tool with `query: "main content"`
2. Set a 30-second mental timeout — if it hangs or returns nothing, move to Tier 2
3. If content ≥ 50 chars → success, clean and use it

### Tier 2: httpx + BeautifulSoup (fallback)
1. If Tier 1 fails or returns < 50 chars → use httpx + BeautifulSoup (with `timeout=15`)
2. See `references/code-patterns.md` for the exact code pattern
3. If content ≥ 50 chars → success

### Tier 3: Playwright Stealth Mode (anti-bot fallback)
1. If both Tier 1 and Tier 2 fail — OR if bot-detection signals are detected (403,
   Cloudflare challenge page, empty JS-rendered content) → escalate to Playwright
2. Run the stealth fetch script:
   ```bash
   python3 .github/skills/gather/scripts/playwright_fetch.py "URL" --wait 3
   ```
3. For multiple URLs:
   ```bash
   python3 .github/skills/gather/scripts/playwright_fetch.py URL1 URL2 URL3 --output collected.md
   ```
4. The script uses comprehensive anti-detection:
   - `--disable-blink-features=AutomationControlled` (hide automation)
   - `navigator.webdriver` override → `undefined`
   - Chrome runtime + plugin array spoofing
   - Real Chrome User-Agent profile
   - CSP bypass + extra HTTP headers
5. See `references/playwright-stealth.md` for full technical details

### Common for all tiers:
- Clean content: remove nav/footer/cookie boilerplate, limit to 50,000 chars
- Report: "  ✅ {page_title} ({url_domain}) — {char_count} ký tự"
- On final failure (all 3 tiers): "  ❌ {url} — Không thể lấy nội dung (đã thử 3 phương pháp)"
- Rate limiting: pause briefly between requests to the same domain

### When to Skip Directly to Playwright
Some sites are known to block non-browser requests consistently. For these, skip Tier 1+2
and go directly to Playwright to save time:
```yaml
DIRECT_PLAYWRIGHT_SIGNALS:
  - User explicitly says "trang này chặn bot" or "cần dùng browser"
  - Domain is known bot-protected (job boards, social media, news paywalls)
  - Previous fetch from same domain failed with 403/429
  - URL pattern suggests dynamic SPA (single-page app with client-side rendering)
```

For error messages and URL error types, see `references/code-patterns.md`.
For Playwright anti-detection details, see `references/playwright-stealth.md`.
For web search workflow, see `references/web-search-enrichment.md`.

### Step 4.5: Post-Fetch Content Verification (MANDATORY)

```
╔══════════════════════════════════════════════════════════════════╗
║  🔴 "Fetched" ≠ "Useful". READ the content after each fetch.  ║
║  Do NOT accept: error pages, login walls, empty stubs, or      ║
║  search/listing pages when you need item detail pages.          ║
╚══════════════════════════════════════════════════════════════════╝
```

After fetching each URL, **READ the first 200-500 chars** and verify:
1. **Not an error page**: no "403 Forbidden", "404 Not Found", "Access Denied"
2. **Not a login/paywall**: no "Please log in", "Subscribe to continue"
3. **Not empty/boilerplate**: content has > 200 chars of actual text (not nav/footer)
4. **Correct page type**: if you need item detail, verify URL has item ID/slug (not ?q= search)
5. **Content relevance**: does the text relate to the user's query?

**If bad**: mark as failed, try next tier or alternative URL. Do NOT pass garbage to compose.

---

## Step 5: Quality Review & Auto-Expansion

Before combining results, review the gathered content quality. This step prevents the common
failure where thin research data leads to thin synthesis. Better to spend extra time gathering
now than to produce a shallow final document.

### Content Quality Assessment

```yaml
GATHERING_QUALITY_CHECK:
  volume_check:
    # Is there enough raw material for comprehensive synthesis?
    minimum_total_chars: 5000  # Standard requests
    minimum_total_chars_deep: 15000  # Deep research
    minimum_per_dimension: 1000  # Per research dimension (if applicable)
    fail_action: Expand search queries, fetch more URLs

  specificity_check:
    # Does the content contain specific, usable data?
    check_for: Numbers, statistics, named entities, dates, case studies, quotes
    fail_signal: Content is mostly generic descriptions and overviews
    fail_action: |
      Search for more specific queries:
      - Add "statistics", "data", "report", "benchmark" to search terms
      - Target data-rich sources: research papers, industry reports, official statistics

  coverage_check:
    # If dimensions were specified (by synthesize Step 1.5), are they all covered?
    method: Map collected content to each requested dimension
    fail_if: Any major dimension has < 500 chars of relevant content
    fail_action: Generate targeted queries for uncovered dimensions

  source_diversity:
    # For web search: are sources varied enough?
    minimum_unique_domains: 3  # Don't rely on a single source
    fail_action: Explicitly search for alternative perspectives and sources

AUTO_EXPANSION_PROTOCOL:
  if_quality_check_fails:
    1. Identify which criteria failed and what's missing
    2. Generate 2-3 targeted supplementary search queries
    3. Execute supplementary searches + fetch
    4. Re-check quality
    5. Maximum 2 supplementary rounds
    6. If still insufficient after 2 rounds, proceed with honest coverage report
  
  report_to_user: |
    📊 Kiểm tra chất lượng thu thập:
    - Khối lượng: {total_chars} ký tự ({pass/fail})
    - Độ cụ thể: {specificity_assessment} ({pass/fail})
    - Phủ sóng: {coverage_assessment} ({pass/fail})
    - Đa dạng nguồn: {N} nguồn từ {M} domain ({pass/fail})
    {if_supplementary: "→ Đã tìm kiếm bổ sung {K} queries"}
```

---

## Step 6: Combine & Return

1. Structure each source as:
   ```
   ## Nguồn: {source_name}
   > File: {path_or_url}
   > Kích thước: {char_count} ký tự

   {extracted_content}

   ---
   ```
2. Return combined Markdown to pipeline OR show summary to user:
   ```
   📋 Thu thập hoàn tất:
   - Tổng cộng: {total_sources} nguồn
   - Thành công: {success_count}, Lỗi: {error_count}
   - Tổng nội dung: {total_chars} ký tự (~{total_words} từ)
   - Chất lượng: {quality_assessment}
   ```

---

## CLI Script (Recommended for batch sources)

```yaml
SCRIPT: scripts/gather.py
USAGE: |
  python3 scripts/gather.py --files doc.pdf report.docx --output collected.md
  python3 scripts/gather.py --urls "https://example.com" --output collected.md
  python3 scripts/gather.py --sources sources.json --output collected.md
JSON_FORMAT: |
  {"files": ["a.pdf", "b.docx"], "urls": ["https://example.com"]}
OUTPUT: Combined Markdown file with source headers
```

Use gather.py when processing multiple files or URLs in batch. For single files, direct
markitdown or fetch_webpage is simpler. The script handles markitdown-first-fallback-second
logic, URL rate limiting, and structured output automatically.

---

## Examples

**Example 1:**
Input: "Đọc 2 file: input/report.pdf và input/data.xlsx"
Output: Combined Markdown (~5,000 ký tự) with source headers, tables preserved from Excel

**Example 2:**
Input: "Tìm kiếm về 'machine learning trends 2026' rồi lấy nội dung top 3 kết quả"
Output: Web search → fetch 3 URLs → Combined Markdown (~15,000 ký tự) with source attribution

**Example 3:**
Input: URL "https://example.com/blog/ai-report" dropped into chat
Output: Fetched page content → cleaned Markdown (~3,000 ký tự), nav/footer removed

---

## What This Skill Does NOT Do

- Does NOT synthesize or merge content — that's compose
- Does NOT translate content — that's compose
- Does NOT generate output files — that's tao-* skills
- Does NOT install dependencies — redirects to setup
