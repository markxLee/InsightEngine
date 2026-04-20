# Adaptive Re-Planning on Failure (Execution Agent)

> Implements **US-16.4.1**. Specifies the exact triggers, request format, and
> budget for **auditor-driven** re-planning — distinct from the
> execution-driven child soft-flow path of US-16.2.2.

## Two Re-Planning Sources (don't confuse)

| Source | Document | Trigger location |
|--------|----------|------------------|
| **Execution-driven** (cascade exhaustion / wrong angle suspected mid-execution) | [`child-soft-flow.md`](child-soft-flow.md) (US-16.2.2) | Inside Execution Agent, before delivering to Auditor |
| **Auditor-driven** (output produced but scored low) | THIS DOCUMENT (US-16.4.1) | After Auditor returns FAIL |

Both paths feed the same downstream pattern: Advisory → new plan → Execution
retry. They differ only in where the trigger fires.

## Hard Triggers

The Execution Agent MUST initiate auditor-driven re-planning when **any** of:

```yaml
TRIGGER (any one):
  - Auditor returned VERDICT=FAIL with score < 60 on the most recent attempt
  - Auditor returned VERDICT=FAIL with score < 80 for 2 consecutive attempts
    (per RULE-2 pivot rule)
  - Auditor flagged a BLOCKING_FAILURE (any requirement scored < 60)
```

`score < 60` after a single attempt is sufficient to trigger Advisory because
small incremental fixes are unlikely to recover. Scores in the 60–79 range get
one same-method pivot first (existing RULE-2 behaviour), only escalating after
the second consecutive sub-80.

## Forbidden: Same-Method Retry

Once any trigger fires, the Execution Agent **MUST NOT** simply retry with the
same approach. The whole point of US-16.4.1 is that brute-force retry is
banned. The Advisory + Strategist replan path is the only allowed continuation:

```yaml
FORBIDDEN:
  - Same tool, same args, same source → no
  - Same tool, slightly different args, same source → no (counts as same method)
  - Same skill mode (e.g. compose:standard) after a sub-80 standard run → must change mode

ALLOWED ONLY VIA REPLAN PATH:
  - Different tool from cascade
  - Different source / domain
  - Different framing of the question
  - Different skill mode or template
```

## Advisory Request Format

```python
runSubagent(
    agentName="advisory",
    description="Adaptive re-planning after auditor failure",
    prompt="""
QUESTION: How should I re-approach this delivery step after auditor failure?
SEVERITY: moderate

WHAT_WAS_TRIED:
- Tool/approach: {tool_used} via {skill_mode}
- Result: produced {N} chars / {M} sections
- Auditor score: {score}/100 (verdict: FAIL)
- BLOCKING_FAILURES: {requirement_ids_below_60}
- Auditor SUMMARY: {auditor_summary_one_liner}

ORIGINAL_REQUIREMENT:
{original_user_requirement_or_step_purpose}

CONSTRAINTS:
- 2–3 alternative approaches with rationale
- Each alternative MUST differ in tool, source, framing, or skill mode
- Each alternative MUST NOT repeat what's listed under WHAT_WAS_TRIED
"""
)
```

Advisory returns the standard `PERSPECTIVES / RECOMMENDATION / CONFIDENCE`
block. Execution Agent applies the recommendation if `CONFIDENCE >= 0.7`;
otherwise returns `status=partial` with the gap report (per RULE-8).

## Strategist Replan Format (after Advisory recommends an alternative)

The Advisory output is fed to the Strategist in **replan mode** (not
child_workflow mode), because the parent step itself is being re-planned, not
decomposed:

```python
runSubagent(
    agentName="strategist",
    description="Replan failed step using Advisory recommendation",
    prompt="""
REPLAN_MODE: true

FAILED_STEP: {step_id}
ADVISORY_RECOMMENDATION: {recommendation_summary}
ADVISORY_CONFIDENCE: {confidence}

FAILURE_CONTEXT:
- Auditor score: {score}/100
- BLOCKING_FAILURES: {requirement_ids}
- WHAT_WAS_TRIED: {one-line summary}

REPLAN_CONSTRAINT:
- Replace ONLY the failed step (do not re-plan upstream steps)
- New step must implement the Advisory recommendation
- Total wall time budget: same as original step
"""
)
```

Strategist returns a single replacement step in `STEPS:` form. Execution Agent
then re-executes that single step using the new tool / source / framing.

## Budget (Hard Cap)

```yaml
PER_FAILED_STEP:
  advisory_calls:    1   # exactly one re-angle consultation per failed step
  strategist_calls:  1   # exactly one replan per failed step
  retry_executions:  1   # exactly one re-execution under the new plan

TOTAL_CYCLE: 1 + 1 + 1 = 3 sub-calls per failed step

PER_PIPELINE_RUN:
  Inherits the standard budgets:
    - advisory: 2 calls total (RULE-9, advisory.agent.md)
    - strategist: 5 calls total shared across initial_plan + replan + child_workflow modes
                  (strategist.agent.md "5-call shared budget" note)
    - execution: 8 calls total (execution.agent.md)
  When the per-pipeline budget is exhausted before the per-step budget:
    MUST: deliver partial result with explicit gap report (RULE-8)
    MUST NOT: bypass budgets to make additional calls
```

## Interaction with Child Soft-Flow (US-16.2.2)

Both paths feed the same Advisory/Strategist agents but they are mutually
exclusive **per parent step**:

```yaml
SELECTION_RULE:
  if Auditor returned FAIL on completed output:
    → THIS DOCUMENT (US-16.4.1) — auditor-driven replan
  elif Execution Agent never reached Auditor (cascade exhausted upstream):
    → child-soft-flow.md (US-16.2.2) — execution-driven decompose/re-angle
  else:
    → no replan needed
```

A single failed step MUST consume **at most one** of the two budgets, never
both. If the auditor-driven replan still fails, the second cycle is forbidden;
the step is delivered as partial (RULE-8).

## Acceptance Criteria Mapping (US-16.4.1)

| AC | Statement | Where met |
|----|-----------|-----------|
| AC1 | On failure (cascade exhausted OR score <60 after 2 attempts), Execution Agent calls Advisory with what was tried, what failed, original requirement | "Hard Triggers" + "Advisory Request Format" sections |
| AC2 | Advisory returns 2–3 alternative approaches with rationale | Advisory request `CONSTRAINTS` block + advisory.agent.md returns `PERSPECTIVES` (3-5 perspectives → recommendation) |
| AC3 | Execution Agent picks best alternative and executes with new approach | "Forbidden: Same-Method Retry" + "Strategist Replan Format" — Execution feeds Advisory → Strategist (replan) → re-executes |
| AC4 | Re-planning adds at most 1 Advisory + 1 Strategist call per failed step. Budget respected. | "Budget (Hard Cap)" section — explicit `PER_FAILED_STEP` table |
