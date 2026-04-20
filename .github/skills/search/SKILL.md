---
name: search
description: |
  Search the internet for information, discover platforms, and collect structured data.
  Web search via vscode-websearchforcopilot_webSearch. 3-tier URL fetching for results:
  fetch_webpage → httpx → Playwright stealth mode (for bot-protected sites).
  Three modes: standard search (single topic), deep research (multi-dimension exhaustive),
  and data collection (structured items with direct URLs from specific platforms).
  Auto-reviews search quality and expands queries if content is insufficient.
  Always use this skill when the user wants to find information online, research a topic,
  or collect structured data from platforms — "tìm kiếm về X", "search Google", "tìm hiểu",
  "danh sách việc làm", "so sánh các nền tảng", or when the pipeline needs web content.
  Do NOT use for reading local files or fetching explicit user-provided URLs → use gather.
argument-hint: "[search query or topic]"
version: 1.1
compatibility:
  requires:
    - Python >= 3.10
    - httpx, beautifulsoup4 (URL fallback)
    - playwright (bot-protected URL fallback)
  tools:
    - run_in_terminal
    - fetch_webpage (fetching search result URLs)
    - vscode-websearchforcopilot_webSearch (primary search, probed for availability)
---

# Tìm Kiếm — Internet Search & Discovery Skill

**References:** `references/tool-availability-probe.md` | `references/playwright-search-fallback.md` | `references/web-search-enrichment.md` | `references/deep-research.md` | `references/playwright-stealth.md` | `references/data-collection.md` | `references/dom-exploration.md` | `references/adaptive-flow.md`

**Governance:** Read and follow `.github/RULE.md` — it overrides all instructions below.

This skill searches the internet, discovers platforms, and collects structured data.
It returns clean Markdown text with source attribution.

**Quality loop (RULE-2):** After each search execution, self-review runs automatically. If results
are insufficient, pivots through strategies (max 3 pivots per RULE-2):
1. Different query formulation (rephrase, add year, switch language)
2. Different source domain (switch to alternative platform)
3. Broaden/narrow scope, switch to deep research mode

**Core principle:** Never rely solely on training knowledge for time-sensitive or region-specific
information. Always search at runtime to discover what currently exists, then combine runtime
findings with training knowledge for best coverage.

All responses to the user are in Vietnamese.

---

## Step 1: Choose Search Mode

```yaml
standard:
  when: Single topic, quick question, or synthesize needs web context
  flow: Steps 2 → 5

deep_research:
  when: >
    Multiple dimensions, temporal range, exhaustive coverage, comparison/classification,
    or synthesize passes research_depth: deep
  flow: Deep Research Protocol (below)

data_collection:
  when: >
    Structured list of items with specific fields (jobs, products, companies, reviews).
    synthesize passes mode: data_collection.
    Must return individual item detail URLs — listing/search page URLs are never acceptable.
  flow: Source Intelligence Protocol → Data Collection Protocol (below)
```

---

## Step 2: Construct Queries

1. Analyze the user request to identify key search dimensions
2. Generate 1–3 targeted queries per dimension
3. Use English queries for technical topics (better index coverage)
4. Include year/date qualifiers for time-sensitive topics
5. Report: "🔍 Tìm kiếm: {query_count} hướng tìm kiếm"

---

## Step 2.5: Tool Availability Probe (Hard Gate Before Step 3)

Before invoking the primary search tool, run the **availability probe** documented in
`references/tool-availability-probe.md`. The probe is a Copilot-level decision
procedure (not a Python script) that returns one of two verdicts:

- `AVAILABLE` → primary tool is safe to invoke; proceed to Step 3 unchanged.
- `UNAVAILABLE` → primary tool MUST be skipped; route to the **fallback tier** (see
  contract below). NO Tavily/auth/configuration text is ever shown to the user.

**Probe summary:**

