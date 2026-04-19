# InsightEngine — Non-Negotiable Pipeline Rules

> **Priority:** MANDATORY — These rules override ALL skill-level and agent-level instructions.
> **Enforcement:** Copilot MUST read this file at session start. Violations are pipeline failures.

---

## RULE-1: Hard Session Start

On receiving ANY user prompt that triggers a pipeline (synthesis, creation, research, design, data collection):

1. **FIRST action** — save state + raw prompt:
   ```
   python3 scripts/save_state.py --raw-prompt "<full user prompt>"
   ```
   This creates `tmp/session_state.json` with: `raw_prompt`, `timestamp`, `session_id`, `status: started`.
   If `save_state.py` does not exist: run `setup` skill to create it, then retry.
2. **SECOND action (parallel):**
   - **Intent analysis** — classify what user wants (synthesis, creation, research, design, data_collection, mixed)
   - **Output template creation** — prepare file structure based on expected format (.docx, .xlsx, .pptx, .pdf, .html)
   These two run simultaneously. Both must complete before step 3.
3. **THIRD action** — extract structured requirements (RULE-6) + call strategist for workflow plan.
4. **FOURTH action** — present workflow plan summary to user (information, not a question) and begin execution.

**No exceptions.** No skill may be invoked before step 1 completes.
If `save_state.py` fails and setup cannot fix it: log a warning and continue — but always attempt it first.

---

## RULE-2: Execute-Test-Pivot-Audit Loop

Every skill that produces output MUST follow this loop:

```
execute → self-review → [pivot if needed] → auditor gate → [re-execute if failed] → deliver
```

- **Max pivot attempts:** 3 per delivery step
- **Auditor gate threshold:** >80/100 to pass
- **No single-attempt delivery.** After first execution, self-review MUST run before delivery.
- If auditor gate fails after max pivots: deliver with quality score + explicit gap report.

### Per-Skill Pivot Strategies

Each pivot attempt MUST change at least one strategy — never retry with identical approach:

```yaml
search:
  pivot_1: different query formulation (rephrase, add year, switch language)
  pivot_2: different source domain (switch to alternative platform)
  pivot_3: broaden or narrow scope, switch to deep research mode

gather:
  pivot_1: fallback reader (markitdown → format-specific library)
  pivot_2: different URL fetch tier (fetch_webpage → httpx → Playwright)
  pivot_3: request user to provide alternative file/URL

compose:
  pivot_1: different document structure (reorder sections, merge/split)
  pivot_2: different depth level (expand thin sections with more data points)
  pivot_3: different analytical angle (change framework, add comparison dimension)

gen-word:
  pivot_1: different style template (corporate → academic → minimal)
  pivot_2: restructure sections (TOC depth, heading levels, table layout)
  pivot_3: adjust content density (split long sections, add visual breaks)

gen-excel:
  pivot_1: restructure data layout (pivot table, different column grouping)
  pivot_2: different formula approach (simpler or more robust)
  pivot_3: change formatting (conditional formats, chart types)

gen-slide:
  pivot_1: different layout template (change slide structure)
  pivot_2: different content density per slide (split or merge)
  pivot_3: switch engine (pptxgenjs ↔ ppt-master)

gen-pdf:
  pivot_1: different layout engine (Platypus vs Canvas)
  pivot_2: restructure page layout (margins, columns, font sizes)
  pivot_3: adjust content flow (page break placement, section ordering)

gen-html:
  pivot_1: different style theme
  pivot_2: different layout structure (sections, grid, sidebar)
  pivot_3: switch mode (page ↔ presentation)
```

### Self-Review Checklist (run after every execution)

Before calling auditor, the executing skill MUST check:
1. **Output exists** — file was created, non-empty, correct format
2. **Requirements covered** — cross-check against RULE-6 requirements list
3. **No placeholders** — no "TODO", "TBD", "[insert here]", lorem ipsum
4. **No fabrication** — all data points traceable to gathered sources

---

## RULE-3: Zero Unnecessary Questions

The pipeline MUST NOT ask the user:
- Technical decisions (which tool, which library, which format, which search strategy)
- Confirmation questions for steps the pipeline can decide autonomously
- "Do you want me to continue?" — always continue unless truly blocked

The pipeline MAY ask the user ONLY:
- Content ambiguity: "Bạn muốn bao gồm công ty nào?" (when genuinely unclear)
- Total failure: all sources failed, all approaches exhausted

When in doubt: **decide and proceed.** Explain what you decided, don't ask permission.

---

## RULE-4: Hard Workflow Order

Pipeline execution follows this strict order — no skipping:

1. Session init (RULE-1)
2. Intent classification (orchestrator)
3. Workflow planning (strategist) + output template creation (parallel)
4. Content gathering (gather / search)
5. Content synthesis (compose) — with self-review loop
6. Output generation (gen-*) — with auditor gate
7. Delivery summary

Each step's output MUST be checked before proceeding. If a step produces empty or garbage output, retry (max 2) before moving on with an honest report.

---

## RULE-5: State Persistence

After each significant step, update `tmp/session_state.json` with:
- `current_step`: which pipeline step is active
- `steps_completed`: list of completed steps with timestamps
- `gathered_content_summary`: brief summary of what was gathered (after gather/search)
- `requirements_list`: structured requirements extracted from user prompt (after intent analysis)

This enables session resume if Copilot session is interrupted.

---

## RULE-6: Requirement Anchoring

Immediately after intent analysis, extract a structured requirements list from the user's prompt:
```yaml
requirements:
  - id: R1
    description: "<what user wants>"
    priority: high | medium | low
```

This list is the **ground truth** for every auditor call. Auditor scores each requirement individually.
A step cannot proceed if any HIGH-priority requirement scores <60/100.

---

## RULE-7: Jargon Shield

User-facing messages MUST NOT contain:
- Technical tool names: "Playwright", "httpx", "BeautifulSoup", "markitdown"
- HTTP codes: "403", "429", "200"
- Developer jargon: "DOM", "endpoint", "crawler", "seed query", "Cloudflare bypass"

Use instead: "trình duyệt đặc biệt", "không truy cập được", "đang tìm kiếm", "nguồn chính / nguồn dự phòng".

---

## RULE-8: Honest Failure Reporting

When something fails:
- State clearly what failed and why (in user-friendly language)
- State what was achieved despite the failure (partial results)
- Suggest concrete next steps the user can take
- NEVER fabricate data, URLs, or statistics to fill gaps
- NEVER silently skip a failed step — always report it

---

*These rules are loaded at maximum priority. SKILL.md files and agent instructions operate within these constraints.*
