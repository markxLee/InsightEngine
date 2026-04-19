# Data Collection Mode — Reference

## When Data Collection Mode Activates

Data collection mode is for requests where the user wants **specific items** collected with
**structured fields** — not knowledge synthesis. The distinction is critical because the
pipeline behavior is fundamentally different.

### Research mode (default):
- Input: topic/question → Output: synthesized document about that topic
- gather: search broadly, gather diverse perspectives
- compose: merge, analyze, write prose
- Example: "Tổng hợp về xu hướng AI 2026" → a report about AI trends

### Data collection mode:
- Input: entity type + filter criteria → Output: structured list of specific items
- gather: search platform-specific, fetch individual item pages, extract fields
- Output: Excel/table with rows = items, columns = fields
- Example: "Tìm tất cả job fresher JS ở HCM" → Excel with 30 job rows

### Mixed mode:
- Both of the above — collect items, then analyze them
- Example: "Tìm jobs, tạo Excel, rồi tạo slide phân tích"

---

## Search Strategy for Data Collection

The biggest failure mode is using generic Google search for data collection. Generic searches
return overview/listing pages, not individual items. For data collection, you need to:

### 1. Identify Target Platforms

```yaml
PLATFORM_SELECTION:
  for_jobs_vietnam:
    primary:
      - ITViec.com (IT-specific, best for tech jobs in Vietnam)
      - TopCV.vn (broad, popular in Vietnam)
      - LinkedIn.com/jobs (international + remote)
    secondary:
      - VietnamWorks.com (established platform)
      - CareerBuilder.vn
      - Indeed.com (broad reach)
    review_sources:
      - Glassdoor.com (company reviews + salary data)
      - ITViec.com/review (IT company reviews in Vietnam)
      - CareerViet.vn reviews

  for_products:
    - Platform depends on product type
    - E-commerce: Shopee, Tiki, Amazon, Lazada
    - Electronics: Thegioididong, CellphoneS, FPTShop
    - Software: G2, Capterra, ProductHunt

  for_courses:
    - Udemy, Coursera, edX (international)
    - Funix, Techmaster, CodeGym (Vietnam)
```

### 2. Construct Platform-Specific Queries

```yaml
QUERY_STRATEGY:
  # DO NOT use generic Google queries for data collection
  # Instead, target specific platforms

  bad_approach:
    query: "fresher javascript developer ho chi minh"
    result: Google search results page → overview articles, NOT individual job listings
  
  good_approach:
    queries:
      - "site:itviec.com fresher javascript developer ho chi minh"
      - "site:topCV.vn javascript fresher ho chi minh"
      - "site:linkedin.com/jobs javascript developer fresher vietnam"
    result: Individual job listing pages from each platform

  even_better_approach:
    # Navigate directly to platform search URLs
    direct_urls:
      - "https://itviec.com/it-jobs?query=javascript&city=ho-chi-minh&level=fresher"
      - "https://www.topcv.vn/tim-viec-lam-javascript-tai-ho-chi-minh"
    # Then extract individual job links from the listing page
    # Then fetch each individual job page for detailed data
```

### 3. Two-Phase Fetching

```yaml
FETCH_PROTOCOL:
  phase_1_listing:
    # First, get the listing/search results page FROM THE PLATFORM
    # (not Google search results)
    action: Fetch platform search page (e.g., itviec.com/it-jobs?query=...)
    extract: List of individual item URLs from the listing
    note: A listing page ON the platform is acceptable as Phase 1 input
    
  phase_2_detail:
    # Then, fetch each INDIVIDUAL ITEM page
    action: Fetch each item URL (e.g., itviec.com/it-jobs/frontend-developer-at-fpt-123)
    extract: Structured fields (title, salary, requirements, etc.)
    note: THIS is the URL that goes into the output — not the Phase 1 listing URL

  url_validation:
    # Validate that extracted URLs are item pages, not listing/search pages
    listing_indicators: ["/search?", "/find?", "?q=", "/tag/", "/category/", "/it-jobs?" without ID]
    item_indicators: [specific slug or ID in path, "/jobs/specific-title-123", "/viec-lam/ten-viec-123"]
```

---

## Field Extraction

When fetching individual item pages, extract the required fields:

```yaml
FIELD_EXTRACTION:
  method: |
    After fetching an item page with fetch_webpage:
    1. Read the content returned
    2. Extract each required field from the content
    3. If a field can't be found → mark as "N/A" or "Không rõ"
    4. For URLs: use the page's actual URL (the one you fetched), NOT the Google search URL

  common_fields_for_jobs:
    job_title: "Position name — usually in <h1> or title"
    company_name: "Company name — usually prominent on page"
    salary: "Salary range — may be hidden ('Thương lượng')"
    experience_required: "Years or level (fresher, junior, senior)"
    skills_required: "Listed technical skills"
    location: "City or 'Remote'"
    job_type: "Full-time, Part-time, Contract"
    direct_url: "The URL of THIS specific job page"
    posted_date: "When the job was posted"
    company_review_url: "Link to company review page (Glassdoor, ITViec review)"
    company_review_summary: "Brief summary of company reputation"

  quality_check:
    # After extracting all items, verify:
    - Each item has a direct_url that's an item page (not search)
    - Required fields have actual values (not all "N/A")
    - Items match the filter criteria (location, experience level)
    - No duplicate items (same job from different sources)
```

