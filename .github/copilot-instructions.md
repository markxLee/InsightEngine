# Copilot Instructions — InsightEngine

<!-- Version: 1.2 | Product: insight-engine | Updated: 2026-04-16 -->

This file is read automatically by GitHub Copilot.
It defines how Copilot MUST behave in this workspace.

---

## Mandatory: Respond to User in Vietnamese

```yaml
MANDATORY:
  - Always respond to the user in Vietnamese
  - Ask and confirm in Vietnamese
  - Output file names and result messages: Vietnamese
  - Exception: technical content in SKILL.md, scripts, code comments use English
```

---

## Product Context

```yaml
active_product:
  slug: insight-engine
  name: InsightEngine
  description: Multi-source content synthesis pipeline → multi-format output
  tech_stack_file: docs/tech-stack/insight-engine/instructions.md
  activated_at: 2026-04-16

COPILOT_MUST:
  - Read and follow the tech stack at docs/tech-stack/insight-engine/instructions.md
  - Use the specified libraries exactly as documented
  - Follow coding conventions defined in instructions.md
  - Communicate with the user in Vietnamese
```

---

## Available Skills

```yaml
SKILLS:
  tong-hop:
    purpose: "Main pipeline — deeply analyzes user intent, expands prompt dimensions, orchestrates sub-skills with auto-quality-review loops. Default content depth is COMPREHENSIVE (expert-level, rich). Auto-reviews each step's output and loops if quality is insufficient."
    location: ".github/skills/tong-hop/SKILL.md"
    triggers:
      - "tổng hợp nội dung"
      - "làm báo cáo"
      - "làm thuyết trình"
      - "tóm tắt từ nhiều nguồn"
      - "synthesize content"
      - "create report"
      - "create presentation"
      - "/tong-hop"

  thu-thap:
    purpose: "Gather content from web (Google search + fetch URL) and read local files. Auto-reviews gathered content quality and expands search if insufficient."
    location: ".github/skills/thu-thap/SKILL.md"
    triggers:
      - "tìm kiếm thông tin"
      - "đọc file"
      - "lấy nội dung từ"
      - "fetch URL"
      - "search web"
      - "read file"
      - "/thu-thap"

  bien-soan:
    purpose: "Synthesize multi-source content into expert-level documents (comprehensive by default). Self-reviews each section for depth, specificity, and analysis — auto-rewrites thin sections. Supports Vietnamese ↔ English translation."
    location: ".github/skills/bien-soan/SKILL.md"
    triggers:
      - "tổng hợp"
      - "gộp nội dung"
      - "dịch thuật"
      - "biên soạn"
      - "synthesize"
      - "translate"
      - "merge content"
      - "/bien-soan"

  tao-word:
    purpose: "Create professional Word (.docx) documents from synthesized content, with 3 style templates"
    location: ".github/skills/tao-word/SKILL.md"
    triggers:
      - "tạo file word"
      - "xuất word"
      - "tạo tài liệu word"
      - "tạo file .docx"
      - "create word document"
      - "export to word"
      - "/tao-word"

  tao-excel:
    purpose: "Create Excel (.xlsx) files with data, formulas, and professional formatting"
    location: ".github/skills/tao-excel/SKILL.md"
    triggers:
      - "tạo file excel"
      - "xuất excel"
      - "tạo bảng tính"
      - "tạo file .xlsx"
      - "create excel"
      - "export to excel"
      - "/tao-excel"

  tao-slide:
    purpose: "Create professional PowerPoint (.pptx) presentations. Default: Pro mode (ppt-master SVG→PPTX, native DrawingML, 20+ layouts, 50+ charts, 6700+ icons, embedded in repo). Quick mode (pptxgenjs) only when user explicitly asks for simple/fast deck"
    location: ".github/skills/tao-slide/SKILL.md"
    triggers:
      - "tạo slide"
      - "làm thuyết trình"
      - "tạo file powerpoint"
      - "tạo file .pptx"
      - "create slides"
      - "create powerpoint"
      - "make presentation"
      - "slide chuyên nghiệp"
      - "consulting-grade slides"
      - "dùng ppt-master"
      - "/tao-slide"

  tao-pdf:
    purpose: "Create PDF documents from synthesized content or converted from other formats"
    location: ".github/skills/tao-pdf/SKILL.md"
    triggers:
      - "tạo file pdf"
      - "xuất pdf"
      - "tạo file .pdf"
      - "create pdf"
      - "export to pdf"
      - "/tao-pdf"

  tao-html:
    purpose: "Create professional static HTML pages OR reveal.js presentations with 8 styles (corporate, academic, minimal, dark-modern, creative, warm-earth, dark-neon, dark-elegant)"
    location: ".github/skills/tao-html/SKILL.md"
    triggers:
      - "tạo trang web"
      - "tạo file html"
      - "tạo html"
      - "create html page"
      - "create website"
      - "static site"
      - "/tao-html"

  tao-hinh:
    purpose: "Generate charts from data and illustration images (Apple Silicon). Supports: bar, line, pie, radar, scatter"
    location: ".github/skills/tao-hinh/SKILL.md"
    triggers:
      - "tạo biểu đồ"
      - "vẽ chart"
      - "tạo hình ảnh"
      - "create chart"
      - "generate image"
      - "visualize data"
      - "/tao-hinh"

  thiet-ke:
    purpose: "Create professional visual designs programmatically — cover pages, posters, certificates, infographic layouts, banners"
    location: ".github/skills/thiet-ke/SKILL.md"
    triggers:
      - "tạo poster"
      - "thiết kế bìa"
      - "làm certificate"
      - "tạo thiệp"
      - "thiết kế cover page"
      - "tạo bằng khen"
      - "tạo banner"
      - "tạo infographic"
      - "design a poster"
      - "make a cover"
      - "/thiet-ke"
```

