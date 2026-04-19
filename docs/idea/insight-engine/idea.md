# InsightEngine — Idea Analysis

> **Idea Slug:** insight-engine  
> **Analysis Date:** 2026-04-16 (Phase 10 update: 2026-04-18)  
> **Status:** REVIEWED — READY (Phase 0-9 DONE; Phase 10 PLANNED)

---

## 1. Problem Statement

### English

Individual professionals (researchers, analysts, students, consultants) routinely face the same painful workflow: gathering information from scattered sources (web pages, PDFs, Excel files, Word documents, presentations), manually synthesizing that information, and then reformatting it into a deliverable — a report, a slide deck, a spreadsheet, or a web page.

This process is:
- **Time-consuming**: Hours spent copy-pasting, reformatting, and restructuring
- **Error-prone**: Manual transfer loses context, introduces inconsistencies
- **Repetitive**: The same gather → synthesize → output pattern repeats daily
- **Tool-fragmented**: Users juggle 5-10 different tools with no unified flow
- **Search-ineffective for structured data**: Finding specific items (sales leads, job openings, products, company profiles) across platforms requires specialist knowledge — knowing which sites to use, how to construct platform-specific queries, and how to navigate inside each site. Generic AI assistants return generic Google results, not direct item URLs.
- **Search-ineffective for structured data**: Finding specific items (sales leads, job openings, products, company profiles) across platforms requires specialist knowledge — knowing which sites to use, how to construct platform-specific queries, and how to navigate inside each site. Generic AI assistants return generic Google results, not direct item URLs.

Current AI assistants can help with parts of this (e.g., summarize one document), but none provide an **end-to-end pipeline** that handles multi-source ingestion, intelligent synthesis, and multi-format output — all within a single conversational interface.

**Why it matters:** Knowledge workers spend up to 30% of their time on information gathering and reformatting rather than analysis and decision-making.

### Tiếng Việt

Các cá nhân (nhà nghiên cứu, chuyên viên phân tích, sinh viên, tư vấn viên) thường xuyên phải đối mặt với quy trình lặp đi lặp lại: thu thập thông tin từ nhiều nguồn rời rạc (trang web, PDF, Excel, Word, PowerPoint), tổng hợp thủ công, rồi chuyển đổi thành sản phẩm hoàn chỉnh — báo cáo, slide thuyết trình, bảng tính, hoặc trang web.

Quy trình này tốn thời gian, dễ sai sót, lặp lại liên tục, và đòi hỏi sử dụng nhiều công cụ khác nhau mà không có một luồng xử lý thống nhất. Ngoài ra, việc tìm kiếm dữ liệu có cấu trúc (sales lead, tin tuyển dụng, sản phẩm, hồ sơ công ty) trên nhiều nền tảng đòi hỏi kiến thức chuyên biệt mà các công cụ AI hiện tại không đáp ứng được.

**Tại sao quan trọng:** Người lao động tri thức dành đến 30% thời gian cho việc thu thập và định dạng lại thông tin thay vì phân tích và ra quyết định.

---

## 2. Target Users

### English

**Primary users:**
- Individual professionals who need to compile data and create presentations/reports
- Vietnamese-speaking users (UI/communication in Vietnamese)
- People already using VS Code with GitHub Copilot

**User profiles:**
- **Researcher/Analyst**: Gathers data from multiple web sources and documents, needs structured reports
- **Student/Academic**: Compiles literature reviews, creates presentation decks from research papers
- **Consultant/Business professional**: Builds client deliverables from diverse data sources
- **Sales/Business development**: Compiles lead lists, company profiles, contact information from platforms (LinkedIn, industry directories, job boards) — needs structured output with direct source URLs
- **Content creator**: Transforms raw information into polished multi-format outputs

**Secondary/indirect users:**
- Recipients of the generated documents (colleagues, clients, audiences)

### Tiếng Việt

**Người dùng chính:**
- Cá nhân cần tổng hợp dữ liệu và tạo thuyết trình/báo cáo
- Người dùng tiếng Việt (giao diện và giao tiếp bằng tiếng Việt)
- Người đang sử dụng VS Code với GitHub Copilot

**Người dùng phụ:**
- Người nhận tài liệu được tạo ra (đồng nghiệp, khách hàng, khán giả)

---

## 3. Value Proposition

### English

InsightEngine transforms the fragmented "gather → synthesize → format" workflow into a **single conversational pipeline**:

