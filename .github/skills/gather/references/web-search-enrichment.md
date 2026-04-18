# Web Search Mode & Enrichment Callback — Full Reference

## Web Search Mode (US-2.1.1)

Auto-search Google when user describes a topic without providing specific sources.

```yaml
TRIGGER:
  - No files or URLs provided by user
  - User says "tìm kiếm về", "search for", "tìm thông tin", "tìm kiếm"
  - Pipeline (tong-hop) routes with search_needed: true
  - Hybrid: user provides some files + asks to supplement with web search
```

## Web Search Workflow

```yaml
STEPS:
  1_BUILD_QUERY:
    - Extract key topic from user request
    - Keep concise (3-8 words for best results)
    - Example: "tổng hợp về AI trong giáo dục" → query: "AI in education trends 2026"

  2_EXECUTE:
    tool: vscode-websearchforcopilot_webSearch
    params:
      query: "{constructed_search_query}"

  3_PRESENT_RESULTS:
    format: |
      🔍 Kết quả tìm kiếm cho: "{query}"
      1. **{title_1}** — {domain_1}: {snippet_1}
      2. **{title_2}** — {domain_2}: {snippet_2}
      3. **{title_3}** — {domain_3}: {snippet_3}
      Bạn muốn lấy nội dung từ nguồn nào? (Mặc định: tất cả top 3-5)
    interactive_mode: Wait for user to approve or select specific sources
    pipeline_mode: Auto-select top 3-5, skip approval

  4_FETCH_SELECTED:
    - Use URL fetch workflow for each selected URL
    - Apply same content cleaning and error handling
    - Combine with any manually provided files/URLs

  5_REPORT:
    format: |
      🔍 Tìm kiếm web hoàn tất:
      - Truy vấn: "{query}"
      - Đã lấy nội dung: {fetched_count} nguồn
```

## Hybrid Mode

```yaml
HYBRID_MODE:
  description: Combine local files + URLs + web search results
  priority:
    1: Local files (most reliable)
    2: Provided URLs (user-selected)
    3: Web search results (supplementary)
  labeling: Mark source origin in combined output as [File], [URL], [Web Search]
```

---

## Enrichment Callback (US-4.4.2)

thu-thap can be called by bien-soan during synthesis when source content is thin.

```yaml
ENRICHMENT_CALLBACK:
  trigger:
    - bien-soan detects thin content in specific sections
    - bien-soan generates search queries for those sections
    - Copilot calls thu-thap web search on behalf of bien-soan

  workflow:
    1. bien-soan passes enrichment queries (1-2 per thin section)
    2. Copilot runs vscode-websearchforcopilot_webSearch per query
    3. Copilot fetches top 2-3 URLs via fetch_webpage
    4. Content returned to bien-soan with [Web: url] attribution

  constraints:
    max_queries: 2 per section
    max_urls_per_query: 3
    max_total: 10 sources
```
