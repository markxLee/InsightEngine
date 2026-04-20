# chore/phase16-audit-fixes — Phase 16 post-delivery audit

## Scope

Read-only audit across all 9 Phase 16 stories, then targeted fixes for
inconsistencies found between the new agent-centric architecture
(US-16.1.x / 16.2.x / 16.4.1 / 16.5.x) and pre-existing pipeline docs.

Phase 16 itself remained 9/9 PASS — these are wiring/consistency fixes,
not feature regressions.

## Findings → Fixes

| # | Severity | Finding | Fix |
|---|----------|---------|-----|
| 1 | HIGH | Orchestrator step 2d (US-16.5.2) passes `prior_experience` hint to Strategist, but `strategist.agent.md` Input section did not declare the field — Strategist would silently drop it. | Added `prior_experience` to OPTIONAL inputs with sub-fields + adoption rule. |
| 2 | MEDIUM | `BUDGET_ENFORCEMENT` in `orchestrator.agent.md` totalled `5+5+2=12` and ignored Execution Agent (8/run, US-16.2.1). Misleading for future budget reasoning. | Renamed `total` → `cross_agent_total: 20`, added explicit `execution: 8` line. |
| 3 | LOW | Orchestrator line 219 said "strategist re-plan uses a separate budget slot" — contradicted the corrected `strategist_total_max: 5` cap. | Rewrote note: replan shares the 5-call cap with initial_plan + child_workflow. |
| 4 | LOW | `execution.agent.md` US-16.4.1 BUDGET said "strategist=5/run shared with child_workflow" — incomplete; replan + initial_plan also share. | Tightened wording to "shared across initial_plan + replan + child_workflow modes" + added `execution=8/run`. |
| 5 | LOW (collateral) | `synthesize/references/agent-mode.md` PIPELINE_BUDGET still showed `total: max 12` (stale). | Updated to mirror orchestrator: `execution: 8`, `cross_agent_total: 20`. |
| 6 | LOW (collateral) | `references/adaptive-replanning.md` PER_PIPELINE_RUN budget block missing execution line + incomplete strategist mode list. | Added execution + reworded strategist line. |

## Files Modified

```
.github/agents/strategist.agent.md                     (+ prior_experience input)
.github/agents/orchestrator.agent.md                   (BUDGET_ENFORCEMENT + Step 7b note)
.github/agents/execution.agent.md                      (US-16.4.1 BUDGET wording)
.github/agents/references/adaptive-replanning.md       (PER_PIPELINE_RUN block)
.github/skills/synthesize/references/agent-mode.md     (PIPELINE_BUDGET block)
```

No scripts modified. No new files except this README.

## Re-Audit Pass

- `grep "max 12"` → 0 matches (was 2)
- `grep "prior_experience"` → 4 matches, all consistent (strategist input + orchestrator + 2 docs)
- `grep "cross_agent_total"` → 2 matches (orchestrator + agent-mode), consistent at 20

## Out of Scope

- RULE-9 already references both child-soft-flow.md and adaptive-replanning.md; no change needed.
- US-16.4.1 "max 1 replan cycle per step" + RULE-9 "max 2 replan cycles per delivery step" are reconcilable: RULE-9's "2" includes the RULE-2 same-method pivot (1) plus US-16.4.1's auditor-driven replan (1). Documented in adaptive-replanning.md → "Hard Triggers" already explains this.
- Image-backend `max_retries` constants in `gen-slide/ppt-master/scripts/image_backends/*.py` are local HTTP retry counters, unrelated to pipeline-level retry budget. Out of scope.
