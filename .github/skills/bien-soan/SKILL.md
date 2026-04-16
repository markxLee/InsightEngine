---
name: bien-soan
description: |
  Synthesize and merge multi-source content into coherent documents.
  Identifies overlapping content, resolves conflicts, proposes outline.
  Supports translation Vietnamese ↔ English (US-1.2.2).
  Use when user says "tổng hợp", "gộp nội dung", "biên soạn", or "/bien-soan".
argument-hint: "[content from thu-thap or direct text]"
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
    
  translation:
    trigger: "dịch", "translate", "dịch sang"
    steps: detect_language → translate_sections → preserve_format
    see: "Translation Mode" section below
    
  summary:
    trigger: "tóm tắt", "summarize"
    steps: extract_key_points → condense → format
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

## What This Skill Does NOT Do

- Does NOT read files — that's thu-thap's job
- Does NOT generate formatted output files — that's tao-* skills' job
- Does NOT install dependencies — redirects to /cai-dat
- Does NOT search the web — that's thu-thap + US-2.1.1
