# InsightEngine

Pipeline tổng hợp nội dung đa nguồn → đa định dạng đầu ra, chạy hoàn toàn trong VS Code với GitHub Copilot.

> **🔄 Đã fork repo này?** Bấm **Sync fork → Update branch** trong repo của bạn trên GitHub, sau đó nhắn Copilot: `setup InsightEngine`

---

## Getting Started

### Option A — GitHub Codespaces (không cần cài đặt gì, chạy ngay trên trình duyệt)

> **Phù hợp để dùng thử.** GitHub cung cấp [60 giờ Codespaces miễn phí](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces) mỗi tháng. Nhớ **stop codespace sau khi dùng xong** để không vượt quota.

**Bước 1 — Fork repo về tài khoản của bạn**

Vào https://github.com/markxLee/InsightEngine, bấm nút **Fork**:

![Fork repo](assets/fork.png)

Điền thông tin fork (giữ nguyên mặc định) rồi bấm **Create fork**:

![Create fork](assets/create-fork.png)

**Bước 2 — Tạo Codespace**

Trong repo vừa fork, bấm **Code → Codespaces → Create codespace on main**:

![Create codespace](assets/create-codespace.png)

Chờ vài phút để Codespace khởi động. VS Code sẽ mở trong trình duyệt.

**Bước 3 — Cài extension GitHub Copilot**

Bấm icon **Extensions** (thanh bên trái), tìm **"copilot"**, chọn **GitHub Copilot** và bấm **Cài đặt**:

![Install Copilot](assets/install-copilot.png)

Đăng nhập GitHub nếu được hỏi.

**Bước 4 — Dùng InsightEngine**

> ⏱️ **Lần đầu tiên:** Cần cài các thư viện Python/Node.js, mất khoảng **2–3 phút**. Chỉ cần làm một lần duy nhất.
>
> ⚡ **Những lần sau:** Start lại codespace là dùng được ngay — không cần cài lại, môi trường đã được lưu.

Mở Copilot Chat (Ctrl+Alt+I hoặc icon chat trên thanh bên), rồi nhắn:

```
setup InsightEngine
```

Sau khi cài xong dependencies, thử ngay:

```
tìm kiếm về xu hướng AI 2025 và tổng hợp thành file Word
```

**Bước 5 — Stop Codespace sau khi dùng xong** ⚠️

Trong repo trên GitHub, bấm **Code → Codespaces**, bấm `...` bên cạnh codespace của bạn và chọn **Stop codespace**:

![Stop codespace](assets/stop-codespace.png)

> Xem chi tiết về quota và billing: https://docs.github.com/en/billing/concepts/product-billing/github-codespaces

---

### Option B — VS Code Local (khuyến nghị nếu dùng thường xuyên)

```bash
git clone https://github.com/<your-username>/InsightEngine
cd InsightEngine
code .
```

Mở Copilot Chat và nhắn `setup InsightEngine` để cài dependencies.

> **Lưu ý:** Image generation với Stable Diffusion chỉ chạy tốt trên Apple Silicon (M1/M2/M3). Các tính năng khác hoạt động trên mọi máy.

---

### Nâng cấp Copilot (tùy chọn)

**GitHub Copilot Free** có giới hạn số request mỗi tháng và chỉ truy cập được một số model nhất định.

**Nâng cấp lên Copilot Pro/Pro+** nếu muốn:
- Không giới hạn số request
- Truy cập đầy đủ các model cao cấp và model mới nhất

> Danh sách model theo từng gói thay đổi theo thời gian — xem thông tin mới nhất tại:

👉 https://github.com/settings/copilot/features

---

## 💡 Hướng dẫn sử dụng hiệu quả

> **InsightEngine là action workflow — không phải AI chat.** Mỗi câu yêu cầu kích hoạt một pipeline tự động: thu thập → tổng hợp → tạo file → kiểm tra chất lượng → giao kết quả. Bạn chỉ cần mô tả những gì bạn muốn.

### 1. Mô tả mục tiêu của bạn — bằng tiếng Việt tự nhiên

Không cần nhớ lệnh hay tên skill. Pipeline tự phân loại yêu cầu và chọn flow phù hợp.

