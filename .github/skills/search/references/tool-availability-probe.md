# Tool Availability Probe — Reference

> **Story:** US-16.1.1 — Tool availability probe before search execution
> **Phase:** 16 (Agent-Centric Architecture & Tool-Agnostic Search)
> **Status:** Active

This document defines the **decision procedure** that the `search` skill follows
**before** invoking `vscode-websearchforcopilot_webSearch` (the primary search tool).
The goal is to silently route around an absent / misconfigured primary tool so that
non-tech users never see a Tavily auth popup, configuration error, or missing-key
warning.

---

## Why a Probe?

The primary search tool, `vscode-websearchforcopilot_webSearch`, is provided by the
`vscode-websearchforcopilot` extension. On first use within a session it may:

1. Trigger a **Tavily API key prompt** (popup) if no key is configured.
2. Throw a **configuration error** if the extension is installed but unconfigured.
3. Be entirely **absent** if the extension is not installed.

Any of these surfaces ugly tooling internals to the end user. The probe lets the
skill **silently** detect each case and move on to fallback tiers (US-16.1.2 +
US-16.1.3) without exposing the user to extension-level concerns.

---

## Probe Verdict

The probe returns one of two verdicts:

| Verdict | Meaning |
|---------|---------|
| `AVAILABLE` | Primary tool can be invoked without surfacing auth/config UI |
| `UNAVAILABLE` | Primary tool MUST be skipped; route to fallback tier |

---

## Decision Tree

```
START
  │
  1. SESSION CACHE CHECK
  │  Is the session-scoped flag `primary_unavailable` already set to true?
  │     ├─ YES → return UNAVAILABLE (skip probe entirely)
  │     └─ NO  → continue
  │
  2. PRIOR FAILURE CHECK
  │  Has the user (in this session) already declined a Tavily auth prompt,
  │  or has any earlier search call surfaced a Tavily/auth/configuration error?
  │     ├─ YES → set `primary_unavailable: true`; return UNAVAILABLE
  │     └─ NO  → continue
  │
  3. ATTEMPT WITH SAFETY NET
  │  Call `vscode-websearchforcopilot_webSearch` with the actual user query
  │  (or a minimal canary query if the actual query is expensive). Wrap so:
  │     a) An auth popup notice → treated as failure
  │     b) A "not configured" / "missing key" error string → treated as failure
  │     c) A "tool not available" / extension-absent error → treated as failure
  │     d) Any other exception → treated as failure
  │
  │  IF the call succeeds and returns a result list:
  │     → cache verdict (`primary_available: true`)
  │     → return AVAILABLE
  │
  │  IF the call fails per (a)-(d):
  │     → set `primary_unavailable: true` (session-scoped)
  │     → SWALLOW the error — do NOT surface Tavily/auth/config text to user
  │     → APPEND an internal diagnostic note to the run folder (see below)
  │     → return UNAVAILABLE
END
```

---

## Session Caching

- **Scope:** A single Copilot session (one chat thread). No persistence across
  sessions or workspace restarts.
- **Storage:** Conceptual — represented by Copilot's awareness within the session.
  No file-based or memory-tool caching is required for this story.
- **Invalidation:** A flag set to UNAVAILABLE persists for the session. AVAILABLE
  is also cached but a future story may add a periodic re-check.

---

## Silent Failure Contract

When the probe returns UNAVAILABLE:

1. **NO** Tavily/auth/configuration words shown to the user.
2. **NO** stack trace, error code, or extension name shown.
3. The user-facing message is in **Vietnamese**, friendly, and limited to status:
   - When the fallback cascade (Tier 2 Playwright + Tier 3 HTTP) returns results,
     the user only ever sees `"🔍 Đang tìm kiếm..."` — no fallback chatter.
   - When the entire cascade is exhausted with no results, emit:
     `"Không tìm thấy kết quả tìm kiếm cho yêu cầu này."`

---

## Internal Diagnostic Note

When the probe returns UNAVAILABLE, append a one-line note to:

```
docs/runs/<branch-slug>/diagnostics/search-probe.log
```

Format (one entry per occurrence):

```
[<ISO-8601 timestamp>] PROBE=UNAVAILABLE reason="<short signal>" query="<first 80 chars>"
```

This file is dev-visible only. The user is never directed to it.

---

## Hook for Fallback Tier (US-16.1.2 — shipped)

When this probe returns UNAVAILABLE, the search skill enters the fallback cascade:

```
fallback_cascade(query)
  → Tier 2: python3 .github/skills/search/scripts/playwright_search.py "<query>" --limit 8
      exit 0 → use {url,title,snippet} results, continue Step 3 fetching
      exit 1 → no results, try next query; all empty → escalate to Tier 3
      exit 2 → log diagnostic, treat as no results
  → Tier 3: python3 .github/skills/search/scripts/http_search.py "<query>" --limit 8
      exit 0 → use {url,title,snippet} results, continue Step 3 fetching
      exit 1 → no results, try next query
      exit 2 → log diagnostic, treat as no results
  → All empty across all tiers: emit Vietnamese "no results" message
```

Full contracts: Tier 2 `references/playwright-search-fallback.md`,
Tier 3 `references/http-search-fallback.md`.

---

## Default Behavior

The probe defaults to **AVAILABLE** unless an explicit unavailability signal is
observed. This avoids regressing fully-configured installations that previously
worked.

---

## Out of Scope (handled by later stories)

- Persistent (cross-session) caching of probe state
- User-controlled re-probe / retry primary command
