# InsightEngine — User Stories Backlog

> **Product:** InsightEngine  
> **Product Slug:** insight-engine  
> **Created:** 2026-04-16  
> **Scope:** Phase 0 → Phase 10 (all phases)  
> **Total User Stories:** 91 (21 Phase 0-3 + 15 Phase 4 + 4 Phase 5 + 14 Phase 6 + 5 Phase 7 + 6 Phase 8 + 12 Phase 9 + 14 Phase 10)

---

## User Stories Overview

- **Product name:** InsightEngine
- **Product slug:** `insight-engine`
- **Scope covered:** Phase 0, Phase 1, Phase 2, Phase 3, Phase 4, Phase 5, Phase 6, Phase 7, Phase 8, Phase 9, Phase 10
- **Total stories:** 91 (Phase 0: 5, Phase 1: 6, Phase 2: 5, Phase 3: 5, Phase 4: 15, Phase 5: 4, Phase 6: 14, Phase 7: 5, Phase 8: 6, Phase 9: 12, Phase 10: 14)
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

## Phase 4: Nâng cấp — Template Library, Presentation HTML & Script Architecture

> **Nguồn gốc:** Phản hồi từ testing Phase 0-3 — output còn sơ sài, slide đơn giản, HTML thiếu tương tác.

---

### Epic 4.1: Template Library PPTX

**US-4.1.1: Professional PPTX template collection**
- Description: As a user, I want a library of 8-10 professional PPTX templates, so my presentations look polished and varied without manual design work.
- Acceptance Criteria:
  - AC1: 8-10 PPTX template scripts in `tao-slide/scripts/` — each produces a distinct visual style
  - AC2: Templates include: title slide, content slide, two-column, image+text, chart slide, section divider, closing slide
  - AC3: Each template has consistent color scheme, font pairing, spacing
  - AC4: Template names are descriptive (e.g., `corporate-blue.js`, `dark-gradient.js`, `minimal-white.js`)
  - AC5: All templates produce valid .pptx files via pptxgenjs
- Blocked By: `US-1.4.1`, `US-3.3.1`
- References: slidemembers.com, aippt.com, canva.com (visual inspiration)

**US-4.1.2: Template preview and selection**
- Description: As a user, I want to preview available templates before generation and select my preferred one, so I have control over the visual output.
- Acceptance Criteria:
  - AC1: `tao-slide` lists available templates with descriptions when user asks
  - AC2: Preview images (PNG) exist in `tao-slide/references/previews/` for each template
  - AC3: User can select template by name or let Copilot suggest based on context
  - AC4: Default template auto-selected based on content type (formal → corporate, tech → dark-modern)
- Blocked By: `US-4.1.1`

**US-4.1.3: PPTX script architecture**
- Description: As a developer, I want `tao-slide` to use executable scripts in `scripts/` for template rendering, so output is reliable and repeatable.
- Acceptance Criteria:
  - AC1: `tao-slide/scripts/` directory exists with Node.js CLI tools
  - AC2: Each template is a standalone script accepting JSON data + outputting .pptx
  - AC3: SKILL.md acts as router — determines template, prepares data, calls script
  - AC4: Scripts accept CLI arguments (no hardcoded paths)
  - AC5: Pattern follows a-z-copilot-flow/skills/pptx/scripts/ architecture
- Blocked By: `US-4.1.1`
- References: a-z-copilot-flow/skills/pptx (script architecture pattern)

---

### Epic 4.2: HTML Presentation Mode (reveal.js)

**US-4.2.1: reveal.js integration for tao-html**
- Description: As a user, I want HTML output to be an interactive presentation (not just a static page), so I can present directly in the browser with slide transitions.
- Acceptance Criteria:
  - AC1: `tao-html` can produce reveal.js-based presentations
  - AC2: Content is organized into slides (sections)
  - AC3: reveal.js loaded via CDN (no local install required)
  - AC4: Output is a single .html file (portable, self-contained)
  - AC5: Keyboard navigation works (arrows, space, ESC for overview)
- Blocked By: `US-2.4.1`, `US-3.3.1`
- References: revealjs.com, slides.com/templates

**US-4.2.2: Transitions, animations, and visual effects**
- Description: As a user, I want my HTML presentations to have smooth transitions and animations, so they feel professional and engaging.
- Acceptance Criteria:
  - AC1: At least 3 transition types available (slide, fade, zoom)
  - AC2: Fragment animations for bullet points (appear one by one)
  - AC3: Background images/gradients per slide
  - AC4: Code syntax highlighting for technical slides
  - AC5: User can specify transition style or use template default
- Blocked By: `US-4.2.1`
- References: revealjs.com (transitions), deckdeckgo.com (animation patterns)

**US-4.2.3: HTML presentation themes and backgrounds**
- Description: As a user, I want themed HTML presentations with professional backgrounds, so each presentation has a cohesive visual identity.
- Acceptance Criteria:
  - AC1: At least 5 reveal.js themes adapted for InsightEngine styles
  - AC2: Custom background support: solid color, gradient, image, video (URL)
  - AC3: Theme includes consistent typography, link colors, table styles
  - AC4: Dark and light variants available
- Blocked By: `US-4.2.1`
- References: slides.com/templates, deckdeckgo.com (themes)

---

### Epic 4.3: Script Architecture cho Skills

**US-4.3.1: tao-slide scripts/ directory**
- Description: As a developer, I want the `tao-slide` skill to have a `scripts/` directory with modular Node.js CLI tools, so template rendering is programmatic and testable.
- Acceptance Criteria:
  - AC1: `tao-slide/scripts/` exists with at least 3 scripts
  - AC2: `gen_slide.js` — main entry point accepting JSON data → .pptx
  - AC3: `templates/` subfolder with template-specific configs
  - AC4: `references/` has pptxgenjs API reference and design guidelines
  - AC5: Scripts print output file path + size as last line
- Blocked By: `US-4.1.3`
- References: a-z-copilot-flow/skills/pptx/scripts/ (architecture pattern)

**US-4.3.2: tao-html scripts/ directory**
- Description: As a developer, I want the `tao-html` skill to have a `scripts/` directory with Python CLI tools for reveal.js generation, so HTML presentation output is reliable.
- Acceptance Criteria:
  - AC1: `tao-html/scripts/` exists with at least 2 scripts
  - AC2: `gen_reveal.py` — main entry point accepting content JSON → .html
  - AC3: `templates/` subfolder with jinja2 reveal.js templates
  - AC4: `references/` has reveal.js API reference
  - AC5: Scripts accept CLI arguments and print output path + size
- Blocked By: `US-4.2.1`

**US-4.3.3: Script architecture for remaining output skills**
- Description: As a developer, I want all output skills (tao-word, tao-excel, tao-pdf) to follow the same scripts/ architecture pattern, so the codebase is consistent.
- Acceptance Criteria:
  - AC1: `tao-word/scripts/gen_docx.py` exists with CLI interface
  - AC2: `tao-excel/scripts/gen_xlsx.py` exists with CLI interface
  - AC3: `tao-pdf/scripts/gen_pdf.py` exists with CLI interface
  - AC4: All scripts accept JSON input + output file path as arguments
  - AC5: Pattern is consistent across all output skills
- Blocked By: `US-4.3.1`, `US-4.3.2`
- References: a-z-copilot-flow/skills/gen-image (multi-level script pattern)

---

### Epic 4.4: Nâng cấp Content Depth

**US-4.4.1: bien-soan comprehensive mode**
- Description: As a user, I want a "comprehensive" synthesis mode that produces richer, more detailed content, so my reports and presentations have sufficient depth.
- Acceptance Criteria:
  - AC1: `bien-soan` supports `--mode=comprehensive` flag (or equivalent)
  - AC2: Comprehensive mode produces 3-5x more content than default mode
  - AC3: Adds sub-sections, examples, data points, and context paragraphs
  - AC4: Generates section summaries and key takeaways
  - AC5: User can choose mode before synthesis begins
- Blocked By: `US-1.2.1`, `US-3.2.1`

**US-4.4.2: Content enrichment from multiple sources**
- Description: As a user, I want the pipeline to automatically enrich content with additional context from web search when source material is thin, so outputs are always substantive.
- Acceptance Criteria:
  - AC1: `bien-soan` detects when source content is insufficient (< threshold)
  - AC2: Automatically triggers `thu-thap` web search for additional context
  - AC3: Enriched content is clearly attributed (source citations)
  - AC4: User can disable auto-enrichment if desired
  - AC5: Works transparently within the pipeline (no extra user action needed)
- Blocked By: `US-2.1.1`, `US-4.4.1`

---

### Epic 4.5: Template Library HTML

**US-4.5.1: HTML reveal.js template collection**
- Description: As a user, I want 5-8 distinct HTML presentation templates based on reveal.js, so I have variety for different contexts (business, education, tech talks).
- Acceptance Criteria:
  - AC1: 5-8 template files in `tao-html/scripts/templates/`
  - AC2: Templates include: corporate-formal, academic-research, tech-dark, creative-colorful, minimal-clean
  - AC3: Each template defines color scheme, fonts, transitions, background style
  - AC4: Templates are jinja2 files extending a base reveal.js structure
  - AC5: All templates produce valid, self-contained .html files
- Blocked By: `US-4.2.1`, `US-4.2.3`
- References: slides.com/templates, deckdeckgo.com

**US-4.5.2: Presenter notes and PDF export**
- Description: As a user, I want my HTML presentations to include speaker notes and be exportable to PDF, so I can use them in professional settings.
- Acceptance Criteria:
  - AC1: Speaker notes support via reveal.js `<aside class="notes">`
  - AC2: `bien-soan` can generate speaker notes from synthesis content
  - AC3: PDF export via reveal.js print stylesheet (Ctrl+P)
  - AC4: PDF maintains slide layout and styling
