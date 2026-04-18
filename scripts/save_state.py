#!/usr/bin/env python3
"""Session state manager for InsightEngine pipeline.

Commands:
    python3 scripts/save_state.py check        # Check if a session state exists
    python3 scripts/save_state.py save <json>   # Save current state (JSON string or @file)
    python3 scripts/save_state.py resume-plan   # Return pending steps as JSON
    python3 scripts/save_state.py archive       # Archive current state and start fresh
    python3 scripts/save_state.py update --step <name> [--output-file <path>]  # Update step status
    python3 scripts/save_state.py complete      # Mark pipeline as completed

State file: tmp/.session-state.json

Enhanced Schema (v2 — Phase 9):
    raw_prompt: str             # Original user request
    intent_classification: str  # synthesis | creation | research | design | data_collection | mixed
    analyzed_requirements: dict # Expanded dimensions from analysis
    generated_plan: dict        # Workflow plan from strategist
    step_states: list           # Per-step: {name, status, input_summary, output_summary, started_at, completed_at}
    audit_test_cases: list      # Dynamic test cases from auditor
    score_history: list         # [{attempt, score, failing_tests}]
    created_skills: list        # Runtime-created skills/agents
    output_files: list          # [{path, hash, format, size}]
    status: str                 # IN_PROGRESS | COMPLETED | FAILED
    schema_version: int         # 2
"""

import hashlib
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Resolve project root relative to this script
PROJECT_ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = PROJECT_ROOT / "tmp" / ".session-state.json"
ARCHIVE_DIR = PROJECT_ROOT / "tmp" / "archives"


def ensure_dirs():
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)


def load_state() -> Optional[dict]:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return None
    return None


def cmd_check():
    state = load_state()
    if state is None:
        print("NO_STATE")
        return

    status = state.get("status", "UNKNOWN")
    version = state.get("schema_version", 1)
    if status == "COMPLETED":
        print("COMPLETED")
        return

    # IN_PROGRESS — show summary
    print(f"IN_PROGRESS (schema v{version})")
    print(f"Request: {state.get('raw_prompt', state.get('original_request', 'N/A'))[:200]}")
    if version >= 2:
        print(f"Intent: {state.get('intent_classification', 'N/A')}")
        steps = state.get("step_states", [])
        done = [s for s in steps if s.get("status") == "completed"]
        pending = [s for s in steps if s.get("status") in ("pending", "not_started")]
        running = [s for s in steps if s.get("status") == "in_progress"]
        print(f"Steps: {len(done)} done, {len(running)} running, {len(pending)} pending")
        scores = state.get("score_history", [])
        if scores:
            latest = scores[-1]
            print(f"Latest audit: {latest.get('score', 'N/A')}/100 (attempt {latest.get('attempt', '?')})")
    else:
        print(f"Current step: {state.get('current_step', 'N/A')}")
        completed = state.get("completed_steps", [])
        pending = state.get("pending_steps", [])
        print(f"Completed: {len(completed)} steps — {', '.join(completed)}")
        print(f"Pending: {len(pending)} steps — {', '.join(pending)}")
    print(f"Started: {state.get('started_at', 'N/A')}")


def cmd_save(data_arg: str):
    ensure_dirs()
    if data_arg.startswith("@"):
        filepath = Path(data_arg[1:])
        data = json.loads(filepath.read_text(encoding="utf-8"))
    else:
        data = json.loads(data_arg)

    # Auto-set schema_version if not present
    if "schema_version" not in data:
        if "step_states" in data or "raw_prompt" in data:
            data["schema_version"] = 2
        else:
            data["schema_version"] = 1

    data["updated_at"] = datetime.now().isoformat()
    STATE_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"STATE_SAVED: {STATE_FILE}")


