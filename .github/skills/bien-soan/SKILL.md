---
name: bien-soan
description: |
  Synthesize and merge multi-source content into coherent documents.
  Two modes: standard (concise) and comprehensive (3-5x richer detail).
  Identifies overlapping content, resolves conflicts, proposes outline.
  Supports translation Vietnamese ↔ English (US-1.2.2).
  Use when user says "tổng hợp", "gộp nội dung", "biên soạn", or "/bien-soan".
argument-hint: "[content from thu-thap or direct text] [mode: standard|comprehensive]"
---

# Biên Soạn — Content Synthesis Skill

Merges and restructures content from multiple sources into a coherent document.

```yaml
MODE: Interactive (proposes outline, gets approval) or Pipeline (from tong-hop)
LANGUAGE: Copilot responds in Vietnamese
INPUT: Markdown text from thu-thap or direct user input
OUTPUT: Structured Markdown content (passed to tao-* output skills)
```

---

## Trigger Conditions

Use this skill when user:
- Says "tổng hợp", "gộp nội dung", "biên soạn"
- Says "synthesize", "merge content", "dịch thuật", "translate"
- Uses command `/bien-soan`
- Pipeline (tong-hop) routes content here for synthesis or translation

---

## Synthesis Modes

```yaml
MODES:
  synthesis:
    trigger: Default mode — merge multiple sources into one document
    steps: analyze → outline → synthesize → format
    depth: standard (~1000-3000 words)
    
  comprehensive:
    trigger: "chi tiết", "comprehensive", "đầy đủ", "chuyên sâu", "--mode=comprehensive"
    steps: analyze → deep_outline → enriched_synthesize → section_summaries → format
    depth: 3-5x standard (~5000-15000 words)
    see: "Comprehensive Mode" section below (US-4.4.1)
    
  translation:
    trigger: "dịch", "translate", "dịch sang"
    steps: detect_language → translate_sections → preserve_format
    see: "Translation Mode" section below
    
  summary:
    trigger: "tóm tắt", "summarize"
    steps: extract_key_points → condense → format

MODE_SELECTION:
  interactive:
    - Ask user: "Bạn muốn biên soạn ở chế độ nào? Standard hay Comprehensive (chi tiết)?"
    - If user says "chi tiết", "đầy đủ", "comprehensive" → comprehensive mode
    - If user says nothing specific → standard mode
  pipeline:
    - tong-hop can specify mode in routing
    - Default: standard unless user's original request implies depth
    - Depth indicators: "báo cáo chi tiết", "detailed report", "phân tích chuyên sâu"
```

---

## Step 1: Analyze Sources

```yaml
ANALYZE:
  for_each_source:
    - Identify main topics and themes
    - Extract key facts, data points, and arguments
    - Note source quality and reliability
    - Detect language (Vietnamese / English / mixed)
    
  cross_source:
    - Identify overlapping content
    - Flag contradictions between sources
    - Find complementary information (source A has X, source B has Y)
    
  report:
    format: |
      📊 Phân tích nguồn:
      - {N} nguồn, ~{total_words} từ
      - Chủ đề chính: {topics}
      - Trùng lặp: {overlap_areas}
      - Mâu thuẫn: {contradictions or "Không có"}
```

---

## Step 2: Propose Outline

```yaml
OUTLINE:
  generate:
    - Create logical section structure from combined content
    - Group related information under headings
    - Order sections for narrative flow
    - Mark which sources contribute to each section
    
  present_to_user:
    format: |
      📝 Đề xuất cấu trúc tài liệu:
      
      1. **{Section 1}** — từ nguồn: {sources}
      2. **{Section 2}** — từ nguồn: {sources}
      3. **{Section 3}** — từ nguồn: {sources}
      ...
      
      Bạn muốn điều chỉnh gì không?
    
  wait_for_approval:
    - If user approves → proceed to synthesis
    - If user modifies → adjust outline → re-present
    - If pipeline mode → auto-approve (no wait)
```

---

## Step 3: Synthesize Content

