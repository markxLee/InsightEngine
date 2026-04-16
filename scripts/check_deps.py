#!/usr/bin/env python3
"""InsightEngine dependency checker.

Checks all required Python packages, Node.js packages,
and runtime versions needed by InsightEngine skills.

Usage:
    python3 scripts/check_deps.py          # Full output
    python3 scripts/check_deps.py --silent  # Exit code only (for pipeline pre-check)
"""

import argparse
import importlib
import shutil
import subprocess
import sys


def check_python_version(min_major=3, min_minor=10):
    v = sys.version_info
    ok = v.major >= min_major and v.minor >= min_minor
    return ok, f"Python {v.major}.{v.minor}.{v.micro}"


def check_node_version(min_major=18):
    node = shutil.which("node")
    if not node:
        return False, "Node.js not found"
    try:
        out = subprocess.check_output([node, "--version"], text=True).strip()
        major = int(out.lstrip("v").split(".")[0])
        return major >= min_major, f"Node.js {out}"
    except Exception as e:
        return False, f"Node.js error: {e}"


def check_pip_package(name):
    try:
        importlib.import_module(name)
        return True
    except ImportError:
        return False


def check_node_package(name):
    try:
        subprocess.check_output(
            ["node", "-e", f"require('{name}')"],
            stderr=subprocess.STDOUT,
            text=True,
            timeout=10,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return False


PIP_PACKAGES = {
    "markitdown": "markitdown",
    "docx (python-docx)": "docx",
    "openpyxl": "openpyxl",
    "pandas": "pandas",
    "reportlab": "reportlab",
    "pypdf": "pypdf",
    "pdfplumber": "pdfplumber",
    "matplotlib": "matplotlib",
    "seaborn": "seaborn",
    "jinja2": "jinja2",
    "httpx": "httpx",
    "beautifulsoup4": "bs4",
}

NODE_PACKAGES = ["pptxgenjs"]

OPTIONAL_PIP = {
    "torch (Apple Silicon)": "torch",
    "diffusers": "diffusers",
    "transformers": "transformers",
    "accelerate": "accelerate",
}


def main():
    parser = argparse.ArgumentParser(description="InsightEngine dependency checker")
    parser.add_argument(
        "--silent", action="store_true", help="Suppress output; exit code only"
    )
    args = parser.parse_args()

    results = []
    total = 0
    ready = 0

    # Python version
    ok, info = check_python_version()
    total += 1
    if ok:
        ready += 1
    results.append(("✅" if ok else "❌", info, "runtime"))

    # Node version
    ok, info = check_node_version()
    total += 1
    if ok:
        ready += 1
    results.append(("✅" if ok else "❌", info, "runtime"))

    # Pip packages (core)
    for label, mod in PIP_PACKAGES.items():
        ok = check_pip_package(mod)
        total += 1
        if ok:
            ready += 1
        results.append(("✅" if ok else "❌", label, "pip (core)"))

    # Node packages
    for pkg in NODE_PACKAGES:
        ok = check_node_package(pkg)
        total += 1
        if ok:
            ready += 1
        results.append(("✅" if ok else "❌", pkg, "npm"))

    # Optional packages (don't affect exit code)
    opt_results = []
    for label, mod in OPTIONAL_PIP.items():
        ok = check_pip_package(mod)
        opt_results.append(("✅" if ok else "⚠️", label, "pip (optional)"))

    if not args.silent:
        print("=" * 50)
        print("InsightEngine — Dependency Check")
        print("=" * 50)
        print()
        for icon, name, category in results:
            print(f"  {icon}  {name}  [{category}]")
        print()
        if opt_results:
            print("Optional (Apple Silicon image generation):")
            for icon, name, category in opt_results:
                print(f"  {icon}  {name}  [{category}]")
            print()
        print("-" * 50)
        print(f"  {ready}/{total} core dependencies ready")
        if ready == total:
            print("  ✅ All core dependencies present — ready to go!")
        else:
            missing = total - ready
            print(f"  ❌ {missing} missing — run /cai-dat to install")
        print()

    sys.exit(0 if ready == total else 1)


if __name__ == "__main__":
    main()
