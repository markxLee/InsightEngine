# Agent Context Schema — InsightEngine

> Shared context file for inter-agent communication.  
> Path: `tmp/.agent-context.json`

---

## Overview

All agents in the InsightEngine pipeline share state through a single JSON file.
This enables stateless subagents to communicate by reading context at the start
of their task and writing results at the end.

---

## Schema

```json
{
  "version": "1.0",
  "pipeline_id": "uuid-v4",
  "created_at": "ISO-8601",
  "updated_at": "ISO-8601",

  "user_request": {
    "original_text": "string — user's exact request",
    "language": "vi | en",
    "request_type": "research | data_collection | mixed",
    "content_depth": "standard | comprehensive",
    "output_formats": ["word", "excel", "slides", "pdf", "html"],
    "expanded_dimensions": {
      "core_question": "string",
      "subtopics": ["string"],
      "data_needs": ["string"],
      "analytical_angles": ["string"],
      "scope_boundaries": ["string"]
    },
    "required_fields": [
      {
        "field_name": "string",
        "description": "string",
        "required": true
      }
    ]
  },

  "model_profile": {
    "self_declared_name": "string | null",
    "capability_levels": {
      "context_window": "basic | standard | advanced",
      "reasoning_depth": "basic | standard | advanced",
      "tool_use": "basic | standard | advanced",
      "multilingual": "basic | standard | advanced",
      "code_generation": "basic | standard | advanced"
    },
    "profile_source": "self_declaration | decision_map | fallback",
    "detected_at": "ISO-8601"
  },

  "workflow": {
    "template_used": "string | null",
    "steps": [
      {
        "step_id": "string",
        "skill": "thu-thap | bien-soan | tao-word | ...",
        "status": "pending | running | completed | failed | skipped",
        "started_at": "ISO-8601 | null",
        "completed_at": "ISO-8601 | null",
        "output_files": ["string"],
        "quality_score": "number | null",
        "retries": 0
      }
    ],
    "current_step_index": 0,
    "total_agent_calls": 0,
    "max_agent_calls": 30
  },

  "audit_history": [
    {
      "step_id": "string",
      "tier": "self_review | agent_audit | final_audit",
      "timestamp": "ISO-8601",
      "result": "pass | fail | warning",
      "score": "number (0-100)",
      "issues": ["string"],
      "action_taken": "proceed | retry | rollback"
    }
  ],

  "decisions": [
    {
      "question": "string",
      "decided_by": "auto | advisory | user",
      "decision": "string",
      "reasoning": "string",
      "timestamp": "ISO-8601",
      "perspectives": [
        {
          "name": "string",
          "recommendation": "string",
          "confidence": "number (0-1)"
        }
      ]
    }
  ],

  "escalation_log": [
    {
      "skill": "string",
      "tool_tried": "string",
      "result": "success | failure",
      "next_tier": "string | null",
      "timestamp": "ISO-8601"
    }
  ]
}
```

---

## Field Descriptions

### `user_request`
Captured once at pipeline start (Step 1 + Step 1.5). Immutable after initial capture.
All agents read this to understand the user's intent.

### `model_profile`
Detected at pipeline start via self-declaration + decision map verification.
Used by strategist to choose workflow, by audit to set quality thresholds.

### `workflow`
Dynamic — updated by the strategist (initial plan) and by each agent (step status).
The `current_step_index` tracks pipeline progress for resume capability.

### `audit_history`
Append-only log of all quality checks. Used by final audit to assess overall quality
and by the advisory agent to understand quality trends.

### `decisions`
Append-only log of all decisions made during pipeline. Provides audit trail and
helps advisory agent avoid asking the same question twice.

### `escalation_log`
Append-only log of tool escalations. Helps diagnose recurring failures.

---

## Write Protocol

```yaml
WRITE_RULES:
  atomic_write: true
  method: |
    1. Read current file
    2. Modify in-memory
    3. Write to tmp/.agent-context.json.tmp
    4. Rename tmp/.agent-context.json.tmp → tmp/.agent-context.json
  
  concurrent_access: Sequential execution (agents don't run in parallel)
  
  append_only_fields:
    - audit_history
    - decisions
    - escalation_log
  
  mutable_fields:
    - workflow.steps[].status
    - workflow.current_step_index
    - workflow.total_agent_calls
    - model_profile (only at startup)
    - updated_at
```

---

## Initialization

At pipeline start (tong-hop Step 0), create the context file:

```python
import json, uuid
from datetime import datetime

context = {
    "version": "1.0",
    "pipeline_id": str(uuid.uuid4()),
    "created_at": datetime.now().isoformat(),
    "updated_at": datetime.now().isoformat(),
    "user_request": {},
    "model_profile": {},
    "workflow": {"steps": [], "current_step_index": 0, "total_agent_calls": 0, "max_agent_calls": 30},
    "audit_history": [],
    "decisions": [],
    "escalation_log": []
}

with open("tmp/.agent-context.json", "w", encoding="utf-8") as f:
    json.dump(context, f, ensure_ascii=False, indent=2)
```
