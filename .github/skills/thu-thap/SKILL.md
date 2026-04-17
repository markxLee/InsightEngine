---
name: thu-thap
description: |
  Gather content from local files, URLs, and web search results.
  Uses markitdown as primary reader with format-specific fallbacks.
  Web search via vscode-websearchforcopilot_webSearch.
  Use when user says "đọc file", "lấy nội dung từ", "read file", or "/thu-thap".
argument-hint: "[file paths or URLs]"
---

# Thu Thập — Content Gathering Skill

**References:** `references/code-patterns.md` | `references/web-search-enrichment.md`

```yaml
MODE: Interactive (reports progress) or Pipeline (called by tong-hop)
LANGUAGE: Copilot responds in Vietnamese
OUTPUT: Markdown text (passed to bien-soan or directly to user)
```

---

## Trigger Conditions

Use this skill when user:
- Says "đọc file", "lấy nội dung từ", "read file"
- Says "tìm kiếm thông tin", "fetch URL", "search web"
- Uses command `/thu-thap`
- Provides file paths or URLs for content extraction
- Pipeline (tong-hop) routes here for input gathering

---

## Supported Formats

```yaml
LOCAL_FILES:
  primary_reader: markitdown
  supported: .docx, .xlsx, .pdf, .pptx, .txt, .md, .csv, .html, .jpg, .png

URLS:
  primary: Copilot fetch_webpage tool
  secondary: httpx + beautifulsoup4 (fallback)

WEB_SEARCH:
  tool: vscode-websearchforcopilot_webSearch
  trigger: No files/URLs provided OR user says "tìm kiếm về..."
  see: references/web-search-enrichment.md
```

---

## Step 1: Identify Sources

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

## Step 2: Read Local Files

For each file:
1. Try markitdown first (see `references/code-patterns.md`)
2. If output < 100 chars → use format-specific fallback reader
3. Report: "  ✅ {filename} — {char_count} ký tự ({format})"
4. On error: "  ❌ {filename} — Lỗi: {error_message}" → skip file, continue with others

---

## Step 3: Fetch URL Content

For each URL:
1. Use `fetch_webpage` tool with `query: "main content"`
2. If unavailable or empty → use httpx + BeautifulSoup fallback
3. Clean content: remove nav/footer/cookie boilerplate, limit to 50,000 chars
4. Report: "  ✅ {page_title} ({url_domain}) — {char_count} ký tự"

For error messages and URL error types, see `references/code-patterns.md`.

For web search workflow, see `references/web-search-enrichment.md`.

---

## Step 4: Combine & Return

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
   ```

---

## What This Skill Does NOT Do

- Does NOT synthesize or merge content — that's bien-soan
- Does NOT translate content — that's bien-soan
- Does NOT generate output files — that's tao-* skills
- Does NOT install dependencies — redirects to /cai-dat