---

## Workflow

```yaml
PIPELINE_FLOW:
  1. User describes request (in Vietnamese)
  2. tong-hop skill analyzes intent:
     - What input sources need to be gathered?
     - What processing is required?
     - What output format is desired?
  3. tong-hop calls sub-skills in order:
     thu-thap → bien-soan → tao-[format]
  4. Copilot executes scripts via run_in_terminal
  5. Confirm result (output file path + size)

CHAINING:
  - Supports output chaining: Excel data → chart → PPT
  - Always show the chaining plan before executing
  - Intermediate files saved to tmp/ and cleaned up afterwards

STYLE_SELECTION:
  - User selects a style (corporate/academic/minimal/dark-modern/creative), or
  - Infer from context: formal → corporate, research → academic, simple → minimal, tech → dark-modern, marketing → creative
```

---

## Tech Stack (Summary)

```yaml
# Full details: docs/tech-stack/insight-engine/instructions.md
file_reading: markitdown[all]         # Convert any format → Markdown
word_output: python-docx
excel_output: openpyxl + pandas
ppt_output: pptxgenjs (Node.js)
pdf_output: reportlab + pypdf
html_output: jinja2 + inline CSS
charts: matplotlib + seaborn
images: diffusers + torch/MPS         # Apple Silicon only, optional
web_search: vscode-websearchforcopilot_webSearch
url_fetch: Copilot fetch_webpage tool
```

---

## Commands Reference

| Command | Description |
|---------|-------------|
| `/tong-hop` | Start content synthesis pipeline |
| `/thu-thap` | Gather content from sources |
| `/bien-soan` | Synthesize / translate content |
| `/tao-word` | Create Word file |
| `/tao-excel` | Create Excel file |
| `/tao-slide` | Create PowerPoint presentation |
| `/tao-pdf` | Create PDF file |
| `/tao-html` | Create HTML page |
| `/tao-hinh` | Create charts / images |

---

## See Also

- [Tech Stack Instructions](../docs/tech-stack/insight-engine/instructions.md)
- [Idea Analysis](../docs/idea/insight-engine/idea.md)

---

**Version:** 1.2
**Activated:** 2026-04-16
