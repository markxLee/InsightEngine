---
name: cai-tien
description: |
  Session retrospective and continuous improvement skill for InsightEngine. Analyzes the entire
  work session — user's original request, intermediate steps, final output, quality gaps — and
  produces actionable improvement recommendations for the pipeline, individual skills, and
  overall process. Can also create new skills or modify existing ones to address systemic issues.
  Always use this skill when: the user says "cải tiến", "retrospective", "phân tích session",
  "tại sao kết quả không tốt", "cải thiện quy trình", "improve pipeline", "analyze what went
  wrong", "session review", "process improvement", "nâng cấp skill", "tại sao output kém",
  "lesson learned", or when the user is frustrated with output quality and wants systemic fixes
  rather than just a redo. Also use when the user explicitly asks to improve a specific skill
  based on real usage experience, or when a pattern of failures is noticed across multiple runs.
  Do NOT use for one-off output fixes (use kiem-tra for that) or for creating skills from scratch
  without session context (use skill-creator/skill-forge for that).
argument-hint: "[session context or specific issue to analyze]"
version: 1.1
compatibility:
  tools:
    - read_file
    - run_in_terminal
    - memory (for storing improvement records)
---

# Cải Tiến — Session Retrospective & Continuous Improvement

**References:** `references/retrospective-template.md`

This skill looks at a completed (or failed) InsightEngine session and asks: **"What went wrong,
why did it go wrong, and how do we prevent it next time?"**

The key insight: individual output fixes are band-aids. Real improvement comes from analyzing
the pattern of failures and updating the skills/pipeline to prevent recurrence. This skill
makes that analysis systematic rather than ad-hoc.

Three modes:
1. **Session retrospective**: Analyze a specific session (input → process → output → gaps)
2. **Skill improvement**: Diagnose a specific skill's weaknesses from usage evidence
3. **Pipeline improvement**: Identify systemic issues across the entire tong-hop pipeline

All responses to the user are in Vietnamese.

---

## Step 1: Gather Session Evidence

The quality of retrospective depends on the evidence available. Gather as much as possible:

```yaml
EVIDENCE_SOURCES:
  user_request:
    # The original prompt — the ground truth for what was expected
    method: Ask user to paste or describe their original request
    critical: true
  
  output_files:
    # What was actually produced
    method: Read output files in output/ or user-specified path
    critical: true
  
  session_state:
    # Pipeline execution log — which steps ran, which failed
    method: python3 scripts/save_state.py check
    optional: true  # May not exist if session was in a previous chat
  
  session_summary:
    # Appended after each pipeline run
    method: Read output/session-summary.md (latest entry)
    optional: true
  
  user_feedback:
    # What the user said about the output
    method: Ask user what specifically was wrong
    critical: true
    prompt: |
      Để phân tích chính xác, tôi cần biết:
      1. Yêu cầu ban đầu của bạn là gì?
      2. Kết quả nhận được như thế nào?
      3. Cụ thể điều gì sai / thiếu / không đúng?
      4. Bạn kỳ vọng kết quả như thế nào?
  
  skill_files:
    # Current skill definitions — to identify instruction gaps
    method: Read relevant SKILL.md files based on the pipeline steps that ran
    optional: true
```

---

## Step 2: Root Cause Analysis

Analyze the gap between expected and actual output. Use a structured framework:

