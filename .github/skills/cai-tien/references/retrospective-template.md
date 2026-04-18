# Retrospective Template — Structured Analysis Format

> Standard template for analyzing InsightEngine sessions.  
> Ensures consistent, actionable retrospective output.

---

## Session Evidence Gathering

```yaml
EVIDENCE_TEMPLATE:
  session_info:
    date: ISO-8601
    user_request: "[original prompt]"
    pipeline_steps_executed: ["thu-thap", "bien-soan", "tao-word"]
    output_files: ["output/report.docx"]
    session_state: "[from tmp/.session-state.json if available]"

  quality_metrics:
    overall_satisfaction: 1-5  # 1=terrible, 5=excellent
    content_depth: thin | adequate | rich
    format_quality: poor | acceptable | professional
    accuracy: low | medium | high
    time_taken: fast (<5min) | normal (5-15min) | slow (>15min)

  failure_points:
    - step: "[which skill/step]"
      issue: "[what went wrong]"
      impact: low | medium | high
      root_cause: "[why it happened]"
```

---

## Root Cause Analysis (5 Whys)

```yaml
FIVE_WHYS_TEMPLATE:
  symptom: "[What the user observed]"
  why_1: "[First-level cause]"
  why_2: "[Deeper cause behind why_1]"
  why_3: "[Structural cause behind why_2]"
  why_4: "[System-level cause]"
  why_5: "[Root cause — the thing to fix]"
  
  root_cause_category:
    - skill_gap: Skill lacks capability for this case
    - instruction_gap: Instructions unclear or incomplete
    - data_gap: Insufficient source data gathered
    - quality_gate_gap: Quality check didn't catch the issue
    - pipeline_gap: Orchestration routing error
    - tool_limitation: External tool limitation (API, library)
```

---

## Improvement Recommendations

```yaml
RECOMMENDATION_TEMPLATE:
  improvements:
    - id: IMP-001
      category: skill | pipeline | instruction | quality_gate
      target: "[skill name or pipeline step]"
      priority: critical | high | medium | low
      description: "[What to change]"
      rationale: "[Why this prevents recurrence]"
      effort: trivial | small | medium | large
      action_type: edit_skill | add_reference | add_script | new_skill | pipeline_change

  action_plan:
    immediate: ["IMP-XXX — quick fixes to apply now"]
    next_session: ["IMP-XXX — improvements for next run"]
    backlog: ["IMP-XXX — larger changes for later"]
```

---

## Improvement Tracking

```yaml
TRACKING:
  location: output/session-summary.md (append retrospective entry)
  
  entry_format: |
    ### Retrospective — {date}
    **Request:** {user_request_summary}
    **Score:** {satisfaction}/5
    **Root cause:** {root_cause_category}: {root_cause_description}
    **Improvements applied:** {list of IMP-XXX applied}
    **Improvements deferred:** {list of IMP-XXX for later}
```
