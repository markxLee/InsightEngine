# InsightEngine — User Stories Backlog

> **Product:** InsightEngine  
> **Product Slug:** insight-engine  
> **Created:** 2026-04-16  
> **Scope:** Phase 0 → Phase 5 (all phases)  
> **Total User Stories:** 40 (21 Phase 0-3 + 15 Phase 4 + 4 Phase 5)

---

## User Stories Overview

- **Product name:** InsightEngine
- **Product slug:** `insight-engine`
- **Scope covered:** Phase 0, Phase 1, Phase 2, Phase 3, Phase 4, Phase 5
- **Total stories:** 40 (Phase 0: 5, Phase 1: 6, Phase 2: 5, Phase 3: 5, Phase 4: 15, Phase 5: 4)
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

---

## Tổng quan User Stories (Tiếng Việt)

- **Tên sản phẩm:** InsightEngine
- **Product slug:** `insight-engine`
- **Phạm vi:** Phase 0 → Phase 5
- **Tổng số User Stories:** 40 (21 Phase 0-3 + 15 Phase 4 + 4 Phase 5)

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

*Backlog này không bao gồm task-level detail hoặc trạng thái thực hiện.*  
*Bước tiếp theo: `/roadmap-to-user-stories-review` hoặc `/product-checklist`*
