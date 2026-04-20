# US-16.1.3 — HTTP Zero-Auth Search Fallback (Tier 3)

**Status:** DONE
**Branch:** `feature/insight-engine-us-16.1.3`
**Phase:** 16 — Epic 16.1
**Blocked By:** US-16.1.2 ✅
**Blocks:** none

## Goal

Replace the placeholder Tier 3 in the search fallback cascade with a real
zero-auth implementation using `httpx` + `beautifulsoup4` against DuckDuckGo's
HTML endpoint. Provides a final search tier that works even when Playwright
is unavailable.

## Acceptance Criteria

| AC  | Statement | Where met |
|-----|-----------|-----------|
| AC1 | A zero-auth HTTP search script exists and returns the same JSON shape as the primary tool | `scripts/http_search.py` — emits `{"query","results":[{url,title,snippet}]}` |
| AC2 | No new dependencies introduced (httpx + beautifulsoup4 already in requirements.txt) | Imports verified — both already required by Tier 1 URL fallback |
| AC3 | Documented exit-code contract (0=results, 1=empty, 2=error) | Script docstring + `references/http-search-fallback.md` "Exit codes" table |
| AC4 | Cascade routes Tier 2 empty → Tier 3 → graceful Vietnamese message on triple-empty | `SKILL.md` "Fallback cascade" Tier 3 block + `tool-availability-probe.md` cascade pseudocode |
| AC5 | Reference doc explains tier distinction and rollback path | `references/http-search-fallback.md` "Distinction from Tier 2" + "Rollback" sections |

## Files Touched

```
.github/skills/search/scripts/http_search.py             (A, ~85 LoC, Python syntax verified)
.github/skills/search/references/http-search-fallback.md (A, full contract)
.github/skills/search/SKILL.md                           (M, Tier 3 placeholder → real implementation)
.github/skills/search/references/tool-availability-probe.md (M, cascade pseudocode + Out-of-Scope cleanup)
docs/runs/insight-engine-us-16.1.3/*                     (A, run artifacts)
docs/product/insight-engine/checklist.md                 (M, status PLANNED→IN_PROGRESS→DONE)
```

## Design Notes

- **Why DuckDuckGo HTML for both Tier 2 and Tier 3**: same provider keeps result
  quality consistent across tiers. Difference is the transport (Playwright vs httpx).
- **No User-Agent rotation**: Tier 3 is the no-frills tier. If a caller needs
  bot evasion, they should already be on Tier 2.
- **Why POST not GET**: `html.duckduckgo.com/html/` accepts both but POST is
  the documented contract that won't be flagged as scraping by aggressive
  rate-limiters.
- **Exit code 1 vs 2**: identical caller behaviour today (treat as empty), but
  the distinction lets future telemetry differentiate "search worked but empty"
  vs "search itself failed".
- **Forbidden additions**: explicit Out-of-Scope list in reference doc rules
  out Brave/SerpAPI etc. — the "zero-auth" requirement is non-negotiable.

## Validation

- Python syntax check passed (`ast.parse`)
- All cross-references resolve (SKILL.md ↔ http-search-fallback.md ↔ tool-availability-probe.md)
- Tier 2 → Tier 3 → empty-message escalation path is documented end-to-end
- No new entries in `requirements.txt` needed (verified imports)

## Commit Message

```
feat(search): real Tier 3 HTTP zero-auth fallback via DuckDuckGo (US-16.1.3)
```
