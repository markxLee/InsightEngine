# Agent Context Read/Write Protocol — InsightEngine

> Consistent protocol for agents to read and write shared context.  
> Every agent call: READ context first → do work → WRITE results last.

---

## Protocol Overview

```yaml
AGENT_LIFECYCLE:
  1_start:
    action: Read tmp/.agent-context.json
    purpose: Get user request, model profile, workflow state, prior decisions
    handle_missing: Create default context if file doesn't exist
    
  2_execute:
    action: Perform agent's task
    purpose: Use context to inform decisions and execution
    
  3_end:
    action: Write results to tmp/.agent-context.json
    purpose: Update workflow status, append audit/decision/escalation logs
    method: Atomic write (write to .tmp file, then rename)
```

---

## Read Protocol

At the start of every agent call, read the shared context:

```yaml
READ_PROTOCOL:
  file: tmp/.agent-context.json
  
  if_exists:
    action: Parse JSON, extract relevant sections
    validate:
      - version field exists and is "1.0"
      - user_request is populated
      - workflow.steps array exists
    on_invalid: Log warning, use what's available, don't crash
    
  if_missing:
    action: Create minimal context with defaults
    defaults:
      version: "1.0"
      pipeline_id: generate UUID
      user_request: {} (will be populated by first agent)
      model_profile: {} (will be populated by detection step)
      workflow:
        steps: []
        current_step_index: 0
        total_agent_calls: 0
        max_agent_calls: 30
      audit_history: []
      decisions: []
      escalation_log: []

  what_each_agent_reads:
    strategist:
      - user_request (full)
      - model_profile (full)
      - decisions (to avoid repeating)
    
    thu-thap:
      - user_request.request_type
      - user_request.required_fields
      - workflow.current_step_index
      - escalation_log (to know what's been tried)
    
    bien-soan:
      - user_request.content_depth
      - user_request.expanded_dimensions
      - audit_history (prior quality checks)
    
    audit:
      - user_request.original_text
      - workflow.steps (all)
      - audit_history (prior audits)
    
    advisory:
      - decisions (all prior)
      - user_request (full context)
      - model_profile (to calibrate advice)
```

---

## Write Protocol

At the end of every agent call, write results:

```yaml
WRITE_PROTOCOL:
  method: Atomic write
  steps:
    1. Read current tmp/.agent-context.json into memory
    2. Update relevant fields (see per-field rules below)
    3. Set updated_at to current ISO-8601 timestamp
    4. Increment workflow.total_agent_calls by 1
    5. Write to tmp/.agent-context.json.tmp
    6. Rename tmp/.agent-context.json.tmp → tmp/.agent-context.json

  per_field_rules:
    # APPEND-ONLY fields (never delete existing entries)
    audit_history: APPEND new audit entry
    decisions: APPEND new decision entry
    escalation_log: APPEND new escalation entry
    
    # MUTABLE fields (update in place)
    workflow.steps[i].status: Update current step status
    workflow.steps[i].completed_at: Set when step completes
    workflow.steps[i].output_files: Set after output generated
    workflow.steps[i].quality_score: Set after quality check
    workflow.steps[i].retries: Increment on retry
    workflow.current_step_index: Advance after step completion
    workflow.total_agent_calls: Increment each call
    updated_at: Always update
    
    # SET-ONCE fields (only write if empty)
    user_request: Set by tong-hop at pipeline start
    model_profile: Set by model detection at pipeline start
    workflow.template_used: Set by strategist

  budget_check:
    before_write: |
      if workflow.total_agent_calls >= workflow.max_agent_calls:
        STOP pipeline, deliver best available output
        Log: "Budget exhausted (max {max_agent_calls} agent calls)"
```

---

## Concurrent Access

```yaml
CONCURRENCY:
  model: Sequential execution
  reason: |
    Copilot agents don't run in parallel. Each agent call completes
    before the next one starts. No file locking needed.
  
  safety_net: |
    Even if somehow two agents ran concurrently:
    - Atomic write (tmp file + rename) prevents corruption
    - Append-only fields prevent data loss
    - SET-ONCE fields prevent overwrite
```

---

## Examples

### Agent reads context at start:

```yaml
# Copilot reads the file using read_file tool:
READ: tmp/.agent-context.json

# Extract what this agent needs:
user_request = context["user_request"]
model_profile = context["model_profile"]
current_step = context["workflow"]["steps"][context["workflow"]["current_step_index"]]
```

### Agent writes results at end:

```yaml
# After completing work, update context:
UPDATE:
  workflow.steps[2].status: "completed"
  workflow.steps[2].completed_at: "2026-04-18T10:30:00Z"
  workflow.steps[2].output_files: ["output/report.docx"]
  workflow.steps[2].quality_score: 85
  workflow.current_step_index: 3
  workflow.total_agent_calls: +1
  updated_at: "2026-04-18T10:30:00Z"
  
APPEND to audit_history:
  - step_id: "bien-soan"
    tier: "self_review"
    result: "pass"
    score: 85
    issues: []
    action_taken: "proceed"
```

### Budget exhaustion handling:

```yaml
CHECK: workflow.total_agent_calls >= workflow.max_agent_calls
IF TRUE:
  - Save current state
  - Deliver best available output
  - Report to user: "Pipeline hoàn tất (đạt giới hạn xử lý)."
```