1. If a session-scoped `primary_unavailable` flag is already set → return UNAVAILABLE.
2. If the user has previously declined a Tavily auth prompt this session, or any
   prior search call surfaced a Tavily/auth/config error → set the flag, return
   UNAVAILABLE.
3. Otherwise, attempt `vscode-websearchforcopilot_webSearch`. If it returns results
   without surfacing auth/config UI → cache AVAILABLE. If it surfaces an auth popup,
   missing-key error, extension-absent error, or any exception → silently set the
   `primary_unavailable` flag, append a single internal diagnostic line to
   `docs/runs/<branch-slug>/diagnostics/search-probe.log`, and return UNAVAILABLE.

**Fallback cascade:**

When the probe returns UNAVAILABLE, route through this cascade. NO Tavily/auth/configuration
text is ever shown to the user. The user only sees `🔍 Đang tìm kiếm...` (AC3 of US-16.1.2).

1. **Tier 2 — Playwright stealth → DuckDuckGo HTML** (US-16.1.2)
   - For each query in Step 2, run:
     ```bash
     python3 .github/skills/search/scripts/playwright_search.py "<query>" --limit 8
     ```
   - Stdout JSON shape matches the primary tool: `{"query","results":[{url,title,snippet}]}`
   - Exit `0` → use results, continue to Step 3 URL fetching unchanged
   - Exit `1` (no results) → continue to next query; if all queries empty → escalate to Tier 3
   - Exit `2` (error) → log diagnostic, treat that query as no results
   - Full contract: `references/playwright-search-fallback.md`

2. **Tier 3 — HTTP zero-auth → DuckDuckGo HTML** (US-16.1.3)
   - For each query that Tier 2 returned empty (or when Playwright itself is unavailable):
     ```bash
     python3 .github/skills/search/scripts/http_search.py "<query>" --limit 8
     ```
   - Stdout JSON shape matches the primary tool: `{"query","results":[{url,title,snippet}]}`
   - Exit `0` → use results, continue to Step 3 URL fetching unchanged
   - Exit `1` (no results) → continue to next query
   - Exit `2` (error) → log diagnostic, treat that query as no results
   - Uses only `httpx` + `beautifulsoup4` (already in `requirements.txt`); no API
     key, no headless browser, no auth UI. Safe for restricted CI environments.
   - If ALL queries return empty across all three tiers:
     - Log a single diagnostic note to `docs/runs/<branch-slug>/diagnostics/search-probe.log`.
     - Skip Step 3 entirely.
     - Emit a single friendly Vietnamese message:
       `"Không tìm thấy kết quả tìm kiếm cho yêu cầu này."`
     - Continue the synthesize pipeline with empty search results.
   - Full contract: `references/http-search-fallback.md`

**Default:** If no unavailability signal exists, the probe returns AVAILABLE. The
goal is to avoid regressing fully-configured installations.

Full algorithm, rationale, and rollback notes: see
`references/tool-availability-probe.md`.

---

## Step 3: Execute Search & Fetch

*(Skip this step if Step 2.5 returned UNAVAILABLE.)*

For each query:
1. Run `vscode-websearchforcopilot_webSearch` with the query
2. Select 2–3 most relevant result URLs (prefer authoritative sources)
3. Fetch each URL using 3-tier fallback:
   - **fetch_webpage** (default) → if content ≥ 50 chars: done
   - **httpx + BeautifulSoup** → if Tier 1 fails
   - **Playwright stealth** → if bot-detection signals (403, Cloudflare, empty JS content)
4. After each fetch: read first 200–500 chars. Reject error pages, login walls, empty stubs.
5. Tag content with source URL and dimension

---

## Step 4: Quality Review & Auto-Expansion

Check gathered content:
- **Volume**: ≥5,000 chars total (standard) / ≥15,000 (deep research)
- **Specificity**: contains numbers, named entities, dates — not just generic descriptions
- **Coverage**: all requested dimensions have ≥500 chars of relevant content
- **Diversity**: ≥3 unique source domains