1. **One interface, many inputs**: Describe what you need in Vietnamese, point to URLs/files, or let the system search — all in one conversation
2. **Intelligent synthesis**: Not just concatenation — the system understands, compares, and restructures content meaningfully
3. **Multi-format output**: Same content can become a Word doc, Excel sheet, PowerPoint deck, PDF, or HTML page
4. **Rich template library**: Professional pre-built templates across multiple styles — 8-10 PPTX templates (ref: slidemembers.com, aippt.com, canva.com), 5-8 HTML presentation templates (ref: revealjs.com, slides.com, deckdeckgo.com)
5. **Presentation-grade HTML**: HTML output is not static pages but interactive presentations with slide transitions, animations, and background effects — powered by reveal.js
6. **Script-powered skills**: Each output skill has executable scripts (Python/Node.js CLI tools) for reliable, repeatable output generation — not just Copilot instructions
7. **Vietnamese-first**: Entire experience designed for Vietnamese speakers, with bilingual capability
8. **Zero infrastructure**: Runs entirely within VS Code + Copilot — no servers, no API keys, no subscriptions beyond Copilot
9. **Model-agnostic skills**: Skill prompts optimized to work consistently with smaller models (GPT-4o-mini, GPT-3.5 Turbo) — not just Claude/GPT-4
10. **Session resilience**: Pipeline automatically saves state after each step — can resume if a Copilot session is interrupted mid-pipeline
11. **VS Code custom agents** *(Phase 9 alignment)*: Agents follow the official VS Code custom agent standard — `.agent.md` files in `.github/agents/`, peer-level with skills (`.github/skills/`). Agents have YAML frontmatter (description, tools, model, handoffs, agents), enabling native agent picker integration, handoff workflows, and subagent invocation. Auditor verifies output quality at every generation point, not only at pipeline end
12. **Model self-awareness with decision maps**: Pipeline detects model capabilities via self-declaration + pre-built decision maps — avoids hallucination about capabilities by verifying against known benchmarks
13. **Quality-first with audit loops**: Tiered audit system (self-review → agent audit → final audit) ensures output quality at every critical step, with automatic retry and step-level rollback
14. **Zero-question UX** *(strengthened Phase 12)*: Pipeline NEVER asks technical questions. ALL technical choices (tools, libraries, query strategies, file formats, platform selection) are auto-decided. Only content decisions may involve the user (e.g., "which companies to include"). Pipeline runs to completion after the initial request — user is only contacted on content ambiguity or total failure.
15. **Dedicated orchestrator, focused skills** *(Phase 9)*: A central orchestrator agent (`dieu-phoi`) handles ALL request types — not just content synthesis. `tong-hop` returns to its natural role as a pure content synthesis skill, doing what its name says: synthesize content. The orchestrator can route creative requests, research tasks, design projects, and mixed workflows without forcing them through the "gather → synthesize → output" pattern
16. **Adaptive self-improvement with user consent** *(Phase 9)*: When a request exceeds current capabilities (e.g., "phóng tác Thánh Gióng thành truyện tranh manga"), the system transparently assesses the gap, proposes creating new agents/skills (literary author, manga art), and proceeds only with user's explicit consent. If self-improvement takes >30 minutes, the system notifies the user and waits for approval
17. **QA-grade weighted audit scoring** *(Phase 9)*: Auditor analyzes each request's requirements to dynamically generate a weighted test case set (100 points total). Critical requirements get higher weight. Score >80/100 to pass. Retries target specific weak areas instead of blind regeneration — max 5 attempts
18. **True cross-session resume** *(Phase 9)*: Working state saves the complete pipeline context — raw prompt, analyzed requirements, generated plan/workflow, and step-level state — enabling full resume in a new session when the current session becomes too heavy
19. **English naming with natural language UX** *(Phase 10)*: All skill and agent names standardized to English (e.g., `gather`, `compose`, `gen-word`, `orchestrator`) for international consistency. Users still interact in Vietnamese (or any language) — the orchestrator classifies intent from natural language without requiring slash commands. Technical names are English; user experience remains Vietnamese-first
20. **Product doc alignment & legacy cleanup** *(Phase 10)*: Consistent naming across all product documents, removal of legacy `shared-agents/` directory, backfill missing user stories for existing skills (`design`, `verify`, `improve`), and fix known inconsistencies (story count, stale headers)
21. **Adaptive search intelligence** *(Phase 11)*: For complex structured data requests (sales leads, job searches, product catalogs), the pipeline generates a specialized search sub-flow per step — rather than a flat Google query. Sub-flow: (1) plan target sources, (2) search via `site:source.com` for platform-specific results, (3) if thin results, navigate into the source's DOM to discover internal structure and search endpoints, (4) use the site's own internal search, (5) for sources that show details via popup or inline expansion, extract the canonical detail-page URL. If a sub-flow fails after 2 attempts, call the advisory agent to propose an alternative flow and present options to the user before retrying.
22. **Fire-and-forget pipeline mode** *(Phase 12)*: After the user confirms the pipeline plan, execution runs fully autonomously to completion. No intermediate confirmations, no batch-by-batch approvals. User receives a single final delivery summary: files created, counts, sources used. Inspired by n8n's automation model — set up once, get results.
23. **Adaptive user communication** *(Phase 12)*: Pipeline detects user technical level from language and behavior signals. For non-technical users, all jargon is hidden (no JSON, Playwright, crawler, seed, HTTP, DOM, endpoint in messages). Progress is shown as human-readable updates: "Đang tìm trên ITViec... ✅ 23 jobs tìm được" instead of "Fetching listings from seed query batch 3 via Playwright stealth mode".

### Tiếng Việt

InsightEngine biến quy trình rời rạc "thu thập → tổng hợp → định dạng" thành **một pipeline hội thoại duy nhất**:

1. **Một giao diện, nhiều nguồn đầu vào**: Mô tả yêu cầu bằng tiếng Việt, trỏ đến URL/file, hoặc để hệ thống tự tìm kiếm
2. **Tổng hợp thông minh**: Không chỉ ghép nối — hệ thống hiểu, so sánh, và tái cấu trúc nội dung
3. **Đầu ra đa định dạng**: Cùng nội dung có thể thành Word, Excel, PowerPoint, PDF, hoặc HTML
4. **Thư viện template phong phú**: Template chuyên nghiệp — 8-10 PPTX templates (tham khảo slidemembers, aippt, canva), 5-8 HTML presentation templates (tham khảo reveal.js, slides.com, deckdeckgo)
5. **HTML dạng thuyết trình**: Output HTML không phải trang tĩnh mà là presentation tương tác với hiệu ứng chuyển slide, animation, background ấn tượng — dựa trên reveal.js
6. **Skill có script thực thi**: Mỗi skill output có scripts/ CLI tools (Python/Node.js) để tạo output đáng tin cậy, có thể lặp lại
7. **Ưu tiên tiếng Việt**: Toàn bộ trải nghiệm thiết kế cho người Việt
8. **Không cần hạ tầng**: Chạy hoàn toàn trong VS Code + Copilot
9. **Tương thích đa model**: Skill được tối ưu để hoạt động ổn định với cả model nhỏ (GPT-4o-mini, GPT-3.5 Turbo) — không chỉ Claude/GPT-4
10. **Độ bền session**: Pipeline tự động lưu state sau mỗi bước — có thể tiếp tục nếu session Copilot bị ngắt giữa chừng
11. **VS Code custom agents** *(Phase 9)*: Agents tuân thủ tiêu chuẩn custom agent của VS Code — file `.agent.md` trong `.github/agents/`, ngang hàng với skills (`.github/skills/`). YAML frontmatter (description, tools, model, handoffs, agents), tích hợp agent picker, handoff workflows, và subagent invocation. Auditor kiểm tra output ở mọi điểm tạo file
12. **Tự nhận diện model với bản đồ quyết định**: Pipeline phát hiện năng lực model qua self-declaration + decision maps — tránh ảo giác về năng lực bằng cách đối chiếu benchmark
13. **Chất lượng trên hết với vòng audit**: Hệ thống audit phân tầng (self-review → agent audit → final audit) đảm bảo chất lượng ở mỗi bước quan trọng, tự retry và rollback
14. **UX không hỏi thừa** *(tăng cường Phase 12)*: Pipeline KHÔNG BAO GIỜ hỏi các câu kỹ thuật. MỌI quyết định kỹ thuật (công cụ, thư viện, chiến lược tìm kiếm, định dạng file, lựa chọn nền tảng) đều tự quyết định. Chỉ các quyết định về NỘI DUNG mới có thể hỏi user (ví dụ: "muốn bao gồm công ty nào"). Pipeline chạy đến khi hoàn tất sau request ban đầu — chỉ liên hệ user khi nội dung chưa rõ hoặc hoàn toàn thất bại.
15. **Orchestrator chuyên biệt, skill đúng vai** *(Phase 9)*: Agent trung tâm (`dieu-phoi`) tiếp nhận MỌI loại yêu cầu — không chỉ tổng hợp nội dung. `tong-hop` trở về vai trò tổng hợp nội dung thuần túy. Orchestrator route yêu cầu sáng tạo, nghiên cứu, thiết kế, và mixed workflow mà không ép qua pattern "thu thập → tổng hợp → xuất"
16. **Tự cải thiện thích ứng** *(Phase 9)*: Khi yêu cầu vượt năng lực hiện tại (ví dụ: "phóng tác Thánh Gióng thành manga"), hệ thống tự đánh giá, đề xuất tạo agent/skill mới, và tiến hành khi user đồng ý. Thông báo nếu >30 phút
17. **Audit thang điểm 100 kiểu QA** *(Phase 9)*: Auditor phân tích yêu cầu để tạo bộ test case có trọng số (tổng 100 điểm). Yêu cầu quan trọng hơn → điểm cao hơn. >80/100 mới pass. Retry nhắm vào điểm yếu cụ thể — tối đa 5 lần
18. **Resume xuyên session** *(Phase 9)*: State lưu đầy đủ: raw prompt, yêu cầu đã phân tích, plan/workflow, state từng step — cho phép resume hoàn chỉnh ở session mới
19. **Đặt tên tiếng Anh với UX ngôn ngữ tự nhiên** *(Phase 10)*: Tất cả skill và agent được chuẩn hóa tên tiếng Anh (ví dụ: `gather`, `compose`, `gen-word`, `orchestrator`). User vẫn tương tác bằng tiếng Việt — orchestrator phân loại intent từ ngôn ngữ tự nhiên, không cần slash commands
20. **Căn chỉnh tài liệu & dọn dẹp legacy** *(Phase 10)*: Tên nhất quán xuyên suốt tài liệu, xóa thư mục `shared-agents/` cũ, bổ sung user stories cho skills thiếu (`design`, `verify`, `improve`), sửa các lỗi nhất quán đã phát hiện
21. **Tìm kiếm thông minh thích ứng** *(Phase 11)*: Với các yêu cầu tìm kiếm có cấu trúc (sales lead, tin tuyển dụng, sản phẩm), pipeline tự tạo sub-flow tìm kiếm chuyên biệt cho từng bước: (1) lên kế hoạch nguồn, (2) tìm `site:nguồn.com`, (3) nếu kết quả mỏng, khám phá DOM của trang nguồn để tìm cấu trúc nội trang và endpoint tìm kiếm, (4) dùng công cụ tìm kiếm nội trang, (5) với nguồn có popup/detail inline, trích xuất URL trang detail chính xác. Nếu sub-flow thất bại sau 2 lần, gọi advisory agent đề xuất flow thay thế và hỏi ý kiến user.
22. **Chế độ pipeline tự động hoàn toàn** *(Phase 12)*: Sau khi user xác nhận kế hoạch pipeline, toàn bộ quá trình thực thi chạy tự động đến khi hoàn tất. Không có xác nhận trung gian, không cần phê duyệt từng batch. User nhận một tin nhắn tổng kết cuối: file đã tạo, số lượng, nguồn đã dùng. Lấy cảm hứng từ mô hình tự động hóa của n8n — thiết lập một lần, nhận kết quả.
23. **Giao tiếp thích ứng với user** *(Phase 12)*: Pipeline phát hiện trình độ kỹ thuật của user từ ngôn ngữ và tín hiệu hành vi. Với user không chuyên kỹ thuật, mọi jargon bị ẩn đi (không có JSON, Playwright, crawler, seed, HTTP, DOM, endpoint trong tin nhắn). Tiến độ hiển thị dạng thân thiện: "Đang tìm trên ITViec... ✅ 23 jobs tìm được" thay vì "Fetching listings from seed query batch 3 via Playwright stealth mode".
---

