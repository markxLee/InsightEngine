#!/usr/bin/env python3
"""Validate state-filesystem integrity for InsightEngine pipeline.

Compares actual tmp/ files against the artifact registry in session state,
detecting orphan files and orphan registry entries.

Usage:
    python3 scripts/validate_state_integrity.py             # Report only
    python3 scripts/validate_state_integrity.py --auto-fix  # Auto-register orphans, mark missing

Exit codes:
    0 — clean (no violations) or auto-fixed successfully
    1 — violations found and --auto-fix not set
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Set

PROJECT_ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = PROJECT_ROOT / "tmp" / ".session-state.json"
TMP_DIR = PROJECT_ROOT / "tmp"

# Files/dirs in tmp/ to exclude from orphan scanning
EXCLUDED_NAMES = {".session-state.json", "archives", ".gitkeep"}


def load_state() -> Optional[dict]:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return None
    return None


def save_state(state: dict):
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def get_registered_paths(state: dict) -> Set[str]:
    """Extract all registered artifact paths from state."""
    paths = set()
    for step in state.get("step_states", []):
        for art in step.get("artifacts", []):
            paths.add(art["path"])
    return paths


def get_filesystem_files() -> Set[str]:
    """Scan tmp/ for files, excluding session state and archives."""
    files = set()
    if not TMP_DIR.exists():
        return files
    for p in TMP_DIR.rglob("*"):
        if p.is_file():
            rel = str(p.relative_to(PROJECT_ROOT))
            # Skip excluded names
            parts = p.relative_to(TMP_DIR).parts
            if any(part in EXCLUDED_NAMES for part in parts):
                continue
            files.add(rel)
    return files


def validate(auto_fix: bool = False) -> int:
    state = load_state()
    if state is None:
        print("NO_STATE — nothing to validate")
        return 0

    registered = get_registered_paths(state)
    filesystem = get_filesystem_files()

    # Orphan files: in filesystem but not in registry
    orphan_files = filesystem - registered
    # Orphan entries: in registry but file missing
    orphan_entries = set()
    for path in registered:
        full_path = PROJECT_ROOT / path
        if not full_path.exists():
            orphan_entries.add(path)

    if not orphan_files and not orphan_entries:
        print("INTEGRITY_OK: state and filesystem are in sync")
        return 0

    violations = 0

    if orphan_files:
        print(f"\n⚠️  ORPHAN FILES ({len(orphan_files)}) — in filesystem but not in registry:")
        for f in sorted(orphan_files):
            print(f"  - {f}")
        if auto_fix:
            # Auto-register orphan files with type 'other'
            for f in sorted(orphan_files):
                # Find or create a catch-all step
                steps = state.get("step_states", [])
                catch_all = None
                for step in steps:
                    if step["name"] == "auto-registered":
                        catch_all = step
                        break
                if catch_all is None:
                    catch_all = {
                        "name": "auto-registered",
                        "status": "completed",
                        "started_at": datetime.now().isoformat(),
                        "completed_at": datetime.now().isoformat(),
                        "artifacts": [],
                    }
                    steps.append(catch_all)
                    state["step_states"] = steps
                catch_all.setdefault("artifacts", [])
                catch_all["artifacts"].append({
                    "path": f,
                    "source_step": "auto-registered",
                    "content_type": "other",
                    "summary": "auto-registered",
                    "quality_score": None,
                    "retention": "transient",
                    "registered_at": datetime.now().isoformat(),
                })
            print(f"  ✅ Auto-registered {len(orphan_files)} orphan file(s)")
        else:
            violations += len(orphan_files)

    if orphan_entries:
        print(f"\n⚠️  ORPHAN ENTRIES ({len(orphan_entries)}) — in registry but file missing:")
        for e in sorted(orphan_entries):
            print(f"  - {e}")
        if auto_fix:
            # Mark orphan entries as deleted
            for step in state.get("step_states", []):
                for art in step.get("artifacts", []):
                    if art["path"] in orphan_entries:
                        art["retention"] = "deleted"
                        art["deleted_at"] = datetime.now().isoformat()
            print(f"  ✅ Marked {len(orphan_entries)} orphan entries as deleted")
        else:
            violations += len(orphan_entries)

    if auto_fix:
        state["updated_at"] = datetime.now().isoformat()
        save_state(state)
        print("\nINTEGRITY_FIXED: all violations auto-resolved")
        return 0

    print(f"\nINTEGRITY_VIOLATIONS: {violations} issue(s) found — run with --auto-fix to resolve")
    return 1


def main():
    auto_fix = "--auto-fix" in sys.argv
    exit_code = validate(auto_fix)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
