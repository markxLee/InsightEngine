# InsightEngine — Product Roadmap

> **Product:** InsightEngine  
> **Product Slug:** insight-engine  
> **Roadmap Created:** 2026-04-16  
> **Scope:** Milestone-based (Phase 0 → Phase 10)

---

## Product Roadmap Overview

- **Product name:** InsightEngine
- **Product slug:** `insight-engine`
- **Roadmap scope:** Milestone-based — each phase delivers a usable capability increment (Phase 0 → Phase 16)
- **Delivery model:** Copilot skill system built incrementally; each phase is independently usable

---

## Phase 0 — Product Foundation

**Goal:** Build the skeleton that all other skills depend on. After Phase 0, the repo is a working Copilot workspace with setup automation, the pipeline skill, and verified environment readiness.

### Epics

| Epic | Description |
|------|-------------|
| **Epic 0.1 — Workspace Setup** | Create complete `.github/` structure: `copilot-instructions.md`, instruction files, skill directories. Repo is ready to use in VS Code. |
| **Epic 0.2 — Cài đặt môi trường (`cai-dat`)** | Skill mới: `cai-dat` — hướng dẫn user cài Python libs, Node.js, và kiểm tra toàn bộ dependencies. Tạo `scripts/check_deps.py` và `scripts/setup.sh`. |
| **Epic 0.3 — Pipeline Chính (`tong-hop`)** | Skill `tong-hop` — nhận intent từ user, **tự động chạy setup check trước mỗi process**, route đến skill con phù hợp. Logic routing và chaining cơ bản. |

---

## Phase 1 — MVP: Thu thập & Xuất cơ bản

**Goal:** User có thể mô tả yêu cầu bằng tiếng Việt, cung cấp file hoặc URL, và nhận output là file Word hoặc PowerPoint hoàn chỉnh. Đây là use case cốt lõi nhất.

### Epics

| Epic | Description |
|------|-------------|
| **Epic 1.1 — Thu thập nội dung (`thu-thap`)** | Skill `thu-thap` — đọc file local (docx, xlsx, pdf, pptx, txt) qua markitdown + fallback thư viện chuyên biệt; fetch URL cụ thể do user cung cấp. |
| **Epic 1.2 — Biên soạn nội dung (`bien-soan`)** | Skill `bien-soan` — gộp nội dung từ nhiều nguồn, tóm tắt, cấu trúc lại theo yêu cầu user. Hỗ trợ dịch thuật Việt ↔ Anh cơ bản. |
| **Epic 1.3 — Xuất Word (`tao-word`)** | Skill `tao-word` — tạo file `.docx` với 3 template style (corporate, academic, minimal). Hỗ trợ heading, table, bullet, image. |
| **Epic 1.4 — Xuất PowerPoint (`tao-slide`)** | Skill `tao-slide` — tạo file `.pptx` với 3 template style. Hỗ trợ title slide, content slides, image placeholder. |

---

## Phase 2 — Mở rộng: Tìm kiếm & Thêm định dạng

**Goal:** Bổ sung khả năng tự tìm kiếm Google để thu thập context, và thêm các định dạng output còn lại (Excel, PDF, HTML). Pipeline trở nên thực sự autonomous.

### Epics

| Epic | Description |
|------|-------------|
| **Epic 2.1 — Tìm kiếm Google tự động** | Tích hợp `vscode-websearchforcopilot_webSearch` vào skill `thu-thap` — tự search + fetch top URLs khi user không cung cấp nguồn cụ thể. |
| **Epic 2.2 — Xuất Excel (`tao-excel`)** | Skill `tao-excel` — tạo file `.xlsx` với dữ liệu, công thức Excel, formatting. Tự động recalculate sau khi tạo. |
| **Epic 2.3 — Xuất PDF (`tao-pdf`)** | Skill `tao-pdf` — tạo file `.pdf` từ nội dung đã tổng hợp. Hỗ trợ table of contents, headers/footers. |
| **Epic 2.4 — Xuất HTML (`tao-html`)** | Skill `tao-html` — tạo trang HTML tĩnh với 3 template style. Portable (inline CSS), charts embedded dạng base64. |
| **Epic 2.5 — Chaining Output** | Nâng cấp `tong-hop` để hỗ trợ chuỗi output: Excel data → chart → PPT. Hiển thị kế hoạch chuỗi trước khi thực hiện. |

---

## Phase 3 — Hoàn thiện: Trực quan & Tối ưu

**Goal:** Nâng cao chất lượng visual của output — biểu đồ chuyên nghiệp, hình ảnh minh họa cho slide. Tối ưu trải nghiệm user với chunking cho tài liệu lớn.

### Epics

| Epic | Description |
|------|-------------|
| **Epic 3.1 — Biểu đồ & Hình ảnh (`tao-hinh`)** | Skill `tao-hinh` — tạo biểu đồ (bar, line, pie, radar, scatter) từ dữ liệu; gen hình minh họa cho slide (Apple Silicon). Embed chart vào Word/PPT. |
| **Epic 3.2 — Xử lý tài liệu lớn** | Nâng cấp `bien-soan` — chunking strategy cho file/corpus > 50,000 words. Incremental synthesis với progress feedback. |
| **Epic 3.3 — Template Library mở rộng** | Thêm style variants: `dark/modern`, `creative` cho tao-slide và tao-html. User có thể preview style trước khi generate. |
| **Epic 3.4 — Cải thiện UX Pipeline** | Nâng cấp `tong-hop` — hiển thị progress rõ hơn, hỏi xác nhận trước step tốn thời gian, gợi ý style dựa trên context. |

---

## Phase 4 — Nâng cấp: Template Library, Presentation HTML & Script Architecture

**Goal:** Nâng cấp đáng kể chất lượng output — thư viện template phong phú cho PPTX, HTML presentation-grade dựa trên reveal.js, kiến trúc script thực thi cho mỗi skill, và nội dung tổng hợp sâu hơn.

> **Nguồn gốc:** Phản hồi từ testing Phase 0-3 — output còn sơ sài, slide đơn giản, HTML thiếu tương tác.
> **Tham khảo:** slidemembers.com, aippt.com, canva.com (PPTX templates); revealjs.com, slides.com/templates, deckdeckgo.com (HTML presentations); a-z-copilot-flow/skills/gen-image, skills/pptx (script architecture pattern)

### Epics

| Epic | Description |
|------|-------------|
| **Epic 4.1 — Template Library PPTX** | Xây dựng thư viện 8-10 template PPTX chuyên nghiệp với scripts/ CLI. Template preview/selection trước khi generate. |
| **Epic 4.2 — HTML Presentation Mode (reveal.js)** | Tích hợp reveal.js cho `tao-html` — output là interactive presentation với slide transitions, animations, backgrounds. |
| **Epic 4.3 — Script Architecture cho Skills** | Mỗi output skill có `scripts/` directory chứa CLI tools (Python/Node.js). SKILL.md làm router → scripts/ xử lý. |
| **Epic 4.4 — Nâng cấp Content Depth** | Nâng cấp `bien-soan` — chế độ comprehensive tạo nội dung phong phú hơn, content enrichment từ nhiều nguồn. |
| **Epic 4.5 — Template Library HTML** | Xây dựng 5-8 reveal.js-based HTML presentation templates. Hỗ trợ presenter notes, PDF export. |

---

## Phase 5 — Tối ưu & Độ bền (Optimization & Resilience)

**Goal:** Make InsightEngine work reliably with smaller AI models and ensure pipeline progress is never lost when a Copilot session is interrupted.

> **Nguồn gốc:** Phản hồi từ testing Phase 0-4 — skills chưa tối ưu cho model nhỏ (GPT-4o-mini, GPT-3.5); user mất tiến độ khi session bị ngắt.

### Epics

| Epic | Description |
|------|-------------|
| **Epic 5.1 — Small Model Optimization** | Research nguyên nhân skills hoạt động kém với model nhỏ. Refactor SKILL.md files để giảm complexity (≤ 300 lines), tối ưu instruction clarity, kiểm tra compatibility với GPT-4o-mini / GPT-3.5 Turbo. |
| **Epic 5.2 — Session State Persistence** | `tong-hop` lưu `.session-state.json` sau mỗi bước. Skill detect và resume session chưa hoàn thành. User nói "tiếp tục" / "resume" để khôi phục pipeline từ checkpoint. |
---

