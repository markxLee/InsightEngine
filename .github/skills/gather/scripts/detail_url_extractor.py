#!/usr/bin/env python3
"""
detail_url_extractor.py — Extract canonical detail-page URLs from inline/popup detail sources.

For sources that display item details via popup, expandable card, or JS-rendered inline
content rather than navigating to a detail page, this script finds the canonical URL
for each item so output always contains direct item URLs, never listing-page URLs.

Usage:
  python3 detail_url_extractor.py <listing_url> [options]

Options:
  --listing-url <url>     URL of the listing/search results page
  --item-selector <css>   CSS selector for clickable item cards (optional hint)
  --click-and-capture     Use Playwright: click each item, capture URL after navigation
  --output <file>         Save extracted URLs to file (default: stdout)
  --limit <N>             Max items to process (default: 20)

Output: JSON list of {canonical_url, title, detection_method}
"""
import sys
import json
import argparse
import re
from urllib.parse import urljoin, urlparse


# Patterns that identify LISTING pages (not item pages) — reject these
LISTING_URL_PATTERNS = [
    r"\?q=", r"\?query=", r"\?keyword=", r"\?search=",
    r"\?page=\d", r"#results", r"#search",
    r"/search\?", r"/jobs\?", r"/find\?", r"/browse\?",
    r"/tim-viec", r"/danh-sach", r"/catalog\?",
]

# Patterns that identify ITEM pages — these have IDs or long slugs
ITEM_URL_PATTERNS = [
    r"/[a-z0-9-]+-\d{4,}(/|$)",        # slug-12345
    r"/\d{4,}(/|$|\.html)",              # /12345 or /12345.html
    r"/view/\d+",                        # /view/12345
    r"/[a-z0-9]{8,}(/|$)",              # long slug without numbers
    r"/jobs/[a-z0-9-]{10,}",            # /jobs/long-job-slug
    r"/products?/[a-z0-9-]{5,}",        # /product/name-slug
]


def is_listing_url(url: str) -> bool:
    """Return True if the URL looks like a listing/search page."""
    for pattern in LISTING_URL_PATTERNS:
        if re.search(pattern, url, re.IGNORECASE):
            return True
    return False


def is_item_url(url: str) -> bool:
    """Return True if the URL looks like a specific item detail page."""
    if is_listing_url(url):
        return False
    for pattern in ITEM_URL_PATTERNS:
        if re.search(pattern, url, re.IGNORECASE):
            return True
    return False


def extract_canonical_from_html(html: str, base_url: str) -> str | None:
    """Try to find canonical URL from HTML meta tags."""
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")

        # 1. <link rel="canonical">
        canonical = soup.find("link", rel="canonical")
        if canonical and canonical.get("href"):
            url = urljoin(base_url, canonical["href"])
            if is_item_url(url):
                return url

        # 2. Open Graph og:url
        og_url = soup.find("meta", property="og:url")
        if og_url and og_url.get("content"):
            url = urljoin(base_url, og_url["content"])
            if is_item_url(url):
                return url

        # 3. data-url or data-href attributes on main content element
        for attr in ["data-url", "data-href", "data-canonical"]:
            el = soup.find(attrs={attr: True})
            if el:
                url = urljoin(base_url, el[attr])
                if is_item_url(url):
                    return url

    except ImportError:
        pass
    return None


def extract_item_urls_from_listing(html: str, base_url: str, limit: int = 20) -> list:
    """Extract item URLs from a standard listing page."""
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        return []

    soup = BeautifulSoup(html, "html.parser")
    base_domain = urlparse(base_url).netloc
    items = []
    seen = set()

    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        full_url = urljoin(base_url, href)
        parsed = urlparse(full_url)

        if base_domain not in parsed.netloc:
            continue
        if full_url in seen:
            continue
        if not is_item_url(full_url):
            continue

        seen.add(full_url)
        title = a.get_text(strip=True)[:100] or ""
        items.append({
            "canonical_url": full_url,
            "title": title,
            "detection_method": "direct_link",
        })
        if len(items) >= limit:
            break

    return items


