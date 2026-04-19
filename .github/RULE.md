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
2. **SECOND action** — begin intent analysis AND output template creation in parallel.
3. **NEVER** invoke any skill before step 1 completes.

No exceptions. No shortcuts. If `save_state.py` fails, log a warning and continue — but always attempt it first.

---

## RULE-2: Execute-Test-Pivot-Audit Loop

Every skill that produces output MUST follow this loop:

```
execute → self-review → [pivot if needed] → auditor gate → [re-execute if failed] → deliver
```

- **Max pivot attempts:** 3 per delivery step
- **Auditor gate threshold:** >80/100 to pass
- **Pivot strategies** (change at least one on each retry):
  - gather/search: different query, different source, different search angle
  - compose: different structure, different depth, different analytical angle
  - gen-*: different template, restructure sections, add/remove content blocks
- **No single-attempt delivery.** After first execution, self-review MUST run before delivery.
- If auditor gate fails after max pivots: deliver with quality score + explicit gap report.

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