## Phase 6 — Agent Architecture & Quality Gates

**Goal:** Transform InsightEngine from a skill-only system into an agent + skill hybrid. Specialized agents handle workflow generation, quality auditing, and decision-making — adapting dynamically to each model’s capabilities and each user’s request.

> **Nguồn gốc:** Phản hồi từ real-world usage — pipeline không đủ linh hoạt cho nhiều model khác nhau, thiếu kiểm tra chất lượng tự động, hỏi user quá nhiều câu hỏi kỹ thuật, file output nằm rải rác.

### Epics

| Epic | Description |
|------|-------------|
| **Epic 6.1 — Strict File Rules & Auto-escalation** | Enforce `/scripts`, `/tmp`, `/output` rules trong tất cả skills. Thêm auto-escalation protocol (tự nâng tool mạnh hơn thay vì hỏi user). |
| **Epic 6.2 — Shared Context Protocol** | Thiết kế `tmp/.agent-context.json` format + read/write protocol cho inter-agent communication. Giải quyết subagent statelessness. |
| **Epic 6.3 — Model Profile & Decision Maps** | Model self-declaration + decision maps per capability category (context_window, reasoning_depth, tool_use, multilingual, code_generation). Fallback medium profile. KHÔNG hardcode model name. |
| **Epic 6.4 — Agent Strategist (`xay-dung-quy-trinh`)** | Agent nhận request + model profile → tạo dynamic workflow. Pre-built workflow templates cho scenarios phổ biến × model capabilities. |
| **Epic 6.5 — Tiered Audit System (`kiem-dinh`)** | Self-review tier 1 (mọi step) → agent audit tier 2 (critical steps) → final audit tier 3 (output vs requirements). Max 3 retries/step, 10 total, fail-fast. |
| **Epic 6.6 — Advisory Agent & Conditional Skill Creation (`tu-van`)** | Agent tư vấn đa góc nhìn (1 call, max 2/pipeline). Conditional skill-forge runtime (30-min budget, clone-first từ verified public repos, mandatory security check). |
| **Epic 6.7 — Pipeline Integration** | Tích hợp agent architecture vào `tong-hop` với feature flag `AGENT_MODE`. Step-level rollback trên final audit fail. Budget cap 30 agent calls/pipeline. |

---

## Phase 7 — Pipeline Enforcement & Compliance Hardening

**Goal:** Close the gap between Phase 6 design and actual runtime behavior. Phase 6 defined the right architecture (strategist, audit, decision maps), but real-world testing reveals models frequently skip critical steps when instructions are buried in reference files. Phase 7 moves enforcement mechanisms inline, adds hard confirmation gates, and makes pipeline compliance visible to the user.

> **Nguồn gốc:** Real-world testing — user prompt "tìm jobs fresher JS ở HCM, tạo Excel + slide phân tích" resulted in: no request analysis shown, no dimension expansion, generic search URLs instead of platform-specific job URLs, no URL validation, AGENT_MODE pipeline flow not activated.

### Root Cause Analysis

```yaml
ROOT_CAUSES:
  RC1_reference_depth:
    problem: "Critical pipeline logic (Step 1.5, REQUEST_TYPE, data_collection protocol) lives in reference files"
    effect: "Models — especially smaller ones — skip reference reads and miss critical steps"
    
  RC2_no_hard_gates:
    problem: "Instructions say MUST but nothing forces the model to stop if it skips"
    effect: "Pipeline runs straight through without showing analysis to user"
    
  RC3_late_validation:
    problem: "URL validation only happens at audit step (4.7) — after output is already generated"
    effect: "Invalid URLs reach the final Excel file; post-hoc fix is wasteful"
    
  RC4_invisible_progress:
    problem: "User cannot see which pipeline steps are running vs skipped"
    effect: "User has no way to catch non-compliance until they inspect the output"
```

### Epics

| Epic | Description |
|------|-------------|
| **Epic 7.1 — Inline Critical Steps & Hard Gates** | Move Step 1.5 request analysis and REQUEST_TYPE detection back inline in tong-hop SKILL.md. Add mandatory user confirmation gate — pipeline MUST show analysis output and get explicit 'ok' before proceeding to Step 3. |
| **Epic 7.2 — Data Collection Enforcement** | Inline data_collection protocol in thu-thap SKILL.md main body (not reference file). Add pre-output URL validation gate — `validate_urls.py` runs BEFORE tao-excel generates the file, not just in post-hoc audit. |
| **Epic 7.3 — Visible Pipeline Trace** | Pipeline prints a numbered step list at start, marks each step ✅ as it completes. User always sees where pipeline is and can catch skips. |

---

## Phase 8 — Shared Copilot Agent Architecture

**Goal:** Refactor Phase 6 agents from inline tong-hop instructions into standalone shared Copilot agents (`runSubagent`). Any skill can invoke any agent — auditor checks quality at every output generation point, not just pipeline end. Strategist and advisory are reusable across skills.

> **Nguồn gốc:** Phase 6 embedded agents inside tong-hop SKILL.md as inline instructions. Real-world usage shows: (1) standalone skill calls have no quality audit, (2) agents share reasoning context with orchestrator leading to shortcuts, (3) tong-hop is overloaded with agent logic. Phase 8 makes agents first-class shared infrastructure.

### Epics

| Epic | Description |
|------|-------------|
| **Epic 8.1 — Shared Auditor Agent** | Create auditor as a standalone Copilot agent (`runSubagent`). Receives generated output + original requirements → returns quality verdict + specific issues. Any output skill (tao-word, tao-excel, tao-slide, tao-pdf, tao-html) can invoke it after file generation. |
| **Epic 8.2 — Shared Strategist Agent** | Refactor strategist from inline tong-hop logic → standalone `runSubagent` agent. Receives user request + model profile → returns optimized workflow plan. Tong-hop calls it instead of inline strategy logic. |
| **Epic 8.3 — Shared Advisory Agent** | Refactor advisory → standalone `runSubagent` agent. Any skill can call it when facing ambiguous decisions (not just tong-hop). Returns multi-perspective analysis in single call. |
| **Epic 8.4 — Agent Integration Protocol** | Standardize input/output format for all agents. Define when each skill calls which agent. Update output skills to call auditor after generation. Budget: auditor max 5/pipeline, advisory max 2, strategist max 1. Remove AGENT_MODE flag from tong-hop (agents always available). |

---

## Phase 9 — Central Orchestrator & Adaptive Self-Improvement

**Goal:** Separate orchestration from content synthesis. Introduce a central orchestrator agent that handles ALL request types—not just content synthesis—while tong-hop focuses purely on merging/structuring content. Add adaptive self-improvement (creating new agents/skills at runtime with user consent), 100-point weighted audit scoring, and full cross-session resume. Align ALL agents with VS Code custom agent standard (`.agent.md` in `.github/agents/`).

> **Nguồn gốc:** Real-world usage reveals tong-hop forces all requests through "gather → synthesize → output" pattern—but many requests (creative writing, visual storytelling, design, research) don’t fit this mold. Audit PASS/FAIL is too coarse. Session state doesn’t store enough context for true cross-session resume. Agents are not aligned with VS Code standard.

### Epics

