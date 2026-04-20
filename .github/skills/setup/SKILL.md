---
name: setup
description: |
  Setup and install all InsightEngine dependencies. Runs check_deps.py first, installs only
  missing packages. Creates utility scripts (recalc.py, save_state.py) if not present.
  Always use this skill when the user gets an import error, ModuleNotFoundError, or says the tool
  isn't working — even casual requests like "bị lỗi import", "thư viện chưa cài", "lần đầu chạy",
  "không chạy được", "cài lại đi", or "setup môi trường" — even without saying "setup".
argument-hint: "[none]"
version: 1.2
compatibility:
  requires:
    - Python >= 3.10
    - pip3
  optional:
    - Node.js >= 18 (for pptxgenjs quick mode)
    - npm (for pptxgenjs)
    - Playwright Chromium (for bot-protected URL fetching)
---

# Cài đặt — InsightEngine Setup Skill

**Governance:** Read and follow `.github/RULE.md` — it overrides all instructions below.

Guides the user through installing all dependencies needed by InsightEngine. The approach is
conservative: check what's missing first (via `check_deps.py`), then install only what's
needed. This avoids unnecessary reinstalls and respects the user's existing environment.

All responses to the user are in Vietnamese. Always confirm before installing.

---

---

## Execution Steps

### Step 1: Pull latest code from git

Before checking or installing anything, pull the latest version of the repo. Skills,
scripts, and requirements.txt may have been updated — installing against an outdated
codebase leads to missing dependencies or stale scripts.

```bash
# Pull from the InsightEngine project root (auto-detected)
cd "$(git rev-parse --show-toplevel)" && git pull
```

Report the result:
- If up to date: "✅ Code đã là phiên bản mới nhất."
- If updated: "🔄 Đã cập nhật code. Đang kiểm tra dependencies..."
- If git pull fails (no internet, merge conflict, etc.): warn and continue anyway —
  dependency check and install should still proceed with current local code.

### Step 2: Check current state
Run `python3 scripts/check_deps.py` and parse the output to identify which packages are
missing vs already installed.

### Step 3: Report findings
Show the user what's installed and what's needed:
```
📋 Kết quả kiểm tra môi trường InsightEngine:
- ✅ Đã có: [list present]
- ❌ Cần cài: [list missing]
```

### Step 4: Install Python packages
Install only the packages that `check_deps.py` reported as missing. Use the pinned versions
from `requirements.txt` when available to ensure reproducible builds:
```bash
pip3 install --user -r requirements.txt
```
Or install individual missing packages:
```bash
pip3 install --user <missing-packages>
```

Core packages: `markitdown[all]`, `python-docx`, `openpyxl`, `pandas`, `reportlab`, `pypdf`,
`pdfplumber`, `matplotlib`, `seaborn`, `jinja2`, `httpx`, `beautifulsoup4`, `playwright`

### Step 5: Install Playwright browser
After installing the playwright Python package, install the Chromium browser binary:
```bash
python3 -m playwright install chromium
```
This is needed by gather's Tier 3 stealth fetch mode for bot-protected websites.
The browser binary is ~150 MB and cached at `~/.cache/ms-playwright/`.
If this step fails (e.g., no disk space), warn but continue — Tier 1 and Tier 2 URL
fetching still work without Playwright.

### Step 6: Install Node.js packages
If pptxgenjs is missing: `npm install -g pptxgenjs`

### Step 7: Create utility scripts
If `scripts/recalc.py` doesn't exist, create it (needed by gen-excel for formula recalculation).

### Step 8: Verify
Run `python3 scripts/check_deps.py` again to confirm everything is installed. Expected:
exit code 0, all items show ✅.

### Step 9: Final report
```
✅ Cài đặt hoàn tất! InsightEngine sẵn sàng sử dụng.
Gõ synthesize để bắt đầu tổng hợp nội dung.
```
On failure: list which packages failed and suggest manual install commands.

---

## Python Version Handling

InsightEngine requires Python ≥ 3.10. If the user's Python is older, warn them in Vietnamese:
"⚠️ Python hiện tại là {version}. InsightEngine cần Python ≥ 3.10. Hãy cài Python mới hơn:
brew install python@3.12"

Do not auto-install Python — it affects the system and requires user judgment.

---

## Optional Dependencies (Apple Silicon)

Only suggest these if the user asks for image generation (gen-image AI mode), or explicitly
requests optional packages:
```bash
pip3 install --user torch diffusers transformers accelerate
```
These are large (~2GB download) and only needed for AI image generation on Apple Silicon.

---

## recalc.py Specification

Forces Excel formula recalculation after openpyxl writes formulas. Without this, formulas
show as `0` until the user manually recalculates in Excel.

Usage: `python3 scripts/recalc.py <file.xlsx>`

Method: opens workbook with `data_only=False`, iterates all sheets, touches formula cells
to mark them dirty, then saves. Full recalc happens when the user opens the file in
Excel/LibreOffice.

Created during `setup` setup or the first time gen-excel runs.

---

## Troubleshooting

For detailed troubleshooting of common installation errors (permissions, version conflicts,
font issues, Apple Silicon problems), see `references/troubleshooting.md`.

---

## Examples

**Example 1 — Fresh install:**
Input: User runs setup for the first time
Output: check_deps.py → 12 missing packages → pip install → npm install pptxgenjs → all ✅

**Example 2 — Partial install:**
Input: User gets "ModuleNotFoundError: No module named 'reportlab'"
Output: check_deps.py → 2 missing (reportlab, pypdf) → pip install only those 2 → ✅

**Example 3 — Optional AI packages:**
Input: User says "tôi muốn tạo ảnh AI" but torch not installed
Output: Confirm with user → pip install torch diffusers transformers accelerate (~2GB) → ✅

---

## What This Skill Does NOT Do

- Does NOT auto-install Python runtime (only packages)
- Does NOT modify system PATH
- Does NOT install packages globally (uses --user flag)
- Does NOT install optional Apple Silicon deps unless asked
- Does NOT proceed silently — always reports to user in Vietnamese

---

## Optional: RULE-12 Pre-Commit Hook

To prevent one-time scripts from being committed to `/scripts/`:

```bash
# Create the hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/sh
python3 scripts/check_no_onetime_in_scripts.py
EOF
chmod +x .git/hooks/pre-commit
```

This runs `scripts/check_no_onetime_in_scripts.py` on every `git commit`, blocking commits that include one-time scripts in `/scripts/` (RULE-12 enforcement).
