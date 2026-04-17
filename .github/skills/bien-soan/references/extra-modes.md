# Extra Modes — Full Reference

## Large Document Chunking (US-3.2.1)

Handles combined input exceeding Copilot context window.

```yaml
THRESHOLD:
  detect: Combined input > 50,000 words OR > 200,000 characters
  action: Switch to chunking mode automatically

CHUNKING_STRATEGY:
  1_SPLIT:
    method: Split by sections (headings) preferring natural boundaries
    chunk_size: ~10,000-15,000 words per chunk
    overlap: 500 words between chunks (for continuity)

  2_PROCESS_EACH_CHUNK:
    - Analyze key points and themes
    - Generate chunk summary (500-1000 words)
    - Extract data/facts/quotes with source attribution

  3_MERGE:
    - Combine chunk summaries into master outline
    - Identify cross-chunk themes and connections
    - Resolve cross-chunk contradictions
    - Generate final coherent document from merged summaries

  4_QUALITY_CHECK:
    - Verify all source chunks represented in output
    - Ensure consistent terminology across merged output

PIPELINE_MODE:
  - Auto-detect and chunk without asking user
  - Report chunking decision and progress
```

---

## Speaker Notes Generation (US-4.5.2)

When output target is a presentation (tao-html presentation mode or tao-slide).

```yaml
TRIGGER:
  - Pipeline output is "presentation" or "html-presentation"
  - User asks for "ghi chú thuyết trình", "speaker notes", "presenter notes"

GENERATION_RULES:
  per_slide:
    title_slide: Opening remarks, greeting, audience engagement prompt
    content_slides: Expansion of each bullet with details not shown on slide
    data_slides: Key insights to highlight, comparison points
    closing_slide: Summary of key takeaways, Q&A preparation

  style:
    - Conversational tone (as if speaking to audience)
    - 2-4 sentences per slide
    - Include transition phrases between slides
    - Language: Vietnamese by default

  output_format:
    - Add "notes" key to each slide JSON object
    - Plain text (no HTML tags)
    - Example: {"type": "content", "title": "...", "bullets": [...], "notes": "Giải thích chi tiết..."}

PIPELINE_INTEGRATION:
  - tong-hop passes "include_notes: true" to bien-soan when output is presentation
  - bien-soan generates notes during synthesis (not as separate step)
```

---

## Content Enrichment (US-4.4.2)

Auto-enriches thin source content by requesting additional context via web search.

```yaml
THIN_CONTENT_DETECTION:
  threshold_per_section:
    - Section has < 100 words of source content
    - Section has only 1 source reference
    - Key keywords appear but have no supporting detail

  detection_timing: During Step 1 (Analyze Sources) BEFORE synthesis

ENRICHMENT_WORKFLOW:
  1_DETECT:
    - Count words per section, mark THIN or SUFFICIENT

  2_GENERATE_QUERIES:
    - For each THIN section, extract main topic keywords
    - Formulate 1-2 search queries in content's language

  3_REQUEST_ENRICHMENT:
    - Trigger thu-thap web search for each query
    - Fetch top 2-3 URLs via fetch_webpage

  4_MERGE:
    - Tag enriched content with [Web: source_url]
    - Proceed with normal synthesis using combined material

  5_ATTRIBUTE:
    - Cite inline: "According to [Source Name](url), ..."
    - Footer note: "Một số nội dung được bổ sung từ tìm kiếm web"

USER_CONTROL:
  disable: "--no-enrich" | "không tìm thêm" | "chỉ dùng nguồn có sẵn"
  interactive: Ask before enriching (show what will be searched)
  pipeline: Auto-enrich without asking

LIMITS:
  max_queries_per_section: 2
  max_urls_per_query: 3
  max_total: 10 sources
```
