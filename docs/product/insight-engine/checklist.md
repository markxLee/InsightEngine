# InsightEngine — Product Checklist

> **Product:** InsightEngine  
> **Product Slug:** insight-engine  
> **Created:** 2026-04-16  
> **Total User Stories:** 97 (21 Phase 0-3 DONE + 15 Phase 4 DONE + 4 Phase 5 DONE + 14 Phase 6 DONE + 5 Phase 7 DONE + 6 Phase 8 DONE + 12 Phase 9 DONE + 13 Phase 10 DONE + 1 Phase 10 PLANNED + 6 Phase 11 PLANNED)  
> **Purpose:** Single source of execution state — track progress, enforce dependencies, enable safe parallel work

---

## Product Checklist Overview

- **Product name:** InsightEngine
- **Product slug:** `insight-engine`
- **Checklist purpose:** Track execution state of all user stories across phases, enforce dependency rules, enable pause/resume

### Status Legend

| Status | Meaning |
|--------|---------|
| PLANNED | Not started |
| IN_PROGRESS | Currently being implemented |
| DONE | Completed and verified |

### Rules

- A story may move to IN_PROGRESS **only** if all stories in its "Blocked By" list are DONE
- Stories with `Blocked By: None` can start immediately

---

## Phase 0: Product Foundation

### Epic 0.1: Workspace Setup

- [x] **US-0.1.1** — Repo structure & Copilot configuration
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-0.1.1
  - Blocked By: None

### Epic 0.2: Cài đặt môi trường (`cai-dat`)

- [x] **US-0.2.1** — Dependency check script
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-0.2.1
  - Blocked By: None

- [x] **US-0.2.2** — Setup skill (`cai-dat`)
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-0.2.2
  - Blocked By: ~~US-0.2.1~~ ✅

### Epic 0.3: Pipeline Chính (`tong-hop`)

- [x] **US-0.3.1** — Pipeline skill skeleton with intent routing
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-0.3.1
  - Blocked By: ~~US-0.1.1~~ ✅, ~~US-0.2.2~~ ✅

- [x] **US-0.3.2** — Setup check before each pipeline process
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-0.3.2
  - Blocked By: ~~US-0.3.1~~ ✅

---

## Phase 1: MVP — Thu thập & Xuất cơ bản

### Epic 1.1: Thu thập nội dung (`thu-thap`)

- [x] **US-1.1.1** — Read local files via markitdown
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-1.1.1
  - Blocked By: ~~US-0.3.2~~ ✅

- [x] **US-1.1.2** — Fetch URL content
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-1.1.2
  - Blocked By: ~~US-1.1.1~~ ✅

### Epic 1.2: Biên soạn nội dung (`bien-soan`)

- [x] **US-1.2.1** — Multi-source content synthesis
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-1.2.1
  - Blocked By: ~~US-0.3.2~~ ✅

- [x] **US-1.2.2** — Basic translation Vietnamese ↔ English
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-1.2.2
  - Blocked By: ~~US-1.2.1~~ ✅

### Epic 1.3: Xuất Word (`tao-word`)

- [x] **US-1.3.1** — Word document output with 3 template styles
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-1.3.1
  - Blocked By: ~~US-1.2.1~~ ✅, ~~US-1.1.1~~ ✅

### Epic 1.4: Xuất PowerPoint (`tao-slide`)

- [x] **US-1.4.1** — PowerPoint output with 3 template styles
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-1.4.1
  - Blocked By: ~~US-1.2.1~~ ✅, ~~US-1.1.1~~ ✅

---

## Phase 2: Mở rộng — Tìm kiếm & Thêm định dạng

### Epic 2.1: Tìm kiếm Google tự động

- [x] **US-2.1.1** — Web search integration in thu-thap
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-2.1.1
  - Blocked By: ~~US-1.1.1~~ ✅

### Epic 2.2: Xuất Excel (`tao-excel`)

- [x] **US-2.2.1** — Excel output with formulas and formatting
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-2.2.1
  - Blocked By: ~~US-1.2.1~~ ✅

### Epic 2.3: Xuất PDF (`tao-pdf`)

- [x] **US-2.3.1** — PDF output from synthesized content
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-2.3.1
  - Blocked By: ~~US-1.2.1~~ ✅

### Epic 2.4: Xuất HTML (`tao-html`)

- [x] **US-2.4.1** — Static HTML page output with 3 template styles
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-2.4.1
  - Blocked By: ~~US-1.2.1~~ ✅

### Epic 2.5: Chaining Output

- [x] **US-2.5.1** — Pipeline output chaining
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-2.5.1
  - Blocked By: ~~US-1.3.1~~ ✅, ~~US-1.4.1~~ ✅, ~~US-2.2.1~~ ✅

---

