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

## Privacy / Hygiene

Raw user prompts are stored verbatim. Strip any sensitive content before
running the orchestrator if that matters for your installation, OR delete
specific files under this directory after the fact (no metadata index to
update — files are self-contained).
