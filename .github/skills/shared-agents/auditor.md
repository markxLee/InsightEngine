# Shared Auditor Agent — Quality Verification via `runSubagent`

> Standalone Copilot agent invocable from ANY skill via `runSubagent`.
> Receives output content + user requirements → returns PASS/FAIL verdict.
> Replaces inline audit logic in tong-hop. Works independently of pipeline.

---

## Invocation

Any skill calls the auditor like this:

```yaml
HOW_TO_CALL:
  1. READ this file (shared-agents/auditor.md)
  2. BUILD prompt from PROMPT_TEMPLATE below, filling variables
  3. CALL runSubagent with the built prompt
  4. PARSE the structured response

BUDGET: Max 5 auditor calls per pipeline run
```

---

## Prompt Template

Skills construct the `runSubagent` prompt by filling `{variables}`:

```
You are an expert quality auditor for InsightEngine content pipeline.

## Task
Audit the following output against the user's original requirements.
Read the content carefully, verify claims, and judge quality.

## User's Original Request
{user_request}

## Output Content to Audit
{output_content}

## Output Format
{output_format}  (e.g., word, excel, slides, pdf, html)

## Required Fields / Dimensions
{required_fields}

## Audit Instructions

### 1. Requirement Coverage
For each requirement from the user's request:
- Find where it is addressed in the output
- Judge: does the output ACTUALLY satisfy this requirement?
- Grade: PASS / PARTIAL / FAIL

### 2. Content Quality
- Depth: Is the content expert-level and comprehensive, or thin/generic?
- Specificity: Are there concrete data, examples, and analysis — or just platitudes?
- Structure: Are sections well-organized with clear hierarchy?
- Completeness: Are all promised sections present and substantive?

### 3. Format-Specific Checks
For Word/PDF: Check section completeness, no placeholder text, proper formatting
For Excel: Check data population, formula correctness, no empty required columns
For Slides: Check slide count adequacy, content per slide, visual structure
For HTML: Check rendering, link validity, responsive structure

### 4. Data Integrity (if applicable)
- Are URLs pointing to real item pages (not search results)?
- Are numerical values plausible?
- Are fields genuinely different across rows (not copy-pasted)?

## Response Format (STRICT — return EXACTLY this structure)

VERDICT: [PASS or FAIL]

SCORE: [1-10]

REQUIREMENT_COVERAGE:
- R1: [requirement] → [PASS/PARTIAL/FAIL] — [evidence]
- R2: [requirement] → [PASS/PARTIAL/FAIL] — [evidence]
...

ISSUES:
- [issue 1 — specific, actionable]
- [issue 2 — specific, actionable]
...

IMPROVEMENTS:
- [specific improvement suggestion 1]
- [specific improvement suggestion 2]
...

SUMMARY: [1-2 sentence overall assessment]
```

---

## Response Parsing

```yaml
PARSE_RESPONSE:
  verdict: Extract "VERDICT: PASS" or "VERDICT: FAIL"
  score: Extract "SCORE: N" (1-10)
  issues: Extract list after "ISSUES:"
  improvements: Extract list after "IMPROVEMENTS:"
  
  ON_PASS:
    action: Continue pipeline / deliver to user
    
  ON_FAIL:
    action: Re-generate with improvements list as guidance
    max_retries: 2
    escalation: If still FAIL after 2 retries → deliver best version with warning
```

---

## Caller Examples

### From tao-word:
```yaml
CALL_AUDITOR:
  when: After generating .docx file
  prompt_vars:
    user_request: "{original user request from pipeline context}"
    output_content: "{read the .docx content via markitdown or read generated text}"
    output_format: "word"
    required_fields: "{sections/topics user asked for}"
```

### From tao-excel:
```yaml
CALL_AUDITOR:
  when: After generating .xlsx file
  prompt_vars:
    user_request: "{original user request}"
    output_content: "{read xlsx content — column headers, sample rows, formula summary}"
    output_format: "excel"
    required_fields: "{data fields user specified}"
```

### From tao-slide:
```yaml
CALL_AUDITOR:
  when: After generating .pptx file
  prompt_vars:
    user_request: "{original user request}"
    output_content: "{slide titles + content summaries}"
    output_format: "slides"
    required_fields: "{topics/sections user wanted}"
```

---

## Standalone Usage (outside pipeline)

Any skill can call the auditor independently:

```yaml
STANDALONE:
  trigger: Skill wants quality check on its output
  steps:
    1. Read shared-agents/auditor.md
    2. Construct prompt with available context
    3. Call runSubagent(prompt=<built_prompt>, description="Audit output quality")
    4. Parse response and act on verdict
  
  note: Works even without tong-hop pipeline context
  note: Caller provides whatever context is available
```

---

## Differences from kiem-tra Skill

```yaml
AUDITOR_AGENT vs KIEM_TRA_SKILL:
  auditor:
    - Lightweight single-call agent (runSubagent)
    - Called automatically by output skills after generation
    - Returns structured PASS/FAIL verdict
    - Budget-controlled (max 5 per pipeline)
    - Used for automated quality gates
    
  kiem-tra:
    - Full skill with URL verification, web fetching, deep analysis
    - Called by user or as tong-hop Step 4.7
    - Produces detailed Vietnamese audit report
    - Opens URLs, compares data, verifies claims
    - Used for final human-facing quality audit
    
  COEXISTENCE:
    - Auditor handles automated per-step quality gates
    - kiem-tra handles thorough final audit with URL verification
    - They complement each other — not replacements
```