- Blocked By: `US-4.5.1`
- References: revealjs.com (speaker view, PDF export)

---

## Phase 5: Tối ưu & Độ bền (Optimization & Resilience)

> **Nguồn gốc:** Phản hồi từ testing Phase 0-4 — skills chưa tối ưu cho model nhỏ; user mất tiến độ khi session bị ngắt.

---

### Epic 5.1: Small Model Optimization

**US-5.1.1: Small model compatibility research**
- Description: As a developer, I want to identify why InsightEngine skills fail or degrade with smaller AI models (GPT-4o-mini, GPT-3.5 Turbo), so I can target root causes for optimization.
- Acceptance Criteria:
  - AC1: Each SKILL.md tested against a smaller model (GPT-4o-mini or equivalent)
  - AC2: Failure patterns documented: token overflow, instruction following degradation, context loss
  - AC3: Compatibility report produced per skill with pass/fail per AC
  - AC4: Top 3 root causes identified with evidence
  - AC5: Report stored in `docs/reports/small-model-compatibility.md`
- Blocked By: `None`

**US-5.1.2: SKILL.md refactor for small model compatibility**
- Description: As a user on a smaller model, I want InsightEngine skills to give consistent, reliable results, so I’m not forced to use GPT-4/Claude.
- Acceptance Criteria:
  - AC1: All SKILL.md files ≤ 300 lines (reduced from ≤ 400)
  - AC2: Instructions rewritten as explicit, unambiguous step-by-step directives
  - AC3: Long reference content moved to `references/` sub-files; SKILL.md links to them instead of embedding
  - AC4: Skills re-tested on GPT-4o-mini with pass rate ≥ 80% on acceptance criteria
  - AC5: No behavior regression on Claude/GPT-4 (existing passing tests still pass)
- Blocked By: `US-5.1.1`

---

### Epic 5.2: Session State Persistence

**US-5.2.1: Session state save after each pipeline step**
- Description: As a user whose Copilot session was interrupted mid-pipeline, I want the pipeline to have saved my progress, so I can continue without re-doing completed steps.
- Acceptance Criteria:
  - AC1: `tong-hop` writes `tmp/.session-state.json` after each sub-skill completes successfully
  - AC2: State file includes: original user request, execution plan, completed steps (with output file paths), pending steps
  - AC3: State file also includes: timestamp, session ID (UUID), InsightEngine version
  - AC4: State file is human-readable JSON (pretty-printed, UTF-8)
  - AC5: Write operation is atomic (write to temp file, then rename) to prevent corruption
- Blocked By: `None`

**US-5.2.2: Pipeline resume from saved state**
- Description: As a user, I want to say „tiếp tục”, „resume”, or „/resume” to have the pipeline detect and continue from a previous interrupted session.
- Acceptance Criteria:
  - AC1: `tong-hop` checks `tmp/.session-state.json` on startup
  - AC2: If state file found: Copilot presents summary of previous session in Vietnamese and asks „Tiếp tục hay bắt đầu lại?”
  - AC3: If user chooses resume: pipeline skips completed steps and continues from last checkpoint
  - AC4: If user chooses start fresh: old state file is archived as `tmp/.session-state.<timestamp>.json`
  - AC5: Triggers on: „tiếp tục”, „resume”, „tiếp tục từ”, „/resume”
  - AC6: If no state file found: pipeline starts normally without asking
- Blocked By: `US-5.2.1`

---

## Phase 6: Agent Architecture & Quality Gates

> **Nguồn gốc:** Phản hồi từ real-world usage — pipeline thiếu linh hoạt, thiếu kiểm tra chất lượng tự động, hỏi user quá nhiều, file output nằm rải rác.

---

### Epic 6.1: Strict File Rules & Auto-escalation

**US-6.1.1: Strict file location rules enforcement**
- Description: As a user, I want all InsightEngine output to follow strict file placement rules (scripts in `/scripts`, temp in `/tmp`, output in `/output`), so files are always predictable regardless of which model runs the pipeline.
- Acceptance Criteria:
  - AC1: All skills updated with explicit file placement rules
  - AC2: Scripts MUST be saved to `/scripts` directory
  - AC3: Temporary/intermediate files MUST be saved to `/tmp` directory
  - AC4: Final output files MUST be saved to `/output` directory
  - AC5: Rules enforced via validation check at pipeline start and after each step
- Blocked By: `None`

