---
name: verify
description: |
  Intelligence-driven audit: Copilot READS output content, OPENS URLs to verify, COMPARES
  data against actual web pages, and REASONS about quality — not just script-based rule checks.
  The key difference: this skill makes Copilot act as a human reviewer who actually clicks
  links, reads pages, and judges whether the output is truthful and complete.
  Works as tong-hop Step 4.7 (automatic) or standalone when user says "kiểm tra", "audit",
  "check xem đúng chưa", "sai ở đâu", "thiếu gì", "verify output".
argument-hint: "[original request] [output file or content to audit]"
version: 2.0
compatibility:
  tools:
    - read_file
    - fetch_webpage (CRITICAL — for URL verification)
    - run_in_terminal
---

# Kiểm Tra — Intelligence-Driven Output Audit

**References:** `references/audit-rubric.md`

## Core Principle: READ → VERIFY → REASON (not script → rules → report)

```
❌ OLD WAY: Run validate_urls.py → check URL patterns → report pass/fail
✅ NEW WAY: Open each URL with fetch_webpage → read the page → judge:
            "Is this actually a job posting? Does it match the data in our output?"
```

**You are a human reviewer, not a script runner.** For every audit check:
1. **READ** the actual output content (not just metadata)
2. **VERIFY** claims by going to the source (fetch URLs, re-search topics)
3. **REASON** about whether the output genuinely serves the user's need
4. **COMPARE** output data against what the source page actually says

---

## Step 1: Gather Audit Inputs

### Pipeline mode (from tong-hop Step 4.7):
Inputs already available: `original_request`, `required_fields`, `expanded_analysis`,
`output_files`, `output_content`.

### Standalone mode:
1. Ask: "Bạn muốn kiểm tra file nào?" → get file path
2. Ask: "Yêu cầu ban đầu là gì?" → get original request
3. Read the output file with read_file or markitdown

---

## Step 2: Requirement Extraction

Parse user's original request into checkable items:
- Each distinct deliverable, data field, scope constraint, format requirement → one checklist item
- Label each: R1, R2, R3...
- For data_collection: each required field + "direct URLs to item pages" is always an implicit requirement

---

## Step 3: Intelligence-Driven Audit

### 3.1: Requirement Coverage (READ output, REASON about each requirement)

For each requirement Rn:
1. **Read** the output content — find where this requirement is addressed
2. **Quote** the exact output text that addresses it (or note absence)
3. **Reason**: does the quoted content actually satisfy what the user wanted?
   - Not just "is the word mentioned" but "is the user's need met?"
4. Grade: ✅ PASS | ⚠️ PARTIAL | ❌ FAIL

### 3.2: URL Verification (OPEN URLs — THE MOST CRITICAL CHECK)

```
╔══════════════════════════════════════════════════════════════════════╗
║  🔗 YOU MUST ACTUALLY OPEN URLs WITH fetch_webpage AND READ THEM   ║
║  Do NOT just check URL patterns. Do NOT just run a script.         ║
║  OPEN the URL. READ the page. JUDGE the content.                   ║
╚══════════════════════════════════════════════════════════════════════╝
```

**For data_collection/mixed outputs — verify ALL URLs (or sample 5-10 if >15):**

For each URL in the output:
1. **OPEN** the URL using `fetch_webpage`
2. **READ** the page content returned
3. **JUDGE** — answer these questions:
   - Is this an individual item page (job posting, product detail) or a search/listing page?
   - Does the page title/content match the item title in our output?
   - Does the salary/price on the page match what we reported?
   - Does the company/brand match?
   - Is the page still live (not 404, not redirected to homepage)?
4. **COMPARE** — for each field in our output, check against the actual page:
   ```
   Our output says: "FPT Software, Senior React Dev, 15-25 triệu"
   Page actually says: "FPT Software, Senior React Developer, Lương: Thương lượng"
   → ⚠️ Salary mismatch: we reported 15-25M but page says "Thương lượng"
   ```
5. **VERDICT** per URL:
   - ✅ VERIFIED: Page is real item, data matches output
   - ⚠️ MISMATCH: Page is real item but some fields don't match
   - ❌ WRONG: Page is search/listing, or 404, or completely different item
   - ❌ FABRICATED: URL returns no relevant content / domain doesn't exist