## 4. In-Scope

### English

**Core pipeline (Skill chính — "Động cơ tổng hợp"):**
- Receive user request in Vietnamese (or English)
- Orchestrate input gathering, synthesis, and output generation
- Intelligently select and invoke sub-skills based on user intent

**Input capabilities:**
- Read files from local filesystem (Word, Excel, PDF, PPT, text, markdown)
- Fetch web page content from provided URLs
- Search Google via VS Code/Copilot web search tool and extract relevant results
- Accept inline text/data from user prompt

**Synthesis capabilities:**
- Merge and restructure content from multiple sources
- Translate content between languages (Vietnamese ↔ English primarily)
- Compare and contrast multiple sources
- Extract key information and summarize
- Generate charts/visualizations from data

**Output formats:**
- Word documents (.docx) — with professional formatting and templates
- Excel spreadsheets (.xlsx) — with formulas, formatting, data organization
- PowerPoint presentations (.pptx) — with multiple style templates
- PDF documents (.pdf) — from generated content
- HTML pages — static sites with professional styling
- Generated images for slide decks (icons, illustrations, charts)

**Template system:**
- Multiple pre-built templates per output format
- Different styles: corporate, academic, minimal, creative, dark/modern + specialized variants
- PPTX: 8-10 professional templates (ref: slidemembers.com, aippt.com, canva.com)
- HTML: 5-8 reveal.js-based presentation templates with slide transitions, animations, backgrounds (ref: revealjs.com, slides.com/templates, deckdeckgo.com)
- User can select style or let the system choose based on context
- Template preview/selection before generation

**Skill architecture (script-powered):**
- All skill names and directories in **English** (Phase 10 migration from Vietnamese to English)
- Skill triggers: **natural language** (bilingual Vietnamese + English) — no slash commands required
- Skill internal content in English (for Copilot performance)
- SKILL.md acts as router — references sub-docs and scripts/ for details
- Each skill has `scripts/` directory with executable CLI tools (Python/Node.js)
- Multi-level scripts for different needs (e.g., gen_image.py vs gen_portrait_v5.py)
- `references/` directory for prompt guides, API docs, template specs
- Pattern follows: a-z-copilot-flow/skills/gen-image, skills/pptx
- Pipeline skill has knowledge of all sub-skills
- SKILL.md files optimized for small model compatibility (≤ 300 lines, step-by-step instructions)
- Session state persistence: pipeline writes `.session-state.json` after each step for resume capability

