#!/usr/bin/env python3
"""Check InsightEngine dependencies and report status.

Usage:
    python3 scripts/check_deps.py          # Check all dependencies
    python3 scripts/check_deps.py --json   # Output as JSON

Exit codes:
    0 = all required dependencies present
    1 = some dependencies missing
"""

import importlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

REQUIRED_PYTHON = [
    ("markitdown", "markitdown[all]", "File reading"),
    ("docx", "python-docx", "Word output"),
    ("openpyxl", "openpyxl", "Excel output"),
    ("pandas", "pandas", "Data operations"),
    ("reportlab", "reportlab", "PDF output"),
    ("pypdf", "pypdf", "PDF manipulation"),
    ("pdfplumber", "pdfplumber", "PDF reading"),
    ("matplotlib", "matplotlib", "Charts"),
    ("seaborn", "seaborn", "Chart styling"),
    ("jinja2", "jinja2", "HTML templating"),
    ("httpx", "httpx", "URL fetching"),
    ("bs4", "beautifulsoup4", "HTML parsing"),
    ("playwright", "playwright", "Stealth web fetch"),
]

OPTIONAL_PYTHON = [
    ("torch", "torch", "AI image generation"),
    ("diffusers", "diffusers", "Stable Diffusion"),
    ("transformers", "transformers", "Model loading"),
    ("accelerate", "accelerate", "GPU acceleration"),
]

REQUIRED_NODE = [
    ("pptxgenjs", "pptxgenjs", "PowerPoint output"),
]


def check_python_package(import_name: str) -> bool:
    try:
        importlib.import_module(import_name)
        return True
    except ImportError:
        return False


def check_node_package(package_name: str) -> bool:
    try:
        result = subprocess.run(
            ["node", "-e", f"require('{package_name}')"],
            capture_output=True,
            timeout=10,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def check_command(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def main():
    as_json = "--json" in sys.argv
    results = {"present": [], "missing": [], "optional_present": [], "optional_missing": []}

    # Check Python version
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    py_ok = sys.version_info >= (3, 10)

    if not as_json:
        print(f"🐍 Python {py_version} — {'✅' if py_ok else '❌ Cần >= 3.10'}")
        print()

    # Required Python packages
    for import_name, pip_name, purpose in REQUIRED_PYTHON:
        found = check_python_package(import_name)
        entry = {"import": import_name, "pip": pip_name, "purpose": purpose}
        if found:
            results["present"].append(entry)
        else:
            results["missing"].append(entry)
        if not as_json:
            status = "✅" if found else "❌"
            print(f"  {status} {pip_name:20s} ({purpose})")

    if not as_json:
        print()

    # Node.js packages
    node_ok = check_command("node")
    if not as_json:
        print(f"📦 Node.js — {'✅' if node_ok else '⚠️ Không tìm thấy (cần cho pptxgenjs)'}")

    if node_ok:
        for pkg_name, npm_name, purpose in REQUIRED_NODE:
            found = check_node_package(pkg_name)
            entry = {"npm": npm_name, "purpose": purpose}
            if found:
                results["present"].append(entry)
            else:
                results["missing"].append(entry)
            if not as_json:
                status = "✅" if found else "❌"
                print(f"  {status} {npm_name:20s} ({purpose})")

    if not as_json:
        print()

    # Optional packages
    for import_name, pip_name, purpose in OPTIONAL_PYTHON:
        found = check_python_package(import_name)
        entry = {"import": import_name, "pip": pip_name, "purpose": purpose}
        if found:
            results["optional_present"].append(entry)
        else:
            results["optional_missing"].append(entry)
        if not as_json:
            status = "✅" if found else "⚪"
            print(f"  {status} {pip_name:20s} ({purpose}) [optional]")

    # Playwright browser — check both Linux (~/.cache) and macOS (~/Library/Caches)
    pw_browsers_linux = Path.home() / ".cache" / "ms-playwright"
    pw_browsers_macos = Path.home() / "Library" / "Caches" / "ms-playwright"
    pw_browsers = pw_browsers_macos if pw_browsers_macos.exists() else pw_browsers_linux
    pw_ok = pw_browsers.exists() and any(pw_browsers.iterdir()) if pw_browsers.exists() else False
    if not as_json:
        print()
        print(f"🌐 Playwright Chromium — {'✅' if pw_ok else '⚠️ Chưa cài (python3 -m playwright install chromium)'}")

    # Summary
    n_missing = len(results["missing"])
    if as_json:
        results["python_version"] = py_version
        results["python_ok"] = py_ok
        results["node_ok"] = node_ok
        results["playwright_browser"] = pw_ok
        results["all_ok"] = n_missing == 0 and py_ok
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print()
        if n_missing == 0 and py_ok:
            print("✅ Tất cả dependencies đã sẵn sàng!")
        else:
            print(f"❌ Thiếu {n_missing} package(s). Chạy: pip3 install --user -r requirements.txt")

    sys.exit(0 if (n_missing == 0 and py_ok) else 1)


if __name__ == "__main__":
    main()
