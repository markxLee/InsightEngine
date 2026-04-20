# Playwright Search Fallback — Tier 2 of Search Cascade

> Implements **US-16.1.2**. Activated when the tool-availability probe
> (US-16.1.1) returns `UNAVAILABLE` for `vscode-websearchforcopilot_webSearch`.

## Cascade Position

```
Tier 1: vscode-websearchforcopilot_webSearch  ← gated by availability probe
   │ UNAVAILABLE
   ▼
Tier 2: Playwright stealth → DuckDuckGo HTML  ← THIS DOCUMENT
   │ no results / error
   ▼
Tier 3: HTTP zero-auth (US-16.1.3, planned)
```

## Contract

The script `scripts/playwright_search.py` returns results in the **same shape**
as the primary tool, so callers can substitute it transparently:

```json
{
  "query": "<original query>",
  "results": [
    {"url": "https://...", "title": "...", "snippet": "..."},
    ...
  ]
}
```

- Exit `0` → results found.
- Exit `1` → no results (engine returned an empty page or all entries filtered).
- Exit `2` → unexpected error (network, browser launch, parser).

## How the Search Skill Invokes It

After the probe in Step 2.5 returns `UNAVAILABLE`:

1. Show the user the standard friendly message: `"Đang tìm kiếm..."`.
   **Do NOT** mention Playwright, fallback, or any tool name.
2. For each query produced in Step 2, run:
   ```bash
   python3 .github/skills/search/scripts/playwright_search.py "<query>" --limit 8
   ```
3. Parse stdout JSON, treat `results` as the equivalent of the primary tool's
   output. Continue with Step 3 URL fetching exactly as before.
4. If exit code `1` for **all** queries, escalate to Tier 3 (US-16.1.3). Until
   Tier 3 ships, emit the existing fallback message
   `"Không tìm thấy kết quả tìm kiếm cho yêu cầu này."`
5. If exit code `2`, log a single diagnostic line to
   `docs/runs/<branch-slug>/diagnostics/search-probe.log` and treat as no
   results for the affected query. Other queries proceed normally.

## Why DuckDuckGo HTML

| Engine            | JS required? | Bot wall? | Captcha? | Auth? |
|-------------------|--------------|-----------|----------|-------|
| html.duckduckgo.com | No         | Light     | Rare     | None  |
| google.com        | Yes (heavy)  | Aggressive| Frequent | None  |
| bing.com          | Yes          | Medium    | Possible | None  |

DuckDuckGo's `/html/` endpoint renders server-side and is the most reliable
zero-auth target for headless extraction. URL unwrapping is required because
DDG wraps outbound links in `/l/?uddg=<encoded>`.

## Anti-Detection

Reuses the proven stack from `playwright-stealth.md` (URL fetching reference):

- `--disable-blink-features=AutomationControlled`
- `navigator.webdriver → undefined` via `addInitScript`
- Realistic UA + Sec-Fetch headers + `Asia/Ho_Chi_Minh` timezone
- 1-second settle wait after `domcontentloaded`

## User-Facing Behavior (AC3)

The user sees only:

> 🔍 Đang tìm kiếm...

They never see:

- "Using fallback Playwright"
- "Primary search unavailable"
- Tool names, exit codes, or error stacks
- Auth/configuration suggestions

All diagnostics go to `docs/runs/<branch-slug>/diagnostics/search-probe.log`
or stderr (which the orchestrator suppresses from user output).

## Performance

- Cold start: ~3 s (Playwright launch + DDG load)
- Warm queries (same context): not yet implemented; v1 spawns a fresh browser per query
- Typical wall time per query: 4–6 s (vs. <1 s for primary tool)

## Limitations (v1)

- Single engine (DuckDuckGo). `--engine google` is reserved for a future bump.
- No result caching across invocations. Each call launches a fresh browser.
- DuckDuckGo may rate-limit aggressive batching. Search skill should keep query
  count ≤ 4 per session when running on Tier 2.

## Dependencies

```
playwright>=1.40
# One-time: python3 -m playwright install chromium
```

If Playwright itself is unavailable, `playwright_search.py` exits with code 2
on the first call and the search skill must escalate to Tier 3 immediately.
