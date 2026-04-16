# InsightEngine — Product Checklist

> **Product:** InsightEngine  
> **Product Slug:** insight-engine  
> **Created:** 2026-04-16  
> **Total User Stories:** 21  
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

- [ ] **US-1.1.2** — Fetch URL content
  - Status: PLANNED
  - Blocked By: ~~US-1.1.1~~ ✅

### Epic 1.2: Biên soạn nội dung (`bien-soan`)

- [x] **US-1.2.1** — Multi-source content synthesis
  - Status: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-1.2.1
  - Blocked By: ~~US-0.3.2~~ ✅

- [ ] **US-1.2.2** — Basic translation Vietnamese ↔ English
  - Status: PLANNED
  - Blocked By: ~~US-1.2.1~~ ✅

### Epic 1.3: Xuất Word (`tao-word`)

- [ ] **US-1.3.1** — Word document output with 3 template styles
  - Status: PLANNED
  - Blocked By: ~~US-1.2.1~~ ✅, ~~US-1.1.1~~ ✅

### Epic 1.4: Xuất PowerPoint (`tao-slide`)

- [ ] **US-1.4.1** — PowerPoint output with 3 template styles
  - Status: PLANNED
  - Blocked By: ~~US-1.2.1~~ ✅, ~~US-1.1.1~~ ✅

---

## Phase 2: Mở rộng — Tìm kiếm & Thêm định dạng

### Epic 2.1: Tìm kiếm Google tự động

- [ ] **US-2.1.1** — Web search integration in thu-thap
  - Status: PLANNED
  - Blocked By: ~~US-1.1.1~~ ✅

### Epic 2.2: Xuất Excel (`tao-excel`)

- [ ] **US-2.2.1** — Excel output with formulas and formatting
  - Status: PLANNED
  - Blocked By: ~~US-1.2.1~~ ✅

### Epic 2.3: Xuất PDF (`tao-pdf`)

- [ ] **US-2.3.1** — PDF output from synthesized content
  - Status: PLANNED
  - Blocked By: ~~US-1.2.1~~ ✅

### Epic 2.4: Xuất HTML (`tao-html`)

- [ ] **US-2.4.1** — Static HTML page output with 3 template styles
  - Status: PLANNED
  - Blocked By: ~~US-1.2.1~~ ✅

### Epic 2.5: Chaining Output

- [ ] **US-2.5.1** — Pipeline output chaining
  - Status: PLANNED
  - Blocked By: US-1.3.1, US-1.4.1, US-2.2.1

---

## Phase 3: Hoàn thiện — Trực quan & Tối ưu

### Epic 3.1: Biểu đồ & Hình ảnh (`tao-hinh`)

- [ ] **US-3.1.1** — Chart generation from data
  - Status: PLANNED
  - Blocked By: US-2.2.1

- [ ] **US-3.1.2** — Image generation for slides (Apple Silicon)
  - Status: PLANNED
  - Blocked By: US-3.1.1

### Epic 3.2: Xử lý tài liệu lớn

- [ ] **US-3.2.1** — Large document chunking strategy
  - Status: PLANNED
  - Blocked By: ~~US-1.2.1~~ ✅

### Epic 3.3: Template Library mở rộng

- [ ] **US-3.3.1** — Additional template styles (dark/modern, creative)
  - Status: PLANNED
  - Blocked By: US-1.3.1, US-1.4.1, US-2.4.1

### Epic 3.4: Cải thiện UX Pipeline

- [ ] **US-3.4.1** — Pipeline UX improvements
  - Status: PLANNED
  - Blocked By: ~~US-0.3.1~~ ✅, US-2.5.1

---

---

## Tổng quan Checklist sản phẩm (Tiếng Việt)

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

- [ ] **US-1.1.2** — Fetch nội dung URL
  - Trạng thái: PLANNED
  - Bị chặn bởi: ~~US-1.1.1~~ ✅

### Epic 1.2: Biên soạn nội dung (`bien-soan`)

