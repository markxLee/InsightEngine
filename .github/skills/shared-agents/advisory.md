# Shared Advisory Agent — Multi-Perspective Decision Support via `runSubagent`

> Standalone Copilot agent invocable from ANY skill via `runSubagent`.
> Receives a decision question + context → returns multi-perspective analysis + recommendation.
> Refactored from tong-hop/agents/advisory.md to be shared infrastructure.

---

## Invocation

```yaml
HOW_TO_CALL:
  1. READ this file (shared-agents/advisory.md)
  2. CHECK decision severity (trivial → auto-decide, no call needed)
  3. BUILD prompt from PROMPT_TEMPLATE below, filling variables
  4. CALL runSubagent with the built prompt
  5. PARSE the structured response → apply recommendation

BUDGET: Max 2 advisory calls per pipeline run
```

---

## Decision Severity Routing

```yaml
SEVERITY_ROUTING:
  trivial:
    examples:
      - Chart color selection
      - File naming convention
      - Template style when context is obvious
    action: Auto-decide WITHOUT calling advisory (0 calls)
    
  moderate:
    examples:
      - Which workflow template for ambiguous request
      - Whether to escalate search to Playwright
      - Whether output needs additional charts
      - Content depth when signals are mixed
    action: 1 advisory call → apply recommendation automatically
    
  critical:
    examples:
      - Whether to create a new runtime skill
      - Whether to restart pipeline vs retry a step
      - Major scope change mid-pipeline
    action: 1 advisory call → IF confidence < 0.7 present to user
```

---

## Prompt Template

Skills construct the `runSubagent` prompt by filling `{variables}`:

```
You are an expert decision advisor for InsightEngine content pipeline.

## Task
Analyze the following decision from multiple perspectives and provide
a clear, actionable recommendation. Do NOT ask for more information —
decide with what you have.

## Decision Question
{question}

## Context
- User's Original Request: {user_request}
- Current Pipeline State: {current_state}
- Prior Decisions: {prior_decisions}
- Severity: {severity}  (moderate | critical)

## Options
{options}

## Instructions
1. Analyze from 3-5 perspectives (User Intent, Technical Feasibility, Quality Impact, Resource Efficiency, Risk Assessment)
2. For each perspective: state analysis, recommend an option, give confidence 0.0-1.0
3. Synthesize into a single final recommendation
4. If all perspectives agree → high confidence
5. If perspectives disagree → explain trade-offs, recommend safest high-quality option

## Response Format (STRICT)

PERSPECTIVES:
1. User Intent: [analysis] → Option [X] (confidence: [0.0-1.0])
2. Technical Feasibility: [analysis] → Option [X] (confidence: [0.0-1.0])
3. Quality Impact: [analysis] → Option [X] (confidence: [0.0-1.0])
4. Resource Efficiency: [analysis] → Option [X] (confidence: [0.0-1.0])
5. Risk Assessment: [analysis] → Option [X] (confidence: [0.0-1.0])

RECOMMENDATION: Option [X]
CONFIDENCE: [0.0-1.0]
REASONING: [1-2 sentence justification]
ASK_USER: [yes/no — yes only if confidence < 0.7 AND severity is critical]
```

---

## Response Parsing

```yaml
PARSE_RESPONSE:
  recommendation: Extract "RECOMMENDATION: Option X"
  confidence: Extract "CONFIDENCE: N.N"
  ask_user: Extract "ASK_USER: yes/no"
  reasoning: Extract "REASONING: ..."
  
  ON_HIGH_CONFIDENCE (≥ 0.7):
    action: Apply recommendation automatically
    log: Add to pipeline decisions list
    
  ON_LOW_CONFIDENCE (< 0.7) + CRITICAL:
    action: Present recommendation to user in Vietnamese
    format: |
      🤔 **Cần xác nhận:**
      {reasoning in Vietnamese}
      Khuyến nghị: {recommendation}
      Đồng ý không?
    
  ON_BUDGET_EXCEEDED:
    action: Auto-decide using highest average confidence option
    note: Do NOT call advisory — decide inline
```

---

## Relationship to tong-hop

```yaml
MIGRATION_PATH:
  before_phase_8:
    - Advisory logic was inline in tong-hop/agents/advisory.md
    - Only tong-hop could request advisory analysis
    - Advisory was coupled to pipeline context
    
  after_phase_8:
    - Advisory is shared infrastructure (this file)
    - Any skill can call via runSubagent when facing ambiguous decisions
    - Caller provides whatever context is available
    - Works with or without full pipeline context
```
