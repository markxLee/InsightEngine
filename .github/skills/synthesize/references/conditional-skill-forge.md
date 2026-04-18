# Conditional Skill-Forge Runtime

> Create new skills at runtime ONLY when absolutely required.  
> Advisory agent must approve. 30-minute budget cap.  
> Created skills follow InsightEngine conventions and are tested before use.

---

## Overview

```yaml
PURPOSE:
  Sometimes a user's request requires a capability that no existing skill
  provides. Rather than failing, the pipeline can create a new skill at
  runtime — but ONLY when the advisory agent confirms it's truly needed.

PRINCIPLE:
  Skill creation is EXPENSIVE (time, tokens, complexity).
  Default behavior: use existing skills + inline instructions.
  Forge only when there is NO existing skill that can handle the task.

BUDGET:
  max_time: 30 minutes (wall-clock)
  max_agent_calls: 5 (for creation + testing)
  counted_against: pipeline's 30-call budget
```

---

## Decision Flow

```yaml
DECISION_FLOW:
  1_detect_gap:
    trigger: Strategist cannot map a workflow step to any existing skill
    signal: step.skill == null OR step.skill == "unknown"
    
  2_evaluate_alternatives:
    before_forging: |
      Can an existing skill handle this with modified instructions?
      Can inline code/script solve this without a full skill?
      
    alternatives:
      - bien-soan with custom instructions → covers most text tasks
      - thu-thap with specific search terms → covers most research
      - Inline Python script in /scripts → covers data transforms
      - tao-html with custom template → covers web output
      
  3_advisory_decision:
    call: advisory agent (1 call)
    question: |
      The user's request requires: {capability_description}
      Existing skills cannot handle this because: {gap_reason}
      Alternatives considered: {alternatives_list}
      
      Decision needed: Should we create a new skill or use an alternative?
    
    severity: moderate (advisory evaluates, no user prompt)
    
    possible_outcomes:
      NOT_NEEDED:
        action: Use alternative approach (advisory specifies which)
        log: decisions array → "skill_forge_skipped: {reason}"
        
      APPROVED:
        action: Proceed to skill creation
        log: decisions array → "skill_forge_approved: {capability}"
        budget_start: NOW (30-minute countdown)
```

---

## Skill Creation Protocol

```yaml
CREATION_STEPS:
  precondition: Advisory approved skill creation
  
  1_define_skill:
    name: Vietnamese, lowercase, hyphenated (e.g., "xu-ly-audio")
    purpose: One-line description
    triggers: 3-5 trigger phrases (Vietnamese primary, English secondary)
    location: .github/skills/<skill-name>/
    
  2_create_skill_structure:
    files:
      SKILL.md: |
        Follow InsightEngine skill conventions:
        - YAML frontmatter (name, description, version, compatibility)
        - English instructions body
        - References section (if needed)
        - Integration with shared context protocol
        
      scripts/<script>.py: |
        If skill needs a script:
        - Accept CLI arguments (no hardcoded paths)
        - Print output path + size as last line
        - Comments in English
        
      references/<ref>.md: |
        If skill needs reference docs
        
  3_conventions_check:
    verify:
      - Vietnamese skill name ✓
      - Scripts in /scripts (not tmp/) ✓
      - Output to /output ✓
      - CLI arguments (no hardcoded paths) ✓
      - Bilingual triggers ✓
      - SKILL.md in English ✓
      - Integrates with shared context protocol ✓
      
  4_test_skill:
    method: |
      Execute the skill with a minimal test case:
      - Provide sample input matching the user's actual request
      - Verify output is produced correctly
      - Verify file placement rules followed
      - Verify shared context updated properly
    
    pass_criteria:
      - Skill produces expected output type
      - No errors during execution
      - Files in correct locations
      
    on_fail:
      retry: 1 attempt with fix
      if_still_fails: |
        Abandon skill creation
        Fall back to inline approach
        Log: "skill_forge_failed: {error}"
        
  5_register_skill:
    action: |
      NOTE: Do NOT modify copilot-instructions.md or tong-hop SKILL.md
      during pipeline runtime. The created skill is used inline for
      this pipeline run only. Registration for future use is a
      post-pipeline task.
    
    runtime_use:
      - Strategist updates workflow to reference new skill
      - Pipeline executes new skill as a regular step
```

---

## Budget Enforcement

```yaml
BUDGET_TRACKING:
  time_budget:
    start: Moment advisory approves
    limit: 30 minutes
    check_at: After each creation step
    on_exceed: |
      STOP creation immediately
      Use best available alternative
      Log: "skill_forge_timeout: {elapsed_minutes}min"
      
  call_budget:
    allocated: 5 agent calls for skill creation
    breakdown:
      - 1 call: advisory decision (already spent)
      - 1 call: skill definition + SKILL.md creation
      - 1 call: script creation (if needed)
      - 1 call: testing
      - 1 call: fix + retest (if needed)
    on_exceed: |
      STOP creation
      Use inline approach
      Log: "skill_forge_budget_exceeded"
      
  pipeline_budget_impact:
    total_pipeline_budget: 30 agent calls
    skill_forge_uses: up to 5 of those 30
    remaining_for_pipeline: 25 minimum
    
    IF pipeline_calls_used > 20 BEFORE forge triggered:
      REJECT forge request (not enough budget)
      Use alternative approach
```

---

## Shared Context Integration

```yaml
CONTEXT_WRITES:
  on_advisory_decision:
    decisions[]:
      type: "skill_forge"
      action: "approved | skipped"
      capability: "description"
      reason: "why approved or skipped"
      timestamp: ISO-8601
      
  on_creation_complete:
    decisions[]:
      type: "skill_forge_result"
      skill_name: "name"
      location: "path"
      test_result: "pass | fail"
      time_elapsed: "Xmin"
      calls_used: N
      
  on_creation_failed:
    decisions[]:
      type: "skill_forge_failed"
      reason: "error description"
      fallback: "what was used instead"
```

---

## Examples

### Example 1: Forge Skipped (Alternative Available)

```yaml
scenario: User wants audio transcription
gap: No audio skill exists
advisory_evaluation:
  alternatives:
    - "Use inline Python with whisper library"
    - "Use thu-thap to read audio file via markitdown"
  decision: NOT_NEEDED
  reason: "markitdown supports audio → use thu-thap with audio mode"
result: No skill created, thu-thap handles it
```

### Example 2: Forge Approved and Successful

```yaml
scenario: User wants interactive web dashboard (not static HTML)
gap: tao-html only does static pages, no interactive dashboards
advisory_evaluation:
  alternatives:
    - "tao-html with JavaScript inline" → too complex, unreliable
    - "Inline streamlit script" → requires running server
  decision: APPROVED
  reason: "No existing skill can produce interactive dashboards reliably"
  
creation:
  name: "tao-dashboard"
  script: scripts/gen_dashboard.py (uses plotly + dash)
  test: Generated sample dashboard, opens in browser
  result: pass
  time: 12 minutes
  calls: 3
  
pipeline_continues: Uses tao-dashboard for this request
```

### Example 3: Forge Failed, Fallback Used

```yaml
scenario: User wants 3D visualization
gap: No 3D rendering skill
advisory: APPROVED
creation_attempt: Script uses three.js but test fails (complex setup)
retry: Still fails (WebGL dependency issues)
fallback: Use tao-hinh to generate 2D charts + note to user
log: "skill_forge_failed: 3D rendering too complex for runtime creation"
```
