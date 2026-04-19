# Done Check — US-14.1.1

## Story
**US-14.1.1:** Source discovery search for domain + country

## DoD Verification

| Criterion | Status |
|-----------|--------|
| AC1: ≥2 search queries before collection | ✅ SD-0 executes ≥2 discovery queries |
| AC2: Queries constructed from domain context | ✅ Templates built from domain+country+year |
| AC3: Results parsed into candidate source list | ✅ name, URL, source_type, description fields |
| AC4: Discovery runs silently — no user questions | ✅ SD-0 auto-proceeds, user never asked |
| AC5: Requires ≥3 candidates before proceeding | ✅ Threshold check + fallback additional round |

## Files Changed
- `.github/skills/gather/SKILL.md` — added `source_discovery_needed` signal in Step 1; added SD-0 section before DC-0; updated DC-0 to reference SD-0 candidates

## Commit Message
```
feat(gather): add SD-0 source discovery protocol for soft-knowledge domains (US-14.1.1)

- Add source_discovery_needed detection signal in gather Step 1
- Add SD-0: Source Discovery section before DC-0 in data_collection mode
- When item type requires soft-knowledge sources (review platforms, job boards,
  regional directories) and no explicit sources provided, SD-0 now runs ≥2
  discovery searches, parses results into candidate source list, checks ≥3
  candidates, and passes list to US-14.1.2 (classification)
- DC-0 updated to use sd0_candidates from SD-0 instead of model assumptions
- Discovery is fully autonomous — user is never asked which sources to use
```
