# InsightEngine — Product Roadmap

> **Product:** InsightEngine  
> **Product Slug:** insight-engine  
> **Roadmap Created:** 2026-04-16  
> **Scope:** Milestone-based (Phase 0 → Phase 3)

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

## Skill Map theo Phase

```
Phase 0:  cai-dat (MỚI)     tong-hop (skeleton)
Phase 1:  thu-thap          bien-soan          tao-word     tao-slide
Phase 2:  thu-thap (nâng)   tao-excel          tao-pdf      tao-html   tong-hop (chaining)
Phase 3:  tao-hinh (MỚI)    bien-soan (nâng)   tao-slide (nâng)  tong-hop (nâng)
```

**Tổng số skills:** 10 (9 đã thiết kế + 1 mới `cai-dat`)

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

*Roadmap này không bao gồm task-level breakdown. Xem User Stories để biết chi tiết triển khai.*  
*Bước tiếp theo: `/product-roadmap-review` hoặc `/roadmap-to-user-stories`*
