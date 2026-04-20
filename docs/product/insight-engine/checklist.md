# InsightEngine — Product Checklist

> **Product:** InsightEngine  
> **Product Slug:** insight-engine  
> **Created:** 2026-04-16  
> **Total User Stories:** 159 (21 Phase 0-3 DONE + 15 Phase 4 DONE + 4 Phase 5 DONE + 14 Phase 6 DONE + 5 Phase 7 DONE + 6 Phase 8 DONE + 12 Phase 9 DONE + 13 Phase 10 DONE + 1 Phase 10 PLANNED + 6 Phase 11 DONE + 8 Phase 12 DONE + 9 Phase 13 DONE + 6 Phase 14 DONE + 12 Phase 15 DONE + 9 Phase 16 DONE + 9 Phase 17 PLANNED + 9 Phase 18 PLANNED)  
> **Purpose:** Single source of execution state — track progress, enforce dependencies, enable safe parallel work

---

## Product Checklist Overview

- **Product name:** InsightEngine
- **Product slug:** `insight-engine`
- **Checklist purpose:** Track execution state of all user stories across phases, enforce dependency rules, enable pause/resume

### Status Legend

| Status | Meaning |
|--------|---------|
| PLANNED | Not started |
| IN_PROGRESS | Currently being implemented |
| DONE | Completed and verified |

### Rules

- A story may move to IN_PROGRESS **only** if all stories in its "Blocked By" list are DONE
- Stories with `Blocked By: None` can start immediately

---

## Phase 0: Product Foundation

### Epic 0.1: Workspace Setup

- [x] **US-0.1.1** — Repo structure & Copilot configuration
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-0.1.1
  - Blocked By: None

### Epic 0.2: Cài đặt môi trường (`cai-dat`)

- [x] **US-0.2.1** — Dependency check script
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-0.2.1
  - Blocked By: None

- [x] **US-0.2.2** — Setup skill (`cai-dat`)
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-0.2.2
  - Blocked By: ~~US-0.2.1~~ ✅

### Epic 0.3: Pipeline Chính (`tong-hop`)

- [x] **US-0.3.1** — Pipeline skill skeleton with intent routing
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-0.3.1
  - Blocked By: ~~US-0.1.1~~ ✅, ~~US-0.2.2~~ ✅

- [x] **US-0.3.2** — Setup check before each pipeline process
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-0.3.2
  - Blocked By: ~~US-0.3.1~~ ✅

---

## Phase 1: MVP — Thu thập & Xuất cơ bản

### Epic 1.1: Thu thập nội dung (`thu-thap`)

- [x] **US-1.1.1** — Read local files via markitdown
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-1.1.1
  - Blocked By: ~~US-0.3.2~~ ✅

- [x] **US-1.1.2** — Fetch URL content
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-1.1.2
  - Blocked By: ~~US-1.1.1~~ ✅

### Epic 1.2: Biên soạn nội dung (`bien-soan`)

- [x] **US-1.2.1** — Multi-source content synthesis
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-1.2.1
  - Blocked By: ~~US-0.3.2~~ ✅

- [x] **US-1.2.2** — Basic translation Vietnamese ↔ English
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-1.2.2
  - Blocked By: ~~US-1.2.1~~ ✅

### Epic 1.3: Xuất Word (`tao-word`)

- [x] **US-1.3.1** — Word document output with 3 template styles
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-1.3.1
  - Blocked By: ~~US-1.2.1~~ ✅, ~~US-1.1.1~~ ✅

### Epic 1.4: Xuất PowerPoint (`tao-slide`)

- [x] **US-1.4.1** — PowerPoint output with 3 template styles
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-1.4.1
  - Blocked By: ~~US-1.2.1~~ ✅, ~~US-1.1.1~~ ✅

---

## Phase 2: Mở rộng — Tìm kiếm & Thêm định dạng

### Epic 2.1: Tìm kiếm Google tự động

- [x] **US-2.1.1** — Web search integration in thu-thap
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-2.1.1
  - Blocked By: ~~US-1.1.1~~ ✅

### Epic 2.2: Xuất Excel (`tao-excel`)

- [x] **US-2.2.1** — Excel output with formulas and formatting
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-2.2.1
  - Blocked By: ~~US-1.2.1~~ ✅

### Epic 2.3: Xuất PDF (`tao-pdf`)

- [x] **US-2.3.1** — PDF output from synthesized content
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-2.3.1
  - Blocked By: ~~US-1.2.1~~ ✅

### Epic 2.4: Xuất HTML (`tao-html`)

- [x] **US-2.4.1** — Static HTML page output with 3 template styles
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-2.4.1
  - Blocked By: ~~US-1.2.1~~ ✅

### Epic 2.5: Chaining Output

- [x] **US-2.5.1** — Pipeline output chaining
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-2.5.1
  - Blocked By: ~~US-1.3.1~~ ✅, ~~US-1.4.1~~ ✅, ~~US-2.2.1~~ ✅

---

## Phase 3: Hoàn thiện — Trực quan & Tối ưu

### Epic 3.1: Biểu đồ & Hình ảnh (`tao-hinh`)

- [x] **US-3.1.1** — Chart generation from data
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-3.1.1
  - Blocked By: ~~US-2.2.1~~ ✅

- [x] **US-3.1.2** — Image generation for slides (Apple Silicon)
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-3.1.2
  - Blocked By: ~~US-3.1.1~~ ✅

### Epic 3.2: Xử lý tài liệu lớn

- [x] **US-3.2.1** — Large document chunking strategy
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-3.2.1
  - Blocked By: ~~US-1.2.1~~ ✅

### Epic 3.3: Template Library mở rộng

- [x] **US-3.3.1** — Additional template styles (dark/modern, creative)
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-3.3.1
  - Blocked By: ~~US-1.3.1~~ ✅, ~~US-1.4.1~~ ✅, ~~US-2.4.1~~ ✅

