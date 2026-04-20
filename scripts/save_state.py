#!/usr/bin/env python3
"""Session state manager for InsightEngine pipeline.

Commands:
    python3 scripts/save_state.py init '<prompt>' [intent]  # FIRST CALL: save raw prompt immediately
    python3 scripts/save_state.py extract-requirements      # Parse raw_prompt → structured requirements list
    python3 scripts/save_state.py check        # Check if a session state exists
    python3 scripts/save_state.py save <json>   # Save current state (JSON string or @file)
    python3 scripts/save_state.py resume-plan   # Return pending steps as JSON
    python3 scripts/save_state.py archive       # Archive current state and start fresh
    python3 scripts/save_state.py update --step <name> [--output-file <path>]  # Update step status
    python3 scripts/save_state.py complete      # Mark pipeline as completed
    python3 scripts/save_state.py set-mode <guided|standard|silent>  # Update session mode
    python3 scripts/save_state.py log-emission --type <type> --reason "<reason>" [--consultation '<json>']  # Log user emission
    python3 scripts/save_state.py register-artifact --step <name> --path <path> --type <type> --summary "<text>" [--score <n>] [--retention keep|transient]  # Register artifact
    python3 scripts/save_state.py list-artifacts [--step <name>] [--type <type>]  # List artifacts as JSON
    python3 scripts/save_state.py read-context <step>  # Read full context for a step (requirements + artifacts + summaries)

State file: tmp/.session-state.json  (hidden file — use: ls -la tmp/)

Enhanced Schema (v4 — Phase 18 update):
    raw_prompt: str             # Original user request — saved FIRST before any processing
    intent_classification: str  # synthesis | creation | research | design | data_collection | mixed
    structured_requirements: dict  # Parsed from raw_prompt: output_files[], fields_required, filters, grouping, format_constraints
    analyzed_requirements: dict # Expanded dimensions from analysis
    generated_plan: dict        # Workflow plan from strategist
    step_states: list           # Per-step: {name, status, input_summary, output_summary, started_at, completed_at, artifacts[]}
    audit_test_cases: list      # Dynamic test cases from auditor
    score_history: list         # [{attempt, score, failing_tests}]
    created_skills: list        # Runtime-created skills/agents
    output_files: list          # [{path, hash, format, size}]
    status: str                 # IN_PROGRESS | COMPLETED | FAILED
    schema_version: int         # 4
    # Mode tracking (Phase 12 — persists across resume)
    session_mode: str           # guided | standard | silent  (default: guided)
    autonomy_mode: bool         # true after user approves plan
    consecutive_approvals: int  # reset on modification
    frustration_detected: bool
    # Delivery channel tracking (Phase 17)
    question_budget: dict       # {max: 2, used: 0, log: [{question, timestamp, consultation_log}]}
    user_emissions: list        # [{type, timestamp, reason, ?consultation_log}]
    template_validations: list  # [{skill, template, timestamp, result}]
    # Artifact registry (Phase 18) — each step_states[] entry gains artifacts[]
    # Each artifact: {path, source_step, content_type, summary, quality_score, retention}
    # content_type: search_result | gathered_content | draft_output | chart | data | other
    # retention: keep | transient
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
            state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
            # Migrate v3 → v4: ensure artifacts[] on each step_states entry
            if state and state.get("schema_version", 1) < 4:
                state["schema_version"] = 4
                for step in state.get("step_states", []):
                    step.setdefault("artifacts", [])
            return state
        except (json.JSONDecodeError, OSError):
            return None
    return None


def cmd_init(prompt: str, intent: str = "unknown"):
    """FIRST CALL: save raw_prompt immediately before any processing.
    Usage: save_state.py init '<user prompt>' [intent]
    This is the insurance against context loss — call this BEFORE Step 1.5 analysis.
    """
    ensure_dirs()
    # If existing IN_PROGRESS state, archive it first
    existing = load_state()
    if existing and existing.get("status") == "IN_PROGRESS":
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_path = ARCHIVE_DIR / f"session-state_{timestamp}.json"
        import shutil
        shutil.copy2(STATE_FILE, archive_path)

    state = {
        "schema_version": 4,
        "raw_prompt": prompt,
        "intent_classification": intent,
        "status": "IN_PROGRESS",
        "session_mode": "guided",
        "autonomy_mode": False,
        "consecutive_approvals": 0,
        "frustration_detected": False,
        "structured_requirements": {},
        "analyzed_requirements": {},
        "generated_plan": {},
        "step_states": [],
        "child_workflows": {},     # {step_id: {plan, step_states, status}}
        "audit_test_cases": [],
        "score_history": [],
        "created_skills": [],
        "output_files": [],
        "question_budget": {"max": 2, "used": 0, "log": []},
        "user_emissions": [],
        "template_validations": [],
        "started_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"STATE_INITIALIZED: {STATE_FILE}")
    print(f"Prompt saved ({len(prompt)} chars). Run 'check' to verify.")


def cmd_set_mode(mode: str):
    """Update session_mode and autonomy_mode in the state file.
    Usage: save_state.py set-mode guided|standard|silent
    """
    state = load_state()
    if state is None:
        print("Error: NO_STATE — run init first")
        sys.exit(1)
    valid_modes = ("guided", "standard", "silent")
    if mode not in valid_modes:
        print(f"Error: mode must be one of {valid_modes}")
        sys.exit(1)
    state["session_mode"] = mode
    state["autonomy_mode"] = mode in ("standard", "silent")
    state["updated_at"] = datetime.now().isoformat()
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"MODE_SET: session_mode={mode}, autonomy_mode={state['autonomy_mode']}")


def cmd_extract_requirements(requirements_json: str = None):
    """Parse raw_prompt into a structured requirements list and save to state.
    Usage: save_state.py extract-requirements [json_string]

    If json_string is provided, it must be a JSON object with typed requirement fields.
    If omitted, Copilot calls this after performing its own analysis of raw_prompt and
    passes the structured object as argument.

    Structured requirements schema (requirement-anchor.md):
        output_files: list[{name, type, structure_hint}]
            # e.g., [{name: "jobs.xlsx", type: "excel", structure_hint: "one sheet per province"}]
        fields_required: dict[output_name → list[str]]
            # e.g., {"jobs.xlsx": ["company_name", "province", "salary", "experience", "skills", "job_url"]}
        filters: list[str]
            # e.g., ["only fresher/junior roles", "max 2 years experience", "Vietnam only"]
        grouping: list[str]
            # e.g., ["by province/city", "by company"]
        format_constraints: list[str]
            # e.g., ["one sheet per province", "10-20 slides", "include charts"]
        sources: list[str]
            # e.g., ["ITViec", "TopCV", "VietnamWorks", "LinkedIn"]
        content_requirements: list[str]
            # e.g., ["company ratings", "review links", "work environment ranking"]
    """
    state = load_state()
    if state is None:
        print("Error: NO_STATE — run init first")
        sys.exit(1)

    if requirements_json:
        try:
            reqs = json.loads(requirements_json)
        except json.JSONDecodeError as e:
            print(f"Error: invalid JSON — {e}")
            sys.exit(1)
    else:
        # Return schema template for Copilot to fill
        reqs = {
            "output_files": [],
            "fields_required": {},
            "filters": [],
            "grouping": [],
            "format_constraints": [],
            "sources": [],
            "content_requirements": [],
        }
        print("REQUIREMENTS_SCHEMA (fill and pass as argument):")
        print(json.dumps(reqs, indent=2, ensure_ascii=False))
        return

    state["structured_requirements"] = reqs
    state["updated_at"] = datetime.now().isoformat()
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")

    # Print summary for verification
    n_outputs = len(reqs.get("output_files", []))
    n_filters = len(reqs.get("filters", []))
    n_fields = sum(len(v) for v in reqs.get("fields_required", {}).values())
    print(f"REQUIREMENTS_SAVED: {n_outputs} output files, {n_filters} filters, {n_fields} required fields")
    print(f"Grouping: {reqs.get('grouping', [])}")
    print(f"Format constraints: {reqs.get('format_constraints', [])}")
    print("Run 'check-requirements' or 'check' to verify.")


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
    # Mode info (v3)
    if version >= 3:
        mode = state.get("session_mode", "guided")
        auto = state.get("autonomy_mode", False)
        print(f"Mode: {mode} | autonomy_mode: {auto}")
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
            data["schema_version"] = 4
        else:
            data["schema_version"] = 1

    # Preserve session_mode/autonomy_mode from existing state if not in new data
    existing = load_state()
    if existing:
        for field in ("session_mode", "autonomy_mode", "consecutive_approvals", "frustration_detected"):
            if field not in data and field in existing:
                data[field] = existing[field]

    # Default mode fields if still missing
    data.setdefault("session_mode", "guided")
    data.setdefault("autonomy_mode", False)
    data.setdefault("consecutive_approvals", 0)
    data.setdefault("frustration_detected", False)

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
            # Mode fields — restore these on resume so user doesn't re-confirm
            "session_mode": state.get("session_mode", "guided"),
            "autonomy_mode": state.get("autonomy_mode", False),
            "frustration_detected": state.get("frustration_detected", False),
            # Phase 13 fields — restore for per-requirement scoring and child workflow state
            "structured_requirements": state.get("structured_requirements", {}),
            "child_workflows": state.get("child_workflows", {}),
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


def cmd_log_emission(args: list):
    """Log a user-facing emission to session state (US-17.1.3 / US-17.2.2).
    Usage: save_state.py log-emission --type <result_delivery|user_question|status_update>
                                      --reason "<reason>"
                                      [--consultation '<json>']
    For user_question type: increments question_budget.used and logs consultation evidence.
    """
    state = load_state()
    if state is None:
        print("Error: NO_STATE — run init first")
        sys.exit(1)

    emission_type = None
    reason = ""
    consultation = None
    timestamp = datetime.now().isoformat()

    i = 0
    while i < len(args):
        if args[i] == "--type" and i + 1 < len(args):
            emission_type = args[i + 1]; i += 2
        elif args[i] == "--reason" and i + 1 < len(args):
            reason = args[i + 1]; i += 2
        elif args[i] == "--consultation" and i + 1 < len(args):
            try:
                consultation = json.loads(args[i + 1])
            except json.JSONDecodeError:
                consultation = {"raw": args[i + 1]}
            i += 2
        elif args[i] == "--timestamp" and i + 1 < len(args):
            timestamp = args[i + 1]; i += 2
        else:
            i += 1

    if not emission_type:
        print("Error: --type is required (result_delivery|user_question|status_update)")
        sys.exit(1)

    # Ensure backward compatibility — add fields if missing
    if "user_emissions" not in state:
        state["user_emissions"] = []
    if "question_budget" not in state:
        state["question_budget"] = {"max": 2, "used": 0, "log": []}
    if "template_validations" not in state:
        state["template_validations"] = []

    emission = {
        "type": emission_type,
        "timestamp": timestamp,
        "reason": reason,
    }

    # For user_question: enforce budget and log consultation
    if emission_type == "user_question":
        budget = state["question_budget"]
        if budget["used"] >= budget["max"]:
            print(f"BUDGET_EXHAUSTED: question budget {budget['used']}/{budget['max']} — cannot ask user")
            sys.exit(1)
        budget["used"] += 1
        log_entry = {
            "question": reason,
            "timestamp": timestamp,
        }
        if consultation:
            log_entry["consultation_log"] = consultation
            emission["consultation_log"] = consultation
        budget["log"].append(log_entry)
        print(f"QUESTION_LOGGED: {budget['used']}/{budget['max']} used")

    state["user_emissions"].append(emission)
    state["updated_at"] = datetime.now().isoformat()
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"EMISSION_LOGGED: type={emission_type}, reason={reason[:80]}")


def file_hash(filepath: str) -> str:
    """Compute SHA-256 hash of a file for integrity tracking."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def cmd_update(args: list):
    """Update a specific step's status in the state file.
    Usage: save_state.py update --step <name> [--status completed|failed|in_progress]
                                              [--output-file <path>]
                                              [--audit-score <0-100>]
                                              [--req-scores <json>]
    """
    state = load_state()
    if state is None:
        print("Error: NO_STATE — save state first")
        sys.exit(1)

    step_name = None
    status = "completed"
    output_file = None
    audit_score = None
    req_scores = None  # list of per-requirement score dicts

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
        elif args[i] == "--audit-score" and i + 1 < len(args):
            try:
                audit_score = int(args[i + 1])
            except ValueError:
                pass
            i += 2
        elif args[i] == "--req-scores" and i + 1 < len(args):
            try:
                req_scores = json.loads(args[i + 1])
            except json.JSONDecodeError:
                pass
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
            if audit_score is not None:
                step["audit_score"] = audit_score
            if req_scores is not None:
                step["per_requirement_scores"] = req_scores
            found = True
            break

    if not found:
        new_step = {
            "name": step_name,
            "status": status,
            "started_at": datetime.now().isoformat() if status == "in_progress" else None,
            "completed_at": datetime.now().isoformat() if status == "completed" else None,
            "artifacts": [],
        }
        if audit_score is not None:
            new_step["audit_score"] = audit_score
        if req_scores is not None:
            new_step["per_requirement_scores"] = req_scores
        steps.append(new_step)
        state["step_states"] = steps

    # Track per-requirement scores in score_history
    if req_scores is not None:
        score_history = state.get("score_history", [])
        attempt_num = len(score_history) + 1
        score_history.append({
            "attempt": attempt_num,
            "step": step_name,
            "score": audit_score,
            "per_requirement_scores": req_scores,
            "failing_requirements": [r for r in req_scores if not r.get("pass", True)],
            "timestamp": datetime.now().isoformat(),
        })
        state["score_history"] = score_history

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


