---
name: kiem-tra
description: |
  Audit any InsightEngine output against the user's original requirements. Compares generated
  files (Excel, Word, Slide, PDF, HTML) against what the user actually asked for — checking
  requirement coverage, data completeness, URL quality, field accuracy, and content specificity.
  Works both as an automatic post-production step in the tong-hop pipeline AND as a standalone
  skill the user can invoke to verify any output.
  Always use this skill when: the user says "kiểm tra đầu ra", "audit output", "so sánh với
  yêu cầu", "check xem đã đúng chưa", "verify output", "output có đúng không", or when the
  tong-hop pipeline reaches Step 4.7. Also use when the user is unhappy with output quality
  and wants a structured analysis of what went wrong — "sai ở đâu", "thiếu gì", "tại sao
  không đúng", "what's missing", "why is this wrong". Do NOT use for general content quality
  reviews (depth, writing style) — those are handled by bien-soan's self-review loop.
  This skill specifically checks: did the output match what the user requested?
argument-hint: "[original request] [output file or content to audit]"
version: 1.1
compatibility:
  tools:
    - read_file
    - run_in_terminal (for file inspection)
---

# Kiểm Tra — Output Audit Skill

**References:** `references/audit-rubric.md`

This skill answers one question: **"Does the output actually match what the user asked for?"**

Quality gates in the pipeline check content depth, formatting, and file size — but they don't
check whether the output addresses the user's specific requirements. A beautifully formatted
20-page report is worthless if it doesn't answer the user's actual question. This skill closes
that gap.

Two modes of operation:
1. **Pipeline mode**: Called automatically by tong-hop at Step 4.7 after all output files
   are generated. Receives structured inputs (original request, required fields, output content).
2. **Standalone mode**: User invokes directly to audit any existing output. The skill reads
   the output file(s) and asks the user for their original requirements.

All responses to the user are in Vietnamese.

---

## Step 1: Gather Audit Inputs

### Pipeline mode (called from tong-hop):
Inputs are already structured:
- `original_request`: User's full original prompt
- `required_fields`: Structured field list (from Step 1 of tong-hop, if data_collection)
- `expanded_analysis`: Dimensions or collection plan from Step 1.5
- `output_files`: Generated file paths
- `output_content`: The actual content in the output

### Standalone mode (user invokes directly):
1. Ask user: "Bạn muốn kiểm tra file nào?" → get output file path(s)
2. Ask user: "Yêu cầu ban đầu của bạn là gì?" → get original request
3. Read the output file(s) using appropriate tool (read_file, markitdown)
4. Extract the content for analysis

---

## Step 2: Requirement Extraction

Parse the user's original request into a structured requirement checklist. Every distinct
thing the user asked for becomes a checkable item.

```yaml
REQUIREMENT_PARSING:
  method: |
    Read the original request sentence by sentence. For each sentence or clause:
    1. Is there a deliverable? (file, document, list, analysis)
    2. Is there a data requirement? (specific fields, items, information)
    3. Is there a quality requirement? (detailed, comprehensive, specific URLs)
    4. Is there a scope requirement? (location, time range, quantity)
    5. Is there a format requirement? (Excel, slides, charts)
  
  output_format:
    requirements:
      - id: R1
        text: "Tìm tất cả job fresher JS ở HCM"
        type: data_collection
        checkable_criteria:
          - "Jobs are specifically for fresher/< 1 year experience"
          - "Jobs are in HCM or remote"
          - "Jobs involve JavaScript/Node.js/React"
          - "Multiple jobs found (not just 1-2)"
      
      - id: R2
        text: "URL cụ thể của job"
        type: field_quality
        checkable_criteria:
          - "Each job has a URL"
          - "URL points to the specific job posting (not a search page)"
          - "URL is accessible/valid format"
      
      - id: R3
        text: "Review công ty"
        type: supplementary_data
        checkable_criteria:
          - "Company review information is present"
          - "Review source is identified (Glassdoor, ITViec reviews, etc.)"
          - "Review link is provided"
```

---

## Step 3: Execute Audit Checks

Run all applicable checks based on the request type and requirements:

### 3.1: Requirement Coverage Audit

For each requirement in the checklist:

```yaml
COVERAGE_CHECK:
  for_each_requirement:
    1. Search the output content for evidence that this requirement is addressed
    2. Grade:
       ✅ PASS: Requirement is fully addressed with specific data
       ⚠️ PARTIAL: Requirement is mentioned but incomplete or vague
       ❌ FAIL: Requirement is missing or not addressed
    3. Provide evidence: quote the relevant part of the output (or note its absence)
  
  example:
    R1: "Tìm tất cả job fresher JS ở HCM"
    grade: ⚠️ PARTIAL
    evidence: "Found 8 jobs but only 3 are specifically fresher-level. Others require 2-3 years."
    fix_suggestion: "Filter more strictly for fresher/entry-level positions"
```

### 3.2: URL Quality Audit (for data_collection requests)

**Automated validation available:** `python3 scripts/validate_urls.py`

```bash
# Validate URLs from command line
python3 scripts/validate_urls.py --urls "url1" "url2" "url3"

# Validate URLs from Excel output
python3 scripts/validate_urls.py --excel output/jobs.xlsx --column "URL"

# Get JSON output for programmatic use
python3 scripts/validate_urls.py --urls "url1" "url2" --json
```

The script classifies each URL as:
- ✅ DIRECT: Individual item page (has item ID/slug)
- ❌ SEARCH: Search results page (?q=, /search?)
- ❌ LISTING: Platform listing page without specific item
- ❓ AMBIGUOUS: Can't determine from URL pattern alone

Threshold: ≤30% bad URLs to pass. If the script isn't available, use manual URL pattern analysis:

