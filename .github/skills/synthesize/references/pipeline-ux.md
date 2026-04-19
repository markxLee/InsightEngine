# Pipeline UX — Full Reference

## Progress Messages

> **Full template set: `progress-messages.md`** — use those templates for all events.

```yaml
PROGRESS_MESSAGES:
  # Abbreviated reference — see progress-messages.md for complete set
  step_start: "⏳ Đang {action}..."   # or use specific template from progress-messages.md
  step_done: "✅ {action} hoàn tất → {next_action}"
  step_error: "❌ Lỗi: {user_friendly_message}"  # apply jargon-shield before showing

COPILOT_MUST:
  - Use templates from progress-messages.md (NOT improvised messages)
  - Fill ALL placeholders with actual values before displaying
  - Never show {placeholder} text to users
  - Apply jargon-shield substitutions on top of templates
  - In silent mode: show only collecting/done events + final delivery
```

---

## Confirmation Gates

```yaml
CONFIRMATION_GATES:
  purpose: Ask user before time-consuming or resource-intensive steps

  triggers:
    image_generation:
      condition: Step involves gen-image image generation (not charts)
      message: |
        ⚠️ Bước tiếp theo: Tạo hình ảnh minh họa (~30-60 giây)
        Bạn muốn tiếp tục không? (có/bỏ qua)

    large_file_processing:
      condition: Combined input > 30,000 words
      message: |
        ⚠️ Tổng dữ liệu đầu vào khá lớn (~{word_count} từ)
        Sẽ cần xử lý theo chunk. Tiếp tục? (có/không)

    multiple_outputs:
      condition: Chain has > 3 output steps
      message: |
        📋 Chuỗi xử lý gồm {step_count} bước.
        Thời gian ước tính: ~{estimated_time}
        Bạn xác nhận thực hiện? (có/không)
```

---

## Style Inference

```yaml
STYLE_INFERENCE:
  corporate:
    signals: "báo cáo", "công ty", "doanh nghiệp", "formal", "chuyên nghiệp"
    confidence: high if ≥2 signals match

  academic:
    signals: "nghiên cứu", "luận văn", "thesis", "khoa học", "research"
    confidence: high if ≥2 signals match

  minimal:
    signals: "đơn giản", "nhanh", "gọn", "clean", "simple"
    confidence: high if ≥1 signal match

  dark-modern:
    signals: "tech", "startup", "công nghệ", "developer", "dark mode"
    confidence: high if ≥1 signal match

  creative:
    signals: "marketing", "sự kiện", "event", "sáng tạo", "creative"
    confidence: high if ≥1 signal match

  suggestion_format: |
    💡 Gợi ý style: **{suggested_style}** (dựa trên nội dung yêu cầu)
    Các style có sẵn: corporate | academic | minimal | dark-modern | creative
    Bạn muốn dùng style nào?

  default: corporate (if no signals match)
```

---

## Time Estimation

```yaml
TIME_ESTIMATION:
  per_step_estimates:
    gather:
      file_read: "~5 giây/file"
      url_fetch: "~10 giây/URL"
      web_search: "~15 giây/truy vấn"
    compose:
      synthesis: "~10 giây/1,000 từ input"
      translation: "~15 giây/1,000 từ"
    gen-word: "~10 giây"
    gen-excel: "~10 giây"
    gen-slide: "~15 giây"
    gen-pdf: "~10 giây"
    gen-html: "~5 giây"
    gen-image:
      chart: "~5 giây/biểu đồ"
      image: "~30-60 giây/hình (Apple Silicon)"

  display_format: |
    ⏱️ Thời gian ước tính:
    - Thu thập: ~{gather_time}
    - Biên soạn: ~{compile_time}
    - Tạo output: ~{output_time}
    → Tổng: ~{total_time}
```
