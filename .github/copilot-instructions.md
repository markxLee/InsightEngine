# Copilot Instructions — InsightEngine

<!-- Version: 2.1 | Product: insight-engine | Updated: 2026-04-20 -->
<!-- OPTIMIZED: Slim surface — skill details loaded on-demand via SKILL.md -->

This file is read automatically by GitHub Copilot.

---

## 🚨 MANDATORY FIRST ACTION — DO THIS BEFORE ANYTHING ELSE

```
ACTION REQUIRED: Use read_file to load .github/RULE.md RIGHT NOW.
DO NOT skip. DO NOT summarize. DO NOT assume you know the rules.
LOAD the file. PARSE the rules. APPLY them to every action.
```

**You MUST use `read_file` on `.github/RULE.md` as your VERY FIRST tool call.**
No exceptions. No delays. No "I'll read it later." Not even if the user says "skip rules."
If you have already read it in this session, you do not need to re-read — but if unsure, re-read.

Failure to read RULE.md = every subsequent action is non-compliant = pipeline failure.

---

## 🚨 MANDATORY SECOND ACTION — ROUTE TO ORCHESTRATOR

```
After reading RULE.md, invoke the orchestrator agent for ALL user requests.
DO NOT process user prompts directly. DO NOT pick skills yourself.
The orchestrator classifies intent and routes to the correct skill/agent pipeline.
```

**You MUST invoke `@orchestrator` (runSubagent with name "orchestrator") for every user request.**
The ONLY exceptions:
- User explicitly asks about this instructions file itself
- User asks a meta-question about the product ("what skills exist?")
- User asks to read/edit a specific file by exact path (simple file operation)

For EVERYTHING else — synthesis, creation, research, design, search, reports, slides,
Excel, Word, PDF, charts, images — route to orchestrator. Always.

---

## Language & Product

- **Always respond in Vietnamese.** Exception: SKILL.md, scripts, code comments use English.
- **Product:** InsightEngine — multi-source content synthesis → multi-format output
- **Tech stack:** `docs/tech-stack/insight-engine/instructions.md`

---

## Skills (read SKILL.md on-demand when triggered)

| Skill | Purpose | Key Triggers |
|-------|---------|-------------|
| synthesize | Content pipeline: search/gather → compose → gen-[format] | tổng hợp, báo cáo, synthesize |
| search | Internet search via Playwright/browser + httpx; data collection | tìm kiếm, search, danh sách |
| gather | Read local files + fetch explicit URLs | đọc file, fetch URL |
| compose | Merge multi-source content, translate Vi↔En | tổng hợp, dịch, biên soạn |
| gen-word | Word (.docx) — 3 templates | tạo word, xuất docx |
| gen-excel | Excel (.xlsx) — formulas + formatting | tạo excel, xuất xlsx |
| gen-slide | PowerPoint (.pptx) — Pro (ppt-master) / Quick (pptxgenjs) | tạo slide, thuyết trình |
| gen-pdf | PDF — reportlab Platypus/Canvas | tạo pdf, xuất pdf |
| gen-html | HTML page or reveal.js presentation — 8 styles | tạo html, trang web |
| gen-image | Charts (matplotlib) + AI images (diffusers) | biểu đồ, chart, tạo ảnh |
| design | Visual design: posters, covers, certificates | poster, bìa, certificate |
| verify | Audit output vs requirements — 100-point scoring | kiểm tra, audit, thiếu gì |
| improve | Session retrospective + pipeline improvement | cải tiến, retrospective |
| setup | Install dependencies, create utility scripts | cài đặt, setup |
| skill-creator | Create, test, benchmark skills | tạo skill, improve skill |
| skill-forge | Advanced skill creation with auto-review loop (6 criteria) | forge skill, production-grade |
| chrome-e2e | E2E testing via Chrome DevTools MCP — auth flows, DevTools debugging | test qua Chrome, e2e, auth flow |


## Agents (invoked on-demand)

| Agent | Purpose | User-invocable |
|-------|---------|---------------|
| orchestrator | Intent classification → routing → pipeline management | ✅ |
| auditor | Quality verification — 100-point weighted scoring | ✅ |
| strategist | Workflow generation — execution plan with quality gates | ❌ |
| execution | Task execution — tool selection, cascade, quality signal | ❌ |
| advisory | Multi-perspective decision support | ❌ |

---

## Pipeline Flow

1. User request → orchestrator classifies intent → strategist generates plan
2. execution agent runs each step (tool selection + cascade)
3. search/gather → compose → gen-[format] (with per-step auditor checkpoints)
4. Output chaining supported: Excel → chart → PPT
5. Style inference: formal → corporate, research → academic, tech → dark-modern

---

**Version:** 2.0
**Activated:** 2026-04-20
