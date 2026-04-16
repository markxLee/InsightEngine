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

Main pipeline skill that receives user requests and orchestrates sub-skills.

```yaml
MODE: Interactive — presents plan, gets approval, then executes
LANGUAGE: All Copilot responses in Vietnamese
ROLE: Orchestrator — does NOT do content work itself, delegates to sub-skills
```

---

## Trigger Conditions

Use this skill when user:
- Says "tổng hợp nội dung", "làm báo cáo", "làm thuyết trình"
- Says "tóm tắt từ nhiều nguồn", "synthesize content"
- Says "create report", "create presentation"
- Uses command `/tong-hop`
- Describes a content task involving multiple sources or output formats

---

## Pipeline Flow

```yaml
PIPELINE:
  ┌──────────────────────────────────────────────────────┐
  │  1. RECEIVE user request (Vietnamese or English)      │
  │  2. ANALYZE intent → determine sources + processing   │
  │  3. CHECK deps (run check_deps.py --silent)           │
  │  4. PRESENT execution plan to user                    │
  │  5. EXECUTE sub-skills in order                       │
  │  6. REPORT results (file paths + sizes)               │
  └──────────────────────────────────────────────────────┘
```

---

## Step 1: Receive & Parse Request

```yaml
PARSE_REQUEST:
  extract:
    input_sources:
      local_files: Any file paths mentioned (.docx, .xlsx, .pdf, .pptx, .txt, .md)
      urls: Any URLs mentioned (http://, https://)
      web_search: If user says "tìm trên mạng", "search Google", or no specific sources given
      inline_content: Text/data provided directly in the conversation
      
    processing_type:
      synthesis: Combine multiple sources → single document (default)
      translation: Translate content (trigger: "dịch", "translate")
      summary: Summarize content (trigger: "tóm tắt", "summarize")
      
    output_format:
      word: "file word", "docx", "tài liệu" (default if not specified)
      excel: "file excel", "xlsx", "bảng tính"
      slides: "thuyết trình", "pptx", "slides", "presentation"
      pdf: "file pdf", "pdf"
      html: "trang web", "html"
      
    style_preference:
      corporate: "chuyên nghiệp", "formal", "công ty"
      academic: "học thuật", "nghiên cứu", "academic"
      minimal: "đơn giản", "minimal", "clean"
      auto: If not specified → infer from context
      
    chaining:
      detect: If request implies multiple output formats
      example: "tạo Excel rồi vẽ biểu đồ rồi đưa vào PPT"
```

---

## Step 2: Analyze Intent

```yaml
INTENT_ROUTING:
  # Determine which sub-skills to invoke and in what order
  
  single_output:
    pattern: "Read sources → synthesize → output one format"
    route: thu-thap → bien-soan → tao-<format>
    
  translation_only:
    pattern: "Read source → translate"
    route: thu-thap → bien-soan (translation mode)
    
  chained_output:
    pattern: "Read sources → synthesize → multiple formats"
    route: thu-thap → bien-soan → tao-excel → tao-hinh → tao-slide (example)
    
  search_and_synthesize:
    pattern: "Search web → fetch → synthesize → output"
    route: thu-thap (web search mode) → bien-soan → tao-<format>

  RESPOND_TO_USER:
    language: Vietnamese
    format: |
      📋 Kế hoạch thực hiện:
      
      **Nguồn dữ liệu:**
      - [list sources: files, URLs, web search topics]
      
      **Xử lý:**
      - [processing type: synthesis/translation/summary]
      
      **Đầu ra:**
      - [output format + style]
      
      **Các bước:**
      1. Thu thập nội dung từ [sources]
      2. Biên soạn và tổng hợp
      3. Xuất [format] kiểu [style]
      
      Bạn đồng ý với kế hoạch này không?
```

---

## Step 3: Pre-flight Check