def cmd_register_artifact(args: list):
    """Register an artifact under a specific step in the state file.
    Usage: save_state.py register-artifact --step <name> --path <path>
                                           --type <search_result|gathered_content|draft_output|chart|data|other>
                                           --summary "<text>"
                                           [--score <0-100>]
                                           [--retention keep|transient]
    """
    state = load_state()
    if state is None:
        print("Error: NO_STATE — run init first")
        sys.exit(1)

    step_name = None
    artifact_path = None
    content_type = None
    summary = ""
    quality_score = None
    retention = "keep"

    valid_types = ("search_result", "gathered_content", "draft_output", "chart", "data", "other")
    valid_retention = ("keep", "transient")

    i = 0
    while i < len(args):
        if args[i] == "--step" and i + 1 < len(args):
            step_name = args[i + 1]; i += 2
        elif args[i] == "--path" and i + 1 < len(args):
            artifact_path = args[i + 1]; i += 2
        elif args[i] == "--type" and i + 1 < len(args):
            content_type = args[i + 1]; i += 2
        elif args[i] == "--summary" and i + 1 < len(args):
            summary = args[i + 1][:100]; i += 2
        elif args[i] == "--score" and i + 1 < len(args):
            try:
                quality_score = max(0, min(100, int(args[i + 1])))
            except ValueError:
                pass
            i += 2
        elif args[i] == "--retention" and i + 1 < len(args):
            retention = args[i + 1]; i += 2
        else:
            i += 1

    if not step_name:
        print("Error: --step is required"); sys.exit(1)
    if not artifact_path:
        print("Error: --path is required"); sys.exit(1)
    if content_type not in valid_types:
        print(f"Error: --type must be one of {valid_types}"); sys.exit(1)
    if retention not in valid_retention:
        retention = "keep"

    artifact = {
        "path": artifact_path,
        "source_step": step_name,
        "content_type": content_type,
        "summary": summary,
        "quality_score": quality_score,
        "retention": retention,
        "registered_at": datetime.now().isoformat(),
    }

    # Find or create the step entry
    steps = state.get("step_states", [])
    found = False
    for step in steps:
        if step["name"] == step_name:
            step.setdefault("artifacts", [])
            step["artifacts"].append(artifact)
            found = True
            break

    if not found:
        steps.append({
            "name": step_name,
            "status": "in_progress",
            "started_at": datetime.now().isoformat(),
            "completed_at": None,
            "artifacts": [artifact],
        })
        state["step_states"] = steps

    state["updated_at"] = datetime.now().isoformat()
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"ARTIFACT_REGISTERED: {artifact_path} → step={step_name}, type={content_type}, retention={retention}")


