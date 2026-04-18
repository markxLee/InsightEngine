# Quality Gates — Full Criteria Reference

These are the specific pass/fail criteria for each pipeline step's quality gate.
The orchestrator (tong-hop) references this file when evaluating step outputs.

---

## General Protocol

```yaml
QUALITY_REVIEW_LOOP:
  after_each_step:
    1. Sub-skill produces output
    2. Orchestrator reviews output against QUALITY_CRITERIA for that step
    3. IF passes → proceed to next step
    4. IF fails → generate IMPROVEMENT_INSTRUCTIONS, re-execute step
    5. Maximum 2 retries per step
    6. After max retries, proceed with warning: "⚠️ Chất lượng bước {step} chưa
       đạt mức tối ưu. Tiếp tục với kết quả hiện tại — bạn có thể yêu cầu
       chỉnh sửa sau."

  REVIEW_MINDSET: |
    Review like a demanding expert reader, not a lenient validator. Ask:
    - Would I be proud to submit this to my boss?
    - Does this teach me something I didn't already know?
    - Are the claims backed by specific evidence, or are they vague platitudes?
    - Would a competing tool produce better output from the same inputs?
```

---

## THU-THAP Quality Gate

```yaml
THU_THAP_QUALITY_CRITERIA:
  volume_check:
    minimum_chars: 5000  # For standard requests
    minimum_chars_deep: 15000  # For deep research requests
    fail_action: "Thu thập chưa đủ dữ liệu. Tìm kiếm bổ sung với queries mở rộng."

  coverage_check:
    method: Check each expanded dimension from analysis against collected content
    fail_if: Any major dimension has < 500 chars of relevant content
    fail_action: "Thiếu dữ liệu về {missing_dimensions}. Tìm kiếm bổ sung."

  diversity_check:
    minimum_unique_sources: 3
    fail_action: "Nguồn dữ liệu quá tập trung. Tìm thêm từ nguồn khác."

  specificity_check:
    method: Scan for numeric data, proper nouns, dates in collected content
    fail_if: Content is mostly generic descriptions without specifics
    fail_action: "Nội dung thu thập quá chung chung, thiếu số liệu cụ thể. Tìm nguồn có data."

  url_fetch_escalation:
    note: thu-thap v1.2 handles Playwright escalation internally. Only retry for topic mismatch.

  # Additional checks for data_collection mode:
  data_collection_checks:
    url_specificity:
      method: Check URL patterns for search indicators (?q=, /search?, /results?)
      fail_if: >30% of URLs are search/listing pages
      fail_action: "URLs trỏ đến trang tìm kiếm. Cần fetch từng item page riêng lẻ."
    
    field_extraction:
      method: Check each item against required_fields list
      fail_if: Any required field is missing for >50% of items
      fail_action: "Thiếu dữ liệu {missing_fields}. Cần fetch lại từ trang chi tiết."
    
    item_quantity:
      method: Count collected items vs target from Step 1.5
      fail_if: Collected < 50% of target
      fail_action: "Mới thu thập {N}/{target} items. Cần mở rộng tìm kiếm trên thêm platforms."
```

---

## BIEN-SOAN Quality Gate (MOST CRITICAL)

```yaml
BIEN_SOAN_QUALITY_CRITERIA:
  depth_check:
    method: Read through the synthesized output and evaluate
    fail_if_any:
      - Average section length < 300 words (comprehensive) or < 200 words (standard)
      - More than 30% of sentences are generic (no specific data/examples)
      - Sections that just restate source content without analysis
      - Missing analytical paragraphs (what the facts mean, implications)
    fail_action: |
      "Nội dung biên soạn chưa đủ sâu. Cần bổ sung:
      - Thêm số liệu cụ thể và ví dụ cho các phần: {weak_sections}
      - Thêm phân tích (implications, trends) cho: {sections_without_analysis}
      - Mở rộng các phần quá ngắn: {short_sections}"

  specificity_check:
    method: Count specific data points (numbers, names, dates, examples, case studies)
    minimum_per_section: 3
    fail_action: "Nội dung quá chung chung. Cần thêm số liệu cụ thể, ví dụ, case study."

  structure_check:
    fail_if_any:
      - No H2/H3 hierarchy (flat structure)
      - Sections longer than 2000 words without sub-headings
      - No comparison tables where comparison data exists
      - No key takeaways at end of major sections
    fail_action: "Cấu trúc cần cải thiện: {specific_structural_issues}"

  analytical_depth_check:
    method: Check for analysis paragraphs, implications, trend identification, recommendations
    fail_if: More than half of sections are purely factual with no analysis
    fail_action: "Thiếu phân tích chuyên sâu. Mỗi phần cần có đoạn phân tích: xu hướng,
    ý nghĩa, khuyến nghị — không chỉ liệt kê sự kiện."
```

