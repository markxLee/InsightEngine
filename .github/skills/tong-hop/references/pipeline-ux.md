# Pipeline UX — Full Reference

## Progress Messages

```yaml
PROGRESS_MESSAGES:
  step_start: "⏳ Đang {action}..."
  step_done: "✅ {action} hoàn tất → {next_action}"
  step_error: "❌ Lỗi tại bước {step}: {error_message}"

  examples:
    gathering: "⏳ Đang thu thập nội dung từ 3 nguồn..."
    gathered: "✅ Thu thập hoàn tất (3 nguồn, ~5,200 từ) → Đang biên soạn..."
    synthesizing: "⏳ Đang biên soạn và tổng hợp nội dung..."
    synthesized: "✅ Biên soạn hoàn tất → Đang tạo file Word..."
    generating: "⏳ Đang tạo file {format}..."
    generated: "✅ Tạo {format} hoàn tất: {file_path} ({file_size})"

  chain_progress: |
    📊 Tiến độ: {completed}/{total} bước
    ✅ {step_1_name}
    ✅ {step_2_name}
    ⏳ {current_step_name}...
    ⬜ {pending_step_name}

COPILOT_MUST:
  - Show progress message BEFORE starting each step
  - Show completion message with metrics AFTER each step
  - Include word count, file count, or file size in completion messages
  - Use Vietnamese for all progress messages
```

---

## Confirmation Gates

```yaml
CONFIRMATION_GATES:
  purpose: Ask user before time-consuming or resource-intensive steps

  triggers:
    image_generation:
      condition: Step involves tao-hinh image generation (not charts)
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
    thu-thap:
      file_read: "~5 giây/file"
      url_fetch: "~10 giây/URL"
      web_search: "~15 giây/truy vấn"
    bien-soan:
      synthesis: "~10 giây/1,000 từ input"
      translation: "~15 giây/1,000 từ"
    tao-word: "~10 giây"
    tao-excel: "~10 giây"
    tao-slide: "~15 giây"
    tao-pdf: "~10 giây"
    tao-html: "~5 giây"
    tao-hinh:
      chart: "~5 giây/biểu đồ"
      image: "~30-60 giây/hình (Apple Silicon)"

  display_format: |
    ⏱️ Thời gian ước tính:
    - Thu thập: ~{gather_time}
    - Biên soạn: ~{compile_time}
    - Tạo output: ~{output_time}
    → Tổng: ~{total_time}
```