def click_and_capture_urls(listing_url: str, selector: str = None, limit: int = 20) -> list:
    """Use Playwright to click each item card and capture the URL after navigation."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise RuntimeError("Install playwright: pip install playwright && playwright install chromium")

    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
        ])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        )
        page = context.new_page()
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        try:
            page.goto(listing_url, wait_until="domcontentloaded", timeout=20000)
            page.wait_for_timeout(2000)

            # Find clickable item elements
            click_selector = selector or "a[href], [role='link'], [data-href], .job-card, .product-card"
            elements = page.query_selector_all(click_selector)

            for el in elements[:limit]:
                initial_url = page.url
                try:
                    # Open in new context to avoid losing listing page
                    href = el.get_attribute("href") or el.get_attribute("data-href") or ""
                    if href:
                        full_url = urljoin(listing_url, href)
                        if is_item_url(full_url) and full_url not in [r["canonical_url"] for r in results]:
                            title = el.text_content()[:80].strip() or ""
                            results.append({
                                "canonical_url": full_url,
                                "title": title,
                                "detection_method": "href_attribute",
                            })
                except Exception:
                    continue

            # If no hrefs found, try clicking and capturing navigation
            if not results:
                elements = page.query_selector_all(selector or ".item, .card, li[data-id]")
                for el in elements[:5]:  # Limited — each click loads a page
                    try:
                        with context.expect_page() as new_page_info:
                            el.click()
                        new_page = new_page_info.value
                        new_page.wait_for_load_state("domcontentloaded")
                        final_url = new_page.url
                        if is_item_url(final_url):
                            results.append({
                                "canonical_url": final_url,
                                "title": new_page.title()[:80],
                                "detection_method": "click_navigation",
                            })
                        new_page.close()
                    except Exception:
                        continue

        finally:
            browser.close()

    return results


def main():
    parser = argparse.ArgumentParser(description="Extract canonical detail-page URLs")
    parser.add_argument("listing_url", help="Listing/search results page URL")
    parser.add_argument("--item-selector", default=None, help="CSS selector for item cards")
    parser.add_argument("--click-and-capture", action="store_true",
                        help="Use Playwright to click items and capture navigation URL")
    parser.add_argument("--limit", type=int, default=20, help="Max items to extract")
    parser.add_argument("--output", default=None, help="Output file path")
    args = parser.parse_args()

    # Validate listing URL is actually a listing (not already an item page)
    if is_item_url(args.listing_url) and not is_listing_url(args.listing_url):
        result = {
            "listing_url": args.listing_url,
            "note": "URL appears to already be an item page",
            "items": [{"canonical_url": args.listing_url, "title": "", "detection_method": "already_item"}],
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.click_and_capture:
        items = click_and_capture_urls(args.listing_url, args.item_selector, args.limit)
    else:
        # Standard: fetch HTML and extract links
        try:
            import httpx
            with httpx.Client(timeout=15, follow_redirects=True) as client:
                resp = client.get(args.listing_url, headers={
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                })
                html = resp.text
        except ImportError:
            import urllib.request
            with urllib.request.urlopen(args.listing_url, timeout=15) as resp:
                html = resp.read().decode("utf-8", errors="replace")
        except Exception as e:
            print(json.dumps({"error": str(e), "items": []}))
            sys.exit(1)

        items = extract_item_urls_from_listing(html, args.listing_url, args.limit)

    # Final validation: reject any remaining listing URLs
    validated = []
    rejected = []
    for item in items:
        if is_listing_url(item["canonical_url"]):
            item["rejected_reason"] = "listing_page_pattern"
            rejected.append(item)
        else:
            validated.append(item)

    result = {
        "listing_url": args.listing_url,
        "items_found": len(validated),
        "items_rejected": len(rejected),
        "items": validated,
    }
    if rejected:
        result["rejected"] = rejected

    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Detail URLs saved: {args.output} ({len(validated)} valid, {len(rejected)} rejected, {len(output)} bytes)",
              file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
