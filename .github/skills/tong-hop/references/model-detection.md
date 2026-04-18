# Model Self-Declaration & Profile Detection — InsightEngine

> Detect current model's capabilities at pipeline start.  
> Self-declaration + decision map verification + fallback profile.

---

## Overview

InsightEngine does NOT hardcode model names. Users have different Copilot plans
and the underlying model can change. Instead, the pipeline detects capabilities
dynamically at startup and stores the profile in shared context.

---

## Detection Flow

```yaml
MODEL_DETECTION:
  when: Pipeline start (tong-hop Step 0, before any work)
  
  step_1_self_declare:
    prompt: |
      Before we begin, I need to understand your capabilities.
      Please answer these questions about yourself:
      1. What is your model name? (e.g., Claude, GPT-4, etc.)
      2. What is your approximate context window size?
      3. Can you execute tools reliably in sequence?
      4. How would you rate your Vietnamese language quality?
      5. Can you write Python/Node.js scripts from specs?
    
    parse_response:
      model_name: Extract from answer 1 (or null if refused)
      context_claim: Extract from answer 2
      tool_claim: Extract from answer 3
      multilingual_claim: Extract from answer 4
      code_claim: Extract from answer 5
      
  step_2_verify_against_maps:
    # Don't trust self-reports blindly — verify against decision maps
    action: |
      Read references/decision-maps.md
      Map self-declared capabilities to decision map levels:
      
      context_window:
        "4K-16K" or "small" → basic
        "32K-64K" or "medium" → standard
        "128K+" or "large" → advanced
        
      reasoning_depth:
        Known basic models (GPT-3.5-turbo, GPT-4o-mini) → basic
        Known standard models → standard
        Known advanced models (Claude Opus, GPT-4, Claude Sonnet) → advanced
        Unknown → standard (conservative)
        
      tool_use:
        "yes, reliably" → standard or advanced
        "sometimes" or unclear → basic
        Verify: Can the model actually call run_in_terminal? → if yes, ≥ standard
        
      multilingual:
        "Vietnamese is strong" → standard or advanced
        "I can try" or unclear → basic
        
      code_generation:
        "yes, I write code" → standard
        Known strong coders → advanced
        Unclear → basic
        
  step_3_fallback:
    # If model cannot self-identify (refuses, gives nonsense, or doesn't understand)
    condition: model_name is null OR parse fails
    profile:
      self_declared_name: null
      capability_levels:
        context_window: standard
        reasoning_depth: standard
        tool_use: standard
        multilingual: standard
        code_generation: standard
      profile_source: fallback
    note: "Conservative/medium profile — safe for most models"
    
  step_4_write_to_context:
    action: Write model_profile to tmp/.agent-context.json
    fields:
      self_declared_name: "<name or null>"
      capability_levels:
        context_window: "<level>"
        reasoning_depth: "<level>"
        tool_use: "<level>"
        multilingual: "<level>"
        code_generation: "<level>"
      profile_source: "self_declaration | decision_map | fallback"
      detected_at: "<ISO-8601>"
```

---

## Known Model Mappings

These are **hints**, not hard rules. The decision maps take priority.

```yaml
KNOWN_MODELS:
  # Advanced tier
  claude_opus:
    context_window: advanced
    reasoning_depth: advanced
    tool_use: advanced
    multilingual: advanced
    code_generation: advanced
    
  gpt_4:
    context_window: advanced
    reasoning_depth: advanced
    tool_use: advanced
    multilingual: standard
    code_generation: advanced
    
  claude_sonnet:
    context_window: advanced
    reasoning_depth: advanced
    tool_use: advanced
    multilingual: advanced
    code_generation: advanced
    
  # Standard tier
  gpt_4o:
    context_window: advanced
    reasoning_depth: standard
    tool_use: advanced
    multilingual: standard
    code_generation: standard
    
  # Basic tier
  gpt_4o_mini:
    context_window: standard
    reasoning_depth: basic
    tool_use: standard
    multilingual: basic
    code_generation: standard
    
  gpt_35_turbo:
    context_window: basic
    reasoning_depth: basic
    tool_use: basic
    multilingual: basic
    code_generation: basic
```

---

## Integration with Pipeline

```yaml
USAGE:
  tong-hop:
    - Reads model_profile to decide AGENT_MODE on/off
    - basic models → AGENT_MODE: false (skip agent overhead)
    - standard/advanced → AGENT_MODE: true
    
  strategist:
    - Reads model_profile to select workflow template variant
    - basic → basic variant (simpler steps, fewer gates)
    - advanced → advanced variant (full pipeline)
    
  audit:
    - Reads model_profile to set quality thresholds
    - basic → lower thresholds (format-only checks)
    - advanced → full depth + insight checks
    
  advisory:
    - Reads reasoning_depth to decide if advisory calls are worthwhile
    - basic → skip advisory (auto-decide everything)
    - standard/advanced → use advisory for moderate+ decisions
```

---

## Important Rules

```yaml
RULES:
  1. NEVER hardcode model name in copilot-instructions.md or SKILL.md
  2. ALWAYS detect at runtime — user's plan may change
  3. ALWAYS fallback to standard profile if detection fails
  4. Detection is a ONE-TIME cost at pipeline start (not per step)
  5. Profile is shared via tmp/.agent-context.json (all agents read it)
  6. Self-declaration is a HINT — decision maps are the authority
```