```yaml
ROOT_CAUSE_FRAMEWORK:
  1_WHAT_HAPPENED:
    # Factual description of the failure
    - What did the user request?
    - What was produced?
    - What specific elements are wrong/missing?
  
  2_WHERE_IN_PIPELINE:
    # Which step(s) failed?
    analysis_per_step:
      step_1_parse:
        question: "Did tong-hop correctly understand the request type?"
        common_failures:
          - Misclassified research vs data_collection
          - Missed required fields in user's prompt
          - Didn't detect chained output need
      
      step_1_5_analysis:
        question: "Did the deep analysis capture what the user actually needed?"
        common_failures:
          - Expanded wrong dimensions (analytical vs data collection)
          - Missed implicit requirements
          - Over-expanded scope, diluting focus
      
      step_4_1_thu_thap:
        question: "Did thu-thap gather the right raw material?"
        common_failures:
          - Used generic search instead of platform-specific
          - Returned search result pages instead of individual item pages
          - Insufficient quantity of items/sources
          - Thin content from poor source selection
      
      step_4_3_bien_soan:
        question: "Did bien-soan synthesize effectively from what it had?"
        common_failures:
          - Synthesized from thin data (garbage in, garbage out)
          - Lost specific details during synthesis
          - Produced generic analysis instead of data-driven content
      
      step_4_4_output:
        question: "Did the output skill faithfully render the content?"
        common_failures:
          - Truncated content to fit format
          - Lost structure during format conversion
          - Missing sections or fields
      
      step_4_7_audit:
        question: "Did the audit catch the issues?"
        common_failures:
          - Audit not implemented yet (skill is new)
          - Audit criteria didn't cover this type of failure
  
  3_WHY_IT_HAPPENED:
    # Root cause — not just symptoms
    categories:
      skill_gap: "The skill's instructions don't cover this scenario"
      detection_gap: "The pipeline didn't detect the request type correctly"
      execution_gap: "Instructions exist but weren't followed correctly"
      tool_limitation: "The tools available can't do what's needed"
      data_gap: "The right data sources weren't accessible"
  
  4_PATTERN_CHECK:
    # Is this a one-off or a systemic issue?
    questions:
      - "Would a similar request fail the same way?"
      - "Does this expose a category of requests the pipeline can't handle?"
      - "Have other sessions had similar failures?"
    check: Review output/session-summary.md for patterns
```

---

## Step 3: Generate Improvement Plan

Based on root cause analysis, create specific, actionable improvements:

```yaml
IMPROVEMENT_CATEGORIES:
  skill_update:
    # Modify an existing skill's SKILL.md
    format:
      skill: "tong-hop"
      file: ".github/skills/tong-hop/SKILL.md"
      change_type: "add_instruction | modify_instruction | add_example"
      description: "Add data_collection request type detection"
      specific_change: |
        In Step 1, add detection for requests that need specific items
        collected rather than knowledge synthesized...
      priority: "high"  # high | medium | low
      effort: "medium"  # small (< 10 lines) | medium (10-50) | large (50+)
  
  new_skill:
    # Create a brand new skill to handle a gap
    format:
      name: "kiem-tra"
      purpose: "Audit output against requirements"
      justification: "No existing skill validates output vs requirements"
      priority: "high"
      effort: "large"
  
  reference_update:
    # Update reference docs or add new ones
    format:
      skill: "thu-thap"
      file: "references/data-collection-mode.md"
      change_type: "create"
      description: "Add protocol for platform-specific data collection"
  
  pipeline_change:
    # Change the overall pipeline flow
    format:
      change: "Add mandatory output audit step after all output generation"
      affects: "tong-hop Step 4"
      justification: "Quality gates check format/depth but not requirement fulfillment"
  
  process_change:
    # Non-technical improvements
    format:
      change: "User should specify output fields explicitly"
      type: "user_guidance"
      justification: "Implicit field requirements are hard to detect automatically"
```

---

## Step 4: Present Retrospective Report

