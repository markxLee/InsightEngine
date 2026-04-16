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
- Says "synthesize", "merge content", "dịch thuật"
- Uses command `/bien-soan`
- Pipeline (tong-hop) routes content here for synthesis

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
    note: Implemented in US-1.2.2 (separate story)
    
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

## What This Skill Does NOT Do

- Does NOT read files — that's thu-thap's job
- Does NOT generate formatted output files — that's tao-* skills' job
- Does NOT install dependencies — redirects to /cai-dat
- Does NOT handle translation (yet) — see US-1.2.2
- Does NOT search the web — that's thu-thap + US-2.1.1
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
- Says "synthesize", "merge content", "dịch thuật"
- Uses command `/bien-soan`
- Pipeline (tong-hop) routes content here for synthesis

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
    note: Implemented in US-1.2.2 (separate story)
    
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

## What This Skill Does NOT Do

- Does NOT read files — that's thu-thap's job
- Does NOT generate formatted output files — that's tao-* skills' job
- Does NOT install dependencies — redirects to /cai-dat
- Does NOT handle translation (yet) — see US-1.2.2
- Does NOT search the web — that's thu-thap + US-2.1.1