## Phase 3: Hoàn thiện — Trực quan & Tối ưu

### Epic 3.1: Biểu đồ & Hình ảnh (`tao-hinh`)

- [x] **US-3.1.1** — Chart generation from data
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-3.1.1
  - Blocked By: ~~US-2.2.1~~ ✅

- [x] **US-3.1.2** — Image generation for slides (Apple Silicon)
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-3.1.2
  - Blocked By: ~~US-3.1.1~~ ✅

### Epic 3.2: Xử lý tài liệu lớn

- [x] **US-3.2.1** — Large document chunking strategy
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-3.2.1
  - Blocked By: ~~US-1.2.1~~ ✅

### Epic 3.3: Template Library mở rộng

- [x] **US-3.3.1** — Additional template styles (dark/modern, creative)
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-3.3.1
  - Blocked By: ~~US-1.3.1~~ ✅, ~~US-1.4.1~~ ✅, ~~US-2.4.1~~ ✅

### Epic 3.4: Cải thiện UX Pipeline

- [x] **US-3.4.1** — Pipeline UX improvements
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-3.4.1
  - Blocked By: ~~US-0.3.1~~ ✅, ~~US-2.5.1~~ ✅

---

## Phase 4: Nâng cấp — Template Library, Presentation HTML & Script Architecture

> **Nguồn gốc:** Phản hồi từ testing Phase 0-3. **15 stories PLANNED.**

### Epic 4.1: Template Library PPTX

- [x] **US-4.1.1** — Professional PPTX template collection
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.1.1
  - Blocked By: ~~US-1.4.1~~ ✅, ~~US-3.3.1~~ ✅
  - Refs: slidemembers.com, aippt.com, canva.com

- [x] **US-4.1.2** — Template preview and selection
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.1.2
  - Blocked By: ~~US-4.1.1~~ ✅

- [x] **US-4.1.3** — PPTX script architecture
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.1.3
  - Blocked By: ~~US-4.1.1~~ ✅
  - Refs: a-z-copilot-flow/skills/pptx/scripts/

### Epic 4.2: HTML Presentation Mode (reveal.js)

- [x] **US-4.2.1** — reveal.js integration for tao-html
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.2.1
  - Blocked By: ~~US-2.4.1~~ ✅, ~~US-3.3.1~~ ✅
  - Refs: revealjs.com, slides.com/templates

- [x] **US-4.2.2** — Transitions, animations, and visual effects
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.2.2
  - Blocked By: ~~US-4.2.1~~ ✅
  - Refs: revealjs.com, deckdeckgo.com

- [x] **US-4.2.3** — HTML presentation themes and backgrounds
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.2.3
  - Blocked By: ~~US-4.2.1~~ ✅
  - Refs: slides.com/templates, deckdeckgo.com

### Epic 4.3: Script Architecture cho Skills

- [x] **US-4.3.1** — tao-slide scripts/ directory
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.3.1
  - Blocked By: ~~US-4.1.3~~ ✅
  - Refs: a-z-copilot-flow/skills/pptx/scripts/

- [x] **US-4.3.2** — tao-html scripts/ directory
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.3.2
  - Blocked By: ~~US-4.2.1~~ ✅

- [x] **US-4.3.3** — Script architecture for remaining output skills
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.3.3
  - Blocked By: ~~US-4.3.1~~ ✅, ~~US-4.3.2~~ ✅
  - Refs: a-z-copilot-flow/skills/gen-image

### Epic 4.4: Nâng cấp Content Depth

- [x] **US-4.4.1** — bien-soan comprehensive mode
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.4.1
  - Blocked By: ~~US-1.2.1~~ ✅, ~~US-3.2.1~~ ✅

- [x] **US-4.4.2** — Content enrichment from multiple sources
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.4.2
  - Blocked By: ~~US-2.1.1~~ ✅, ~~US-4.4.1~~ ✅

### Epic 4.5: Template Library HTML

- [x] **US-4.5.1** — HTML reveal.js template collection
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.5.1
  - Blocked By: ~~US-4.2.1~~ ✅, ~~US-4.2.3~~ ✅
  - Refs: slides.com/templates, deckdeckgo.com

- [x] **US-4.5.2** — Presenter notes and PDF export
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.5.2
  - Blocked By: ~~US-4.5.1~~ ✅
  - Refs: revealjs.com

---

### Execution Order (Recommended)

