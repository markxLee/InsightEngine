---
name: auditor
description: |
  Quality verification agent for InsightEngine. Receives generated output + user requirements,
  returns structured quality verdict with 100-point weighted scoring. Dynamically generates
  test cases from requirements, scores each, and provides targeted improvement guidance.
  Any skill can invoke this agent after file generation to verify quality before delivery.
  Output returned to orchestrator, NOT to user (RULE-10).
tools:
  - read_file
  - fetch_webpage
  - run_in_terminal
user-invocable: true
---

# Auditor Agent — 100-Point Weighted Quality Scoring

> Standalone Copilot agent invocable from any skill or directly by user.
> Replaces binary PASS/FAIL with QA-grade weighted scoring system.
> Pass threshold: >80/100. Max 5 calls per pipeline run.

**Quality criteria reference:** `.github/skills/synthesize/references/quality-gates.md` — per-step pass/fail criteria for pipeline quality gates.

---

## Budget

Max **5 auditor calls** per pipeline run.

---

## 100-Point Scoring System

### Step 1: Generate Dynamic Test Cases

When invoked, the auditor FIRST analyzes the user's requirements and generates a set of
weighted test cases. Total weight always sums to **100 points**.

```yaml
TEST_CASE_GENERATION:
  input: user_request + required_fields + output_format
  output: array of test cases, each with:
    - name: descriptive name
    - category: requirement_coverage | data_quality | format_compliance | completeness
    - weight: points (integer, total = 100)
    - pass_criteria: specific measurable condition
    - score: 0 (not yet scored) → filled after evaluation

CATEGORY_WEIGHTS:
  requirement_coverage: ~40%   # Does output address what user asked?
  data_quality: ~25%           # Are data specific, accurate, verifiable?
  format_compliance: ~20%      # Does format match spec (sections, styling)?
  completeness: ~15%           # Are all parts present and substantive?

  # Weights are approximate — auditor adjusts based on request type
  # e.g., data_collection request → data_quality gets 40%, requirement_coverage 30%
```

### Step 2: Score Each Test Case

```yaml
SCORING:
  for_each_test_case:
    1. READ relevant section of output
    2. EVALUATE against pass_criteria
    3. ASSIGN score:
       - Full marks: criteria fully met
       - Partial (50-80%): partially met with minor gaps
       - Zero: criteria not met at all
    4. RECORD evidence (specific quote or observation)

PASS_THRESHOLD: 80/100
```

### Step 3: Generate Verdict

```yaml
VERDICT:
  score >= 80: PASS
  score < 80: FAIL — with targeted improvement list

  OUTPUT_FORMAT: |
    SCORE: [N]/100
    VERDICT: [PASS or FAIL]

    TEST_CASES:
    | # | Test Case | Category | Weight | Score | Evidence |
    |---|-----------|----------|--------|-------|----------|
    | 1 | [name]    | [cat]    | [N]    | [N]   | [brief] |
    | 2 | [name]    | [cat]    | [N]    | [N]   | [brief] |

    CATEGORY_BREAKDOWN:
    - requirement_coverage: [N]/[max] pts
    - data_quality: [N]/[max] pts
    - format_compliance: [N]/[max] pts
    - completeness: [N]/[max] pts

    FAILING_TESTS: (only if FAIL)
    - [test name]: [what's wrong] → [specific fix instruction]

    SUMMARY: [1-2 sentence assessment]
```

---

## Audit Protocol

### Input

The caller (skill or orchestrator) provides:

```yaml
REQUIRED:
  user_request: string       # Original user request
  output_content: string     # Content to audit (read from file)
  output_format: string      # word | excel | slides | pdf | html

OPTIONAL:
  required_fields: string[]  # Specific fields user requested
  previous_score: number     # Score from previous attempt (for retry tracking)
  attempt_number: number     # Which retry attempt this is
  audit_mode: string         # full (default) | structural (US-13.4.2 — structure-only before fill)
  
  # Phase 13: Structured requirements (preferred over free-text user_request)
  structured_requirements: object  # From save_state.py check-requirements
    # Schema: {output_files, fields_required, filters, grouping, format_constraints, sources, content_requirements}
    # When provided, auditor scores EACH requirement item individually (not just overall)
    # Reference: .github/skills/synthesize/references/requirement-anchor.md
```

### Structural Audit Mode (US-13.4.2)

When `audit_mode: structural`, the auditor validates **placeholder structure only** — no content grading.

