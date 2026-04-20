# InsightEngine — Non-Negotiable Pipeline Rules

> **Priority:** MANDATORY — These rules override ALL skill-level and agent-level instructions.
> **Enforcement:** Copilot MUST read this file at session start. Violations are pipeline failures.

---

## RULE-1: Hard Session Start

On receiving ANY user prompt that triggers a pipeline (synthesis, creation, research, design, data collection):

1. **FIRST action** — save state + raw prompt:
   ```
   python3 scripts/save_state.py --raw-prompt "<full user prompt>"
   ```
   This creates `tmp/session_state.json` with: `raw_prompt`, `timestamp`, `session_id`, `status: started`.
   If `save_state.py` does not exist: run `setup` skill to create it, then retry.
2. **SECOND action (parallel):**
   - **Intent analysis** — classify what user wants (synthesis, creation, research, design, data_collection, mixed)
   - **Output template creation** — prepare file structure based on expected format (.docx, .xlsx, .pptx, .pdf, .html)
   These two run simultaneously. Both must complete before step 3.
3. **THIRD action** — extract structured requirements (RULE-6) + call strategist for workflow plan.
4. **FOURTH action** — present workflow plan summary to user (information, not a question) and begin execution.

**No exceptions.** No skill may be invoked before step 1 completes.
If `save_state.py` fails and setup cannot fix it: log a warning and continue — but always attempt it first.

---

## RULE-2: Execute-Test-Pivot-Audit Loop

Every skill that produces output MUST follow this loop:

```
execute → self-review → [pivot if needed] → auditor gate → [re-execute if failed] → deliver
```

- **Max pivot attempts:** 3 per delivery step
- **Auditor gate threshold:** >80/100 to pass
- **No single-attempt delivery.** After first execution, self-review MUST run before delivery.
- If auditor gate fails after max pivots: deliver with quality score + explicit gap report.

### Per-Skill Pivot Strategies

Each pivot attempt MUST change at least one strategy — never retry with identical approach:

```yaml
search:
  pivot_1: different query formulation (rephrase, add year, switch language)
  pivot_2: different source domain (switch to alternative platform)
  pivot_3: broaden or narrow scope, switch to deep research mode

gather:
  pivot_1: fallback reader (markitdown → format-specific library)
  pivot_2: different URL fetch tier (fetch_webpage → httpx → Playwright)
  pivot_3: request user to provide alternative file/URL

compose:
  pivot_1: different document structure (reorder sections, merge/split)
  pivot_2: different depth level (expand thin sections with more data points)
  pivot_3: different analytical angle (change framework, add comparison dimension)

gen-word:
  pivot_1: different style template (corporate → academic → minimal)
  pivot_2: restructure sections (TOC depth, heading levels, table layout)
  pivot_3: adjust content density (split long sections, add visual breaks)

gen-excel:
  pivot_1: restructure data layout (pivot table, different column grouping)
  pivot_2: different formula approach (simpler or more robust)
  pivot_3: change formatting (conditional formats, chart types)

gen-slide:
  pivot_1: different layout template (change slide structure)
  pivot_2: different content density per slide (split or merge)
  pivot_3: switch engine (pptxgenjs ↔ ppt-master)

gen-pdf:
  pivot_1: different layout engine (Platypus vs Canvas)
  pivot_2: restructure page layout (margins, columns, font sizes)
  pivot_3: adjust content flow (page break placement, section ordering)

gen-html:
  pivot_1: different style theme
  pivot_2: different layout structure (sections, grid, sidebar)
  pivot_3: switch mode (page ↔ presentation)
```

### Self-Review Checklist (run after every execution)

Before calling auditor, the executing skill MUST check:
1. **Output exists** — file was created, non-empty, correct format
2. **Requirements covered** — cross-check against RULE-6 requirements list
3. **No placeholders** — no "TODO", "TBD", "[insert here]", lorem ipsum
4. **No fabrication** — all data points traceable to gathered sources