```
Wave 1 (parallel): US-0.1.1, US-0.2.1
Wave 2:            US-0.2.2
Wave 3:            US-0.3.1
Wave 4:            US-0.3.2
Wave 5 (parallel): US-1.1.1, US-1.2.1
Wave 6 (parallel): US-1.1.2, US-1.2.2, US-2.1.1, US-2.2.1, US-2.3.1, US-2.4.1, US-3.2.1
Wave 7 (parallel): US-1.3.1, US-1.4.1
Wave 8 (parallel): US-2.5.1, US-3.1.1, US-3.3.1
Wave 9 (parallel): US-3.1.2, US-3.4.1
--- Phase 0-3 DONE (21/21) ---
Wave 10 (parallel): US-4.1.1, US-4.2.1, US-4.4.1
Wave 11 (parallel): US-4.1.2, US-4.1.3, US-4.2.2, US-4.2.3, US-4.4.2
Wave 12 (parallel): US-4.3.1, US-4.3.2, US-4.5.1
Wave 13 (parallel): US-4.3.3, US-4.5.2
--- Phase 4 DONE (15/15) ---
Wave 14 (parallel): US-5.1.1, US-5.2.1
Wave 15 (sequential): US-5.1.2 (after 5.1.1), US-5.2.2 (after 5.2.1)
```

- **Tên sản phẩm:** InsightEngine
- **Product slug:** `insight-engine`
- **Mục đích checklist:** Nguồn duy nhất cho trạng thái triển khai — theo dõi tiến độ, kiểm soát dependency, hỗ trợ làm việc song song

---

## Phase 0: Nền tảng sản phẩm

### Epic 0.1: Workspace Setup

- [x] **US-0.1.1** — Cấu trúc repo & cấu hình Copilot
  - Trạng thái: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-0.1.1
  - Bị chặn bởi: None

### Epic 0.2: Cài đặt môi trường (`cai-dat`)

- [x] **US-0.2.1** — Script kiểm tra dependencies
  - Trạng thái: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-0.2.1
  - Bị chặn bởi: None

- [x] **US-0.2.2** — Skill cài đặt (`cai-dat`)
  - Trạng thái: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-0.2.2
  - Bị chặn bởi: ~~US-0.2.1~~ ✅

### Epic 0.3: Pipeline Chính (`tong-hop`)

- [x] **US-0.3.1** — Pipeline skeleton với intent routing
  - Trạng thái: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-0.3.1
  - Bị chặn bởi: ~~US-0.1.1~~ ✅, ~~US-0.2.2~~ ✅

- [x] **US-0.3.2** — Kiểm tra setup trước mỗi process
  - Trạng thái: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-0.3.2
  - Bị chặn bởi: ~~US-0.3.1~~ ✅

---

## Phase 1: MVP — Thu thập & Xuất cơ bản

### Epic 1.1: Thu thập nội dung (`thu-thap`)

- [x] **US-1.1.1** — Đọc file local qua markitdown
  - Trạng thái: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-1.1.1
  - Bị chặn bởi: ~~US-0.3.2~~ ✅

- [x] **US-1.1.2** — Fetch nội dung URL
  - Trạng thái: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-1.1.2
  - Bị chặn bởi: ~~US-1.1.1~~ ✅

### Epic 1.2: Biên soạn nội dung (`bien-soan`)

- [x] **US-1.2.1** — Tổng hợp nội dung đa nguồn
  - Trạng thái: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-1.2.1
  - Bị chặn bởi: ~~US-0.3.2~~ ✅

- [x] **US-1.2.2** — Dịch thuật cơ bản Việt ↔ Anh
  - Trạng thái: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-1.2.2
  - Bị chặn bởi: ~~US-1.2.1~~ ✅

### Epic 1.3: Xuất Word (`tao-word`)

- [x] **US-1.3.1** — Xuất Word với 3 template style
  - Trạng thái: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-1.3.1
  - Bị chặn bởi: ~~US-1.2.1~~ ✅, ~~US-1.1.1~~ ✅

### Epic 1.4: Xuất PowerPoint (`tao-slide`)

- [x] **US-1.4.1** — Xuất PowerPoint với 3 template style
  - Trạng thái: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-1.4.1
  - Bị chặn bởi: ~~US-1.2.1~~ ✅, ~~US-1.1.1~~ ✅

---

## Phase 2: Mở rộng — Tìm kiếm & Thêm định dạng

### Epic 2.1: Tìm kiếm Google tự động

- [x] **US-2.1.1** — Tích hợp web search vào thu-thap
  - Trạng thái: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-2.1.1
  - Bị chặn bởi: ~~US-1.1.1~~ ✅

### Epic 2.2: Xuất Excel (`tao-excel`)

- [x] **US-2.2.1** — Xuất Excel với công thức và formatting
  - Trạng thái: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-2.2.1
  - Bị chặn bởi: ~~US-1.2.1~~ ✅

### Epic 2.3: Xuất PDF (`tao-pdf`)

- [x] **US-2.3.1** — Xuất PDF từ nội dung tổng hợp
  - Trạng thái: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-2.3.1
  - Bị chặn bởi: ~~US-1.2.1~~ ✅

