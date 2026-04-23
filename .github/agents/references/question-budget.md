# Question Budget & User Channel Protocol (Orchestrator)

> Extracted from orchestrator.agent.md for maintainability.
> Referenced by: orchestrator core agent.
> Implements: RULE-10 (Orchestrator-Exclusive User Channel), RULE-11 (Pre-Question Consultation)

---

## User Channel Gatekeeper (US-17.1.3)

The orchestrator is the SOLE gatekeeper for all user-facing emissions. Implements RULE-10.

### Emission Types

| Type | Preconditions | Examples |
|------|--------------|---------|
| `result_delivery` | Auditor PASS (score ≥ 80/100) + all output files verified | Final files + delivery summary |
| `user_question` | RULE-11 consultation satisfied + question budget not exhausted | Content ambiguity clarification |
| `status_update` | Pipeline step boundary (step completed or failed) | Progress messages ("✅ Đã xong...") |

### Gatekeeper Protocol

```yaml
BEFORE_ANY_USER_EMISSION:
  1. CLASSIFY emission type: result_delivery | user_question | status_update
  2. CHECK preconditions for that type (see table above)
  3. APPLY jargon shield (RULE-7) to message content
  4. LOG emission to session state:
     python3 scripts/save_state.py log-emission \
       --type <emission_type> \
       --reason "<why this emission is needed>" \
       --timestamp <ISO-8601>
  5. EMIT to user

ON_PRECONDITION_FAILURE:
  result_delivery without auditor PASS:
    → Route back to auditor or retry loop — do NOT deliver unaudited output
  user_question without consultation:
    → Consult advisory + strategist first (RULE-11) — do NOT ask user prematurely
  status_update without step boundary:
    → Suppress — internal progress stays internal
```

---

## Question Budget Enforcement (US-17.2.2)

Hard question budget per pipeline run (default: max 2 questions).

```yaml
QUESTION_BUDGET_PROTOCOL:
  init:
    # question_budget initialized by save_state.py init: {max: 2, used: 0, log: []}

  before_asking_user:
    1. CHECK budget: python3 scripts/save_state.py log-emission \
         --type user_question \
         --reason "<the question>" \
         --consultation '<json evidence from advisory+strategist>'
       # EXIT 1 if budget exhausted → orchestrator MUST NOT ask
    2. IF exit code 1 (BUDGET_EXHAUSTED):
       → Make autonomous decision using available context
       → Log decision rationale to step_states
       → Continue pipeline without user input
    3. IF exit code 0 (QUESTION_LOGGED):
       → Proceed to ask user (budget decremented automatically)

  budget_exhausted_fallback:
    - Use advisory agent for ambiguous decisions
    - Use strategist agent for workflow alternatives
    - Apply reasonable defaults documented in skill instructions
    - Log "autonomous_decision" in step notes with rationale

  budget_reset:
    - Resets on new pipeline run (save_state.py init)
    - Does NOT reset mid-pipeline
    - Per-session, not per-step
```

---

## Pre-Question Consultation (RULE-11)

```yaml
CONSULTATION_SEQUENCE:
  1. CONSULT advisory: "Can this be resolved autonomously? Suggest alternatives."
  2. CONSULT strategist: "Given this gap, can we proceed with reasonable defaults?"
  3. EVALUATE: IF either agent provides autonomous solution → USE IT, do NOT ask user
  4. ASK user: ONLY if step 3 allows + LOG consultation evidence

MUST:
  - Consult advisory AND strategist before any user question
  - Log consultation evidence to session state
  - Respect question budget (default max 2)
  - If budget exhausted: decide autonomously — no more questions

MUST_NOT:
  - Ask user without prior consultation
  - Exceed question budget
  - Reset question budget mid-pipeline
```
