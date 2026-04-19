# File Placement Rules — InsightEngine

> Strict rules enforced across ALL skills and ALL models.

---

## Directory Structure

```yaml
FILE_PLACEMENT:
  scripts:
    path: /scripts
    purpose: Permanent reusable utility scripts only (shared across sessions)
    examples:
      - scripts/check_deps.py
      - scripts/recalc.py
      - scripts/save_state.py
      - scripts/validate_urls.py
    rule: ONLY place scripts here if they are reusable utilities. These are tracked by git.
    anti_pattern: NEVER place one-time/session-specific scripts here — they pollute the repo.

  tmp:
    path: /tmp
    purpose: Temporary/intermediate files AND one-time scripts during pipeline execution
    examples:
      - tmp/.session-state.json
      - tmp/.agent-context.json
      - tmp/raw_content.md
      - tmp/search_results.json
      - tmp/gen_custom_report.py    # one-time script for this session
      - tmp/scrape_listings.py      # session-specific scraping script
      - tmp/fetch_data.py           # one-time data fetching script
    rule: Everything in /tmp is gitignored. Cleaned up after pipeline completion (optional).
    note: Session state, agent context files, AND one-time scripts live here.

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
       - Any .py or .js file created in /scripts → verify it's a reusable utility
       - One-time/session-specific scripts MUST go to /tmp, NOT /scripts
       - Exception: .github/skills/*/scripts/ (skill-internal scripts are OK)
    
    2. Output check:
       - Any .docx/.xlsx/.pptx/.pdf/.html in wrong location → ERROR
       - Must be in /output directory
    
    3. Temp check:
       - Intermediate JSON/MD files should be in /tmp
       - One-time scripts should be in /tmp
       - Session state must be in /tmp/.session-state.json
    
  on_violation:
    - Log warning with file path and correct location
    - Auto-move file to correct directory
    - Continue pipeline (don't fail for misplacement)
```

---

## Enforcement in Skills

Each skill MUST follow these rules. The synthesize orchestrator validates after each step.

```yaml
SKILL_RULES:
  gen-word:    output → /output/*.docx
  gen-excel:   output → /output/*.xlsx
  gen-slide:   output → /output/*.pptx
  gen-pdf:     output → /output/*.pdf
  gen-html:    output → /output/*.html
  gen-image:    output → /output/images/*.png
  design:    output → /output/*.png or /output/*.pdf
  gather:    temp → /tmp/raw_content.md or /tmp/search_results.json
  compose:   temp → /tmp/synthesized_content.md
  synthesize:    state → /tmp/.session-state.json, /tmp/.agent-context.json
```
