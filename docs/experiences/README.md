# Experience Templates

Persistent storage for successful pipeline-run snapshots. Created and managed
by [`scripts/experience.py`](../../scripts/experience.py). See US-16.5.1 for
the save behaviour and US-16.5.2 for load/match behaviour.

## Layout

```
docs/experiences/
  <intent>/
    <YYYYMMDD-HHMMSS>-<short-hash>.json
```

Where `<intent>` is the orchestrator's classified intent
(`synthesis`, `creation`, `research`, `design`, `data_collection`, `mixed`).

## Schema

See `experience.py::_extract_template` — current schema_version is `1`. Each
template captures: intent, raw prompt + hash, plan summary, per-step
outcomes (status + audit_score + retries), final audit score, budget used,
detected output formats.

## Save Criteria (US-16.5.1)

Templates are saved ONLY when:

- `intent_classification` is set in the session state
- `final_audit_score` (or max step audit_score) is `>= 80`

Failed or low-quality runs are deliberately not preserved — the goal is to
accumulate exemplars worth replaying, not noise.

## Match Behaviour (US-16.5.2)

Subcommand: `experience.py match --intent <intent> --prompt "<raw>"`.

Algorithm:

1. Filter to `docs/experiences/<intent>/`.
2. Tokenize both the new prompt and each saved `raw_prompt` (Unicode word
   regex; lowercase; drop tokens of length ≤ 1; drop English/Vietnamese
   stopwords).
3. Score each candidate by Jaccard similarity of token sets.
4. Drop candidates below `--min-score` (default `0.15`).
5. Sort by `(score DESC, final_audit_score DESC)` and return top `--limit`
   (default 3) as JSON.

Output JSON shape:

```json
{
  "matches": [
    {"path": "...", "score": 0.7, "saved_at": "...", "final_audit_score": 91,
     "output_formats": ["word"], "plan_summary": [...]}
  ],
  "reason": "ok"
}
```

The orchestrator (step 2d, before strategist call) reads `matches` and, if
non-empty, passes the top match's `plan_summary` + `output_formats` to the
strategist as a non-binding `prior_experience` hint. Strategist remains free
to adapt or discard.

## Privacy / Hygiene

Raw user prompts are stored verbatim. Strip any sensitive content before
running the orchestrator if that matters for your installation, OR delete
specific files under this directory after the fact (no metadata index to
update — files are self-contained).