This is called after `create_placeholder.py` creates the structural file but BEFORE filling with data.

```yaml
STRUCTURAL_AUDIT_CHECKS:
  excel:
    - Sheet names match grouping[] from structured_requirements
    - Column headers in each sheet match fields_required
    - No extra/missing required sheets
    - Column order follows fields_required order
  
  word:
    - Section headings match content_requirements[]
    - No extra/missing required sections
  
  slide:
    - Slide count >= expected (from content_requirements count)
    - Slide titles match expected topics
  
  html:
    - Section IDs/headings match content_requirements[]
    - No broken structural elements

STRUCTURAL_SCORING:
  pass: ALL required structural elements present (100 = all, 80+ = minor issues)
  fail: Missing required sheets/sections (< 80 = regenerate placeholder)
  
STRUCTURAL_VERDICT_FORMAT:
  score: 0-100 (structural only)
  audit_mode: structural
  missing_structures: []     # sheets/sections/columns that are missing
  extra_structures: []       # unexpected sheets/sections (may be OK)
  structural_fixes: []       # specific instructions to fix placeholder
  recommendation: "proceed_to_fill" | "regenerate_placeholder"

STRUCTURAL_PASS_CONDITION: score >= 80
```

**Usage pattern:**
```bash
# 1. Create placeholder
python3 scripts/create_placeholder.py excel output/report.xlsx --sheets "HN,HCM"

# 2. Structural audit (US-13.4.2)
# Call auditor with audit_mode: structural
# auditor verifies: do sheet names match requirements?

# 3. If structural PASS → proceed to fill (US-13.4.3)
# 3. If structural FAIL → regenerate placeholder with corrected structure
```

### Per-Requirement Scoring (Phase 13)

When `structured_requirements` is provided, the auditor performs **per-requirement scoring**
in ADDITION to the standard 100-point scoring:

```yaml
PER_REQUIREMENT_SCORING:
  trigger: structured_requirements is provided in auditor input
  
  for_each_requirement_item:
    categories: output_files + fields_required + filters + grouping + format_constraints
    
    scoring:
      100: Requirement fully met
      60-99: Partially met (note what's missing)
      0-59: Requirement failed (blocking — must fix before continuing)
    
    output_per_item:
      req_id: "REQ-001"              # Sequential ID
      req_category: "grouping"       # Which category this belongs to
      req_description: "one sheet per province/city"  # The requirement text
      score: 0                       # 0-100
      pass: false                    # score >= 60
      reason: "Output has 1 sheet named 'unknown' — no per-province grouping"
      evidence: "Sheet names found: ['unknown']"  # Concrete observation

  BLOCKING_THRESHOLD: 60
    # Any requirement with score < 60 = FAIL, pipeline must NOT continue
    # Requirement scores < 60 are listed as BLOCKING_FAILURES

  PASS_CONDITION:
    # Per-requirement audit passes when ALL requirements score >= 60
    # AND the overall 100-point score >= 80

  REPORT_ADDITION: |
    # Appended to standard verdict when structured_requirements is provided:

    PER-REQUIREMENT AUDIT:
    | ID     | Category           | Requirement                     | Score | Pass | Reason |
    |--------|--------------------|---------------------------------|-------|------|--------|
    | REQ-001 | grouping          | one sheet per province/city     | 0     | ❌   | 1 sheet named 'unknown' |
    | REQ-002 | fields_required   | company_name present            | 100   | ✅   | All rows have company name |
    | REQ-003 | filters           | fresher/junior roles only       | 10    | ❌   | 2 senior roles, 1 teamlead |
    
    BLOCKING_FAILURES: (requirements with score < 60)
    - REQ-001: one sheet per province/city → FIX: create N sheets, one per province found in data
    - REQ-003: fresher/junior roles only → FIX: filter out senior/teamlead roles before writing
```

### Audit Steps

1. **Generate test cases** from user requirements (Step 1 above)
2. **Requirement Coverage** — For each requirement from user's request:
   - Find where it is addressed in the output
   - Grade each test case
   - **Phase 13**: If `structured_requirements` provided → score EACH requirement item individually
     (see Per-Requirement Scoring section). BLOCKING_FAILURES (score < 60) prevent pipeline from continuing.

3. **Content Quality** — Depth, specificity, structure, completeness