**Prompt mẫu — Nghiên cứu & báo cáo:**
```
tìm hiểu về xu hướng AI 2025 và tổng hợp thành file Word phong cách corporate
```
```
phân tích thị trường fintech Đông Nam Á, so sánh top 5 công ty và làm slide dark-modern 15 trang
```
```
tổng hợp toàn bộ các mô hình ngôn ngữ lớn từ 2023 đến nay — benchmark, nhà phát triển, chi phí
```

**Prompt mẫu — Đọc file:**
```
đọc file input/meeting-notes.docx và tóm tắt thành email
```
```
đọc tất cả file trong thư mục input/ và gộp thành một báo cáo duy nhất
```
```
đọc báo cáo tài chính Q4 trong input/ và tạo dashboard Excel với biểu đồ
```

**Prompt mẫu — Tạo nhanh:**
```
tạo slide thuyết trình về blockchain cho người mới bắt đầu, 10 trang, minimal
```
```
tạo bảng Excel tổng hợp số liệu doanh thu Q1-Q4 với biểu đồ line chart
```
```
tạo certificate đẹp cho workshop AI ngày 20/4 — logo công ty, tên người nhận để trống
```

**Prompt mẫu — Nâng cao:**
```
tìm kiếm về AI trong giáo dục, tạo Excel tổng hợp số liệu, 
sau đó dùng số liệu làm slide thuyết trình 15 trang phong cách academic
```
```
đọc file input/product-roadmap.pdf, phân tích và tạo báo cáo Word + slide tóm tắt cho ban lãnh đạo
```

Pipeline sẽ hiển thị **kế hoạch thực hiện** trước khi chạy — bạn duyệt, điều chỉnh, hoặc bổ sung.
```
đọc file input/meeting-notes.docx và tóm tắt thành email
```
```
tạo slide thuyết trình về thị trường fintech Đông Nam Á
```
```
đọc tất cả file trong thư mục input/ và gộp thành một báo cáo duy nhất
```

Pipeline sẽ hiển thị **kế hoạch thực hiện** trước khi chạy — bạn duyệt, điều chỉnh, hoặc bổ sung.

---

### 2. Muốn output dài và chi tiết hơn? Nói rõ trong prompt

Mặc định tạo output ở mức vừa phải (~3,000–5,000 từ). Để nhận tài liệu chuyên sâu:

| Bạn muốn | Từ khóa nên thêm | Kết quả |
|----------|-----------------|---------|
| Tóm tắt nhanh | `"tóm tắt ngắn gọn"`, `"overview"` | ~1,000–2,000 từ |
| Báo cáo đầy đủ | *(mặc định)* | ~3,000–5,000 từ |
| Phân tích chuyên sâu | `"phân tích sâu"`, `"chi tiết"`, `"đầy đủ"` | ~8,000–15,000 từ |

---

### 3. Muốn tìm kiếm toàn diện? Mô tả nhiều chiều

Pipeline tự động kích hoạt **deep research** khi phát hiện yêu cầu phức tạp:
- Có **so sánh** ("so sánh A và B", "phân loại các loại...")
- Trải dài **thời gian** ("từ 2023 đến nay")
- Yêu cầu **đầy đủ** ("tất cả các mô hình", "toàn bộ thị trường")

**Ví dụ:**
```
tổng hợp toàn bộ các mô hình AI lớn từ 2023 đến nay — so sánh benchmark,
nhà phát triển, và ứng dụng thực tế — làm slide dark-modern
```

---

### 4. Chọn style phù hợp

Thêm tên style vào cuối yêu cầu để kiểm soát giao diện slide và HTML:

| Style | Dùng khi nào |
|-------|-------------|
| `corporate` | Báo cáo doanh nghiệp, tài liệu chính thức |
| `academic` | Nghiên cứu, luận văn, hội thảo |
| `minimal` | Tóm tắt nhanh, đơn giản |
| `dark-modern` | Tech talks, startup, công nghệ |
| `creative` | Marketing, sự kiện, workshop |

Nếu không chỉ định, pipeline tự chọn style phù hợp nhất.

---

### 5. Kết hợp nhiều đầu ra

InsightEngine hỗ trợ **output chaining** — tạo nhiều file liên kết nhau:

