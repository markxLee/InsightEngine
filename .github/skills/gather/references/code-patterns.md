# File Reading Code Patterns — Full Reference

## Read Local Files — Code Patterns

```yaml
PRIMARY_READER:
  library: markitdown
  code: |
    from markitdown import MarkItDown
    md = MarkItDown()
    result = md.convert(file_path)
    content = result.text_content
  check: len(content.strip()) >= 100

FALLBACK_BY_FORMAT:
  .docx: |
    from docx import Document
    doc = Document(file_path)
    content = "\n\n".join(p.text for p in doc.paragraphs if p.text.strip())

  .xlsx: |
    from openpyxl import load_workbook
    wb = load_workbook(file_path)
    # Convert each sheet to Markdown table rows

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
```

## Fetch URL Content — Code Patterns

```yaml
PRIMARY:
  tool: fetch_webpage
  args:
    urls: [url]
    query: "main content"
  check: len(content.strip()) >= 50

FALLBACK_HTTPX: |
  import httpx
  from bs4 import BeautifulSoup

  resp = httpx.get(url, follow_redirects=True, timeout=15)
  resp.raise_for_status()
  soup = BeautifulSoup(resp.text, "html.parser")

  for tag in soup(["script", "style", "nav", "footer", "header",
                    "aside", "form", "iframe", "noscript"]):
      tag.decompose()

  main = soup.find("article") or soup.find("main") or soup.find("body")
  content = main.get_text(separator="\n", strip=True) if main else ""

FALLBACK_PLAYWRIGHT: |
  # Tier 3 — For bot-protected sites (Cloudflare, CAPTCHA walls, JS-heavy SPAs)
  # Use the bundled script:
  python3 .github/skills/gather/scripts/playwright_fetch.py "URL" --wait 3
  
  # Multiple URLs:
  python3 .github/skills/gather/scripts/playwright_fetch.py URL1 URL2 --output result.md
  
  # See references/playwright-stealth.md for full anti-detection details

ESCALATION_LOGIC: |
  1. Try fetch_webpage → if content >= 50 chars → done
  2. Try httpx → if content >= 50 chars → done
  3. If both failed OR bot-detection signals (403, Cloudflare, empty SPA) → Playwright
  4. If Playwright also fails → report error honestly

BOT_DETECTION_SIGNALS:
  http_codes: [403, 429, 503]
  page_text: ["Just a moment", "Checking your browser", "Verify you are human",
              "Access denied", "Enable JavaScript", "Cloudflare"]
  empty_spa: Content < 50 chars despite valid URL (JS-rendered page)

CONTENT_CLEANING:
  - Remove duplicate blank lines
  - Strip navigation breadcrumbs
  - Remove "cookie consent" / "subscribe" boilerplate
  - Limit to first 50,000 chars (truncate with notice)
```

## CLI Script

```yaml
CLI_SCRIPT:
  path: scripts/extract_content.py
  usage: |
    python3 scripts/extract_content.py file1.pdf file2.docx
    python3 scripts/extract_content.py --output combined.md file1.pdf
    python3 scripts/extract_content.py --list paths.txt
  output: Combined Markdown with "## Source: <path>" headers per file

COPILOT_USE:
  when: Batch reading 3+ local files OR markitdown may fail (scanned PDFs)
  steps:
    1. Run: python3 .github/skills/gather/scripts/extract_content.py <files...>
    2. Read combined Markdown from stdout
    3. Pass to bien-soan for synthesis
```

## Error Messages

```yaml
ERRORS:
  file_not_found: "❌ File không tồn tại: {path}"
  unsupported_format: "⚠️ Định dạng không hỗ trợ: {extension}"
  markitdown_error: "⚠️ markitdown lỗi, thử phương pháp khác..."
  url_fetch_error: "❌ Không thể lấy nội dung từ: {url} ({error})"
  all_failed: "❌ Không thể đọc nguồn nào. Vui lòng kiểm tra lại file/URL."

  url_error_types:
    404: "Trang không tồn tại (404)"
    403: "Truy cập bị từ chối (403)"
    timeout: "Hết thời gian chờ (timeout 15s)"
    ssl_error: "Lỗi chứng chỉ SSL"
    connection: "Không thể kết nối đến server"
```
