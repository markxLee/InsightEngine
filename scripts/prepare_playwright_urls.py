#!/usr/bin/env python3
"""
Prepare a JSON file with job-detail links for Playwright parser.
Reads `tmp/listings_raw.json` and writes `tmp/itviec_job_urls.json` with structure {"links": [...]}
"""
import json
import os
from urllib.parse import urlparse

IN = 'tmp/listings_raw.json'
OUT = 'tmp/itviec_job_urls.json'

def plausible_job_url(u):
    if not u:
        return False
    u = u.lower()
    terms = ['job', 'viec', 'viec-lam', 'it-jobs', 'jobs', 'ung-vien', 'recruit', 'career', '/viec-lam/']
    try:
        parsed = urlparse(u)
        if parsed.scheme not in ('http','https'):
            return False
    except Exception:
        return False
    for t in terms:
        if t in u:
            return True
    return False

def main(limit=20, platforms=None):
    os.makedirs('tmp', exist_ok=True)
    if not os.path.exists(IN):
        print('Input listings not found:', IN)
        return
    data = json.load(open(IN, 'r', encoding='utf-8'))
    links = []
    seen = set()
    for batch in data.get('batches', []):
        p = batch.get('platform')
        if platforms and p not in platforms:
            continue
        for entry in batch.get('entries', []):
            for u in entry.get('found_urls', []):
                if len(links) >= limit:
                    break
                if not plausible_job_url(u):
                    continue
                if u in seen:
                    continue
                seen.add(u)
                links.append(u)
            if len(links) >= limit:
                break
        if len(links) >= limit:
            break

    out = {'generated_at': __import__('datetime').datetime.utcnow().isoformat()+'Z', 'links': links}
    open('tmp/itviec_job_urls.json', 'w', encoding='utf-8').write(json.dumps(out, ensure_ascii=False, indent=2))
    print(f'Wrote {len(links)} links -> tmp/itviec_job_urls.json')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, default=20)
    parser.add_argument('--platforms', type=str, default='itviec,topcv,vietnamworks')
    args = parser.parse_args()
    plats = [p.strip() for p in args.platforms.split(',') if p.strip()]
    main(limit=args.limit, platforms=plats)
