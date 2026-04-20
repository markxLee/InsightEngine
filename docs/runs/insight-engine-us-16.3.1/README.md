# US-16.3.1 — Formalize Hard-Flow Execution Order in RULE.md

**Status:** DONE
**Branch:** `feature/insight-engine-us-16.3.1`
**Phase:** 16 — Epic 16.3 (Hard-Flow Protocol in RULE.md)
**Blocked By:** US-16.2.1 ✅

## Goal

Make the agent-level execution order non-negotiable law. Every session MUST
follow Orchestrator → State+Checklist → Strategist → Execution Agent → Auditor
→ (PASS: notify) / (FAIL: Advisory → replan → Execution → Auditor).

## Acceptance Criteria

| AC  | Statement | Where met |
|-----|-----------|-----------|
| AC1 | RULE.md gains Hard-Flow section: Orchestrator → state+checklist → Strategist → Execution → Auditor → (pass: notify) / (fail: Advisory → new plan → Execution retry) | New `RULE-9: Agent-Centric Hard-Flow` with explicit flow diagram and per-step MUST table |
| AC2 | Each step uses explicit "MUST" language, no optionality | Per-Step MUST Statements block — every transition has MUST + MUST_NOT clauses |
| AC3 | Child soft-flow trigger condition documented (Execution Agent requests it) | Dedicated "Child Soft-Flow Trigger (Hard Rule)" subsection — TRIGGER + INVOCATION + REPORTING |
| AC4 | Existing RULE.md rules preserved unchanged | Diff confirms only an APPEND between RULE-8 and the closing footer; RULE-1..8 untouched. New rule numbered RULE-9 to preserve numbering. |

## Files Touched

```
.github/RULE.md                            (M, append RULE-9 only — RULE-1..8 byte-identical)
docs/runs/insight-engine-us-16.3.1/*       (A, run artifacts)
docs/product/insight-engine/checklist.md   (M, status PLANNED→IN_PROGRESS→DONE)
```

## Design Notes

- **Numbering choice:** Added as **RULE-9** (not inserted between existing
  rules) so external references like "RULE-2" or "RULE-4" remain stable. AC4
  preserved byte-for-byte.
- **Skill flow vs Agent flow distinction:** The closing paragraph of RULE-9
  explicitly states the relationship to RULE-4 — RULE-4 governs *which skills*
  run in what order; RULE-9 governs *which agents* own each transition.
- **Child soft-flow** documented as a Hard Rule subsection because it's the
  only mechanism for mid-execution sub-flow expansion — must be explicit so no
  agent invents its own escalation path.
- **Failure handling** mirrors RULE-2 pivot rules but binds them to the
  Auditor → Advisory → Strategist (replan) → Execution chain.

## Validation

- `wc -l RULE.md`: 179 → ~280 lines (RULE-9 added at end before footer)
- All RULE-1..8 headings + bodies unchanged (verified by visual diff during edit)
- Cross-refs resolve: RULE-9 references RULE-2/RULE-4/RULE-5/RULE-6/RULE-8 + child-soft-flow.md

## Commit Message

```
feat(rule): add RULE-9 Agent-Centric Hard-Flow protocol (US-16.3.1)
```
