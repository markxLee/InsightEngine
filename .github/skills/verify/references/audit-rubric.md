# Audit Rubric — Structured Scoring Template

> Reusable scoring framework for comparing output against user requirements.  
> Used by kiem-tra in both pipeline and standalone modes.

---

## Scoring Dimensions

| # | Dimension | Weight | What It Checks |
|---|-----------|--------|---------------|
| 1 | Requirement Coverage | 35% | Every explicit requirement from user addressed? |
| 2 | Data Specificity | 25% | Specific data, numbers, examples, URLs (not generic text)? |
| 3 | Field Completeness | 20% | Required fields all populated? (data_collection mode) |
| 4 | Format Compliance | 10% | Output in requested format, correct structure? |
| 5 | Factual Accuracy | 10% | No contradictions, outdated info, or fabricated data? |

---

## Scoring Scale (per dimension)

| Score | Label | Meaning |
|-------|-------|---------|
| 90-100 | Excellent | Fully meets or exceeds expectations |
| 70-89 | Good | Meets most expectations, minor gaps |
| 50-69 | Adequate | Notable gaps but core request addressed |
| 30-49 | Poor | Significant missing content or errors |
| 0-29 | Failing | Does not address the request |

---

## Audit Checklist Template

```yaml
AUDIT_CHECKLIST:
  requirement_coverage:
    items:
      - requirement: "[extracted from user request]"
        status: covered | partial | missing
        evidence: "[quote or reference from output]"
        score: 0-100
    dimension_score: weighted_average

  data_specificity:
    checks:
      - has_numbers: true | false
      - has_named_entities: true | false  # companies, products, people
      - has_examples: true | false
      - has_urls: true | false  # for data_collection
      - generic_text_ratio: 0-100%  # lower is better
    dimension_score: 0-100

  field_completeness:
    # Only for data_collection mode
    fields:
      - field_name: "[from required_fields]"
        populated: N / total_rows
        empty_rate: 0-100%
        quality: valid | partial | placeholder
    dimension_score: 0-100

  format_compliance:
    checks:
      - correct_format: true | false  # .docx, .xlsx, .pptx as requested
      - file_exists: true | false
      - file_size_reasonable: true | false
      - structure_matches: true | false  # sections, sheets, slides present
    dimension_score: 0-100

  factual_accuracy:
    # Spot-check up to 5 claims
    spot_checks:
      - claim: "[specific claim from output]"
        verifiable: true | false
        accurate: true | false | unverified
    dimension_score: 0-100
```

---

## Overall Score Calculation

```yaml
SCORING:
  formula: |
    overall = (requirement_coverage × 0.35)
            + (data_specificity × 0.25)
            + (field_completeness × 0.20)  # 0 if not data_collection → redistribute
            + (format_compliance × 0.10)
            + (factual_accuracy × 0.10)

  when_not_data_collection:
    # Redistribute field_completeness weight
    requirement_coverage: 45%
    data_specificity: 30%
    format_compliance: 15%
    factual_accuracy: 10%

  result_thresholds:
    pass: overall >= 70
    warning: 50 <= overall < 70
    fail: overall < 50
```

---

## Report Format (Vietnamese)

```yaml
REPORT_TEMPLATE: |
  ## 📋 Kết quả kiểm tra

  **Score tổng: {overall_score}/100** — {result_label}

  | Tiêu chí | Score | Đánh giá |
  |----------|-------|----------|
  | Độ phủ yêu cầu | {req_score} | {req_label} |
  | Độ cụ thể dữ liệu | {data_score} | {data_label} |
  | Hoàn thiện trường dữ liệu | {field_score} | {field_label} |
  | Đúng định dạng | {format_score} | {format_label} |
  | Độ chính xác | {accuracy_score} | {accuracy_label} |

  ### ✅ Điểm mạnh
  {strengths_list}

  ### ⚠️ Vấn đề cần cải thiện
  {issues_list}

  ### 📌 Khuyến nghị
  {recommendations}
```