```yaml
SYNTHESIZE:
  principles:
    - Merge, don't concatenate — create coherent narrative
    - Resolve contradictions by noting both perspectives
    - Preserve key data points and statistics
    - Use consistent terminology throughout
    - Maintain source attribution when appropriate
    
  for_each_section:
    1. Gather relevant content from all sources
    2. Identify the best structure/framing
    3. Merge content, eliminating redundancy
    4. Ensure smooth transitions between subsections
    5. Add section summary if section is long
    
  output_format:
    type: Structured Markdown
    includes:
      - Headings (H1, H2, H3)
      - Paragraphs
      - Bullet lists
      - Tables (for structured data)
      - Bold/italic for emphasis
      - Blockquotes for attributions
```

---

## Step 4: Format & Deliver

```yaml
FORMAT:
  target_length:
    short: ~500-1000 words (summary mode)
    medium: ~1000-3000 words (standard synthesis)
    long: ~3000-10000 words (comprehensive report)
    user_specified: Honor user's length preference
    
  quality_checks:
    - No duplicate paragraphs
    - Consistent heading levels
    - Tables have headers
    - All sections have content (no empty sections)
    - Vietnamese or English consistently (not mixed unless bilingual requested)
    
  deliver:
    to_pipeline: Return structured Markdown for output skill
    to_user: |
      ✅ Biên soạn hoàn tất:
      - Cấu trúc: {N} phần, {M} phần phụ
      - Độ dài: ~{word_count} từ
      - Ngôn ngữ: {language}
      
      [Show preview of first section]
      
      Bạn muốn chỉnh sửa gì trước khi xuất file?
```

---

## Comprehensive Mode (US-4.4.1)

Produces 3-5x more content than standard mode with richer detail, examples, and analysis.

### When to Use

```yaml
TRIGGERS:
  explicit:
    - "chi tiết", "comprehensive", "đầy đủ", "chuyên sâu"
    - "--mode=comprehensive"
    - "báo cáo chi tiết", "detailed report"
  implicit:
    - User's request implies depth (research paper, whitepaper, detailed analysis)
    - Pipeline routes with mode=comprehensive
```

### Comprehensive Outline (Deep Structure)

```yaml
DEEP_OUTLINE:
  # Standard outline creates H2 sections with content
  # Comprehensive adds H3 sub-sections, context paragraphs, and enrichment markers
  
  for_each_section:
    1. H2 section heading (same as standard)
    2. Introduction paragraph (context and relevance)
    3. H3 sub-sections:
       a. Core content from sources
       b. Analysis and implications
       c. Examples and case studies (inferred or from sources)
       d. Data points and supporting evidence
    4. Section summary and key takeaways
    
  additional_sections:
    - Executive Summary (generated after all sections complete)
    - Methodology / Approach (if applicable)
    - Key Findings and Recommendations
    - Conclusion with forward-looking insights
```

### Enriched Synthesis

```yaml
ENRICHED_SYNTHESIZE:
  principles:
    - Everything from standard SYNTHESIZE, PLUS:
    - Add explanatory context for each key point
    - Include concrete examples where sources provide them
    - Add comparative analysis when multiple perspectives exist
    - Expand bullet points into explanatory paragraphs
    - Create transitional paragraphs between sections
    - Add data tables summarizing quantitative information
    
  for_each_section:
    1. Write introduction paragraph (why this section matters)
    2. Expand each key point with:
       - Definition/explanation
       - Example or case study
       - Data support (numbers, percentages, dates)
       - Source attribution
    3. Add analysis paragraph (implications, trends, patterns)
    4. Write section summary (3-5 key takeaways as bullet points)
    
  content_multiplier:
    standard: ~200-500 words per section
    comprehensive: ~800-2000 words per section
    ratio: 3-5x more content
```

### Section Summaries & Key Takeaways

```yaml
SECTION_SUMMARIES:
  format_per_section: |
    ---
    **📌 Tóm tắt phần "{section_title}":**
    - {takeaway_1}
    - {takeaway_2}
    - {takeaway_3}
    ---
  
  executive_summary:
    location: Top of document (after title)
    content:
      - Purpose of the document
      - Key findings (3-5 bullets)
      - Main recommendations (if applicable)
      - Scope and limitations
    length: ~300-500 words
    
  conclusion:
    location: End of document
    content:
      - Summary of all sections
      - Connections between findings
      - Forward-looking insights
      - Recommended next steps
    length: ~200-400 words
```

### Comprehensive Mode Delivery

