# Progress Message Templates — Reference

## Overview

This reference provides user-friendly Vietnamese progress messages for every
pipeline event. All messages comply with jargon-shield rules (see jargon-shield.md):
- No library names
- No script paths
- Outcome-focused
- Short (1-2 sentences)

---

## Core Template Set

### Phase: Intake & Planning

```yaml
INTAKE:
  analyzing:         "🔍 Đang phân tích yêu cầu..."
  plan_ready:        "📋 Kế hoạch thực hiện đã sẵn sàng."
  starting:          "🚀 Bắt đầu thực hiện..."
  resuming:          "▶️ Tiếp tục từ bước trước..."
```

### Phase: Gathering Content

```yaml
GATHER:
  starting_files:    "📂 Đang đọc tài liệu nguồn ({count} file)..."
  file_done:         "📂 Đã đọc {count} file ({total_words} từ)"
  
  starting_urls:     "🌐 Đang lấy nội dung từ {count} địa chỉ..."
  url_done:          "🌐 Đã lấy {count}/{total} địa chỉ"
  url_retry:         "⚠️ Thử lại địa chỉ {n} ({attempt}/2)..."
  url_failed:        "⚠️ Bỏ qua 1 địa chỉ không truy cập được"
  
  starting_search:   "🔍 Đang tìm kiếm thông tin về {topic}..."
  search_done:       "🔍 Tìm thấy nội dung từ {count} nguồn"
  
  summary:           "✅ Thu thập xong — {total_words} từ từ {source_count} nguồn"
```

### Phase: Data Collection (structured items)

```yaml
DATA_COLLECTION:
  starting:          "🔍 Bắt đầu thu thập {entity_type}..."
  
  platform_start:    "🔍 Đang tìm trên {platform}..."
  platform_done:     "🔍 {platform}: ✅ {count} {entity_type}"
  platform_failed:   "🔍 {platform}: ⚠️ Không tìm được, thử nguồn khác"
  
  dedup:             "🔄 Loại trùng: còn {final_count} ({removed} trùng)"
  
  progress:          "📊 Đã thu thập: {count}/{target} {entity_type}"
  summary:           "✅ Thu thập xong — {total} {entity_type} từ {platform_count} nguồn"
```

### Phase: Synthesizing / Writing

```yaml
COMPOSE:
  starting:          "✍️ Đang biên soạn nội dung..."
  section_done:      "✍️ Đã viết phần {n}/{total}: {section_name}"
  reviewing:         "🔎 Kiểm tra chất lượng nội dung..."
  rewriting:         "✍️ Cải thiện phần {section_name}..."
  done:              "✅ Biên soạn xong ({word_count} từ)"
  
  translating:       "🌏 Đang dịch nội dung..."
  translated:        "✅ Dịch xong ({word_count} từ)"
```

### Phase: Generating Files

```yaml
GEN_WORD:
  starting:          "📄 Đang tạo file Word..."
  done:              "✅ File Word đã sẵn sàng: {file_path} ({file_size})"
  
GEN_EXCEL:
  starting:          "📊 Đang tạo file Excel..."
  adding_data:       "📊 Đang điền dữ liệu ({row_count} dòng)..."
  recalculating:     "📊 Đang tính toán công thức..."
  done:              "✅ File Excel đã sẵn sàng: {file_path} ({file_size})"
  
GEN_SLIDE:
  starting:          "🎯 Đang tạo file thuyết trình..."
  building_slides:   "🎯 Đang dựng {slide_count} slide..."
  done:              "✅ File thuyết trình đã sẵn sàng: {file_path} ({file_size})"
  
GEN_PDF:
  starting:          "📄 Đang tạo file PDF..."
  done:              "✅ File PDF đã sẵn sàng: {file_path} ({file_size})"
  
GEN_HTML:
  starting:          "🌐 Đang tạo trang web..."
  done:              "✅ Trang web đã sẵn sàng: {file_path} ({file_size})"
  
GEN_IMAGE:
  starting_chart:    "📈 Đang vẽ biểu đồ {chart_type}..."
  chart_done:        "📈 Biểu đồ {chart_type}: ✅ {file_path}"
  starting_image:    "🎨 Đang tạo hình ảnh... (~30-60 giây)"
  image_done:        "🎨 Hình ảnh đã sẵn sàng: {file_path}"
  
DESIGN:
  starting:          "🎨 Đang thiết kế {design_type}..."
  done:              "✅ Thiết kế {design_type} hoàn tất: {file_path}"
```