| Epic | Description |
|------|-------------|
| **Epic 9.1 — Central Orchestrator Agent (`dieu-phoi`)** | Create `dieu-phoi.agent.md` in `.github/agents/` as the central request handler. Classifies intent (synthesis/creation/research/design/data_collection/mixed/unknown), routes to appropriate skills and agents. tong-hop refactored to pure content synthesis skill. Uses VS Code custom agent standard with YAML frontmatter (tools, agents, handoffs). |
| **Epic 9.2 — Adaptive Self-Improvement** | Orchestrator evaluates capability gaps before execution. Can create new specialized agents (e.g., literary author, art director) and skills (e.g., manga page layout) at runtime with user consent. Time notification at 30 min. User can "unlock" extended self-improvement. Created artifacts follow `.agent.md`/`SKILL.md` standards and are tested before use. |
| **Epic 9.3 — Enhanced Working State & Cross-Session Resume** | Upgrade session state to store: raw_prompt, analyzed_requirements, generated_plan, step_states[], audit_test_cases[], score_history[], created_skills[]. Enable full context reconstruction and resume in a new session. Output file hash tracking for conflict detection. |
| **Epic 9.4 — 100-Point Weighted Audit Scoring** | Replace PASS/FAIL with QA-grade weighted scoring. Auditor analyzes requirements → generates dynamic test case set (total 100 pts, weighted by importance). Pass threshold >80/100. Max 5 retries targeting specific low-scoring test cases. Score progression tracking. |
| **Epic 9.5 — VS Code Custom Agent Standard Migration** | Migrate all agents from `runSubagent`/shared-agents pattern to `.github/agents/*.agent.md` format. YAML frontmatter: description, tools, model, agents, handoffs, user-invocable. Agents and skills are peer-level. Auditor and dieu-phoi are user-invocable; strategist and advisory are subagent-only. |

---

## Phase 10 — English Naming, Natural Language UX & Product Alignment

**Goal:** Standardize all skill and agent names to English for international consistency. Remove slash-command dependency — users interact via natural language, the orchestrator classifies intent and routes. Clean up legacy artifacts and backfill missing skill documentation.

> **Nguồn gốc:** Self-review of Phase 0-9 revealed naming inconsistency (Vietnamese skill names, mixed agent names), stale documentation references, legacy `shared-agents/` directory, and missing user stories for 3 skills that exist in code (`thiet-ke`/design, `kiem-tra`/verify, `cai-tien`/improve). Natural language UX aligns with Phase 9's orchestrator architecture.

### Naming Map (Vietnamese → English)

| Current | New | Purpose |
|---------|-----|---------|
| `tong-hop` | `synthesize` | Content synthesis pipeline |
| `thu-thap` | `gather` | Gather content from files/URLs/web |
| `bien-soan` | `compose` | Compose/merge multi-source content |
| `tao-word` | `gen-word` | Generate Word documents |
| `tao-excel` | `gen-excel` | Generate Excel spreadsheets |
| `tao-slide` | `gen-slide` | Generate PowerPoint slides |
| `tao-pdf` | `gen-pdf` | Generate PDF documents |
| `tao-html` | `gen-html` | Generate HTML pages |
| `tao-hinh` | `gen-image` | Generate charts and images |
| `thiet-ke` | `design` | Visual design (poster, cover, certificate) |
| `kiem-tra` | `verify` | Output verification and audit |
| `cai-tien` | `improve` | Session retrospective and improvement |
| `cai-dat` | `setup` | Environment setup and dependency check |
| `dieu-phoi` | `orchestrator` | Central orchestrator agent |

### Epics

| Epic | Description |
|------|-------------|
| **Epic 10.1 — Rename Skills to English** | Rename all 13 skill directories from Vietnamese to English. Update SKILL.md files, triggers, and all cross-references in copilot-instructions.md and instructions.md. |
| **Epic 10.2 — Rename Agents to English** | Rename `dieu-phoi.agent.md` → `orchestrator.agent.md`. Update frontmatter, handoff references, and all documentation references. |
| **Epic 10.3 — Natural Language UX** | Remove slash command dependency from all skills and documentation. Update orchestrator to classify intent from natural language only. Remove `/command` table from copilot-instructions.md. Update README. |
| **Epic 10.4 — copilot-instructions.md Refresh** | Fix stale PIPELINE_FLOW (tong-hop no longer orchestrates). Update skill registry with English names. Remove Commands Reference table. Update Vietnamese Language Rules for skill naming. |
| **Epic 10.5 — Clean Up Legacy Artifacts** | Remove `shared-agents/` directory under `.github/skills/`. Move `agent-protocol.md` to `.github/agents/`. Delete duplicate old agent files. Fix user-stories.md overview count discrepancy. |
| **Epic 10.6 — Backfill Missing Skill Stories** | Add User Stories for `design` (formerly thiet-ke), `verify` (formerly kiem-tra), `improve` (formerly cai-tien) — skills that exist in code but have no formal stories. |
| **Epic 10.7 — Product Doc Alignment** | Update idea.md, roadmap.md Vietnamese Language Rules. Update Skill Map with English names. Ensure all docs use English skill names consistently. |

---

## Phase 11 — Adaptive Search Intelligence

**Goal:** Make complex structured-data searches (sales leads, job listings, product catalogs) reliable and precise. Instead of a flat Google query, the `gather` skill generates a specialized search sub-flow for each complex search step: source planning → site-scoped search → DOM exploration → internal search → detail URL extraction. If a sub-flow fails, the advisory agent proposes an alternative approach.

> **Origin:** Real-world usage reveals internet-based searches for structured data (e.g., "find sales leads", "collect job openings with direct URLs") consistently produce poor results because the current `gather` skill runs a flat Google search with no source strategy. Phase 11 adds per-step micro-planning and adaptive fallbacks to close this gap.

### Epics

| Epic | Description |
|------|-------------|
| **Epic 11.1 — Per-Step Search Planner** | Before any complex search step, call the strategist agent to generate a specialized search sub-flow (source plan → site-scoped search → DOM navigation → internal search). Replaces flat "search Google → get results" for data-collection requests. Budget: 1 strategist call per search step, max 3 per pipeline. |
| **Epic 11.2 — Source DOM Explorer** | When `site:source.com` search returns thin results (< threshold), automatically fetch the source homepage, extract DOM structure (nav links, search inputs, URL patterns), and construct targeted queries or direct navigation paths using the discovered structure. Falls back to existing Playwright stealth tier when needed. |
| **Epic 11.3 — Detail URL Extractor** | For sources that display results via open popup, expandable card, or JS-rendered inline detail — detect this pattern and extract the canonical detail-page URL. Enforce the rule: a listing-page URL is never acceptable as a final item output URL. |
| **Epic 11.4 — Adaptive Flow Advisor** | If a search sub-flow produces insufficient results after 2 attempts, call the advisory agent to propose an alternative flow (e.g., switch from Google site-search to direct platform URL pattern, use internal search API, or suggest alternative platforms). Present 2-3 options to the user before retrying. Budget: 1 advisory call per failed sub-flow, max 2 per pipeline. |

---

## Phase 12 — Autonomous Pipeline UX

**Goal:** Make InsightEngine's pipeline truly autonomous — fire-and-forget like n8n. After confirming a request, the user receives results, not follow-up questions. Eliminate all technical jargon from user-facing messages. Detect user frustration signals and switch to full-auto mode mid-pipeline.

> **Origin:** Real-world user feedback: "flow kém hiệu quả hơn n8n, tính tự động hóa quá thấp, luôn luôn cần user túc trực và trả lời câu hỏi." Identified 5 root causes: excessive questions, technical jargon exposure, lack of autonomous batch execution, visible intermediate steps, no "just do it" mode.

### Epics

| Epic | Description |
|------|-------------|
| **Epic 12.1 — Fire-and-Forget Pipeline Mode** | After user confirms the pipeline plan at Step 1.5, execution runs fully autonomously to completion. No intermediate confirmations, no per-batch approvals, no technical questions. The pipeline only interrupts for CONTENT ambiguity (e.g., scope clarification) or complete failure after all retries. Delivers a single final summary message. |
| **Epic 12.2 — Technical Jargon Shield** | All user-facing messages MUST pass through a jargon filter before display. Banned terms: JSON, Playwright, crawler, seed, HTTP, DOM, endpoint, selector, API, batch, fetch, parse. Replaced with user-friendly equivalents: "đang tìm trên ITViec… ✅ 23 jobs", "đang đọc thông tin chi tiết từng công ty", "đang tạo file Excel". |
| **Epic 12.3 — User Signal Detection & Mode Switching** | Detect user frustration/impatience signals ("tiếp tục", "không cần hỏi", "tôi cần kết quả", "just do it", "cứ làm đi") and automatically switch to full-auto mode: suppress all remaining confirmation prompts in the current pipeline run and execute to completion. |
| **Epic 12.4 — Batch Progress Model for Data Collection** | Replace per-item/per-source confirmations with a batch execution model: show periodic progress summary ("🔍 Đang tìm: ITViec ✅ 23 | TopCV ✅ 34 | VietnamWorks ⏳...") and a single delivery summary at the end ("Hoàn tất! 87 jobs từ 5 nguồn → output/jobs.xlsx (6 sheets)"). |