### Epic 3.4: Cải thiện UX Pipeline

- [x] **US-3.4.1** — Pipeline UX improvements
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-3.4.1
  - Blocked By: ~~US-0.3.1~~ ✅, ~~US-2.5.1~~ ✅

---

## Phase 4: Nâng cấp — Template Library, Presentation HTML & Script Architecture

> **Nguồn gốc:** Phản hồi từ testing Phase 0-3. **15 stories PLANNED.**

### Epic 4.1: Template Library PPTX

- [x] **US-4.1.1** — Professional PPTX template collection
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.1.1
  - Blocked By: ~~US-1.4.1~~ ✅, ~~US-3.3.1~~ ✅
  - Refs: slidemembers.com, aippt.com, canva.com

- [x] **US-4.1.2** — Template preview and selection
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.1.2
  - Blocked By: ~~US-4.1.1~~ ✅

- [x] **US-4.1.3** — PPTX script architecture
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.1.3
  - Blocked By: ~~US-4.1.1~~ ✅
  - Refs: a-z-copilot-flow/skills/pptx/scripts/

### Epic 4.2: HTML Presentation Mode (reveal.js)

- [x] **US-4.2.1** — reveal.js integration for tao-html
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.2.1
  - Blocked By: ~~US-2.4.1~~ ✅, ~~US-3.3.1~~ ✅
  - Refs: revealjs.com, slides.com/templates

- [x] **US-4.2.2** — Transitions, animations, and visual effects
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.2.2
  - Blocked By: ~~US-4.2.1~~ ✅
  - Refs: revealjs.com, deckdeckgo.com

- [x] **US-4.2.3** — HTML presentation themes and backgrounds
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.2.3
  - Blocked By: ~~US-4.2.1~~ ✅
  - Refs: slides.com/templates, deckdeckgo.com

### Epic 4.3: Script Architecture cho Skills

- [x] **US-4.3.1** — tao-slide scripts/ directory
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.3.1
  - Blocked By: ~~US-4.1.3~~ ✅
  - Refs: a-z-copilot-flow/skills/pptx/scripts/

- [x] **US-4.3.2** — tao-html scripts/ directory
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.3.2
  - Blocked By: ~~US-4.2.1~~ ✅

- [x] **US-4.3.3** — Script architecture for remaining output skills
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.3.3
  - Blocked By: ~~US-4.3.1~~ ✅, ~~US-4.3.2~~ ✅
  - Refs: a-z-copilot-flow/skills/gen-image

### Epic 4.4: Nâng cấp Content Depth

- [x] **US-4.4.1** — bien-soan comprehensive mode
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.4.1
  - Blocked By: ~~US-1.2.1~~ ✅, ~~US-3.2.1~~ ✅

- [x] **US-4.4.2** — Content enrichment from multiple sources
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.4.2
  - Blocked By: ~~US-2.1.1~~ ✅, ~~US-4.4.1~~ ✅

### Epic 4.5: Template Library HTML

- [x] **US-4.5.1** — HTML reveal.js template collection
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.5.1
  - Blocked By: ~~US-4.2.1~~ ✅, ~~US-4.2.3~~ ✅
  - Refs: slides.com/templates, deckdeckgo.com

- [x] **US-4.5.2** — Presenter notes and PDF export
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.5.2
  - Blocked By: ~~US-4.5.1~~ ✅
  - Refs: revealjs.com

---

### Execution Order (Recommended)

```
Wave 1 (parallel): US-0.1.1, US-0.2.1
Wave 2:            US-0.2.2
Wave 3:            US-0.3.1
Wave 4:            US-0.3.2
Wave 5 (parallel): US-1.1.1, US-1.2.1
Wave 6 (parallel): US-1.1.2, US-1.2.2, US-2.1.1, US-2.2.1, US-2.3.1, US-2.4.1, US-3.2.1
Wave 7 (parallel): US-1.3.1, US-1.4.1
Wave 8 (parallel): US-2.5.1, US-3.1.1, US-3.3.1
Wave 9 (parallel): US-3.1.2, US-3.4.1
--- Phase 0-3 DONE (21/21) ---
Wave 10 (parallel): US-4.1.1, US-4.2.1, US-4.4.1
Wave 11 (parallel): US-4.1.2, US-4.1.3, US-4.2.2, US-4.2.3, US-4.4.2
Wave 12 (parallel): US-4.3.1, US-4.3.2, US-4.5.1
Wave 13 (parallel): US-4.3.3, US-4.5.2
--- Phase 4 DONE (15/15) ---
Wave 14 (parallel): US-5.1.1, US-5.2.1
Wave 15 (sequential): US-5.1.2 (after 5.1.1), US-5.2.2 (after 5.2.1)
```

---

## Phase 5: Tối ưu & Độ bền

### Epic 5.1: Small Model Optimization

- [x] **US-5.1.1** — Small model compatibility research
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-5.1.1
  - Blocked By: None

- [x] **US-5.1.2** — SKILL.md refactor for small model compatibility
  - Status: DONE ✅
  - Assignee: copilot
  - Branch: feature/insight-engine-us-5.1.2
  - Blocked By: ~~US-5.1.1~~ ✅

### Epic 5.2: Session State Persistence

- [x] **US-5.2.1** — Session state save after each pipeline step
  - Status: DONE ✅
  - Assignee: copilot
  - Branch: feature/insight-engine-us-5.2.1
  - Blocked By: None

- [x] **US-5.2.2** — Pipeline resume from saved state
  - Status: DONE ✅
  - Assignee: copilot
  - Branch: feature/insight-engine-us-5.2.2
  - Blocked By: ~~US-5.2.1~~ ✅

---

## Phase 6: Agent Architecture & Quality Gates

> **Nguồn gốc:** Phản hồi từ real-world usage. **14 stories PLANNED.**

