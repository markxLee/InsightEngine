# Tiered Audit System — InsightEngine

> Apply the right level of quality scrutiny to each pipeline step.  
> 3 tiers: self-review (free) → agent audit (1 call) → final audit (1 call).

---

## Tier Overview

```yaml
AUDIT_TIERS:
  tier_1_self_review:
    cost: 0 agent calls (inline check)
    applied_to: ALL steps
    purpose: Quick sanity check — format, completeness, obvious errors
    who: The skill itself checks its own output before returning
    
  tier_2_agent_audit:
    cost: 1 agent call per step
    applied_to: CRITICAL steps only
    critical_steps:
      - bien-soan (content synthesis — #1 quality complaint area)
      - tao-word (final document — thin content check)
      - tao-slide (final presentation — thin content check)
      - tao-excel (formulas and data integrity)
    purpose: Deep quality check — depth, specificity, analysis quality
    who: Audit agent reviews output against criteria
    
  tier_3_final_audit:
    cost: 1 agent call total
    applied_to: Final output only (last step)
    purpose: Compare final deliverable against user's original request
    who: Audit agent compares output vs user_request from shared context
    
  BUDGET: Max 5 audit agent calls per pipeline run
```

---

## Tier 1: Self-Review (Inline)

Every step does a self-check before returning. No extra agent calls.

```yaml
SELF_REVIEW_CHECKS:
  thu-thap:
    - Content length > 500 chars (not empty/garbled)
    - All requested sources attempted
    - File format correctly read (not raw binary)
    
  bien-soan:
    - Output length meets depth target (comprehensive > 3000 words)
    - All sections from outline present
    - No placeholder text ("[TODO]", "[INSERT]")
    - No untranslated sections (for translation mode)
    
  tao-word:
    - File created and size > 10KB
    - All major sections present
    - No empty pages
    
  tao-excel:
    - File created and has data
    - Formulas present (no hardcoded calculations)
    - recalc.py executed
    
  tao-slide:
    - File created and size > 20KB
    - Slide count matches plan (±2)
    - No empty slides
    
  tao-pdf:
    - File created and size > 5KB
    - Content renders correctly
    
  tao-html:
    - File created and valid HTML
    - Styles applied
    
  ON_FAIL:
    action: Retry step with specific fix instructions
    max_retries: 2
    log: Append to audit_history with tier: "self_review"
```

---

## Tier 2: Agent Audit (Critical Steps)

One agent call to review quality deeply. Only for critical steps.

```yaml
AGENT_AUDIT_PROTOCOL:
  trigger: After self-review passes on critical steps
  
  input_to_audit:
    - Step output (content or file path)
    - User's original request (from shared context)
    - Content depth target (from shared context)
    - Quality criteria (per step type)
    
  audit_criteria:
    bien-soan:
      - Depth score (0-100): Is content expert-level or surface-level?
      - Specificity score (0-100): Are there specific data, examples, numbers?
      - Analysis score (0-100): Is there original analysis or just regurgitation?
      - Coverage score (0-100): Are all dimensions from request expansion covered?
      - PASS threshold: average ≥ 70
      
    tao-word:
      - Completeness (0-100): All sections present with content?
      - Formatting (0-100): Professional appearance, consistent styles?
      - Thin Content Flag: Any section < 100 words?
      - PASS threshold: completeness ≥ 80, no thin sections
      
    tao-slide:
      - Content per slide: Each slide has meaningful content?
      - Visual elements: Charts, icons, or images present?
      - Thin Content Flag: Any slide with only a title?
      - PASS threshold: no empty slides, avg content score ≥ 70
      
    tao-excel:
      - Formula integrity: All formulas resolve? No #REF!, #DIV/0!?
      - Data completeness: Required fields all populated?
      - PASS threshold: 0 formula errors, ≥ 90% field completeness
  
  output_format:
    result: pass | fail | warning
    score: number (0-100)
    issues: ["specific issue description"]
    action: proceed | retry_with_instructions
    retry_instructions: "specific guidance for improvement"
    
  ON_FAIL:
    action: Re-execute step with retry_instructions
    max_retries: 2
    escalation: If fails after 2 retries → deliver best available + quality note
    log: Append to audit_history with tier: "agent_audit"
```

---

## Tier 3: Final Audit

One agent call at the very end to compare output against original request.

```yaml
FINAL_AUDIT_PROTOCOL:
  trigger: After last output step completes
  
  input_to_audit:
    - Final output file(s)
    - user_request.original_text (from shared context)
    - user_request.expanded_dimensions (from shared context)
    - user_request.required_fields (if data_collection)
    - All prior audit_history entries
    
  checks:
    requirement_coverage:
      - Every dimension from request expansion addressed?
      - Required output format(s) generated?
      - Required fields present? (for data_collection)
      
    quality_consistency:
      - Overall quality score (average of all tier 2 audits)
      - Any step had to retry 2+ times? (quality risk flag)
      
    deliverable_check:
      - Output file exists in /output directory?
      - File size reasonable for content type?
      - File opens correctly? (format validation)
      
  output_format:
    overall_score: number (0-100)
    requirement_coverage: number (0-100)
    quality_grade: A (≥90) | B (≥75) | C (≥60) | D (<60)
    missing_requirements: ["what was asked but not delivered"]
    quality_warnings: ["potential issues"]
    recommendation: deliver | retry_step_X | add_content
    
  ON_FAIL:
    if recommendation == "retry_step_X":
      action: Re-execute specific step (not full pipeline)
      max_pipeline_retries: 3 total across all steps
    if recommendation == "deliver":
      action: Deliver with quality note to user
    log: Append to audit_history with tier: "final_audit"
```

---

## Budget Tracking

```yaml
AUDIT_BUDGET:
  max_audit_agent_calls: 5
  
  typical_distribution:
    tier_2_bien_soan: 1 call
    tier_2_output_skill: 1 call
    tier_3_final: 1 call
    retry_audits: 2 calls (reserve)
    
  budget_exceeded:
    action: Skip remaining audits, deliver best available
    log: "Audit budget exhausted — delivering without further quality checks"
    
  tracking:
    field: workflow.total_agent_calls (shared context)
    check_before_each_audit: total < max_agent_calls AND audit_calls < 5
```