**US-6.1.2: Auto-escalation protocol**
- Description: As a non-technical user, I want the pipeline to automatically escalate to more powerful tools when the current approach fails, without asking me technical questions I don't understand.
- Acceptance Criteria:
  - AC1: Each skill defines escalation tiers (e.g., thu-thap: fetch_webpage → httpx → Playwright)
  - AC2: On failure, skill automatically tries the next tier without user interaction
  - AC3: User is only asked when ALL escalation tiers have been exhausted
  - AC4: Technical tool names are never exposed to user (e.g., don't mention "Playwright tier 3")
  - AC5: Escalation attempts are logged in shared context for audit trail
- Blocked By: `US-6.1.1`

---

### Epic 6.2: Shared Context Protocol

**US-6.2.1: Shared context file design**
- Description: As a pipeline component, I need a standardized shared context file (`tmp/.agent-context.json`) that all agents can read and write to, so inter-agent communication works despite subagent statelessness.
- Acceptance Criteria:
  - AC1: `tmp/.agent-context.json` schema defined with fields: user_request, model_profile, workflow, audit_history, decisions
  - AC2: File is human-readable JSON (pretty-printed, UTF-8)
  - AC3: Write operation is atomic (temp file + rename)
  - AC4: Schema documented in `references/agent-context-schema.md`
- Blocked By: `None`

**US-6.2.2: Agent context read/write API**
- Description: As an agent, I need a consistent protocol for reading context before my task and writing results after, so no information is lost between agent calls.
- Acceptance Criteria:
  - AC1: Every agent call starts by reading shared context file
  - AC2: Every agent call ends by writing results to shared context file
  - AC3: Protocol handles concurrent access gracefully (file locking or sequential execution)
  - AC4: Protocol documented with examples in references/
- Blocked By: `US-6.2.1`

---

### Epic 6.3: Model Profile & Decision Maps

**US-6.3.1: Decision maps per capability category**
- Description: As a pipeline strategist, I need pre-built decision maps for each model capability category (context_window, reasoning_depth, tool_use, multilingual, code_generation), so I can choose the right workflow without trusting model self-reports blindly.
- Acceptance Criteria:
  - AC1: Decision maps created for 5 capability categories
  - AC2: Each category has 3 levels: basic, standard, advanced
  - AC3: Each level has corresponding workflow recommendations
  - AC4: Maps stored in `references/decision-maps.md`
  - AC5: Maps are model-name-agnostic (based on capabilities, not brand)
- Blocked By: `None`

**US-6.3.2: Model self-declaration with fallback**
- Description: As a pipeline, I need to determine the current model's capabilities at startup via self-declaration + decision map verification, falling back to a medium/conservative profile if detection fails.
- Acceptance Criteria:
  - AC1: Pipeline asks model to self-declare name and capabilities at startup
  - AC2: Self-declared capabilities are verified against decision maps (not blindly trusted)
  - AC3: If model cannot self-identify: fallback to conservative/medium profile (context 32K, clear instructions needed, small steps)
  - AC4: Model name is NOT hardcoded in copilot-instructions.md
  - AC5: Model profile is written to shared context file for all agents to use
- Blocked By: `US-6.3.1`, `US-6.2.1`

**US-6.3.3: Pre-built workflow templates**
- Description: As a strategist agent, I need pre-built workflow templates for common scenarios × model capability levels, so I can quickly generate a custom workflow instead of building from scratch.
- Acceptance Criteria:
  - AC1: At least 5 workflow templates covering common scenarios (report, presentation, data collection, translation, comparison)
  - AC2: Each template has variants for basic/standard/advanced model capabilities
  - AC3: Templates stored in `references/workflow-templates/`
  - AC4: Strategist can customize templates based on specific request
- Blocked By: `US-6.3.1`

---

### Epic 6.4: Agent Strategist

**US-6.4.1: Strategist agent — dynamic workflow generation**
- Description: As a user, I want the pipeline to generate a custom workflow tailored to my specific request AND the current model's capabilities, so the process is optimized for the best possible output.
- Acceptance Criteria:
  - AC1: Strategist agent receives: user request + model profile (from shared context)
  - AC2: Generates a step-by-step workflow with skill assignments and quality checkpoints
  - AC3: Selects and customizes from pre-built workflow templates
  - AC4: Budget: 1 strategist call per pipeline run (no retries on strategist itself)
  - AC5: Generated workflow is written to shared context and presented to user before execution
- Blocked By: `US-6.3.2`, `US-6.3.3`, `US-6.2.1`

---

### Epic 6.5: Tiered Audit System

**US-6.5.1: Tiered audit implementation**
- Description: As a pipeline, I need a tiered quality audit system that applies the right level of scrutiny to each step, so quality is ensured without wasting resources on trivial checks.
- Acceptance Criteria:
  - AC1: Tier 1 (self-review): Applied to ALL steps — inline quality check, 0 extra agent calls
  - AC2: Tier 2 (agent audit): Applied to CRITICAL steps (bien-soan, output generation) — 1 agent call per step
  - AC3: Tier 3 (final audit): Applied to final output — full comparison against user requirements
  - AC4: Max 5 audit agent calls per pipeline run
  - AC5: Audit results written to shared context `audit_history`
- Blocked By: `US-6.2.1`

**US-6.5.2: Final output audit with step-level rollback**
- Description: As a user, I want the pipeline to automatically audit the final output against my original request, and if it doesn't meet requirements, go back to the specific step that failed instead of restarting everything.
- Acceptance Criteria:
  - AC1: Final audit compares output against user's original request (extracted from shared context)
  - AC2: If audit fails: identifies which step produced insufficient quality
  - AC3: Pipeline re-executes from the failed step (not from beginning)
  - AC4: Max 3 attempts per step, max 10 total retries across pipeline
  - AC5: Fail-fast: if quality score doesn't improve between retry 1 and retry 2, stop retrying and deliver best available
  - AC6: Budget cap: max 30 agent calls per pipeline run
- Blocked By: `US-6.5.1`, `US-6.4.1`

---

### Epic 6.6: Advisory Agent & Conditional Skill Creation

**US-6.6.1: Advisory agent — multi-perspective single-call**
- Description: As a pipeline, I need an advisory agent that can analyze a decision from 3-5 perspectives in a single call, so I get expert guidance without excessive token overhead.
- Acceptance Criteria:
  - AC1: Advisory agent receives a question + context → returns analysis from 3-5 perspectives + final recommendation
  - AC2: Single call format (not 5 separate calls)
  - AC3: Max 2 advisory calls per pipeline run
  - AC4: Decision severity routing: trivial → auto-decide, moderate → 1 advisory, critical → advisory + user
  - AC5: Advisory decisions logged in shared context `decisions` array
- Blocked By: `US-6.2.1`

**US-6.6.2: Conditional skill-forge runtime**
- Description: As a pipeline, I want the ability to create new skills at runtime when they are absolutely required to complete the user's request, with a 30-minute budget and advisory approval.
- Acceptance Criteria:
  - AC1: Advisory agent evaluates: is a new skill REQUIRED? (cannot complete without it)
  - AC2: If advisory says not needed: use existing skills + inline instructions
  - AC3: If advisory approves: skill creation with 30-minute budget
  - AC4: Created skills follow InsightEngine conventions (Vietnamese naming, scripts/, references/)
  - AC5: Created skills are tested before use in the current pipeline
- Blocked By: `US-6.6.1`

**US-6.6.3: Public skill clone with security check**
- Description: As a pipeline creating a new skill, I want to prioritize cloning from verified public repositories to save time, with mandatory security review before adoption.
- Acceptance Criteria:
  - AC1: Clone sources whitelist: github.com/anthropics/skills, github.com/openclaw/openclaw/tree/main/skills, github.com/openai/skills
  - AC2: Clone priority: (1) clone + adapt from public repos → (2) build from scratch
  - AC3: Security check MANDATORY before using any cloned skill: no malware, no data exfiltration, no dangerous commands
  - AC4: Security check results logged in shared context
  - AC5: If security check fails: fall back to building from scratch
- Blocked By: `US-6.6.2`

---

### Epic 6.7: Pipeline Integration

**US-6.7.1: tong-hop integration with AGENT_MODE feature flag**
- Description: As a developer, I want the agent architecture to be toggleable via a feature flag in tong-hop, so I can switch between the current pipeline and the agent-enhanced pipeline.
- Acceptance Criteria:
  - AC1: `AGENT_MODE` flag in tong-hop SKILL.md (default: true)
  - AC2: When `AGENT_MODE: true`: strategist → dynamic workflow → tiered audit → advisory
  - AC3: When `AGENT_MODE: false`: current static pipeline (backward compatible)
  - AC4: User experience unchanged — user still says request → gets output
  - AC5: Existing skills NOT modified — agents wrap around them
- Blocked By: `US-6.4.1`, `US-6.5.1`, `US-6.6.1`

---

## Phase 7: Pipeline Enforcement & Compliance Hardening

> **Nguồn gốc:** Real-world testing reveals models skip critical pipeline steps (request analysis, URL validation, AGENT_MODE flow) when instructions are buried in reference files. Phase 7 moves enforcement inline and adds hard gates.

---

### Epic 7.1: Inline Critical Steps & Hard Gates

**US-7.1.1: Inline request analysis and REQUEST_TYPE detection**
- Description: As a pipeline user, I want Step 1.5 (request deep analysis) and Step 1 REQUEST_TYPE detection logic to live inline in tong-hop SKILL.md rather than in reference files, so that all models — including smaller ones — reliably execute these critical steps.
- Acceptance Criteria:
  - AC1: Step 1.5 request analysis protocol (dimension expansion, data collection strategy) is inline in tong-hop SKILL.md
  - AC2: REQUEST_TYPE detection logic (research vs data_collection vs mixed) is inline in Step 1
  - AC3: Reference files (`references/request-analysis.md`) retain supplementary details only — not the core decision flow
  - AC4: tong-hop SKILL.md remains ≤ 500 lines (use progressive disclosure for non-critical content)
  - AC5: Tested with GPT-4o-mini — model correctly identifies REQUEST_TYPE and shows analysis
- Blocked By: `None`

**US-7.1.2: Hard confirmation gate before execution**
- Description: As a user, I want the pipeline to STOP and show me its analysis of my request (expanded dimensions, detected type, execution plan) and wait for my explicit 'ok' before proceeding, so I can verify the pipeline understood correctly.
- Acceptance Criteria:
  - AC1: Pipeline MUST display Step 1.5 analysis output to user in Vietnamese
  - AC2: Pipeline MUST receive explicit user confirmation ("ok", "đồng ý", "tiếp tục") before moving to Step 3
  - AC3: If user does not confirm, pipeline STOPS (does not silently proceed)
  - AC4: Analysis display includes: request_type, detected dimensions/fields, planned steps, content_depth
  - AC5: Gate is enforced regardless of model — instruction is unambiguous imperative ("STOP HERE. Show analysis. Wait for user.")
- Blocked By: `US-7.1.1`

---

### Epic 7.2: Data Collection Enforcement

**US-7.2.1: Inline data collection protocol in thu-thap**
- Description: As a pipeline user requesting structured data collection (jobs, products, courses), I want thu-thap to reliably use platform-specific search and extract individual item URLs, so I get direct links instead of search result pages.
- Acceptance Criteria:
  - AC1: Data collection protocol (platform-specific search, individual page fetch, field extraction) is inline in thu-thap SKILL.md main body
  - AC2: `references/data-collection-mode.md` retains advanced examples only — core protocol is inline
  - AC3: thu-thap MUST use `site:{platform}` search when mode=data_collection (not generic Google)
  - AC4: thu-thap MUST fetch and verify individual item pages (not search result pages, not aggregator listing pages)
  - AC5: Each extracted item MUST have a `direct_url` field pointing to the specific item page
- Blocked By: `None`

**US-7.2.2: Pre-output URL validation gate**
- Description: As a user, I want URLs in my Excel output to be validated BEFORE the file is generated, so invalid URLs never reach the final deliverable.
- Acceptance Criteria:
  - AC1: `scripts/validate_urls.py` runs BEFORE tao-excel generates the output file (not just in post-hoc audit)
  - AC2: URLs classified as SEARCH or LISTING trigger automatic re-fetch for that specific item
  - AC3: After re-fetch attempt, remaining invalid URLs are flagged with ⚠️ in the Excel file
  - AC4: Validation summary shown to user: "X/Y URLs verified as direct links"
  - AC5: If >50% URLs invalid after re-fetch: STOP and ask user whether to proceed or re-search
- Blocked By: `US-7.2.1`

---

### Epic 7.3: Visible Pipeline Trace

**US-7.3.1: Numbered step trace with live progress**
- Description: As a user, I want to see a numbered list of all pipeline steps at the start, with each step marked ✅ as it completes, so I can verify the pipeline is following the correct sequence and catch any skipped steps.
- Acceptance Criteria:
  - AC1: Pipeline prints numbered step list at start (after plan approval): "📋 Pipeline steps: 1. Phân tích yêu cầu 2. Thu thập 3. Biên soạn 4. Xuất file 5. Kiểm tra"
  - AC2: Each step is marked ✅ with a one-line summary when completed
  - AC3: Skipped steps are marked ⏭️ with explanation
  - AC4: Failed steps are marked ❌ with error summary
  - AC5: Step trace is always visible (not buried in collapsed sections or reference files)
- Blocked By: `None`

---

## Phase 8: Shared Copilot Agent Architecture

> **Nguồn gốc:** Phase 6 embedded agents inside tong-hop as inline instructions. Phase 8 refactors them into standalone shared Copilot agents (`runSubagent`) that any skill can invoke.

---

### Epic 8.1: Shared Auditor Agent

**US-8.1.1: Auditor as standalone Copilot agent**
- Description: As a pipeline, I need an auditor agent that can be invoked via `runSubagent` from any skill, so output quality is verified at every generation point — not just at pipeline end.
- Acceptance Criteria:
  - AC1: Auditor agent exists as a standalone prompt/agent definition (not inline in tong-hop)
  - AC2: Receives: generated file content (or summary) + original user requirements
  - AC3: Returns structured verdict: PASS/FAIL + specific issues list + improvement suggestions
  - AC4: Can be invoked via `runSubagent` from any skill context
  - AC5: Auditor reads back file content and verifies against requirements (not just checks file existence)
- Blocked By: `None`

**US-8.1.2: Auditor integration into output skills**
- Description: As a user, I want every output skill (tao-word, tao-excel, tao-slide, tao-pdf, tao-html) to automatically call the auditor agent after file generation, so quality is verified regardless of whether I used the full pipeline or called a skill directly.
- Acceptance Criteria:
  - AC1: tao-word calls auditor after generating .docx — verifies content depth, section completeness
  - AC2: tao-excel calls auditor after generating .xlsx — verifies data population, URL validity, formula correctness
  - AC3: tao-slide calls auditor after generating .pptx — verifies slide count, content per slide, coverage
  - AC4: tao-pdf and tao-html call auditor with appropriate checks
  - AC5: If auditor returns FAIL → skill re-generates with auditor's improvement suggestions (max 2 retries)
  - AC6: Budget: max 5 auditor calls per pipeline run
- Blocked By: `US-8.1.1`

---

### Epic 8.2: Shared Strategist Agent

**US-8.2.1: Strategist as standalone Copilot agent**
- Description: As a pipeline orchestrator, I need the strategist agent refactored from inline tong-hop logic into a standalone `runSubagent` agent, so workflow generation is isolated and reusable.
- Acceptance Criteria:
  - AC1: Strategist agent exists as standalone prompt/agent definition
  - AC2: Receives: user request + model profile (from shared context)
  - AC3: Returns: step-by-step workflow with skill assignments and quality checkpoints
  - AC4: Selects from pre-built workflow templates (retained from Phase 6)
  - AC5: tong-hop calls strategist via `runSubagent` instead of inline strategy logic
  - AC6: Budget: max 1 strategist call per pipeline run
- Blocked By: `None`

---

### Epic 8.3: Shared Advisory Agent

**US-8.3.1: Advisory as standalone Copilot agent**
- Description: As any skill facing an ambiguous decision, I need an advisory agent I can call via `runSubagent` to get multi-perspective analysis, so decisions are informed rather than guessed.
- Acceptance Criteria:
  - AC1: Advisory agent exists as standalone prompt/agent definition
  - AC2: Receives: decision question + context → returns analysis from 3-5 perspectives + recommendation
  - AC3: Any skill can invoke it (not restricted to tong-hop)
  - AC4: Single call format (not multiple separate calls per perspective)
  - AC5: Budget: max 2 advisory calls per pipeline run
- Blocked By: `None`

---

### Epic 8.4: Agent Integration Protocol

**US-8.4.1: Standardized agent calling protocol**
- Description: As a developer, I need a standardized protocol for how skills call agents, so all agent interactions are consistent and predictable.
- Acceptance Criteria:
  - AC1: Documented input format for each agent (auditor, strategist, advisory) — what data to pass in `runSubagent` prompt
  - AC2: Documented output format — how to parse agent response (verdict, workflow, recommendation)
  - AC3: Budget enforcement documented: auditor 5/pipeline, advisory 2, strategist 1
  - AC4: Protocol documented in `references/agent-protocol.md`
- Blocked By: `US-8.1.1`, `US-8.2.1`, `US-8.3.1`

**US-8.4.2: tong-hop migration to shared agents**
- Description: As a pipeline orchestrator, I need tong-hop to delegate to shared agents instead of using inline agent logic, so the SKILL.md is leaner and agents are truly shared.
- Acceptance Criteria:
  - AC1: tong-hop calls strategist agent via `runSubagent` for workflow generation (replaces inline strategy)
  - AC2: tong-hop calls auditor agent for critical step verification (replaces inline quality gate text)
  - AC3: AGENT_MODE feature flag removed — agents are always available as infrastructure
  - AC4: tong-hop SKILL.md reduced in complexity (inline agent personas removed)
  - AC5: No regression in pipeline behavior — same user experience, better quality
- Blocked By: `US-8.4.1`

---

## Phase 9: Central Orchestrator & Adaptive Self-Improvement

> Separate orchestration from content synthesis. Introduce central orchestrator agent, adaptive self-improvement, 100-point weighted audit scoring, and full cross-session resume. Align ALL agents with VS Code custom agent standard (`.github/agents/*.agent.md`).

### Epic 9.1: Central Orchestrator Agent (`dieu-phoi`)

**US-9.1.1: Central orchestrator agent skeleton**
- Description: As a user, I need a central orchestrator agent (`dieu-phoi.agent.md` in `.github/agents/`) that classifies my request intent and routes to the appropriate skills and agents, so I’m not forced through the synthesis pipeline for non-synthesis tasks.
- Acceptance Criteria:
  - AC1: `dieu-phoi.agent.md` exists in `.github/agents/` with valid VS Code custom agent YAML frontmatter (description, tools, agents, handoffs, user-invocable: true)
  - AC2: Classifies intent into categories: synthesis, creation, research, design, data_collection, mixed, unknown
  - AC3: Routes to appropriate skills/agents based on classification
  - AC4: Falls back to asking user for clarification on `unknown` intent
  - AC5: Logs classification + routing decision to session state
- Blocked By: `US-8.4.2`

**US-9.1.2: tong-hop refactor to synthesis-only skill**
- Description: As a developer, I need tong-hop refactored to be a pure content synthesis skill (no orchestration logic), so the orchestration responsibility belongs solely to dieu-phoi.
- Acceptance Criteria:
  - AC1: tong-hop SKILL.md contains only content synthesis logic (gather → merge → structure)
  - AC2: All intent classification, routing, and pipeline orchestration removed from tong-hop
  - AC3: dieu-phoi calls tong-hop as one of many possible skills
  - AC4: Standalone `/tong-hop` trigger still works (dieu-phoi intercepts and routes)
  - AC5: No regression in synthesis quality
- Blocked By: `US-9.1.1`

**US-9.1.3: dieu-phoi integration with shared agents**
- Description: As an orchestrator, I need dieu-phoi to invoke shared agents (strategist, auditor, advisory) via VS Code agent handoffs, so workflow planning and quality checks are orchestrated centrally.
- Acceptance Criteria:
  - AC1: dieu-phoi YAML frontmatter lists `agents: [strategist, auditor, advisory]`
  - AC2: dieu-phoi calls strategist for workflow generation before execution
  - AC3: dieu-phoi calls auditor at pipeline end for final quality gate
  - AC4: Budget enforcement: strategist 1/pipeline, auditor 5/pipeline, advisory 2/pipeline
- Blocked By: `US-9.1.1`

---

### Epic 9.2: Adaptive Self-Improvement

**US-9.2.1: Capability gap evaluation protocol**
- Description: As an orchestrator, I need dieu-phoi to evaluate whether existing skills and agents can fulfill the user’s request before execution, so capability gaps are identified early.
- Acceptance Criteria:
  - AC1: Before execution, dieu-phoi maps request requirements to available skills/agents
  - AC2: Identifies specific gaps (e.g., "no skill for manga page layout")
  - AC3: Reports gaps to user with proposed solution (create new skill/agent)
  - AC4: Proceeds with existing capabilities if user declines creation
- Blocked By: `US-9.1.1`

**US-9.2.2: Runtime agent creation with user consent**
- Description: As a user, I want the orchestrator to create specialized agents at runtime when a capability gap is identified, so the system adapts to my needs without manual setup.
- Acceptance Criteria:
  - AC1: dieu-phoi proposes new agent creation with description and purpose
  - AC2: User must explicitly approve before creation
  - AC3: Created agent follows `.agent.md` format in `.github/agents/`
  - AC4: Created agent is tested with a smoke test before use
  - AC5: Time notification at 30 min; user can "unlock" extended self-improvement
- Blocked By: `US-9.2.1`

**US-9.2.3: Runtime skill creation/upgrade**
- Description: As a user, I want the orchestrator to create or upgrade skills at runtime when existing skills are insufficient, so the system’s capabilities grow organically.
- Acceptance Criteria:
  - AC1: dieu-phoi proposes skill creation/upgrade with rationale
  - AC2: User must approve; created skill follows SKILL.md standard
  - AC3: Skill is registered in copilot-instructions.md
  - AC4: Created skill is smoke-tested before use in current pipeline
- Blocked By: `US-9.2.1`

---

### Epic 9.3: Enhanced Working State & Cross-Session Resume

**US-9.3.1: Enhanced session state schema**
- Description: As a pipeline, I need the session state to store comprehensive context (raw_prompt, analyzed_requirements, generated_plan, step_states[], audit_test_cases[], score_history[], created_skills[]), so full context can be reconstructed for resume.
- Acceptance Criteria:
  - AC1: State schema documented with all required fields
  - AC2: `save_state.py` updated to persist new schema
  - AC3: Output file hash tracking for conflict detection
  - AC4: Backwards-compatible with existing Phase 5 state format
- Blocked By: `US-5.2.1`

**US-9.3.2: Step-level state persistence**
- Description: As a pipeline, I need state saved after each step (not just at checkpoints), so any interruption loses at most one step of work.
- Acceptance Criteria:
  - AC1: State saved after each sub-skill completes
  - AC2: Each step’s input, output summary, and status recorded
  - AC3: Audit test cases and scores persisted per step
  - AC4: Resume correctly identifies last completed step
- Blocked By: `US-9.3.1`

**US-9.3.3: Cross-session resume**
- Description: As a user, I need to resume a pipeline in a completely new Copilot session by loading the saved state, so interruptions don’t force me to start over.
- Acceptance Criteria:
  - AC1: dieu-phoi detects saved state on session start and offers to resume
  - AC2: Full context reconstructed from state (no guessing or re-analysis)
  - AC3: Output file hashes checked for conflicts (files modified externally)
  - AC4: User can choose to resume or start fresh
- Blocked By: `US-9.3.2`

---

### Epic 9.4: 100-Point Weighted Audit Scoring

**US-9.4.1: 100-point audit scoring system**
- Description: As a quality gate, I need auditor to generate dynamic test cases from requirements (total 100 pts, weighted by importance) and score output against them, replacing the binary PASS/FAIL verdict.
- Acceptance Criteria:
  - AC1: Auditor analyzes user requirements → generates test case set (total weight = 100)
  - AC2: Each test case has: name, weight (pts), pass criteria, category
  - AC3: Categories: requirement_coverage (40%), data_quality (25%), format_compliance (20%), completeness (15%)
  - AC4: Output scored against test cases → total score /100
  - AC5: Pass threshold: >80/100
  - AC6: Score breakdown visible to user
- Blocked By: `US-8.1.1`

**US-9.4.2: Targeted retry loop with score tracking**
- Description: As a pipeline, I need failed audits to trigger targeted retries that focus on specific low-scoring test cases, so retries are efficient rather than full regeneration.
- Acceptance Criteria:
  - AC1: On score <80, identify test cases with score 0
  - AC2: Retry targets only the failing areas (not full regeneration)
  - AC3: Max 5 retries per pipeline run
  - AC4: Score progression tracked: [attempt1: 62, attempt2: 78, attempt3: 85]
  - AC5: If score plateaus (no improvement for 2 consecutive retries), stop and report to user
- Blocked By: `US-9.4.1`

---

### Epic 9.5: VS Code Custom Agent Standard Migration

**US-9.5.1: Migrate existing agents to .agent.md format**
- Description: As a developer, I need all existing shared agents (auditor, strategist, advisory) migrated from `runSubagent`/shared-agents pattern to `.github/agents/*.agent.md` files with proper YAML frontmatter.
- Acceptance Criteria:
  - AC1: `auditor.agent.md` exists in `.github/agents/` with frontmatter: description, tools, user-invocable: true
  - AC2: `strategist.agent.md` exists in `.github/agents/` with frontmatter: user-invocable: false
  - AC3: `advisory.agent.md` exists in `.github/agents/` with frontmatter: user-invocable: false
  - AC4: Old `shared-agents/` references updated to `.github/agents/`
  - AC5: copilot-instructions.md updated with agent registry
- Blocked By: `US-8.1.1`, `US-8.2.1`, `US-8.3.1`

---

## Phase 10: English Naming, Natural Language UX & Product Alignment

### Epic 10.1: Rename Skills to English

**US-10.1.1: Rename all skill directories from Vietnamese to English**
- Description: As a developer, I need all 13 skill directories renamed from Vietnamese to English (tong-hop→synthesize, thu-thap→gather, bien-soan→compose, tao-word→gen-word, tao-excel→gen-excel, tao-slide→gen-slide, tao-pdf→gen-pdf, tao-html→gen-html, tao-hinh→gen-image, thiet-ke→design, kiem-tra→verify, cai-tien→improve, cai-dat→setup) so skill names are internationally consistent.
- Acceptance Criteria:
  - AC1: All 13 skill directories renamed under `.github/skills/`
  - AC2: Each SKILL.md file header updated to reflect new English name
  - AC3: All internal cross-references between skills updated
  - AC4: No broken references after rename
- Blocked By: `None`

**US-10.1.2: Update SKILL.md triggers for renamed skills**
- Description: As a user, I need all SKILL.md trigger lists updated so both Vietnamese and English natural language phrases work with the new English skill names.
- Acceptance Criteria:
  - AC1: Each SKILL.md triggers section uses natural language phrases (Vietnamese + English)
  - AC2: Old slash commands (`/tong-hop`, `/thu-thap`, etc.) removed from triggers
  - AC3: Copilot correctly routes to skills via natural language prompts
- Blocked By: `US-10.1.1`

---

### Epic 10.2: Rename Agents to English

**US-10.2.1: Rename dieu-phoi agent to orchestrator**
- Description: As a developer, I need `dieu-phoi.agent.md` renamed to `orchestrator.agent.md` with all frontmatter and documentation references updated.
- Acceptance Criteria:
  - AC1: `.github/agents/orchestrator.agent.md` exists with updated frontmatter (name: orchestrator)
  - AC2: Old `.github/agents/dieu-phoi.agent.md` removed
  - AC3: All agent handoff references updated (auditor, strategist, advisory reference orchestrator)
  - AC4: copilot-instructions.md agent registry updated
- Blocked By: `None`

---

### Epic 10.3: Natural Language UX

**US-10.3.1: Remove slash command dependency**
- Description: As a user, I want to describe my needs in natural language without memorizing slash commands, so the orchestrator agent handles intent classification and routing automatically.
- Acceptance Criteria:
  - AC1: orchestrator.agent.md classifies intent from natural language (no slash command parsing)
  - AC2: All `/command` references removed from SKILL.md trigger lists
  - AC3: copilot-instructions.md Commands Reference table removed or replaced with natural language examples
  - AC4: README updated with natural language usage examples
- Blocked By: `US-10.1.2`, `US-10.2.1`

**US-10.3.2: Update README for natural language UX**
- Description: As a user reading the README, I want clear examples of natural language interaction (not slash commands) so I understand how to use InsightEngine effectively.
- Acceptance Criteria:
  - AC1: README shows natural language examples for all common use cases
  - AC2: No slash command references in user-facing documentation
  - AC3: Skill names shown in English throughout README
- Blocked By: `US-10.3.1`

---

### Epic 10.4: copilot-instructions.md Refresh

**US-10.4.1: Update skill registry with English names**
- Description: As Copilot, I need copilot-instructions.md skill registry updated with English skill names, purposes, locations, and triggers so I correctly discover and invoke skills.
- Acceptance Criteria:
  - AC1: All skill entries use new English names (synthesize, gather, compose, gen-word, etc.)
  - AC2: All location paths point to renamed directories
  - AC3: All triggers use natural language (no slash commands)
  - AC4: Agent registry uses orchestrator (not dieu-phoi)
- Blocked By: `US-10.1.1`, `US-10.2.1`

**US-10.4.2: Fix stale PIPELINE_FLOW and update Vietnamese Language Rules**
- Description: As Copilot, I need the PIPELINE_FLOW section fixed (tong-hop no longer orchestrates — orchestrator does) and Vietnamese Language Rules updated to reflect English skill naming convention.
- Acceptance Criteria:
  - AC1: PIPELINE_FLOW references orchestrator agent as entry point
  - AC2: tong-hop described as synthesis-only skill in the flow
  - AC3: Vietnamese Language Rules updated: "Skill names and directories: **English**, lowercase, hyphenated"
  - AC4: Commands Reference table removed
- Blocked By: `US-10.4.1`

---

### Epic 10.5: Clean Up Legacy Artifacts

**US-10.5.1: Remove shared-agents directory**
- Description: As a developer, I need the legacy `shared-agents/` directory under `.github/skills/` removed since all agents now live in `.github/agents/` per Phase 9 migration.
- Acceptance Criteria:
  - AC1: `.github/skills/shared-agents/` directory deleted
  - AC2: `agent-protocol.md` moved to `.github/agents/` (if still needed)
  - AC3: No remaining references to `shared-agents/` path in any file
- Blocked By: `None`

**US-10.5.2: Remove duplicate agent files**
- Description: As a developer, I need any duplicate agent definition files cleaned up — old `shared-agents/*.md` copies removed, only `.github/agents/*.agent.md` files remain.
- Acceptance Criteria:
  - AC1: No agent definitions exist in `shared-agents/` (directory deleted in US-10.5.1)
  - AC2: All agent invocations in skills reference `.github/agents/` path
  - AC3: No stale `runSubagent` references pointing to old agent locations
- Blocked By: `US-10.5.1`

---

### Epic 10.6: Backfill Missing Skill Stories

**US-10.6.1: design skill user story (formerly thiet-ke)**
- Description: As a user, I want a `design` skill that creates professional visual designs programmatically (cover pages, posters, certificates, banners, infographic layouts) using reportlab Canvas and Pillow with 80+ bundled fonts.
- Acceptance Criteria:
  - AC1: `.github/skills/design/SKILL.md` exists with English name and natural language triggers
  - AC2: Supports at least: cover pages, posters, certificates, banners
  - AC3: Uses reportlab Canvas + Pillow for rendering
  - AC4: Output: PNG or PDF
  - AC5: Prints output file path + size
- Blocked By: `US-10.1.1`

**US-10.6.2: verify skill user story (formerly kiem-tra)**
- Description: As a user, I want a `verify` skill that audits InsightEngine output against my original requirements — checking requirement coverage, URL quality, field completeness, and data specificity.
- Acceptance Criteria:
  - AC1: `.github/skills/verify/SKILL.md` exists with English name and natural language triggers
  - AC2: Reads output content and opens URLs to verify accuracy
  - AC3: Compares data against actual web pages (intelligence-driven, not just rule-based)
  - AC4: Works standalone or as Step 4.7 in synthesize pipeline
  - AC5: Returns structured findings with pass/fail per criterion
- Blocked By: `US-10.1.1`

**US-10.6.3: improve skill user story (formerly cai-tien)**
- Description: As a user, I want an `improve` skill that performs session retrospective — analyzing the work session (input → process → output → gaps), identifying root causes, and proposing/executing improvements to skills and pipeline.
- Acceptance Criteria:
  - AC1: `.github/skills/improve/SKILL.md` exists with English name and natural language triggers
  - AC2: Analyzes complete session: user request, intermediate steps, final output, quality gaps
  - AC3: Identifies root causes for quality issues
  - AC4: Proposes actionable improvements (skill modifications, new skills, process changes)
  - AC5: Can create or modify skills based on findings (with user consent)
- Blocked By: `US-10.1.1`

---

### Epic 10.7: Product Doc Alignment

**US-10.7.1: Update instructions.md Vietnamese Language Rules**
- Description: As Copilot, I need `.github/instructions/insight-engine.instructions.md` updated so the Vietnamese Language Rules section reflects English skill naming convention.
- Acceptance Criteria:
  - AC1: "Skill names and directories: **English**, lowercase, hyphenated" (was Vietnamese)
  - AC2: Skill System section uses English names in the directory listing
  - AC3: All skill descriptions reference English names
- Blocked By: `US-10.1.1`

**US-10.7.2: Final cross-document consistency check**
- Description: As a product maintainer, I need all 4 product documents (idea.md, roadmap.md, user-stories.md, checklist.md) verified for consistent naming, counts, and references after Phase 10 updates.
- Acceptance Criteria:
  - AC1: idea.md ↔ roadmap.md: Phase count and epic names match
  - AC2: roadmap.md ↔ user-stories.md: All epics have corresponding stories
  - AC3: user-stories.md ↔ checklist.md: Story count and IDs match
  - AC4: No Vietnamese skill names remain in product documentation (except in historical DONE story descriptions)
- Blocked By: `US-10.7.1`

---

---

## Tổng quan User Stories (Tiếng Việt)

- **Tên sản phẩm:** InsightEngine
- **Product slug:** `insight-engine`
- **Phạm vi:** Phase 0 → Phase 10
- **Tổng số User Stories:** 91 (21 Phase 0-3 + 15 Phase 4 + 4 Phase 5 + 14 Phase 6 + 5 Phase 7 + 6 Phase 8 + 12 Phase 9 + 14 Phase 10)

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

## Phase 4: Nâng cấp — Template Library, Presentation HTML & Script Architecture

> **Nguồn gốc:** Phản hồi từ testing Phase 0-3 — output còn sơ sài, slide đơn giản, HTML thiếu tương tác.

---

### Epic 4.1: Template Library PPTX

**US-4.1.1: Thư viện template PPTX chuyên nghiệp**
- Mô tả: Xây dựng 8-10 template PPTX chuyên nghiệp với scripts/ CLI.
- Tiêu chí nghiệm thu:
  - AC1: 8-10 template scripts trong `tao-slide/scripts/`
  - AC2: Templates gồm: title, content, two-column, image+text, chart, section divider, closing
  - AC3: Mỗi template có color scheme, font pairing, spacing nhất quán
  - AC4: Tất cả template tạo file .pptx hợp lệ qua pptxgenjs
- Bị chặn bởi: `US-1.4.1`, `US-3.3.1`
- Tham khảo: slidemembers.com, aippt.com, canva.com

**US-4.1.2: Preview và chọn template**
- Mô tả: User có thể xem danh sách template và chọn trước khi generate.
- Tiêu chí nghiệm thu:
  - AC1: Liệt kê templates với mô tả
  - AC2: Preview images (PNG) trong `tao-slide/references/previews/`
  - AC3: Auto-select dựa trên content type
- Bị chặn bởi: `US-4.1.1`

**US-4.1.3: Kiến trúc script cho tao-slide**
- Mô tả: `tao-slide` dùng scripts/ thực thi để render template — đáng tin cậy, lặp lại được.
- Tiêu chí nghiệm thu:
  - AC1: `tao-slide/scripts/` chứa Node.js CLI tools
  - AC2: Mỗi template là script độc lập nhận JSON data → .pptx
  - AC3: SKILL.md làm router — xác định template, chuẩn bị data, gọi script
  - AC4: Scripts nhận CLI arguments, không hardcode path
- Bị chặn bởi: `US-4.1.1`
- Tham khảo: a-z-copilot-flow/skills/pptx/scripts/

---

### Epic 4.2: HTML Presentation Mode (reveal.js)

**US-4.2.1: Tích hợp reveal.js cho tao-html**
- Mô tả: HTML output là presentation tương tác, không phải trang tĩnh.
- Tiêu chí nghiệm thu:
  - AC1: `tao-html` tạo reveal.js presentations
  - AC2: Content tổ chức thành slides
  - AC3: reveal.js qua CDN (không cần cài local)
  - AC4: Output là single .html file portable
  - AC5: Keyboard navigation hoạt động
- Bị chặn bởi: `US-2.4.1`, `US-3.3.1`
- Tham khảo: revealjs.com, slides.com/templates

**US-4.2.2: Hiệu ứng chuyển đổi và animation**
- Mô tả: HTML presentations có transitions mượt mà và animations chuyên nghiệp.
- Tiêu chí nghiệm thu:
  - AC1: Ít nhất 3 loại transition (slide, fade, zoom)
  - AC2: Fragment animations cho bullet points
  - AC3: Background images/gradients mỗi slide
  - AC4: Syntax highlighting cho technical slides
- Bị chặn bởi: `US-4.2.1`
- Tham khảo: revealjs.com, deckdeckgo.com

**US-4.2.3: Themes và backgrounds cho HTML presentation**
- Mô tả: HTML presentations có theme chuyên nghiệp với background ấn tượng.
- Tiêu chí nghiệm thu:
  - AC1: Ít nhất 5 reveal.js themes
  - AC2: Custom background: solid, gradient, image, video
  - AC3: Typography, link colors, table styles nhất quán
  - AC4: Dark và light variants
- Bị chặn bởi: `US-4.2.1`
- Tham khảo: slides.com/templates, deckdeckgo.com

---

### Epic 4.3: Script Architecture cho Skills

**US-4.3.1: scripts/ cho tao-slide**
- Mô tả: `tao-slide` có `scripts/` với Node.js CLI tools modular.
- Tiêu chí nghiệm thu:
  - AC1: `tao-slide/scripts/` tồn tại với ít nhất 3 scripts
  - AC2: `gen_slide.js` — entry point nhận JSON → .pptx
  - AC3: `templates/` subfolder với configs cho từng template
  - AC4: `references/` có pptxgenjs API reference
- Bị chặn bởi: `US-4.1.3`
- Tham khảo: a-z-copilot-flow/skills/pptx/scripts/

**US-4.3.2: scripts/ cho tao-html**
- Mô tả: `tao-html` có `scripts/` với Python CLI tools cho reveal.js generation.
- Tiêu chí nghiệm thu:
  - AC1: `tao-html/scripts/` tồn tại với ít nhất 2 scripts
  - AC2: `gen_reveal.py` — entry point nhận content JSON → .html
  - AC3: `templates/` subfolder với jinja2 reveal.js templates
  - AC4: Scripts nhận CLI arguments, in output path + size
- Bị chặn bởi: `US-4.2.1`

**US-4.3.3: Script architecture cho tao-word, tao-excel, tao-pdf**
- Mô tả: Tất cả output skills theo cùng pattern scripts/.
- Tiêu chí nghiệm thu:
  - AC1: `tao-word/scripts/gen_docx.py` với CLI
  - AC2: `tao-excel/scripts/gen_xlsx.py` với CLI
  - AC3: `tao-pdf/scripts/gen_pdf.py` với CLI
  - AC4: Tất cả nhận JSON input + output path
- Bị chặn bởi: `US-4.3.1`, `US-4.3.2`

---

### Epic 4.4: Nâng cấp Content Depth

**US-4.4.1: bien-soan comprehensive mode**
- Mô tả: Chế độ "comprehensive" tạo nội dung phong phú gấp 3-5 lần mặc định.
- Tiêu chí nghiệm thu:
  - AC1: Hỗ trợ `--mode=comprehensive`
  - AC2: Nội dung phong phú gấp 3-5 lần default
  - AC3: Thêm sub-sections, ví dụ, data points
  - AC4: Tạo section summaries và key takeaways
- Bị chặn bởi: `US-1.2.1`, `US-3.2.1`

**US-4.4.2: Tự động làm giàu nội dung từ web**
- Mô tả: Pipeline tự search web bổ sung khi source material quá mỏng.
- Tiêu chí nghiệm thu:
  - AC1: Phát hiện khi source content không đủ
  - AC2: Tự trigger `thu-thap` web search
  - AC3: Nội dung bổ sung có source citations
  - AC4: User có thể tắt auto-enrichment
- Bị chặn bởi: `US-2.1.1`, `US-4.4.1`

---

### Epic 4.5: Template Library HTML

**US-4.5.1: Thư viện template HTML reveal.js**
- Mô tả: 5-8 template HTML presentation dựa trên reveal.js.
- Tiêu chí nghiệm thu:
  - AC1: 5-8 template files trong `tao-html/scripts/templates/`
  - AC2: Templates: corporate-formal, academic-research, tech-dark, creative-colorful, minimal-clean
  - AC3: Mỗi template định nghĩa color scheme, fonts, transitions, background
  - AC4: Tất cả tạo .html files hợp lệ, self-contained
- Bị chặn bởi: `US-4.2.1`, `US-4.2.3`
- Tham khảo: slides.com/templates, deckdeckgo.com

**US-4.5.2: Presenter notes và PDF export**
- Mô tả: HTML presentations có speaker notes và export được PDF.
- Tiêu chí nghiệm thu:
  - AC1: Speaker notes qua `<aside class="notes">`
  - AC2: `bien-soan` tạo speaker notes từ synthesis content
  - AC3: PDF export qua reveal.js print stylesheet
- Bị chặn bởi: `US-4.5.1`
- Tham khảo: revealjs.com (speaker view, PDF export)

---

## Phase 5: Tối ưu & Độ bền

### Epic 5.1: Small Model Optimization

**US-5.1.1: Nghiên cứu tương thích model nhỏ**
- Mô tả: Xác định tại sao skills hoạt động kém với model nhỏ.
- Tiêu chí nghiệm thu:
  - AC1: Mỗi SKILL.md test với model nhỏ
  - AC2: Document failure patterns
  - AC3: Xác định top 3 nguyên nhân gốc
- Bị chặn bởi: `None`

**US-5.1.2: Refactor SKILL.md cho model nhỏ**
- Mô tả: SKILL.md ≤ 300 dòng, instructions rõ ràng, nội dung dài chuyển sang references/.
- Bị chặn bởi: `US-5.1.1`

### Epic 5.2: Session State Persistence

**US-5.2.1: Lưu state sau mỗi bước pipeline**
- Mô tả: Pipeline lưu `tmp/.session-state.json` sau mỗi sub-skill hoàn thành.
- Bị chặn bởi: `None`

**US-5.2.2: Resume pipeline từ state đã lưu**
- Mô tả: User nói "tiếp tục" / "resume" → pipeline khôi phục từ checkpoint.
- Bị chặn bởi: `US-5.2.1`

---

## Phase 6: Agent Architecture & Quality Gates

### Epic 6.1: Strict File Rules & Auto-escalation

**US-6.1.1: Enforce quy tắc vị trí file bắt buộc**
- Mô tả: Scripts → `/scripts`, file tạm → `/tmp`, output → `/output`. Áp dụng tất cả skills.
- Bị chặn bởi: `None`

**US-6.1.2: Auto-escalation protocol**
- Mô tả: Khi tool fail → tự nâng tool mạnh hơn, không hỏi user câu hỏi kỹ thuật.
- Bị chặn bởi: `US-6.1.1`

### Epic 6.2: Shared Context Protocol

**US-6.2.1: Thiết kế shared context file**
- Mô tả: `tmp/.agent-context.json` cho giao tiếp giữa các agent.
- Bị chặn bởi: `None`

**US-6.2.2: Protocol đọc/ghi context cho agent**
- Mô tả: Mỗi agent đọc context trước, ghi kết quả sau.
- Bị chặn bởi: `US-6.2.1`

### Epic 6.3: Model Profile & Decision Maps

**US-6.3.1: Bản đồ quyết định theo category năng lực**
- Mô tả: Decision maps cho 5 categories, mỗi category 3 levels, có workflow recommendations.
- Bị chặn bởi: `None`

**US-6.3.2: Model tự nhận diện + fallback**
- Mô tả: Model self-declare → verify bằng decision maps → fallback medium nếu không nhận diện được.
- Bị chặn bởi: `US-6.3.1`, `US-6.2.1`

**US-6.3.3: Workflow templates sẵn có**
- Mô tả: Ít nhất 5 templates cho scenarios phổ biến × mức năng lực model.
- Bị chặn bởi: `US-6.3.1`

### Epic 6.4: Agent Strategist

**US-6.4.1: Strategist tạo dynamic workflow**
- Mô tả: Nhận request + model profile → tạo workflow tùy chỉnh. 1 call/pipeline.
- Bị chặn bởi: `US-6.3.2`, `US-6.3.3`, `US-6.2.1`

### Epic 6.5: Tiered Audit System

**US-6.5.1: Triển khai audit phân tầng**
- Mô tả: Tier 1 self-review (mọi step) → Tier 2 agent audit (critical) → Tier 3 final audit. Max 5 audit calls.
- Bị chặn bởi: `US-6.2.1`

**US-6.5.2: Final audit với step-level rollback**
- Mô tả: Audit final → nếu fail → xác định step lỗi → redo từ đó. Max 3 retries/step, 10 total, fail-fast.
- Bị chặn bởi: `US-6.5.1`, `US-6.4.1`

### Epic 6.6: Advisory Agent & Skill Creation

**US-6.6.1: Advisory agent đa góc nhìn**
- Mô tả: 1 call phân tích 3-5 perspectives → recommendation. Max 2 calls/pipeline.
- Bị chặn bởi: `US-6.2.1`

**US-6.6.2: Tạo skill runtime có điều kiện**
- Mô tả: Advisory đánh giá cần thiết → nếu bắt buộc → cho phép tạo (30 phút).
- Bị chặn bởi: `US-6.6.1`

**US-6.6.3: Clone skill từ public repos + security check**
- Mô tả: Ưu tiên clone từ repos public → kiểm tra bảo mật BẮT BUỘC → dùng nếu an toàn.
- Bị chặn bởi: `US-6.6.2`

### Epic 6.7: Pipeline Integration

**US-6.7.1: Tích hợp tong-hop với feature flag AGENT_MODE**
- Mô tả: AGENT_MODE true → agent pipeline, false → current pipeline. User experience không đổi.
- Bị chặn bởi: `US-6.4.1`, `US-6.5.1`, `US-6.6.1`

---

## Phase 7: Pipeline Enforcement & Compliance Hardening

> **Nguồn gốc:** Test thực tế — model skip Step 1.5, không dùng platform-specific search, trả URL search page, không kích hoạt AGENT_MODE flow.

### Epic 7.1: Inline Critical Steps & Hard Gates

**US-7.1.1: Đưa request analysis và REQUEST_TYPE detection inline**
- Mô tả: Step 1.5 và REQUEST_TYPE detection phải nằm inline trong tong-hop SKILL.md, không ở reference files, để mọi model đều tuân thủ.
- Tiêu chí nghiệm thu:
  - AC1: Step 1.5 request analysis inline trong tong-hop SKILL.md
  - AC2: REQUEST_TYPE detection inline trong Step 1
  - AC3: Reference files chỉ chứa supplementary details
  - AC4: tong-hop SKILL.md ≤ 500 dòng
  - AC5: Test pass với GPT-4o-mini
- Bị chặn bởi: `None`

**US-7.1.2: Gate xác nhận bắt buộc trước khi thực thi**
- Mô tả: Pipeline PHẢI hiển thị phân tích cho user VÀ nhận xác nhận trước Step 3. Không xác nhận → STOP.
- Tiêu chí nghiệm thu:
  - AC1: Hiển thị phân tích Step 1.5 bằng tiếng Việt
  - AC2: Nhận xác nhận rõ ràng trước Step 3
  - AC3: Không xác nhận → pipeline STOP
  - AC4: Phân tích gồm: request_type, dimensions/fields, planned steps, content_depth
- Bị chặn bởi: `US-7.1.1`

### Epic 7.2: Data Collection Enforcement

**US-7.2.1: Inline data collection protocol trong thu-thap**
- Mô tả: Protocol thu thập dữ liệu cấu trúc (platform-specific search, fetch individual page, extract fields) nằm inline trong thu-thap SKILL.md.
- Tiêu chí nghiệm thu:
  - AC1: Protocol nằm inline trong thu-thap main body
  - AC2: Dùng `site:{platform}` khi mode=data_collection
  - AC3: Fetch individual item pages, không phải search result pages
  - AC4: Mỗi item phải có `direct_url`
- Bị chặn bởi: `None`

**US-7.2.2: URL validation gate trước khi tạo output**
- Mô tả: validate_urls.py chạy TRƯỚC khi tao-excel tạo file. URL sai → re-fetch hoặc flag.
- Tiêu chí nghiệm thu:
  - AC1: validate_urls.py chạy trước tao-excel output
  - AC2: URL SEARCH/LISTING → auto re-fetch
  - AC3: URL còn sai sau re-fetch → flag ⚠️ trong Excel
  - AC4: >50% invalid → STOP hỏi user
- Bị chặn bởi: `US-7.2.1`

### Epic 7.3: Visible Pipeline Trace

**US-7.3.1: Trace pipeline có đánh số với progress trực tiếp**
- Mô tả: Pipeline in danh sách step có đánh số ở đầu, đánh dấu ✅ từng step khi hoàn thành.
- Tiêu chí nghiệm thu:
  - AC1: In danh sách step có đánh số ở đầu pipeline
  - AC2: Mỗi step hoàn thành → ✅ + tóm tắt 1 dòng
  - AC3: Step bị skip → ⏭️ + lý do
  - AC4: Step fail → ❌ + error summary
  - AC5: Trace luôn hiển thị, không bị ẩn
- Bị chặn bởi: `None`

---

## Phase 8: Shared Copilot Agent Architecture

> **Nguồn gốc:** Phase 6 nhúng agents trong tong-hop dưới dạng inline instructions. Phase 8 tái cấu trúc thành shared Copilot agents (`runSubagent`) mà bất kỳ skill nào cũng gọi được.

### Epic 8.1: Shared Auditor Agent

**US-8.1.1: Auditor dưới dạng standalone Copilot agent**
- Mô tả: Auditor agent được gọi qua `runSubagent` từ bất kỳ skill nào, kiểm tra chất lượng output tại mọi điểm tạo file.
- Tiêu chí nghiệm thu:
  - AC1: Auditor agent tồn tại dưới dạng standalone prompt/agent definition
  - AC2: Nhận: nội dung file + yêu cầu gốc của user
  - AC3: Trả verdict: PASS/FAIL + danh sách issues + gợi ý cải thiện
  - AC4: Gọi được qua `runSubagent` từ mọi skill
  - AC5: Đọc lại nội dung file và so sánh với yêu cầu
- Bị chặn bởi: `None`

**US-8.1.2: Tích hợp auditor vào output skills**
- Mô tả: Mọi output skill (tao-word, tao-excel, tao-slide, tao-pdf, tao-html) tự động gọi auditor sau khi tạo file.
- Tiêu chí nghiệm thu:
  - AC1: tao-word gọi auditor sau khi tạo .docx
  - AC2: tao-excel gọi auditor sau khi tạo .xlsx
  - AC3: tao-slide gọi auditor sau khi tạo .pptx
  - AC4: tao-pdf và tao-html gọi auditor tương tự
  - AC5: Auditor FAIL → skill tạo lại (tối đa 2 lần retry)
  - AC6: Budget: tối đa 5 lần gọi auditor / pipeline
- Bị chặn bởi: `US-8.1.1`

### Epic 8.2: Shared Strategist Agent

**US-8.2.1: Strategist dưới dạng standalone Copilot agent**
- Mô tả: Refactor strategist từ inline trong tong-hop → standalone `runSubagent` agent.
- Tiêu chí nghiệm thu:
  - AC1: Strategist agent tồn tại dưới dạng standalone definition
  - AC2: Nhận: user request + model profile
  - AC3: Trả: workflow plan từng bước với skill assignments
  - AC4: Chọn từ workflow templates có sẵn
  - AC5: tong-hop gọi qua `runSubagent`
  - AC6: Budget: tối đa 1 lần gọi / pipeline
- Bị chặn bởi: `None`

### Epic 8.3: Shared Advisory Agent

**US-8.3.1: Advisory dưới dạng standalone Copilot agent**
- Mô tả: Refactor advisory → standalone `runSubagent` agent. Bất kỳ skill nào cũng gọi được khi cần tư vấn.
- Tiêu chí nghiệm thu:
  - AC1: Advisory agent tồn tại dưới dạng standalone definition
  - AC2: Nhận: câu hỏi quyết định + context → trả phân tích 3-5 góc nhìn + khuyến nghị
  - AC3: Bất kỳ skill nào đều gọi được
  - AC4: Gọi 1 lần duy nhất (không tách nhiều lần gọi cho mỗi góc nhìn)
  - AC5: Budget: tối đa 2 lần gọi / pipeline
- Bị chặn bởi: `None`

### Epic 8.4: Agent Integration Protocol

**US-8.4.1: Chuẩn hóa protocol gọi agent**
- Mô tả: Protocol chuẩn cho cách skills gọi agents, đảm bảo mọi tương tác nhất quán.
- Tiêu chí nghiệm thu:
  - AC1: Tài liệu input format cho từng agent
  - AC2: Tài liệu output format — cách parse response
  - AC3: Budget enforcement: auditor 5/pipeline, advisory 2, strategist 1
  - AC4: Protocol tài liệu hóa trong `references/agent-protocol.md`
- Bị chặn bởi: `US-8.1.1`, `US-8.2.1`, `US-8.3.1`

**US-8.4.2: Migration tong-hop sang shared agents**
- Mô tả: tong-hop delegate cho shared agents thay vì dùng inline agent logic.
- Tiêu chí nghiệm thu:
  - AC1: tong-hop gọi strategist agent cho workflow generation
  - AC2: tong-hop gọi auditor agent cho verification
  - AC3: Xóa AGENT_MODE feature flag — agents luôn khả dụng
  - AC4: tong-hop SKILL.md giảm complexity (bỏ inline agent personas)
  - AC5: Không regression — cùng user experience, chất lượng tốt hơn
- Bị chặn bởi: `US-8.4.1`

---

## Phase 9: Central Orchestrator & Adaptive Self-Improvement

> Tách orchestration khỏi tổng hợp nội dung. Tạo agent trung tâm, tự cải thiện thích ứng, audit thang 100 điểm, resume xuyên session, chuẩn hóa agents theo VS Code custom agent standard (`.github/agents/*.agent.md`).

### Epic 9.1: Central Orchestrator (`dieu-phoi`)

**US-9.1.1: Agent điều phối trung tâm**
- Mô tả: Tạo `dieu-phoi.agent.md` trong `.github/agents/` phân loại intent và route đến skills/agents phù hợp.
- Tiêu chí nghiệm thu:
  - AC1: `dieu-phoi.agent.md` tồn tại với YAML frontmatter đúng chuẩn VS Code
  - AC2: Phân loại intent: synthesis, creation, research, design, data_collection, mixed, unknown
  - AC3: Route đúng skill/agent theo phân loại
  - AC4: Fallback hỏi user khi intent `unknown`
  - AC5: Log classification + routing vào session state
- Bị chặn bởi: `US-8.4.2`

**US-9.1.2: Refactor tong-hop thành skill tổng hợp thuần túy**
- Mô tả: Loại bỏ logic orchestration khỏi tong-hop, chỉ giữ tổng hợp nội dung.
- Tiêu chí nghiệm thu:
  - AC1: tong-hop chỉ chứa logic tổng hợp (gather → merge → structure)
  - AC2: Logic routing và orchestration đã chuyển sang dieu-phoi
  - AC3: Trigger `/tong-hop` vẫn hoạt động (dieu-phoi intercept và route)
  - AC4: Không giảm chất lượng tổng hợp
- Bị chặn bởi: `US-9.1.1`

**US-9.1.3: Tích hợp dieu-phoi với shared agents**
- Mô tả: dieu-phoi gọi strategist, auditor, advisory qua VS Code agent handoffs.
- Tiêu chí nghiệm thu:
  - AC1: YAML frontmatter liệt kê `agents: [strategist, auditor, advisory]`
  - AC2: Gọi strategist cho workflow generation
  - AC3: Gọi auditor cho quality gate cuối pipeline
  - AC4: Budget enforcement: strategist 1, auditor 5, advisory 2 / pipeline
- Bị chặn bởi: `US-9.1.1`

### Epic 9.2: Tự cải thiện thích ứng

**US-9.2.1: Đánh giá gap năng lực**
- Mô tả: dieu-phoi đánh giá skills/agents hiện có đủ đáp ứng yêu cầu không trước khi thực thi.
- Tiêu chí nghiệm thu:
  - AC1: Map yêu cầu → skills/agents có sẵn
  - AC2: Xác định gap cụ thể
  - AC3: Báo cáo gap cho user với giải pháp đề xuất
  - AC4: Tiếp tục với năng lực hiện có nếu user từ chối
- Bị chặn bởi: `US-9.1.1`

**US-9.2.2: Tạo agent runtime với user consent**
- Mô tả: Tạo agent chuyên biệt tại runtime khi phát hiện gap, với sự đồng ý user.
- Tiêu chí nghiệm thu:
  - AC1: Đề xuất tạo agent mới với mô tả mục đích
  - AC2: User phải approve trước khi tạo
  - AC3: Agent theo đúng `.agent.md` format
  - AC4: Smoke test trước khi sử dụng
  - AC5: Thông báo thời gian >30 phút, user có thể "unlock" để tiếp
- Bị chặn bởi: `US-9.2.1`

**US-9.2.3: Tạo/nâng cấp skill runtime**
- Mô tả: Tạo hoặc nâng cấp skill khi skill hiện tại không đủ đáp ứng.
- Tiêu chí nghiệm thu:
  - AC1: Đề xuất tạo/nâng cấp với lý do
  - AC2: User approve; skill theo SKILL.md standard
  - AC3: Đăng ký trong copilot-instructions.md
  - AC4: Smoke test trước khi dùng
- Bị chặn bởi: `US-9.2.1`

### Epic 9.3: Working State & Resume xuyên session

**US-9.3.1: Schema session state nâng cao**
- Mô tả: Lưu đủ context (raw_prompt, analyzed_requirements, generated_plan, step_states[], audit_test_cases[], score_history[], created_skills[]).
- Tiêu chí nghiệm thu:
  - AC1: Schema được tài liệu hóa đầy đủ
  - AC2: `save_state.py` cập nhật hỗ trợ schema mới
  - AC3: Tracking hash output file cho conflict detection
  - AC4: Tương thích ngược với Phase 5 format
- Bị chặn bởi: `US-5.2.1`

**US-9.3.2: Lưu state sau mỗi step**
- Mô tả: State persist sau mỗi sub-skill, không chỉ ở checkpoint.
- Tiêu chí nghiệm thu:
  - AC1: Lưu state sau mỗi sub-skill hoàn thành
  - AC2: Ghi input, output summary, status từng step
  - AC3: Audit test cases và scores persist theo step
  - AC4: Resume xác định đúng step cuối cùng hoàn thành
- Bị chặn bởi: `US-9.3.1`

**US-9.3.3: Resume xuyên session**
- Mô tả: Load state từ session trước và tiếp tục pipeline mà không cần làm lại.
- Tiêu chí nghiệm thu:
  - AC1: dieu-phoi detect state đã lưu và đề nghị resume
  - AC2: Full context reconstructed từ state
  - AC3: Kiểm tra hash output file cho conflict
  - AC4: User chọn resume hoặc bắt đầu mới
- Bị chặn bởi: `US-9.3.2`

### Epic 9.4: Audit thang 100 điểm

**US-9.4.1: Hệ thống chấm điểm 100**
- Mô tả: Auditor tạo bộ test case động từ yêu cầu (100 điểm, trọng số), thay thế PASS/FAIL.
- Tiêu chí nghiệm thu:
  - AC1: Phân tích yêu cầu → tạo bộ test case (tổng weight = 100)
  - AC2: Mỗi test case có: tên, weight, pass criteria, category
  - AC3: Categories: requirement_coverage (40%), data_quality (25%), format_compliance (20%), completeness (15%)
  - AC4: Score đầu ra /100, pass threshold >80
  - AC5: Score breakdown hiển thị cho user
- Bị chặn bởi: `US-8.1.1`

**US-9.4.2: Vòng retry nhắm mục tiêu với score tracking**
- Mô tả: Retry chỉ nhắm vào test case điểm thấp, không tạo lại toàn bộ.
- Tiêu chí nghiệm thu:
  - AC1: Score <80 → xác định test case điểm 0
  - AC2: Retry chỉ sửa vùng lỗi
  - AC3: Tối đa 5 retries / pipeline
  - AC4: Score progression tracking: [lần 1: 62, lần 2: 78, lần 3: 85]
  - AC5: Nếu điểm không tăng 2 lần liên tiếp → dừng và báo user
- Bị chặn bởi: `US-9.4.1`

### Epic 9.5: Chuẩn VS Code Custom Agent

**US-9.5.1: Migrate agents sang .agent.md**
- Mô tả: Chuyển auditor, strategist, advisory từ shared-agents sang `.github/agents/*.agent.md`.
- Tiêu chí nghiệm thu:
  - AC1: `auditor.agent.md` trong `.github/agents/` với user-invocable: true
  - AC2: `strategist.agent.md` với user-invocable: false
  - AC3: `advisory.agent.md` với user-invocable: false
  - AC4: Cập nhật references từ shared-agents sang .github/agents
  - AC5: Cập nhật copilot-instructions.md với agent registry
- Bị chặn bởi: `US-8.1.1`, `US-8.2.1`, `US-8.3.1`

---

*Backlog này không bao gồm task-level detail hoặc trạng thái thực hiện.*
*Bước tiếp theo: `/roadmap-to-user-stories-review` hoặc `/product-checklist`*