### Epic 2.4: Xuất HTML (`tao-html`)

- [x] **US-2.4.1** — Xuất trang HTML tĩnh với 3 template style
  - Trạng thái: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-2.4.1
  - Bị chặn bởi: ~~US-1.2.1~~ ✅

### Epic 2.5: Chaining Output

- [x] **US-2.5.1** — Chuỗi output trong pipeline
  - Trạng thái: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-2.5.1
  - Bị chặn bởi: ~~US-1.3.1~~ ✅, ~~US-1.4.1~~ ✅, ~~US-2.2.1~~ ✅

---

## Phase 3: Hoàn thiện — Trực quan & Tối ưu

### Epic 3.1: Biểu đồ & Hình ảnh (`tao-hinh`)

- [x] **US-3.1.1** — Tạo biểu đồ từ dữ liệu
  - Trạng thái: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-3.1.1
  - Bị chặn bởi: ~~US-2.2.1~~ ✅

- [x] **US-3.1.2** — Tạo hình minh họa cho slide (Apple Silicon)
  - Trạng thái: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-3.1.2
  - Bị chặn bởi: ~~US-3.1.1~~ ✅

### Epic 3.2: Xử lý tài liệu lớn

- [x] **US-3.2.1** — Chunking strategy cho tài liệu lớn
  - Trạng thái: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-3.2.1
  - Bị chặn bởi: ~~US-1.2.1~~ ✅

### Epic 3.3: Template Library mở rộng

- [x] **US-3.3.1** — Thêm style dark/modern và creative
  - Trạng thái: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-3.3.1
  - Bị chặn bởi: ~~US-1.3.1~~ ✅, ~~US-1.4.1~~ ✅, ~~US-2.4.1~~ ✅

### Epic 3.4: Cải thiện UX Pipeline

- [x] **US-3.4.1** — Cải thiện UX pipeline
  - Trạng thái: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-3.4.1
  - Bị chặn bởi: ~~US-0.3.1~~ ✅, ~~US-2.5.1~~ ✅

---

## Phase 4: Nâng cấp — Template Library, Presentation HTML & Script Architecture

> **Nguồn gốc:** Phản hồi từ testing Phase 0-3. **15 stories PLANNED.**

### Epic 4.1: Template Library PPTX

- [x] **US-4.1.1** — Thư viện template PPTX chuyên nghiệp
  - Trạng thái: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.1.1
  - Bị chặn bởi: ~~US-1.4.1~~ ✅, ~~US-3.3.1~~ ✅
  - Tham khảo: slidemembers.com, aippt.com, canva.com

- [x] **US-4.1.2** — Preview và chọn template
  - Trạng thái: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.1.2
  - Bị chặn bởi: ~~US-4.1.1~~ ✅

- [x] **US-4.1.3** — Kiến trúc script cho tao-slide
  - Trạng thái: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.1.3
  - Bị chặn bởi: ~~US-4.1.1~~ ✅
  - Tham khảo: a-z-copilot-flow/skills/pptx/scripts/

### Epic 4.2: HTML Presentation Mode (reveal.js)

- [x] **US-4.2.1** — Tích hợp reveal.js cho tao-html
  - Trạng thái: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.2.1
  - Bị chặn bởi: ~~US-2.4.1~~ ✅, ~~US-3.3.1~~ ✅
  - Tham khảo: revealjs.com, slides.com/templates

- [x] **US-4.2.2** — Hiệu ứng chuyển đổi và animation
  - Trạng thái: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.2.2
  - Bị chặn bởi: ~~US-4.2.1~~ ✅
  - Tham khảo: revealjs.com, deckdeckgo.com

- [x] **US-4.2.3** — Themes và backgrounds
  - Trạng thái: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.2.3
  - Bị chặn bởi: ~~US-4.2.1~~ ✅
  - Tham khảo: slides.com/templates, deckdeckgo.com

### Epic 4.3: Script Architecture cho Skills

- [x] **US-4.3.1** — scripts/ cho tao-slide
  - Trạng thái: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.3.1
  - Bị chặn bởi: ~~US-4.1.3~~ ✅
  - Tham khảo: a-z-copilot-flow/skills/pptx/scripts/

- [x] **US-4.3.2** — scripts/ cho tao-html
  - Trạng thái: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.3.2
  - Bị chặn bởi: ~~US-4.2.1~~ ✅

- [x] **US-4.3.3** — Script architecture cho tao-word, tao-excel, tao-pdf
  - Trạng thái: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.3.3
  - Bị chặn bởi: ~~US-4.3.1~~ ✅, ~~US-4.3.2~~ ✅

### Epic 4.4: Nâng cấp Content Depth