---

## RULE-3: Zero Unnecessary Questions

The pipeline MUST NOT ask the user:
- Technical decisions (which tool, which library, which format, which search strategy)
- Confirmation questions for steps the pipeline can decide autonomously
- "Do you want me to continue?" — always continue unless truly blocked

The pipeline MAY ask the user ONLY:
- Content ambiguity: "Bạn muốn bao gồm công ty nào?" (when genuinely unclear)
- Total failure: all sources failed, all approaches exhausted

When in doubt: **decide and proceed.** Explain what you decided, don't ask permission.

---

## RULE-4: Hard Workflow Order

Pipeline execution follows this strict order — no skipping:

1. Session init (RULE-1)
2. Intent classification (orchestrator)
3. Workflow planning (strategist) + output template creation (parallel)
4. Content gathering (gather / search)
5. Content synthesis (compose) — with self-review loop
6. Output generation (gen-*) — with auditor gate
7. Delivery summary

Each step's output MUST be checked before proceeding. If a step produces empty or garbage output, retry (max 2) before moving on with an honest report.

---

## RULE-5: State Persistence

After each significant step, update `tmp/session_state.json` with:
- `current_step`: which pipeline step is active
- `steps_completed`: list of completed steps with timestamps
- `gathered_content_summary`: brief summary of what was gathered (after gather/search)
- `requirements_list`: structured requirements extracted from user prompt (after intent analysis)

This enables session resume if Copilot session is interrupted.

---

## RULE-6: Requirement Anchoring

Immediately after intent analysis, extract a structured requirements list from the user's prompt:
```yaml
requirements:
  - id: R1
    description: "<what user wants>"
    priority: high | medium | low
```

This list is the **ground truth** for every auditor call. Auditor scores each requirement individually.
A step cannot proceed if any HIGH-priority requirement scores <60/100.

---

## RULE-7: Jargon Shield

User-facing messages MUST NOT contain:
- Technical tool names: "Playwright", "httpx", "BeautifulSoup", "markitdown"
- HTTP codes: "403", "429", "200"
- Developer jargon: "DOM", "endpoint", "crawler", "seed query", "Cloudflare bypass"

Use instead: "trình duyệt đặc biệt", "không truy cập được", "đang tìm kiếm", "nguồn chính / nguồn dự phòng".

---

## RULE-8: Honest Failure Reporting

When something fails:
- State clearly what failed and why (in user-friendly language)
- State what was achieved despite the failure (partial results)
- Suggest concrete next steps the user can take
- NEVER fabricate data, URLs, or statistics to fill gaps
- NEVER silently skip a failed step — always report it

---

## RULE-9: Agent-Centric Hard-Flow (US-16.3.1)

The canonical agent-level execution order for every pipeline run is **non-negotiable
law**. Every session MUST follow this exact sequence — no skipping, no reordering,
no optional steps:

```
Orchestrator
   │ MUST classify intent and route
   ▼
State + Checklist update (immediate)
   │ MUST persist raw_prompt, intent, requirements before any other agent runs
   ▼
Strategist
   │ MUST produce a workflow plan (initial_plan mode) before execution begins
   ▼
Execution Agent
   │ MUST own tool selection, probe availability, run the cascade per step
   ▼
Auditor
   │ MUST score the output against requirements (>80/100 to pass)
   │
   ├─ PASS  ───► Notify user (deliver result)
   │
   └─ FAIL  ───► Advisory  ──► new plan ──► Execution Agent retry
                  │                              │
                  │                              ▼
                  └────────────────────► Auditor (re-score)
```

### Per-Step MUST Statements

