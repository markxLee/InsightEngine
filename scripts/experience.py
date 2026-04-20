#!/usr/bin/env python3
"""
Experience template management (US-16.5.1 save / US-16.5.2 load).

An "experience template" is a JSON snapshot of a successful pipeline run
that captures the intent, the executed plan, per-step outcomes, total
budget used, and the final audit score. Future pipeline runs with similar
intent can load matching templates as a planning hint.

Storage: docs/experiences/<intent>/<YYYYMMDD-HHMMSS>-<short_hash>.json
(persistent — survives `tmp/` cleanup so templates accumulate across runs).

Subcommands:
    save    Persist a successful run (US-16.5.1).
    find    List recent saves for an intent (raw listing).
    match   Score saved templates against a new prompt and return best matches
            (US-16.5.2 — used by orchestrator at pipeline start).

Usage:
    experience.py save --state-file tmp/.session-state.json
    experience.py find --intent <intent> [--limit N]
    experience.py match --intent <intent> --prompt "<raw_user_prompt>" [--limit N] [--min-score F]
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import re
import sys
from pathlib import Path

EXPERIENCE_ROOT = Path("docs/experiences")
MIN_AUDIT_SCORE_TO_SAVE = 80
SCHEMA_VERSION = 1


def _short_hash(payload: str) -> str:
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:8]


def _extract_template(state: dict) -> dict | None:
    intent = state.get("intent_classification") or state.get("intent")
    if not intent:
        return None

    final_score = (
        state.get("final_audit_score")
        or state.get("audit_score")
        or _max_step_score(state)
    )
    if final_score is None or final_score < MIN_AUDIT_SCORE_TO_SAVE:
        return None

    plan = state.get("generated_plan") or state.get("plan") or []
    step_states = state.get("step_states") or []
    raw_prompt = state.get("raw_prompt", "")

    template = {
        "schema_version": SCHEMA_VERSION,
        "saved_at": datetime.datetime.utcnow().isoformat() + "Z",
        "intent": intent,
        "raw_prompt": raw_prompt,
        "raw_prompt_hash": _short_hash(raw_prompt),
        "plan_summary": [_summarize_step(p) for p in plan],
        "step_outcomes": [_summarize_outcome(s) for s in step_states],
        "final_audit_score": final_score,
        "budget_used": state.get("budget_used", {}),
        "output_formats": _detect_formats(step_states),
    }
    return template


def _summarize_step(step: dict) -> dict:
    return {
        "name": step.get("name") or step.get("skill") or "unknown",
        "tool": step.get("tool") or step.get("skill"),
        "purpose": (step.get("purpose") or step.get("description") or "")[:200],
    }


def _summarize_outcome(step_state: dict) -> dict:
    return {
        "name": step_state.get("name", "unknown"),
        "status": step_state.get("status", "unknown"),
        "audit_score": step_state.get("audit_score"),
        "retries": step_state.get("retries", 0),
    }


def _max_step_score(state: dict) -> int | None:
    scores = [
        s.get("audit_score")
        for s in state.get("step_states", [])
        if isinstance(s.get("audit_score"), (int, float))
    ]
    return max(scores) if scores else None


def _detect_formats(step_states: list) -> list[str]:
    formats: list[str] = []
    for step in step_states:
        name = (step.get("name") or "").lower()
        for fmt in ("word", "excel", "slide", "pdf", "html", "image"):
            if fmt in name and fmt not in formats:
                formats.append(fmt)
    return formats


def cmd_save(args: argparse.Namespace) -> int:
    state_path = Path(args.state_file)
    if not state_path.is_file():
        sys.stderr.write(f"State file not found: {state_path}\n")
        return 2

    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"State file is not valid JSON: {exc}\n")
        return 2

    template = _extract_template(state)
    if template is None:
        sys.stderr.write(
            "Pipeline did not meet save criteria "
            f"(needs intent + final audit score >= {MIN_AUDIT_SCORE_TO_SAVE}).\n"
        )
        return 1

    intent_dir = EXPERIENCE_ROOT / template["intent"]
    intent_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    out_path = intent_dir / f"{timestamp}-{template['raw_prompt_hash']}.json"
    out_path.write_text(json.dumps(template, ensure_ascii=False, indent=2), encoding="utf-8")

    sys.stdout.write(f"EXPERIENCE_SAVED: {out_path}\n")
    return 0


def cmd_find(args: argparse.Namespace) -> int:
    intent_dir = EXPERIENCE_ROOT / args.intent
    if not intent_dir.is_dir():
        sys.stderr.write(f"No experiences saved for intent: {args.intent}\n")
        return 1
    files = sorted(intent_dir.glob("*.json"), reverse=True)[: args.limit]
    sys.stdout.write(json.dumps([str(f) for f in files], ensure_ascii=False) + "\n")
    return 0


# ---------- US-16.5.2 — match ----------

_TOKEN_RE = re.compile(r"[\w\u00C0-\u024F\u1E00-\u1EFF]+", re.UNICODE)
_STOPWORDS = {
    # English
    "the", "a", "an", "and", "or", "of", "to", "for", "in", "on", "at", "from",
    "with", "by", "is", "are", "be", "this", "that", "it", "as", "i", "we",
    # Vietnamese (high-frequency)
    "và", "hoặc", "của", "cho", "với", "là", "tôi", "bạn", "một", "các",
    "những", "này", "đó", "có", "không", "được", "để", "trong", "từ", "về",
}


def _tokenize(text: str) -> set[str]:
    return {
        token.lower()
        for token in _TOKEN_RE.findall(text or "")
        if len(token) > 1 and token.lower() not in _STOPWORDS
    }


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def cmd_match(args: argparse.Namespace) -> int:
    intent_dir = EXPERIENCE_ROOT / args.intent
    if not intent_dir.is_dir():
        sys.stdout.write(json.dumps({"matches": [], "reason": "no_experiences_for_intent"}) + "\n")
        return 1

    prompt_tokens = _tokenize(args.prompt)
    if not prompt_tokens:
        sys.stdout.write(json.dumps({"matches": [], "reason": "empty_prompt_after_tokenize"}) + "\n")
        return 1

    scored: list[dict] = []
    for path in intent_dir.glob("*.json"):
        try:
            template = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        score = _jaccard(prompt_tokens, _tokenize(template.get("raw_prompt", "")))
        if score >= args.min_score:
            scored.append({
                "path": str(path),
                "score": round(score, 3),
                "saved_at": template.get("saved_at"),
                "final_audit_score": template.get("final_audit_score"),
                "output_formats": template.get("output_formats", []),
                "plan_summary": template.get("plan_summary", []),
            })

    scored.sort(key=lambda x: (x["score"], x["final_audit_score"] or 0), reverse=True)
    matches = scored[: args.limit]
    sys.stdout.write(json.dumps({"matches": matches, "reason": "ok"}, ensure_ascii=False) + "\n")
    return 0 if matches else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Experience template management")
    sub = parser.add_subparsers(dest="command", required=True)

    save = sub.add_parser("save", help="Save experience template after successful pipeline")
    save.add_argument("--state-file", default="tmp/.session-state.json")
    save.set_defaults(func=cmd_save)

    find = sub.add_parser("find", help="List recent experiences for an intent")
    find.add_argument("--intent", required=True)
    find.add_argument("--limit", type=int, default=5)
    find.set_defaults(func=cmd_find)

    match = sub.add_parser("match", help="Find best-matching experience templates (US-16.5.2)")
    match.add_argument("--intent", required=True)
    match.add_argument("--prompt", required=True, help="Raw user prompt to match against")
    match.add_argument("--limit", type=int, default=3)
    match.add_argument("--min-score", type=float, default=0.15,
                       help="Minimum Jaccard similarity to include (default 0.15)")
    match.set_defaults(func=cmd_match)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
