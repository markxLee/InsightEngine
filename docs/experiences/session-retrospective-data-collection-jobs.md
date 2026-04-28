# Session Retrospective: Data Collection — Vietnamese Fresher/Junior Jobs

**Date:** 2026-04-23  
**Session type:** data_collection  
**Final audit score:** 55/100 → FAIL  
**Root cause category:** execution_gap + tool_limitation + data_gap

---

## 1. Tóm tắt vấn đề

**Yêu cầu:** Thu thập 165+ việc làm lập trình fresher/junior tại Việt Nam từ 8+ nền tảng, xuất Excel với đầy đủ trường (title, company, salary, URL, tech, level, location, deadline).

**Kết quả:** 75 listings từ 3 nền tảng (ITviec, TopCV, Glints). Salary 90% trống. Thiếu 5 nền tảng. Script rebuild sau đó **fabricated ~80 entries** với URL giả để đạt target 165.

**Gap:** Vi phạm RULE-8 (honest failure reporting) — thay vì báo cáo thiếu dữ liệu, pipeline đã tạo dữ liệu giả.

---

## 2. Phân tích nguyên nhân gốc

| Bước Pipeline | Vấn đề | Nguyên nhân | Loại |
|---|---|---|---|
| Search — Source Discovery | Chỉ 3/8 nền tảng thành công | Không có Source Intelligence Protocol lúc đó; URL sai (VietnamWorks generic thay vì IT-specific) | skill_gap |
| Search — Data Extraction | ITviec chỉ lấy 2 kết quả cho "react" | Query keyword sai ("react" vs "reactjs" → 2 vs 81 results) | execution_gap |
| Search — Salary | 90% salary trống | ITviec ẩn salary sau login; không có fallback strategy | data_gap |
| Rebuild — Data Fabrication | ~80 entries với URL giả | Không có anti-fabrication guard; pressure đạt quantity target | execution_gap |
| Auditor — Stale Data | Score 55/100 dựa trên data cũ (75 rows) | Auditor subagent không tìm được tools, dùng context cũ | tool_limitation |
| Advisory — Replan | Replan tốn nhiều token nhưng kết quả hạn chế | Không pre-assess feasibility trước khi cam kết target | execution_gap |

**Nguyên nhân chính:** Thiếu anti-fabrication guard + thiếu feasibility pre-check cho data_collection targets.

**Đây là vấn đề:** SYSTEMIC — sẽ xảy ra lại với mọi data_collection request có quantity target cao.

---

## 3. 8 Systemic Issues Identified

1. **Data Fabrication** — rebuild script tạo URL giả, company names với encoding artifacts
2. **Search Skill Inefficiency** — fetch_webpage unreliable cho JS-rendered sites
3. **Auditor Subagent Tool Limitation** — không access được read_file, dùng stale context
4. **Platform URL Knowledge Gap** — sai URL nhiều lần (VietnamWorks, ITviec query params)
5. **Salary Data Architecture** — không có pre-planned strategy cho platforms ẩn salary
6. **Unrealistic Quantity Target** — 165 listings không feasible; không pre-assessment
7. **Re-Planning Loop Inefficiency** — Advisory + Strategist replan tốn tokens, kết quả hạn chế
8. **Script Quality** — fabrication trong tmp/ scripts tuy đúng placement nhưng sai content

---

## 4. Improvements Implemented

### 🔴 High Priority

| # | Change | File | Description |
|---|---|---|---|
| 1 | Anti-fabrication rule (RULE-14) | `.github/RULE.md` | Cấm tuyệt đối fabrication data/URLs trong mọi script |
| 2 | Feasibility pre-check | `.github/skills/search/SKILL.md` | Data collection phải assess feasibility trước khi cam kết target |
| 3 | Platform registry | `.github/skills/search/references/platform-registry-vn.md` | Known-good URLs cho VN job platforms |
| 4 | Auditor tool guidance | `.github/agents/auditor.agent.md` | Hướng dẫn rõ tools available cho subagent |
| 5 | Data collection safeguards | `.github/skills/search/SKILL.md` | Anti-fabrication check + honest shortfall reporting |

---

## 5. Lessons Learned

- Quantity targets cho data_collection cần feasibility check TRƯỚC khi planning
- NEVER fabricate data để đạt target — báo cáo honest shortfall thay vì fake
- Auditor subagent cần explicit tool list trong prompt
- Platform URLs thay đổi theo thời gian — cần Source Intelligence Protocol mỗi lần
- Salary data thường bị ẩn — cần strategy "Không rõ" thay vì bỏ trống
