# Per-Step Audit Protocol (US-13.2.1)

> Reference for orchestrator.agent.md FLOW step 6c.
> Defines when and how to call the auditor after each pipeline step.

---

## When to Call Auditor

Call the auditor after **every step that produces output files or structured content**.

| Step | Trigger for auditor | What to check |
|------|---------------------|---------------|
| `gather` | After URL fetch / search round | Volume, source diversity, specificity |
| `compose` | After content synthesis | Coverage of content_requirements, depth |
| `gen-excel` | After .xlsx created | fields_required, grouping (sheet names), filters |
| `gen-word` | After .docx created | Section completeness, content_requirements |
| `gen-slide` | After .pptx created | Slide count, content per slide |
| `gen-html` | After .html created | Section coverage, link validity |
| `gen-pdf` | After .pdf created | Layout, completeness |

Skip auditor for: `save_state.py` commands, utility scripts, setup steps.

---

## Call Protocol

```yaml
AUDITOR_CALL_SPEC:
  required_inputs:
    - user_request: raw_prompt (from state)
    - output_content: summary of what was generated
    - output_format: excel | word | slide | pdf | html | text
    - structured_requirements: from `python3 scripts/save_state.py check-requirements`

  optional_inputs:
    - required_fields: comma list of expected data fields
    - previous_score: prior audit score for this step (if retry)
    - attempt_number: 1 | 2 | 3

  save_result:
    command: |
      python3 scripts/save_state.py update \
        --step <name> --status completed \
        --audit-score <score> \
        --req-scores '<json_array>'
```

---

## Pass/Fail Logic

```yaml
PASS_CONDITION:
  overall_score: >= 80
  per_requirement: ALL requirements scored >= 60

FAIL_ACTION:
  1. Log BLOCKING_FAILURES to step state
  2. Re-execute step targeting BLOCKING_FAILURES (max 2 retries)
  3. Pass previous_score + attempt_number to auditor on retries
  4. After 2 failed retries → invoke failure handling (see US-13.2.2)

RETRY_TARGETING:
  - Provide auditor's BLOCKING_FAILURES as explicit guidance to the step skill
  - Example: "gen-excel failed REQ-003 (correct sheet names). Retry with sheets named by province."
```

---

## Budget Management

```yaml
AUDITOR_BUDGET: 5 calls per pipeline run

PRIORITY_ORDER (if steps > 5):
  1. gen-excel        # most specific structural requirements
  2. gen-slide        # content completeness
  3. gen-word         # narrative coverage
  4. gen-html         # link validity
  5. compose          # only if content_requirements are complex

ALWAYS_CALL:
  - Last output step regardless of budget
  - Any step with structured_requirements.fields_required (field coverage is critical)

SKIP_IF_BUDGET_EXHAUSTED:
  - gather (unless data collection mode)
  - compose (if gen-* skills will verify content coverage)
```

---

## Output Format for `--req-scores`

```json
[
  {
    "req_id": "REQ-001",
    "req_category": "grouping",
    "req_description": "One sheet per province",
    "score": 100,
    "pass": true,
    "reason": "Found 63 sheets, one per province",
    "evidence": "Sheet names: 'Hà Nội', 'Hồ Chí Minh', ..."
  },
  {
    "req_id": "REQ-002",
    "req_category": "filters",
    "req_description": "Fresher level only",
    "score": 0,
    "pass": false,
    "reason": "2 rows contain 'Senior' in level column",
    "evidence": "Row 14: level='Senior', Row 38: level='Senior'"
  }
]
```

---

## Integration with synthesize/SKILL.md

Each gen-* skill step in synthesize should follow:

```yaml
STEP_PROTOCOL:
  1. Announce step start in Vietnamese: "Đang tạo file Excel..."
  2. Execute the gen-* skill
  3. Call auditor with structured_requirements (Phase 13 mandatory)
  4. If FAIL → retry with BLOCKING_FAILURES as guidance
  5. Save final audit result to state
  6. Announce completion: "✅ File Excel đã tạo: output/xxx.xlsx (45KB, score: 88/100)"
```
