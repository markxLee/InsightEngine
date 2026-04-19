#!/usr/bin/env python3
"""
Playwright Stealth Fetch — Anti-bot URL content extractor.

Uses Playwright with comprehensive anti-detection to fetch content from
bot-protected websites. This is the 3rd-tier fallback when fetch_webpage
and httpx both fail due to bot detection (403, Cloudflare, CAPTCHA walls).

Techniques adapted from A2Z-TEST.IO's proven anti-detection stack:
- navigator.webdriver override
- Chrome runtime spoofing
- Plugin array spoofing
- User-Agent spoofing (real Chrome profile)
- AutomationControlled blink feature disabled

Usage:
    python3 playwright_fetch.py URL [--output FILE] [--wait SECONDS] [--full-page]
    python3 playwright_fetch.py URL1 URL2 URL3 --output combined.md
    python3 playwright_fetch.py --help

Examples:
    python3 playwright_fetch.py "https://itviec.com/it-jobs/javascript"
    python3 playwright_fetch.py "https://example.com/protected" --wait 5
    python3 playwright_fetch.py URL1 URL2 --output results.md
"""

import argparse
import sys
import time
import re
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
except ImportError:
    print("❌ Playwright chưa được cài. Chạy: pip3 install playwright && python3 -m playwright install chromium", file=sys.stderr)
    sys.exit(1)


# Anti-detection init script (proven patterns from A2Z-TEST.IO)
STEALTH_SCRIPT = """
// Override navigator.webdriver — primary bot detection signal
Object.defineProperty(navigator, 'webdriver', { get: () => undefined });

// Add chrome.runtime to look like a real Chrome browser with extensions
if (!window.chrome) { window.chrome = {}; }
window.chrome.runtime = {
    connect: function() {},
    sendMessage: function() {},
    id: 'real-extension-id'
};

// Override plugins to match a real Chrome profile
Object.defineProperty(navigator, 'plugins', {
    get: () => [
        { name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer' },
        { name: 'Chrome PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai' },
        { name: 'Native Client', filename: 'internal-nacl-plugin' }
    ]
});

// Override languages to match User-Agent locale
Object.defineProperty(navigator, 'languages', {
    get: () => ['en-US', 'en', 'vi']
});

// Override permissions query
const origQuery = window.navigator.permissions.query;
window.navigator.permissions.query = (params) =>
    params.name === 'notifications'
        ? Promise.resolve({ state: 'granted', onchange: null,
            addEventListener: ()=>{}, removeEventListener: ()=>{},
            dispatchEvent: ()=>true })
        : origQuery.call(window.navigator.permissions, params);
"""

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0.0.0 Safari/537.36"
)


def create_stealth_context(playwright):
    """Create a browser context with full anti-detection features."""
    browser = playwright.chromium.launch(
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",
            "--disable-blink-features=AutomationControlled",
            "--no-first-run",
            "--disable-extensions",
            "--disable-client-side-phishing-detection",
        ],
    )

    context = browser.new_context(
        user_agent=USER_AGENT,
        viewport={"width": 1440, "height": 900},
        locale="en-US",
        timezone_id="Asia/Ho_Chi_Minh",
        ignore_https_errors=True,
        bypass_csp=True,
        extra_http_headers={
            "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
        },
    )

    context.add_init_script(STEALTH_SCRIPT)
    return browser, context


def extract_main_content(page):
    """Extract clean text content from the page, removing boilerplate."""
    # Try common content selectors in priority order
    content_selectors = [
        "article",
        "main",
        '[role="main"]',
        ".content",
        ".post-content",
        ".article-content",
        ".entry-content",
        "#content",
        "#main-content",
    ]

    for selector in content_selectors:
        el = page.query_selector(selector)
        if el:
            text = el.inner_text()
            if len(text.strip()) > 200:
                return clean_text(text)

    # Fallback: get body text after removing noise elements
    page.evaluate("""
        for (const tag of document.querySelectorAll(
            'script, style, nav, footer, header, aside, form, iframe, noscript, ' +
            '.cookie-banner, .cookie-consent, .newsletter, .sidebar, .advertisement, ' +
            '.social-share, .comments, [role="navigation"], [role="banner"]'
        )) { tag.remove(); }
    """)

    body = page.query_selector("body")
    return clean_text(body.inner_text()) if body else ""