def cmd_list_artifacts(args: list):
    """List artifacts from the state file.
    Usage: save_state.py list-artifacts [--step <name>] [--type <type>]
    Returns JSON array of matching artifacts.
    """
    state = load_state()
    if state is None:
        print(json.dumps([], ensure_ascii=False))
        return

    filter_step = None
    filter_type = None

    i = 0
    while i < len(args):
        if args[i] == "--step" and i + 1 < len(args):
            filter_step = args[i + 1]; i += 2
        elif args[i] == "--type" and i + 1 < len(args):
            filter_type = args[i + 1]; i += 2
        else:
            i += 1

    all_artifacts = []
    for step in state.get("step_states", []):
        for art in step.get("artifacts", []):
            if filter_step and art.get("source_step") != filter_step:
                continue
            if filter_type and art.get("content_type") != filter_type:
                continue
            all_artifacts.append(art)

    print(json.dumps(all_artifacts, indent=2, ensure_ascii=False))


def cmd_read_context(args: list):
    """Read full context for a step: requirements + relevant artifacts + step summaries + audit test cases.
    Usage: save_state.py read-context <step_name>
    Returns JSON object for pipeline consumption.
    """
    state = load_state()
    if state is None:
        print(json.dumps({"error": "NO_STATE"}, ensure_ascii=False))
        sys.exit(1)

    step_name = args[0] if args else None
    if not step_name:
        print("Error: step name is required")
        sys.exit(1)

    # Collect all artifacts from all steps (for cross-step reference)
    all_artifacts = []
    for step in state.get("step_states", []):
        for art in step.get("artifacts", []):
            all_artifacts.append(art)

    # Filter relevant artifacts: keep-retention with quality_score >= 60, or all from prior steps
    relevant = [a for a in all_artifacts if a.get("retention") == "keep"]

    # Collect previous step summaries
    step_summaries = []
    for step in state.get("step_states", []):
        if step["name"] == step_name:
            break
        step_summaries.append({
            "name": step["name"],
            "status": step.get("status"),
            "output_summary": step.get("output_summary", ""),
            "artifact_count": len(step.get("artifacts", [])),
        })

    context = {
        "step_name": step_name,
        "structured_requirements": state.get("structured_requirements", {}),
        "relevant_artifacts": relevant,
        "previous_step_summaries": step_summaries,
        "audit_test_cases": state.get("audit_test_cases", []),
        "raw_prompt": state.get("raw_prompt", ""),
        "intent_classification": state.get("intent_classification", ""),
    }

    print(json.dumps(context, indent=2, ensure_ascii=False))


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
        print("Usage: save_state.py <init|extract-requirements|check|save|resume-plan|update|set-mode|complete|archive|register-artifact|list-artifacts|read-context> [data]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "init":
        if len(sys.argv) < 3:
            print("Error: init requires a prompt argument")
            sys.exit(1)
        intent = sys.argv[3] if len(sys.argv) >= 4 else "unknown"
        cmd_init(sys.argv[2], intent)
    elif command == "extract-requirements":
        reqs_json = sys.argv[2] if len(sys.argv) >= 3 else None
        cmd_extract_requirements(reqs_json)
    elif command == "set-mode":
        if len(sys.argv) < 3:
            print("Error: set-mode requires guided|standard|silent")
            sys.exit(1)
        cmd_set_mode(sys.argv[2])
    elif command == "check-requirements":
        state = load_state()
        if state is None:
            print("NO_STATE")
            sys.exit(1)
        reqs = state.get("structured_requirements", {})
        if not reqs:
            print("NO_REQUIREMENTS — run extract-requirements first")
        else:
            print(json.dumps(reqs, indent=2, ensure_ascii=False))
    elif command == "child-workflow":
        # child-workflow <subcommand> --step-id <id> [--plan <json>] [--step-name <n>] [--status <s>]
        subcmd = sys.argv[2] if len(sys.argv) >= 3 else None
        args_rest = sys.argv[3:]
        if subcmd == "init":
            # init --step-id <id> --plan <json>
            step_id, plan_json = None, None
            i = 0
            while i < len(args_rest):
                if args_rest[i] == "--step-id" and i + 1 < len(args_rest):
                    step_id = args_rest[i + 1]; i += 2
                elif args_rest[i] == "--plan" and i + 1 < len(args_rest):
                    plan_json = args_rest[i + 1]; i += 2
                else:
                    i += 1
            if not step_id:
                print("Error: --step-id required"); sys.exit(1)
            state = load_state()
            if state is None:
                print("Error: NO_STATE"); sys.exit(1)
            child_workflows = state.get("child_workflows", {})
            child_workflows[step_id] = {
                "plan": json.loads(plan_json) if plan_json else {},
                "step_states": [],
                "status": "IN_PROGRESS",
                "started_at": datetime.now().isoformat(),
            }
            state["child_workflows"] = child_workflows
            state["updated_at"] = datetime.now().isoformat()
            STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"CHILD_WORKFLOW_INIT: {step_id}")
        elif subcmd == "update":
            # update --step-id <id> --step-name <n> --status <s> [--audit-score <score>]
            step_id, step_name, step_status = None, None, "completed"
            audit_score = None
            i = 0
            while i < len(args_rest):
                if args_rest[i] == "--step-id" and i + 1 < len(args_rest):
                    step_id = args_rest[i + 1]; i += 2
                elif args_rest[i] == "--step-name" and i + 1 < len(args_rest):
                    step_name = args_rest[i + 1]; i += 2
                elif args_rest[i] == "--status" and i + 1 < len(args_rest):
                    step_status = args_rest[i + 1]; i += 2
                elif args_rest[i] == "--audit-score" and i + 1 < len(args_rest):
                    try:
                        audit_score = int(args_rest[i + 1])
                    except ValueError:
                        pass
                    i += 2
                else:
                    i += 1
            if not step_id or not step_name:
                print("Error: --step-id and --step-name required"); sys.exit(1)
            state = load_state()
            if state is None:
                print("Error: NO_STATE"); sys.exit(1)
            child_workflows = state.get("child_workflows", {})
            if step_id not in child_workflows:
                print(f"Error: child workflow {step_id} not found — call init first"); sys.exit(1)
            wf = child_workflows[step_id]
            steps = wf.get("step_states", [])
            found = False
            for step in steps:
                if step["name"] == step_name:
                    step["status"] = step_status
                    if audit_score is not None:
                        step["audit_score"] = audit_score
                    if step_status == "completed":
                        step["completed_at"] = datetime.now().isoformat()
                    found = True; break
            if not found:
                new_step = {"name": step_name, "status": step_status,
                            "started_at": datetime.now().isoformat() if step_status == "in_progress" else None,
                            "completed_at": datetime.now().isoformat() if step_status == "completed" else None}
                if audit_score is not None:
                    new_step["audit_score"] = audit_score
                steps.append(new_step)
            wf["step_states"] = steps
            state["child_workflows"] = child_workflows
            state["updated_at"] = datetime.now().isoformat()
            STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"CHILD_STEP_UPDATED: {step_id}/{step_name} → {step_status}")
        elif subcmd == "complete":
            # complete --step-id <id> [--status completed|failed]
            step_id, final_status = None, "completed"
            i = 0
            while i < len(args_rest):
                if args_rest[i] == "--step-id" and i + 1 < len(args_rest):
                    step_id = args_rest[i + 1]; i += 2
                elif args_rest[i] == "--status" and i + 1 < len(args_rest):
                    final_status = args_rest[i + 1]; i += 2
                else:
                    i += 1
            if not step_id:
                print("Error: --step-id required"); sys.exit(1)
            state = load_state()
            if state is None:
                print("Error: NO_STATE"); sys.exit(1)
            child_workflows = state.get("child_workflows", {})
            if step_id in child_workflows:
                wf = child_workflows[step_id]
                # Auto-detect status from step_states if not specified
                steps = wf.get("step_states", [])
                failed = [s for s in steps if s.get("status") == "failed"]
                succeeded = [s for s in steps if s.get("status") == "completed"]
                if final_status == "completed" and len(failed) > 0 and len(succeeded) == 0:
                    final_status = "failed"
                elif final_status == "completed" and len(failed) > 0:
                    final_status = "partial"
                wf["status"] = final_status
                wf["completed_at"] = datetime.now().isoformat()
                wf["failed_steps"] = [s["name"] for s in failed]
                wf["succeeded_steps"] = [s["name"] for s in succeeded]
                state["child_workflows"] = child_workflows
                state["updated_at"] = datetime.now().isoformat()
                STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
                if failed:
                    print(f"CHILD_WORKFLOW_COMPLETE: {step_id} → {final_status} ({len(succeeded)} ok, {len(failed)} failed: {[s['name'] for s in failed]})")
                else:
                    print(f"CHILD_WORKFLOW_COMPLETE: {step_id} → {final_status}")
            else:
                print(f"Error: child workflow {step_id} not found"); sys.exit(1)
        elif subcmd == "check":
            # check [--step-id <id>]
            step_id = None
            i = 0
            while i < len(args_rest):
                if args_rest[i] == "--step-id" and i + 1 < len(args_rest):
                    step_id = args_rest[i + 1]; i += 2
                else:
                    i += 1
            state = load_state()
            if state is None:
                print("NO_STATE"); sys.exit(1)
            child_workflows = state.get("child_workflows", {})
            if step_id:
                print(json.dumps(child_workflows.get(step_id, {}), indent=2, ensure_ascii=False))
            else:
                print(json.dumps(child_workflows, indent=2, ensure_ascii=False))
        elif subcmd == "list-failed":
            # list-failed [--step-id <id>]  → prints failed child step names
            step_id = None
            i = 0
            while i < len(args_rest):
                if args_rest[i] == "--step-id" and i + 1 < len(args_rest):
                    step_id = args_rest[i + 1]; i += 2
                else:
                    i += 1
            state = load_state()
            if state is None:
                print("NO_STATE"); sys.exit(1)
            child_workflows = state.get("child_workflows", {})
            if step_id:
                wf = child_workflows.get(step_id, {})
                failed = wf.get("failed_steps", [])
                print(json.dumps(failed, ensure_ascii=False))
            else:
                # List all failed steps across all child workflows
                all_failed = {}
                for wf_id, wf in child_workflows.items():
                    if wf.get("failed_steps"):
                        all_failed[wf_id] = wf["failed_steps"]
                print(json.dumps(all_failed, indent=2, ensure_ascii=False))
        else:
            print(f"Error: unknown child-workflow subcommand: {subcmd}")
            print("Usage: child-workflow <init|update|complete|check> --step-id <id> ...")
            sys.exit(1)
    elif command == "check":
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
    elif command == "log-emission":
        cmd_log_emission(sys.argv[2:])
    elif command == "register-artifact":
        cmd_register_artifact(sys.argv[2:])
    elif command == "list-artifacts":
        cmd_list_artifacts(sys.argv[2:])
    elif command == "read-context":
        cmd_read_context(sys.argv[2:])
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