```yaml
ORCHESTRATOR:
  MUST: classify intent (synthesis | creation | research | design | data_collection | mixed | unknown)
  MUST: route to the appropriate skill cluster
  MUST: invoke State + Checklist update IMMEDIATELY after classification
  MUST_NOT: invoke any execution skill before Strategist returns a plan

STATE_AND_CHECKLIST_UPDATE:
  MUST: write raw_prompt, intent, structured requirements to tmp/session_state.json (RULE-5)
  MUST: occur BEFORE Strategist is called
  MUST_NOT: be skipped under any pivot or recovery path

STRATEGIST:
  MUST: produce a workflow plan in initial_plan mode for new sessions
  MUST: produce a workflow plan in replan mode after auditor FAIL + advisory output
  MUST: produce a child_workflow plan when called by Execution Agent (US-16.2.2)
  MUST_NOT: execute steps itself — planning only

EXECUTION_AGENT:
  MUST: own tool selection per step, probe availability, run cascade in order
  MUST: emit quality_signal (confidence + suggested_audit) with every result
  MUST: escalate to Strategist (CHILD_WORKFLOW) or Advisory per US-16.2.2 thresholds
  MUST_NOT: retry the same tool with the same args after failure
  MUST_NOT: skip the Auditor handoff when suggested_audit=true

AUDITOR:
  MUST: score every delivery step against the requirements anchor (RULE-6)
  MUST: return PASS only when score > 80/100
  MUST: emit explicit gap report on FAIL (which requirements unmet, with evidence)
  MUST_NOT: be bypassed by any skill or other agent

ADVISORY (only invoked on Auditor FAIL or wrong-angle suspicion):
  MUST: return 2–3 alternative approaches with rationale and confidence
  MUST: respect the 2-call session budget
  MUST_NOT: re-suggest an approach already attempted in this session

RETRY_AFTER_ADVISORY:
  MUST: feed Advisory's recommendation back to Strategist (replan mode) before retry
  MUST: NOT retry the same approach that just failed
  MUST: re-enter the loop at Execution Agent with the new plan
  MUST: respect max_retries = 2 (per RULE-2 pivot budget)
```

### Child Soft-Flow Trigger (Hard Rule)

A **child soft-flow** is the ONLY mechanism by which a single parent step may
spawn sub-steps mid-execution. It is triggered exclusively by the Execution
Agent under the conditions specified in `.github/agents/references/child-soft-flow.md`:

```yaml
TRIGGER (any one suffices):
  - Execution Agent's tool cascade is exhausted (>=3 tools tried, no success)
  - 2+ consecutive attempts returned quality_signal.confidence = "low"
  - parent_context.complexity_hint == "high" AND first attempt failed

INVOCATION:
  MUST: call Strategist in CHILD_WORKFLOW_MODE (decompose) OR Advisory (re-angle)
  MUST: pick at most ONE escalation path per parent step
  MUST: keep child state isolated (in-memory only — never written to state file)
  MUST: limit recursion to one level (a child step that fails escalates upward)
  MUST_NOT: be triggered proactively by any agent other than Execution

REPORTING:
  MUST: return only the consolidated child result to the parent step
  MUST: set quality_signal.suggested_audit = true (Auditor verifies child output)
```

### Failure Handling (Hard Rule)

```yaml
ON_AUDITOR_FAIL:
  step_1: MUST call Advisory with the failure context
  step_2: MUST feed Advisory's recommendation to Strategist (replan mode)
  step_3: MUST re-execute via Execution Agent with the NEW plan
  step_4: MUST re-score via Auditor

  budget: MUST NOT exceed 2 replan cycles per delivery step (RULE-2)
  on_budget_exhaustion: MUST deliver partial result with explicit gap report (RULE-8)
  MUST_NOT: retry with the same approach that just failed (RULE-2 pivot rule)
```

> Concrete trigger thresholds, request formats, and per-step budget caps for
> auditor-driven re-planning are documented in
> [`.github/agents/references/adaptive-replanning.md`](../agents/references/adaptive-replanning.md)
> (US-16.4.1). Cascade-exhaustion (pre-Auditor) replan is documented in
> [`.github/agents/references/child-soft-flow.md`](../agents/references/child-soft-flow.md)
> (US-16.2.2). A single failed step uses AT MOST one of the two paths.