### Epic 6.1: Strict File Rules & Auto-escalation

- [x] **US-6.1.1** — Strict file location rules enforcement
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-6.1.1
  - Blocked By: None

- [x] **US-6.1.2** — Auto-escalation protocol
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-6.1.2
  - Blocked By: ~~US-6.1.1~~ ✅

### Epic 6.2: Shared Context Protocol

- [x] **US-6.2.1** — Shared context file design
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-6.2.1
  - Blocked By: None

- [x] **US-6.2.2** — Agent context read/write API
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-6.2.2
  - Blocked By: ~~US-6.2.1~~ ✅

### Epic 6.3: Model Profile & Decision Maps

- [x] **US-6.3.1** — Decision maps per capability category
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-6.3.1
  - Blocked By: None

- [x] **US-6.3.2** — Model self-declaration with fallback
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-6.3.2
  - Blocked By: ~~US-6.3.1~~ ✅, ~~US-6.2.1~~ ✅

- [x] **US-6.3.3** — Pre-built workflow templates
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-6.3.3
  - Blocked By: ~~US-6.3.1~~ ✅

### Epic 6.4: Agent Strategist

- [x] **US-6.4.1** — Strategist agent — dynamic workflow generation
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-6.4.1
  - Blocked By: ~~US-6.3.2~~ ✅, ~~US-6.3.3~~ ✅, ~~US-6.2.1~~ ✅

### Epic 6.5: Tiered Audit System

- [x] **US-6.5.1** — Tiered audit implementation
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-6.5.1
  - Blocked By: ~~US-6.2.1~~ ✅

- [x] **US-6.5.2** — Final output audit with step-level rollback
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-6.5.2
  - Blocked By: ~~US-6.5.1~~ ✅, ~~US-6.4.1~~ ✅

### Epic 6.6: Advisory Agent & Conditional Skill Creation

- [x] **US-6.6.1** — Advisory agent — multi-perspective single-call
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-6.6.1
  - Blocked By: ~~US-6.2.1~~ ✅

- [x] **US-6.6.2** — Conditional skill-forge runtime
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-6.6.2
  - Blocked By: ~~US-6.6.1~~ ✅

- [x] **US-6.6.3** — Public skill clone with security check
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-6.6.3
  - Blocked By: ~~US-6.6.2~~ ✅

### Epic 6.7: Pipeline Integration

- [x] **US-6.7.1** — tong-hop integration with AGENT_MODE feature flag
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-6.7.1
  - Blocked By: ~~US-6.4.1~~ ✅, ~~US-6.5.1~~ ✅, ~~US-6.6.1~~ ✅

---

## Phase 7: Pipeline Enforcement & Compliance Hardening

> **Nguồn gốc:** Real-world testing — model skip critical steps khi instructions nằm trong reference files. **5 stories PLANNED.**

### Epic 7.1: Inline Critical Steps & Hard Gates

- [x] **US-7.1.1** — Inline request analysis and REQUEST_TYPE detection
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-7.1.1
  - Blocked By: None

- [x] **US-7.1.2** — Hard confirmation gate before execution
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-7.1.2
  - Blocked By: ~~US-7.1.1~~ ✅

### Epic 7.2: Data Collection Enforcement

- [x] **US-7.2.1** — Inline data collection protocol in thu-thap
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-7.2.1
  - Blocked By: None

- [x] **US-7.2.2** — Pre-output URL validation gate
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-7.2.2
  - Blocked By: ~~US-7.2.1~~ ✅

### Epic 7.3: Visible Pipeline Trace

- [x] **US-7.3.1** — Numbered step trace with live progress
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-7.3.1
  - Blocked By: None

---

## Phase 8: Shared Copilot Agent Architecture

> Refactor agents from Phase 6 inline instructions → standalone shared Copilot agents (`runSubagent`).

### Epic 8.1: Shared Auditor Agent

- [x] **US-8.1.1** — Auditor as standalone Copilot agent
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-8.1.1
  - Blocked By: None

- [x] **US-8.1.2** — Auditor integration into output skills
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-8.1.2
  - Blocked By: ~~US-8.1.1~~ ✅

### Epic 8.2: Shared Strategist Agent

- [x] **US-8.2.1** — Strategist as standalone Copilot agent
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-8.2.1
  - Blocked By: None

### Epic 8.3: Shared Advisory Agent

- [x] **US-8.3.1** — Advisory as standalone Copilot agent
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-8.3.1
  - Blocked By: None

### Epic 8.4: Agent Integration Protocol

- [x] **US-8.4.1** — Standardized agent calling protocol
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-8.4.1
  - Blocked By: ~~US-8.1.1~~ ✅, ~~US-8.2.1~~ ✅, ~~US-8.3.1~~ ✅

- [x] **US-8.4.2** — tong-hop migration to shared agents
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-8.4.2
  - Blocked By: ~~US-8.4.1~~ ✅

---

## Phase 9: Central Orchestrator & Adaptive Self-Improvement

> Tách orchestration khỏi tổng hợp nội dung. Agent trung tâm, tự cải thiện thích ứng, audit thang 100 điểm, resume xuyên session, chuẩn hóa agents theo VS Code custom agent standard (`.github/agents/*.agent.md`).

### Epic 9.1: Central Orchestrator (`dieu-phoi`)

- [x] **US-9.1.1** — Central orchestrator agent skeleton
  - Status: DONE
  - Assignee: Copilot
  - Branch: feature/insight-engine-us-9.1.1
  - Blocked By: ~~US-8.4.2~~ ✅

- [x] **US-9.1.2** — tong-hop refactor to synthesis-only
  - Status: DONE
  - Assignee: Copilot
  - Branch: feature/insight-engine-us-9.1.2
  - Blocked By: ~~US-9.1.1~~ ✅