---

## Phase 13 — Requirement Tracking & Structured Output Enforcement

**Goal:** Ensure the pipeline never "forgets" the original request across many execution steps. Every step output is audited against a structured requirements list extracted from the raw request. Output files are created via a template-first approach. Complex steps receive their own child soft-workflow with isolated state and failure handling.

> **Origin:** Real-world failure — user requested "list all fresher/junior dev jobs in Vietnam by province" and received a single Excel sheet named "unknown" with 3 senior/teamlead roles. Root cause: requirement drift. Phase 7-12 designed the right enforcement mechanisms (hard gates, auditor, state) but AI skips them when they are in reference files, not inline. Phase 13 moves enforcement into runtime protocol as explicit mandatory terminal commands that cannot be bypassed.

### Root Cause Analysis

```yaml
ROOT_CAUSES:
  RC1_requirement_drift:
    problem: "AI loses track of original requirements over a multi-step pipeline"
    effect: "Final output structure/content is completely wrong even though each step appeared reasonable"
    example: "fresher jobs by province → Excel with 1 sheet 'unknown' containing 3 senior/teamlead roles"

  RC2_enforcement_gap:
    problem: "Phase 7-12 designed correct enforcement (hard gates, auditor, state) but placed them in reference files"
    effect: "AI skips enforcement when instructions are not inline mandatory steps"
    note: "This is not a design gap — it is an enforcement gap. Phase 13 moves enforcement inline."

  RC3_late_structure:
    problem: "Output file structure (sheet names, headings, slides) only materializes when content is generated"
    effect: "Structure errors (wrong sheets, missing columns, wrong slide count) are only caught at delivery time"

  RC4_flat_complex_steps:
    problem: "Multi-platform research or multi-source data collection runs as a flat sequence"
    effect: "No strategy per source, no isolated retry, parent pipeline can't distinguish source-level failure"
```

### Epics

| Epic | Description |
|------|-------------|
| **Epic 13.1 — Requirement Anchor Protocol** | On pipeline start, orchestrator extracts a **structured requirements list** from the raw_prompt (not just stores the prompt text). List items are typed: output_files[], fields_required[], filters[], grouping[], format_constraints[]. This list is stored in session state and sent as part of every auditor call. The auditor scores each requirement item individually (not just overall output). |
| **Epic 13.2 — Per-Step Auditor Enforcement** | After every substantive step (gather, compose, gen-excel, gen-slide, gen-word, gen-pdf, gen-html), a mandatory auditor call runs against the structured requirements list. If any requirement item scores < 60: STOP, log failure reason to state, trigger re-plan for that step. The next step cannot start until the current step passes audit. This is enforced as an explicit terminal command, not a documentation note. |
| **Epic 13.3 — Child Soft-Workflow for Complex Steps** | Steps with high complexity (multi-platform data collection, multi-source research with > 3 sources) are executed as child workflows generated by the strategist agent. Child workflow has: dedicated strategy, execution sequence, per-source retry logic, isolated state, and its own audit gate. Parent workflow suspends until child completes and passes audit. Child failure triggers re-planning of the child only, not the full pipeline. |
| **Epic 13.4 — Template-First Output Protocol** | Before generating content for any structured output (Excel, Word, PPT, HTML): (1) create a placeholder file with correct structure (sheet names matching requirements, section headings, slide titles, column names), (2) validate placeholder structure against requirements via auditor, (3) only then fill content into the validated placeholder. Output scripts receive the placeholder path and update it — they do not create a new file from scratch. |

---

## Phase 14 — Source Intelligence & Verify-Retry Protocol

**Goal:** Pipeline should never assume it knows which platforms, review sites, or directories exist for a given country or domain. Sources are discovered, tested, and ranked before data collection begins. Every collection step follows test → verify → retry logic.

> **Origin:** Real-world testing failure — pipeline uses stale model training knowledge to select data sources (review sites, job boards, directories) instead of discovering and verifying current sources. The concrete failure: a request for company review platforms in Vietnam prompted the model to produce a hardcoded list of sites — some missing, some inaccessible, without any actual verification.

### Epics

| Epic | Description |
|------|-------------|
| **Epic 14.1 — Source Discovery Protocol** | Before any data collection requiring "soft knowledge" sources (review platforms, job boards, local directories), perform gather searches to discover current sources for that country/domain. Never assumes model training knowledge is current or correct. |
| **Epic 14.2 — Per-Source Accessibility Test** | After discovering candidate sources, test each one: fetch homepage, check data structure, score reliability. Tier by score: primary (≥60) / Playwright fallback / skip. |
| **Epic 14.3 — Verified Source Plan** | Before proceeding to collection, produce a verified source plan. Present discovered + tested sources as INFORMATION (not a question): "Found 4 review sites: itviec.com ✅, topdev.vn ✅, glassdoor.com ⚠️ (Playwright needed)". Auto-proceed; user can override if desired. |
| **Epic 14.4 — Retry Loop for Data Collection** | Per source: attempt fetch → check data quality → retry up to 2× with alternative approaches (Playwright, different query, different URL pattern) before marking failed. Never stops pipeline on single source failure — partial results preferred. |

---

## Phase 17 — Delivery Channel Lockdown & Compliance Enforcement

**Goal:** Eliminate three persistent compliance failures observed after Phase 13–16 shipped: (1) one-time scripts polluting `/scripts/` and being pushed to git, (2) skills shipping single-attempt unaudited results directly to the user with fabricated URLs, (3) user questions being asked without prior agent consultation. Phase 17 enforces orchestrator-exclusive user channel, mandatory pre-question consultation, hard one-time script isolation, and a template-first hard gate for all `gen-*` skills.

> **Origin:** Real-world post-Phase-16 testing — Copilot continued to: (a) place one-time scripts under `/scripts/` (committed to git); (b) fabricate non-existent URLs and ship results in a single attempt without auditor verification; (c) ask user questions before consulting advisory/strategist; (d) skip the Phase 13 template-first protocol when generating output. The architecture is correct; enforcement is the gap.

### Epics

| Epic | Description |
|------|-------------|
| **Epic 17.1 — Orchestrator-Exclusive Delivery Channel** | Add RULE-10 to `RULE.md`: only `orchestrator` agent may emit user-facing messages or questions. All skills and other agents (strategist, execution, auditor, advisory) MUST return output internally to the orchestrator — never directly to the user. Refactor SKILL.md and `.agent.md` files to remove direct user-facing language from non-orchestrator components. Orchestrator becomes the sole gatekeeper for delivery and questions. |
| **Epic 17.2 — Mandatory Pre-Question Consultation** | Add RULE-11 to `RULE.md`: before any user question, orchestrator MUST consult `advisory` AND `strategist` to determine if an autonomous decision is possible. Question-asking is last-resort. Track per-pipeline question budget (default max 2) in `tmp/session_state.json`. If consultation concludes autonomous resolution exists, orchestrator decides and proceeds without asking. |
| **Epic 17.3 — One-Time Script Isolation** | Add RULE-12 to `RULE.md`: scripts created for a single pipeline run MUST live in `/tmp/scripts/`. Only reusable utility scripts may live in `/scripts/`. Create `scripts/validate_script_placement.py` validator + invoke at pipeline start and after each step. Update `.gitignore` to ensure `/tmp/` (including `/tmp/scripts/`) is excluded. Document one-time vs reusable distinction in setup skill. |
| **Epic 17.4 — Template-First Hard Gate** | Auditor enforces template-first protocol from Phase 13 as a hard pre-execution gate. No `gen-*` skill may execute content generation until: (1) a structural template file exists for the requested output, AND (2) auditor has validated the template against the requirements anchor. Auditor refuses to score generations that bypass this gate. Eliminates direct content generation that skips structure validation. |

