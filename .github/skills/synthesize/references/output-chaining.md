# Output Chaining — Full Reference

Handles multi-format pipelines where one output feeds the next.

## Chain Detection

```yaml
CHAIN_DETECTION:
  trigger:
    - User requests multiple output formats in one request
    - User says "rồi", "sau đó", "tiếp theo" between format requests
    - Example: "tạo bảng Excel rồi vẽ biểu đồ rồi đưa vào thuyết trình"

  common_chains:
    data_to_presentation:
      - tao-excel → tao-hinh (charts) → tao-slide (embed charts)
    report_multi_format:
      - bien-soan → tao-word + tao-pdf (parallel export)
    visual_report:
      - thu-thap → bien-soan → tao-hinh → tao-html (embed all)
```

## Chain Execution

```yaml
CHAIN_EXECUTION:
  1_DETECT:
    - Parse request for multiple output indicators
    - Identify dependencies between outputs
    - Build execution order (respect input/output deps)

  2_PRESENT_PLAN:
    format: |
      📋 Chuỗi xử lý:
      1. {step_1_skill} → {output_1}
      2. {step_2_skill} (input: {output_1}) → {output_2}
      3. {step_3_skill} (input: {output_2}) → {output_3}

      Thời gian ước tính: ~{estimated_time}
      Bạn đồng ý không?

  3_EXECUTE:
    - Execute steps sequentially (respect dependencies)
    - Pass output path of step N as input to step N+1
    - Store intermediate files in tmp/
    - Report progress after each step

  4_CLEANUP:
    - List all final output files
    - Remove intermediate files from tmp/
    - Report total files generated with paths and sizes

  5_REPORT:
    format: |
      Chuỗi output hoàn tất:
      - Bước 1: {file_1} ({size_1})
      - Bước 2: {file_2} ({size_2})
      - Bước 3: {file_3} ({size_3})
      Tổng: {total_files} file, {total_size}
```

## Intermediate Files

```yaml
INTERMEDIATE_FILES:
  directory: tmp/
  naming: "{timestamp}_{skill}_{step}.{ext}"
  cleanup: Auto-delete after chain completes
  on_error: Preserve intermediate files for debugging
```