- [x] **US-9.1.3** — dieu-phoi integration with shared agents
  - Status: DONE
  - Assignee: Copilot
  - Branch: feature/insight-engine-us-9.1.3
  - Blocked By: ~~US-9.1.1~~ ✅

### Epic 9.2: Adaptive Self-Improvement

- [x] **US-9.2.1** — Capability gap evaluation protocol
  - Status: DONE
  - Assignee: Copilot
  - Branch: feature/insight-engine-us-9.2.1
  - Blocked By: ~~US-9.1.1~~ ✅

- [x] **US-9.2.2** — Runtime agent creation with user consent
  - Status: DONE
  - Assignee: Copilot
  - Branch: feature/insight-engine-us-9.2.2
  - Blocked By: ~~US-9.2.1~~ ✅

- [x] **US-9.2.3** — Runtime skill creation/upgrade
  - Status: DONE
  - Assignee: Copilot
  - Branch: feature/insight-engine-us-9.2.3
  - Blocked By: ~~US-9.2.1~~ ✅

### Epic 9.3: Enhanced Working State & Cross-Session Resume

- [x] **US-9.3.1** — Enhanced session state schema
  - Status: DONE
  - Assignee: Copilot
  - Branch: feature/insight-engine-us-9.3.1
  - Blocked By: ~~US-5.2.1~~ ✅

- [x] **US-9.3.2** — Step-level state persistence
  - Status: DONE
  - Assignee: Copilot
  - Branch: feature/insight-engine-us-9.3.2
  - Blocked By: ~~US-9.3.1~~ ✅

- [x] **US-9.3.3** — Cross-session resume
  - Status: DONE
  - Assignee: Copilot
  - Branch: feature/insight-engine-us-9.3.3
  - Blocked By: ~~US-9.3.2~~ ✅

### Epic 9.4: 100-Point Weighted Audit Scoring

- [x] **US-9.4.1** — 100-point audit scoring system
  - Status: DONE
  - Assignee: Copilot
  - Branch: feature/insight-engine-us-9.4.1
  - Blocked By: ~~US-8.1.1~~ ✅

- [x] **US-9.4.2** — Targeted retry loop with score tracking
  - Status: DONE
  - Assignee: Copilot
  - Branch: feature/insight-engine-us-9.4.2
  - Blocked By: ~~US-9.4.1~~ ✅

### Epic 9.5: VS Code Custom Agent Standard Migration

- [x] **US-9.5.1** — Migrate existing agents to .agent.md format
  - Status: DONE
  - Assignee: Copilot
  - Branch: feature/insight-engine-us-9.5.1
  - Blocked By: ~~US-8.1.1~~ ✅, ~~US-8.2.1~~ ✅, ~~US-8.3.1~~ ✅

---

## Phase 10: English Naming, Natural Language UX & Product Alignment

> Chuẩn hóa tên skill/agent sang tiếng Anh, UX ngôn ngữ tự nhiên, dọn dẹp legacy, bổ sung stories thiếu. **14 stories PLANNED.**

### Epic 10.1: Rename Skills to English

- [x] **US-10.1.1** — Rename all skill directories from Vietnamese to English
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-10.1.1
  - Blocked By: None

- [x] **US-10.1.2** — Update SKILL.md triggers for renamed skills
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-10.1.2
  - Blocked By: ~~US-10.1.1~~ ✅

### Epic 10.2: Rename Agents to English

- [x] **US-10.2.1** — Rename dieu-phoi agent to orchestrator
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-10.2.1
  - Blocked By: None

### Epic 10.3: Natural Language UX

- [x] **US-10.3.1** — Remove slash command dependency
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-10.3.1
  - Blocked By: ~~US-10.1.2~~ ✅, ~~US-10.2.1~~ ✅

- [x] **US-10.3.2** — Update README for natural language UX
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-10.3.2
  - Blocked By: ~~US-10.3.1~~ ✅

### Epic 10.4: copilot-instructions.md Refresh

- [x] **US-10.4.1** — Update skill registry with English names
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-10.4.1
  - Blocked By: ~~US-10.1.1~~ ✅, ~~US-10.2.1~~ ✅

- [x] **US-10.4.2** — Fix stale PIPELINE_FLOW and update Vietnamese Language Rules
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-10.4.2
  - Blocked By: ~~US-10.4.1~~ ✅

### Epic 10.5: Clean Up Legacy Artifacts

- [x] **US-10.5.1** — Remove shared-agents directory
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-10.5.1
  - Blocked By: None

- [x] **US-10.5.2** — Remove duplicate agent files
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-10.5.2
  - Blocked By: ~~US-10.5.1~~ ✅

### Epic 10.6: Backfill Missing Skill Stories

- [x] **US-10.6.1** — design skill user story (formerly thiet-ke)
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-10.6.1-2-3
  - Blocked By: ~~US-10.1.1~~ ✅

- [x] **US-10.6.2** — verify skill user story (formerly kiem-tra)
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-10.6.1-2-3
  - Blocked By: ~~US-10.1.1~~ ✅

- [x] **US-10.6.3** — improve skill user story (formerly cai-tien)
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-10.6.1-2-3
  - Blocked By: ~~US-10.1.1~~ ✅

### Epic 10.7: Product Doc Alignment

