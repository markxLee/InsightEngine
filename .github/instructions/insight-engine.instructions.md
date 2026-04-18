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
- **Strict file placement**: Scripts → `/scripts`, temp files → `/tmp`, output → `/output`, input → `/input`. Validated at pipeline start and after each step.

---

## Vietnamese Language Rules

- All Copilot responses to user: **tiếng Việt**
- Skill names and directories: **tiếng Việt**, lowercase, hyphenated
- Skill triggers: **bilingual** (Vietnamese primary, English secondary)
- Skill SKILL.md content (instructions to Copilot): **English**
- Scripts: comments in English; CLI help text in English

---

## Skill System

```
.github/skills/
  tong-hop/      # 🔑 Pipeline chính — phân tích prompt → mở rộng → route → orchestrate + auto-review loop
  thu-thap/      # Thu thập từ web (search + fetch) và đọc file + auto quality check + data collection mode
  bien-soan/     # Tổng hợp nội dung comprehensive (default) + self-review loop + dịch thuật
  tao-word/      # Xuất Word (.docx) + thin content guard
  tao-excel/     # Xuất Excel (.xlsx)
  tao-slide/     # Xuất PowerPoint (.pptx) + thin content guard
  tao-pdf/       # Xuất PDF + thin content guard
  tao-html/      # Xuất HTML + thin content guard
  tao-hinh/      # Biểu đồ + hình ảnh
  thiet-ke/      # Thiết kế visual (poster, bìa, certificate, banner)
  kiem-tra/      # Audit output vs yêu cầu user (Step 4.7 trong pipeline + standalone)
  cai-tien/      # Session retrospective + continuous improvement
```

Full stack documentation: `docs/tech-stack/insight-engine/instructions.md`
