#!/usr/bin/env python3
"""
Filter extracted jobs for fresher/junior (<=2 years) and save to tmp/jobs_extracted_filtered.json
"""
import json, re, os

INPUTS = ['tmp/jobs_extracted_playwright.json','tmp/jobs_extracted.json']
OUT = 'tmp/jobs_extracted_filtered.json'

KEYWORDS = ['fresher','junior','entry-level','entry level','intern','internship','mới','moi','mới tốt nghiệp','thực tập','new grad','graduate']
EXCLUDE_TITLE = ['senior','lead','team lead','manager','principal','director']

def score_job(j):
    title = (j.get('job_title') or '').lower()
    exp_raw = (j.get('years_of_experience_raw') or '').lower()
    salary = j.get('salary_raw','')
    # exclude obvious senior roles by title
    for e in EXCLUDE_TITLE:
        if e in title:
            return 0
    # prefer explicit keywords
    for k in KEYWORDS:
        if k in title or k in exp_raw:
            return 10
    # try parse numeric years from experience text
    m = re.findall(r'(\d+(?:[\.,]\d+)?)\s*(?:year|years|năm)', exp_raw)
    if m:
        try:
            vals = [float(x.replace(',','.')) for x in m]
            if max(vals) <= 2.0:
                return 8
            else:
                return 0
        except:
            pass
    # fallback: look for '0' or '1' ranges
    m2 = re.search(r'0\s*[-–to]\s*2|0\s*[-–to]\s*1|1\s*[-–to]\s*2', exp_raw)
    if m2:
        return 8
    # otherwise low score
    return 0

def main():
    jobs = []
    for p in INPUTS:
        if os.path.exists(p):
            try:
                data = json.load(open(p,'r',encoding='utf-8'))
                jobs.extend(data.get('jobs',[]))
            except Exception:
                pass
    uniq = {}
    for j in jobs:
        url = j.get('job_detail_url') or (j.get('sources',[{}])[0].get('url') if j.get('sources') else None)
        key = url or (j.get('job_title','')+j.get('company_name',''))
        if key in uniq:
            continue
        sc = score_job(j)
        if sc>0:
            uniq[key]=j
    out_list = list(uniq.values())
    os.makedirs('tmp', exist_ok=True)
    json.dump({'generated_at': __import__('datetime').datetime.utcnow().isoformat()+'Z', 'jobs': out_list}, open(OUT,'w',encoding='utf-8'), ensure_ascii=False, indent=2)
    print('Filtered', len(out_list), 'jobs ->', OUT)

if __name__=='__main__':
    main()
