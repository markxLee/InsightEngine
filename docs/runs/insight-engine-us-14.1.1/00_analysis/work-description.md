# Work Description — US-14.1.1

## Story
**US-14.1.1:** Source discovery search for domain + country  
**Phase:** 14 | **Epic:** 14.1 — Source Discovery Protocol  
**Branch:** `feature/insight-engine-us-14.1.1`

## Problem Statement
The gather skill currently enters data collection mode assuming it already knows which platforms
exist for the requested domain + country (review sites, job boards, local directories). This
reliance on model training knowledge produces stale or inaccurate source lists — for example,
hardcoding Vietnamese review platforms without checking whether they're currently active or
complete. US-14.1.1 adds an autonomous source discovery step that runs BEFORE any data
collection begins when soft-knowledge domain sources are involved.

## Expected Outcome
When `gather` enters `data_collection` mode for soft-knowledge sources (not well-known global
platforms like LinkedIn/Shopee), it first performs ≥2 search queries to discover current
platforms, then builds a candidate source list with name, URL, source type, and description.
This list is passed to US-14.1.2 (source classification) and ultimately US-14.2.1 (accessibility
testing). The user is never asked which sources to use — discovery is fully autonomous.

## In Scope
- Add new signal `source_discovery_needed` to Step 1 detection logic in gather SKILL.md
- Add new `## Source Discovery Protocol (SD-0)` section to gather SKILL.md:
  - When to trigger (soft-knowledge domain sources)
  - How to construct discovery search queries
  - How to parse results into candidate source list
  - Minimum 3 candidates requirement
  - Report format for discovered sources

## Out of Scope
- Source classification (US-14.1.2)
- Accessibility testing (US-14.2.1, US-14.2.2)
- Verified source plan output (US-14.3.1)
- Retry loop (US-14.4.1)

## Acceptance Criteria
- AC1: Before data collection requiring source selection, pipeline performs ≥2 search queries
- AC2: Queries constructed from domain context (e.g., "company review sites Vietnam 2024")
- AC3: Results parsed into candidate source list: name, URL, source type, description
- AC4: Discovery runs silently — user NOT asked which sources to use
- AC5: Requires ≥3 candidate sources before proceeding to accessibility testing

## Affected Files
- `.github/skills/gather/SKILL.md` — primary change (add SD-0 section + Step 1 detection)

## Tech Constraints
- Skill documentation only (no Python scripts for this US)
- Must integrate cleanly with existing DC-0 → DC-7 protocol chain
- Report format must respect jargon shield (no HTTP codes, no "scraping", etc.)
