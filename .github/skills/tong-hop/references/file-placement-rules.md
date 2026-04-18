# File Placement Rules — InsightEngine

> Strict rules enforced across ALL skills and ALL models.

---

## Directory Structure

```yaml
FILE_PLACEMENT:
  scripts:
    path: /scripts
    purpose: All executable scripts (Python, Node.js CLI tools)
    examples:
      - scripts/gen_report.py
      - scripts/gen_slides.js
      - scripts/fetch_data.py
    rule: NEVER place scripts in tmp/, output/, or root directory

  tmp:
    path: /tmp
    purpose: Temporary/intermediate files during pipeline execution
    examples:
      - tmp/.session-state.json
      - tmp/.agent-context.json
      - tmp/raw_content.md
      - tmp/search_results.json
    rule: Cleaned up after pipeline completion (optional)
    note: Session state and agent context files live here

  output:
    path: /output
    purpose: All final deliverable files for the user
    examples:
      - output/report.docx
      - output/presentation.pptx
      - output/data.xlsx
      - output/analysis.pdf
      - output/page.html
    rule: NEVER place final output in tmp/ or scripts/

  input:
    path: /input
    purpose: User-provided source files
    examples:
      - input/source_document.pdf
      - input/data.xlsx
    rule: Read-only — never modify input files
```

---

## Validation Protocol

```yaml
VALIDATION:
  when:
    - Pipeline start (Step 0)
    - After each sub-skill execution (Step 4 quality loop)

  checks:
    1. Scripts check:
       - Any .py or .js file created outside /scripts → ERROR
       - Exception: .github/skills/*/scripts/ (skill-internal scripts are OK)
    
    2. Output check:
       - Any .docx/.xlsx/.pptx/.pdf/.html in wrong location → ERROR
       - Must be in /output directory
    
    3. Temp check:
       - Intermediate JSON/MD files should be in /tmp
       - Session state must be in /tmp/.session-state.json
    
  on_violation:
    - Log warning with file path and correct location
    - Auto-move file to correct directory
    - Continue pipeline (don't fail for misplacement)
```

---

## Enforcement in Skills

Each skill MUST follow these rules. The tong-hop orchestrator validates after each step.

```yaml
SKILL_RULES:
  tao-word:    output → /output/*.docx
  tao-excel:   output → /output/*.xlsx
  tao-slide:   output → /output/*.pptx
  tao-pdf:     output → /output/*.pdf
  tao-html:    output → /output/*.html
  tao-hinh:    output → /output/images/*.png
  thiet-ke:    output → /output/*.png or /output/*.pdf
  thu-thap:    temp → /tmp/raw_content.md or /tmp/search_results.json
  bien-soan:   temp → /tmp/synthesized_content.md
  tong-hop:    state → /tmp/.session-state.json, /tmp/.agent-context.json
```
