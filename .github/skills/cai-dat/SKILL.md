---
name: cai-dat
description: |
  Setup and install all InsightEngine dependencies. Runs check_deps.py first, installs only
  missing packages. Creates utility scripts (recalc.py, save_state.py) if not present.
  Always use this skill when the user gets an import error, ModuleNotFoundError, or says the tool
  isn't working — even casual requests like "bị lỗi import", "thư viện chưa cài", "lần đầu chạy",
  "không chạy được", "cài lại đi", or "setup môi trường" — even without saying "/cai-dat".
argument-hint: "[none]"
---

# Cài đặt — InsightEngine Setup Skill

Guides the user through installing all dependencies needed by InsightEngine.

```yaml
MODE: Interactive (user confirms before installing)
LANGUAGE: Copilot responds in Vietnamese
```

---

---

## Execution Steps

```yaml
STEPS:
  1_CHECK:
    action: Run check_deps.py to assess current state
    command: python3 scripts/check_deps.py
    parse: Read output to identify missing packages
    
  2_REPORT:
    action: Report findings to user in Vietnamese
    format: |
      📋 Kết quả kiểm tra môi trường InsightEngine:
      - ✅ Đã có: [list present]
      - ❌ Cần cài: [list missing]
      
  3_INSTALL_PYTHON:
    condition: Missing pip packages exist
    action: Install missing packages only
    command: pip3 install --user <missing-packages>
    packages_core:
      - "markitdown[all]"
      - python-docx
      - openpyxl
      - pandas
      - reportlab
      - pypdf
      - pdfplumber
      - matplotlib
      - seaborn
      - jinja2
      - httpx
      - beautifulsoup4
    note: Only install packages that check_deps.py reported as missing
    
  4_INSTALL_NODE:
    condition: pptxgenjs missing
    action: Install pptxgenjs globally
    command: npm install -g pptxgenjs
    
  5_CREATE_RECALC:
    condition: scripts/recalc.py does not exist
    action: Create the Excel recalculation script
    path: scripts/recalc.py
    
  6_VERIFY:
    action: Run check_deps.py again to verify
    command: python3 scripts/check_deps.py
    expected: Exit code 0, all ✅
    
  7_REPORT_FINAL:
    action: Report final status in Vietnamese
    format: |
      ✅ Cài đặt hoàn tất! InsightEngine sẵn sàng sử dụng.
      Gõ /tong-hop để bắt đầu tổng hợp nội dung.
    on_failure: |
      ⚠️ Một số package không cài được. Chi tiết:
      [list failed packages with error messages]
      Hãy thử cài thủ công: pip3 install --user <package>
```

---

## Python Version Handling

```yaml
PYTHON_VERSION:
  if_below_3_10:
    action: |
      Warn user in Vietnamese:
      "⚠️ Python hiện tại là {version}. InsightEngine cần Python ≥ 3.10.
       Hãy cài Python mới hơn: brew install python@3.12"
    do_not: Auto-install Python (too risky, affects system)
```

---

## Optional Dependencies (Apple Silicon)

```yaml
OPTIONAL_DEPS:
  trigger: User mentions image generation, or asks to install optional packages
  packages:
    - torch
    - diffusers
    - transformers
    - accelerate
  install: pip3 install --user torch diffusers transformers accelerate
  note: Only suggest if user asks, or if tao-hinh image generation is needed
```

---

## recalc.py Specification

```yaml
RECALC_SCRIPT:
  purpose: Force Excel formula recalculation after openpyxl writes formulas
  usage: python3 scripts/recalc.py <file.xlsx>
  method: |
    Open workbook with data_only=False, iterate all sheets,
    touch formula cells to mark dirty, save.
    Note: Full recalc requires opening in Excel/LibreOffice.
    This script marks formulas as needing recalc on next open.
  create_when: During /cai-dat setup OR first time tao-excel runs
```

---

## What This Skill Does NOT Do

- Does NOT auto-install Python runtime (only packages)
- Does NOT modify system PATH
- Does NOT install packages globally (uses --user flag)
- Does NOT install optional Apple Silicon deps unless asked
- Does NOT proceed silently — always reports to user in Vietnamese