- [x] **US-10.7.1** — Update instructions.md Vietnamese Language Rules
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-10.7.1`
  - Blocked By: ~~US-10.1.1~~ ✅

- [x] **US-10.7.2** — Final cross-document consistency check
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-10.7.2
  - Blocked By: ~~US-10.7.1~~ ✅

---

### Execution Order (Recommended)

```
Wave 1 (parallel): US-0.1.1, US-0.2.1
Wave 2:            US-0.2.2
Wave 3:            US-0.3.1
Wave 4:            US-0.3.2
Wave 5 (parallel): US-1.1.1, US-1.2.1
Wave 6 (parallel): US-1.1.2, US-1.2.2, US-2.1.1, US-2.2.1, US-2.3.1, US-2.4.1, US-3.2.1
Wave 7 (parallel): US-1.3.1, US-1.4.1
Wave 8 (parallel): US-2.5.1, US-3.1.1, US-3.3.1
Wave 9 (parallel): US-3.1.2, US-3.4.1
--- Phase 0-3 DONE (21/21) ---
Wave 10 (parallel): US-4.1.1, US-4.2.1, US-4.4.1
Wave 11 (parallel): US-4.1.2, US-4.1.3, US-4.2.2, US-4.2.3, US-4.4.2
Wave 12 (parallel): US-4.3.1, US-4.3.2, US-4.5.1
Wave 13 (parallel): US-4.3.3, US-4.5.2
--- Phase 4 DONE (15/15) ---
Wave 14 (parallel): US-5.1.1, US-5.2.1
Wave 15 (sequential): US-5.1.2 (after 5.1.1), US-5.2.2 (after 5.2.1)
--- Phase 5 DONE (4/4) ---
Wave 16 (parallel): US-6.1.1, US-6.2.1, US-6.3.1
Wave 17 (parallel): US-6.1.2, US-6.2.2, US-6.3.3, US-6.5.1, US-6.6.1
Wave 18 (parallel): US-6.3.2, US-6.4.1, US-6.6.2
Wave 19 (parallel): US-6.5.2, US-6.6.3, US-6.7.1
--- Phase 6 DONE (14/14) ---
Wave 20 (parallel): US-7.1.1, US-7.2.1, US-7.3.1
Wave 21 (sequential): US-7.1.2 (after 7.1.1), US-7.2.2 (after 7.2.1)
--- Phase 7 DONE (5/5) ---
Wave 22 (parallel): US-8.1.1, US-8.2.1, US-8.3.1
Wave 23 (sequential): US-8.1.2 (after 8.1.1)
Wave 24 (sequential): US-8.4.1 (after 8.1.1, 8.2.1, 8.3.1)
Wave 25 (sequential): US-8.4.2 (after 8.4.1)
--- Phase 8 DONE (6/6) ---
Wave 26 (parallel): US-9.1.1, US-9.4.1, US-9.5.1
Wave 27 (parallel): US-9.1.2, US-9.1.3, US-9.2.1, US-9.3.1
Wave 28 (parallel): US-9.2.2, US-9.2.3, US-9.3.2
Wave 29 (parallel): US-9.3.3, US-9.4.2
--- Phase 9 DONE (12/12) ---
Wave 30 (parallel): US-10.1.1, US-10.2.1, US-10.5.1
Wave 31 (parallel): US-10.1.2, US-10.4.1, US-10.5.2, US-10.6.1, US-10.6.2, US-10.6.3, US-10.7.1
Wave 32 (parallel): US-10.3.1, US-10.4.2, US-10.7.2
Wave 33 (sequential): US-10.3.2 (after 10.3.1)
--- Phase 10: 13 DONE, 1 PLANNED (US-10.7.1) ---

## Phase 11: Adaptive Search Intelligence

> Tìm kiếm thông minh thích ứng — per-step search planning, DOM exploration, detail URL extraction, adaptive flow advisor. **6 stories PLANNED.**

### Epic 11.1: Per-Step Search Planner

- [x] **US-11.1.1** — Integrate per-step search planner in gather skill
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-11.1.1`
  - Blocked By: None

### Epic 11.2: Source DOM Explorer

- [x] **US-11.2.1** — Auto DOM exploration when site-scoped search returns thin results
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-11.2.1`
  - Blocked By: ~~US-11.1.1~~ ✅

- [x] **US-11.2.2** — Internal search usage via DOM-discovered endpoints
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-11.2.2`
  - Blocked By: ~~US-11.2.1~~ ✅

### Epic 11.3: Detail URL Extractor

- [x] **US-11.3.1** — Extract canonical detail-page URLs for inline/popup detail sources
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-11.3.1`
  - Blocked By: ~~US-11.2.1~~ ✅

### Epic 11.4: Adaptive Flow Advisor

- [x] **US-11.4.1** — Advisory agent fallback after 2 failed search attempts
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-11.4.1`
  - Blocked By: ~~US-11.1.1~~ ✅

- [x] **US-11.4.2** — User-facing flow alternatives presentation
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-11.4.2`
  - Blocked By: ~~US-11.4.1~~ ✅

Wave 34 (sequential): US-11.1.1
Wave 35 (sequential): US-11.2.1 (after 11.1.1)
Wave 36 (parallel): US-11.2.2 (after 11.2.1), US-11.3.1 (after 11.2.1)
Wave 37 (sequential): US-11.4.1 (after 11.1.1)
Wave 38 (sequential): US-11.4.2 (after 11.4.1)
--- Phase 11 PLANNED (6/6) ---

## Phase 12: Autonomous Pipeline UX

> **Origin:** Real-world feedback — pipeline asks too many technical questions, exposes jargon, lacks autonomous execution. **8 stories PLANNED.**

### Epic 12.1: Fire-and-Forget Pipeline Mode

- [x] **US-12.1.1** — Default auto-execute mode after plan approval
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-12.1.1`
  - Blocked By: None

- [x] **US-12.1.2** — Content-only question filter (suppress technical prompts)
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-12.1.2`
  - Blocked By: US-12.1.1

### Epic 12.2: Technical Jargon Shield

- [x] **US-12.2.1** — Technical jargon blocklist for user messages
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-12.2.1`
  - Blocked By: None

- [x] **US-12.2.2** — User-friendly progress message templates
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-12.2.2`
  - Blocked By: US-12.2.1

### Epic 12.3: User Signal Detection & Mode Switching

- [x] **US-12.3.1** — User frustration signal detection
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-12.3.1`
  - Blocked By: None

- [x] **US-12.3.2** — Dynamic mode switching (interactive → autonomous)
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-12.3.2`
  - Blocked By: US-12.3.1, US-12.1.1