---

## Skill Map theo Phase

```
Phase 0:  setup (NEW)        synthesize (skeleton)
Phase 1:  gather             compose              gen-word     gen-slide
Phase 2:  gather (enhanced)  gen-excel             gen-pdf      gen-html   synthesize (chaining)
Phase 3:  gen-image (NEW)    compose (enhanced)    gen-slide (enhanced)  synthesize (enhanced)
Phase 4:  gen-slide (templates)  gen-html (reveal.js)  compose (depth)  all skills (scripts/)
Phase 5:  all skills (small model refactor)  synthesize (session state + resume)
Phase 6:  agents (NEW: strategist, audit, advisory)  synthesize (dynamic workflow)  all skills (strict rules)
Phase 7:  synthesize (inline critical steps + hard gates)  gather (data collection hardening)  pipeline trace
Phase 8:  shared agents (refactor → runSubagent)  all output skills (auditor integration)  synthesize (delegate to agents)
Phase 9:  orchestrator (NEW agent)  synthesize (refactor → synthesis-only)  all agents (→ .agent.md standard)  auditor (100-point scoring)  improve (upgrade)  session state (enhanced)
Phase 10: ALL skills (Vietnamese → English rename)  orchestrator (renamed from dieu-phoi)  natural language UX  legacy cleanup  design/verify/improve (backfill stories)
Phase 11: gather (per-step search planner + DOM explorer + detail URL extractor + adaptive flow advisor)
Phase 12: orchestrator (fire-and-forget mode + jargon shield + signal detection)  gather (batch progress model)
Phase 13: orchestrator + auditor (requirement anchor + per-step audit)  synthesize (child soft-workflow)  all output skills (template-first output protocol)
Phase 14: gather (source discovery + accessibility test + verified plan)  orchestrator (verify-retry collection loop)
Phase 17: orchestrator (exclusive user channel + pre-question consultation gate)  auditor (template-first hard gate for all gen-*)  RULE.md (RULE-10/11/12)  scripts (validate_script_placement.py)  .gitignore (one-time script isolation)
```

> Note: Phase 0-9 Skill Map shows English names for readability. Actual rename happens in Phase 10.

**Tổng số:** 13 skills (`.github/skills/`) + 4 custom agents (`.github/agents/`) — peer-level per VS Code standard

---

## Setup Check Architecture (Cross-phase requirement)

> Yêu cầu từ user: pipeline phải check setup trước mỗi process.

```yaml
SETUP_CHECK_PATTERN:
  trigger: mỗi khi tong-hop bắt đầu xử lý yêu cầu
  
  check_sequence:
    1. Chạy scripts/check_deps.py (silent mode)
    2. Nếu missing deps → thông báo user + gợi ý chạy /cai-dat
    3. Nếu đủ deps → tiếp tục pipeline bình thường
  
  cai-dat skill:
    trigger_manual: "/cai-dat", "cài đặt", "setup", "install dependencies"
    trigger_auto: khi check_deps phát hiện thiếu package
    actions:
      - Kiểm tra Python version (cần 3.10+)
      - Kiểm tra Node.js version (cần 18+)
      - Cài Python packages (pip install --user)
      - Cài Node.js packages (npm install -g pptxgenjs)
      - Tạo thư mục scripts/ với check_deps.py, recalc.py, setup.sh
      - Verify toàn bộ và báo cáo kết quả
```

---

## Thứ tự xây dựng được đề xuất

```
Phase 0 → Phase 1 → Phase 2 → Phase 3
  ↑ Bắt đầu ở đây. Mỗi phase hoàn chỉnh là một sản phẩm có thể dùng được.
```

Phase 0 là bắt buộc — không có `cai-dat` và `tong-hop` thì các skill con không chạy được.

---

---

## Tổng quan lộ trình sản phẩm (Tiếng Việt)

- **Tên sản phẩm:** InsightEngine
- **Product slug:** `insight-engine`
- **Phạm vi roadmap:** Theo mốc — mỗi phase là một increment có thể sử dụng được

---

## Phase 0 — Nền tảng sản phẩm

**Mục tiêu:** Xây dựng khung cho toàn bộ hệ thống. Sau Phase 0, repo là workspace Copilot hoạt động được với setup automation và pipeline cơ bản.

| Epic | Mô tả |
|------|-------|
| **Epic 0.1 — Workspace Setup** | Tạo cấu trúc `.github/` hoàn chỉnh, copilot-instructions, skill directories |
| **Epic 0.2 — Skill `cai-dat`** | Hướng dẫn + tự động cài Python libs, Node.js, kiểm tra dependencies |
| **Epic 0.3 — Skill `tong-hop` (skeleton)** | Pipeline chính — nhận intent, check setup, route đến skill con |

---

## Phase 1 — MVP: Thu thập & Xuất cơ bản

**Mục tiêu:** User cung cấp file/URL → nhận file Word hoặc PowerPoint hoàn chỉnh.

| Epic | Mô tả |
|------|-------|
| **Epic 1.1 — Skill `thu-thap`** | Đọc file local + fetch URL do user cung cấp |
| **Epic 1.2 — Skill `bien-soan`** | Gộp, tóm tắt, cấu trúc nội dung; dịch Việt ↔ Anh |
| **Epic 1.3 — Skill `tao-word`** | Xuất Word (.docx) với 3 template style |
| **Epic 1.4 — Skill `tao-slide`** | Xuất PowerPoint (.pptx) với 3 template style |

---

## Phase 2 — Mở rộng: Tìm kiếm & Thêm định dạng

**Mục tiêu:** Thêm tìm kiếm Google tự động và các định dạng Excel, PDF, HTML.

| Epic | Mô tả |
|------|-------|
| **Epic 2.1 — Search Google tự động** | Tích hợp web search vào `thu-thap` khi user không cung cấp nguồn |
| **Epic 2.2 — Skill `tao-excel`** | Xuất Excel với dữ liệu và công thức |
| **Epic 2.3 — Skill `tao-pdf`** | Xuất PDF từ nội dung tổng hợp |
| **Epic 2.4 — Skill `tao-html`** | Xuất HTML tĩnh portable |
| **Epic 2.5 — Chaining Output** | Chuỗi output (Excel → chart → PPT) |

---

## Phase 3 — Hoàn thiện: Trực quan & Tối ưu

**Mục tiêu:** Nâng cao chất lượng visual, xử lý tài liệu lớn, mở rộng template.

| Epic | Mô tả |
|------|-------|
| **Epic 3.1 — Skill `tao-hinh`** | Biểu đồ chuyên nghiệp + gen image cho slide |
| **Epic 3.2 — Xử lý tài liệu lớn** | Chunking strategy cho corpus > 50,000 words |
| **Epic 3.3 — Template mở rộng** | Thêm style dark/modern, creative |
| **Epic 3.4 — UX Pipeline** | Progress feedback, xác nhận trước step nặng |

---

## Phase 4 — Nâng cấp: Template Library, Presentation HTML & Script Architecture

**Mục tiêu:** Thư viện template phong phú cho PPTX, HTML presentation dựa trên reveal.js, script architecture, content depth.

| Epic | Mô tả |
|------|-------|
| **Epic 4.1 — Template Library PPTX** | 8-10 template PPTX chuyên nghiệp, preview/selection |
| **Epic 4.2 — HTML Presentation Mode** | Tích hợp reveal.js — transitions, animations, backgrounds |
| **Epic 4.3 — Script Architecture** | Mỗi output skill có `scripts/` CLI tools |
| **Epic 4.4 — Content Depth** | `bien-soan` comprehensive mode, content enrichment |
| **Epic 4.5 — Template Library HTML** | 5-8 reveal.js presentation templates, presenter notes, PDF export |
---

## Phase 5 — Tối ưu & Độ bền

