---
name: thu-thap
description: |
  Gather content from local files and URLs. Uses markitdown as primary reader
  with format-specific fallbacks. Supports docx, xlsx, pdf, pptx, txt, md, csv.
  Use when user says "đọc file", "lấy nội dung từ", "read file", or "/thu-thap".
argument-hint: "[file paths or URLs]"
---

# Thu Thập — Content Gathering Skill

Extracts content from local files and URLs, converting everything to Markdown text.

```yaml
MODE: Interactive (reports progress) or Pipeline (called by tong-hop)
LANGUAGE: Copilot responds in Vietnamese
OUTPUT: Markdown text (passed to bien-soan or directly to user)
```

---

## Trigger Conditions

Use this skill when user:
- Says "đọc file", "lấy nội dung từ", "read file"
- Says "tìm kiếm thông tin", "fetch URL", "search web"
- Uses command `/thu-thap`
- Provides file paths or URLs for content extraction
- Pipeline (tong-hop) routes to this skill for input gathering

---

## Supported Formats

```yaml
LOCAL_FILES:
  primary_reader: markitdown
  supported:
    - .docx (Word documents)
    - .xlsx (Excel spreadsheets)
    - .pdf (PDF documents)
    - .pptx (PowerPoint presentations)
    - .txt (Plain text)
    - .md (Markdown)
    - .csv (CSV data)
    - .html (HTML pages)
    - .jpg, .png (Images — OCR via markitdown)

URLS:
  primary: Copilot fetch_webpage tool
  secondary: httpx + beautifulsoup4 (if fetch_webpage unavailable)

WEB_SEARCH:
  tool: vscode-websearchforcopilot_webSearch
  note: Implemented in US-2.1.1, not this story
```

---

## Step 1: Identify Sources

```yaml
IDENTIFY_SOURCES:
  from_user_request:
    - Extract file paths (absolute or relative)
    - Extract URLs (http:// or https://)
    - Detect if web search is needed (no specific sources given)
    
  validate:
    files:
      - Check each file exists: Path(file).exists()
      - Check format is supported
      - Report any invalid files in Vietnamese
    urls:
      - Basic URL format validation
      - Report any invalid URLs in Vietnamese
      
  report_to_user:
    format: |
      📂 Nguồn dữ liệu:
      - File: {N} file ({formats})
      - URL: {M} đường dẫn
      [- Tìm kiếm: {topic} (chưa hỗ trợ — cần US-2.1.1)]
```

---

## Step 2: Read Local Files

```yaml
READ_LOCAL_FILES:
  for_each_file:
    1_TRY_MARKITDOWN:
      code: |
        from markitdown import MarkItDown
        md = MarkItDown()
        result = md.convert(file_path)
        content = result.text_content
      check: len(content.strip()) >= 100
      
    2_FALLBACK_IF_NEEDED:
      condition: markitdown output is empty or < 100 chars
      fallback_by_format:
        .docx: |
          from docx import Document
          doc = Document(file_path)
          content = "\n\n".join(p.text for p in doc.paragraphs if p.text.strip())
        .xlsx: |
          from openpyxl import load_workbook
          wb = load_workbook(file_path)
          # Extract all sheets as Markdown tables
          for ws in wb.worksheets:
            # Convert rows to Markdown table format
        .pdf: |
          import pdfplumber
          with pdfplumber.open(file_path) as pdf:
            content = "\n\n".join(page.extract_text() or "" for page in pdf.pages)
        .pptx: |
          from pptx import Presentation
          prs = Presentation(file_path)
          content = "\n\n".join(
            shape.text for slide in prs.slides
            for shape in slide.shapes if hasattr(shape, "text")
          )
      
    3_REPORT:
      format: "  ✅ {filename} — {char_count} ký tự ({format})"
      on_error: "  ❌ {filename} — Lỗi: {error_message}"
```

---

## Step 3: Fetch URL Content

```yaml
FETCH_URLS:
  for_each_url:
    1_USE_FETCH_WEBPAGE:
      tool: fetch_webpage
      args:
        urls: [url]
        query: "main content"
      extract: Main content from result
      
    2_REPORT:
      format: "  ✅ {url_title} — {char_count} ký tự"
      on_error: "  ❌ {url} — Lỗi: {status_code or timeout}"
```

---

## Step 4: Combine & Return

```yaml
COMBINE:
  structure:
    for_each_source:
      header: "## Nguồn: {source_name}"
      content: |
        > File: {path_or_url}
        > Kích thước: {char_count} ký tự
        
        {extracted_content}
        
        ---
  
  return:
    to_pipeline: Combined Markdown text (for bien-soan to process)
    to_user: Summary report
    
  summary:
    format: |
      📋 Thu thập hoàn tất:
      - Tổng cộng: {total_sources} nguồn
      - Thành công: {success_count}
      - Lỗi: {error_count}
      - Tổng nội dung: {total_chars} ký tự (~{total_words} từ)
```

---

## Script Pattern

```yaml
SCRIPT_PATTERN:
  # Copilot generates ephemeral Python scripts for file reading
  # Pattern for reading a single file:
  
  single_file: |
    python3 -c "
    from markitdown import MarkItDown
    md = MarkItDown()
    result = md.convert('$FILE_PATH')
    text = result.text_content
    if len(text.strip()) < 100:
        print('FALLBACK_NEEDED')
    else:
        print(f'LENGTH: {len(text)}')
        print('---CONTENT---')
        print(text)
    "
    
  # If FALLBACK_NEEDED, Copilot runs format-specific script
  
  note: |
    Scripts are generated per-task by Copilot, not permanent files.
    All file paths passed as arguments (never hardcoded).
```

---

## Error Handling

```yaml
ERRORS:
  file_not_found:
    message: "❌ File không tồn tại: {path}"
    action: Skip file, continue with others
    
  unsupported_format:
    message: "⚠️ Định dạng không hỗ trợ: {extension}. Hỗ trợ: docx, xlsx, pdf, pptx, txt, md, csv"
    action: Skip file, continue with others
    
  markitdown_error:
    message: "⚠️ markitdown lỗi, thử phương pháp khác..."
    action: Try fallback reader for that format
    
  url_fetch_error:
    message: "❌ Không thể lấy nội dung từ: {url} ({error})"
    action: Skip URL, continue with others
    
  all_sources_failed:
    message: "❌ Không thể đọc nguồn nào. Vui lòng kiểm tra lại file/URL."
    action: Stop pipeline, report to user
```

---

## What This Skill Does NOT Do

- Does NOT synthesize or merge content — that's bien-soan's job
- Does NOT search the web — that's US-2.1.1 (future)
- Does NOT translate content — that's bien-soan's job
- Does NOT generate output files — that's tao-* skills' job
- Does NOT install dependencies — redirects to /cai-dat
