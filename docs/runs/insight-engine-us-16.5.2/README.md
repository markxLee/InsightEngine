# US-16.5.2 — Load Matching Experience Template at Pipeline Start

**Status:** DONE
**Branch:** `feature/insight-engine-us-16.5.2`
**Phase:** 16 — Epic 16.5
**Blocked By:** US-16.5.1 ✅
**Blocks:** none — closes Phase 16

## Goal

At pipeline start (before strategist), look up the closest past successful
run for the same intent and pass its plan as a non-binding hint. Lets the
strategist warm-start from proven patterns instead of planning from scratch.

## Acceptance Criteria

| AC  | Statement | Where met |
|-----|-----------|-----------|
| AC1 | `experience.py match` subcommand exists; takes `--intent`, `--prompt`, optional `--limit`/`--min-score` | `scripts/experience.py::cmd_match` + argparse `match` subparser |
| AC2 | Matching algorithm uses tokenized Jaccard similarity with stopword filtering for English + Vietnamese | `_tokenize` (Unicode-aware regex + length & stopword filter) + `_jaccard`; documented in README |
| AC3 | Output JSON includes path, score, audit score, formats, plan_summary; sorted by (score DESC, audit_score DESC) | `cmd_match` returns this exact shape — verified via functional test (Jaccard 0.7 for similar, 0 for unrelated) |
| AC4 | Orchestrator step 2d calls `match` BEFORE strategist; failure is non-fatal (best-effort) | `orchestrator.agent.md` step 2d — explicit "any error is non-fatal", "MUST NOT block the pipeline", "purely additive" |
| AC5 | When matches found, top match passed to strategist as `prior_experience` hint; strategist may adapt or discard | step 2d narrative; README explicitly notes "non-binding suggestion" |

## Files Touched

```
scripts/experience.py                    (M, +match subcommand + tokenize/jaccard helpers; find stub upgraded)
docs/experiences/README.md               (M, full Match Behaviour section)
.github/agents/orchestrator.agent.md     (M, new step 2d before strategist call)
docs/runs/insight-engine-us-16.5.2/*     (A, run artifacts)
docs/product/insight-engine/checklist.md (M, status PLANNED→IN_PROGRESS→DONE; closes Phase 16)
```

## Design Notes

- **Why Jaccard over embeddings**: zero new dependencies, deterministic,
  fast enough for a directory of <1000 files. Embeddings would add a model
  download to the critical path of pipeline startup.
- **Why stopword filtering**: prevents two unrelated prompts from matching
  on "the", "và", "của" etc., which would dominate the union and flatten
  scores.
- **`min_score=0.15` default**: empirically chosen — Vietnamese prompts of
  10-20 tokens with stopwords removed need ~3 shared content tokens to clear
  the bar. Tunable per-call via CLI arg.
- **Best-effort + non-binding**: critical design choice. The orchestrator
  must run identically when no experiences exist (clean install) AND when
  match finds something. Strategist owns the final plan — hint never
  overrides judgement.
- **Sort by (score, audit_score)**: ties on similarity broken by which past
  run produced the better-graded output. Encourages the system to replay
  high-quality patterns.
- **Out of scope**: sub-intent clustering, prompt-embedding similarity, plan
  diffing across templates. All deferred — current Jaccard is sufficient
  signal for the warm-start use case.

## Validation

- `ast.parse` syntax check passed
- Functional smoke test:
  - Save: `EXPERIENCE_SAVED: docs/experiences/research/<...>.json`
  - Match (similar prompt): `score: 0.7`, returned with full payload
  - Match (unrelated prompt): `matches: []`, `reason: ok`
  - Cleanup verified
- Cross-reference between README, script docstring, and orchestrator step 2d are consistent

## Phase 16 Complete

US-16.5.2 closes Phase 16 (Agent-Centric Architecture & Tool-Agnostic
Search). All 9 stories shipped:

- 16.1.1 Probe ✅, 16.1.2 Playwright ✅, 16.1.3 HTTP ✅
- 16.2.1 Execution Agent ✅, 16.2.2 Child soft-flow ✅
- 16.3.1 RULE-9 Hard-Flow ✅
- 16.4.1 Adaptive replan ✅
- 16.5.1 Save experience ✅, 16.5.2 Load experience ✅

## Commit Message

```
feat(experience): match prior runs at pipeline start as planning hint (US-16.5.2)
```