**Mục tiêu:** Làm InsightEngine hoạt động tốt với nhiều model AI hơn và không bị mất tiến độ khi session bị ngắt.

| Epic | Mô tả |
|------|-------|
| **Epic 5.1 — Small Model Optimization** | Research tại sao skills hoạt động kém với model nhỏ. Refactor SKILL.md giảm complexity, tối ưu instruction clarity |
| **Epic 5.2 — Session State Persistence** | Pipeline lưu state sau mỗi bước. `tong-hop` detect và resume session chưa hoàn thành |
---

## Phase 6 — Agent Architecture & Quality Gates

**Mục tiêu:** Chuyển InsightEngine từ hệ thống skill-only sang agent + skill hybrid. Agents chuyên biệt xử lý workflow, kiểm tra chất lượng, và tư vấn quyết định.

| Epic | Mô tả |
|------|-------|
| **Epic 6.1 — Strict File Rules & Auto-escalation** | Enforce `/scripts`, `/tmp`, `/output`. Auto-escalation khi tool fail |
| **Epic 6.2 — Shared Context Protocol** | `tmp/.agent-context.json` cho giao tiếp giữa các agent |
| **Epic 6.3 — Model Profile & Decision Maps** | Self-declaration + decision maps, fallback profile trung bình |
| **Epic 6.4 — Agent Strategist** | Tạo dynamic workflow từ request + model profile |
| **Epic 6.5 — Tiered Audit System** | Self-review → agent audit (critical) → final audit. Max 3 retries/step |
| **Epic 6.6 — Advisory Agent & Skill Creation** | Tư vấn đa góc nhìn. Tạo skill có điều kiện (30 phút, clone-first, security check) |
| **Epic 6.7 — Pipeline Integration** | Tích hợp agents vào tong-hop với feature flag AGENT_MODE |

---

## Phase 7 — Pipeline Enforcement & Compliance Hardening

**Mục tiêu:** Đóng khoảng cách giữa thiết kế Phase 6 và hành vi thực tế. Model thường bỏ qua các step quan trọng khi instruction nằm quá sâu trong reference files. Phase 7 đưa enforcement inline, thêm hard gates, và làm pipeline compliance hiển thị cho user.

> **Nguồn gốc:** Test thực tế — model skip Step 1.5 request analysis, không dùng platform-specific search, trả URL search page thay vì direct job URL, không activate AGENT_MODE flow.

| Epic | Mô tả |
|------|-------|
| **Epic 7.1 — Inline Critical Steps & Hard Gates** | Đưa Step 1.5 và REQUEST_TYPE detection về inline trong tong-hop. Thêm gate xác nhận bắt buộc trước Step 3. |
| **Epic 7.2 — Data Collection Enforcement** | Inline data_collection protocol trong thu-thap. URL validation chạy TRƯỚC khi tạo Excel output. |
| **Epic 7.3 — Visible Pipeline Trace** | Pipeline in danh sách step có đánh số ở đầu, đánh dấu ✅ từng step khi hoàn thành. |

---

## Phase 8 — Shared Copilot Agent Architecture

**Mục tiêu:** Tái cấu trúc agents từ Phase 6 (nhúng trong tong-hop) thành **shared Copilot agents** (`runSubagent`). Bất kỳ skill nào cũng gọi được agent. Auditor kiểm tra chất lượng ở mọi điểm tạo output, không chỉ cuối pipeline.

> **Nguồn gốc:** Phase 6 nhúng agents trong tong-hop SKILL.md dưới dạng inline instructions. Thực tế cho thấy: (1) gọi skill standalone không có audit, (2) agents chia sẻ reasoning context với orchestrator dẫn đến shortcut, (3) tong-hop quá tải với agent logic.

| Epic | Mô tả |
|------|-------|
| **Epic 8.1 — Shared Auditor Agent** | Tạo auditor dưới dạng Copilot agent (`runSubagent`). Nhận output + yêu cầu gốc → trả verdict + issues. Mọi output skill đều gọi được. |
| **Epic 8.2 — Shared Strategist Agent** | Refactor strategist từ inline tong-hop → standalone `runSubagent`. Nhận request + model profile → trả workflow plan. |
| **Epic 8.3 — Shared Advisory Agent** | Refactor advisory → standalone `runSubagent`. Bất kỳ skill nào cần tư vấn đều gọi được. Trả phân tích đa góc nhìn. |
| **Epic 8.4 — Agent Integration Protocol** | Chuẩn hóa input/output format cho agents. Cập nhật output skills gọi auditor. Budget: auditor 5/pipeline, advisory 2, strategist 1. Bỏ AGENT_MODE flag. |

---

## Phase 9 — Central Orchestrator & Adaptive Self-Improvement

**Mục tiêu:** Tách orchestration khỏi việc tổng hợp nội dung. Tạo agent trung tâm (`dieu-phoi`) xử lý MỌI loại yêu cầu — tong-hop chỉ làm tổng hợp thuần túy. Thêm cơ chế tự cải thiện (tạo agent/skill mới runtime với sự đồng ý user), audit thang 100 điểm, resume xuyên session, và chuẩn hóa agents theo VS Code custom agent standard (`.agent.md`).

> **Nguồn gốc:** Sử dụng thực tế cho thấy tong-hop ép mọi request qua pattern "thu thập → tổng hợp → xuất" — nhưng nhiều yêu cầu (sáng tác, thiết kế, nghiên cứu) không phù hợp. Audit PASS/FAIL quá thô. Session state chưa lưu đủ context cho resume xuyên session. Agents chưa theo chuẩn VS Code.

| Epic | Mô tả |
|------|-------|
| **Epic 9.1 — Central Orchestrator (`dieu-phoi`)** | Tạo `dieu-phoi.agent.md` trong `.github/agents/`. Phân loại intent, route đến skills/agents. tong-hop refactor thành skill tổng hợp thuần túy. |
| **Epic 9.2 — Tự cải thiện thích ứng** | Đánh giá gap năng lực, tạo agent/skill mới với user consent. Thông báo >30 phút. Test trước khi dùng. |
| **Epic 9.3 — Working State & Resume xuyên session** | Lưu raw_prompt, analyzed_requirements, generated_plan, step_states[], audit_test_cases[]. Resume đầy đủ ở session mới. |
| **Epic 9.4 — Audit thang 100 điểm** | Thay PASS/FAIL bằng QA-grade scoring. Auditor tạo bộ test case động (100 điểm, trọng số theo mức quan trọng). >80/100 mới pass. Tối đa 5 lần retry nhắm vào điểm yếu. |
| **Epic 9.5 — Chuẩn VS Code Custom Agent** | Migrate agents từ `runSubagent` sang `.github/agents/*.agent.md`. YAML frontmatter: description, tools, model, agents, handoffs, user-invocable. Agents ngang hàng với skills. |

---

## Phase 10 — Đặt tên tiếng Anh, UX ngôn ngữ tự nhiên & Căn chỉnh sản phẩm

**Mục tiêu:** Chuẩn hóa tên skill và agent sang tiếng Anh cho tính nhất quán quốc tế. Bỏ phụ thuộc slash command — user tương tác bằng ngôn ngữ tự nhiên, orchestrator phân loại intent và route. Dọn dẹp artifact cũ và bổ sung tài liệu skill còn thiếu.

> **Nguồn gốc:** Self-review Phase 0-9 phát hiện: tên skill tiếng Việt gây nhầm lẫn, tài liệu stale, thư mục `shared-agents/` cũ, thiếu user stories cho 3 skills đang có trong code (`thiet-ke`/design, `kiem-tra`/verify, `cai-tien`/improve). UX ngôn ngữ tự nhiên phù hợp với kiến trúc orchestrator Phase 9.

