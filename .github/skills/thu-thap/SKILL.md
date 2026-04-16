---
name: thu-thap
description: |
  Gather content from local files, URLs, and web search results.
  Uses markitdown as primary reader with format-specific fallbacks.
  Web search via vscode-websearchforcopilot_webSearch.
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
  mode: Auto-search when no files/URLs provided, or hybrid with manual sources
  results: Fetches top 3-5 relevant URLs from search results
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
      - Tìm kiếm web: "{query}" → {K} kết quả
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
      extract: Main content text from tool result
      check: len(content.strip()) >= 50
      
    2_FALLBACK_HTTPX:
      condition: fetch_webpage unavailable or returned empty/error
      script: |
        import httpx
        from bs4 import BeautifulSoup
        
        resp = httpx.get(url, follow_redirects=True, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Extract title
        title = soup.title.string if soup.title else url
        
        # Remove non-content elements
        for tag in soup(["script", "style", "nav", "footer", "header",
                          "aside", "form", "iframe", "noscript"]):
            tag.decompose()
        
        # Try article/main content first, fallback to body
        main = soup.find("article") or soup.find("main") or soup.find("body")
        content = main.get_text(separator="\n", strip=True) if main else ""
      
    3_CONTENT_CLEANING:
      steps:
        - Remove duplicate blank lines
        - Strip navigation breadcrumbs
        - Remove "cookie consent" / "subscribe" boilerplate
        - Limit to first 50,000 chars (truncate with notice)
      
    4_REPORT:
      format: "  ✅ {page_title} ({url_domain}) — {char_count} ký tự"
      on_error: |
        ❌ Không thể lấy nội dung từ: {url}
           Lỗi: {error_type} — {error_message}
           (HTTP {status_code} / Timeout / Connection refused)
      
    5_ERROR_TYPES:
      404: "Trang không tồn tại (404)"
      403: "Truy cập bị từ chối (403)"
      timeout: "Hết thời gian chờ (timeout 15s)"
      ssl_error: "Lỗi chứng chỉ SSL"
      connection: "Không thể kết nối đến server"
      parse_error: "Không thể trích xuất nội dung"
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
- Does NOT translate content — that's bien-soan's job
- Does NOT generate output files — that's tao-* skills' job
- Does NOT install dependencies — redirects to /cai-dat

---

## Web Search Mode (US-2.1.1)

Auto-search Google when user describes a topic without providing specific sources.

```yaml
TRIGGER:
  - No files or URLs provided by user
  - User explicitly asks to search: "tìm kiếm về", "search for"
  - Pipeline (tong-hop) routes with search_needed: true
  - Hybrid: user provides some files + asks to supplement with web search

WORKFLOW:
  1_DETECT_SEARCH_NEED:
    - User gives topic description but no file paths / URLs
    - User says "tìm thông tin", "search", "tìm kiếm"
    - Pipeline sends search_query parameter
    
  2_BUILD_SEARCH_QUERY:
    - Extract key topic from user request
    - Add language qualifier if needed (Vietnamese / English context)
    - Keep query concise (3-8 words for best results)
    - Example: user says "tổng hợp về AI trong giáo dục" → query: "AI in education trends 2026"
    
  3_EXECUTE_SEARCH:
    tool: vscode-websearchforcopilot_webSearch
    params:
      query: "{constructed_search_query}"
    result: List of URLs with titles and snippets
    
  4_PRESENT_RESULTS:
    format: |
      🔍 Kết quả tìm kiếm cho: "{query}"
      
      1. **{title_1}** — {domain_1}
         {snippet_1}
      2. **{title_2}** — {domain_2}
         {snippet_2}
      3. **{title_3}** — {domain_3}
         {snippet_3}
      ...
      
      Bạn muốn lấy nội dung từ nguồn nào? (Mặc định: tất cả top 3-5)
    
    interactive_mode:
      - Wait for user to approve or select specific sources
      - User can say "tất cả" (all) or pick by number
    pipeline_mode:
      - Auto-select top 3-5 most relevant URLs
      - Skip approval, proceed to fetch
    
  5_FETCH_SELECTED:
    - Use Step 3 (Fetch URL Content) for each selected URL
    - Apply same content cleaning and error handling
    - Combine with any manually provided files/URLs
    
  6_REPORT:
    format: |
      🔍 Tìm kiếm web hoàn tất:
      - Truy vấn: "{query}"
      - Kết quả tìm thấy: {total_results}
      - Đã lấy nội dung: {fetched_count} nguồn
      - Lỗi: {error_count}

HYBRID_MODE:
  description: Combine local files + URLs + web search results
  priority:
    1: Local files (most reliable)
    2: Provided URLs (user-selected)
    3: Web search results (supplementary)
  labeling:
    - Mark source origin in combined output: [File], [URL], [Web Search]
    - bien-soan can use origin to weight reliability
```