### Epic 12.4: Batch Progress Model for Data Collection

- [x] **US-12.4.1** — Batch progress reporting for data_collection
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-12.4.1`
  - Blocked By: None

- [x] **US-12.4.2** — Final delivery summary (single message with all outputs)
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-12.4.2`
  - Blocked By: US-12.4.1

```
Wave 39 (parallel): US-12.1.1, US-12.2.1, US-12.3.1, US-12.4.1
Wave 40 (parallel): US-12.1.2 (after 12.1.1), US-12.2.2 (after 12.2.1)
Wave 41 (sequential): US-12.3.2 (after 12.3.1 + 12.1.1)
Wave 42 (sequential): US-12.4.2 (after 12.4.1)
--- Phase 12 PLANNED (0/8) ---

## Phase 13: Requirement Tracking & Structured Output Enforcement

> **Origin:** Real-world failure — requirement drift over multi-step pipelines. Phase 13 adds requirement anchoring, per-step audit enforcement, child soft-workflows, template-first output. **9 stories PLANNED.**

### Epic 13.1: Requirement Anchor Protocol

- [x] **US-13.1.1** — Structured requirements extraction from raw_prompt
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-13.1.1`
  - Blocked By: None

- [x] **US-13.1.2** — Per-requirement scoring in auditor calls
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-13.1.2`
  - Blocked By: ~~US-13.1.1~~ ✅

### Epic 13.2: Per-Step Auditor Enforcement

- [x] **US-13.2.1** — Mandatory auditor checkpoint after each pipeline step
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-13.2.1`
  - Blocked By: ~~US-13.1.2~~ ✅

- [x] **US-13.2.2** — Failure-triggered re-planning protocol
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-13.2.2`
  - Blocked By: ~~US-13.2.1~~ ✅

### Epic 13.3: Child Soft-Workflow for Complex Steps

- [x] **US-13.3.1** — Child workflow generation via strategist for complex steps
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-13.3.1`
  - Blocked By: ~~US-13.1.1~~ ✅

- [x] **US-13.3.2** — Child workflow state + failure isolation
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-13.3.2`
  - Blocked By: ~~US-13.3.1~~ ✅

### Epic 13.4: Template-First Output Protocol

- [x] **US-13.4.1** — Placeholder file creation before output generation
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-13.4.1`
  - Blocked By: ~~US-13.1.1~~ ✅

- [x] **US-13.4.2** — Placeholder validation vs requirements before fill
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-13.4.2`
  - Blocked By: ~~US-13.4.1~~ ✅, ~~US-13.1.2~~ ✅

- [x] **US-13.4.3** — Content-fill into validated placeholder (update, not create)
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-13.4.3`
  - Blocked By: ~~US-13.4.2~~ ✅

```
Wave 43 (parallel): US-13.1.1
Wave 44 (sequential): US-13.1.2 (after 13.1.1)
Wave 45 (parallel): US-13.2.1 (after 13.1.2), US-13.3.1 (after 13.1.1), US-13.4.1 (after 13.1.1)
Wave 46 (sequential): US-13.2.2 (after 13.2.1)
Wave 47 (sequential): US-13.3.2 (after 13.3.1)
Wave 48 (sequential): US-13.4.2 (after 13.4.1 + 13.1.2)
Wave 49 (sequential): US-13.4.3 (after 13.4.2)
--- Phase 13 DONE (9/9) ---
```

---

## Phase 14: Source Intelligence & Verify-Retry Protocol

> **Origin:** Real-world testing failure — pipeline uses stale model training knowledge to select data sources (review sites, job boards, directories) instead of discovering and verifying current sources. Phase 14 adds source discovery, per-source accessibility testing, verified source planning, and per-source retry loops. **6 stories PLANNED.**

### Epic 14.1: Source Discovery Protocol

- [x] **US-14.1.1** — Source discovery search for domain + country
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-14.1.1`
  - Blocked By: None

- [x] **US-14.1.2** — Source classification by reliability and data type
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-14.1.2`
  - Blocked By: ~~US-14.1.1~~ ✅

### Epic 14.2: Per-Source Accessibility Test

- [x] **US-14.2.1** — Per-source accessibility test with auto-retry (Playwright escalation)
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-14.2.1`
  - Blocked By: ~~US-14.1.2~~ ✅

- [x] **US-14.2.2** — Source reliability scoring and ranking
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-14.2.2`
  - Blocked By: ~~US-14.2.1~~ ✅

### Epic 14.3: Verified Source Plan

- [x] **US-14.3.1** — Verified source plan output (information, not question)
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-14.3.1`
  - Blocked By: ~~US-14.2.2~~ ✅

### Epic 14.4: Retry Loop for Data Collection

- [x] **US-14.4.1** — Verify-retry data collection loop per source
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-14.4.1`
  - Blocked By: ~~US-14.3.1~~ ✅

```
Wave 50 (sequential): US-14.1.1
Wave 51 (sequential): US-14.1.2 (after 14.1.1)
Wave 52 (sequential): US-14.2.1 (after 14.1.2)
Wave 53 (sequential): US-14.2.2 (after 14.2.1)
Wave 54 (sequential): US-14.3.1 (after 14.2.2)
Wave 55 (sequential): US-14.4.1 (after 14.3.1)
--- Phase 14 DONE (6/6) ---
```

---

## Phase 15: Pipeline Hardening & Skill Decomposition

> **Origin:** Real-world feedback — gather too broad, automation too low, execute-test-pivot loop missing, hard workflow compliance too low. Phase 15 adds gather/search split, RULE.md enforcement, hard session start, and execute-test-pivot-audit loop. **12 stories PLANNED.**

### Epic 15.1: gather / search Skill Split

