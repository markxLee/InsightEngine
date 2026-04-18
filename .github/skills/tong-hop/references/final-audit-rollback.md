# Final Output Audit — Step-Level Rollback Protocol

> Compare final output against user's original request.  
> If audit fails, identify the failing step and re-execute from there (not from scratch).  
> Max 3 attempts per step, max 10 total retries, 30 agent-call budget cap.

---

## Overview

```yaml
FINAL_AUDIT_FLOW:
  trigger: After last output step completes (before delivering to user)
  
  1. EXTRACT user_request from shared context (tmp/.agent-context.json)
  2. COMPARE output against original request dimensions
  3. IF PASS → deliver output
  4. IF FAIL → identify failing step → rollback → re-execute from that step
  5. REPEAT until pass OR budget exhausted → deliver best available

BUDGET_CAPS:
  max_retries_per_step: 3
  max_total_retries: 10
  max_agent_calls: 30  # Hard cap across entire pipeline
  
FAIL_FAST_RULE:
  If quality_score(retry_2) <= quality_score(retry_1):
    STOP retrying — score not improving
    Deliver best available + quality note to user
```

---

## Step 1: Extract Audit Inputs

```yaml
AUDIT_INPUTS:
  from_shared_context:
    user_request:
      original_text: "string"
      expanded_dimensions: { ... }
      required_fields: [ ... ]  # for data_collection mode
      output_formats: ["word", "slides", ...]
      content_depth: "standard | comprehensive"
    
    workflow:
      steps: [ ... ]  # Full step list from strategist
      current_step_index: N
      
    audit_history: [ ... ]  # All prior tier 1/2 audits
    
  from_filesystem:
    output_files: /output/*  # Final deliverables
    tmp_files: /tmp/*  # Intermediate artifacts (for rollback context)
```

---

## Step 2: Audit Comparison

```yaml
AUDIT_CHECKS:
  requirement_coverage:
    description: Every dimension from request expansion addressed?
    method: |
      For each dimension in expanded_dimensions:
        Search output content for relevant coverage
        Score: covered / partially_covered / missing
    weight: 40%
    
  format_compliance:
    description: Output matches requested format(s)?
    method: |
      For each format in output_formats:
        Verify file exists in /output/
        Verify file size > minimum threshold
        Verify format-specific checks (from tiered-audit.md tier 1)
    weight: 15%
    
  content_depth:
    description: Content depth matches target?
    method: |
      If content_depth == "comprehensive":
        Check total word count >= 3000
        Check each section >= 200 words
        Check specific data/examples present
      If content_depth == "standard":
        Check total word count >= 1000
        Check no empty sections
    weight: 25%
    
  data_completeness:
    description: Required fields populated? (data_collection mode only)
    method: |
      For each field in required_fields:
        Check field exists in output
        Check field has non-empty value
      Score: populated / empty / missing
    weight: 20% (only if data_collection mode)
    
  SCORING:
    overall_score: weighted average of all applicable checks (0-100)
    pass_threshold: 70
    result: pass (>=70) | warning (50-69) | fail (<50)
```

---

## Step 3: Failure Diagnosis — Identify Failing Step

```yaml
DIAGNOSIS_PROTOCOL:
  trigger: audit result == "fail" or "warning" with score < 60
  
  step_attribution:
    description: Map each failure to the pipeline step that caused it
    
    mapping_rules:
      requirement_coverage_low:
        likely_cause: bien-soan (synthesis step)
        reason: Content wasn't synthesized with all dimensions
        
      format_compliance_low:
        likely_cause: tao-<format> (output step)
        reason: Output generation had formatting issues
        
      content_depth_low:
        likely_cause: bien-soan OR thu-thap
        check: |
          IF gathered content was thin → thu-thap (insufficient sources)
          IF gathered content was rich but output thin → bien-soan (poor synthesis)
        
      data_completeness_low:
        likely_cause: thu-thap (data collection step)
        reason: Data wasn't fully gathered from sources
        
  output:
    failing_step_id: "string"  # e.g., "synthesize", "search", "output_word"
    failure_reason: "string"
    retry_instructions: "specific guidance for improvement"
    quality_scores:
      current: N
      previous: N  # from prior retry, if any
```

---

## Step 4: Step-Level Rollback & Re-execution

