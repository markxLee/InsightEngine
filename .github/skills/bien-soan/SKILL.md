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

**References:** `references/comprehensive-mode.md` | `references/translation-mode.md` | `references/extra-modes.md`

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

## Mode Selection

```yaml
MODES:
  synthesis:    Default — merge multiple sources into one document
  comprehensive: "chi tiết", "comprehensive", "đầy đủ", "--mode=comprehensive"
                 See references/comprehensive-mode.md for full spec
  translation:  "dịch", "translate", "dịch sang"
                See references/translation-mode.md for full spec
  summary:      "tóm tắt", "summarize" — extract key points and condense

MODE_SELECTION:
  interactive: Ask user: "Bạn muốn biên soạn ở chế độ nào? Standard hay Comprehensive?"
  pipeline: Default standard unless tong-hop specifies mode=comprehensive
```

---

## Step 1: Analyze Sources

1. For each source: identify main topics, extract key facts, detect language
2. Cross-source: identify overlapping content, flag contradictions
3. If combined input > 50,000 words → switch to chunking mode (see `references/extra-modes.md`)
4. If thin sections detected → trigger enrichment callback (see `references/extra-modes.md`)
5. Report:
   ```
   📊 Phân tích nguồn:
   - {N} nguồn, ~{total_words} từ
   - Chủ đề chính: {topics}
   - Trùng lặp: {overlap_areas}
   - Mâu thuẫn: {contradictions or "Không có"}
   ```

---

## Step 2: Propose Outline

1. Create logical section structure from combined content
2. Group related information under headings, order for narrative flow
3. Mark which sources contribute to each section
4. Present to user:
   ```
   📝 Đề xuất cấu trúc tài liệu:
   1. **{Section 1}** — từ nguồn: {sources}
   2. **{Section 2}** — từ nguồn: {sources}
   ...
   Bạn muốn điều chỉnh gì không?
   ```
5. Interactive: wait for approval or modification
6. Pipeline mode: auto-approve, proceed immediately

---

## Step 3: Synthesize Content

1. For each section: gather relevant content from all sources
2. Merge content — eliminate redundancy, create coherent narrative
3. Resolve contradictions: present both perspectives with attribution
4. Ensure smooth transitions between subsections
5. Output format: Structured Markdown (H1/H2/H3, paragraphs, bullet lists, tables, bold/italic)

For comprehensive mode (3-5x depth), see `references/comprehensive-mode.md`.
For speaker notes (when output is presentation), see `references/extra-modes.md`.

---

## Step 4: Format & Deliver

1. Apply target length: short (~500-1000 words) | medium (~1000-3000) | long (~3000-10000) | user-specified
2. Quality checks: no duplicate paragraphs, consistent headings, tables have headers, consistent language
3. Deliver:
   ```
   ✅ Biên soạn hoàn tất:
   - Cấu trúc: {N} phần, {M} phần phụ
   - Độ dài: ~{word_count} từ
   - Ngôn ngữ: {language}
   [Preview first section]
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
  date_conflicts:
    action: Use most recent source, note the discrepancy
  user_resolution:
    - Interactive: ask user to decide on critical conflicts
    - Pipeline: use most recent/reliable source
```

---

## What This Skill Does NOT Do

- Does NOT read files — that's thu-thap
- Does NOT generate output files — that's tao-* skills
- Does NOT install dependencies — redirects to /cai-dat
- Does NOT search the web — delegates to thu-thap
