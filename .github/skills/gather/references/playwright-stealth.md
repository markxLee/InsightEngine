# Playwright Stealth Fetch — Technical Reference

## Architecture

3-tier URL fetching strategy with automatic escalation:

```
URL → Tier 1: fetch_webpage (fastest, zero overhead)
  │      ↓ fails / < 50 chars
  ├→ Tier 2: httpx + BeautifulSoup (lightweight HTTP)
  │      ↓ fails / 403 / bot-detection
  └→ Tier 3: Playwright stealth (headless Chrome with anti-detection)
```

## Anti-Detection Techniques

Adapted from A2Z-TEST.IO's proven production anti-bot stack.

### Browser Launch Flags

```python
args = [
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-dev-shm-usage",
    "--disable-blink-features=AutomationControlled",  # CRITICAL: hides automation
    "--no-first-run",
    "--disable-extensions",
    "--disable-client-side-phishing-detection",
]
```

### Context Configuration

```python
context = browser.new_context(
    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ...",
    viewport={"width": 1440, "height": 900},
    locale="en-US",
    timezone_id="Asia/Ho_Chi_Minh",
    ignore_https_errors=True,
    bypass_csp=True,
    extra_http_headers={
        "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
    },
)
```

### JavaScript Injection (addInitScript)

| Override | What it does |
|----------|-------------|
| `navigator.webdriver → undefined` | Primary bot detection bypass |
| `window.chrome.runtime` | Fake Chrome extension runtime |
| `navigator.plugins` | Real Chrome plugin list |
| `navigator.languages` | Match UA locale |
| `permissions.query` | Grant notifications permission |

## Script Usage

```bash
# Single URL
python3 scripts/playwright_fetch.py "https://example.com" 

# Multiple URLs
python3 scripts/playwright_fetch.py URL1 URL2 URL3

# Save to file
python3 scripts/playwright_fetch.py URL --output result.md

# Extra wait for heavy SPAs
python3 scripts/playwright_fetch.py URL --wait 5
```

### Output Format

Markdown with source headers:
```markdown
## Page Title
> URL: https://example.com
> Kích thước: 12,345 ký tự

{extracted content}

---
```

### Return Codes

- Success: content ≥ 50 chars extracted
- Failure: timeout, empty content, or error

## Bot Detection Signals

The script auto-detects these and applies extra wait:
- "Just a moment" (Cloudflare)
- "Checking your browser"
- "Verify you are human"
- "Access denied"
- "Please enable JavaScript"

## Content Extraction Priority

1. `<article>` tag
2. `<main>` tag
3. `[role="main"]`
4. `.content`, `.post-content`, `.article-content`
5. `#content`, `#main-content`
6. Fallback: `<body>` after removing noise (`nav`, `footer`, `header`, `aside`, etc.)

## Performance Notes

- First run downloads Chromium (~150 MB, cached afterwards)
- Browser launch: ~1-2 seconds
- Page load + render: 3-10 seconds depending on site
- Rate limiting: 1.5 seconds between requests

## Limitations

- Cannot solve CAPTCHAs (image/text challenges)
- Cannot handle login-required pages (no credentials)
- Cloudflare Turnstile may block after multiple requests
- Heavy sites may need --wait > 5 seconds
- Max 50,000 chars per page (truncated)

## Dependencies

```
playwright>=1.40
# Install browser: python3 -m playwright install chromium
```