### Phase: Quality Check

```yaml
QUALITY:
  checking:          "🔎 Đang kiểm tra chất lượng đầu ra..."
  passed:            "✅ Kiểm tra đạt ({score}/100)"
  improving:         "🔧 Đang cải thiện {aspect}..."
  passed_after_fix:  "✅ Kiểm tra đạt sau khi cải thiện"
  warning:           "⚠️ Chất lượng chấp nhận được (có thể cải thiện thêm)"
```

### Phase: Errors

```yaml
ERRORS:
  deps_missing:      "⚠️ Một số công cụ chưa được cài. Gõ 'setup' để cài tự động."
  source_failed:     "⚠️ Không truy cập được 1 nguồn. Tiếp tục với các nguồn còn lại."
  partial_failure:   "⚠️ Một bước xử lý gặp lỗi. Tiếp tục với kết quả hiện có."
  total_failure:     "❌ Không thể hoàn thành do lỗi nghiêm trọng. Chi tiết bên dưới."
  low_data:          "⚠️ Chỉ thu thập được {count} {entity_type} (thấp hơn mục tiêu). Tiếp tục tạo file."
```

---

## Final Delivery Summary Templates

```yaml
FINAL_DELIVERY:
  single_file: |
    ✅ **Hoàn thành!**
    📄 {file_type}: [{file_name}]({file_path}) ({file_size})
    
  multiple_files: |
    ✅ **Hoàn thành! {file_count} file đã tạo:**
    📄 {file_type_1}: [{file_name_1}]({path_1}) ({size_1})
    📊 {file_type_2}: [{file_name_2}]({path_2}) ({size_2})
    ...
    
  with_stats: |
    ✅ **Hoàn thành!**
    📄 {output_summary}
    📊 Nội dung: {content_summary}
    
  data_collection: |
    ✅ **Hoàn thành thu thập dữ liệu!**
    📊 [{file_name}]({file_path}) — {row_count} {entity_type}, {column_count} trường
    🔍 Nguồn: {platform_list}
    
  with_quality: |
    ✅ **Hoàn thành!**
    📄 {file_type}: [{file_name}]({file_path}) ({file_size})
    ⭐ Chất lượng: {quality_emoji} {score}/100
    
# Quality emoji mapping:
#   90-100: ⭐⭐⭐ xuất sắc
#   75-89:  ⭐⭐ tốt
#   60-74:  ⭐ chấp nhận được
#   <60:    ⚠️ cần cải thiện (automatic retry triggered before this)
```

---

## Chain Progress Template

When multiple output files are generated in a chain:

```yaml
CHAIN_PROGRESS:
  format: |
    📊 Tiến độ: {completed}/{total} bước
    {✅/⏳/⬜} {step_1_label}
    {✅/⏳/⬜} {step_2_label}
    ...
    
  step_labels:
    gather:    "Thu thập nội dung"
    compose:   "Biên soạn"
    gen-word:  "Tạo file Word"
    gen-excel: "Tạo file Excel"
    gen-slide: "Tạo thuyết trình"
    gen-pdf:   "Tạo file PDF"
    gen-html:  "Tạo trang web"
    gen-image: "Tạo biểu đồ"
    design:    "Thiết kế"
    verify:    "Kiểm tra chất lượng"
```

---

## Application Rules

1. **Always use these templates** — do not improvise new message text
2. **Fill placeholders** with actual values — never leave `{placeholder}` in output
3. **Omit optional fields** if data unavailable — don't show empty placeholders
4. **Apply jargon-shield substitutions** on top of these templates
5. **In silent mode**: only show `platform_done`, `summary`, and `FINAL_DELIVERY`
