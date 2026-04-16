# InsightEngine — User Stories Backlog

> **Product:** InsightEngine  
> **Product Slug:** insight-engine  
> **Created:** 2026-04-16  
> **Scope:** Phase 0 → Phase 3 (all phases)  
> **Total User Stories:** 21

---

## User Stories Overview

- **Product name:** InsightEngine
- **Product slug:** `insight-engine`
- **Scope covered:** Phase 0, Phase 1, Phase 2, Phase 3
- **Total stories:** 21 (Phase 0: 5, Phase 1: 6, Phase 2: 5, Phase 3: 5)
- **ID format:** `US-<phase>.<epic>.<index>`

### Dependency Graph (Summary)

```
US-0.1.1 ──────────────────────────────────────────────────────────┐
US-0.2.1 → US-0.2.2                                               │
US-0.1.1 + US-0.2.2 → US-0.3.1 → US-0.3.2                        │
                                                                   │
US-0.3.2 → US-1.1.1 → US-1.1.2                                   │
US-0.3.2 → US-1.2.1 → US-1.2.2                                   │
US-1.2.1 + US-1.1.1 → US-1.3.1                                   │
US-1.2.1 + US-1.1.1 → US-1.4.1                                   │
                                                                   │
US-1.1.1 → US-2.1.1                                               │
US-1.2.1 → US-2.2.1                                               │
US-1.2.1 → US-2.3.1                                               │
US-1.2.1 → US-2.4.1                                               │
US-1.3.1 + US-1.4.1 + US-2.2.1 → US-2.5.1                        │
                                                                   │
US-2.2.1 → US-3.1.1                                               │
US-3.1.1 → US-3.1.2                                               │
US-1.2.1 → US-3.2.1                                               │
US-1.3.1 + US-1.4.1 + US-2.4.1 → US-3.3.1                        │
US-0.3.1 + US-2.5.1 → US-3.4.1                                   │
```

---

## Phase 0: Product Foundation

### Epic 0.1: Workspace Setup

**US-0.1.1: Repo structure & Copilot configuration**
- Description: As a user opening InsightEngine in VS Code, I want the repo to have a complete `.github/` structure (copilot-instructions.md, instructions/, skills/ directories, scripts/) so that Copilot recognizes the workspace and all skills are discoverable.
- Acceptance Criteria:
  - AC1: `.github/copilot-instructions.md` exists with product context, skill registry, and Vietnamese language rules
  - AC2: `.github/instructions/insight-engine.instructions.md` exists with tech stack quick reference
  - AC3: `.github/skills/` directory has a subdirectory for each of the 10 skills (`cai-dat`, `tong-hop`, `thu-thap`, `bien-soan`, `tao-word`, `tao-excel`, `tao-slide`, `tao-pdf`, `tao-html`, `tao-hinh`)
  - AC4: `scripts/` directory exists with placeholder README
  - AC5: Copilot in VS Code recognizes the workspace and loads instructions on session start
- Blocked By: `None`

---

### Epic 0.2: Cài đặt môi trường (`cai-dat`)

**US-0.2.1: Dependency check script**
- Description: As a user running InsightEngine for the first time, I want a script that checks all required dependencies (Python, Node.js, pip packages, npm packages) and clearly reports what is missing, so I know what to install.
- Acceptance Criteria:
  - AC1: `scripts/check_deps.py` exists and runs with `python3 scripts/check_deps.py`
  - AC2: Checks Python ≥ 3.10, Node.js ≥ 18
  - AC3: Checks each required pip package: `markitdown`, `python-docx`, `openpyxl`, `pandas`, `reportlab`, `pypdf`, `pdfplumber`, `matplotlib`, `seaborn`, `jinja2`, `httpx`, `beautifulsoup4`
  - AC4: Checks `pptxgenjs` availability via Node.js
  - AC5: Prints ✅/❌ per dependency and summary line "X/Y dependencies ready"
  - AC6: Exit code 0 if all core deps present, exit code 1 if any missing
- Blocked By: `None`