**Report format for URL verification:**
```
🔗 Kiểm tra URL (đã mở và đọc {N} URLs):

| # | URL | Loại trang | Khớp dữ liệu? | Chi tiết |
|---|-----|-----------|---------------|----------|
| 1 | itviec.com/it-jobs/react-dev-fpt-123 | ✅ Job posting | ✅ Khớp | Title, company đúng |
| 2 | topcv.vn/viec-lam/js-dev-456 | ✅ Job posting | ⚠️ Sai lương | Output: 15M, thực tế: Thương lượng |
| 3 | google.com/search?q=jobs | ❌ Search page | ❌ | Không phải job posting |
```

### 3.3: Content Cross-Verification (for research reports)

**For research outputs — verify key claims against sources:**

Sample 5 key claims/data points from the output. For each:
1. **IDENTIFY** the claim and its implied source
2. **SEARCH** or **FETCH** to verify — use web search or fetch the cited URL
3. **COMPARE** what the output says vs what the source actually says
4. Grade: ✅ VERIFIED | ⚠️ UNVERIFIABLE | ❌ WRONG

```
Claim: "GPT-4o đạt 86.5% trên MMLU benchmark (OpenAI, 2024)"
Action: Search "GPT-4o MMLU benchmark score"
Source says: "GPT-4o: 88.7% on MMLU" (OpenAI blog)
→ ⚠️ Score slightly off (86.5 vs 88.7) — minor factual error
```

### 3.4: Field Completeness (data_collection — READ actual values, not just structure)

Don't just check "does the column exist" — READ the actual cell values:
1. How many items have real, meaningful values vs "N/A", "Không rõ", empty?
2. Are the values plausible? (salary "1 tỷ/tháng" for fresher job = suspicious)
3. Are fields copy-pasted across rows? (all items have identical descriptions = AI fabrication)

---

## Step 4: Audit Report

```
📋 **Báo cáo Kiểm Tra (Intelligence-Driven)**

**Yêu cầu gốc:** {summary}
**File kiểm tra:** {paths}
**Phương pháp:** Copilot đã đọc output, mở {N} URLs, so sánh nội dung thực tế

---
### 1. Phủ sóng yêu cầu ({met}/{total})
| # | Yêu cầu | Kết quả | Bằng chứng |
|---|---------|---------|------------|
| R1 | ... | ✅/⚠️/❌ | {quote from output or "không tìm thấy"} |

### 2. Xác thực URL ({verified}/{total} URLs đã mở và đọc)
| # | URL | Trang thực tế | Khớp dữ liệu? | Chi tiết |
|---|-----|-------------|---------------|----------|
{table}
**Phát hiện:** {N} URLs là trang tìm kiếm, {M} URLs có dữ liệu sai

### 3. Xác thực nội dung ({verified}/{sampled} claims kiểm chứng được)
{claim verification results}

### 4. Đầy đủ dữ liệu
{field analysis with actual value quality, not just fill rate}

---
### Tổng kết
**Đánh giá:** {PASS / PARTIAL / FAIL}
**Phương pháp xác thực:** Đã mở {N} URLs, so sánh {M} claims, đọc {K} trang thực tế

{if PARTIAL or FAIL:}
**Vấn đề cụ thể:**
1. {issue + evidence}
2. {issue + evidence}

**Đề xuất sửa:**
1. {specific fix with instructions}
{end if}
```

**Grading:**
- **PASS**: All requirements met, ≥80% URLs verified as real items with matching data
- **PARTIAL**: Requirements mostly met, some URL/data mismatches but output is usable
- **FAIL**: Key requirements missed, OR >30% URLs are fake/wrong, OR major data fabrication

---

## Step 5: Remediation

**Pipeline mode:** Report failures → generate specific re-fetch instructions → orchestrator re-runs.
**Standalone:** Present report → ask user "Bạn muốn tôi sửa không?" → execute fixes if yes.

Fix instructions must be specific:
- ❌ "Fix the URLs" → too vague
- ✅ "Re-fetch items #3, #7, #12 from itviec.com — current URLs are search pages. Need: specific job page URL, verify salary matches"

---

## What This Skill Does NOT Do

- Does NOT evaluate writing style or content depth (bien-soan handles that)
- Does NOT check formatting/layout (tao-format quality gates handle that)
- Does NOT run validate_urls.py as primary method — script is supplementary only
- Does NOT generate content — only audits and verifies existing output
