# InsightEngine — Product Roadmap

> **Product:** InsightEngine  
> **Product Slug:** insight-engine  
> **Roadmap Created:** 2026-04-16  
> **Scope:** Milestone-based (Phase 0 → Phase 6)

---

## Product Roadmap Overview

- **Product name:** InsightEngine
- **Product slug:** `insight-engine`
- **Roadmap scope:** Milestone-based — each phase delivers a usable capability increment
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

## Skill Map theo Phase

```
Phase 0:  cai-dat (MỚI)     tong-hop (skeleton)
Phase 1:  thu-thap          bien-soan          tao-word     tao-slide
Phase 2:  thu-thap (nâng)   tao-excel          tao-pdf      tao-html   tong-hop (chaining)
Phase 3:  tao-hinh (MỚI)    bien-soan (nâng)   tao-slide (nâng)  tong-hop (nâng)
Phase 4:  tao-slide (templates)  tao-html (reveal.js)  bien-soan (depth)  all skills (scripts/)
Phase 5:  all skills (small model refactor)  tong-hop (session state + resume)
Phase 6:  agents (MỚI: strategist, audit, advisory)  tong-hop (dynamic workflow)  all skills (strict rules)
```

**Tổng số skills:** 10 + 3 agents (strategist, audit, advisory)

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

*Roadmap này không bao gồm task-level breakdown. Xem User Stories để biết chi tiết triển khai.*  
*Bước tiếp theo: `/product-roadmap-review` hoặc `/roadmap-to-user-stories`*
