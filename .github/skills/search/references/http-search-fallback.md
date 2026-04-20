# HTTP Zero-Auth Search Fallback (Tier 3 — US-16.1.3)

## Purpose

Final tier of the search cascade. Used when:

1. Tier 1 (`vscode-websearchforcopilot_webSearch`) is unavailable, AND
2. Tier 2 (Playwright stealth → DuckDuckGo HTML) returned empty results OR
   Playwright itself is unavailable in the runtime environment.

## Why a Third Tier

Tier 2 depends on a working Playwright + Chromium installation. In some
runtimes (locked-down CI, minimal containers, CodeSpaces without browser
deps) Playwright is unavailable. Tier 3 needs only `httpx` + `beautifulsoup4`
— both already in `requirements.txt` for the existing URL-fetch fallback —
so it works in any environment that can make outbound HTTPS calls.

## Contract

**Script:** `.github/skills/search/scripts/http_search.py`

**Invocation:**

```bash
python3 .github/skills/search/scripts/http_search.py "<query>" [--limit N]
```

**Stdout (exit 0):** JSON matching the primary search tool

```json
{"query": "...", "results": [{"url": "...", "title": "...", "snippet": "..."}, ...]}
```

**Exit codes:**

| Code | Meaning | Caller action |
|------|---------|---------------|
| 0    | Results found | Use results, continue Step 3 URL fetching |
| 1    | HTTP 200 but no matches | Treat query as empty, continue to next query |
| 2    | Error (network, parse) | Log diagnostic, treat query as empty |

## Provider

Uses `https://html.duckduckgo.com/html/` (DuckDuckGo's no-JS HTML endpoint).
No API key, no rate-limit cookie, no auth flow. Sends a standard browser
User-Agent and follows redirects. POSTs the query as form data to match the
endpoint's expected request shape.

## Why DuckDuckGo (Same as Tier 2)

- Zero-auth and zero-rate-limit for low-volume searches
- HTML structure is parser-friendly (stable `div.result__a` selectors)
- Same provider as Tier 2 → consistent result quality across tiers
- No telemetry concerns vs. Google scraping
- Safe ToS for non-commercial assistant use

## Distinction from Tier 2

| Aspect | Tier 2 (US-16.1.2) | Tier 3 (US-16.1.3) |
|--------|--------------------|--------------------|
| Engine | Playwright stealth Chromium | Plain `httpx` request |
| Dependencies | playwright + browser binary | httpx + beautifulsoup4 only |
| Bot evasion | Stealth fingerprint | Standard UA header only |
| Failure mode | Browser launch errors | Pure HTTP errors |
| Best for | Bot-protected sites | Restricted runtimes |

## Diagnostics

On any non-zero exit, the script writes a one-line error to stderr (caller
appends to `docs/runs/<branch-slug>/diagnostics/search-probe.log`).

## Out of Scope

- Bing, Brave, Google scraping (each requires more sophisticated rate-limit handling)
- Image/video search (only general web results)
- Localization beyond `kl=wt-wt` (no-region) — the caller can pass the query
  in the user's language and DuckDuckGo handles language detection internally
- Auth-gated APIs (Brave Search API, SerpAPI) — explicitly excluded per
  US-16.1.3 "zero-auth" requirement

## Rollback

If Tier 3 misbehaves in production:

1. Comment out the Tier 3 block in `SKILL.md` "Fallback cascade"
2. Restore the empty-results message immediately on Tier 2 exhaustion
3. The script file can stay on disk — it has no import side effects