- [x] **US-4.4.1** — bien-soan comprehensive mode
  - Trạng thái: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.4.1
  - Bị chặn bởi: ~~US-1.2.1~~ ✅, ~~US-3.2.1~~ ✅

- [x] **US-4.4.2** — Tự động làm giàu nội dung từ web
  - Trạng thái: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.4.2
  - Bị chặn bởi: ~~US-2.1.1~~ ✅, ~~US-4.4.1~~ ✅

### Epic 4.5: Template Library HTML

- [x] **US-4.5.1** — Thư viện template HTML reveal.js
  - Trạng thái: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.5.1
  - Bị chặn bởi: ~~US-4.2.1~~ ✅, ~~US-4.2.3~~ ✅
  - Tham khảo: slides.com/templates, deckdeckgo.com

- [x] **US-4.5.2** — Presenter notes và PDF export
  - Trạng thái: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-4.5.2
  - Bị chặn bởi: ~~US-4.5.1~~ ✅
  - Tham khảo: revealjs.com

---

## Phase 5: Tối ưu & Độ bền

### Epic 5.1: Small Model Optimization

- [x] **US-5.1.1** — Small model compatibility research
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-5.1.1
  - Blocked By: None

- [x] **US-5.1.2** — SKILL.md refactor for small model compatibility
  - Status: DONE ✅
  - Assignee: copilot
  - Branch: feature/insight-engine-us-5.1.2
  - Blocked By: ~~US-5.1.1~~ ✅

### Epic 5.2: Session State Persistence

- [x] **US-5.2.1** — Session state save after each pipeline step
  - Status: DONE ✅
  - Assignee: copilot
  - Branch: feature/insight-engine-us-5.2.1
  - Blocked By: None

- [x] **US-5.2.2** — Pipeline resume from saved state
  - Status: DONE ✅
  - Assignee: copilot
  - Branch: feature/insight-engine-us-5.2.2
  - Blocked By: ~~US-5.2.1~~ ✅

---

## Phase 6: Agent Architecture & Quality Gates

> **Nguồn gốc:** Phản hồi từ real-world usage. **14 stories PLANNED.**

### Epic 6.1: Strict File Rules & Auto-escalation

- [x] **US-6.1.1** — Strict file location rules enforcement
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-6.1.1
  - Blocked By: None

- [x] **US-6.1.2** — Auto-escalation protocol
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-6.1.2
  - Blocked By: ~~US-6.1.1~~ ✅

### Epic 6.2: Shared Context Protocol

- [x] **US-6.2.1** — Shared context file design
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-6.2.1
  - Blocked By: None

- [x] **US-6.2.2** — Agent context read/write API
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-6.2.2
  - Blocked By: ~~US-6.2.1~~ ✅

### Epic 6.3: Model Profile & Decision Maps

- [x] **US-6.3.1** — Decision maps per capability category
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-6.3.1
  - Blocked By: None

- [x] **US-6.3.2** — Model self-declaration with fallback
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-6.3.2
  - Blocked By: ~~US-6.3.1~~ ✅, ~~US-6.2.1~~ ✅

- [x] **US-6.3.3** — Pre-built workflow templates
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-6.3.3
  - Blocked By: ~~US-6.3.1~~ ✅

### Epic 6.4: Agent Strategist

- [x] **US-6.4.1** — Strategist agent — dynamic workflow generation
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-6.4.1
  - Blocked By: ~~US-6.3.2~~ ✅, ~~US-6.3.3~~ ✅, ~~US-6.2.1~~ ✅

### Epic 6.5: Tiered Audit System

- [x] **US-6.5.1** — Tiered audit implementation
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-6.5.1
  - Blocked By: ~~US-6.2.1~~ ✅

- [x] **US-6.5.2** — Final output audit with step-level rollback
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-6.5.2
  - Blocked By: ~~US-6.5.1~~ ✅, ~~US-6.4.1~~ ✅

### Epic 6.6: Advisory Agent & Conditional Skill Creation

- [x] **US-6.6.1** — Advisory agent — multi-perspective single-call
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-6.6.1
  - Blocked By: ~~US-6.2.1~~ ✅

- [x] **US-6.6.2** — Conditional skill-forge runtime
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-6.6.2
  - Blocked By: ~~US-6.6.1~~ ✅

- [x] **US-6.6.3** — Public skill clone with security check
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-6.6.3
  - Blocked By: ~~US-6.6.2~~ ✅

### Epic 6.7: Pipeline Integration

- [x] **US-6.7.1** — tong-hop integration with AGENT_MODE feature flag
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-6.7.1
  - Blocked By: ~~US-6.4.1~~ ✅, ~~US-6.5.1~~ ✅, ~~US-6.6.1~~ ✅

---

## Phase 7: Pipeline Enforcement & Compliance Hardening

