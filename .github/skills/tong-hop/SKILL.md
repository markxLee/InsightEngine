---
name: tong-hop
description: |
  Main InsightEngine pipeline — orchestrates all sub-skills based on user intent.
  Analyzes user request to determine input sources, processing type, and output format,
  then routes to appropriate sub-skills in correct order.
  Use when user says "tổng hợp nội dung", "làm báo cáo", "làm thuyết trình", or "/tong-hop".
argument-hint: "[content request in Vietnamese or English]"
---

# Tổng Hợp — InsightEngine Pipeline Orchestrator

**References:** `references/pipeline-ux.md` | `references/session-summary.md` | `references/output-chaining.md`

```yaml
MODE: Interactive — presents plan, gets approval, then executes
LANGUAGE: All Copilot responses in Vietnamese
ROLE: Orchestrator — delegates ALL content work to sub-skills
```

---

## Trigger Conditions

Use this skill when user:
- Says "tổng hợp nội dung", "làm báo cáo", "làm thuyết trình"
- Says "tóm tắt từ nhiều nguồn", "synthesize content", "create report"
- Uses command `/tong-hop`
- Describes a content task involving sources or output formats

---

## Step 1: Parse Request

1. Extract **input sources**: file paths, URLs, web-search topics, inline text
2. Determine **processing type**: synthesis (default) | translation | summary
3. Determine **output format**: word (default) | excel | slides | pdf | html
4. Detect **style**: corporate | academic | minimal | dark-modern | creative (see `references/pipeline-ux.md`)
5. Detect if request implies **chained outputs** (see `references/output-chaining.md`)

---

## Step 2: Pre-flight Check

1. Run: `python3 scripts/check_deps.py --silent`
2. If exit 0 → continue to Step 3
3. If exit 1 → respond in Vietnamese: "⚠️ Một số thư viện chưa được cài đặt. Gõ /cai-dat để cài đặt tự động." — STOP

---

## Step 3: Present Execution Plan

```yaml
PLAN_FORMAT: |
  📋 Kế hoạch thực hiện:

  **Nguồn dữ liệu:** [list each source]
  **Xử lý:** [synthesis | translation | summary]
  **Đầu ra:** [format + style]

  **Các bước:**
  1. Thu thập nội dung từ [sources]
  2. Biên soạn và tổng hợp
  3. Xuất [format] kiểu [style]
  ⏱️ Ước tính: ~{total_time}

  Bạn đồng ý với kế hoạch này không?

ROUTING:
  single_output:    thu-thap → bien-soan → tao-<format>
  translation_only: thu-thap → bien-soan (translation mode)
  chained_output:   thu-thap → bien-soan → tao-excel → tao-hinh → tao-slide
  search_and_out:   thu-thap (web search) → bien-soan → tao-<format>
```

---

## Step 4: Execute Sub-Skills

Show progress before and after each step (format: see `references/pipeline-ux.md`).
For chained outputs and intermediate files, see `references/output-chaining.md`.

1. **thu-thap** (`references/../../thu-thap/SKILL.md`)
   - Input: sources from user request
   - Output: combined Markdown text
   - Report: "✅ Thu thập hoàn tất — {N} nguồn, {total_chars} ký tự"

2. **bien-soan** (`.github/skills/bien-soan/SKILL.md`)
   - Input: Markdown from thu-thap
   - Options: `enrich: true` (default) | `include_notes: true` (if output = presentation)
   - Output: structured Markdown content
   - Report: "✅ Biên soạn hoàn tất — {sections} phần, {total_words} từ"

3. **tao-\<format\>** (skill determined by output_format)
   - Mapping: word → tao-word | excel → tao-excel | slides → tao-slide | pdf → tao-pdf | html → tao-html
   - Input: synthesized content from bien-soan
   - Output: final file
   - Report: "✅ Xuất file hoàn tất — {path} ({size})"

4. **tao-hinh** (conditional — if charts requested OR output is slides with data)
   - Report: "✅ Tạo {N} biểu đồ hoàn tất"

---

## Step 5: Final Report

```yaml
FINAL_REPORT:
  format: |
    🎉 Hoàn tất! Kết quả:

    📄 File đầu ra:
    - {file_path} ({file_size})

    ⏱️ Các bước đã thực hiện:
    1. ✅ Thu thập: {source_count} nguồn
    2. ✅ Biên soạn: {word_count} từ
    3. ✅ Xuất {format}: {file_path}

    💡 Bạn muốn chỉnh sửa gì không?
```

---

## Step 6: Session Summary & View Suggestions

After every completed pipeline run:
1. Append session entry to `output/session-summary.md`
2. Show how to open the output file(s)

See `references/session-summary.md` for full format and view suggestion specs.

---

## What This Skill Does NOT Do

- Does NOT generate content itself — delegates to sub-skills
- Does NOT install dependencies — redirects to /cai-dat
- Does NOT process files directly — uses thu-thap
- Does NOT skip the execution plan — always shows plan first
