---
name: gather
description: |
  Read content from local files and explicit URLs provided by the user.
  Uses markitdown as primary reader with format-specific fallbacks for garbled output.
  3-tier URL fetching: fetch_webpage → httpx → Playwright stealth mode (for bot-protected sites).
  Auto-reviews gathered content quality and retries with fallback readers if insufficient.
  Always use this skill when the user provides files to read or specific URLs to fetch —
  "đọc file này", "lấy nội dung từ URL này", or when a file path or URL is dropped into chat.
  Do NOT use for web search, topic research, or platform discovery → use search skill.
argument-hint: "[file paths or URLs]"
version: 3.0
compatibility:
  requires:
    - Python >= 3.10
    - markitdown[all]
    - httpx, beautifulsoup4 (URL fallback)
    - playwright (bot-protected URL fallback)
  tools:
    - run_in_terminal
    - fetch_webpage (primary URL reader)
---

# Thu Thập — File & URL Reading Skill

**References:** `references/code-patterns.md` | `references/playwright-stealth.md`

**Governance:** Read and follow `.github/RULE.md` — it overrides all instructions below.

This skill reads content from local files and explicit URLs — and returns clean Markdown text.
It runs standalone or as part of the synthesize pipeline.

**Quality loop (RULE-2):** After reading all sources, self-review runs automatically. If content
is insufficient, pivots through fallback strategies (max 3 pivots per RULE-2):
1. Switch reader: markitdown → format-specific library
2. Switch fetch tier: fetch_webpage → httpx → Playwright
3. Report failure with honest gap assessment

For web search, topic research, or platform discovery → use the **search** skill instead.

All responses to the user are in Vietnamese.

---

## Supported Formats

```yaml
LOCAL_FILES:
  primary_reader: markitdown
  supported: .docx, .xlsx, .pdf, .pptx, .txt, .md, .csv, .html, .jpg, .png
  fallback: format-specific library if markitdown returns < 100 chars

URLS:
  tier_1: Copilot fetch_webpage tool (fast, default)
  tier_2: httpx + beautifulsoup4 (fallback for failures)
  tier_3: Playwright stealth mode (bot-protected / JS-rendered sites)
  bot_signals: 403/429, Cloudflare challenge, empty JS content → auto-escalate to Tier 3
```

---

## Step 1: Identify Sources

1. Extract file paths from the user request (absolute or relative)
2. Extract URLs (http:// or https://)
3. If user provides neither files nor URLs, check if they want web search → route to **search** skill
4. Report: "📂 Nguồn: {N} file / {M} URL"

---

## Step 2: Read Local Files

For each file:
1. Skip files > 50 MB with a warning (too large for context)
2. Try `markitdown {file}` first
3. If output < 100 chars → use format-specific fallback reader (see `references/code-patterns.md`)
4. Report: "✅ {filename} — {chars} ký tự" or "❌ {filename} — {error}"

---

## Step 3: Fetch URL Content (3-Tier Fallback)

Try tiers in order — escalate on failure or bot-detection:

1. **fetch_webpage** (default) — if content ≥ 50 chars: done
2. **httpx + BeautifulSoup** — if Tier 1 fails (see `references/code-patterns.md`)
3. **Playwright stealth** — if bot-detection signals (403, Cloudflare challenge, empty JS
   content): `python3 scripts/playwright_fetch.py "{url}" --wait 3`

**After each fetch:** read first 200–500 chars. Reject error pages, login walls, empty stubs,
or wrong page type (e.g., got a listing page when you need a detail page). If bad → next tier.

Skip directly to Playwright when: domain is known bot-protected, a previous request from the
same domain returned 403/429, or the URL pattern clearly indicates a JS-rendered SPA.

---

## Step 4: Quality Review

Before returning content, check:
- **Volume**: ≥500 chars per source (reject empty/error pages)
- **Specificity**: contains actual content, not just navigation/headers

If a source fails: try fallback reader once. If still empty, report failure for that source.

---

## Step 5: Combine & Return

Structure each source:

```
## Nguồn: {source_name}
> {path_or_url} | {char_count} ký tự

{content}

---
```

Final summary: "📋 Thu thập hoàn tất: {N} nguồn / {total_chars} ký tự / {quality_assessment}"

---

## Examples

- "Đọc file report.pdf và data.xlsx" → markitdown both → combined Markdown
- "Lấy nội dung từ https://example.com" → fetch_webpage → Markdown
- "Đọc 3 file docx trong thư mục input/" → markitdown each → combined output

---

## What This Skill Does NOT Do

- Does NOT search the internet or discover platforms → search
- Does NOT synthesize or translate content → compose
- Does NOT generate output files → gen-* skills
- Does NOT install dependencies → setup