> **Nguồn gốc:** Real-world testing — model skip critical steps khi instructions nằm trong reference files. **5 stories PLANNED.**

### Epic 7.1: Inline Critical Steps & Hard Gates

- [x] **US-7.1.1** — Inline request analysis and REQUEST_TYPE detection
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-7.1.1
  - Blocked By: None

- [x] **US-7.1.2** — Hard confirmation gate before execution
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-7.1.2
  - Blocked By: ~~US-7.1.1~~ ✅

### Epic 7.2: Data Collection Enforcement

- [x] **US-7.2.1** — Inline data collection protocol in thu-thap
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-7.2.1
  - Blocked By: None

- [x] **US-7.2.2** — Pre-output URL validation gate
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-7.2.2
  - Blocked By: ~~US-7.2.1~~ ✅

### Epic 7.3: Visible Pipeline Trace

- [x] **US-7.3.1** — Numbered step trace with live progress
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-7.3.1
  - Blocked By: None

---

## Phase 8: Shared Copilot Agent Architecture

> Refactor agents from Phase 6 inline instructions → standalone shared Copilot agents (`runSubagent`).

### Epic 8.1: Shared Auditor Agent

- [x] **US-8.1.1** — Auditor as standalone Copilot agent
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-8.1.1
  - Blocked By: None

- [x] **US-8.1.2** — Auditor integration into output skills
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-8.1.2
  - Blocked By: ~~US-8.1.1~~ ✅

### Epic 8.2: Shared Strategist Agent

- [x] **US-8.2.1** — Strategist as standalone Copilot agent
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-8.2.1
  - Blocked By: None

### Epic 8.3: Shared Advisory Agent

- [x] **US-8.3.1** — Advisory as standalone Copilot agent
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-8.3.1
  - Blocked By: None

### Epic 8.4: Agent Integration Protocol

- [x] **US-8.4.1** — Standardized agent calling protocol
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-8.4.1
  - Blocked By: ~~US-8.1.1~~ ✅, ~~US-8.2.1~~ ✅, ~~US-8.3.1~~ ✅

- [x] **US-8.4.2** — tong-hop migration to shared agents
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-8.4.2
  - Blocked By: ~~US-8.4.1~~ ✅

---

## Phase 9: Central Orchestrator & Adaptive Self-Improvement

> Tách orchestration khỏi tổng hợp nội dung. Agent trung tâm, tự cải thiện thích ứng, audit thang 100 điểm, resume xuyên session, chuẩn hóa agents theo VS Code custom agent standard (`.github/agents/*.agent.md`).

### Epic 9.1: Central Orchestrator (`dieu-phoi`)

- [x] **US-9.1.1** — Central orchestrator agent skeleton
  - Status: DONE
  - Assignee: Copilot
  - Branch: feature/insight-engine-us-9.1.1
  - Blocked By: ~~US-8.4.2~~ ✅

- [x] **US-9.1.2** — tong-hop refactor to synthesis-only
  - Status: DONE
  - Assignee: Copilot
  - Branch: feature/insight-engine-us-9.1.2
  - Blocked By: ~~US-9.1.1~~ ✅

- [x] **US-9.1.3** — dieu-phoi integration with shared agents
  - Status: DONE
  - Assignee: Copilot
  - Branch: feature/insight-engine-us-9.1.3
  - Blocked By: ~~US-9.1.1~~ ✅

### Epic 9.2: Adaptive Self-Improvement

- [x] **US-9.2.1** — Capability gap evaluation protocol
  - Status: DONE
  - Assignee: Copilot
  - Branch: feature/insight-engine-us-9.2.1
  - Blocked By: ~~US-9.1.1~~ ✅

- [x] **US-9.2.2** — Runtime agent creation with user consent
  - Status: DONE
  - Assignee: Copilot
  - Branch: feature/insight-engine-us-9.2.2
  - Blocked By: ~~US-9.2.1~~ ✅

- [x] **US-9.2.3** — Runtime skill creation/upgrade
  - Status: DONE
  - Assignee: Copilot
  - Branch: feature/insight-engine-us-9.2.3
  - Blocked By: ~~US-9.2.1~~ ✅

### Epic 9.3: Enhanced Working State & Cross-Session Resume

- [x] **US-9.3.1** — Enhanced session state schema
  - Status: DONE
  - Assignee: Copilot
  - Branch: feature/insight-engine-us-9.3.1
  - Blocked By: ~~US-5.2.1~~ ✅

- [x] **US-9.3.2** — Step-level state persistence
  - Status: DONE
  - Assignee: Copilot
  - Branch: feature/insight-engine-us-9.3.2
  - Blocked By: ~~US-9.3.1~~ ✅