def clean_text(text):
    """Clean extracted text content."""
    # Remove excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    # Remove common boilerplate patterns
    lines = text.split('\n')
    cleaned = []
    skip_patterns = [
        r'^\s*cookie', r'^\s*subscribe', r'^\s*newsletter',
        r'^\s*©\s*\d{4}', r'^\s*all rights reserved',
        r'^\s*privacy policy', r'^\s*terms of service',
    ]
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            cleaned.append('')
            continue
        skip = False
        for pat in skip_patterns:
            if re.match(pat, line_stripped, re.IGNORECASE):
                skip = True
                break
        if not skip:
            cleaned.append(line_stripped)

    result = '\n'.join(cleaned).strip()
    # Truncate to 50,000 chars
    if len(result) > 50000:
        result = result[:50000] + "\n\n[... Nội dung bị cắt ngắn — giới hạn 50,000 ký tự]"
    return result


def fetch_url(context, url, wait_seconds=3):
    """Fetch a single URL with stealth browser context."""
    page = context.new_page()
    try:
        print(f"  🌐 Đang tải: {url}", file=sys.stderr)
        page.goto(url, wait_until="domcontentloaded", timeout=30000)

        # Wait for dynamic content to render
        page.wait_for_load_state("networkidle", timeout=15000)

        # Extra wait for JS-heavy SPAs
        if wait_seconds > 0:
            page.wait_for_timeout(int(wait_seconds * 1000))

        # Check for common bot-detection pages
        title = page.title().lower()
        body_text = page.inner_text("body")[:500].lower()

        bot_signals = ["just a moment", "checking your browser", "verify you are human",
                       "access denied", "please enable javascript", "cloudflare"]
        for signal in bot_signals:
            if signal in title or signal in body_text:
                print(f"  ⚠️ Bot detection detected, waiting 5s extra...", file=sys.stderr)
                page.wait_for_timeout(5000)
                break

        content = extract_main_content(page)
        page_title = page.title()
        final_url = page.url

        return {
            "url": url,
            "final_url": final_url,
            "title": page_title,
            "content": content,
            "chars": len(content),
            "success": len(content.strip()) >= 50,
        }
    except PWTimeout:
        return {"url": url, "title": "", "content": "", "chars": 0, "success": False,
                "error": "Timeout — trang mất quá lâu để tải"}
    except Exception as e:
        return {"url": url, "title": "", "content": "", "chars": 0, "success": False,
                "error": str(e)}
    finally:
        page.close()


def main():
    parser = argparse.ArgumentParser(
        description="Playwright Stealth Fetch — Lấy nội dung từ trang web có chống bot"
    )
    parser.add_argument("urls", nargs="+", help="URL(s) cần fetch")
    parser.add_argument("--output", "-o", help="File output (Markdown). Mặc định: stdout")
    parser.add_argument("--wait", type=float, default=3,
                        help="Thời gian chờ thêm sau khi trang tải (giây, mặc định: 3)")
    parser.add_argument("--full-page", action="store_true",
                        help="Lấy toàn bộ body thay vì chỉ main content")
    args = parser.parse_args()

    results = []
    with sync_playwright() as pw:
        browser, context = create_stealth_context(pw)
        try:
            for i, url in enumerate(args.urls):
                result = fetch_url(context, url, args.wait)
                results.append(result)
                # Rate limiting between requests
                if i < len(args.urls) - 1:
                    time.sleep(1.5)
        finally:
            browser.close()

    # Format output as Markdown
    output_parts = []
    success_count = 0
    for r in results:
        if r["success"]:
            success_count += 1
            output_parts.append(f"## {r['title'] or 'Untitled'}\n")
            output_parts.append(f"> URL: {r['url']}\n")
            if r["url"] != r.get("final_url", r["url"]):
                output_parts.append(f"> Redirected to: {r['final_url']}\n")
            output_parts.append(f"> Kích thước: {r['chars']:,} ký tự\n\n")
            output_parts.append(r["content"])
            output_parts.append("\n\n---\n\n")
        else:
            error_msg = r.get("error", "Không lấy được nội dung")
            output_parts.append(f"## ❌ Lỗi: {r['url']}\n> {error_msg}\n\n---\n\n")
            print(f"  ❌ {r['url']} — {error_msg}", file=sys.stderr)

    combined = "".join(output_parts)

    if args.output:
        Path(args.output).write_text(combined, encoding="utf-8")
        size_kb = Path(args.output).stat().st_size / 1024
        print(f"\n✅ Đã lưu: {args.output} ({size_kb:.1f} KB)", file=sys.stderr)
    else:
        print(combined)

    # Summary to stderr
    print(f"\n📋 Kết quả: {success_count}/{len(results)} URL thành công, "
          f"tổng {sum(r['chars'] for r in results):,} ký tự", file=sys.stderr)


if __name__ == "__main__":
    main()