**Agent architecture (Phase 6 design → Phase 8 shared → Phase 9 VS Code standard):**
- Phase 6 designed agents as inline tong-hop instructions
- Phase 8 refactored into shared agents via `runSubagent`
- **Phase 9 alignment**: Agents follow the **official VS Code custom agent standard** (ref: https://code.visualstudio.com/docs/copilot/customization/custom-agents)
- Agent files use `.agent.md` format with YAML frontmatter (description, name, tools, model, agents, handoffs, user-invocable)
- Agents live in `.github/agents/` — **peer-level with** `.github/skills/`, NOT nested inside skills
- 4 custom agents: `orchestrator` (central routing, formerly `dieu-phoi`), `auditor` (quality), `strategist` (workflow), `advisory` (decisions)
- Agents appear in VS Code's agent picker dropdown — user can invoke directly or via handoff
- `handoffs` enable guided workflows between agents (e.g., dieu-phoi → auditor after output)
- `user-invocable: false` for agents that should only be called as subagents (strategist, advisory)
- `user-invocable: true` for agents users interact with directly (dieu-phoi, auditor)
- Agent `tools` field restricts tool access per agent role (e.g., auditor = read-only tools)
- Agent `agents` field controls which subagents each agent can invoke
- Shared context file (`tmp/.agent-context.json`) for inter-agent communication
- Model self-awareness via self-declaration + decision maps (NO hardcoded model name)
- Decision maps per capability category: context_window, reasoning_depth, tool_use, multilingual, code_generation — each with 3 levels
- Fallback to conservative/medium profile if model cannot self-identify
- Budget: auditor max 5 calls/pipeline, advisory max 2, strategist max 1

**Strict file rules (Phase 6):**
- All scripts MUST be placed in `/scripts`
- All temporary files MUST be placed in `/tmp`
- All output files MUST be placed in `/output`
- Enforced across ALL skills and ALL models

**Auto-escalation protocol (Phase 6):**
- When a tool/approach fails, automatically escalate to a more powerful alternative
- Example: thu-thap fetch_webpage fail → httpx → Playwright stealth — never ask user which tier to use
- Only ask user when ALL escalation tiers have been exhausted

**Dynamic workflow generation (Phase 6):**
- Strategist agent receives user request + model profile → generates custom workflow
- Pre-built workflow templates for common scenarios × model capability levels
- 10-minute self-improvement budget (max) before execution starts

**Conditional runtime skill creation (Phase 6):**
- Advisory agent evaluates: is a new skill REQUIRED (cannot complete without it)?
- If yes: allow creation with 30-minute budget, prioritize cloning from verified public repos (anthropics/skills, openclaw/skills, openai/skills)
- MANDATORY security check before cloning any external skill
- If advisory says not needed: use existing skills + inline instructions

**Central Orchestrator Agent — `orchestrator.agent.md` (Phase 9 → Phase 10 renamed from `dieu-phoi`):**
- VS Code custom agent (`.github/agents/orchestrator.agent.md`) — user-invocable, appears in agent picker
- YAML frontmatter: `tools: [*]`, `agents: [auditor, strategist, advisory]`, `handoffs` to auditor after output
- Replaces tong-hop as the central request handler — tong-hop becomes a pure content synthesis skill
- Analyzes ANY user request and classifies intent from **natural language** (no slash commands needed): synthesis / creation / research / design / data_collection / mixed / unknown
- Routes to appropriate skill(s) and agent(s) based on intent — not just the gather→synthesize→output pattern
- Integrates with strategist, auditor, and advisory agents via native `agents` field (not ad-hoc runSubagent)
- Handles creative requests (literature, art, comics) by composing multiple skills/agents
- Manages the full pipeline lifecycle including retry, rollback, and cross-session resume
- Uses `handoffs` for guided transitions: dieu-phoi → auditor (verify) → dieu-phoi (retry if needed)

**Adaptive Self-Improvement Protocol (Phase 9):**
- **Gap assessment**: Before execution, orchestrator evaluates whether current skills/agents can fully satisfy the request
- **Capability expansion**: If a gap is identified, the system can:
  - Create new specialized agents (e.g., literary author agent for creative writing, art director agent for visual storytelling)
  - Upgrade existing skills (e.g., enhance tao-hinh for sequential art / manga panels)
  - Create entirely new skills (e.g., skill for comic/manga page layout, skill for literary composition)
- **User consent required**: The system MUST explain what it plans to create/upgrade, estimated time, and why. Proceed only with user's explicit approval
- **Time budget with notification**: If self-improvement will take >30 minutes, notify user with explanation and estimated duration. Continue only with user consent. No hard time limit if user agrees
- **Breaking existing limits**: With user consent, the system can exceed the 30-minute skill creation budget from Phase 6. The user explicitly "unlocks" extended self-improvement
- **Quality gate on created skills**: New skills/agents are tested before use in the current pipeline. If creation fails, fall back to best-effort with existing capabilities

**Enhanced Working State & Cross-Session Resume (Phase 9):**
- Session state (`tmp/.session-state.json`) upgraded to store complete pipeline context:
  - `raw_prompt`: Exact user input text (preserved verbatim)
  - `analyzed_requirements`: Orchestrator's analysis (intent, dimensions, fields, constraints)
  - `generated_plan`: The workflow/plan created by strategist or orchestrator
  - `step_states[]`: Per-step detail — input, output summary, status (pending/running/done/failed), retry count, audit score
  - `audit_test_cases[]`: The weighted test case set generated by auditor for this request
  - `created_skills[]`: Any skills/agents created during self-improvement (for persistence across sessions)
- Cross-session resume: When a new session starts and state file exists, orchestrator can fully reconstruct context and continue from the exact checkpoint
- State file is self-documenting: a human or a new Copilot session can read it and understand the full pipeline status

**100-Point Weighted Audit Scoring System (Phase 9):**
- **Replaces binary PASS/FAIL** with granular, requirement-specific quality measurement
- **Dynamic test case generation**: Auditor reads the user's original requirements and generates a custom test case set — like a QA engineer creating test cases from a feature specification
- **Weighted scoring**: Each test case gets a point value based on its importance to output quality. Total always sums to 100 points. Examples:
  - Core requirement coverage: 15-25 points per critical aspect
  - Data specificity and accuracy: 10-15 points
  - Source quality and citations: 5-10 points
  - Formatting and presentation: 5-10 points
  - Language quality: 3-5 points
  - Added-value insights: 2-5 points
- **Pass threshold: >80/100** — Output must score above 80 points to proceed
- **Max 5 retries** (up from 3 in Phase 6): Each retry targets the specific test cases that scored low, with improvement instructions derived from the scoring
- **Targeted retry**: Instead of regenerating everything, the system identifies which step produced the low-scoring test cases and re-executes only that step with specific improvement guidance
- **Audit report**: Each audit produces a structured report showing every test case, its score, and specific evidence/reasoning — stored in working state for cross-session visibility
- **Score progression tracking**: Working state tracks audit scores across retries (e.g., attempt 1: 62/100, attempt 2: 78/100, attempt 3: 85/100 → PASS). If score doesn't improve between consecutive retries, stop and deliver best available

### Tiếng Việt

**Pipeline chính:**
- Nhận yêu cầu bằng tiếng Việt, điều phối thu thập → tổng hợp → xuất kết quả

**Khả năng đầu vào:**
- Đọc file cục bộ (Word, Excel, PDF, PPT, text, markdown)
- Lấy nội dung web từ URL
- Tự tìm Google qua công cụ Copilot
- Nhận text/data trực tiếp từ user

**Khả năng tổng hợp:**
- Gộp và tái cấu trúc nội dung đa nguồn
- Dịch thuật (chủ yếu Việt ↔ Anh)
- So sánh đối chiếu nhiều nguồn
- Tạo biểu đồ/minh họa từ dữ liệu

**Định dạng đầu ra:**
- Word (.docx), Excel (.xlsx), PowerPoint (.pptx), PDF (.pdf), HTML, hình ảnh

**Hệ thống template:**
- Nhiều template sẵn có theo nhiều phong cách (corporate, academic, minimal, creative, dark/modern + biến thể chuyên biệt)
- PPTX: 8-10 template chuyên nghiệp (tham khảo: slidemembers, aippt, canva)
- HTML: 5-8 presentation template dựa trên reveal.js với hiệu ứng chuyển slide, animation, background

**Kiến trúc skill (có script thực thi):**
- Mỗi skill có thư mục `scripts/` chứa CLI tools (Python/Node.js)
- Multi-level scripts cho nhu cầu khác nhau
- `references/` chứa hướng dẫn, API docs, template specs
- Pattern theo: a-z-copilot-flow/skills/gen-image, skills/pptx
- SKILL.md tối ưu tương thích model nhỏ (≤ 300 dòng, hướng dẫn từng bước)
- Lưu state pipeline (.session-state.json) để hỗ trợ resume khi session bị ngắt

**Kiến trúc agent (Phase 6 → Phase 8 → Phase 9 chuẩn VS Code):**
- Phase 6 nhúng trong tong-hop. Phase 8 tái cấu trúc thành shared agents
- **Phase 9**: Tuân thủ **chuẩn VS Code custom agent** (ref: code.visualstudio.com/docs/copilot/customization/custom-agents)
- File `.agent.md` trong `.github/agents/` — **ngang hàng** với `.github/skills/`, KHÔNG lồng trong skills
- 4 custom agents: `orchestrator` (trung tâm, đổi tên từ `dieu-phoi`), `auditor` (chất lượng), `strategist` (workflow), `advisory` (tư vấn)
- YAML frontmatter: description, tools, model, agents (subagents), handoffs, user-invocable
- Hiển thị trong agent picker của VS Code — user chọn trực tiếp hoặc qua handoff
- `handoffs` cho workflow tuần tự: dieu-phoi → auditor → dieu-phoi
- `user-invocable: false` cho agent chỉ gọi qua subagent (strategist, advisory)
- Agent `tools` giới hạn quyền truy cập (auditor = read-only)
- File context chia sẻ (`tmp/.agent-context.json`) cho giao tiếp giữa các agent
- Model tự nhận diện qua self-declaration + bản đồ quyết định (KHÔNG hardcode model name)
- Budget: auditor max 5 lần/pipeline, advisory max 2, strategist max 1

**Quy tắc file bắt buộc (Phase 6):**
- Scripts PHẢI đặt trong `/scripts`
- File tạm PHẢI đặt trong `/tmp`
- Output PHẢI đặt trong `/output`

**Auto-escalation (Phase 6):**
- Khi tool/approach fail → tự nâng lên tool mạnh hơn, không hỏi user

**Tạo workflow động (Phase 6):**
- Strategist agent nhận request + model profile → tạo workflow tùy chỉnh
- Template workflow sẵn có cho scenarios phổ biến × mức năng lực model

**Tạo skill runtime có điều kiện (Phase 6):**
- Advisory agent đánh giá: có BẮT BUỘC phải tạo skill mới không?
- Nếu cần: cho phép tạo (30 phút), ưu tiên clone từ repos public đã xác minh
- Kiểm tra bảo mật BẮT BUỘC trước khi clone
- Nếu không cần: dùng skill hiện tại + inline instructions

**Agent Orchestrator trung tâm — `orchestrator.agent.md` (Phase 9 → Phase 10 đổi tên từ `dieu-phoi`):**
- VS Code custom agent (`.github/agents/orchestrator.agent.md`) — hiển thị trong agent picker
- YAML frontmatter: `tools: [*]`, `agents: [auditor, strategist, advisory]`, có `handoffs`
- Thay thế tong-hop làm điểm tiếp nhận mọi request — tong-hop trở thành skill tổng hợp thuần túy
- Phân loại intent từ **ngôn ngữ tự nhiên** (không cần slash commands): synthesis / creation / research / design / data_collection / mixed / unknown
- Route đến skill/agent phù hợp — không ép mọi request qua pattern thu thập → tổng hợp → xuất
- Tích hợp với strategist, auditor, advisory qua trường `agents` chuẩn (không phải ad-hoc)
- Xử lý yêu cầu sáng tạo (văn học, nghệ thuật, truyện tranh) bằng cách tổ hợp nhiều skill/agent
- `handoffs` cho chuyển tiếp: dieu-phoi → auditor (kiểm tra) → dieu-phoi (retry nếu cần)

**Cơ chế tự cải thiện thích ứng (Phase 9):**
- Đánh giá năng lực hiện tại vs yêu cầu — phát hiện khoảng trống
- Tự tạo agent mới (ví dụ: agent tác giả văn học, agent đạo diễn nghệ thuật)
- Nâng cấp skill hiện có hoặc tạo skill mới (ví dụ: skill truyện tranh manga)
- BẮT BUỘC có sự đồng ý user trước khi tạo. Thông báo nếu >30 phút
- User có thể "mở khóa" tự cải thiện mở rộng — phá giới hạn Phase 6
- Skill/agent mới phải test trước khi dùng trong pipeline hiện tại

**Working State nâng cấp & Resume xuyên session (Phase 9):**
- Lưu đầy đủ: raw_prompt, analyzed_requirements, generated_plan, step_states[], audit_test_cases[], created_skills[]
- Session mới có thể reconstruct hoàn toàn context và tiếp tục từ checkpoint chính xác
- File state tự mô tả — người hoặc session mới đều đọc hiểu được

**Audit thang 100 điểm kiểu QA (Phase 9):**
- Thay thế PASS/FAIL bằng đo lường chất lượng chi tiết theo yêu cầu cụ thể
- Auditor phân tích yêu cầu → tạo bộ test case có trọng số (tổng 100 điểm)
- Yêu cầu lõi: 15-25 điểm/mục; dữ liệu chính xác: 10-15 điểm; nguồn trích dẫn: 5-10 điểm; trình bày: 5-10 điểm
- Ngưỡng pass: >80/100. Tối đa 5 lần retry
- Retry nhắm vào test case điểm thấp — không tái tạo lại toàn bộ
- Báo cáo audit chi tiết từng test case, có theo dõi tiến trình điểm qua các lần retry

---

## 5. Out-of-Scope / Non-Goals

### English

- **NOT a web application** — no server, no database, no deployment
- **NOT a code development tool** — no governed workflow, no CI/CD, no testing pipeline
- **NOT a real-time collaboration tool** — single-user, local execution
- **NOT a fully autonomous agent** — agents assist within Copilot's conversational loop; user remains in control of final approval gates. Self-improvement requires explicit user consent. User can revoke at any time
- **NO dependency on a-z-copilot-flow at runtime** — repo must be fully self-contained
- **NO custom LLM/AI model** — relies entirely on GitHub Copilot (Claude) as the reasoning engine
- **NO paid API integrations** — Google search via built-in Copilot tool, no SerpAPI/custom search
- **NO interactive web dashboards** — output is static files, not running applications
- **NO video/audio processing** — text and image-based content only

### Tiếng Việt

- **KHÔNG** là ứng dụng web — không server, database, deployment
- **KHÔNG** là công cụ phát triển code — không có governed workflow, CI/CD
- **KHÔNG** là agent tự trị hoàn toàn — agents hỗ trợ trong vòng hội thoại Copilot; user vẫn kiểm soát approval gates. Tự cải thiện BẮT BUỘC có sự đồng ý user. User có thể thu hồi bất kỳ lúc nào
- **KHÔNG** phụ thuộc vào a-z-copilot-flow khi sử dụng — repo hoàn toàn độc lập
- **KHÔNG** dùng AI/LLM riêng — chỉ dùng GitHub Copilot
- **KHÔNG** tích hợp API trả phí
- **KHÔNG** xử lý video/audio

---

## 6. Assumptions

### English

1. **User has VS Code + GitHub Copilot** — this is the only runtime requirement
2. **User has Python 3.x installed** — needed for document generation scripts
3. **User has Node.js installed** — needed for pptxgenjs and some output tools
4. **Copilot supports the required tools** — web search, file reading, terminal execution
5. **Apple Silicon (M-series) for image generation** — gen-image skill requires MPS; non-Apple users can skip image generation or use alternatives
6. **User is comfortable with VS Code** — basic familiarity with editor and chat panel
7. **Internet access available** — for web search and URL fetching (offline mode limited to local files)
8. **Vietnamese is the primary language** — all user-facing text defaults to Vietnamese; English as secondary
9. **Self-improvement stays within Copilot capabilities** *(Phase 9)*: Created skills/agents still operate within Copilot's tool set (read_file, run_in_terminal, runSubagent, etc.). Self-improvement means better instructions and organization, not new runtime capabilities
10. **User provides creative direction for novel requests** *(Phase 9)*: For unprecedented requests (e.g., manga creation), user provides style references, examples, or creative direction. The system adapts its capabilities, but creative judgment ultimately comes from user + Copilot reasoning
11. **Session state file is not corrupted** *(Phase 9)*: Cross-session resume assumes the state file in `tmp/.session-state.json` is intact. If file is corrupted, pipeline starts fresh

### Tiếng Việt

1. User có VS Code + GitHub Copilot
2. Python 3.x và Node.js đã cài đặt
3. Apple Silicon cho tạo hình ảnh (tùy chọn)
4. User quen dùng VS Code cơ bản
5. Có kết nối internet (cho search và fetch web)
6. Tiếng Việt là ngôn ngữ chính
7. Tự cải thiện vẫn nằm trong khả năng tool của Copilot *(Phase 9)*
8. User cung cấp hướng sáng tạo cho yêu cầu mới lạ *(Phase 9)*
9. File state không bị hỏng — nếu hỏng thì pipeline bắt đầu lại *(Phase 9)*

---

## 7. Risks & Unknowns

### English

**Product risks:**
- **Skill complexity**: The pipeline skill must orchestrate many sub-skills — getting the routing logic right is critical
- **Template quality**: Pre-built templates must look professional; poor design will undermine trust
- **Vietnamese language quality**: AI-generated Vietnamese must be natural and accurate, not machine-translated
- **Skill size constraint (≤400 lines)**: Complex skills may be hard to keep under the limit while maintaining clarity

**Technical risks:**
- **Web search reliability**: VS Code web search tool quality may vary; results may not always be relevant
- **File format edge cases**: PDF extraction can be lossy; complex Excel formulas may not transfer cleanly
- **Image generation dependency on Apple Silicon**: Limits portability for non-Mac users
- **Copilot context window**: Large multi-source synthesis may exceed context limits
- **Subagent statelessness**: Each subagent call is stateless — must pass full context via shared context file; risk of information loss between agents
- **Token overhead from agent calls**: Multiple agent calls (strategist + audit + advisory) multiply token usage 2-4x; mitigated by tiered audit and budget cap
- **Advisory non-convergence**: Multiple perspectives may conflict; mitigated by single-call multi-perspective approach
- **Cloned skill security**: External skills from public repos may contain vulnerabilities; mitigated by mandatory security review before adoption
- **Model self-awareness accuracy**: Models may hallucinate about their capabilities; mitigated by decision maps that verify claims against known benchmarks

**Adoption risks:**
- **Learning curve**: Users must understand the skill/prompt mental model
- **Expectation management**: AI output quality varies; users may expect perfection
- **Vietnamese-only naming**: May confuse non-Vietnamese contributors to the repo

**Open questions:**
1. How many template styles are needed at launch? → **RESOLVED (Phase 4):** 3-5 per format. PPTX: Pro mode (ppt-master, 20+ layouts) + Quick mode (pptxgenjs). HTML: 8 reveal.js styles.
2. Should there be a "quick mode" vs "detailed mode" for the pipeline? → **RESOLVED (Phase 4):** Yes. `content_depth: comprehensive` (default, 5000-15000 words) vs `standard` (when user explicitly asks for brevity).
3. How to handle very large documents that exceed Copilot's context window? → **RESOLVED (Phase 5):** Session state persistence (`save_state.py`), chunking in thu-thap, incremental synthesis in bien-soan.
4. Should the pipeline support chaining outputs? → **RESOLVED (Phase 3):** Yes. `references/output-chaining.md` documents chaining (e.g., Excel → chart → PPT). Routing in tong-hop Step 3.

**New learnings from Phase 7 (Pipeline Enforcement):**
5. **SKILL.md line limits need flexibility**: Original idea specified ≤300 lines. In practice, complex skills (tong-hop, thu-thap) need 400-500 lines when critical instructions must be inline (not in references/) because weaker models skip reference files. Current policy: ≤400 lines target, ≤500 hard limit, verbose details in references/ with `⚠️ MUST_READ` markers.
6. **Model compliance varies dramatically**: Tier 1 models (Claude Opus, GPT-4o) follow multi-step instructions reliably. Tier 2 (GPT-4o-mini) may skip HARD GATEs and quality gates. Phase 7 added visual `╔══ 🛑 HARD GATE ══╗` boxes and numbered step traces to improve compliance.
7. **Reference files are unreliable for enforcement**: Instructions in `references/*.md` are only read when the model is strong enough to follow "READ this file" directives. Critical decision logic must be inline in SKILL.md. References should be reserved for examples, advanced features, and supplementary context.
8. **Pre-output validation beats post-hoc audit**: URL validation gate (Step 4.3b) catches bad URLs BEFORE they enter Excel output, rather than flagging them in kiem-tra audit afterward. This pattern should extend to other quality dimensions.
9. **Smoke testing infrastructure is essential**: Created `scripts/smoke_test.py` to validate all 15 skills, 4 scripts, directories, and dependencies in one command. Benchmark test cases documented in `docs/reports/compatibility-matrix.md`.

**New questions from Phase 9 (Central Orchestrator & Adaptive Self-Improvement):**
10. How should dieu-phoi handle requests that don't fit any known intent category? → **OPEN**: Fallback to advisory agent consultation + user clarification. Needs Phase 9 design.
11. What is the maximum token budget for a single self-improvement cycle? → **OPEN**: Needs benchmarking. Estimated 50K-100K tokens for skill creation + testing.
12. Should audit test cases be reusable across similar requests? → **OPEN**: Potential optimization — cache test case templates for common request patterns.
13. How to handle state file conflicts when user modifies output files between sessions? → **OPEN**: State file tracks output file hashes; if mismatch detected, warn user and offer re-audit.
14. Should the 100-point audit generate different test case sets per output format? → **PROPOSED**: Yes — a Word report audit has different quality dimensions than an Excel data collection audit. Auditor adapts test cases to output type.

### Tiếng Việt

**Rủi ro sản phẩm:**
- Skill pipeline phải điều phối nhiều skill con — logic định tuyến rất quan trọng
- Template phải đẹp chuyên nghiệp; thiết kế kém sẽ giảm độ tin cậy
- Tiếng Việt do AI tạo phải tự nhiên, chính xác

**Rủi ro kỹ thuật:**
- Web search không phải lúc nào cũng cho kết quả tốt
- Trích xuất PDF có thể mất dữ liệu
- Tạo hình ảnh chỉ chạy trên Apple Silicon
- Subagent stateless: phải truyền đầy đủ context qua shared context file; rủi ro mất thông tin giữa các agent
- Token overhead: nhiều agent calls nhân token 2-4x; giảm thiểu bằng tiered audit và budget cap
- Skill clone từ bên ngoài có thể chứa lỗ hổng bảo mật; bắt buộc kiểm tra security trước khi dùng
- Model có thể ảo giác về năng lực; giảm thiểu bằng decision maps đối chiếu benchmark

**Câu hỏi còn bỏ ngỏ:**
1. Cần bao nhiêu template style khi ra mắt? → **ĐÃ GIẢI QUYẾT (Phase 4):** 3-5 mỗi format. PPTX: 20+ layouts (ppt-master) + Quick mode. HTML: 8 styles.
2. Có cần chế độ "nhanh" vs "chi tiết"? → **ĐÃ GIẢI QUYẾT (Phase 4):** comprehensive (mặc định) vs standard.
3. Xử lý tài liệu lớn? → **ĐÃ GIẢI QUYẾT (Phase 5):** save_state.py, chunking, incremental synthesis.
4. Pipeline hỗ trợ chuỗi output? → **ĐÃ GIẢI QUYẾT (Phase 3):** Có, Excel → chart → PPT.

**Bài học từ Phase 7:**
5. SKILL.md cần linh hoạt kích thước — 400-500 dòng cho skill phức tạp, không phải 300.
6. Model yếu skip HARD GATE → cần visual box `╔══ 🛑 ══╗` và numbered step trace.
7. Reference files không đáng tin cho enforcement → logic quyết định phải inline.
8. Validate trước output tốt hơn audit sau → URL validation gate (Step 4.3b).
9. Smoke test (`scripts/smoke_test.py`) là cần thiết cho CI.

**Câu hỏi mới từ Phase 9:**
10. dieu-phoi xử lý intent không xác định? → **MỞ**: Hỏi advisory + clarify user.
11. Token budget tối đa cho 1 vòng self-improvement? → **MỞ**: Ước tính 50K-100K tokens.
12. Test case audit có reusable cho request tương tự? → **MỞ**: Tiềm năng cache template test case.
13. Xử lý conflict state khi user sửa output giữa sessions? → **MỞ**: Track hash file, cảnh báo nếu khác.
14. Audit 100 điểm tạo test case khác nhau theo format output? → **ĐỀ XUẤT**: Có — Word report vs Excel data collection cần quality dimensions khác nhau.

---

## Proposed Skill Architecture (Product-Level)

> **Note:** This is a product-level mapping only — NOT technical design.

```
InsightEngine/
  .github/
    copilot-instructions.md          # Main instructions (Vietnamese-first)
    instructions/                     # Instruction files
    prompts/                          # Prompt files
    agents/                           # 🤖 VS Code custom agents (.agent.md format)
      dieu-phoi.agent.md             # 🔑 Central Orchestrator — user-invocable, tiếp nhận mọi request
      auditor.agent.md               # Quality audit — 100-point scoring, user-invocable for standalone audit
      strategist.agent.md            # Workflow generation — user-invocable: false (subagent only)
      advisory.agent.md              # Multi-perspective decisions — user-invocable: false (subagent only)
    skills/
      tong-hop/                      # Tổng hợp nội dung đa nguồn (refactored: synthesis-only, không còn orchestrate)
      thu-thap/                      # Thu thập từ web + đọc file
      bien-soan/                     # Biên soạn nội dung + dịch thuật
      tao-word/                      # Xuất Word (.docx)
      tao-excel/                     # Xuất Excel (.xlsx)
      tao-slide/                     # Xuất PowerPoint (.pptx)
      tao-pdf/                       # Xuất PDF
      tao-html/                      # Xuất HTML
      tao-hinh/                      # Biểu đồ + hình ảnh
```

**Architecture:** 4 agents (`.github/agents/`) + 9 skills (`.github/skills/`) — peer-level, per VS Code standard

**Agent specification (`.agent.md` YAML frontmatter):**
```yaml
# dieu-phoi.agent.md
---
name: dieu-phoi
description: Central InsightEngine orchestrator — analyzes intent, routes to skills/agents
tools: ['*']                          # Full tool access for orchestration
agents: [auditor, strategist, advisory]
model: Claude Sonnet 4.5 (copilot)   # Preferred; falls back to available
handoffs:
  - label: Kiểm tra chất lượng
    agent: auditor
    prompt: Audit the output against the original requirements.
    send: false
---
```
```yaml
# auditor.agent.md
---
name: auditor
description: Quality audit agent — 100-point weighted scoring, targeted retry guidance
tools: ['read_file', 'grep_search', 'semantic_search', 'fetch_webpage']
agents: []                            # No subagents — auditor is leaf agent
user-invocable: true                  # Can be used standalone for ad-hoc audits
---
```
```yaml
# strategist.agent.md
---
name: strategist
description: Workflow generation — receives request + model profile, returns execution plan
tools: ['read_file', 'semantic_search', 'list_dir']
agents: []
user-invocable: false                 # Only accessible as subagent
---
```
```yaml
# advisory.agent.md
---
name: advisory
description: Multi-perspective decision support — 3-5 viewpoints + recommendation
tools: ['read_file', 'semantic_search', 'fetch_webpage']
agents: []
user-invocable: false                 # Only accessible as subagent
---
```

**Consolidation rationale:**
- `thu-thap-web` + `doc-tai-lieu` → `thu-thap` (same ingestion group)
- `tong-hop-noi-dung` + `dich-thuat` → `bien-soan` (translation is a form of content processing)
- `tao-bieu-do` + `tao-hinh-anh` → `tao-hinh` (same visual generation group)
- `mau-template` → embedded as `references/` in each output skill

**Naming convention:**
- Skill directory names: Vietnamese, lowercase, hyphenated (in `.github/skills/`)
- Skill file: `SKILL.md` (content in English for Copilot)
- Skill triggers: Bilingual (Vietnamese primary, English secondary)
- Agent file names: Vietnamese, lowercase, `.agent.md` extension (in `.github/agents/`)
- Agent YAML frontmatter: English (for Copilot compatibility)
- Agent body: English instructions with Vietnamese trigger phrases
- References: In `references/` subdirectory within each skill

**V1 decisions (Phase 0-3):**
- Templates: 3-5 styles per format (corporate, academic, minimal, dark/modern, creative)
- Chaining outputs: Supported (e.g., Excel data → PPT charts)
- Large documents: Chunking strategy with incremental synthesis

**V2 decisions (Phase 4 — post-testing feedback):**
- PPTX templates: 8-10 professional templates with scripts/ (ref: slidemembers.com, aippt.com, canva.com)
- HTML presentation mode: reveal.js-based with transitions, animations, backgrounds (ref: revealjs.com, slides.com/templates, deckdeckgo.com)
- Script-powered skills: Each output skill gets scripts/ with CLI tools (ref pattern: a-z-copilot-flow/skills/gen-image, skills/pptx)
- Content depth: bien-soan produces richer, more detailed synthesis
- Multi-level scripts: Different script versions for different complexity levels

**V3 decisions (Phase 6 — agent architecture & quality gates):**
- Agent architecture: 3 specialized agents (strategist, audit, advisory) orchestrate pipeline
- Shared context file: `tmp/.agent-context.json` for inter-agent communication
- Model self-awareness: self-declaration + decision maps per capability category (NO hardcoded model name)
- Tiered audit: self-review → agent audit (critical steps) → final audit (output vs requirements)
- Strict file rules: `/scripts`, `/tmp`, `/output` enforced across all skills
- Auto-escalation: tools auto-upgrade on failure, never ask user technical questions
- Conditional skill creation: advisory decides, 30-min budget, clone-first from verified public repos
- Budget cap: max 30 agent calls/pipeline, max 3 retries/step, max 10 total retries
- Feature flag: `AGENT_MODE` in tong-hop for backward compatibility

**V4 decisions (Phase 9 — central orchestrator, adaptive self-improvement, weighted audit):**

*VS Code Custom Agent Standard Compliance:*
- ALL agents follow `.agent.md` format in `.github/agents/` (ref: code.visualstudio.com/docs/copilot/customization/custom-agents)
- Agents and skills are **peer-level** — agents in `.github/agents/`, skills in `.github/skills/`
- Agent YAML frontmatter: description, name, tools, model, agents, handoffs, user-invocable
- `handoffs` for guided sequential workflows between agents
- `user-invocable` controls agent picker visibility (false = subagent-only)
- Agent `tools` enforces least-privilege per role (auditor = read-only, orchestrator = full)
- Native integration with VS Code agent picker, subagent system, and model selection
- AGENT_MODE feature flag removed — agents are always available as first-class VS Code custom agents

*Central Orchestrator:*
- `dieu-phoi.agent.md` — primary user-facing agent, appears in VS Code agent picker
- tong-hop refactored to pure content synthesis skill (`.github/skills/tong-hop/SKILL.md`) — doing what its name says
- Intent taxonomy: synthesis / creation / research / design / data_collection / mixed / unknown
- Orchestrator uses `agents: [auditor, strategist, advisory]` field for native subagent access
- `handoffs` enable guided transitions: dieu-phoi → auditor → dieu-phoi (retry loop)
- Created agents during self-improvement also placed in `.github/agents/` following the same standard

*Adaptive Self-Improvement:*
- System performs gap assessment: current capabilities vs request requirements
- Can create new agents (literary author, art director, etc.) and new skills (manga layout, etc.) at runtime
- User consent REQUIRED before any creation/upgrade. Transparent about what and why
- Time notification at 30 minutes. User can "unlock" extended self-improvement (no hard time cap)
- Created skills/agents tested before use. Fall back to best-effort if creation fails
- Self-improvement is constrained to Copilot's existing tool set — better instructions, not new runtime capabilities

*100-Point Weighted Audit (QA Model):*
- Auditor dynamically generates test case set per request — like QA creating test cases from a feature spec
- Each test case gets a weight (points) based on importance. Total = 100
- Weight distribution principle: core requirements 50-60%, quality dimensions 20-30%, polish 10-20%
- Pass threshold: >80/100. Max 5 retries (up from 3)
- Targeted retry: identifies which step/test case scored low, re-executes only that step
- Score progression tracked in working state. No-improvement detection: if score doesn't improve between consecutive retries, stop
- Test case sets adapt to output format (Word report ≠ Excel data ≠ PowerPoint deck)
- Example test case set for "market analysis report":
  ```
  TC-1: Core topic coverage                 25 pts
  TC-2: Data specificity (numbers, dates)    15 pts
  TC-3: Source quality and citations         10 pts
  TC-4: Competitive analysis depth           15 pts
  TC-5: Consumer/trend insights              10 pts
  TC-6: Formatting (TOC, headings, charts)    8 pts
  TC-7: Language quality (natural VN)          5 pts
  TC-8: Actionable recommendations            7 pts
  TC-9: Visual aids (charts, tables)           5 pts
  TOTAL                                     100 pts
  ```

*Enhanced Working State:*
- State file stores: raw_prompt, analyzed_requirements, generated_plan, step_states[], audit_test_cases[], score_history[], created_skills[]
- Cross-session resume: new session reads state file → reconstructs full context → continues from checkpoint
- State file is human-readable and self-documenting
- Output file hash tracking for conflict detection between sessions

---

*This document was produced by Idea Analysis. Updated with Phase 4 scope based on testing feedback.*
*Updated with Phase 6 scope based on real-world usage feedback (agent architecture, quality gates, strict rules).*
*Updated with Phase 7 learnings (2026-04-18): open questions resolved, enforcement hardening insights, compatibility matrix.*
*Updated with Phase 9 scope (2026-04-18): central orchestrator, adaptive self-improvement, 100-point weighted audit, cross-session resume, VS Code custom agent standard alignment.*
