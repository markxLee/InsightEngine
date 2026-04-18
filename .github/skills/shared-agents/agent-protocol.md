# Agent Calling Protocol — InsightEngine

> **Version:** 2.0 (Phase 9 — VS Code Custom Agent Standard)
> **Purpose:** Standardized input/output format, budget enforcement, and calling conventions for all agents.
> **Applies to:** All agents in `.github/agents/` and any skill that interacts with them.

---

## Architecture Overview

```yaml
AGENTS:   # Located in .github/agents/*.agent.md (VS Code custom agent standard)
  dieu-phoi:
    file: .github/agents/dieu-phoi.agent.md
    purpose: Central orchestrator — classifies intent, routes to skills/agents
    user-invocable: true

  auditor:
    file: .github/agents/auditor.agent.md
    purpose: Quality verification — 100-point weighted scoring
    budget: max 5 calls per pipeline run
    user-invocable: true

  strategist:
    file: .github/agents/strategist.agent.md
    purpose: Workflow generation — execution plan
    budget: max 1 call per pipeline run
    user-invocable: false

  advisory:
    file: .github/agents/advisory.agent.md
    purpose: Multi-perspective decision support
    budget: max 2 calls per pipeline run
    user-invocable: false

TOTAL_BUDGET: max 8 agent calls per pipeline run (excluding dieu-phoi)
```

---

## Standard Calling Convention

Every shared agent call follows this 4-step pattern:

```yaml
CALLING_PATTERN:
  step_1_read:
    action: READ the agent's .md file from shared-agents/
    why: Contains the prompt template with {variables} to fill
    
  step_2_build:
    action: BUILD the prompt by filling all {variable} placeholders
    rules:
      - Fill ALL required variables (agent-specific)
      - Use actual content, not placeholders like "see above"
      - Truncate output_content to ~3000 chars if very long (keep structure)
      - Include the full prompt template text with variables replaced
    
  step_3_call:
    action: CALL runSubagent(prompt=<built_prompt>, description=<short_desc>)
    rules:
      - description should be 3-5 words (e.g., "Audit Word output")
      - prompt is the ENTIRE filled template from the agent .md file
      - Do NOT add extra instructions outside the template
    
  step_4_parse:
    action: PARSE the structured response
    rules:
      - Each agent returns a specific response format (see below)
      - Extract verdict/plan/recommendation from the response
      - Act on the result according to agent-specific logic
```

---

## Agent Input/Output Formats

### Auditor

```yaml
INPUT_VARIABLES:
  user_request: string       # Original user request (verbatim or summarized)
  output_content: string     # Content to audit (file text or summary)
  output_format: string      # "word" | "excel" | "slides" | "pdf" | "html"
  required_fields: string    # Sections/topics user asked for

OUTPUT_FORMAT:
  verdict: PASS | FAIL
  score: 0-100
  issues: list of {category, severity, description, suggestion}
  summary: string

ON_RESULT:
  PASS: Deliver output to user
  FAIL: Re-generate with issues as improvement guidance (max 2 retries)
  FAIL_after_retries: Deliver with known-issues disclaimer
```

### Strategist

```yaml
INPUT_VARIABLES:
  user_request: string           # Original user request
  request_type: string           # "research" | "data_collection" | "mixed"
  content_depth: string          # "standard" | "comprehensive"
  output_formats: string         # Comma-separated: "word, slides"
  expanded_dimensions: string    # Prompt expansion results
  required_fields: string        # Key fields/sections
  context_window: string         # "basic" | "standard" | "advanced"
  reasoning_depth: string        # Model capability assessment
  tool_use: string               # Tool access description
  multilingual: string           # Language capabilities
  profile_source: string         # "self_declaration" | "fallback"

OUTPUT_FORMAT:
  selected_template: WF-XX
  workflow_steps: ordered list of {step_num, skill, action, quality_gate}
  quality_gates: list of checkpoints
  estimated_complexity: "low" | "medium" | "high"
  warnings: list of potential issues

ON_RESULT:
  Use workflow_steps as the execution plan
  Apply quality_gates at specified checkpoints
```

### Advisory

```yaml
INPUT_VARIABLES:
  decision_question: string    # The specific question to analyze
  context: string              # Relevant context for the decision
  options: string              # Known options (if any)
  constraints: string          # Constraints or requirements

OUTPUT_FORMAT:
  perspectives: list of {name, analysis, recommendation, confidence}
  consensus: string            # Overall recommendation
  confidence: 0.0-1.0
  rationale: string

ON_RESULT:
  confidence >= 0.7: Apply recommendation automatically
  confidence < 0.7:  Present to user for decision
```