---

## OUTPUT Quality Gate

```yaml
OUTPUT_QUALITY_CRITERIA:
  completeness_check:
    method: Compare section count in input vs output
    fail_if: Output is missing sections or has significantly truncated content
    fail_action: "File đầu ra thiếu nội dung. Kiểm tra lại các phần: {missing_sections}"

  formatting_check:
    fail_if_any:
      - Tables with broken layouts
      - Missing headings or inconsistent hierarchy
      - Images overflowing margins
      - Empty pages or sections
    fail_action: "Lỗi format: {specific_issues}. Tạo lại file."

  size_sanity_check:
    minimum_size_kb:
      docx: 15
      pptx: 50
      pdf: 20
      html: 5
    fail_action: "File quá nhỏ — có thể thiếu nội dung. Kiểm tra lại."
```

---

## OUTPUT AUDIT Gate (Step 4.7 — kiem-tra)

```yaml
OUTPUT_AUDIT:
  trigger: ALWAYS — after all tao-<format> steps complete, before final report
  sub_skill: kiem-tra (see .github/skills/verify/SKILL.md)
  
  inputs:
    - original_request: The user's full original prompt (verbatim)
    - required_fields: From Step 1 extraction (if data_collection/mixed)
    - expanded_analysis: From Step 1.5 (dimensions or collection plan)
    - output_files: List of generated files with paths
    - output_content: The content that was put into the files
  
  checks_for_ALL_requests:
    requirement_coverage:
      method: |
        1. List every distinct requirement from user's prompt
        2. For each requirement, check: is it present in the output?
        3. Grade: ✅ fully addressed | ⚠️ partially addressed | ❌ missing
      fail_if: Any requirement is ❌ missing
    
    specificity_vs_vagueness:
      method: Sample 5 claims from the output — are they specific or generic?
      fail_if: More than 2/5 sampled claims are vague/unverifiable
  
  checks_for_data_collection:
    field_completeness:
      method: Check required_fields list against actual output columns
      fail_if: Any required field is missing from output structure
    
    url_quality:
      method: |
        For each URL in output:
        1. Check URL pattern — search indicators: ?q=, /search?, /results?, /find?
        2. Check if URL points to a specific item page
        3. Flag any URL that looks like a search results page
      fail_if: >30% of URLs are search/listing pages instead of individual item pages
      fail_action: |
        "⚠️ {N} URLs trỏ đến trang tìm kiếm thay vì trang job cụ thể.
        Cần thu thập lại với URLs trực tiếp từ các platform."
    
    data_quantity:
      method: Count rows/items in output vs target_quantity from Step 1.5
      fail_if: Collected < 50% of target quantity
    
    data_freshness:
      method: Check dates, "đã hết hạn", expired indicators
      warn_if: Any items appear outdated

  on_audit_failure:
    1. Report specific failures to user with details
    2. Propose remediation
    3. If user approves, re-run failed steps with targeted fix instructions
    4. Maximum 1 audit-fix cycle
    5. After fix cycle, re-audit and report final status

  on_audit_pass:
    report: |
      ✅ Kiểm tra đầu ra:
      - Yêu cầu: {total_requirements} → {met} đã đáp ứng, {partial} một phần
      - Dữ liệu: {total_items} items, {fields_complete}% đầy đủ fields
      - URLs: {valid_urls}% là links trực tiếp
```