- [x] **US-15.1.1** — Create new `search` skill with internet discovery logic
  - Status: DONE
  - Assignee: copilot
  - Branch: `main` (17d9621)
  - Blocked By: `None`

- [x] **US-15.1.2** — Refactor `gather` skill — file and URL only
  - Status: DONE
  - Assignee: copilot
  - Branch: `main` (158c06a)
  - Blocked By: ~~`US-15.1.1`~~

- [x] **US-15.1.3** — Update copilot-instructions.md skill registry
  - Status: DONE
  - Assignee: copilot
  - Branch: `main` (3f8ae24)
  - Blocked By: ~~`US-15.1.2`~~

### Epic 15.2: RULE.md Enforcement Layer

- [x] **US-15.2.1** — Create `.github/RULE.md` with non-negotiable pipeline rules
  - Status: DONE
  - Assignee: copilot
  - Branch: `main` (51fb840)
  - Blocked By: `None`

- [x] **US-15.2.2** — Inject RULE.md into copilot-instructions.md with mandatory priority
  - Status: DONE
  - Assignee: copilot
  - Branch: `main` (5070daf)
  - Blocked By: ~~`US-15.2.1`~~

### Epic 15.3: Hard Session Start Discipline

- [x] **US-15.3.1** — Define hard session start init sequence in RULE.md
  - Status: DONE
  - Assignee: copilot
  - Branch: `main` (da65de6)
  - Blocked By: ~~`US-15.2.1`~~

- [x] **US-15.3.2** — Apply hard session start to orchestrator agent
  - Status: DONE
  - Assignee: copilot
  - Branch: `main` (557bcd9)
  - Blocked By: ~~`US-15.3.1`~~

- [x] **US-15.3.3** — Parallel output template creation
  - Status: DONE
  - Assignee: copilot
  - Branch: `main` (1593130)
  - Blocked By: ~~`US-15.3.1`~~

### Epic 15.4: Execute-Test-Pivot-Audit Loop

- [x] **US-15.4.1** — Define execute-test-pivot-audit loop standard
  - Status: DONE
  - Assignee: copilot
  - Branch: `main` (1ef11a1)
  - Blocked By: ~~`US-15.2.1`~~

- [x] **US-15.4.2** — Apply loop to gather and search skills
  - Status: DONE
  - Assignee: copilot
  - Branch: `main` (53e883c)
  - Blocked By: ~~`US-15.4.1`~~

- [x] **US-15.4.3** — Apply loop to compose skill
  - Status: DONE
  - Assignee: copilot
  - Branch: `main` (d533b16)
  - Blocked By: ~~`US-15.4.1`~~

- [x] **US-15.4.4** — Apply loop to all gen-* skills
  - Status: DONE
  - Assignee: copilot
  - Branch: `main` (22a26b3)
  - Blocked By: ~~`US-15.4.1`~~

```
Wave 56 (parallel): US-15.1.1 ✅ + US-15.2.1 ✅
Wave 57 (sequential): US-15.1.2 ✅ + US-15.2.2 ✅ + US-15.3.1 ✅ + US-15.4.1 ✅
Wave 58 (sequential): US-15.1.3 ✅ + US-15.3.2 ✅ + US-15.3.3 ✅ + US-15.4.2 ✅ + US-15.4.3 ✅ + US-15.4.4 ✅
--- Phase 15 PLANNED (0/12) ---
```

---

## Phase 16: Agent-Centric Architecture & Tool-Agnostic Search

### Epic 16.1: Tool-Agnostic Search Cascade

- [x] **US-16.1.1** — Tool availability probe before search execution
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-16.1.1
  - Blocked By: None

- [x] **US-16.1.2** — Playwright stealth fallback when primary search fails
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-16.1.2
  - Blocked By: ~~US-16.1.1~~ ✅

- [x] **US-16.1.3** — HTTP zero-auth fallback as final tier
  - Status: DONE
  - Assignee: copilot
  - Device: Trucs-MacBook-Air-2
  - AI: copilot
  - Branch: feature/insight-engine-us-16.1.3
  - Blocked By: ~~US-16.1.2~~ ✅

### Epic 16.2: Execution Agent

- [x] **US-16.2.1** — Create execution.agent.md
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-16.2.1
  - Blocked By: None

- [x] **US-16.2.2** — Execution Agent child soft-flow request
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-16.2.2
  - Blocked By: ~~US-16.2.1~~ ✅

### Epic 16.3: Hard-Flow Protocol in RULE.md

- [x] **US-16.3.1** — Formalize Hard-Flow execution order in RULE.md
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-16.3.1
  - Blocked By: ~~US-16.2.1~~ ✅

### Epic 16.4: Adaptive Re-planning on Failure

- [x] **US-16.4.1** — Failure triggers Advisory/Strategist re-planning, not same-method retry
  - Status: DONE
  - Assignee: copilot
  - Device: Trucs-MacBook-Air-2
  - AI: copilot
  - Branch: feature/insight-engine-us-16.4.1
  - Blocked By: ~~US-16.2.1~~ ✅

### Epic 16.5: Experience Template Accumulation

- [x] **US-16.5.1** — Save experience template after successful pipeline run
  - Status: DONE
  - Assignee: copilot
  - Device: Trucs-MacBook-Air-2
  - AI: copilot
  - Branch: feature/insight-engine-us-16.5.1
  - Blocked By: ~~US-16.4.1~~ ✅

- [x] **US-16.5.2** — Load matching experience template at pipeline start
  - Status: DONE
  - Assignee: copilot
  - Device: Trucs-MacBook-Air-2
  - AI: copilot
  - Branch: feature/insight-engine-us-16.5.2
  - Blocked By: ~~US-16.5.1~~ ✅