| Epic | Mô tả |
|------|-------|
| **Epic 10.1 — Đổi tên Skills sang tiếng Anh** | Đổi tên 13 thư mục skill từ tiếng Việt sang tiếng Anh. Cập nhật SKILL.md, triggers, và cross-references. |
| **Epic 10.2 — Đổi tên Agents sang tiếng Anh** | Đổi `dieu-phoi.agent.md` → `orchestrator.agent.md`. Cập nhật frontmatter, handoffs, tài liệu. |
| **Epic 10.3 — UX ngôn ngữ tự nhiên** | Bỏ phụ thuộc slash command. Orchestrator phân loại intent từ ngôn ngữ tự nhiên. Xóa bảng `/command` trong copilot-instructions.md. Cập nhật README. |
| **Epic 10.4 — Làm mới copilot-instructions.md** | Sửa PIPELINE_FLOW stale. Cập nhật skill registry với tên tiếng Anh. Xóa Commands Reference. Cập nhật Vietnamese Language Rules. |
| **Epic 10.5 — Dọn dẹp artifact cũ** | Xóa `shared-agents/` trong `.github/skills/`. Di chuyển `agent-protocol.md`. Xóa file agent trùng lặp. Sửa lỗi số lượng user-stories. |
| **Epic 10.6 — Bổ sung User Stories thiếu** | Thêm stories cho `design`, `verify`, `improve` — skills có trong code nhưng chưa có stories. |
| **Epic 10.7 — Căn chỉnh tài liệu sản phẩm** | Cập nhật idea.md, roadmap.md. Cập nhật Skill Map. Đảm bảo tên tiếng Anh nhất quán. |

---

## Phase 11 — Tìm kiếm thông minh thích ứng

**Mục tiêu:** Biến các yêu cầu tìm kiếm dữ liệu có cấu trúc (sales lead, tin tuyển dụng, danh mục sản phẩm) trở nên đáng tin cậy và chính xác. Thay vì tìm kiếm Google phẳng, skill `gather` tự tạo sub-flow tìm kiếm chuyên biệt cho từng bước phức tạp. Nếu sub-flow thất bại, advisory agent đề xuất hướng tiếp cận thay thế.

> **Nguồn gốc:** Sử dụng thực tế cho thấy tìm kiếm internet dạng "tìm sales lead", "thu thập tin tuyển dụng với URL trực tiếp" thường không hiệu quả vì `gather` skill đang chạy tìm kiếm Google phẳng, không có chiến lược nguồn.

| Epic | Mô tả |
|------|-------|
| **Epic 11.1 — Per-Step Search Planner** | Trước mọi bước tìm kiếm phức tạp, gọi strategist agent để tạo sub-flow chuyên biệt (lên kế hoạch nguồn → tìm theo site → khám phá DOM → tìm kiếm nội trang). Thay thế tìm kiếm Google phẳng cho các yêu cầu data-collection. |
| **Epic 11.2 — Source DOM Explorer** | Khi tìm `site:nguồn.com` trả kết quả mỏng, tự động fetch trang chủ nguồn, trích xuất cấu trúc DOM (nav links, ô tìm kiếm, URL patterns), và xây dựng query nhắm mục tiêu hoặc đường dẫn trực tiếp dựa trên cấu trúc vừa khám phá. |
| **Epic 11.3 — Detail URL Extractor** | Với nguồn hiển thị kết quả qua popup mở, expandable card, hoặc detail inline — phát hiện pattern và trích xuất URL trang detail chính xác. Quy tắc bắt buộc: URL trang listing không bao giờ được dùng làm URL đầu ra cuối cùng. |
| **Epic 11.4 — Adaptive Flow Advisor** | Nếu sub-flow tìm kiếm thất bại sau 2 lần, gọi advisory agent đề xuất hướng tiếp cận thay thế (chuyển sang URL pattern trực tiếp, API nội trang, hoặc nền tảng khác). Hiển thị 2-3 lựa chọn cho user trước khi thử lại. |

---

---

## Phase 14 — Source Intelligence & Verify-Retry Protocol (Tiếng Việt)

**Mục tiêu:** Pipeline không bao giờ giả định biết nền tảng nào tồn tại trong một quốc gia hay lĩnh vực. Nguồn được khám phá, test, và xếp hạng trước khi bắt đầu thu thập. Mọi bước thu thập theo logic test → verify → retry.

> **Nguồn gốc:** Thất bại thực tế — pipeline sử dụng kiến thức huấn luyện cũ để chọn nguồn dữ liệu (trang đánh giá, job board, thư mục) thay vì khám phá và xác thực nguồn hiện tại. Ví dụ cụ thể: yêu cầu liệt kê các trang đánh giá công ty Việt Nam dẫn đến danh sách cứng — một số trang thiếu, một số không truy cập được, không có xác minh nào.

| Epic | Mô tả |
|------|-------|
| **Epic 14.1 — Source Discovery Protocol** | Trước khi thu thập dữ liệu từ nguồn “soft knowledge”, tự tìm kiếm khám phá nguồn hiện tại — không dựa vào kiến thức huấn luyện. |
| **Epic 14.2 — Per-Source Accessibility Test** | Test từng nguồn: fetch trang chủ, kiểm tra cấu trúc dữ liệu, chấm điểm độ tin cậy. Phân tầng: primary (≥60), Playwright fallback, bỏ qua. |
| **Epic 14.3 — Verified Source Plan** | Trước khi thu thập, xuất kế hoạch nguồn đã xác minh dưới dạng THÔNG TIN (không phải câu hỏi). Tự động tiếp tục; user có thể chỉnh sửa nếu muốn. |
| **Epic 14.4 — Retry Loop for Data Collection** | Mỗi nguồn: fetch → kiểm tra chất lượng → retry đến 2 lần với chiến lược thay thế trước khi đánh dấu thất bại. Pipeline không bao giờ dừng vì một nguồn thất bại. |

---

## Phase 15 — Pipeline Hardening & Skill Decomposition

**Goal:** Enforce strict, non-negotiable pipeline discipline across all skills. Split the `gather` skill into two focused skills (`gather` for files/URLs, `search` for internet discovery). Introduce a RULE.md enforcement layer that overrides all skill-level instructions. Establish a hard session-start discipline (state file + raw prompt saved before any skill invocation). Add an execute-test-pivot-audit loop as a mandatory delivery standard.

> **Origin:** Real-world feedback reveals four systemic gaps: (1) `gather` is too broad — mixing file reading and internet search reduces reliability; (2) automation level too low — Copilot still asks unnecessary questions instead of deciding autonomously; (3) execute-test-pivot-audit loop missing — skills deliver on a single attempt with no angle-change or re-test cycle; (4) hard workflow and state compliance too low — RULE.md at highest instruction priority can fix the root cause.

### Epics

| Epic | Description |
|------|-------------|
| **Epic 15.1 — gather / search Skill Split** | Extract web-search and internet-discovery logic from `gather` into a new focused `search` skill. `gather` becomes file+URL only. Update `copilot-instructions.md` skill registry to reference both skills. |
| **Epic 15.2 — RULE.md Enforcement Layer** | Create `.github/RULE.md` with non-negotiable pipeline rules (state init, workflow order, audit gates, autonomous execution, no unnecessary questions). Inject mandatory reference at top of `copilot-instructions.md` with `[MANDATORY — overrides all other instructions]` marker. |
| **Epic 15.3 — Hard Session Start Discipline** | Define and enforce the non-negotiable session init sequence: create state file + save raw prompt via `scripts/save_state.py` as the absolute first action before any skill routing. Add parallel template creation — output template spawned concurrently with prompt analysis. |
| **Epic 15.4 — Execute-Test-Pivot-Audit Loop** | Define the standard execute → self-review → change angle → retest → auditor → re-execute loop. Specify pivot strategies (angle, depth, structure change) per skill type. Apply loop to gather, search, compose, and all gen-* skills. |

---

## Phase 15 — Pipeline Hardening & Skill Decomposition (Tiếng Việt)

**Mục tiêu:** Bắt buộc kỷ luật pipeline không thương lượng trên toàn bộ skill. Tách skill `gather` thành hai skill (`gather` cho file/URL, `search` cho tìm kiếm internet). Tạo lớp bắt buộc RULE.md ghi đè mọi instruction cấp skill. Thiết lập kỷ luật bắt đầu session cứng (lưu state file + raw prompt trước mọi skill). Thêm vòng lặp execute-test-pivot-audit như tiêu chuẩn giao hàng bắt buộc.

