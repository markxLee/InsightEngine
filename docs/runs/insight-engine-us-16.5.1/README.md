# US-16.5.1 — Save Experience Template After Successful Pipeline Run

**Status:** DONE
**Branch:** `feature/insight-engine-us-16.5.1`
**Phase:** 16 — Epic 16.5
**Blocked By:** US-16.4.1 ✅
**Blocks:** US-16.5.2

## Goal

Persist a JSON snapshot of every successful pipeline run (intent, plan,
per-step outcomes, audit scores, budget) so future runs with similar intent
can replay or pattern-match against past successes (US-16.5.2 will consume).

## Acceptance Criteria

| AC  | Statement | Where met |
|-----|-----------|-----------|
| AC1 | Script `scripts/experience.py save` exists with documented schema_version | `scripts/experience.py` — schema_version=1, full docstring, save subcommand |
| AC2 | Templates saved only when `final_audit_score >= 80` AND intent classified | `_extract_template` returns None on missing intent or score < 80 → exit 1 |
| AC3 | Storage path is persistent (not under `tmp/`) and intent-partitioned | `EXPERIENCE_ROOT = docs/experiences`; layout `<intent>/<timestamp>-<hash>.json` |
| AC4 | Orchestrator step 9 calls save in best-effort mode (failure non-fatal) | `orchestrator.agent.md` step 9 — `python3 scripts/experience.py save ... \|\| true` |
| AC5 | Schema captures: intent, raw prompt + hash, plan summary, step outcomes, final score, budget, formats | Verified via functional smoke test — output JSON contains all 7 fields |

## Files Touched

```
scripts/experience.py                   (A, ~150 LoC, syntax + functional smoke test passed)
docs/experiences/README.md              (A, layout + schema + privacy notes)
.github/agents/orchestrator.agent.md    (M, step 9 calls experience.py save)
docs/runs/insight-engine-us-16.5.1/*    (A, run artifacts)
docs/product/insight-engine/checklist.md (M, status PLANNED→IN_PROGRESS→DONE)
```

## Design Notes

- **Persistent path (`docs/experiences/`) not `tmp/`**: experience templates
  must survive `tmp/` cleanups across sessions. `docs/` is the only persistent
  tree the agent owns.
- **Best-effort save (`|| true`)**: experience persistence is a side benefit,
  never a blocker for delivery. Exit 1 (criteria-not-met) is normal for runs
  that didn't reach 80 and must not surface as an error.
- **Intent partitioning**: enables US-16.5.2's load query to be a simple
  directory listing rather than a full-text search.
- **Score gate (>=80)**: deliberately strict. Storage is for replay-worthy
  exemplars, not noise. Failed/low-quality runs would actively hurt US-16.5.2.
- **Raw prompt hash**: short hash collision-resists same-intent-different-
  prompt entries while keeping filenames human-scannable.
- **Find subcommand stub**: included in US-16.5.1 so the storage layout is
  end-to-end testable. US-16.5.2 will replace the stub with intent-based
  matching logic.

## Validation

- `python3 -c "import ast; ast.parse(...)"` → OK
- Functional smoke test: synthetic state file → `EXPERIENCE_SAVED: docs/experiences/synthesis/<...>.json`
- Output JSON contains all 7 schema fields (verified via cat)
- `find` stub returns the saved file path
- Test artifacts cleaned up post-validation

## Commit Message

```
feat(experience): save successful pipeline run as replayable template (US-16.5.1)
```