**US-0.2.2: Setup skill (`cai-dat`)**
- Description: As a user who has missing dependencies, I want to say "cài đặt" or "/cai-dat" and have Copilot guide me through installing everything needed, so I can start using InsightEngine without manual research.
- Acceptance Criteria:
  - AC1: Skill file `.github/skills/cai-dat/SKILL.md` exists (≤ 400 lines, English content)
  - AC2: Triggers on: "cài đặt", "setup", "install dependencies", "/cai-dat"
  - AC3: Runs `check_deps.py` first, then installs only missing packages
  - AC4: Installs Python packages via `pip install --user`
  - AC5: Installs Node packages via `npm install -g pptxgenjs`
  - AC6: Creates `scripts/recalc.py` if not present
  - AC7: Runs verification after install and reports final status in Vietnamese
- Blocked By: `US-0.2.1`

---

### Epic 0.3: Pipeline Chính (`tong-hop`)

**US-0.3.1: Pipeline skill skeleton with intent routing**
- Description: As a user, I want to describe my content needs in Vietnamese (e.g., "tổng hợp báo cáo từ 3 file này") and have the pipeline skill understand my intent and plan which sub-skills to invoke, so I don't need to call each skill manually.
- Acceptance Criteria:
  - AC1: Skill file `.github/skills/tong-hop/SKILL.md` exists (≤ 400 lines)
  - AC2: Triggers on: "tổng hợp nội dung", "làm báo cáo", "làm thuyết trình", "/tong-hop"
  - AC3: Skill analyzes user request to determine: input sources, processing needed, output format
  - AC4: Skill presents execution plan to user before proceeding (e.g., "Thu thập → Biên soạn → Xuất Word")
  - AC5: Skill routes to appropriate sub-skills in correct order
  - AC6: Copilot responds entirely in Vietnamese
- Blocked By: `US-0.1.1`, `US-0.2.2`

**US-0.3.2: Setup check before each pipeline process**
- Description: As a user, I want the pipeline to automatically verify my environment is ready before processing any request, so I never get a cryptic error from a missing dependency mid-pipeline.
- Acceptance Criteria:
  - AC1: `tong-hop` skill runs `check_deps.py` in silent mode before every process
  - AC2: If dependencies are missing, Copilot stops and suggests running `/cai-dat` (in Vietnamese)
  - AC3: If all dependencies are present, pipeline continues without interruption
  - AC4: Check adds < 2 seconds overhead to pipeline start
- Blocked By: `US-0.3.1`

---

## Phase 1: MVP — Thu thập & Xuất cơ bản

### Epic 1.1: Thu thập nội dung (`thu-thap`)

**US-1.1.1: Read local files via markitdown**
- Description: As a user, I want to point the pipeline at local files (docx, xlsx, pdf, pptx, txt, md) and have their content extracted as structured text, so I can use them as input for synthesis.
- Acceptance Criteria:
  - AC1: Skill file `.github/skills/thu-thap/SKILL.md` exists (≤ 400 lines)
  - AC2: Triggers on: "đọc file", "lấy nội dung từ", "read file", "/thu-thap"
  - AC3: Uses `markitdown` as primary reader for all supported formats
  - AC4: Falls back to format-specific library if markitdown output is empty or < 100 chars (python-docx for .docx, openpyxl for .xlsx, pdfplumber for .pdf, python-pptx for .pptx)
  - AC5: Returns extracted content as Markdown text to the pipeline
  - AC6: Reports file name and extracted content length to user
- Blocked By: `US-0.3.2`

**US-1.1.2: Fetch URL content**
- Description: As a user, I want to provide one or more URLs and have the pipeline fetch and extract their main content, so I can use web sources alongside local files.
- Acceptance Criteria:
  - AC1: `thu-thap` skill accepts URLs as input alongside files
  - AC2: Uses Copilot `fetch_webpage` tool as primary method
  - AC3: Extracts main content (strips navigation, ads, boilerplate)
  - AC4: Reports URL title and content length for each fetched page
  - AC5: Handles errors gracefully (404, timeout) with Vietnamese error message
- Blocked By: `US-1.1.1`

---

### Epic 1.2: Biên soạn nội dung (`bien-soan`)