- [x] **US-1.2.1** — Tổng hợp nội dung đa nguồn
  - Trạng thái: DONE
  - Assignee: copilot
  - Branch: feature/insight-engine-us-1.2.1
  - Bị chặn bởi: ~~US-0.3.2~~ ✅

- [ ] **US-1.2.2** — Dịch thuật cơ bản Việt ↔ Anh
  - Trạng thái: PLANNED
  - Bị chặn bởi: ~~US-1.2.1~~ ✅

### Epic 1.3: Xuất Word (`tao-word`)

- [ ] **US-1.3.1** — Xuất Word với 3 template style
  - Trạng thái: PLANNED
  - Bị chặn bởi: ~~US-1.2.1~~ ✅, ~~US-1.1.1~~ ✅

### Epic 1.4: Xuất PowerPoint (`tao-slide`)

- [ ] **US-1.4.1** — Xuất PowerPoint với 3 template style
  - Trạng thái: PLANNED
  - Bị chặn bởi: ~~US-1.2.1~~ ✅, ~~US-1.1.1~~ ✅

---

## Phase 2: Mở rộng — Tìm kiếm & Thêm định dạng

### Epic 2.1: Tìm kiếm Google tự động

- [ ] **US-2.1.1** — Tích hợp web search vào thu-thap
  - Trạng thái: PLANNED
  - Bị chặn bởi: ~~US-1.1.1~~ ✅

### Epic 2.2: Xuất Excel (`tao-excel`)

- [ ] **US-2.2.1** — Xuất Excel với công thức và formatting
  - Trạng thái: PLANNED
  - Bị chặn bởi: ~~US-1.2.1~~ ✅

### Epic 2.3: Xuất PDF (`tao-pdf`)

- [ ] **US-2.3.1** — Xuất PDF từ nội dung tổng hợp
  - Trạng thái: PLANNED
  - Bị chặn bởi: ~~US-1.2.1~~ ✅

### Epic 2.4: Xuất HTML (`tao-html`)

- [ ] **US-2.4.1** — Xuất HTML tĩnh với 3 template style
  - Trạng thái: PLANNED
  - Bị chặn bởi: ~~US-1.2.1~~ ✅

### Epic 2.5: Chaining Output

- [ ] **US-2.5.1** — Chuỗi output trong pipeline
  - Trạng thái: PLANNED
  - Bị chặn bởi: US-1.3.1, US-1.4.1, US-2.2.1

---

## Phase 3: Hoàn thiện — Trực quan & Tối ưu

### Epic 3.1: Biểu đồ & Hình ảnh (`tao-hinh`)

- [ ] **US-3.1.1** — Tạo biểu đồ từ dữ liệu
  - Trạng thái: PLANNED
  - Bị chặn bởi: US-2.2.1

- [ ] **US-3.1.2** — Tạo hình minh họa cho slide (Apple Silicon)
  - Trạng thái: PLANNED
  - Bị chặn bởi: US-3.1.1

### Epic 3.2: Xử lý tài liệu lớn

- [ ] **US-3.2.1** — Chunking strategy cho tài liệu lớn
  - Trạng thái: PLANNED
  - Bị chặn bởi: ~~US-1.2.1~~ ✅

### Epic 3.3: Template Library mở rộng

- [ ] **US-3.3.1** — Thêm style dark/modern và creative
  - Trạng thái: PLANNED
  - Bị chặn bởi: US-1.3.1, US-1.4.1, US-2.4.1

### Epic 3.4: Cải thiện UX Pipeline

- [ ] **US-3.4.1** — Cải thiện UX pipeline
  - Trạng thái: PLANNED
  - Bị chặn bởi: ~~US-0.3.1~~ ✅, US-2.5.1

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
```

---

*This checklist is the single source of execution state. Status changes happen here only.*  
*Bước tiếp theo: `/roadmap-to-delivery` — Chọn user story đầu tiên để bắt đầu triển khai.*