```yaml
DELIVER_COMPREHENSIVE:
  to_pipeline: Return enriched Markdown for output skill
  to_user: |
    ✅ Biên soạn chi tiết hoàn tất:
    - Chế độ: Comprehensive (chi tiết)
    - Cấu trúc: {N} phần chính, {M} phần phụ
    - Độ dài: ~{word_count} từ ({multiplier}x so với standard)
    - Tóm tắt: Executive summary + {N} section summaries
    - Kết luận: Có
    
    [Show executive summary preview]
    
    Bạn muốn chỉnh sửa gì trước khi xuất file?
```

---

## Conflict Resolution

```yaml
CONFLICTS:
  data_conflicts:
    action: Present both values with source attribution
    format: "Theo {source_A}: X. Trong khi đó, {source_B} ghi nhận: Y."
    
  opinion_conflicts:
    action: Present both perspectives fairly
    format: Present each view, note agreement/disagreement areas
    
  date_conflicts:
    action: Use most recent source, note the discrepancy
    
  user_resolution:
    - For critical conflicts, ask user to decide (if interactive)
    - For pipeline mode, use most recent/reliable source
```

---

## Translation Mode (US-1.2.2)

Translates structured content between Vietnamese and English while preserving document structure.

```yaml
TRIGGER:
  - "dịch thuật", "dịch sang tiếng Anh", "dịch sang tiếng Việt"
  - "translate", "translate to Vietnamese", "translate to English"
  - "dịch sang", "/bien-soan translate"

DETECT_INTENT:
  1. Determine source language:
     - Analyze input text character frequency
     - Vietnamese indicators: diacritics (ă, â, đ, ê, ô, ơ, ư), common words (và, của, là, được)
     - English indicators: common words (the, is, are, with, from)
     - Mixed: treat as source language = dominant language
  2. Determine target language:
     - If user says "dịch sang tiếng Anh" or "translate to English" → target = English
     - If user says "dịch sang tiếng Việt" or "translate to Vietnamese" → target = Vietnamese
     - If ambiguous: ask user (interactive) or infer opposite of source (pipeline)
```

### Translation Workflow

```yaml
STEPS:
  1_PREPARE:
    - Split content into translatable sections (by heading/paragraph)
    - Identify non-translatable elements:
      - Code blocks → preserve as-is
      - URLs, file paths → preserve as-is
      - Proper nouns / brand names → preserve or transliterate
      - Technical terms → translate with original in parentheses first occurrence
    - Preserve Markdown structure (headings, lists, tables, bold/italic)

  2_TRANSLATE_SECTIONS:
    for_each_section:
      - Translate heading text (preserve heading level)
      - Translate paragraph text naturally (not word-by-word)
      - Translate table cell content (preserve table structure)
      - Translate bullet point text (preserve list markers)
      - Translate blockquote text (preserve > prefix)
    
    quality_rules:
      - Use natural, fluent target language (not machine-translation style)
      - Preserve meaning and tone of original
      - Keep consistent terminology throughout document
      - Technical terms: first occurrence = "translated_term (original_term)"
      - Subsequent occurrences: just "translated_term"

  3_PRESERVE_FORMATTING:
    must_preserve:
      - Heading hierarchy (H1, H2, H3 levels)
      - Bold and italic markers
      - Inline code
      - Code blocks
      - Tables with pipe separators
      - Numbered and bulleted lists
      - Links — translate link text, preserve URL
      - Images — translate alt text, preserve path
    
  4_DELIVER:
    to_pipeline: Return translated Markdown for output skill
    to_user: |
      ✅ Dịch thuật hoàn tất / Translation complete:
      - Ngôn ngữ gốc / Source: {source_language}
      - Ngôn ngữ đích / Target: {target_language}
      - Số phần / Sections: {N}
      - Độ dài / Length: ~{word_count} từ/words
      
      Bạn muốn chỉnh sửa gì không? / Any edits needed?
```

### Translation Quality Rules

