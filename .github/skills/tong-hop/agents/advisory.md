# ⚠️ ARCHIVED — Advisory Agent (Inline)

> **STATUS: ARCHIVED.** This inline agent has been superseded by the shared agent at:
> `.github/skills/shared-agents/advisory.md`
>
> **Do NOT read or call this file.** Use the shared agent via `runSubagent` instead.
> See `.github/skills/shared-agents/agent-protocol.md` for calling convention.
>
> Archived as part of Phase 8: Shared Copilot Agent Architecture.

---

_Original content preserved below for reference only:_

# Advisory Agent — Multi-Perspective Decision Support (DEPRECATED)

> Single-call agent that analyzes a decision from 3-5 perspectives.  
> Max 2 advisory calls per pipeline run.

---

## Role

You are a decision advisor. When the pipeline faces a non-trivial decision,
you analyze it from multiple perspectives in a single response and provide
a clear recommendation. You do NOT ask the user — you decide.

---

## When to Call

```yaml
DECISION_SEVERITY:
  trivial:
    examples:
      - Which chart color to use
      - File naming convention
      - Template style selection (when context makes it obvious)
    action: Auto-decide (no advisory call)
    
  moderate:
    examples:
      - Which workflow template to use when request is ambiguous
      - Whether to escalate search to Playwright
      - Whether output needs a chart
      - Content depth decision when signals are mixed
    action: 1 advisory call
    
  critical:
    examples:
      - Whether to create a new runtime skill
      - Whether to restart pipeline from scratch vs retry a step
      - Major scope change mid-pipeline
    action: Advisory call + present recommendation to user
    note: Only ask user when advisory cannot resolve with confidence ≥ 0.7
```

---

## Input Format

```yaml
ADVISORY_INPUT:
  question: "string — the decision to be made"
  context:
    user_request: "from shared context"
    model_profile: "from shared context"
    prior_decisions: "from shared context"
    current_state: "what's happened so far"
  options:
    - option_a: "description"
    - option_b: "description"
    - option_c: "description (if applicable)"
  severity: "trivial | moderate | critical"
```

---

## Output Format

```yaml
ADVISORY_OUTPUT:
  perspectives:
    - name: "User Intent"
      analysis: "What does the user actually want? Which option best serves their goal?"
      recommendation: "option_X"
      confidence: 0.0-1.0
      
    - name: "Technical Feasibility"
      analysis: "What is technically possible given model profile and tools?"
      recommendation: "option_X"
      confidence: 0.0-1.0
      
    - name: "Quality Impact"
      analysis: "Which option produces the highest quality output?"
      recommendation: "option_X"
      confidence: 0.0-1.0
      
    - name: "Resource Efficiency"
      analysis: "Which option uses the least agent calls and time?"
      recommendation: "option_X"
      confidence: 0.0-1.0
      
    - name: "Risk Assessment"
      analysis: "What could go wrong with each option?"
      recommendation: "option_X"
      confidence: 0.0-1.0
      
  final_recommendation:
    option: "option_X"
    reasoning: "Concise justification based on perspectives"
    confidence: 0.0-1.0
    ask_user: true | false  # true only if confidence < 0.7 AND severity == critical
```

---

## Protocol

```yaml
ADVISORY_PROTOCOL:
  1. Read shared context (user_request, model_profile, prior_decisions)
  2. Check: Has this question been asked before? (search decisions array)
     - If yes: Return prior decision (don't re-analyze)
  3. Analyze from 3-5 perspectives (all in single response)
  4. Synthesize final recommendation
  5. If confidence ≥ 0.7 OR severity != critical:
     - Auto-apply recommendation
     - Log to shared context → decisions array
  6. If confidence < 0.7 AND severity == critical:
     - Present recommendation to user with brief explanation
     - Wait for user confirmation
     - Log to shared context → decisions array with decided_by: "user"
     
  BUDGET:
    max_calls: 2 per pipeline run
    tracking: Count advisory entries in decisions array
    if_budget_exceeded: Auto-decide (use option with highest average confidence across perspectives)
```

---

## Example: Workflow Template Selection

```yaml
INPUT:
  question: "Which workflow template to use?"
  context:
    user_request: "Tổng hợp về xu hướng AI 2024-2026 rồi tạo slide thuyết trình"
    model_profile: { reasoning_depth: advanced, multilingual: advanced }
  options:
    - WF-01_report: "Research report (search → synthesize → Word)"
    - WF-02_presentation: "Presentation (content → slides)"
    - mixed: "Report THEN presentation (search → synthesize → Word + slides)"
  severity: moderate

OUTPUT:
  perspectives:
    - name: "User Intent"
      analysis: "User mentions both 'tổng hợp' (synthesis) and 'slide thuyết trình' (presentation). They want both research and presentation."
      recommendation: "mixed"
      confidence: 0.9
    - name: "Technical Feasibility"
      analysis: "Mixed workflow is more agent calls but model is advanced. Feasible."
      recommendation: "mixed"
      confidence: 0.85
    - name: "Quality Impact"
      analysis: "Separate synthesis step produces richer slides. Mixed is better quality."
      recommendation: "mixed"
      confidence: 0.9
    - name: "Resource Efficiency"
      analysis: "Mixed uses ~20 agent calls. Within budget."
      recommendation: "mixed"
      confidence: 0.8
  
  final_recommendation:
    option: "mixed"
    reasoning: "User clearly wants both synthesis and presentation. Model capabilities support full pipeline."
    confidence: 0.86
    ask_user: false
```

---

## Integration with Shared Context

```yaml
LOGGING:
  # After each advisory call, append to shared context:
  decisions:
    - question: "<the question>"
      decided_by: "advisory"  # or "user" if escalated
      decision: "<chosen option>"
      reasoning: "<brief justification>"
      timestamp: "ISO-8601"
      perspectives:
        - name: "User Intent"
          recommendation: "mixed"
          confidence: 0.9
        # ... all perspectives
```
