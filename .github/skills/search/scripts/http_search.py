#!/usr/bin/env python3
"""
HTTP zero-auth search fallback (Tier 3, US-16.1.3).

Uses DuckDuckGo's HTML endpoint via plain httpx (no headless browser, no API key).
Distinct from Tier 2 (Playwright stealth) — used when Playwright is unavailable
(e.g. headless browser banned in the runtime environment) OR Tier 2 also returned
empty results.

Output (stdout) matches the primary search tool contract:
    {"query": "<query>", "results": [{"url","title","snippet"}, ...]}

Exit codes:
    0  Results found, JSON written to stdout
    1  Empty results (HTTP 200 but no matches)
    2  Error (network failure, parse error, etc.)

Usage:
    python3 http_search.py "<query>" [--limit N]

Dependencies: httpx, beautifulsoup4 (already in requirements.txt for Tier 1
URL fallback — no new dependencies introduced).
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
TIMEOUT_SECONDS = 10
DDG_HTML_URL = "https://html.duckduckgo.com/html/"


def search(query: str, limit: int) -> list[dict[str, Any]]:
    import httpx
    from bs4 import BeautifulSoup

    headers = {"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"}
    with httpx.Client(timeout=TIMEOUT_SECONDS, follow_redirects=True, headers=headers) as client:
        response = client.post(DDG_HTML_URL, data={"q": query, "kl": "wt-wt"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

    results: list[dict[str, Any]] = []
    for result_div in soup.select("div.result, div.web-result"):
        title_link = result_div.select_one("a.result__a")
        if title_link is None:
            continue
        url = title_link.get("href", "").strip()
        title = title_link.get_text(strip=True)
        snippet_el = result_div.select_one("a.result__snippet, div.result__snippet")
        snippet = snippet_el.get_text(strip=True) if snippet_el else ""
        if url and title:
            results.append({"url": url, "title": title, "snippet": snippet})
        if len(results) >= limit:
            break
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="HTTP zero-auth search (Tier 3)")
    parser.add_argument("query", help="Search query string")
    parser.add_argument("--limit", type=int, default=8, help="Max results (default 8)")
    args = parser.parse_args()

    try:
        results = search(args.query, args.limit)
    except Exception as exc:  # noqa: BLE001 — Tier-3 must never crash the pipeline
        sys.stderr.write(f"http_search error: {exc}\n")
        return 2

    if not results:
        return 1

    sys.stdout.write(json.dumps({"query": args.query, "results": results}, ensure_ascii=False))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