---

## Budget Enforcement

```yaml
BUDGET_RULES:
  tracking:
    - Each pipeline run starts with fresh budget counters
    - Caller skill increments counter after each call
    - Counter is tracked in pipeline context (not persisted to file)
    
  enforcement:
    - Before calling: check if budget remaining > 0
    - If budget exhausted: skip agent call, use fallback logic
    - Log when budget is exhausted (inform user in pipeline summary)
    
  fallback_when_exhausted:
    auditor: Use inline self-verification (Step 4.5 in output skills)
    strategist: Use default workflow template (WF-01)
    advisory: Auto-decide based on best available context

  per_pipeline_limits:
    auditor: 5
    strategist: 1
    advisory: 2
    total: 8

BUDGET_ALLOCATION_GUIDANCE:
  typical_report_pipeline:
    strategist: 1 (at start)
    auditor: 2-3 (one per output format)
    advisory: 0-1 (if ambiguous decisions arise)
    
  complex_multi_format_pipeline:
    strategist: 1 (at start)
    auditor: 4-5 (one per format + retry)
    advisory: 1-2 (scope/depth decisions)
```

---

## Error Handling

```yaml
AGENT_ERRORS:
  timeout:
    symptom: runSubagent takes too long or returns empty
    action: Retry once, then skip with fallback
    
  malformed_response:
    symptom: Agent returns text that doesn't match expected format
    action: Extract what you can, treat as partial result
    
  unexpected_content:
    symptom: Agent returns content unrelated to the request
    action: Discard result, use fallback logic, log warning
    
  all_retries_failed:
    action: Continue pipeline without agent input, note in summary
```

---

## Caller Code Examples

### Calling Auditor from tao-word

```yaml
EXAMPLE_AUDITOR_CALL:
  1. READ .github/skills/shared-agents/auditor.md
  2. BUILD prompt:
     user_request: "Tạo báo cáo phân tích thị trường AI 2024"
     output_content: "<first 3000 chars of docx content via markitdown>"
     output_format: "word"
     required_fields: "market size, key players, trends, forecast, risks"
  3. CALL runSubagent(prompt=filled_template, description="Audit Word output")
  4. IF verdict == PASS → deliver
     IF verdict == FAIL → fix issues → retry (max 2)
```

### Calling Strategist from tong-hop

```yaml
EXAMPLE_STRATEGIST_CALL:
  1. READ .github/skills/shared-agents/strategist.md
  2. BUILD prompt:
     user_request: "Nghiên cứu so sánh framework frontend 2024, xuất Word + Slide"
     request_type: "research"
     content_depth: "comprehensive"
     output_formats: "word, slides"
     expanded_dimensions: "React, Vue, Angular, Svelte | performance, DX, ecosystem"
     required_fields: "comparison matrix, benchmarks, recommendations"
  3. CALL runSubagent(prompt=filled_template, description="Generate workflow plan")
  4. USE workflow_steps as pipeline execution plan
```

### Calling Advisory from any skill

```yaml
EXAMPLE_ADVISORY_CALL:
  1. CHECK severity: "Whether to escalate to Playwright" → moderate
  2. READ .github/skills/shared-agents/advisory.md
  3. BUILD prompt:
     decision_question: "Should we escalate URL fetching to Playwright?"
     context: "fetch_webpage returned 403 for 3/5 URLs. Site uses Cloudflare."
     options: "A) Retry with different headers B) Use Playwright stealth C) Skip these URLs"
     constraints: "Need data from at least 4/5 URLs for comprehensive report"
  4. CALL runSubagent(prompt=filled_template, description="Advise on URL fetching")
  5. IF confidence >= 0.7 → apply recommendation
     IF confidence < 0.7 → ask user
```

---

## Coexistence with Inline Logic

```yaml
MIGRATION_STATUS:
  shared_agents: Active and preferred
  inline_agents: Still exist in tong-hop/agents/ — deprecated
  
COEXISTENCE_RULES:
  - New skills MUST use shared-agents/
  - tong-hop will migrate to shared agents in US-8.4.2
  - Until migration: tong-hop may use either inline or shared
  - After migration: inline agents archived, shared agents canonical
  
SKILL_THAT_SHOULD_USE_SHARED:
  - tao-word → auditor (Step 5)
  - tao-excel → auditor (Step 5)
  - tao-slide → auditor (Step 5)
  - tao-pdf → auditor (Step 5)
  - tao-html → auditor (Step 5)
  - tong-hop → strategist, advisory, auditor (after US-8.4.2)
  - kiem-tra → may invoke auditor for automated checks
```