```yaml
RETROSPECTIVE_REPORT: |
  🔍 **Phân tích Session & Đề xuất Cải tiến**

  ---

  ### 1. Tóm tắt vấn đề
  **Yêu cầu:** {original_request_summary}
  **Kết quả:** {actual_output_summary}
  **Gap:** {specific_gaps}

  ---

  ### 2. Phân tích nguyên nhân gốc
  | Bước Pipeline | Vấn đề | Nguyên nhân | Loại |
  |---------------|--------|-------------|------|
  | {step_1} | {issue} | {root_cause} | {category} |
  | {step_2} | {issue} | {root_cause} | {category} |
  ...

  **Nguyên nhân chính:** {primary_root_cause}
  **Đây là vấn đề:** {one_off / systemic}

  ---

  ### 3. Kế hoạch cải tiến
  
  #### 🔴 Ưu tiên cao (phải fix)
  | # | Thay đổi | Skill | Effort | Mô tả |
  |---|---------|-------|--------|--------|
  | 1 | {change_1} | {skill} | {effort} | {description} |
  ...

  #### 🟡 Ưu tiên trung bình (nên fix)
  | # | Thay đổi | Skill | Effort | Mô tả |
  |---|---------|-------|--------|--------|
  ...

  #### 🟢 Ưu tiên thấp (nice to have)
  ...

  ---

  ### 4. Skill mới cần tạo
  {if any new skills needed:}
  | Skill | Mục đích | Lý do | Effort |
  |-------|---------|-------|--------|
  | {name} | {purpose} | {justification} | {effort} |
  {end if}

  ---

  👉 Bạn muốn tôi thực hiện cải tiến nào? (Nhập số hoặc "tất cả")
```

---

## Step 5: Execute Improvements

When the user approves improvements:

```yaml
EXECUTION_ORDER:
  1. Skill updates (modify existing SKILL.md files)
  2. New reference files (add to references/ folders)
  3. New skills (create SKILL.md + directory structure)
  4. Pipeline changes (update tong-hop routing/flow)
  5. Registration (update copilot-instructions.md if new skills added)

EXECUTION_METHOD:
  for_skill_updates:
    - Read current SKILL.md
    - Apply specific changes using replace_string_in_file
    - Verify no broken references
  
  for_new_skills:
    - Create directory: .github/skills/{skill-name}/
    - Write SKILL.md following skill-creator patterns
    - Create references/ if needed
    - Register in copilot-instructions.md
  
  for_reference_updates:
    - Create or update .md files in appropriate references/ folder
    - Update SKILL.md pointers if needed

AFTER_EXECUTION:
  1. Report what was changed with file paths
  2. Save improvement record to output/session-summary.md
  3. Suggest: "Bạn có thể thử lại request gốc để kiểm tra cải tiến"
```

---

## Step 6: Record & Learn

Save the retrospective findings for future reference:

```yaml
LEARNING_RECORD:
  append_to: output/session-summary.md
  format: |
    ## Retrospective: {date}
    **Request:** {original_request_summary}
    **Root cause:** {primary_root_cause}
    **Improvements made:**
    - {improvement_1}
    - {improvement_2}
    **Skills modified:** {list_of_modified_skills}
    **New skills created:** {list_of_new_skills}
    ---
  
  also_consider:
    - Update memory files if patterns are recurring
    - Flag if same root cause appears in 3+ sessions → escalate to architecture review
```

---

## Examples

**Example 1: Job search output had search links instead of job links**
```
Root cause: tong-hop didn't detect data_collection request type → thu-thap used generic search → fetched search result pages
Improvements:
1. [HIGH] Add REQUEST_TYPE detection to tong-hop Step 1
2. [HIGH] Add data_collection mode to thu-thap with platform-specific search
3. [HIGH] Create kiem-tra skill for output audit
4. [MED] Add URL quality validation to thu-thap quality gate
```

**Example 2: Report content was too shallow despite comprehensive mode**
```
Root cause: thu-thap only fetched 3 sources with thin content → bien-soan couldn't produce depth from scraps
Improvements:
1. [HIGH] Increase minimum_chars threshold in thu-thap quality gate
2. [MED] Add source diversity check (min 5 sources from 3+ domains)
3. [LOW] Add example in bien-soan showing how to request enrichment callback
```

---

## What This Skill Does NOT Do

- Does NOT fix individual output files (use kiem-tra for spot fixes)
- Does NOT create skills from scratch without usage context (use skill-creator)
- Does NOT re-run the pipeline (user does that after improvements are applied)
- Does NOT modify skills without user approval
