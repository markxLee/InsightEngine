# Data Collection Mode — Thu Thập Reference

## Overview

Data collection mode is fundamentally different from research mode. Instead of gathering
diverse perspectives on a topic, we're finding **specific items** (jobs, products, courses)
on **specific platforms** and extracting **structured fields** from each item's detail page.

The key principle: **every item in the output must have a direct URL to its detail page.**
A search result URL or listing page URL is never acceptable as a final output URL.

---

## Platform-Specific Search Strategy

### Why Not Generic Google?

When you search Google for "fresher javascript developer ho chi minh", you get:
- Google search result page (google.com/search?q=...) — NOT a job
- Overview articles about job markets — NOT individual jobs
- Platform homepage links (itviec.com, topcv.vn) — NOT specific jobs

What the user needs:
- itviec.com/it-jobs/frontend-developer-at-fpt-software-1234 — a SPECIFIC job
- topcv.vn/viec-lam/react-developer-tai-tiki-567890 — a SPECIFIC job

### How to Search Correctly

**Option A: Site-specific Google search**
```
vscode-websearchforcopilot_webSearch:
  query: "site:itviec.com fresher javascript developer ho chi minh 2026"
```
This returns individual job pages FROM itviec, not generic results.

**Option B: Direct platform search URLs**
Fetch the platform's own search page:
```
fetch_webpage:
  url: "https://itviec.com/it-jobs?query=javascript&city=ho-chi-minh&level=fresher"
  query: "job listings"
```
Then extract individual job links from the listing page.

**Option C: Both combined** (recommended)
Use Option A to find individual items across platforms, then use Option B to find additional
items on the most relevant platform.

---

## Two-Phase Fetch Protocol

### Phase 1: Discover Item URLs

Search across platforms to build a list of individual item URLs:

1. Run site-specific searches for each target platform
2. From search results, extract URLs that look like individual items
3. Also fetch platform listing pages directly
4. From listing pages, extract individual item links
5. Deduplicate by URL

**URL pattern recognition:**

| Platform | Listing page (OK for Phase 1) | Item page (needed for Phase 2) |
|----------|-------------------------------|-------------------------------|
| ITViec | itviec.com/it-jobs?query=... | itviec.com/it-jobs/title-at-company-123 |
| TopCV | topcv.vn/tim-viec-lam-... | topcv.vn/viec-lam/title-123456 |
| LinkedIn | linkedin.com/jobs/search/... | linkedin.com/jobs/view/1234567 |
| VietnamWorks | vietnamworks.com/tim-viec/... | vietnamworks.com/viec-lam/title-123.html |

### Phase 2: Fetch Item Details

For each individual item URL from Phase 1:

1. Fetch the item detail page using the standard 3-tier fallback
2. Extract required fields from the page content
3. Use the item URL as the `direct_url` field in output
4. If a field can't be extracted, mark as "Không rõ" (not blank)

**Efficiency:** Don't fetch all items if you have 100+ URLs. Prioritize:
- Items that match filter criteria based on title/snippet
- Items from top platforms first
- Stop at target quantity (e.g., 30 items)

---

## Field Extraction Patterns

When reading a fetched job page, look for these patterns:

```yaml
JOB_FIELDS:
  job_title:
    look_for: First <h1>, page title, "Tuyển dụng {title}"
    fallback: Extract from URL slug
  
  company_name:
    look_for: "at {company}", company section, employer info
    fallback: Extract from URL if format includes company name
  
  salary:
    look_for: "Lương:", "Salary:", "Mức lương:", specific numbers with "triệu"
    if_not_found: "Thương lượng" (many VN jobs hide salary)
  
  experience_required:
    look_for: "Kinh nghiệm:", "Experience:", "Yêu cầu kinh nghiệm"
    normalize_to: "Không yêu cầu" | "< 1 năm" | "1-2 năm" | etc.
  
  skills_required:
    look_for: "Yêu cầu:", "Requirements:", "Kỹ năng:", tech stack lists
    format: Comma-separated list of skills
  
  location:
    look_for: "Địa điểm:", "Location:", city names, "Remote"
    normalize_to: City name or "Remote"
  
  direct_url:
    value: The URL you fetched (the item page URL)
    NEVER: The Google search URL, the listing page URL, or a shortened URL
```

---

## Company Review Collection

When the user requests company reviews alongside items:

### Strategy

1. **After** collecting all items, extract unique company names
2. For each unique company (deduplicated), search for reviews:
   - `site:glassdoor.com "{company_name}" reviews`
   - `site:itviec.com/company/{company_slug}`
   - `"{company_name}" đánh giá nhân viên review`
3. Fetch the most relevant review page
4. Extract: overall rating, key themes, red flags
5. Store as supplementary data linked to company name
6. In output: add `company_review_url` and `company_review_summary` columns

### Efficiency

- Only fetch reviews for unique companies (if 5 jobs at FPT, 1 review fetch)
- Limit to top review source (Glassdoor preferred for rating consistency)
- Cap at 20 unique companies per run
- If review page blocked (Glassdoor is bot-protected), use Playwright stealth

---

## Quality Validation

After collection, validate before returning to pipeline:

```yaml
VALIDATION_CHECKLIST:
  ☐ All direct_urls point to individual item pages (no search/listing URLs)
  ☐ >70% of items have populated required fields
  ☐ Items match filter criteria (location, experience, skills)
  ☐ No duplicate items (same job from different platforms)
  ☐ Quantity meets target (or explain why not)
  ☐ Company reviews fetched for unique companies (if requested)
```

If validation fails, attempt 1 supplementary round targeting the specific gap.