- [x] **US-9.3.3** — Cross-session resume
  - Status: DONE
  - Assignee: Copilot
  - Branch: feature/insight-engine-us-9.3.3
  - Blocked By: ~~US-9.3.2~~ ✅

### Epic 9.4: 100-Point Weighted Audit Scoring

- [x] **US-9.4.1** — 100-point audit scoring system
  - Status: DONE
  - Assignee: Copilot
  - Branch: feature/insight-engine-us-9.4.1
  - Blocked By: ~~US-8.1.1~~ ✅

- [x] **US-9.4.2** — Targeted retry loop with score tracking
  - Status: DONE
  - Assignee: Copilot
  - Branch: feature/insight-engine-us-9.4.2
  - Blocked By: ~~US-9.4.1~~ ✅

### Epic 9.5: VS Code Custom Agent Standard Migration

- [x] **US-9.5.1** — Migrate existing agents to .agent.md format
  - Status: DONE
  - Assignee: Copilot
  - Branch: feature/insight-engine-us-9.5.1
  - Blocked By: ~~US-8.1.1~~ ✅, ~~US-8.2.1~~ ✅, ~~US-8.3.1~~ ✅

---

## Phase 10: English Naming, Natural Language UX & Product Alignment

> Chuẩn hóa tên skill/agent sang tiếng Anh, UX ngôn ngữ tự nhiên, dọn dẹp legacy, bổ sung stories thiếu. **14 stories PLANNED.**

### Epic 10.1: Rename Skills to English

- [x] **US-10.1.1** — Rename all skill directories from Vietnamese to English
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-10.1.1
  - Blocked By: None

- [x] **US-10.1.2** — Update SKILL.md triggers for renamed skills
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-10.1.2
  - Blocked By: ~~US-10.1.1~~ ✅

### Epic 10.2: Rename Agents to English

- [x] **US-10.2.1** — Rename dieu-phoi agent to orchestrator
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-10.2.1
  - Blocked By: None

### Epic 10.3: Natural Language UX

- [x] **US-10.3.1** — Remove slash command dependency
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-10.3.1
  - Blocked By: ~~US-10.1.2~~ ✅, ~~US-10.2.1~~ ✅

- [x] **US-10.3.2** — Update README for natural language UX
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-10.3.2
  - Blocked By: ~~US-10.3.1~~ ✅

### Epic 10.4: copilot-instructions.md Refresh

- [x] **US-10.4.1** — Update skill registry with English names
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-10.4.1
  - Blocked By: ~~US-10.1.1~~ ✅, ~~US-10.2.1~~ ✅

- [x] **US-10.4.2** — Fix stale PIPELINE_FLOW and update Vietnamese Language Rules
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-10.4.2
  - Blocked By: ~~US-10.4.1~~ ✅

### Epic 10.5: Clean Up Legacy Artifacts

- [x] **US-10.5.1** — Remove shared-agents directory
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-10.5.1
  - Blocked By: None

- [x] **US-10.5.2** — Remove duplicate agent files
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-10.5.2
  - Blocked By: ~~US-10.5.1~~ ✅

### Epic 10.6: Backfill Missing Skill Stories

- [x] **US-10.6.1** — design skill user story (formerly thiet-ke)
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-10.6.1-2-3
  - Blocked By: ~~US-10.1.1~~ ✅

- [x] **US-10.6.2** — verify skill user story (formerly kiem-tra)
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-10.6.1-2-3
  - Blocked By: ~~US-10.1.1~~ ✅

- [x] **US-10.6.3** — improve skill user story (formerly cai-tien)
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-10.6.1-2-3
  - Blocked By: ~~US-10.1.1~~ ✅

### Epic 10.7: Product Doc Alignment

- [ ] **US-10.7.1** — Update instructions.md Vietnamese Language Rules
  - Status: PLANNED
  - Assignee: copilot
  - Blocked By: ~~US-10.1.1~~ ✅

- [x] **US-10.7.2** — Final cross-document consistency check
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-10.7.2
  - Blocked By: ~~US-10.7.1~~ ✅

---

### Execution Order (Recommended)