### What This Rule Replaces

This rule does NOT remove or modify RULE-1 through RULE-8. It adds the
**agent-level** hard-flow on top of the **skill-level** hard-flow already
declared in RULE-4. Where the two interact: RULE-4 governs which skills run in
what order; RULE-9 governs which agents own each transition between skills.

---

## RULE-10: Orchestrator-Exclusive User Channel (US-17.1.1)

Only the `orchestrator` agent may emit user-facing messages, questions, or status updates.
All other skills and agents MUST return output internally to the orchestrator — never to the user.

### MUST

- `orchestrator` is the SOLE agent that sends messages to the user
- All skill output (search, gather, compose, gen-*, design, verify) goes to orchestrator as internal return
- All non-orchestrator agent output (strategist, execution, auditor, advisory) goes to orchestrator as internal return
- Orchestrator validates and formats all user-facing output before emission

### MUST_NOT

- Skills MUST NOT print final results directly to the user
- Skills MUST NOT ask the user questions
- Skills MUST NOT emit delivery summaries
- Non-orchestrator agents MUST NOT emit user-facing messages
- No agent except orchestrator may call `vscode_askQuestions` or equivalent

### Emission Types

The orchestrator gates three types of user-facing emissions:

| Type | Precondition | Example |
|------|-------------|---------|
| `result_delivery` | Auditor PASS (score ≥ 80/100) | Final output files + summary |
| `user_question` | RULE-11 consultation protocol satisfied | Content ambiguity question |
| `status_update` | Pipeline step boundary | Progress messages |

### Enforcement

If a non-orchestrator skill/agent attempts to emit user-facing output:
- Orchestrator intercepts and reformats through jargon shield (RULE-7)
- Incident logged to `tmp/session_state.json` under `rule_violations[]`

---

## RULE-11: (Reserved — see US-17.2.1)

---

## RULE-12: Script Placement Discipline (US-17.3.1)

One-time scripts and reusable utilities MUST live in separate directories.
This prevents pipeline-generated throwaway scripts from polluting the repo.

### Definitions

| Type | Definition | Location |
|------|-----------|----------|
| **One-time script** | Created for a single pipeline run — session-specific paths, single-use logic, hardcoded run data | `/tmp/scripts/` |
| **Reusable utility** | Invoked by 2+ pipeline runs OR 2+ skills — generic, parameterized, no session state | `/scripts/` |

### MUST

- Any skill creating a script MUST classify it as one-time or reusable
- One-time scripts MUST live in `/tmp/scripts/` (gitignored)
- Reusable scripts MUST live in `/scripts/` (committed to repo)
- `scripts/validate_script_placement.py` is the runtime enforcer — invoked by orchestrator at pipeline start AND after every step

### MUST_NOT

- One-time scripts MUST NOT be placed in `/scripts/`
- One-time scripts MUST NOT be committed to git
- Reusable utilities MUST NOT be placed in `/tmp/`

### Classification Heuristics

A script is **one-time** if ANY of these apply:
- Contains a hardcoded `session_id` or run-specific path
- References files from the current pipeline run (e.g., `tmp/data_processed.json`)
- Has no CLI parameter interface (hardcoded inputs)
- Was generated to solve a single pipeline step

A script is **reusable** if ALL of these apply:
- Accepts CLI arguments for all inputs
- Contains no session-specific data
- Is useful across multiple pipeline runs
- Follows existing `/scripts/` conventions

### Enforcement Chain

```
Skill creates script
  → Classifies: one-time or reusable
  → Places in /tmp/scripts/ or /scripts/ accordingly
  → validate_script_placement.py runs (orchestrator calls after each step)
  → If misplaced: validator MOVES file to correct location + logs
  → .gitignore blocks /tmp/ from commits
  → Pre-commit check catches any leaks
```

---

*These rules are loaded at maximum priority. SKILL.md files and agent instructions operate within these constraints.*
