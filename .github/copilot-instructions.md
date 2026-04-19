# Copilot Instructions — InsightEngine

<!-- Version: 2.0 | Product: insight-engine | Updated: 2026-04-20 -->
<!-- OPTIMIZED: Slim surface — skill details loaded on-demand via SKILL.md -->

This file is read automatically by GitHub Copilot.

---

## ⚠️ RULE.md — Non-Negotiable Pipeline Rules

READ `.github/RULE.md` at session start. It overrides ALL skill/agent instructions.
Route user prompts to orchestrator agent for intent classification and pipeline management.

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
| search | Internet search, platform discovery, data collection | tìm kiếm, search, danh sách |
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

## Agents (invoked on-demand)

| Agent | Purpose | User-invocable |
|-------|---------|---------------|
| orchestrator | Intent classification → routing → pipeline management | ✅ |
| auditor | Quality verification — 100-point weighted scoring | ✅ |
| strategist | Workflow generation — execution plan with quality gates | ❌ |
| advisory | Multi-perspective decision support | ❌ |

---

## Pipeline Flow

1. User request → orchestrator classifies intent → strategist generates plan
2. search/gather → compose → gen-[format] (with per-step auditor checkpoints)
3. Output chaining supported: Excel → chart → PPT
4. Style inference: formal → corporate, research → academic, tech → dark-modern

---

**Version:** 2.0
**Activated:** 2026-04-20