---

## Handling Company Reviews

When the user asks for company reviews alongside items:

```yaml
COMPANY_REVIEW_PROTOCOL:
  for_each_unique_company:
    1. Search for company reviews:
       queries:
         - "site:glassdoor.com {company_name} review"
         - "site:itviec.com/review/{company_name}"
         - "{company_name} review nhân viên đánh giá"
    
    2. Fetch review page (1 source is sufficient)
    
    3. Extract:
       - Overall rating (if available)
       - Key positive/negative themes
       - Red flags (if any): layoffs, poor management, delayed salary
       - Review URL (direct link to review page)
    
    4. Summarize in 1-2 sentences per company
    
  efficiency: 
    # Don't fetch reviews for every single job — group by company
    # If 5 jobs are from FPT, only fetch FPT review once
    deduplicate_by: company_name
```

---

## Quality Validation for Data Collection Output

```yaml
OUTPUT_VALIDATION:
  url_check:
    for_each_item:
      - URL format is valid (starts with http:// or https://)
      - URL doesn't contain search indicators (?q=, /search?, google.com/search)
      - URL points to the platform domain (itviec.com, topCV.vn, linkedin.com)
      - URL has a specific item path (not just the homepage or listing page)
    
  field_check:
    for_each_required_field:
      - Field exists in the output
      - >70% of items have a non-empty value
      - Values are meaningful (not all identical or all "N/A")
  
  filter_check:
    - Items match the user's filter criteria
    - Location matches (or is remote if allowed)
    - Experience level matches (fresher/junior if specified)
    - Skills match (at least partially)
  
  quantity_check:
    - At least 10 items for a basic collection request
    - At least 20 items for "tất cả" / comprehensive requests
    - Report if target couldn't be met and explain why
```

---

## Batch Progress Model

When executing data_collection pipelines, emit non-interactive progress updates
so the user knows what's happening without needing to be on-call.

```yaml
BATCH_PROGRESS:
  purpose: >
    User sees autonomous progress without approving each batch.
    Replaces: "Đã thu thập 10 items, bạn có muốn tiếp tục không?" (BANNED)
    With:      "🔍 ITViec: ✅ 10 items" (non-interactive update)
    
  PROGRESS_EVENTS:
    platform_start:
      format: "🔍 Đang thu thập từ {platform}..."
      when: Before starting search on each platform
      
    platform_done:
      format: "🔍 {platform}: ✅ {count} items ({field_sample})"
      when: After extracting all items from a platform
      example: "🔍 ITViec: ✅ 12 items (JavaScript Fresher, HCM)"
      
    batch_complete:
      format: "📊 Tổng đã thu thập: {total} items từ {platform_count} nền tảng"
      when: After all platforms are done, before Excel generation
      
    dedup_report:
      format: "🔄 Sau khi loại trùng: {final_count} items ({removed} trùng đã xóa)"
      when: After deduplication (if any duplicates found)
      skip_if: removed == 0

  BATCH_DECISIONS:
    # ALL decisions below are made AUTOMATICALLY — never ask user
    
    platform_order:
      rule: primary platforms first (ITViec, TopCV), secondary after
      never_ask: "Bắt đầu từ nền tảng nào?"
      
    items_per_platform:
      rule: Collect up to target/platform_count per platform
      cap: 30 items per platform maximum (avoid infinite loops)
      never_ask: "Thu thập bao nhiêu items từ {platform}?"
      
    quality_threshold:
      rule: If <5 items from a platform → try next, don't ask
      never_ask: "Chỉ có 3 items, bạn muốn tiếp tục không?"
      
    retry_on_failure:
      rule: Retry once with simplified query, then skip platform
      max_retries: 1
      never_ask: "Lấy được ít, tiếp tục hay thử lại?"
      
    batch_size:
      rule: Process all items without artificial pausing
      never_ask: "Đã có 10 items, thu thập thêm không?"

  MINIMAL_INTERACTION_CONTRACT:
    before_collection:  "🔍 Thu thập {entity_type} từ {platform_list}..."
    during_collection:  "{platform_done events} — non-interactive, no approval needed"
    after_collection:   "📊 Tổng: {final_count} {entity_type} → Đang tạo {output_format}..."
    on_completion:      (see Final Delivery section)
```

