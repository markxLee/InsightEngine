# InsightEngine — Idea Analysis

> **Idea Slug:** insight-engine  
> **Analysis Date:** 2026-04-16  
> **Status:** REVIEWED — READY

---

## 1. Problem Statement

### English

Individual professionals (researchers, analysts, students, consultants) routinely face the same painful workflow: gathering information from scattered sources (web pages, PDFs, Excel files, Word documents, presentations), manually synthesizing that information, and then reformatting it into a deliverable — a report, a slide deck, a spreadsheet, or a web page.

This process is:
- **Time-consuming**: Hours spent copy-pasting, reformatting, and restructuring
- **Error-prone**: Manual transfer loses context, introduces inconsistencies
- **Repetitive**: The same gather → synthesize → output pattern repeats daily
- **Tool-fragmented**: Users juggle 5-10 different tools with no unified flow

Current AI assistants can help with parts of this (e.g., summarize one document), but none provide an **end-to-end pipeline** that handles multi-source ingestion, intelligent synthesis, and multi-format output — all within a single conversational interface.

**Why it matters:** Knowledge workers spend up to 30% of their time on information gathering and reformatting rather than analysis and decision-making.

### Tiếng Việt

Các cá nhân (nhà nghiên cứu, chuyên viên phân tích, sinh viên, tư vấn viên) thường xuyên phải đối mặt với quy trình lặp đi lặp lại: thu thập thông tin từ nhiều nguồn rời rạc (trang web, PDF, Excel, Word, PowerPoint), tổng hợp thủ công, rồi chuyển đổi thành sản phẩm hoàn chỉnh — báo cáo, slide thuyết trình, bảng tính, hoặc trang web.

Quy trình này tốn thời gian, dễ sai sót, lặp lại liên tục, và đòi hỏi sử dụng nhiều công cụ khác nhau mà không có một luồng xử lý thống nhất.

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
- All skill names and directories in Vietnamese
- Skill triggers bilingual (Vietnamese + English)
- Skill internal content in English (for Copilot performance)
- SKILL.md acts as router — references sub-docs and scripts/ for details
- Each skill has `scripts/` directory with executable CLI tools (Python/Node.js)
- Multi-level scripts for different needs (e.g., gen_image.py vs gen_portrait_v5.py)
- `references/` directory for prompt guides, API docs, template specs
- Pattern follows: a-z-copilot-flow/skills/gen-image, skills/pptx
- Pipeline skill has knowledge of all sub-skills
- SKILL.md files optimized for small model compatibility (≤ 300 lines, step-by-step instructions)
- Session state persistence: pipeline writes `.session-state.json` after each step for resume capability

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

---

## 5. Out-of-Scope / Non-Goals

### English

- **NOT a web application** — no server, no database, no deployment
- **NOT a code development tool** — no governed workflow, no CI/CD, no testing pipeline
- **NOT a real-time collaboration tool** — single-user, local execution
- **NOT an autonomous agent** — user initiates and guides each request
- **NO dependency on a-z-copilot-flow at runtime** — repo must be fully self-contained
- **NO custom LLM/AI model** — relies entirely on GitHub Copilot (Claude) as the reasoning engine
- **NO paid API integrations** — Google search via built-in Copilot tool, no SerpAPI/custom search
- **NO interactive web dashboards** — output is static files, not running applications
- **NO video/audio processing** — text and image-based content only

### Tiếng Việt

- **KHÔNG** là ứng dụng web — không server, database, deployment
- **KHÔNG** là công cụ phát triển code — không có governed workflow, CI/CD
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

### Tiếng Việt

1. User có VS Code + GitHub Copilot
2. Python 3.x và Node.js đã cài đặt
3. Apple Silicon cho tạo hình ảnh (tùy chọn)
4. User quen dùng VS Code cơ bản
5. Có kết nối internet (cho search và fetch web)
6. Tiếng Việt là ngôn ngữ chính

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

**Adoption risks:**
- **Learning curve**: Users must understand the skill/prompt mental model
- **Expectation management**: AI output quality varies; users may expect perfection
- **Vietnamese-only naming**: May confuse non-Vietnamese contributors to the repo

**Open questions:**
1. How many template styles are needed at launch? (Suggest: 3-5 per format)
2. Should there be a "quick mode" vs "detailed mode" for the pipeline?
3. How to handle very large documents that exceed Copilot's context window?
4. Should the pipeline support chaining outputs (e.g., generate Excel → use data for PPT)?

### Tiếng Việt

**Rủi ro sản phẩm:**
- Skill pipeline phải điều phối nhiều skill con — logic định tuyến rất quan trọng
- Template phải đẹp chuyên nghiệp; thiết kế kém sẽ giảm độ tin cậy
- Tiếng Việt do AI tạo phải tự nhiên, chính xác

**Rủi ro kỹ thuật:**
- Web search không phải lúc nào cũng cho kết quả tốt
- Trích xuất PDF có thể mất dữ liệu
- Tạo hình ảnh chỉ chạy trên Apple Silicon

**Câu hỏi còn bỏ ngỏ:**
1. Cần bao nhiêu template style khi ra mắt?
2. Có cần chế độ "nhanh" vs "chi tiết" cho pipeline?
3. Xử lý tài liệu lớn vượt quá context window như thế nào?
4. Pipeline có hỗ trợ chuỗi output không (Excel → dùng data cho PPT)?

---

## Proposed Skill Architecture (Product-Level)

> **Note:** This is a product-level mapping only — NOT technical design.

```
InsightEngine/
  .github/
    copilot-instructions.md          # Main instructions (Vietnamese-first)
    instructions/                     # Instruction files
    prompts/                          # Prompt files
    skills/
      tong-hop/                      # 🔑 Pipeline chính — orchestrator
      thu-thap/                      # Thu thập từ web + đọc file
      bien-soan/                     # Tổng hợp nội dung + dịch thuật
      tao-word/                      # Xuất Word (.docx)
      tao-excel/                     # Xuất Excel (.xlsx)
      tao-slide/                     # Xuất PowerPoint (.pptx)
      tao-pdf/                       # Xuất PDF
      tao-html/                      # Xuất HTML
      tao-hinh/                      # Biểu đồ + hình ảnh
```

**Skill count:** 9 skills (1 pipeline + 8 sub-skills)

**Consolidation rationale:**
- `thu-thap-web` + `doc-tai-lieu` → `thu-thap` (same ingestion group)
- `tong-hop-noi-dung` + `dich-thuat` → `bien-soan` (translation is a form of content processing)
- `tao-bieu-do` + `tao-hinh-anh` → `tao-hinh` (same visual generation group)
- `mau-template` → embedded as `references/` in each output skill

**Naming convention:**
- Directory names: Vietnamese, lowercase, hyphenated
- Skill file: `SKILL.md` (content in English for Copilot)
- Triggers: Bilingual (Vietnamese primary, English secondary)
- Agents/references: Split into `agents/` and `references/` subdirectories when needed

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

---

*This document was produced by Idea Analysis. Updated with Phase 4 scope based on testing feedback.*
*Next step: Review this analysis before proceeding to tech stack and roadmap planning.*