```yaml
PRE_FLIGHT:
  action: Run check_deps.py in silent mode
  command: python3 scripts/check_deps.py --silent
  
  if_exit_0:
    continue: true
    
  if_exit_1:
    action: |
      Report in Vietnamese:
      "⚠️ Một số thư viện chưa được cài đặt. 
       Gõ /cai-dat để cài đặt tự động."
    block: true — do not proceed until deps are resolved
```

---

## Step 4: Execute Sub-Skills

```yaml
EXECUTION:
  # Read and invoke each sub-skill's SKILL.md in sequence
  
  step_1_thu_thap:
    skill: .github/skills/thu-thap/SKILL.md
    input: Sources from user request
    output: Extracted content as Markdown text
    report: "✅ Thu thập hoàn tất — {N} nguồn, {total_chars} ký tự"
    
  step_2_bien_soan:
    skill: .github/skills/bien-soan/SKILL.md
    input: Extracted content from thu-thap
    output: Synthesized/translated content
    report: "✅ Biên soạn hoàn tất — {sections} phần, {total_words} từ"
    
  step_3_output:
    skill: Determined by output_format
    mapping:
      word: .github/skills/tao-word/SKILL.md
      excel: .github/skills/tao-excel/SKILL.md
      slides: .github/skills/tao-slide/SKILL.md
      pdf: .github/skills/tao-pdf/SKILL.md
      html: .github/skills/tao-html/SKILL.md
    input: Synthesized content from bien-soan
    output: Final file
    report: "✅ Xuất file hoàn tất — {path} ({size})"
    
  step_4_charts:
    condition: User requested charts/visuals OR output is slides with data
    skill: .github/skills/tao-hinh/SKILL.md
    input: Data from bien-soan or tao-excel output
    output: Chart PNG files
    report: "✅ Tạo {N} biểu đồ hoàn tất"
```

---

## Step 5: Report Results

```yaml
FINAL_REPORT:
  language: Vietnamese
  format: |
    🎉 Hoàn tất! Kết quả:
    
    📄 File đầu ra:
    - {file_path} ({file_size})
    [- additional files if chained]
    
    ⏱️ Các bước đã thực hiện:
    1. ✅ Thu thập: {source_count} nguồn
    2. ✅ Biên soạn: {word_count} từ
    3. ✅ Xuất {format}: {file_path}
    
    💡 Bạn muốn chỉnh sửa gì không?
```

---

## Chaining Support

```yaml
CHAINING:
  detection:
    - User mentions multiple output formats in one request
    - User says "rồi", "sau đó", "tiếp theo" between format requests
    - Example: "tạo bảng Excel rồi vẽ biểu đồ rồi đưa vào thuyết trình"
    
  plan_display:
    format: |
      📋 Chuỗi xử lý:
      1. Thu thập → Biên soạn
      2. Xuất Excel (.xlsx)
      3. Tạo biểu đồ từ Excel → PNG
      4. Xuất PowerPoint (.pptx) với biểu đồ
      
  intermediate_files:
    location: tmp/ directory (relative to user's working directory)
    cleanup: After chain completes, report which tmp files can be deleted
    
  error_handling:
    if_step_fails: Stop chain, report error, ask user how to proceed
```

---

## Style Inference

```yaml
STYLE_INFERENCE:
  # When user doesn't specify a style, infer from context:
  
  corporate:
    triggers: "báo cáo công ty", "formal", "chuyên nghiệp", business context
    
  academic:
    triggers: "nghiên cứu", "luận văn", "research", "academic", scientific topics
    
  minimal:
    triggers: "đơn giản", "nhanh", "minimal", "clean", casual requests
    
  default: corporate (if no clear signal)
  
  always_confirm: Ask user to confirm style choice before generating
```

---

## What This Skill Does NOT Do

- Does NOT generate content itself — delegates to sub-skills
- Does NOT install dependencies — redirects to /cai-dat
- Does NOT process files directly — uses thu-thap skill
- Does NOT skip the execution plan — always shows plan before executing
- Does NOT proceed without user confirmation of the plan