**US-1.2.1: Multi-source content synthesis**
- Description: As a user, I want the pipeline to merge and restructure content from multiple sources into a coherent, well-organized document, so I don't have to manually combine and edit information.
- Acceptance Criteria:
  - AC1: Skill file `.github/skills/bien-soan/SKILL.md` exists (≤ 400 lines)
  - AC2: Triggers on: "tổng hợp", "gộp nội dung", "biên soạn", "synthesize", "/bien-soan"
  - AC3: Identifies overlapping content across sources and resolves conflicts
  - AC4: Proposes an outline to user before generating full content
  - AC5: Produces structured content with headings, sections, and key points
  - AC6: Preserves source attribution when appropriate
- Blocked By: `US-0.3.2`

**US-1.2.2: Basic translation Vietnamese ↔ English**
- Description: As a user, I want to request translation of synthesized content between Vietnamese and English, so I can produce bilingual documents or translate source material.
- Acceptance Criteria:
  - AC1: `bien-soan` skill supports translation as a processing mode
  - AC2: Translates section by section, preserving document structure
  - AC3: User can specify target language: "dịch sang tiếng Anh" or "translate to Vietnamese"
  - AC4: Translation maintains formatting (headings, bullets, tables)
  - AC5: Triggers on: "dịch thuật", "translate", "dịch sang"
- Blocked By: `US-1.2.1`

---

### Epic 1.3: Xuất Word (`tao-word`)

**US-1.3.1: Word document output with 3 template styles**
- Description: As a user, I want to export synthesized content as a professionally formatted Word document, choosing from corporate, academic, or minimal styles, so I can deliver polished documents without design effort.
- Acceptance Criteria:
  - AC1: Skill file `.github/skills/tao-word/SKILL.md` exists (≤ 400 lines)
  - AC2: Triggers on: "tạo file word", "xuất word", "create word document", "/tao-word"
  - AC3: Generates `.docx` using `python-docx` with proper page setup (A4)
  - AC4: Supports 3 styles: corporate (blue/formal), academic (serif/footnotes), minimal (clean/light)
  - AC5: Includes: headings, paragraphs, tables, bullet lists, images (if provided)
  - AC6: Uses `WidthType.DXA` for table widths (never PERCENTAGE)
  - AC7: Prints output file path and size upon completion
  - AC8: References template specs stored in `references/` subdirectory
- Blocked By: `US-1.2.1`, `US-1.1.1`

---

### Epic 1.4: Xuất PowerPoint (`tao-slide`)

**US-1.4.1: PowerPoint output with 3 template styles**
- Description: As a user, I want to export synthesized content as a professional PowerPoint presentation, choosing from corporate, academic, or minimal styles, so I can present information without manual slide design.
- Acceptance Criteria:
  - AC1: Skill file `.github/skills/tao-slide/SKILL.md` exists (≤ 400 lines)
  - AC2: Triggers on: "tạo slide", "làm thuyết trình", "create powerpoint", "/tao-slide"
  - AC3: Generates `.pptx` using `pptxgenjs` via Node.js script
  - AC4: 3 styles: corporate (bold colors, shapes), academic (clean serif), minimal (whitespace)
  - AC5: Every slide has a visual element (no text-only slides)
  - AC6: Supports: title slide, section dividers, content slides with bullets, image placeholders
  - AC7: No `#` prefix in hex colors (pptxgenjs requirement)
  - AC8: Font pairings documented per style in `references/`
  - AC9: Prints output file path and size upon completion
- Blocked By: `US-1.2.1`, `US-1.1.1`

---

## Phase 2: Mở rộng — Tìm kiếm & Thêm định dạng

### Epic 2.1: Tìm kiếm Google tự động

**US-2.1.1: Web search integration in thu-thap**
- Description: As a user, I want the pipeline to automatically search Google when I don't provide specific sources, so it can gather relevant context on its own.
- Acceptance Criteria:
  - AC1: `thu-thap` skill uses `vscode-websearchforcopilot_webSearch` to search when no files/URLs are provided
  - AC2: Searches based on user's topic description
  - AC3: Fetches content from top 3-5 relevant URLs
  - AC4: Presents found sources to user for approval before proceeding
  - AC5: Works alongside manual file/URL input (hybrid mode)
- Blocked By: `US-1.1.1`

