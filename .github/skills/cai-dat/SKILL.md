---
name: cai-dat
description: |
  Setup and install all InsightEngine dependencies. Runs check_deps.py first, installs only
  missing packages. Creates utility scripts (recalc.py, save_state.py) if not present.
  Always use this skill when the user gets an import error, ModuleNotFoundError, or says the tool
  isn't working — even casual requests like "bị lỗi import", "thư viện chưa cài", "lần đầu chạy",
  "không chạy được", "cài lại đi", or "setup môi trường" — even without saying "/cai-dat".
argument-hint: "[none]"
version: 1.1
---

# Cài đặt — InsightEngine Setup Skill

Guides the user through installing all dependencies needed by InsightEngine. The approach is
conservative: check what's missing first (via `check_deps.py`), then install only what's
needed. This avoids unnecessary reinstalls and respects the user's existing environment.

All responses to the user are in Vietnamese. Always confirm before installing.

---

---

## Execution Steps

### Step 1: Check current state
Run `python3 scripts/check_deps.py` and parse the output to identify which packages are
missing vs already installed.

### Step 2: Report findings
Show the user what's installed and what's needed:
```
📋 Kết quả kiểm tra môi trường InsightEngine:
- ✅ Đã có: [list present]
- ❌ Cần cài: [list missing]
```

### Step 3: Install Python packages
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
`pdfplumber`, `matplotlib`, `seaborn`, `jinja2`, `httpx`, `beautifulsoup4`

### Step 4: Install Node.js packages
If pptxgenjs is missing: `npm install -g pptxgenjs`

### Step 5: Create utility scripts
If `scripts/recalc.py` doesn't exist, create it (needed by tao-excel for formula recalculation).

### Step 6: Verify
Run `python3 scripts/check_deps.py` again to confirm everything is installed. Expected:
exit code 0, all items show ✅.

### Step 7: Final report
```
✅ Cài đặt hoàn tất! InsightEngine sẵn sàng sử dụng.
Gõ /tong-hop để bắt đầu tổng hợp nội dung.
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

Only suggest these if the user asks for image generation (tao-hinh AI mode), or explicitly
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

Created during `/cai-dat` setup or the first time tao-excel runs.

---

## What This Skill Does NOT Do

- Does NOT auto-install Python runtime (only packages)
- Does NOT modify system PATH
- Does NOT install packages globally (uses --user flag)
- Does NOT install optional Apple Silicon deps unless asked
- Does NOT proceed silently — always reports to user in Vietnamese