```
Wave 1 (parallel): US-0.1.1, US-0.2.1
Wave 2:            US-0.2.2
Wave 3:            US-0.3.1
Wave 4:            US-0.3.2
Wave 5 (parallel): US-1.1.1, US-1.2.1
Wave 6 (parallel): US-1.1.2, US-1.2.2, US-2.1.1, US-2.2.1, US-2.3.1, US-2.4.1, US-3.2.1
Wave 7 (parallel): US-1.3.1, US-1.4.1
Wave 8 (parallel): US-2.5.1, US-3.1.1, US-3.3.1
Wave 9 (parallel): US-3.1.2, US-3.4.1
--- Phase 0-3 DONE (21/21) ---
Wave 10 (parallel): US-4.1.1, US-4.2.1, US-4.4.1
Wave 11 (parallel): US-4.1.2, US-4.1.3, US-4.2.2, US-4.2.3, US-4.4.2
Wave 12 (parallel): US-4.3.1, US-4.3.2, US-4.5.1
Wave 13 (parallel): US-4.3.3, US-4.5.2
--- Phase 4 DONE (15/15) ---
Wave 14 (parallel): US-5.1.1, US-5.2.1
Wave 15 (sequential): US-5.1.2 (after 5.1.1), US-5.2.2 (after 5.2.1)
--- Phase 5 DONE (4/4) ---
Wave 16 (parallel): US-6.1.1, US-6.2.1, US-6.3.1
Wave 17 (parallel): US-6.1.2, US-6.2.2, US-6.3.3, US-6.5.1, US-6.6.1
Wave 18 (parallel): US-6.3.2, US-6.4.1, US-6.6.2
Wave 19 (parallel): US-6.5.2, US-6.6.3, US-6.7.1
--- Phase 6 DONE (14/14) ---
Wave 20 (parallel): US-7.1.1, US-7.2.1, US-7.3.1
Wave 21 (sequential): US-7.1.2 (after 7.1.1), US-7.2.2 (after 7.2.1)
--- Phase 7 DONE (5/5) ---
Wave 22 (parallel): US-8.1.1, US-8.2.1, US-8.3.1
Wave 23 (sequential): US-8.1.2 (after 8.1.1)
Wave 24 (sequential): US-8.4.1 (after 8.1.1, 8.2.1, 8.3.1)
Wave 25 (sequential): US-8.4.2 (after 8.4.1)
--- Phase 8 DONE (6/6) ---
Wave 26 (parallel): US-9.1.1, US-9.4.1, US-9.5.1
Wave 27 (parallel): US-9.1.2, US-9.1.3, US-9.2.1, US-9.3.1
Wave 28 (parallel): US-9.2.2, US-9.2.3, US-9.3.2
Wave 29 (parallel): US-9.3.3, US-9.4.2
--- Phase 9 DONE (12/12) ---
Wave 30 (parallel): US-10.1.1, US-10.2.1, US-10.5.1
Wave 31 (parallel): US-10.1.2, US-10.4.1, US-10.5.2, US-10.6.1, US-10.6.2, US-10.6.3, US-10.7.1
Wave 32 (parallel): US-10.3.1, US-10.4.2, US-10.7.2
Wave 33 (sequential): US-10.3.2 (after 10.3.1)
--- Phase 10: 13 DONE, 1 PLANNED (US-10.7.1) ---

## Phase 11: Adaptive Search Intelligence

> Tìm kiếm thông minh thích ứng — per-step search planning, DOM exploration, detail URL extraction, adaptive flow advisor. **6 stories PLANNED.**

### Epic 11.1: Per-Step Search Planner

- [ ] **US-11.1.1** — Integrate per-step search planner in gather skill
  - Status: PLANNED
  - Assignee: copilot
  - Blocked By: None

### Epic 11.2: Source DOM Explorer

- [ ] **US-11.2.1** — Auto DOM exploration when site-scoped search returns thin results
  - Status: PLANNED
  - Assignee: copilot
  - Blocked By: US-11.1.1

- [ ] **US-11.2.2** — Internal search usage via DOM-discovered endpoints
  - Status: PLANNED
  - Assignee: copilot
  - Blocked By: US-11.2.1

### Epic 11.3: Detail URL Extractor

- [ ] **US-11.3.1** — Extract canonical detail-page URLs for inline/popup detail sources
  - Status: PLANNED
  - Assignee: copilot
  - Blocked By: US-11.2.1

### Epic 11.4: Adaptive Flow Advisor

- [ ] **US-11.4.1** — Advisory agent fallback after 2 failed search attempts
  - Status: PLANNED
  - Assignee: copilot
  - Blocked By: US-11.1.1

- [ ] **US-11.4.2** — User-facing flow alternatives presentation
  - Status: PLANNED
  - Assignee: copilot
  - Blocked By: US-11.4.1

Wave 34 (sequential): US-11.1.1
Wave 35 (sequential): US-11.2.1 (after 11.1.1)
Wave 36 (parallel): US-11.2.2 (after 11.2.1), US-11.3.1 (after 11.2.1)
Wave 37 (sequential): US-11.4.1 (after 11.1.1)
Wave 38 (sequential): US-11.4.2 (after 11.4.1)
--- Phase 11 PLANNED (6/6) ---
```

---

*This checklist is the single source of execution state. Status changes happen here only.*  
*Bước tiếp theo: `/roadmap-to-delivery` — Chọn user story đầu tiên để bắt đầu triển khai.*