```yaml
URL_AUDIT:
    1. CHECK URL PATTERN:
       - Search indicators: ?q=, /search?, /results?, /find?, /tag/, /category/
       - Platform listing pages: /jobs, /viec-lam (without specific job ID)
       - Direct item indicators: /jobs/12345, /viec-lam/abc-xyz-123, /job/detail/
    
    2. CLASSIFY:
       ✅ DIRECT: URL points to a specific item page (has item ID or slug)
       ⚠️ AMBIGUOUS: Can't determine from URL pattern alone
       ❌ SEARCH/LISTING: URL is clearly a search or listing page
    
    3. VERIFY (for ambiguous URLs):
       - Use fetch_webpage to check if the page has a single item vs a list
       - Only verify a sample (3-5 URLs) to save time
    
    result_format:
      total_urls: 25
      direct: 18 (72%)
      ambiguous: 4 (16%)
      search_listing: 3 (12%)
      verdict: "⚠️ 3 URLs là search links — cần thay thế bằng direct job links"
```

### 3.3: Field Completeness Audit (for data_collection requests)

```yaml
FIELD_AUDIT:
  for_each_required_field:
    1. Check: is this field present in the output structure?
    2. Check: what % of items have a value for this field?
    3. Check: are the values meaningful (not all "N/A" or empty)?
  
  result_format:
    fields:
      - field: "job_title"
        present: true
        fill_rate: "100%"
        quality: "✅ All have meaningful values"
      - field: "salary"
        present: true
        fill_rate: "60%"
        quality: "⚠️ 40% are 'Thương lượng' — acceptable but noted"
      - field: "direct_url"
        present: true
        fill_rate: "100%"
        quality: "❌ 12% are search links, not direct job URLs"
```

### 3.4: Specificity Audit (for all requests)

```yaml
SPECIFICITY_AUDIT:
  method: |
    Sample 5 key claims or data points from the output.
    For each, classify:
    ✅ SPECIFIC: Contains verifiable data (numbers, names, dates, URLs)
    ⚠️ SEMI-SPECIFIC: References real things but lacks precision
    ❌ VAGUE: Generic statement that could apply to anything
  
  example:
    sample_1:
      claim: "Nhiều công ty IT đang tuyển fresher JavaScript ở HCM"
      grade: ❌ VAGUE
      reason: "No company names, no job counts, no specific data"
      better: "ITViec có 45 job fresher JS tại HCM (tính đến 04/2026), TopCV có 28 job"
    
    sample_2:
      claim: "FPT Software tuyển Junior React Developer, lương 8-15 triệu, yêu cầu < 1 năm"
      grade: ✅ SPECIFIC
      reason: "Named company, specific position, salary range, experience requirement"
```

---

## Step 4: Generate Audit Report

```yaml
AUDIT_REPORT_FORMAT: |
  📋 **Báo cáo Kiểm Tra Đầu Ra**

  **Yêu cầu gốc:** {original_request_summary}
  **File kiểm tra:** {output_file_paths}

  ---

  ### 1. Phủ sóng yêu cầu ({met}/{total})
  | # | Yêu cầu | Kết quả | Ghi chú |
  |---|---------|---------|---------|
  | R1 | {requirement_1} | ✅/⚠️/❌ | {evidence} |
  | R2 | {requirement_2} | ✅/⚠️/❌ | {evidence} |
  ...

  {if data_collection:}
  ### 2. Chất lượng URLs ({direct_pct}% trực tiếp)
  - ✅ Direct links: {N}
  - ❌ Search/listing links: {M}
  - Cần fix: {specific_urls_to_fix}

  ### 3. Đầy đủ dữ liệu
  | Field | Có? | Fill rate | Chất lượng |
  |-------|-----|-----------|-----------|
  | {field_1} | ✅ | {pct}% | {quality} |
  ...
  {end if}

  ### {N}. Độ cụ thể ({specific_pct}% cụ thể)
  - Mẫu kiểm tra: {samples_checked} claims
  - Cụ thể: {specific_count} | Mơ hồ: {vague_count}

  ---

  ### Tổng kết
  **Đánh giá chung:** {overall_grade: PASS / PARTIAL / FAIL}
  
  {if PARTIAL or FAIL:}
  **Cần cải thiện:**
  1. {improvement_1}
  2. {improvement_2}
  ...
  
  **Đề xuất:** {remediation_suggestion}
  {end if}

OVERALL_GRADE:
  PASS: All requirements ✅, URLs valid, fields complete
  PARTIAL: Some ⚠️ but no ❌, minor gaps acceptable
  FAIL: Any ❌ requirement, or >30% URLs are search links, or critical fields missing
```

---

## Step 5: Remediation (if audit fails)

When called from the tong-hop pipeline:

```yaml
REMEDIATION:
  if_audit_fails:
    1. Report specific failures to the orchestrator
    2. Generate targeted fix instructions:
       - For URL issues: "Re-fetch these {N} items from platform pages, not search results"
       - For missing fields: "Need to fetch {field} from individual item pages"
       - For missing requirements: "Requirement R{N} not addressed — need additional search for {topic}"
    3. Orchestrator re-runs the relevant step with fix instructions
    4. Re-audit after fix (maximum 1 fix cycle from pipeline)
  
  if_standalone:
    1. Present full audit report to user
    2. Ask: "Bạn muốn tôi sửa những vấn đề này không?"
    3. If yes: generate fix plan and execute
    4. If no: save report for reference
```

---

## What This Skill Does NOT Do

- Does NOT evaluate writing quality or content depth (bien-soan handles that)
- Does NOT check formatting/layout (tao-<format> quality gates handle that)
- Does NOT generate content — only audits existing output
- Does NOT run automatically outside the tong-hop pipeline (unless user invokes)