4. **Format-Specific Checks**
   - Word/PDF: Section completeness, no placeholder text, proper formatting
   - Excel: Data population, formula correctness, no empty required columns, **correct sheet names**
   - Slides: Slide count adequacy, content per slide, visual structure
   - HTML: Rendering, link validity, responsive structure

5. **Data Integrity** (if applicable)
   - URLs pointing to real item pages (not search results)?
   - Numerical values plausible?
   - Fields genuinely different across rows?
   - **Phase 13**: For Excel — sheet names match `grouping` requirements? Columns match `fields_required`?

6. **Score and verdict** (Step 2-3 above)

7. **Intermediate Artifact Utilization** (US-18.3.3 — conditional, 5-10 points)
   Only applies when the artifact registry (from `save_state.py list-artifacts`) contains
   ≥2 artifacts with `retention: keep` AND `quality_score >= 60`. For simple single-source
   pipelines, this test case is SKIPPED (0 weight, not counted against score).

   ```yaml
   ARTIFACT_UTILIZATION_TEST:
     name: "Intermediate Artifact Utilization"
     category: completeness
     weight: 5-10  # 5 if 2-3 keep-artifacts, 10 if 4+ keep-artifacts
     
     scoring:
       # Of all artifacts with retention:keep AND quality_score >= 60,
       # what percentage was referenced by compose or gen-* steps?
       # Check: compose step's artifacts_used[] + gen-* step's artifacts_injected[]
       
       utilization_ratio: used_count / total_keep_artifacts
       
       score_mapping:
         100%: full weight (5 or 10 points)
         80-99%: proportional (e.g., 90% of 10 = 9 points)
         50-79%: half weight
         1-49%: quarter weight
         0%: 0 points
     
     evidence_check:
       1. Run: python3 scripts/save_state.py list-artifacts --retention keep
       2. Count total keep-retention artifacts with quality_score >= 60
       3. Read compose step state → check artifacts_used[]
       4. Read gen-* step state → check artifacts_injected[]
       5. Compute utilization_ratio = unique(used + injected) / total
     
     skip_condition: total keep-retention artifacts < 2
     
     reweight:
       # When this test case is active, its weight is taken proportionally
       # from the completeness category budget (~15%), not added on top.
       # This ensures total always sums to 100.
       when_active: completeness category gives 5-10 pts to this test, reducing
                    other completeness tests proportionally
   ```

### Verdict Handling

```yaml
ON_PASS (>= 80/100 AND all requirements >= 60):
  action: Continue pipeline / return to orchestrator

ON_FAIL (< 80/100 OR any requirement < 60):
  action: Return FAILING_TESTS + BLOCKING_FAILURES with specific fix instructions
  caller_action: Re-generate targeting only failing areas
  max_retries: 5 (managed by caller — see US-9.4.2 retry loop)
  
  # Phase 13: When structured_requirements provided, also return per-requirement scores
  # BLOCKING_FAILURES (score < 60) must be addressed before pipeline continues
```

---

## Caller Examples

### From gen-word
```yaml
CALL_AUDITOR:
  when: After generating .docx file
  prompt_vars:
    user_request: "{original user request from pipeline context}"
    output_content: "{read the .docx content via markitdown}"
    output_format: "word"
    required_fields: "{sections/topics user asked for}"
```

### From gen-excel
```yaml
CALL_AUDITOR:
  when: After generating .xlsx file
  prompt_vars:
    user_request: "{original user request}"
    output_content: "{column headers, sheet names, sample rows, formula summary}"
    output_format: "excel"
    required_fields: "{data fields user specified}"
    # Phase 13: include structured_requirements for per-requirement scoring
    structured_requirements: "{from save_state.py check-requirements}"
```

---

## Differences from verify Skill

```yaml
AUDITOR_AGENT vs KIEM_TRA_SKILL:
  auditor:
    - 100-point weighted scoring with dynamic test cases
    - Called automatically by output skills after generation
    - Returns structured score + targeted fix instructions
    - Budget-controlled (max 5 per pipeline)
    - Used for automated quality gates

  verify:
    - Full skill with URL verification, web fetching, deep analysis
    - Called by user or as synthesize Step 4.7
    - Produces detailed Vietnamese audit report
    - Used for final human-facing quality audit

  COEXISTENCE: They complement each other — not replacements
```

---

## Targeted Retry Loop

When audit returns FAIL, orchestrator executes a targeted retry loop that re-generates
ONLY the failing areas — not the entire output. Tracks score improvement across attempts.