```yaml
ROLLBACK_PROTOCOL:
  principle: Re-execute from the failing step, NOT from the beginning
  
  rollback_steps:
    1_validate_budget:
      check: |
        total_retries < 10
        step_retries < 3
        agent_calls < 30
      if_exceeded: SKIP rollback → deliver best available
      
    2_check_fail_fast:
      check: |
        IF this is retry >= 2 for this step:
          Compare current score vs previous retry score
          IF current_score <= previous_score:
            STOP — quality not improving
            Deliver best available + quality note
      
    3_prepare_retry_context:
      action: |
        Build retry instructions from diagnosis:
        - What specifically was wrong
        - What the step should do differently
        - Any additional sources/data to use
        
    4_re_execute_step:
      action: |
        Call the failing skill with:
        - Original inputs
        - Enhanced instructions (retry_instructions)
        - Flag: is_retry = true, attempt = N
        
    5_re_run_downstream:
      action: |
        After re-executing the failing step,
        re-execute ALL downstream steps too.
        
        Example: If bien-soan failed, re-run:
          bien-soan (retry) → tao-word (re-generate)
          
        This ensures output reflects the improved intermediate step.
        
    6_re_audit:
      action: |
        Run audit again on new output
        Log to audit_history with:
          tier: "final_audit"
          attempt: N
          previous_score: X
          new_score: Y
          
  RETRY_COUNTER_TRACKING:
    location: shared context → audit_history array
    per_entry:
      step_id: "string"
      tier: "final_audit"
      attempt: N
      score: number
      result: pass | fail
      issues: ["..."]
      retry_instructions: "..."
      timestamp: ISO-8601
```

---

## Step 5: Deliver Best Available

```yaml
DELIVERY_PROTOCOL:
  on_pass:
    action: Deliver output to user
    message: |
      ✅ Output đã qua kiểm tra chất lượng (score: {score}/100)
      📄 File: {output_path} ({file_size})
      
  on_warning:
    action: Deliver output with quality note
    message: |
      ⚠️ Output đạt mức chấp nhận được (score: {score}/100)
      📋 Lưu ý: {issues_summary}
      📄 File: {output_path} ({file_size})
      
  on_budget_exhausted:
    action: Deliver best available output
    message: |
      📄 File: {output_path} ({file_size})
      ⚠️ Đã thử cải thiện {total_retries} lần, đây là kết quả tốt nhất.
      📋 Vấn đề còn tồn tại: {remaining_issues}
      
  on_fail_fast:
    action: Deliver best scoring version
    message: |
      📄 File: {output_path} ({file_size})  
      ⚠️ Chất lượng không cải thiện sau {attempts} lần thử.
      📋 Score tốt nhất: {best_score}/100
      📋 Vấn đề: {issues_summary}
```

---

## Integration with Pipeline

```yaml
INTEGRATION:
  called_by: tong-hop orchestrator (Step 4.7 — final quality gate)
  
  in_pipeline_flow:
    ... → tao-<format> → FINAL AUDIT → deliver
                              ↓ (if fail)
                         diagnose → rollback → re-execute → re-audit
                              ↓ (if still fail, budget OK)
                         retry loop (max per constraints)
                              ↓ (budget exhausted OR fail-fast)
                         deliver best available
                         
  shared_context_writes:
    audit_history: Append all audit entries
    workflow.audit_result: "pass | warning | fail_delivered_best"
    workflow.total_retries: N
    workflow.quality_score: final score
```

---

## Examples

### Example 1: Successful First Audit
```yaml
scenario: User asked for a Word report on AI trends
final_audit:
  requirement_coverage: 85 (all 5 dimensions covered)
  content_depth: 80 (comprehensive, 4200 words)
  format_compliance: 95 (Word file, 45KB, all sections)
  overall_score: 85
  result: pass
action: Deliver immediately
```

### Example 2: Rollback to bien-soan
```yaml
scenario: User asked for comprehensive analysis, output is thin
final_audit:
  requirement_coverage: 60 (2/5 dimensions shallow)
  content_depth: 40 (only 1200 words, expected 3000+)
  format_compliance: 90 (file OK)
  overall_score: 55
  result: fail
  
diagnosis:
  failing_step: "synthesize" (bien-soan)
  reason: "Content lacks depth in dimensions: market_analysis, competitive_landscape"
  
rollback:
  retry_instructions: |
    Expand sections on market_analysis and competitive_landscape.
    Add specific data points, company names, market size figures.
    Target: 3000+ words total, 400+ words per major section.
  re_execute: bien-soan → tao-word → re-audit
  
re_audit:
  overall_score: 78
  result: pass
  total_retries: 1
```

### Example 3: Fail-Fast Triggered
```yaml
scenario: Source data inherently limited
retry_1_score: 52
retry_2_score: 51  # Not improving
action: STOP retrying, deliver retry_1 output (score 52) with quality note
```
