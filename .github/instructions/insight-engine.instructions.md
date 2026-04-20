---
description: "InsightEngine — Content synthesis pipeline. Tech stack and coding conventions."
applyTo: "**"
---

# InsightEngine — Active Tech Stack Instructions

> **Product:** InsightEngine  
> **Product Slug:** insight-engine  
> **Activated:** 2026-04-16  
> **Stack Review:** READY (26/30)  
> **Full instructions:** docs/tech-stack/insight-engine/instructions.md

---

## Stack Quick Reference

| Layer | Technology |
|-------|-----------|
| AI / Reasoning | GitHub Copilot (Claude) |
| File reading | `markitdown[all]` |
| Word output | `python-docx` |
| Excel output | `openpyxl` + `pandas` |
| PPT output | `pptxgenjs` (Node.js) quick mode; `ppt-master` SVG→PPTX pro mode |
| PDF output | `reportlab` + `pypdf` |
| HTML output | `jinja2` + inline CSS |
| Charts | `matplotlib` + `seaborn` (Agg backend) |
| Images | `diffusers` + `torch/MPS` (Apple Silicon, optional) |
| Visual design | `reportlab` Canvas + `Pillow` (80+ bundled fonts) |
| Web search | `vscode-websearchforcopilot_webSearch` (built-in) |
| URL fetch | Copilot `fetch_webpage` (built-in) |

---

## Critical Rules (Always Apply)

- Always `matplotlib.use('Agg')` before any other matplotlib import
- Never hardcode calculated values in Excel — use `=FORMULA()`
- Always run `scripts/recalc.py` after writing Excel formulas
- Never use `\n` in python-docx paragraphs — use separate Paragraph objects
- Never use `#` prefix for colors in pptxgenjs (`"FF5733"` not `"#FF5733"`)
- Never use `WidthType.PERCENTAGE` for docx tables — use `WidthType.DXA`
- All scripts must accept CLI arguments — no hardcoded paths
- Always print output file path + size as last line of every script
- markitdown first; if empty/garbled → format-specific fallback library
- **Default content depth is COMPREHENSIVE** — expert-level, rich content. Only use standard when user explicitly asks for brevity.
- **Auto-review every pipeline step** — check quality after each sub-skill, loop back if insufficient (max 2 retries)
- **Strict file placement**: Reusable utility scripts → `/scripts`, one-time/session scripts + temp files → `/tmp`, output → `/output`, input → `/input`. Validated at pipeline start and after each step.

---

## Vietnamese Language Rules

- All Copilot responses to user: **tiếng Việt**
- Skill names and directories: **English**, lowercase, hyphenated
- Skill triggers: **bilingual** (Vietnamese primary, English secondary)
- Skill SKILL.md content (instructions to Copilot): **English**
- Scripts: comments in English; CLI help text in English

---

## Skill System

```
.github/skills/
  synthesize/      # 🔑 Main pipeline — analyze prompt → expand dimensions → route → orchestrate + auto-review loop
  search/          # Web search via vscode-websearchforcopilot_webSearch + 3-tier URL fetch (fetch_webpage → httpx → Playwright)
  gather/          # Read local files (markitdown + format-specific fallbacks) and fetch explicit user-provided URLs
  compose/         # Synthesize content comprehensive (default) + self-review loop + translation
  gen-word/        # Export Word (.docx) + thin content guard
  gen-excel/       # Export Excel (.xlsx)
  gen-slide/       # Export PowerPoint (.pptx) + thin content guard
  gen-pdf/         # Export PDF + thin content guard
  gen-html/        # Export HTML + thin content guard
  gen-image/       # Charts + images
  design/          # Visual design (poster, cover, certificate, banner)
  verify/          # Audit output vs user requirements (Step 4.7 in pipeline + standalone)
  improve/         # Session retrospective + continuous improvement
  setup/           # Install dependencies + create utility scripts
  skill-creator/   # Create, improve, test, benchmark skills
  skill-forge/     # Advanced auto-review loop — grade 6 criteria (A/B/C/D), iterate until all A
```

## Agent System

```
.github/agents/
  orchestrator.agent.md   # User-invocable. Central request handler — classify intent → route
  strategist.agent.md     # Subagent. Workflow generation (initial_plan / replan / child_workflow)
  execution.agent.md      # Subagent. Task execution — tool selection, cascade, quality signal
  auditor.agent.md        # User-invocable. 100-point weighted quality verification
  advisory.agent.md       # Subagent. Multi-perspective decision support
```

Full stack documentation: `docs/tech-stack/insight-engine/instructions.md`