```yaml
VIETNAMESE_TO_ENGLISH:
  - Use American English spelling
  - Expand Vietnamese abbreviations
  - Adapt Vietnamese-specific idioms to equivalent English expressions
  - Keep formal/informal tone matching the original
  - Dates: Vietnamese DD/MM/YYYY → note if ambiguous

ENGLISH_TO_VIETNAMESE:
  - Use standard Vietnamese (phổ thông)
  - Technical terms: keep English original in parentheses on first use
  - Adapt English idioms to natural Vietnamese equivalents
  - Use appropriate Vietnamese pronouns and honorifics
  - Numbers and units: keep as-is (no conversion)

BILINGUAL_MODE:
  trigger: "song ngữ", "bilingual", "cả hai ngôn ngữ"
  format: |
    Each section rendered in both languages sequentially:
    
    ## Heading (English)
    ## Tiêu đề (Tiếng Việt)
    
    English paragraph...
    
    Đoạn văn tiếng Việt...
```

---

## Large Document Chunking (US-3.2.1)

Handles combined input exceeding Copilot context window by processing in chunks.

```yaml
THRESHOLD:
  detect: Combined input > 50,000 words OR > 200,000 characters
  action: Switch to chunking mode automatically

CHUNKING_STRATEGY:
  1_SPLIT:
    method: Split by sections (headings) preferring natural boundaries
    fallback: Split by paragraphs if sections are too large
    chunk_size: ~10,000-15,000 words per chunk
    overlap: 500 words overlap between chunks (for continuity)
    
  2_PROCESS_INCREMENTALLY:
    for_each_chunk:
      - Analyze key points and themes
      - Generate chunk summary (500-1000 words)
      - Extract data/facts/quotes
      - Preserve source attribution
    progress_report: |
      Dang xu ly phan {current}/{total}...
      
  3_MERGE_SUMMARIES:
    - Combine chunk summaries into master outline
    - Identify cross-chunk themes and connections
    - Resolve any cross-chunk contradictions
    - Generate final coherent document from summaries
    
  4_QUALITY_CHECK:
    - Verify all source chunks represented in output
    - Check no major topics dropped between chunks
    - Ensure consistent terminology across merged output
    - Compare output length to expected range

PIPELINE_MODE:
  - Auto-detect and chunk without asking user
  - Report chunking decision and progress
  - Final output quality comparable to non-chunked processing
```

---

## Speaker Notes Generation (US-4.5.2)

When output target is a reveal.js presentation (tao-html presentation mode), bien-soan
generates speaker notes alongside slide content.

```yaml
SPEAKER_NOTES:
  trigger:
    - Pipeline output is "presentation" or "html-presentation"
    - User asks for "ghi chú thuyết trình", "speaker notes", "presenter notes"
    
  generation_rules:
    per_slide_notes:
      - Title slide: Opening remarks, greeting, audience engagement prompt
      - Content slides: Expansion of each bullet point with details not shown on slide
      - Data/table slides: Key insights to highlight, comparison points
      - Quote slides: Context about the quote, why it matters
      - Closing slide: Summary of key takeaways, Q&A preparation
      
    notes_style:
      - Conversational tone (as if speaking to audience)
      - 2-4 sentences per slide (enough to guide, not script)
      - Include transition phrases between slides
      - Vietnamese by default (match presentation language)
      
    notes_format:
      - Add "notes" key to each slide JSON object
      - Plain text (no HTML tags — gen_reveal.py handles escaping)
      - Example: {"type": "content", "title": "...", "bullets": [...], "notes": "Giải thích chi tiết..."}

  output_json_example: |
    {
      "slides": [
        {
          "type": "title",
          "title": "Báo cáo Q1",
          "subtitle": "Kết quả kinh doanh",
          "notes": "Chào mọi người. Hôm nay tôi sẽ trình bày kết quả kinh doanh Q1. Lưu ý 3 điểm chính..."
        },
        {
          "type": "content",
          "title": "Doanh thu",
          "bullets": ["Tăng 15%", "Vượt target 5%"],
          "notes": "Doanh thu tăng 15% so với cùng kỳ năm trước. Đặc biệt, segment B2B tăng mạnh nhất."
        }
      ]
    }

  pipeline_integration:
    - tong-hop passes "include_notes: true" to bien-soan when output is presentation
    - bien-soan generates notes during synthesis (not as separate step)
    - Notes are part of the slide JSON passed to tao-html/gen_reveal.py
```

---

## Content Enrichment (US-4.4.2)

Automatically enriches thin source content by requesting additional context from thu-thap web search.

### Thin Content Detection

