#!/usr/bin/env python3
"""
Playwright Stealth Search — Tier 2 fallback for the search skill.

Performs a search engine query via DuckDuckGo HTML (no JS required) using the
same anti-detection stack as playwright_fetch.py. Returns results in the same
shape as vscode-websearchforcopilot_webSearch:

    [{"url": ..., "title": ..., "snippet": ...}, ...]

Usage:
    python3 playwright_search.py "<query>" [--limit N] [--engine duckduckgo|google]

Prints JSON to stdout. Exits 0 on success (results found), 1 on no results,
2 on error. NEVER prints credentials, auth prompts, or fallback diagnostics.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from typing import Any
from urllib.parse import quote_plus, urlparse, parse_qs, unquote

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
)

LAUNCH_ARGS = [
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-dev-shm-usage",
    "--disable-blink-features=AutomationControlled",
    "--no-first-run",
    "--disable-extensions",
    "--disable-client-side-phishing-detection",
]

INIT_SCRIPT = """
Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
window.chrome = {runtime: {}};
Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
Object.defineProperty(navigator, 'languages', {get: () => ['en-US','en','vi']});
"""


def _clean_ddg_url(href: str) -> str:
    """DuckDuckGo HTML links wrap targets in /l/?uddg=<encoded>. Unwrap."""
    if not href:
        return ""
    if href.startswith("//"):
        href = "https:" + href
    if "duckduckgo.com/l/" in href or href.startswith("/l/"):
        try:
            qs = parse_qs(urlparse(href).query)
            if "uddg" in qs:
                return unquote(qs["uddg"][0])
        except Exception:
            pass
    return href


def search_duckduckgo(query: str, limit: int = 10) -> list[dict[str, str]]:
    from playwright.sync_api import sync_playwright

    url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
    results: list[dict[str, str]] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=LAUNCH_ARGS)
        try:
            context = browser.new_context(
                user_agent=USER_AGENT,
                viewport={"width": 1440, "height": 900},
                locale="en-US",
                timezone_id="Asia/Ho_Chi_Minh",
                ignore_https_errors=True,
                bypass_csp=True,
                extra_http_headers={
                    "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                },
            )
            context.add_init_script(INIT_SCRIPT)
            page = context.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=20000)
            time.sleep(1.0)

            # html.duckduckgo.com uses .result blocks
            blocks = page.query_selector_all("div.result, div.web-result")
            for b in blocks:
                if len(results) >= limit:
                    break
                title_el = b.query_selector("a.result__a, h2 a")
                snippet_el = b.query_selector(".result__snippet, .snippet")
                if not title_el:
                    continue
                href = title_el.get_attribute("href") or ""
                href = _clean_ddg_url(href)
                if not href.startswith("http"):
                    continue
                title = (title_el.inner_text() or "").strip()
                snippet = (snippet_el.inner_text() or "").strip() if snippet_el else ""
                results.append({"url": href, "title": title, "snippet": snippet})
        finally:
            browser.close()

    return results


def main() -> int:
    ap = argparse.ArgumentParser(description="Playwright stealth search fallback")
    ap.add_argument("query", help="Search query")
    ap.add_argument("--limit", type=int, default=10, help="Max results (default 10)")
    ap.add_argument(
        "--engine",
        default="duckduckgo",
        choices=["duckduckgo"],
        help="Search engine (only duckduckgo supported in v1)",
    )
    args = ap.parse_args()

    try:
        if args.engine == "duckduckgo":
            results = search_duckduckgo(args.query, limit=args.limit)
        else:
            results = []
    except Exception as e:
        # Stay silent for the user. Diagnostic on stderr only.
        print(f"playwright_search error: {type(e).__name__}: {e}", file=sys.stderr)
        return 2

    print(json.dumps({"query": args.query, "results": results}, ensure_ascii=False, indent=2))
    return 0 if results else 1


if __name__ == "__main__":
    sys.exit(main())
