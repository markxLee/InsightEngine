# Copilot Instructions — InsightEngine

<!-- Version: 1.0 | Product: insight-engine | Activated: 2026-04-16 -->

This file is read automatically by GitHub Copilot.
It defines how Copilot MUST behave in this workspace.

---

## Bắt buộc: Giao tiếp bằng tiếng Việt

```yaml
MANDATORY:
  - Luôn trả lời user bằng tiếng Việt
  - Hỏi và xác nhận bằng tiếng Việt
  - Tên file output, thông báo kết quả: tiếng Việt
  - Ngoại lệ: nội dung kỹ thuật trong SKILL.md, scripts, code comments dùng tiếng Anh
```

---

## Product Context

```yaml
active_product:
  slug: insight-engine
  name: InsightEngine
  description: Pipeline tổng hợp nội dung đa nguồn → đa định dạng đầu ra
  tech_stack_file: docs/tech-stack/insight-engine/instructions.md
  activated_at: 2026-04-16

COPILOT_MUST:
  - Đọc và tuân theo tech stack tại docs/tech-stack/insight-engine/instructions.md
  - Sử dụng đúng thư viện đã được chỉ định
  - Tuân theo các coding conventions trong instructions.md
  - Giao tiếp với user bằng tiếng Việt
```

---

## Available Skills

```yaml
SKILLS:
  tong-hop:
    purpose: "Pipeline chính — nhận yêu cầu, phân tích intent, điều phối các skill con để hoàn thành tác vụ tổng hợp nội dung / Main pipeline — orchestrates all sub-skills based on user intent"
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
    purpose: "Thu thập nội dung từ web (search Google + fetch URL) và đọc file cục bộ (docx, xlsx, pdf, pptx, txt) / Gather content from web and local files"
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
    purpose: "Tổng hợp, gộp, và biên soạn nội dung từ nhiều nguồn. Hỗ trợ dịch thuật Việt ↔ Anh / Synthesize and merge multi-source content, with translation support"
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
    purpose: "Tạo file Word (.docx) chuyên nghiệp từ nội dung đã tổng hợp, với 3 template style / Create professional Word documents with 3 style templates"
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
    purpose: "Tạo file Excel (.xlsx) với dữ liệu, công thức, và định dạng chuyên nghiệp / Create Excel spreadsheets with data, formulas, and professional formatting"
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
    purpose: "Tạo bài thuyết trình PowerPoint (.pptx) chuyên nghiệp với nhiều style template / Create professional PowerPoint presentations with style templates"
    location: ".github/skills/tao-slide/SKILL.md"
    triggers:
      - "tạo slide"
      - "làm thuyết trình"
      - "tạo file powerpoint"
      - "tạo file .pptx"
      - "create slides"
      - "create powerpoint"
      - "make presentation"
      - "/tao-slide"

  tao-pdf:
    purpose: "Tạo file PDF từ nội dung đã tổng hợp hoặc chuyển đổi từ định dạng khác / Create PDF documents from synthesized content or converted from other formats"
    location: ".github/skills/tao-pdf/SKILL.md"
    triggers:
      - "tạo file pdf"
      - "xuất pdf"
      - "tạo file .pdf"
      - "create pdf"
      - "export to pdf"
      - "/tao-pdf"

  tao-html:
    purpose: "Tạo trang HTML tĩnh chuyên nghiệp với 3 style template (corporate, academic, minimal) / Create professional static HTML pages with 3 style templates"
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
    purpose: "Tạo biểu đồ từ dữ liệu và hình ảnh minh họa (Apple Silicon). Hỗ trợ: bar, line, pie, radar, scatter chart / Generate charts from data and illustration images"
    location: ".github/skills/tao-hinh/SKILL.md"
    triggers:
      - "tạo biểu đồ"
      - "vẽ chart"
      - "tạo hình ảnh"
      - "create chart"
      - "generate image"
      - "visualize data"
      - "/tao-hinh"
```

---

## Workflow

```yaml
PIPELINE_FLOW:
  1. User mô tả yêu cầu bằng tiếng Việt
  2. tong-hop skill phân tích intent:
     - Nguồn đầu vào cần thu thập?
     - Loại xử lý cần thực hiện?
     - Định dạng đầu ra mong muốn?
  3. tong-hop gọi các skill con theo thứ tự:
     thu-thap → bien-soan → tao-[format]
  4. Copilot thực thi script qua run_in_terminal
  5. Xác nhận kết quả (đường dẫn + kích thước file)

CHAINING:
  - Hỗ trợ chuỗi output: Excel data → chart → PPT
  - Luôn hiển thị kế hoạch chuỗi trước khi thực hiện
  - File trung gian lưu vào tmp/ và dọn dẹp sau

STYLE_SELECTION:
  - User chọn style (corporate/academic/minimal) hoặc
  - Tự suy luận từ context: formal → corporate, research → academic, simple → minimal
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

| Lệnh | Mô tả |
|------|-------|
| `/tong-hop` | Bắt đầu pipeline tổng hợp |
| `/thu-thap` | Thu thập nội dung |
| `/bien-soan` | Biên soạn/dịch thuật nội dung |
| `/tao-word` | Tạo file Word |
| `/tao-excel` | Tạo file Excel |
| `/tao-slide` | Tạo bài thuyết trình |
| `/tao-pdf` | Tạo file PDF |
| `/tao-html` | Tạo trang HTML |
| `/tao-hinh` | Tạo biểu đồ/hình ảnh |

---

## See Also

- [Tech Stack Instructions](../docs/tech-stack/insight-engine/instructions.md)
- [Idea Analysis](../docs/idea/insight-engine/idea.md)

---

**Version:** 1.0  
**Activated:** 2026-04-16