If any check fails: generate 2–3 targeted supplementary queries, fetch, re-check.
Max 2 supplementary rounds. If still insufficient, proceed with an honest coverage report.

---

## Step 5: Combine & Return

Structure each source:
```
## Nguồn: {source_name}
> {url} | {char_count} ký tự

{content}

---
```

Final summary: "📋 Tìm kiếm hoàn tất: {N} nguồn / {total_chars} ký tự / {quality_assessment}"

---

## Source Intelligence Protocol

**Purpose:** Discover which platforms are currently active and accessible for a target domain
and region. Run before data collection whenever sources are not universally known.

**When to run (all three must be true):**
1. Mode is `data_collection`
2. Item type relies on region-specific or domain-specific platforms (job boards, review sites,
   local marketplaces, regional directories) — sources that change over time
3. No explicit source list provided by user or orchestrator

**When to skip:** User provides explicit URLs, or targets universally-known stable platforms.

### Phase 1: Discover

Search for currently active platforms for the domain + region + current year.
Use English queries. Run ≥2 queries for diversity. Parse into candidate list: `{name, url, type}`.
Exclude news/blog sites. Tag aggregators so collection extracts original-source URLs.
Target: ≥3 candidates. Report: "🔍 Tìm thấy {N} nền tảng: {list}"

### Phase 2: Test and rank

Test each candidate with 3-tier fetch. Assess: accessible? Data present? Playwright needed?
- **Primary:** accessible directly + data visible
- **Fallback:** accessible via Playwright only
- **Skip:** login wall, paywall, or no relevant data

If no viable sources: report failure with concrete next-step options.

### Phase 3: Present plan and proceed

Present as **information, not a question**. Auto-proceed to data collection immediately.
In autonomous mode: skip override window. If user sends an override before collection starts: apply it.

---

## Data Collection Protocol

**Rule:** Every collected item MUST have a `direct_url` to its own detail page.
Search/listing page URLs are never acceptable as output URLs.

### Per-source collection loop

For each source (primary first, fallback if needed):

**1. Search** — `site:{source}` queries to find item URLs. If < 3 items: explore DOM structure
(nav links, search forms, URL patterns) to find internal search paths, then retry.
See `../gather/references/data-collection.md` for details.

**2. Extract** — Fetch each item detail URL. Extract required fields. Missing → "Không rõ".
Validate URLs: must have unique ID/slug. Reject `?q=`, `?page=`, `/search?` patterns.

**3. Verify quality** — ≥3 items, >60% required fields present, all URLs are item pages.

**4. Retry on failure** (max 2 per source) — different query, different URL pattern,
Playwright escalation, detail URL extractor. Different strategy each retry.

**5. Mark and move on** — if still insufficient, mark source failed with friendly reason.
**Never stop the pipeline for one source failure.**

### After all sources

Combine items from succeeded sources. Report: "✅ Thu thập: {N} nguồn / {total} kết quả"
If zero sources succeeded: report failure clearly — do NOT fabricate.

**Adaptive fallback:** When multiple sources fail, call advisory agent for alternatives.

---

## Deep Research Protocol

Full protocol: `../gather/references/deep-research.md`.

1. **Decompose** — identify distinct information dimensions → 1–2 queries each
2. **Round 1** — broad search across all dimensions, 2–3 sources per dimension
3. **Gap analysis** — which dimensions are thin? Missing specifics? Temporal gaps?
4. **Round 2+** — targeted searches for gaps (max 3 rounds, max 15 URL fetches)
5. **Consolidate** — structured output with dimension headers + honest coverage assessment

---

## What This Skill Does NOT Do

- Does NOT read local files → gather
- Does NOT fetch user-provided explicit URLs → gather
- Does NOT synthesize or translate content → compose
- Does NOT generate output files → gen-* skills
