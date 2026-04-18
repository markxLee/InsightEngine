# Request Analysis — Deep Analysis Protocol

## Step 1.5: Request Deep Analysis (CRITICAL — DO NOT SKIP)

The difference between mediocre and excellent output starts here. Most user prompts are
underspecified — the user has a rich mental model of what they want but only types a short
sentence. This step bridges that gap by analyzing the request deeply, expanding implicit
dimensions, and confirming with the user before execution.

**Why this matters:** Without this step, a request like "làm báo cáo về AI" gets parsed as
"search AI → write report" which produces generic content. With deep analysis, it becomes
"search AI applications in [user's domain], trends 2024-2026, key players, market size,
risks, and opportunities → write analytical report with data tables and recommendations."

---

## Expand Request Dimensions

**Behavior depends on REQUEST_TYPE detected in Step 1:**

### For `research` requests — Expand analytical dimensions:

For the user's request, identify ALL implicit dimensions:

```yaml
DIMENSION_EXPANSION:
  for_each_request:
    1. CORE_QUESTION: What is the user literally asking for?
    2. IMPLICIT_SUBTOPICS: What sub-topics must be covered to make this useful?
       - A report about "AI trends" implicitly needs: current state, key players,
         recent breakthroughs, market data, risks/challenges, future predictions
    3. CONTEXT_DIMENSIONS: What context makes this actionable?
       - Who is the audience? (infer from style/format if not stated)
       - What decisions will this support?
       - What level of technical detail is appropriate?
    4. DATA_NEEDS: What specific data would make this credible?
       - Numbers, statistics, comparisons, timelines, case studies
    5. ANALYTICAL_ANGLES: What analysis would add genuine value?
       - Comparisons, trend analysis, SWOT, recommendations, implications
    6. SCOPE_BOUNDARIES: What should NOT be included? (to stay focused)
```

### For `data_collection` or `mixed` requests — Expand collection strategy:

This is fundamentally different from research analysis. The user wants SPECIFIC ITEMS
collected, not knowledge synthesized. The analysis must focus on:

```yaml
DATA_COLLECTION_ANALYSIS:
  for_each_request:
    1. TARGET_ENTITIES: What specific items does the user want?
       - "Job listings", "apartments", "products", "courses", "companies"
       - Be precise: "fresher JavaScript jobs" not just "jobs"
    
    2. SEARCH_PLATFORMS: Where should we look for these items?
       # This is critical — generic Google search returns overview pages, NOT individual items.
       # Must identify platform-specific sources where individual items live.
       example_for_jobs:
         - ITViec.com (IT jobs Vietnam — most relevant)
         - TopCV.vn (general jobs Vietnam)
         - LinkedIn Jobs (remote + international)
         - VietnamWorks.com (established platform)
         - Glassdoor.com (reviews + jobs)
         - Indeed.com (broad reach)
       example_for_products:
         - Specific e-commerce platforms (Shopee, Tiki, Amazon)
       example_for_courses:
         - Udemy, Coursera, specific school websites
    
    3. FILTER_CRITERIA: What filters narrow the search?
       - Location: "HCM", "remote"
       - Experience: "fresher", "< 1 year"
       - Skills: "JavaScript", "Node.js", "React"
       - Salary range, company size, etc.
    
    4. REQUIRED_FIELDS: What data must be extracted per item?
       # Extract from user's prompt + add essential defaults
       user_explicit: [fields user mentioned directly]
       auto_added:
         - direct_url: "ALWAYS — link to the specific item page, never a search page"
         - source_platform: "Which platform/site this was found on"
       validation_rules:
         - direct_url must point to individual item (e.g., itviec.com/jobs/xyz NOT itviec.com/search?q=xyz)
         - Salary can be "Thương lượng" if not disclosed
    
    5. SEARCH_QUERIES: Generate platform-specific search queries
       # NOT generic Google queries — target specific platforms
       bad:  "fresher javascript developer ho chi minh"  ← returns Google search results
       good:
         - site:itviec.com fresher javascript developer ho chi minh
         - site:topCV.vn javascript fresher
         - site:linkedin.com/jobs javascript developer fresher vietnam remote
       # Also: navigate directly to platform search pages when possible
    
    6. SUPPLEMENTARY_RESEARCH: Additional context needed per item?
       - "review công ty" → need company review data from Glassdoor, ITViec reviews
       - "so sánh" → need comparison dimensions
    
    7. QUANTITY_EXPECTATION: How many items should we aim for?
       - "tất cả" → as many as feasible (20-50 for job search)
       - "top 10" → 10 items, ranked
       - No quantity specified → aim for 15-30 relevant items
```

---

## Presentation Formats

### Data Collection Analysis Presentation:

```yaml
ANALYSIS_PRESENTATION_FORMAT: |
  🔍 **Phân tích yêu cầu thu thập dữ liệu:**

  **Đối tượng thu thập:** {target_entities}
  **Tiêu chí lọc:** {filter_criteria}
  
  📌 **Các nền tảng sẽ tìm kiếm:**
  1. {platform_1} — {why_relevant}
  2. {platform_2} — {why_relevant}
  ...
  
  📊 **Thông tin sẽ thu thập cho mỗi item:**
  | Field | Mô tả | Bắt buộc |
  |-------|--------|----------|
  | {field_1} | {desc} | ✅ |
  | {field_2} | {desc} | ✅ |
  | direct_url | Link trực tiếp tới job/item | ✅ |
  ...
  
  🔢 **Mục tiêu:** ~{target_quantity} items
  
  {if mixed: "📝 Sau khi thu thập, sẽ phân tích và tạo {analysis_output_format}"}
  
  👉 Bạn đồng ý với kế hoạch này không? Có muốn thêm/bớt trường dữ liệu nào?
```

### Research Analysis Presentation:

```yaml
ANALYSIS_FORMAT: |
  🔍 **Phân tích yêu cầu:**

  **Yêu cầu gốc:** {original_request}

  **Phân tích mở rộng:**
  Tôi hiểu bạn cần {core_interpretation}. Để tạo nội dung thật sự chất lượng,
  tôi đề xuất mở rộng phạm vi như sau:

  📌 **Các khía cạnh sẽ bao gồm:**
  1. {dimension_1} — {why_this_matters}
  2. {dimension_2} — {why_this_matters}
  3. {dimension_3} — {why_this_matters}
  ...

  📊 **Dữ liệu sẽ thu thập:**
  - {data_need_1}
  - {data_need_2}
  - {data_need_3}

  🎯 **Góc phân tích:**
  - {analytical_angle_1}
  - {analytical_angle_2}

  ⚠️ **Sẽ KHÔNG bao gồm:** {scope_boundaries}

  **Đầu ra:** {format} kiểu {style}, dự kiến {estimated_length}

  👉 Bạn đồng ý với phân tích này không? Có muốn thêm/bớt khía cạnh nào?

USER_RESPONSE_HANDLING:
  approved: Proceed to Step 2 with expanded dimensions
  modified: Adjust dimensions based on feedback, re-present if major changes
  simplified: Respect user's wish to narrow scope, but keep content_depth comprehensive
```

**Important:** This step may feel like it slows the pipeline down, but it prevents the much
worse outcome of executing in the wrong direction and producing irrelevant content. A 30-second
confirmation saves 5 minutes of wasted generation.