> **Nguồn gốc:** Phản hồi thực tế cho thấy bốn khoảng thiếu hệ thống: (1) `gather` quá rộng — trộn lẫn đọc file và tìm kiếm internet làm giảm độ tin cậy; (2) mức độ tự động hóa quá thấp — Copilot vẫn hỏi thừa thay vì tự quyết; (3) thiếu vòng lặp execute-test-pivot — skill giao hàng sau một lần thử không có chu kỳ đổi góc và retest; (4) tuân thủ hard workflow và state quá thấp — RULE.md ở mức ưu tiên cao nhất có thể fix root cause.

| Epic | Mô tả |
|------|-------|
| **Epic 15.1 — Tách skill gather / search** | Tách logic tìm kiếm web và khám phá internet từ `gather` sang skill `search` mới. `gather` chỉ còn xử lý file + URL. Cập nhật registry trong `copilot-instructions.md`. |
| **Epic 15.2 — Lớp bắt buộc RULE.md** | Tạo `.github/RULE.md` với luật pipeline không thương lượng (init state, thứ tự workflow, cổng audit, thực thi tự động, không hỏi thừa). Inject tham chiếu bắt buộc đầu `copilot-instructions.md`. |
| **Epic 15.3 — Kỷ luật bắt đầu session cứng** | Định nghĩa và bắt buộc trình tự init session: tạo state file + lưu raw prompt qua `save_state.py` là hành động đầu tiên tuyệt đối trước mọi routing. Template output tạo song song với phân tích prompt. |
| **Epic 15.4 — Vòng lặp Execute-Test-Pivot-Audit** | Định nghĩa vòng lặp chuẩn execute → tự đánh giá → đổi góc → retest → auditor → thực thi lại. Chỉ định chiến lược pivot theo từng loại skill. Áp dụng cho gather, search, compose, và tất cả gen-* skills. |

---

## Phase 16 — Agent-Centric Architecture & Tool-Agnostic Search

**Goal:** Formalize the agent-centric hard-flow as the canonical execution model. No agent replaces another — all agents are peer-level with single responsibilities. Introduce an Execution Agent that owns tool selection and task execution. Replace hard-coded search tool dependency with an auto-cascade fallback strategy. Failed steps trigger re-planning by Advisory/Strategist — not dumb retries. Accumulate experience templates from successful runs for future reuse.

> **Origin:** Real-world failure — `vscode-websearchforcopilot_webSearch` requires Tavily auth popup, blocking non-tech users silently. Broader issue: pipeline has no agent dedicated to *execution* — orchestrator, strategist, and skills all partially own it. This phase formalizes the Hard-Flow agent protocol and makes tool selection adaptive.

### Epics

| Epic | Description |
|------|-------------|
| **Epic 16.1 — Tool-Agnostic Search Cascade** | `search` skill probes tool availability before each call. Cascade: (1) `vscode-websearchforcopilot` if available → (2) Playwright stealth mode → (3) HTTP zero-auth (DuckDuckGo/Brave free tier). No auth popup ever surfaced to user. Unavailability is silently handled, not reported as an error. |
| **Epic 16.2 — Execution Agent** | Create `execution.agent.md` in `.github/agents/`. Receives task + available tools from orchestrator → executes → ships result to Auditor. Owns tool selection per task. Can self-request Advisory or Strategist to generate a child soft-flow if a step proves too complex or tool cascade exhausts all options. Peer-level with all other agents. |
| **Epic 16.3 — Hard-Flow Protocol in RULE.md** | Formalize the canonical execution order in RULE.md as non-negotiable law: (1) Orchestrator creates state + audit checklist immediately on request → (2) Orchestrator calls Strategist for soft-flow → (3) Orchestrator routes to Execution Agent → (4) Execution Agent ships to Auditor → (5a) Pass: Auditor reports to Orchestrator → Orchestrator notifies user. (5b) Fail: Auditor calls Advisory → Advisory generates new soft plan → Execution Agent retries. Child soft-flows triggered by Execution Agent for complex steps. |
| **Epic 16.4 — Adaptive Re-planning on Failure** | When any step fails (tool unavailable, quality below threshold), Execution Agent calls Advisory or Strategist to generate a *new approach* — different tool, different source, different query strategy. Never retries with the same method. Advisory response = new soft plan. Strategist response = revised workflow steps. |
| **Epic 16.5 — Experience Template Accumulation** | After a successful pipeline run, Execution Agent calls a summary routine: extract what worked (tool path, query strategy, source list, pivot sequence) → save as experience template in `tmp/experience-templates/`. On future similar requests, orchestrator loads matching templates to prime the strategist's plan. Templates accumulate over sessions; stale templates are versioned, not deleted. |

---

## Phase 16 — Kiến trúc Agent-centric & Tìm kiếm Tool-Agnostic (Tiếng Việt)

**Mục tiêu:** Chuẩn hóa Hard-Flow agent-centric làm mô hình thực thi chính thức. Không agent nào thay thế agent khác — tất cả ngang hàng, mỗi agent một trách nhiệm duy nhất. Thêm Execution Agent sở hữu lựa chọn tool và thực thi task. Thay thế phụ thuộc cứng vào search tool bằng chiến lược fallback tự động. Bước thất bại kích hoạt tái hoạch định qua Advisory/Strategist — không phải retry mù quáng. Tích lũy experience template từ các run thành công để tái sử dụng.

> **Nguồn gốc:** Thất bại thực tế — `vscode-websearchforcopilot_webSearch` yêu cầu popup xác thực Tavily, block user non-tech trong im lặng. Vấn đề sâu hơn: pipeline không có agent nào chuyên về *thực thi* — orchestrator, strategist, và skill đều sở hữu một phần. Phase này chuẩn hóa giao thức Hard-Flow agent và làm cho lựa chọn tool thích nghi.

| Epic | Mô tả |
|------|-------|
| **Epic 16.1 — Search Cascade Tool-Agnostic** | Skill `search` dò tool trước mỗi lần gọi. Cascade: (1) `vscode-websearchforcopilot` nếu có → (2) Playwright stealth → (3) HTTP zero-auth. Không có popup nào hiển thị với user. Không khả dụng thì xử lý ngầm, không báo lỗi ra ngoài. |
| **Epic 16.2 — Execution Agent** | Tạo `execution.agent.md` trong `.github/agents/`. Nhận task + tool từ orchestrator → thực thi → ship kết quả đến Auditor. Sở hữu lựa chọn tool. Có thể tự request Advisory hoặc Strategist để tạo child soft-flow nếu bước quá phức tạp. Ngang hàng với tất cả agent khác. |
| **Epic 16.3 — Hard-Flow Protocol trong RULE.md** | Chuẩn hóa thứ tự thực thi không thể thương lượng trong RULE.md: (1) Orchestrator tạo state + audit checklist ngay lập tức → (2) Gọi Strategist tạo soft-flow → (3) Điều phối đến Execution Agent → (4) Execution Agent ship đến Auditor → (5a) Pass: Auditor báo Orchestrator → thông báo user. (5b) Fail: Auditor gọi Advisory → Advisory tạo soft plan mới → Execution Agent retry. Child soft-flow do Execution Agent kích hoạt cho các bước phức tạp. |
| **Epic 16.4 — Tái hoạch định thích nghi khi thất bại** | Khi bước thất bại, Execution Agent gọi Advisory hoặc Strategist để tạo *phương pháp mới* — tool khác, nguồn khác, chiến lược query khác. Không bao giờ retry cùng phương pháp. |
| **Epic 16.5 — Tích lũy Experience Template** | Sau pipeline thành công, tổng kết những gì đã hoạt động → lưu thành experience template trong `tmp/experience-templates/`. Các request tương tự trong tương lai sẽ load template phù hợp để khởi động kế hoạch của Strategist. Template tích lũy qua session; template cũ được versioned, không xóa. |

---

*Roadmap này không bao gồm task-level breakdown. Xem User Stories để biết chi tiết triển khai.*  
*Bước tiếp theo: `/product-roadmap-review` hoặc `/roadmap-to-user-stories`*
