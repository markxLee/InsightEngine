# InsightEngine

Pipeline tổng hợp nội dung đa nguồn → đa định dạng đầu ra.

Transform scattered information from documents, spreadsheets, web content, and other sources into structured reports, presentations, charts, and more — all orchestrated by AI skills.

## Skills

| Skill | Purpose | Command |
|-------|---------|---------|
| **tong-hop** | Pipeline orchestrator — analyzes intent, coordinates sub-skills | `/tong-hop` |
| **thu-thap** | Gather content from files, URLs, web search | `/thu-thap` |
| **bien-soan** | Synthesize, merge, translate (Vi↔En), chunk large docs | `/bien-soan` |
| **tao-word** | Create professional Word (.docx) with 3 style templates | `/tao-word` |
| **tao-excel** | Create Excel (.xlsx) with formulas, formatting, recalc | `/tao-excel` |
| **tao-slide** | Create PowerPoint (.pptx) with 5 style templates | `/tao-slide` |
| **tao-pdf** | Create PDF with reportlab, Vietnamese font support | `/tao-pdf` |
| **tao-html** | Create static HTML pages with 5 style templates | `/tao-html` |
| **tao-hinh** | Charts (matplotlib) + image generation (Apple Silicon) | `/tao-hinh` |
| **cai-dat** | Install/verify dependencies | `/cai-dat` |

## Pipeline Flow

```
User Request → tong-hop (orchestrator)
  ├─ thu-thap (gather from files/URLs/web)
  ├─ bien-soan (synthesize + translate)
  └─ tao-[format] (output)
       ├─ tao-word (.docx)
       ├─ tao-excel (.xlsx)
       ├─ tao-slide (.pptx)
       ├─ tao-pdf (.pdf)
       ├─ tao-html (.html)
       └─ tao-hinh (charts/images → PNG)
```

## Template Styles

5 styles available for slides and HTML:

| Style | Vibe | Best For |
|-------|------|----------|
| **corporate** | Blue accent, professional | Business reports, formal docs |
| **academic** | Serif, structured | Research papers, thesis |
| **minimal** | Whitespace, clean | Quick summaries, clean docs |
| **dark-modern** | Dark bg, neon accents | Tech talks, startup pitches |
| **creative** | Vibrant gradients, playful | Marketing, events, workshops |

## Key Features

- **Output Chaining**: Pipeline multiple outputs (e.g., Excel → Chart → PPT)
- **Large Document Chunking**: Process documents >50,000 words via chunking
- **Translation**: Vietnamese ↔ English with quality checks
- **Web Search**: Integrated Google search via Copilot tools
- **Chart Generation**: Bar, line, pie, radar, scatter with consistent palette
- **Image Generation**: Text-to-image with SD-Turbo on Apple Silicon (optional)
- **Progress UX**: Step-by-step Vietnamese progress messages, time estimates, style suggestions

## Tech Stack

| Component | Library |
|-----------|---------|
| File reading | markitdown[all] |
| Word output | python-docx |
| Excel output | openpyxl + pandas |
| PPT output | pptxgenjs (Node.js) |
| PDF output | reportlab + pypdf |
| HTML output | jinja2 + inline CSS |
| Charts | matplotlib + seaborn |
| Images | diffusers + torch/MPS (Apple Silicon) |
| Web search | vscode-websearchforcopilot_webSearch |

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

> ⏱️ **Lần đầu tiên:** Bước `/cai-dat` sẽ cài các thư viện Python/Node.js cần thiết, mất khoảng **2–3 phút**. Chỉ cần làm một lần duy nhất.
>
> ⚡ **Những lần sau:** Start lại codespace là dùng được ngay — không cần cài lại, môi trường đã được lưu.

Mở Copilot Chat (Ctrl+Alt+I hoặc icon chat trên thanh bên), rồi gõ:

```
/cai-dat
```

Sau khi cài xong dependencies, thử ngay:

```
/tong-hop tìm kiếm về xu hướng AI 2025 và tổng hợp thành file Word
```

```
/tong-hop đọc file input/my-report.pdf và tạo thuyết trình 10 slide style corporate
```

```
/tong-hop tổng hợp dữ liệu từ 3 URL sau thành bảng Excel với biểu đồ
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

Mở Copilot Chat và chạy `/cai-dat` để cài dependencies.

> **Lưu ý:** Image generation (`tao-hinh` với SD-Turbo) chỉ chạy tốt trên Apple Silicon (M1/M2/M3). Các tính năng khác hoạt động trên mọi máy.

---

### Nâng cấp Copilot (tùy chọn)

GitHub Copilot Free có giới hạn request/tháng. Nếu muốn dùng model cao cấp hơn (Claude Sonnet, GPT-4o) và không giới hạn:

👉 https://github.com/settings/copilot/features

## License

MIT
