---
name: tong-hop
description: |
  Main InsightEngine pipeline — analyzes user intent and orchestrates all sub-skills end-to-end.
  Handles any content task: research → synthesis → output in Word/Excel/PPT/PDF/HTML/chart format.
  Supports session resume via save_state.py and chained outputs (e.g., Excel data → chart → slide).
  Always use this skill whenever the user describes any content creation, reporting, or presentation
  task — even casual requests like "làm cái báo cáo", "tổng hợp giúp tôi", "tạo slide từ mấy cái
  file này", "search rồi tạo file", or simply describes what they need without naming a specific
  skill. Also triggers on resume requests: "tiếp tục", "resume", "tiếp tục từ", "/resume".
argument-hint: "[content request in Vietnamese or English]"
---

# Tổng Hợp — InsightEngine Pipeline Orchestrator

**References:** `references/pipeline-ux.md` | `references/session-summary.md` | `references/output-chaining.md`
**State:** `tmp/.session-state.json` (written after each step via `scripts/save_state.py`)

```yaml
MODE: Interactive — presents plan, gets approval, then executes
LANGUAGE: All Copilot responses in Vietnamese
ROLE: Orchestrator — delegates ALL content work to sub-skills
```

---

---

## Step 0: Resume Check (run on every startup)

```bash
python3 scripts/save_state.py check
```

| Output | Action |
|--------|--------|
| `NO_STATE` or `COMPLETED` | Skip to Step 1 (normal start) |
| `IN_PROGRESS` + summary | Show summary to user in Vietnamese (see below), ask "⚡ Tiếp tục hay bắt đầu lại?" |

**If user says tiếp tục / resume / "1" / "tiếp":**
```bash
python3 scripts/save_state.py resume-plan
# Returns JSON list of pending steps
# Skip completed steps — execute ONLY pending steps (from Step 4)
```

**If user says bắt đầu lại / fresh / "2" / "mới":**
```bash
python3 scripts/save_state.py archive
# Then proceed from Step 1 as normal
```

**If no state file OR trigger was NOT a resume keyword:** skip to Step 1 silently.

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

After user approves plan, initialize session state:
```bash
python3 scripts/save_state.py init \
  --request "<original user request>" \
  --plan '{"input_sources":[...],"processing_type":"...","output_format":"...","style":"..."}'
```

---

## Step 4: Execute Sub-Skills

Show progress before and after each step (format: see `references/pipeline-ux.md`).
For chained outputs and intermediate files, see `references/output-chaining.md`.

1. **thu-thap** (`references/../../thu-thap/SKILL.md`)
   - Input: sources from user request
   - Output: combined Markdown text
   - Report: "✅ Thu thập hoàn tất — {N} nguồn, {total_chars} ký tự"
   - Save state: `python3 scripts/save_state.py update --step thu-thap`

2. **bien-soan** (`.github/skills/bien-soan/SKILL.md`)
   - Input: Markdown from thu-thap
   - Options: `enrich: true` (default) | `include_notes: true` (if output = presentation)
   - Output: structured Markdown content
   - Report: "✅ Biên soạn hoàn tất — {sections} phần, {total_words} từ"
   - Save state: `python3 scripts/save_state.py update --step bien-soan`

3. **tao-\<format\>** (skill determined by output_format)
   - Mapping: word → tao-word | excel → tao-excel | slides → tao-slide | pdf → tao-pdf | html → tao-html
   - Input: synthesized content from bien-soan
   - Output: final file
   - Report: "✅ Xuất file hoàn tất — {path} ({size})"
   - Save state: `python3 scripts/save_state.py update --step tao-<format> --output-file "<path>"`

4. **tao-hinh** (conditional — if charts requested OR output is slides with data)
   - Report: "✅ Tạo {N} biểu đồ hoàn tất"
   - Save state: `python3 scripts/save_state.py update --step tao-hinh --output-file "<chart_path>"`

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

After reporting, mark pipeline complete:
```bash
python3 scripts/save_state.py complete
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