```yaml
THIN_CONTENT_DETECTION:
  threshold:
    # Content is considered "thin" when:
    per_section:
      - Section has < 100 words of source content
      - Section has only 1 source reference (single perspective)
      - Key topic keywords appear but have no supporting detail
    overall:
      - Total source content < 500 words for a multi-section document
      - More than 50% of sections are thin

  detection_timing:
    # Runs during Step 1 (Analyze Sources) BEFORE synthesis begins
    - Count words per topic/section
    - Identify sections below threshold
    - Generate enrichment queries for thin sections
    
  reporting:
    interactive: |
      ⚠️ Phát hiện nội dung mỏng ở {N} phần:
      {list_of_thin_sections}
      → Tự động tìm kiếm bổ sung qua thu-thap? (Có/Không)
    pipeline: Auto-enrich without asking (transparent)
```

### Auto-Enrichment Workflow

```yaml
ENRICHMENT_WORKFLOW:
  1_DETECT:
    - During source analysis, count content depth per section
    - Mark sections as THIN or SUFFICIENT
    
  2_GENERATE_QUERIES:
    for_each_thin_section:
      - Extract main topic keywords
      - Formulate 1-2 search queries in the content's language
      - Example: section "AI in Healthcare" with thin content →
        queries: ["AI healthcare applications 2025", "artificial intelligence medical diagnosis"]
    
  3_REQUEST_ENRICHMENT:
    method: |
      Copilot triggers thu-thap skill internally:
      - Use vscode-websearchforcopilot_webSearch for each query
      - Fetch top 2-3 URLs per query via fetch_webpage
      - Extract relevant content matching the section topic
    
  4_MERGE_ENRICHED_CONTENT:
    - Append web-sourced content to section's source material
    - Tag enriched content with source attribution: [Web: source_url]
    - Proceed with normal synthesis using combined material
    
  5_ATTRIBUTE_SOURCES:
    citation_format: |
      Content from web enrichment is cited inline:
      - "According to [Source Name](url), ..." 
      - Or footnote: "... [^1]" with "[^1]: Source Name, URL"
    transparency: |
      In output metadata/footer:
      "Một số nội dung được bổ sung tự động từ tìm kiếm web / 
       Some content was automatically enriched from web search"
```

### User Control

```yaml
USER_CONTROL:
  disable_enrichment:
    flags:
      - "--no-enrich" in pipeline
      - "không tìm thêm", "no enrichment", "chỉ dùng nguồn có sẵn"
      - "only use provided sources", "không bổ sung"
    behavior: Skip enrichment, synthesize only from provided sources
    
  enable_enrichment:
    default: true (auto-enrich when thin content detected)
    explicit: "bổ sung thêm", "enrich", "tìm thêm thông tin"
    
  interactive_mode:
    - Ask user before enriching: "Nội dung mỏng, tìm thêm?"
    - Show what will be searched
    - User can approve/reject/modify queries
    
  pipeline_mode:
    - Auto-enrich without asking (transparent)
    - Report enrichment in output metadata
    - User can set no_enrich=true in tong-hop routing

ENRICHMENT_LIMITS:
  max_queries_per_section: 2
  max_urls_per_query: 3
  max_total_enrichment_sources: 10
  timeout_per_search: 10s
```

### Pipeline Integration

```yaml
PIPELINE_INTEGRATION:
  tong_hop_routing:
    # tong-hop can control enrichment:
    enrich: true          # default — auto-enrich thin content
    enrich: false         # disable — use only provided sources
    enrich: "aggressive"  # always search, even if content seems sufficient
    
  bien_soan_to_thu_thap:
    # bien-soan requests enrichment from thu-thap via Copilot:
    1. bien-soan identifies thin sections
    2. Copilot runs thu-thap web search (vscode-websearchforcopilot_webSearch)
    3. Copilot runs fetch_webpage on top results
    4. Content returned to bien-soan for integration
    
  output_metadata:
    # All enriched outputs include:
    sources_original: [list of user-provided sources]
    sources_enriched: [list of auto-fetched web sources]
    enriched_sections: [list of section names that were enriched]
```

---

## What This Skill Does NOT Do

- Does NOT read files directly — delegates to thu-thap
- Does NOT generate formatted output files — that's tao-* skills' job
- Does NOT install dependencies — redirects to /cai-dat
- Does NOT perform web search directly — delegates to thu-thap (via Copilot tools)