```
đọc file input/sales_data.xlsx, tạo biểu đồ bar chart và line chart,
rồi nhúng vào báo cáo Word kiểu corporate
```
```
tìm kiếm về AI trends 2025, tạo bảng Excel tổng hợp số liệu,
sau đó dùng số liệu đó làm slide thuyết trình 15 trang
```

---

### 6. Cung cấp file đầu vào

Đặt file cần xử lý vào thư mục `input/`. Hỗ trợ: Word, PDF, Excel, PowerPoint, Text, Markdown, URL, web search.

```
đọc tất cả file trong thư mục input/ và tổng hợp thành một báo cáo duy nhất
```

---

### 7. Kiểm tra chất lượng output

Pipeline tự động chấm điểm output (thang 100 điểm) trước khi giao. Nếu không đạt, tự sửa các phần yếu.

Bạn cũng có thể yêu cầu kiểm tra thủ công:
```
kiểm tra xem output có đúng yêu cầu không
```

---

### 9. Tự động cải thiện pipeline

Sau session làm việc, kích hoạt retrospective để pipeline tự học và cải tiến:
```
cải tiến quy trình từ session vừa rồi
```

---

### 10. Tiếp tục từ lần trước

Nếu pipeline bị gián đoạn (hết context, đổi session), trạng thái được lưu tự động. Chỉ cần nói:
```
tiếp tục
```

Pipeline sẽ tiếp tục từ bước đang dở, không cần bắt đầu lại.

---

## Architecture

```
User Request → orchestrator (central agent)
  ├─ Phân loại intent (synthesis / research / creation / design / data)
  ├─ Lên kế hoạch workflow
  ├─ Thu thập dữ liệu (files, URLs, web search)
  ├─ Tổng hợp & biên soạn nội dung
  ├─ Xuất file (Word / Excel / Slide / PDF / HTML / Chart / Image)
  ├─ Kiểm tra chất lượng (100-point audit)
  └─ Giao kết quả
```

InsightEngine là **action workflow**, không phải AI chat thông thường. Mỗi yêu cầu kích hoạt một pipeline tự động — thu thập dữ liệu, tổng hợp, tạo file, kiểm tra chất lượng, rồi trả kết quả. Bạn không cần nhớ lệnh hay biết pipeline chạy như thế nào.

---

## Tech Stack

| Component | Library |
|-----------|---------|
| File reading | `markitdown[all]` (Word, PDF, Excel, PPT, TXT, MD) |
| Word output | `python-docx` (3 style templates: corporate, academic, minimal) |
| Excel output | `openpyxl` + `pandas` (formulas, charts, formatting) |
| PPT output (Quick) | `pptxgenjs` (Node.js, 10 templates) |
| PPT output (Pro) | `ppt-master` SVG→PPTX pipeline (20+ layouts, 50+ charts, 6700+ icons) |
| PDF output | `reportlab` + `pypdf` (Vietnamese font support) |
| HTML output | `jinja2` + inline CSS (8 styles: corporate, academic, minimal, dark-modern, creative, warm-earth, dark-neon, dark-elegant) |
| Charts | `matplotlib` + `seaborn` (bar, line, pie, radar, scatter) |
| Visual design | `reportlab` Canvas + `Pillow` (posters, certificates, covers, infographics) |
| Image generation | `diffusers` + `torch/MPS` (Apple Silicon, SD-Turbo) |
| Web search | `vscode-websearchforcopilot_webSearch` |
| URL fetch | Copilot `fetch_webpage` (with Playwright fallback for JS-heavy sites) |

---

## Cơ chế tự động nâng cấp

InsightEngine tự cải thiện theo thời gian. Sau mỗi session làm việc, bạn có thể kích hoạt **retrospective** để pipeline phân tích những gì chưa tốt và tự đề xuất cải tiến:

```
cải tiến quy trình từ session vừa rồi
```

Pipeline sẽ:
1. Phân tích toàn bộ session (input → quá trình → output → gap)
2. Xác định nguyên nhân gốc rễ của các vấn đề
3. Đề xuất cải tiến cụ thể cho từng skill/agent
4. Tự tạo hoặc cập nhật skill nếu cần thiết
5. Kiểm tra lại để xác nhận cải tiến có hiệu quả

Skill mới và cải tiến được lưu vào `.github/skills/` và áp dụng ngay trong session tiếp theo — không cần deploy hay restart.

---

## License

MIT