```
Dependency map:
Wave 59 (parallel): US-16.1.1 + US-16.2.1
Wave 60 (parallel): US-16.1.2 + US-16.2.2 + US-16.3.1 + US-16.4.1
Wave 61 (sequential): US-16.1.3 (after 16.1.2) + US-16.5.1 (after 16.4.1)
Wave 62 (sequential): US-16.5.2 (after 16.5.1)
--- Phase 16 PLANNED (0/9) ---
```

> **2026-04-20 update:** Phase 16 fully shipped (9/9). All stories merged to
> `main`. See `docs/runs/insight-engine-us-16.*/README.md` for per-story
> artifacts.

---

## Phase 17: Delivery Channel Lockdown & Compliance Enforcement

> **Origin:** Real-world post-Phase-16 testing — three persistent compliance failures: (1) one-time scripts polluting `/scripts/` and pushed to git, (2) skills shipping single-attempt unaudited results with fabricated URLs, (3) user questions asked without prior agent consultation, (4) template-first protocol from Phase 13 bypassed. **9 stories PLANNED.**

### Epic 17.1: Orchestrator-Exclusive Delivery Channel

- [x] **US-17.1.1** — Add RULE-10 — orchestrator-only user channel
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-17.1.1`
  - Blocked By: None

- [x] **US-17.1.2** — Refactor non-orchestrator skills/agents to internal-return only
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-17.1.2`
  - Blocked By: ~~US-17.1.1~~ ✅

- [x] **US-17.1.3** — Orchestrator agent — gatekeeper for user-facing output
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-17.1.3`
  - Blocked By: ~~US-17.1.1~~ ✅

### Epic 17.2: Mandatory Pre-Question Consultation Protocol

- [x] **US-17.2.1** — Add RULE-11 — pre-question consultation required
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-17.2.1`
  - Blocked By: ~~US-17.1.1~~ ✅

- [x] **US-17.2.2** — Question budget tracker in session state
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-17.2.2`
  - Blocked By: ~~US-17.2.1~~ ✅

### Epic 17.3: One-Time Script Isolation

- [x] **US-17.3.1** — Add RULE-12 — one-time script placement
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-17.3.1`
  - Blocked By: None

- [x] **US-17.3.2** — Runtime validator + pipeline gate
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-17.3.2`
  - Blocked By: ~~US-17.3.1~~ ✅

- [x] **US-17.3.3** — Update .gitignore + pre-commit check
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-17.3.3`
  - Blocked By: ~~US-17.3.2~~ ✅

### Epic 17.4: Template-First Hard Gate

- [x] **US-17.4.1** — Auditor blocks gen-* without validated template
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-17.4.1`
  - Blocked By: ~~US-17.1.1~~ ✅

```
Wave 63 (parallel): US-17.1.1 + US-17.3.1
Wave 64 (parallel after 17.1.1): US-17.1.2 + US-17.1.3 + US-17.2.1 + US-17.4.1
Wave 65 (sequential): US-17.2.2 (after 17.2.1) + US-17.3.2 (after 17.3.1) + US-17.3.3 (after 17.3.2)
--- Phase 17 PLANNED (0/9) ---
```

---

## Phase 18: State Effectiveness & Artifact Reuse

> **Origin:** Real-world pipeline observation — state is write-only, intermediate tmp artifacts are discarded at synthesis time, compose only uses the last file. No integrity check between state and filesystem. **9 stories PLANNED.**

### Epic 18.1: Artifact Registry Protocol

- [x] **US-18.1.1** — Extend session state schema v4 with artifacts[] per step
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-18.1.1`
  - Blocked By: None

- [x] **US-18.1.2** — save_state.py register-artifact, list-artifacts, and read-context commands
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-18.1.2`
  - Blocked By: ~~US-18.1.1~~ ✅

### Epic 18.2: Mandatory State Read-Back Gate

- [ ] **US-18.2.1** — Add RULE-13 — mandatory state read-back before every step
  - Status: IN_PROGRESS
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-18.2.1`
  - Blocked By: ~~US-18.1.2~~ ✅

- [ ] **US-18.2.2** — Refactor skills to call read-context and register-artifact
  - Status: PLANNED
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-18.2.2`
  - Blocked By: US-18.2.1

### Epic 18.3: Multi-Artifact Synthesis

- [ ] **US-18.3.1** — Compose skill accepts artifact bundle input
  - Status: PLANNED
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-18.3.1`
  - Blocked By: US-18.2.2

- [ ] **US-18.3.2** — gen-* skills inject artifact evidence into output
  - Status: PLANNED
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-18.3.2`
  - Blocked By: US-18.2.2

- [ ] **US-18.3.3** — Auditor test case — Intermediate Artifact Utilization
  - Status: PLANNED
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-18.3.3`
  - Blocked By: US-18.3.1

### Epic 18.4: State-Filesystem Integrity Validator

- [x] **US-18.4.1** — validate_state_integrity.py script
  - Status: DONE
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-18.4.1`
  - Blocked By: ~~US-18.1.1~~ ✅

- [ ] **US-18.4.2** — Pipeline gate — integrity check before each step
  - Status: PLANNED
  - Assignee: copilot
  - Branch: `feature/insight-engine-us-18.4.2`
  - Blocked By: ~~US-18.4.1~~ ✅, US-18.2.1

```
Wave 66 (parallel): US-18.1.1
Wave 67 (parallel after 18.1.1): US-18.1.2 + US-18.4.1
Wave 68 (sequential): US-18.2.1 (after 18.1.2)
Wave 69 (parallel): US-18.2.2 + US-18.4.2 (after 18.2.1 + 18.4.1)
Wave 70 (parallel): US-18.3.1 + US-18.3.2 (after 18.2.2)
Wave 71 (sequential): US-18.3.3 (after 18.3.1)
--- Phase 18 PLANNED (0/9) ---
```

---

*This checklist is the single source of execution state. Status changes happen here only.*  
*Bước tiếp theo: `/roadmap-to-delivery` — Chọn user story đầu tiên để bắt đầu triển khai.*