---

### Epic 2.2: Xuất Excel (`tao-excel`)

**US-2.2.1: Excel output with formulas and formatting**
- Description: As a user, I want to export structured data as a professionally formatted Excel file with working formulas, so I can use the data for further analysis.
- Acceptance Criteria:
  - AC1: Skill file `.github/skills/tao-excel/SKILL.md` exists (≤ 400 lines)
  - AC2: Triggers on: "tạo file excel", "xuất excel", "create excel", "/tao-excel"
  - AC3: Uses `openpyxl` for formatting/formulas and `pandas` for data operations
  - AC4: All calculated values use Excel formulas (never hardcoded)
  - AC5: Runs `scripts/recalc.py` after generation to force recalculation
  - AC6: Verifies no formula errors (#REF!, #DIV/0!, etc.) after recalc
  - AC7: Color coding: blue = inputs, black = formulas, green = cross-sheet links
  - AC8: Prints output file path and size upon completion
- Blocked By: `US-1.2.1`

---

### Epic 2.3: Xuất PDF (`tao-pdf`)

**US-2.3.1: PDF output from synthesized content**
- Description: As a user, I want to export synthesized content as a PDF document with proper formatting, headers, and table of contents, so I can share professional read-only documents.
- Acceptance Criteria:
  - AC1: Skill file `.github/skills/tao-pdf/SKILL.md` exists (≤ 400 lines)
  - AC2: Triggers on: "tạo file pdf", "xuất pdf", "create pdf", "/tao-pdf"
  - AC3: Uses `reportlab` Platypus for complex layouts, Canvas for simple ones
  - AC4: Supports: headings, paragraphs, tables, images, page numbers
  - AC5: Uses `<sub>` and `<super>` XML tags for subscript/superscript (never Unicode)
  - AC6: Embeds fonts for Vietnamese character support
  - AC7: Prints output file path and size upon completion
- Blocked By: `US-1.2.1`

---

### Epic 2.4: Xuất HTML (`tao-html`)

**US-2.4.1: Static HTML page output with 3 template styles**
- Description: As a user, I want to export content as a portable static HTML page with professional styling, so I can share reports that open in any browser without dependencies.
- Acceptance Criteria:
  - AC1: Skill file `.github/skills/tao-html/SKILL.md` exists (≤ 400 lines)
  - AC2: Triggers on: "tạo trang web", "tạo html", "create html page", "/tao-html"
  - AC3: Uses `jinja2` templates with inline CSS (no external dependencies)
  - AC4: 3 styles: corporate, academic, minimal — stored in `references/templates/`
  - AC5: Charts embedded as base64 PNG `<img>` tags for portability
  - AC6: Single-file output (all CSS inline)
  - AC7: Prints output file path and size upon completion
- Blocked By: `US-1.2.1`

---

### Epic 2.5: Chaining Output

**US-2.5.1: Pipeline output chaining**
- Description: As a user, I want the pipeline to chain outputs (e.g., generate Excel data → create charts → embed in PPT), showing me the chain plan before executing, so I can produce complex deliverables in one request.
- Acceptance Criteria:
  - AC1: `tong-hop` skill detects when user request requires multiple output formats
  - AC2: Presents chain plan to user (e.g., "1. Tạo Excel → 2. Vẽ biểu đồ → 3. Đưa vào PPT")
  - AC3: Executes chain sequentially, passing output of one step as input to next
  - AC4: Intermediate files stored in `tmp/` and cleaned up after completion
  - AC5: Reports all generated files with paths and sizes at the end
- Blocked By: `US-1.3.1`, `US-1.4.1`, `US-2.2.1`

---

## Phase 3: Hoàn thiện — Trực quan & Tối ưu

### Epic 3.1: Biểu đồ & Hình ảnh (`tao-hinh`)

**US-3.1.1: Chart generation from data**
- Description: As a user, I want to generate professional charts (bar, line, pie, radar, scatter) from data, so I can visualize information for reports and presentations.
- Acceptance Criteria:
  - AC1: Skill file `.github/skills/tao-hinh/SKILL.md` exists (≤ 400 lines)
  - AC2: Triggers on: "tạo biểu đồ", "vẽ chart", "create chart", "/tao-hinh"
  - AC3: Uses `matplotlib` with `Agg` backend (always `matplotlib.use('Agg')` first)
  - AC4: Supports: bar, line, pie, radar, scatter chart types
  - AC5: Consistent color palette across charts in a document
  - AC6: Output PNG at `dpi=160`, `bbox_inches='tight'`
  - AC7: Can embed charts into Word/PPT when chained
  - AC8: Vietnamese labels with proper font handling
- Blocked By: `US-2.2.1`

**US-3.1.2: Image generation for slides (Apple Silicon)**
- Description: As a user on Apple Silicon, I want to generate illustration images for my slides from text prompts, so my presentations have custom visuals without stock photos.
- Acceptance Criteria:
  - AC1: `tao-hinh` skill supports image generation mode (text-to-image)
  - AC2: Uses `diffusers` + `torch` with MPS backend
  - AC3: Style presets: flat-icon, dark-tech, cartoon, minimal, watercolor, realistic
  - AC4: SD-Turbo settings: `guidance_scale=0.0`, `num_inference_steps=4`
  - AC5: Output at minimum 512×512 px; 768×768 for presentation images
  - AC6: Gracefully skips with message if not on Apple Silicon
  - AC7: Never attempts to render text inside generated images
- Blocked By: `US-3.1.1`
- Notes: Optional capability — Apple Silicon only. Non-Apple users still get chart generation.

---

### Epic 3.2: Xử lý tài liệu lớn

**US-3.2.1: Large document chunking strategy**
- Description: As a user working with large source documents (> 50,000 words combined), I want the pipeline to handle them reliably using chunking, so I'm not limited by Copilot's context window.
- Acceptance Criteria:
  - AC1: `bien-soan` skill detects when combined input exceeds chunking threshold
  - AC2: Splits content by sections/pages and processes incrementally
  - AC3: Synthesizes chunk summaries into final coherent output
  - AC4: Reports progress to user during processing (e.g., "Đang xử lý phần 3/7...")
  - AC5: Final output quality is comparable to non-chunked processing
- Blocked By: `US-1.2.1`

---

### Epic 3.3: Template Library mở rộng

**US-3.3.1: Additional template styles (dark/modern, creative)**
- Description: As a user, I want additional style options beyond the base 3, so I can create more varied and visually distinctive outputs.
- Acceptance Criteria:
  - AC1: 2 new styles available: `dark/modern` and `creative`
  - AC2: Applied to `tao-slide` and `tao-html` skills (at minimum)
  - AC3: Each new style has color scheme, font pairing, and layout spec in `references/`
  - AC4: User can preview/select style by name before generation
  - AC5: Existing 3 styles (corporate, academic, minimal) remain unchanged
- Blocked By: `US-1.3.1`, `US-1.4.1`, `US-2.4.1`

---

### Epic 3.4: Cải thiện UX Pipeline

**US-3.4.1: Pipeline UX improvements**
- Description: As a user, I want the pipeline to show clear progress, ask for confirmation before time-consuming steps, and suggest appropriate styles based on context, so the experience feels guided and efficient.
- Acceptance Criteria:
  - AC1: Pipeline shows step-by-step progress (e.g., "✅ Thu thập hoàn tất → Đang biên soạn...")
  - AC2: Asks confirmation before steps > 30 seconds (image generation, large file processing)
  - AC3: Suggests style based on context (formal request → corporate, research → academic)
  - AC4: Provides estimated completion time for multi-step chains
  - AC5: Vietnamese throughout all progress messages
- Blocked By: `US-0.3.1`, `US-2.5.1`

---

---

## Tổng quan User Stories (Tiếng Việt)

- **Tên sản phẩm:** InsightEngine
- **Product slug:** `insight-engine`
- **Phạm vi:** Phase 0 → Phase 3
- **Tổng số User Stories:** 21

---

## Phase 0: Nền tảng sản phẩm

### Epic 0.1: Workspace Setup

**US-0.1.1: Cấu trúc repo & cấu hình Copilot**
- Mô tả: Khi mở InsightEngine trong VS Code, repo có đầy đủ cấu trúc `.github/` để Copilot nhận diện workspace và tất cả skill.
- Tiêu chí nghiệm thu:
  - AC1: `copilot-instructions.md` tồn tại với product context và skill registry
  - AC2: `instructions/insight-engine.instructions.md` tồn tại
  - AC3: Thư mục `.github/skills/` có đầy đủ 10 subdirectory cho 10 skills
  - AC4: Thư mục `scripts/` tồn tại
  - AC5: Copilot nhận diện workspace khi mở VS Code
- Bị chặn bởi: `None`

---

### Epic 0.2: Cài đặt môi trường (`cai-dat`)

**US-0.2.1: Script kiểm tra dependencies**
- Mô tả: Script kiểm tra tất cả dependencies cần thiết và báo cáo rõ ràng thiếu gì.
- Tiêu chí nghiệm thu:
  - AC1: `scripts/check_deps.py` tồn tại
  - AC2: Kiểm tra Python ≥ 3.10, Node.js ≥ 18
  - AC3: Kiểm tra tất cả pip/npm packages cần thiết
  - AC4: In ✅/❌ từng dependency + summary
  - AC5: Exit code 0 nếu đủ, 1 nếu thiếu
- Bị chặn bởi: `None`

**US-0.2.2: Skill cài đặt (`cai-dat`)**
- Mô tả: User nói "cài đặt" hoặc "/cai-dat" → Copilot hướng dẫn cài mọi thứ cần thiết.
- Tiêu chí nghiệm thu:
  - AC1: SKILL.md tồn tại (≤ 400 dòng)
  - AC2: Trigger song ngữ Việt/Anh
  - AC3: Cài chỉ những package thiếu
  - AC4: Verify và báo kết quả bằng tiếng Việt
- Bị chặn bởi: `US-0.2.1`

---

### Epic 0.3: Pipeline Chính (`tong-hop`)

**US-0.3.1: Pipeline skeleton với intent routing**
- Mô tả: User mô tả yêu cầu bằng tiếng Việt → pipeline hiểu intent và lên kế hoạch gọi skill con.
- Tiêu chí nghiệm thu:
  - AC1: SKILL.md tồn tại (≤ 400 dòng)
  - AC2: Phân tích: nguồn đầu vào, loại xử lý, format đầu ra
  - AC3: Trình bày kế hoạch cho user trước khi thực hiện
  - AC4: Route đúng skill con theo thứ tự
- Bị chặn bởi: `US-0.1.1`, `US-0.2.2`

**US-0.3.2: Kiểm tra setup trước mỗi process**
- Mô tả: Pipeline tự check môi trường trước mỗi yêu cầu — không bao giờ để lỗi thiếu dep xảy ra giữa chừng.
- Tiêu chí nghiệm thu:
  - AC1: Chạy `check_deps.py` silent mode trước mỗi process
  - AC2: Nếu thiếu dep → dừng và gợi ý `/cai-dat`
  - AC3: Nếu đủ → tiếp tục không gián đoạn
- Bị chặn bởi: `US-0.3.1`

---

## Phase 1: MVP — Thu thập & Xuất cơ bản

### Epic 1.1: Thu thập nội dung (`thu-thap`)

**US-1.1.1: Đọc file local qua markitdown**
- Mô tả: Trỏ đến file local → nội dung được trích xuất dạng text có cấu trúc.
- Tiêu chí nghiệm thu:
  - AC1: SKILL.md tồn tại (≤ 400 dòng)
  - AC2: Dùng markitdown → fallback thư viện chuyên biệt nếu rỗng
  - AC3: Hỗ trợ: docx, xlsx, pdf, pptx, txt, md
  - AC4: Báo tên file và độ dài nội dung
- Bị chặn bởi: `US-0.3.2`

**US-1.1.2: Fetch nội dung URL**
- Mô tả: User cung cấp URL → pipeline fetch và trích xuất nội dung chính.
- Tiêu chí nghiệm thu:
  - AC1: Dùng Copilot `fetch_webpage` tool
  - AC2: Trích xuất nội dung chính (bỏ nav, ads)
  - AC3: Xử lý lỗi (404, timeout) với thông báo tiếng Việt
- Bị chặn bởi: `US-1.1.1`

---

### Epic 1.2: Biên soạn nội dung (`bien-soan`)

**US-1.2.1: Tổng hợp nội dung đa nguồn**
- Mô tả: Pipeline gộp và tái cấu trúc nội dung từ nhiều nguồn thành tài liệu mạch lạc.
- Tiêu chí nghiệm thu:
  - AC1: SKILL.md tồn tại (≤ 400 dòng)
  - AC2: Xác định nội dung trùng lặp giữa các nguồn
  - AC3: Đề xuất outline trước khi viết
  - AC4: Output có headings, sections, key points
- Bị chặn bởi: `US-0.3.2`

**US-1.2.2: Dịch thuật cơ bản Việt ↔ Anh**
- Mô tả: User yêu cầu dịch → nội dung được dịch từng phần, giữ nguyên cấu trúc.
- Tiêu chí nghiệm thu:
  - AC1: Dịch theo section, giữ formatting
  - AC2: Trigger: "dịch thuật", "translate", "dịch sang"
- Bị chặn bởi: `US-1.2.1`

---

### Epic 1.3: Xuất Word (`tao-word`)

**US-1.3.1: Xuất Word với 3 template style**
- Mô tả: Xuất nội dung tổng hợp ra file .docx chuyên nghiệp — chọn corporate, academic, hoặc minimal.
- Tiêu chí nghiệm thu:
  - AC1: SKILL.md tồn tại (≤ 400 dòng)
  - AC2: 3 style: corporate, academic, minimal
  - AC3: Hỗ trợ: heading, table, bullet, image
  - AC4: Dùng WidthType.DXA cho table
  - AC5: In đường dẫn và kích thước file
- Bị chặn bởi: `US-1.2.1`, `US-1.1.1`

---

### Epic 1.4: Xuất PowerPoint (`tao-slide`)

**US-1.4.1: Xuất PowerPoint với 3 template style**
- Mô tả: Xuất nội dung ra file .pptx chuyên nghiệp — mỗi slide có visual element.
- Tiêu chí nghiệm thu:
  - AC1: SKILL.md tồn tại (≤ 400 dòng)
  - AC2: 3 style: corporate, academic, minimal
  - AC3: Dùng pptxgenjs (Node.js), không dùng # prefix cho màu
  - AC4: Mỗi slide có ít nhất 1 visual element
  - AC5: In đường dẫn và kích thước file
- Bị chặn bởi: `US-1.2.1`, `US-1.1.1`

---

## Phase 2: Mở rộng — Tìm kiếm & Thêm định dạng

### Epic 2.1: Tìm kiếm Google tự động

**US-2.1.1: Tích hợp web search vào thu-thap**
- Mô tả: Khi user không cung cấp nguồn cụ thể → pipeline tự search Google và fetch kết quả.
- Tiêu chí nghiệm thu:
  - AC1: Dùng `vscode-websearchforcopilot_webSearch`
  - AC2: Fetch top 3-5 URL → trình bày cho user duyệt
  - AC3: Hoạt động kết hợp với file/URL thủ công
- Bị chặn bởi: `US-1.1.1`

---

### Epic 2.2: Xuất Excel (`tao-excel`)

**US-2.2.1: Xuất Excel với công thức và formatting**
- Mô tả: Xuất dữ liệu có cấu trúc ra file .xlsx với công thức Excel hoạt động.
- Tiêu chí nghiệm thu:
  - AC1: SKILL.md tồn tại (≤ 400 dòng)
  - AC2: Dùng openpyxl + pandas
  - AC3: Mọi giá trị tính toán dùng =FORMULA()
  - AC4: Chạy recalc.py sau khi tạo
  - AC5: Kiểm tra không có lỗi công thức
- Bị chặn bởi: `US-1.2.1`

---

### Epic 2.3: Xuất PDF (`tao-pdf`)

**US-2.3.1: Xuất PDF từ nội dung tổng hợp**
- Mô tả: Xuất file PDF chuyên nghiệp với TOC, headers/footers, hỗ trợ tiếng Việt.
- Tiêu chí nghiệm thu:
  - AC1: SKILL.md tồn tại (≤ 400 dòng)
  - AC2: Dùng reportlab Platypus
  - AC3: Embed font cho tiếng Việt
- Bị chặn bởi: `US-1.2.1`

---

### Epic 2.4: Xuất HTML (`tao-html`)

**US-2.4.1: Xuất HTML tĩnh với 3 template style**
- Mô tả: Xuất trang HTML portable (inline CSS), mở được trên mọi browser.
- Tiêu chí nghiệm thu:
  - AC1: SKILL.md tồn tại (≤ 400 dòng)
  - AC2: Dùng jinja2 templates
  - AC3: 3 style, single-file output
  - AC4: Chart embed dạng base64
- Bị chặn bởi: `US-1.2.1`

---

### Epic 2.5: Chaining Output

**US-2.5.1: Chuỗi output trong pipeline**
- Mô tả: Pipeline hỗ trợ chuỗi (Excel → chart → PPT), hiển thị kế hoạch trước khi chạy.
- Tiêu chí nghiệm thu:
  - AC1: Nhận diện yêu cầu cần nhiều format
  - AC2: Hiển thị chain plan trước
  - AC3: File trung gian lưu tmp/, dọn sau
- Bị chặn bởi: `US-1.3.1`, `US-1.4.1`, `US-2.2.1`

---

## Phase 3: Hoàn thiện — Trực quan & Tối ưu

### Epic 3.1: Biểu đồ & Hình ảnh (`tao-hinh`)

**US-3.1.1: Tạo biểu đồ từ dữ liệu**
- Mô tả: Tạo biểu đồ chuyên nghiệp (bar, line, pie, radar, scatter) và embed vào Word/PPT.
- Tiêu chí nghiệm thu:
  - AC1: SKILL.md tồn tại (≤ 400 dòng)
  - AC2: Luôn dùng matplotlib.use('Agg')
  - AC3: 5+ loại biểu đồ
  - AC4: Output PNG dpi=160
- Bị chặn bởi: `US-2.2.1`

**US-3.1.2: Tạo hình minh họa cho slide (Apple Silicon)**
- Mô tả: Gen hình minh họa từ prompt text để đưa vào slide — chỉ Apple Silicon.
- Tiêu chí nghiệm thu:
  - AC1: Dùng diffusers + torch/MPS
  - AC2: Bỏ qua nếu không phải Apple Silicon
  - AC3: Không render text trong ảnh
- Bị chặn bởi: `US-3.1.1`

---

### Epic 3.2: Xử lý tài liệu lớn

**US-3.2.1: Chunking strategy cho tài liệu lớn**
- Mô tả: Pipeline xử lý được corpus > 50,000 words bằng chunking + tổng hợp incremental.
- Tiêu chí nghiệm thu:
  - AC1: Phát hiện khi input vượt ngưỡng
  - AC2: Chia theo section/page, xử lý từng phần
  - AC3: Báo tiến độ cho user
- Bị chặn bởi: `US-1.2.1`

---

### Epic 3.3: Template Library mở rộng

**US-3.3.1: Thêm style dark/modern và creative**
- Mô tả: Thêm 2 style mới cho tao-slide và tao-html.
- Tiêu chí nghiệm thu:
  - AC1: 2 style mới: dark/modern, creative
  - AC2: Áp dụng cho tao-slide và tao-html
  - AC3: 3 style cũ không bị ảnh hưởng
- Bị chặn bởi: `US-1.3.1`, `US-1.4.1`, `US-2.4.1`

---

### Epic 3.4: Cải thiện UX Pipeline

**US-3.4.1: Cải thiện UX pipeline**
- Mô tả: Pipeline hiển thị progress rõ, hỏi xác nhận trước step nặng, gợi ý style.
- Tiêu chí nghiệm thu:
  - AC1: Progress step-by-step bằng tiếng Việt
  - AC2: Xác nhận trước step > 30 giây
  - AC3: Gợi ý style dựa trên context
- Bị chặn bởi: `US-0.3.1`, `US-2.5.1`

---

*Backlog này không bao gồm task-level detail hoặc trạng thái thực hiện.*  
*Bước tiếp theo: `/roadmap-to-user-stories-review` hoặc `/product-checklist`*