def cmd_resume_plan():
    state = load_state()
    if state is None:
        print(json.dumps({"error": "NO_STATE"}, ensure_ascii=False))
        sys.exit(1)

    version = state.get("schema_version", 1)
    if version >= 2:
        steps = state.get("step_states", [])
        pending = [s for s in steps if s.get("status") in ("pending", "not_started")]
        plan = {
            "raw_prompt": state.get("raw_prompt", ""),
            "intent_classification": state.get("intent_classification", ""),
            "pending_steps": [s["name"] for s in pending],
            "step_states": pending,
            "generated_plan": state.get("generated_plan", {}),
            "content_depth": state.get("content_depth", "comprehensive"),
            "score_history": state.get("score_history", []),
        }
    else:
        pending = state.get("pending_steps", [])
        plan = {
            "original_request": state.get("original_request", ""),
            "current_step": state.get("current_step", ""),
            "pending_steps": pending,
            "execution_plan": state.get("execution_plan", {}),
            "content_depth": state.get("content_depth", "comprehensive"),
        }
    print(json.dumps(plan, indent=2, ensure_ascii=False))


def file_hash(filepath: str) -> str:
    """Compute SHA-256 hash of a file for integrity tracking."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def cmd_update(args: list):
    """Update a specific step's status in the state file.
    Usage: save_state.py update --step <name> [--status completed|failed|in_progress] [--output-file <path>]
    """
    state = load_state()
    if state is None:
        print("Error: NO_STATE — save state first")
        sys.exit(1)

    step_name = None
    status = "completed"
    output_file = None

    i = 0
    while i < len(args):
        if args[i] == "--step" and i + 1 < len(args):
            step_name = args[i + 1]
            i += 2
        elif args[i] == "--status" and i + 1 < len(args):
            status = args[i + 1]
            i += 2
        elif args[i] == "--output-file" and i + 1 < len(args):
            output_file = args[i + 1]
            i += 2
        else:
            i += 1

    if not step_name:
        print("Error: --step is required")
        sys.exit(1)

    # Update step_states (v2 schema)
    steps = state.get("step_states", [])
    found = False
    for step in steps:
        if step["name"] == step_name:
            step["status"] = status
            if status == "completed":
                step["completed_at"] = datetime.now().isoformat()
            elif status == "in_progress":
                step["started_at"] = datetime.now().isoformat()
            found = True
            break

    if not found:
        steps.append({
            "name": step_name,
            "status": status,
            "started_at": datetime.now().isoformat() if status == "in_progress" else None,
            "completed_at": datetime.now().isoformat() if status == "completed" else None,
        })
        state["step_states"] = steps

    # Track output file
    if output_file and Path(output_file).exists():
        output_files = state.get("output_files", [])
        p = Path(output_file)
        output_files.append({
            "path": str(p),
            "hash": file_hash(output_file),
            "format": p.suffix.lstrip("."),
            "size": p.stat().st_size,
        })
        state["output_files"] = output_files

    state["updated_at"] = datetime.now().isoformat()
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"STEP_UPDATED: {step_name} → {status}")


def cmd_complete():
    """Mark the pipeline as completed."""
    state = load_state()
    if state is None:
        print("Error: NO_STATE")
        sys.exit(1)

    state["status"] = "COMPLETED"
    state["completed_at"] = datetime.now().isoformat()
    state["updated_at"] = datetime.now().isoformat()
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"PIPELINE_COMPLETED at {state['completed_at']}")


def cmd_archive():
    state = load_state()
    if state is None:
        print("NO_STATE — nothing to archive")
        return

    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_path = ARCHIVE_DIR / f"session-state_{timestamp}.json"
    shutil.copy2(STATE_FILE, archive_path)
    STATE_FILE.unlink()
    print(f"ARCHIVED: {archive_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: save_state.py <check|save|resume-plan|update|complete|archive> [data]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "check":
        cmd_check()
    elif command == "save":
        if len(sys.argv) < 3:
            print("Error: save requires a JSON argument")
            sys.exit(1)
        cmd_save(sys.argv[2])
    elif command == "resume-plan":
        cmd_resume_plan()
    elif command == "update":
        cmd_update(sys.argv[2:])
    elif command == "complete":
        cmd_complete()
    elif command == "archive":
        cmd_archive()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