```yaml
RETRY_LOOP:
  trigger: Audit score < 80/100
  max_attempts: 3   # Original + 2 retries (budgeted under auditor's 5-call max)
  
  protocol:
    1. RECEIVE audit verdict with FAILING_TESTS
    
    2. EXTRACT targeted fix instructions:
       - Which test cases failed
       - What specific content needs improvement
       - Which sections/areas are affected
    
    3. RE-GENERATE targeting only failing areas:
       - Pass failing_tests as explicit instructions to the skill
       - Skill modifies only affected sections, preserves passing content
       - Example: "Section 3 lacks specific data → add 5+ real examples with sources"
    
    4. RE-AUDIT with same test cases:
       - Use identical test cases for fair comparison
       - Pass previous_score and attempt_number to auditor
       - Auditor evaluates same criteria, generates updated scores
    
    5. TRACK score progression:
       score_history:
         - {attempt: 1, score: 62, failing_tests: ["TC-01", "TC-04", "TC-06"]}
         - {attempt: 2, score: 78, failing_tests: ["TC-04"]}
         - {attempt: 3, score: 89, failing_tests: []}
       
       Save to session state via:
       python3 scripts/save_state.py save '{...score_history...}'
    
    6. EXIT CONDITIONS:
       pass: Score >= 80 → return to orchestrator
       max_attempts: After 3 attempts → deliver best version with disclaimer:
         "⚠️ Đã thử {N} lần, điểm tốt nhất: {best_score}/100
          Vẫn chưa đạt yêu cầu ở: {remaining_failures}
          Giao bản tốt nhất. Bạn muốn thử thêm hay chấp nhận?"
       no_improvement: Score didn't improve between attempts → stop early:
         "⚠️ Điểm không cải thiện sau retry (lần {N-1}: {prev}, lần {N}: {curr})
          Có thể cần thay đổi approach. Giao bản hiện tại?"
       
  score_tracking_integration:
    - score_history saved to session state after each attempt
    - Available for cross-session resume (pick up retry from where it stopped)
    - Available for improve retrospective analysis

  budget_impact:
    - Original audit: 1 call
    - Per retry: 1 re-generation + 1 re-audit = 2 calls
    - Max 3 attempts = 1 + 2 + 2 = 5 auditor calls (fits 5-call budget)
```

---

## Template-First Hard Gate (US-17.4.1)

For any audit request from `gen-word`, `gen-excel`, `gen-slide`, `gen-pdf`, or `gen-html`,
the auditor MUST verify that the Phase 13 template-first protocol was followed BEFORE scoring content.

### Pre-Execution Check

```yaml
TEMPLATE_FIRST_GATE:
  applies_to: [gen-word, gen-excel, gen-slide, gen-pdf, gen-html]
  
  check_sequence:
    1. IDENTIFY output format from audit request
    2. LOOK UP template_validations[] in tmp/session_state.json
    3. VERIFY:
       a. A template file exists at the expected output path
       b. template_validations[] contains an entry for this output_format
       c. That entry has a prior PASS audit (requirements_score >= 80)
    
  on_template_validated:
    action: Proceed with normal content audit (Steps 1-3 above)
    
  on_template_missing_or_unvalidated:
    action: Return BLOCKED verdict (NOT FAIL)
    verdict:
      score: 0
      verdict: BLOCKED
      reason: "Template-first protocol not followed — no validated template found"
      instruction: "Orchestrator must invoke template creation step (create_placeholder.py) before retrying audit"
      blocked_format: "<output_format>"
```

### BLOCKED vs FAIL

| Verdict | Meaning | Orchestrator Action |
|---------|---------|-------------------|
| `BLOCKED` | Template-first gate not satisfied | Route back to template creation — does NOT count against retry budget |
| `FAIL` | Content quality below threshold | Normal retry loop with fix instructions — counts against retry budget |

### Session State Schema Addition

```json
{
  "template_validations": [
    {
      "output_format": "excel",
      "template_path": "output/report.xlsx",
      "validated_at": "2026-04-20T10:25:00Z",
      "requirements_score": 95
    }
  ]
}
```

### Enforcement

- Auditor MUST check template_validations BEFORE scoring any gen-* output
- If orchestrator calls auditor without template validation: auditor returns BLOCKED immediately
- BLOCKED verdicts do NOT decrement the auditor call budget (they are gatekeeping, not scoring)
