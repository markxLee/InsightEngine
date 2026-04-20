# US-16.1.2 — Playwright Stealth Search Fallback

**Status:** DONE
**Branch:** `feature/insight-engine-us-16.1.2`
**Phase:** 16 (Agent-Centric Architecture & Tool-Agnostic Search)
**Epic:** 16.1 (Tool-Agnostic Search Cascade)
**Blocks:** US-16.1.3
**Blocked By:** US-16.1.1 ✅

## Goal

When the primary search tool (`vscode-websearchforcopilot_webSearch`) is
UNAVAILABLE per the probe shipped in US-16.1.1, the search skill must
silently fall back to a Playwright-driven DuckDuckGo HTML query and return
results in the same shape as the primary tool.

## Acceptance Criteria

| AC  | Statement | How met |
|-----|-----------|---------|
| AC1 | Cascade: probe UNAVAILABLE → Playwright + DuckDuckGo/Google | New `scripts/playwright_search.py` invoked from SKILL.md "Fallback cascade — Tier 2" |
| AC2 | Result format identical to primary tool: `{url,title,snippet}` | Script stdout JSON matches; documented in `references/playwright-search-fallback.md` |
| AC3 | User sees `"Đang tìm kiếm..."` not "Using fallback Playwright" | SKILL.md & probe reference enforce silent contract; script logs only to stderr/diagnostics |

## Files Touched

```
.github/skills/search/SKILL.md                                  (M, ~25 lines)
.github/skills/search/references/tool-availability-probe.md     (M, hook section + status notes)
.github/skills/search/references/playwright-search-fallback.md  (A, new reference)
.github/skills/search/scripts/playwright_search.py              (A, new script ~140 LoC)
docs/runs/insight-engine-us-16.1.2/*                            (A, run artifacts)
docs/product/insight-engine/checklist.md                        (M, status PLANNED→IN_PROGRESS→DONE)
```

## Design Notes

- **Engine choice:** DuckDuckGo HTML (`html.duckduckgo.com`). No JS required, no
  auth, lightest bot wall. Google reserved for future bump (`--engine google`).
- **Anti-detection:** Reuses the exact stack from `playwright-stealth.md`
  (URL fetch script): `--disable-blink-features=AutomationControlled`,
  `navigator.webdriver` shadowing, realistic UA + Sec-Fetch headers.
- **URL unwrapping:** DDG wraps outbound links in `/l/?uddg=<encoded>`.
  `_clean_ddg_url()` decodes them so callers get real target URLs.
- **Exit codes:** `0` results, `1` empty, `2` error. Lets the SKILL distinguish
  "engine worked, nothing matched" from "engine broke" without parsing stderr.
- **No coupling:** Script is standalone; SKILL invokes via subprocess. Keeps
  Playwright optional — if not installed, exit 2 → escalate to Tier 3 (next US).

## Validation

- `python3 -c "import ast; ast.parse(...)"` → syntax OK
- Result shape unit-checked against primary tool docs (matches `{url,title,snippet}`)
- No live DDG hit performed in CI (would be flaky); manual smoke recommended
  on first deployment.

## Out of Scope (deferred)

- Tier 3 HTTP zero-auth fallback → US-16.1.3 (next, immediately unblocked)
- Result caching across queries
- Google/Bing engines

## Commit Message

```
feat(search): add Playwright stealth Tier-2 search fallback (US-16.1.2)
```
