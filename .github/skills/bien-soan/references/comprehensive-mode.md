# Comprehensive Mode — Full Reference (US-4.4.1)

Produces 3-5x more content than standard mode with richer detail, examples, and analysis.

## Triggers

```yaml
TRIGGERS:
  explicit: "chi tiết", "comprehensive", "đầy đủ", "chuyên sâu", "--mode=comprehensive"
  implicit: Research paper, whitepaper, detailed analysis request
```

## Deep Outline Structure

```yaml
DEEP_OUTLINE:
  for_each_section:
    1. H2 section heading
    2. Introduction paragraph (context and relevance)
    3. H3 sub-sections:
       a. Core content from sources
       b. Analysis and implications
       c. Examples and case studies
       d. Data points and supporting evidence
    4. Section summary and key takeaways

  additional_sections:
    - Executive Summary (generated after all sections complete)
    - Methodology / Approach (if applicable)
    - Key Findings and Recommendations
    - Conclusion with forward-looking insights
```

## Enriched Synthesis

```yaml
ENRICHED_SYNTHESIZE:
  for_each_section:
    1. Write introduction paragraph (why this section matters)
    2. Expand each key point with definition, example, data support, source attribution
    3. Add analysis paragraph (implications, trends, patterns)
    4. Write section summary (3-5 key takeaways as bullet points)

  content_multiplier:
    standard: ~200-500 words per section
    comprehensive: ~800-2000 words per section
    ratio: 3-5x more content
```

## Section Summaries & Key Takeaways

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
    length: ~300-500 words
    content: Purpose, key findings (3-5 bullets), recommendations, scope

  conclusion:
    location: End of document
    length: ~200-400 words
    content: Summary of all sections, connections between findings, next steps
```

## Delivery

```yaml
DELIVER:
  to_user: |
    ✅ Biên soạn chi tiết hoàn tất:
    - Chế độ: Comprehensive
    - Cấu trúc: {N} phần chính, {M} phần phụ
    - Độ dài: ~{word_count} từ ({multiplier}x so với standard)
    - Tóm tắt: Executive summary + {N} section summaries
```
