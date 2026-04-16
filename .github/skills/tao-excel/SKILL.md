---
name: tao-excel
description: |
  Create professional Excel (.xlsx) files with data, formulas, and formatting.
  Uses openpyxl for formatting/formulas, pandas for data operations.
  Runs scripts/recalc.py after generation to force recalculation.
  Use when user says "tạo file excel", "xuất excel", or "/tao-excel".
argument-hint: "[data from bien-soan or direct input] [output path]"
---

# Tạo Excel — Excel Spreadsheet Output Skill

Generates professionally formatted `.xlsx` files with working formulas and color-coded cells.

```yaml
MODE: Interactive (asks for data structure) or Pipeline (from tong-hop)
LANGUAGE: Copilot responds in Vietnamese
INPUT: Structured data from bien-soan, tables, or user-provided data
OUTPUT: .xlsx file saved to user-specified path
LIBRARIES: openpyxl (formatting/formulas), pandas (data operations)
```

---

## Trigger Conditions

Use this skill when user:
- Says "tạo file excel", "xuất excel", "tạo bảng tính", "tạo file .xlsx"
- Says "create excel", "export to excel", "export spreadsheet"
- Uses command `/tao-excel`
- Pipeline (tong-hop) routes data here for Excel output

---

## Script Architecture (US-4.3.3)

```yaml
CLI_SCRIPT:
  path: scripts/gen_xlsx.py
  purpose: Reusable CLI tool for generating .xlsx from JSON data
  usage: |
    python3 scripts/gen_xlsx.py --input data.json --output report.xlsx --style corporate
  
  args:
    --input: Path to JSON file with data (required)
    --output: Output .xlsx file path (required)
    --style: corporate | academic | minimal (default: corporate)
  
  json_format: |
    {
      "title": "Sheet Title",
      "headers": ["Col1", "Col2", "Col3"],
      "rows": [["a", 100, 200], ["b", 150, 250]],
      "formulas": {"D3": "=SUM(B3:C3)"},
      "column_widths": {"A": 20, "B": 15}
    }
    # Multi-sheet: wrap in {"sheets": [{...}, {...}]}
  
  output: Prints "✅ Saved: <path> (<size> KB, <N> sheet(s), style: <style>)"

COPILOT_WORKFLOW:
  1. Prepare data as JSON (from bien-soan output or user data)
  2. Save JSON to tmp file
  3. Run: python3 .github/skills/tao-excel/scripts/gen_xlsx.py --input data.json --output output.xlsx --style <style>
  4. Run recalc.py if formulas used
  5. Report file path + size
```

---

## Pre-Flight Check

```yaml
PRE_FLIGHT:
  1. Check openpyxl installed:
     command: python3 -c "import openpyxl" 2>&1
     if_fail: "Chạy: pip install --user openpyxl"
     
  2. Check pandas installed:
     command: python3 -c "import pandas" 2>&1
     if_fail: "Chạy: pip install --user pandas"
     
  3. Check recalc.py exists:
     path: scripts/recalc.py
     if_missing: Create from template (see Script Pattern)
     
  4. Check data available:
     - From pipeline: structured data from bien-soan
     - From user: raw data, CSV, or description
     if_missing: Ask user for data or redirect to thu-thap
```

---

## Step 1: Analyze Data Structure

```yaml
ANALYZE_DATA:
  determine:
    - Number of sheets needed
    - Column headers and data types
    - Which values should be formulas vs static data
    - Summary rows/columns needed (SUM, AVERAGE, COUNT)
    - Cross-sheet references if multi-sheet
    
  data_sources:
    - Markdown tables from bien-soan
    - CSV/TSV data
    - User-described structure
    - Numbers extracted from synthesized text
    
  present_plan:
    format: |
      📊 Kế hoạch tạo Excel:
      - Số sheet: {N}
      - Sheet 1: {name} — {rows} hàng × {cols} cột
      - Công thức: {formula_count} ô tính toán
      - Định dạng: {format_description}
      
      Bạn muốn điều chỉnh gì không?
    pipeline_mode: Auto-approve, proceed immediately
```

---

## Step 2: Generate Excel Script

```yaml
GENERATE_SCRIPT:
  approach: |
    Copilot generates an ephemeral Python script that:
    1. Creates workbook with openpyxl
    2. Adds data and formulas
    3. Applies formatting
    4. Saves to output path
    
  script_structure: |
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "{sheet_name}"
    
    # --- Column widths ---
    # --- Headers with formatting ---
    # --- Data rows ---
    # --- Formula rows (NEVER hardcode calculated values) ---
    # --- Conditional formatting ---
    # --- Save ---
    wb.save("{output_path}")
```

---

## Step 3: Apply Formatting Rules

```yaml
FORMATTING:
  color_coding:
    inputs: 
      font_color: "0000FF"     # Blue — user-editable input cells
      description: Cells containing raw data that users may modify
    formulas:
      font_color: "000000"     # Black — formula/calculated cells
      description: Cells with Excel formulas (SUM, AVERAGE, etc.)
    cross_sheet:
      font_color: "008000"     # Green — cross-sheet references
      description: Cells referencing other sheets
    headers:
      font: Bold
      fill: Light gray background
      alignment: Center
      
  number_formats:
    currency: '#,##0'
    percentage: '0.0%'
    date: 'YYYY-MM-DD'
    decimal: '#,##0.00'
    integer: '#,##0'
    
  layout:
    freeze_panes: "A2"        # Freeze header row
    auto_filter: true          # Enable filter on header row
    column_width: Auto-fit based on content (min 10, max 40)
    row_height: Default 15, header 20
    
  page_setup:
    orientation: landscape     # For wide tables
    paper_size: A4
    fit_to_page: true
```

---

## Step 4: Formula Rules

```yaml
FORMULA_RULES:
  CRITICAL: |
    NEVER hardcode calculated values. ALWAYS use Excel formulas.
    This ensures the spreadsheet remains interactive and recalculates
    when users modify input data.
    
  examples:
    sum: "=SUM(B2:B10)"
    average: "=AVERAGE(C2:C10)"
    count: "=COUNTA(A2:A100)"
    percentage: "=B2/B$11"
    if_condition: '=IF(C2>100,"Cao","Thấp")'
    vlookup: "=VLOOKUP(A2,Sheet2!A:B,2,FALSE)"
    cross_sheet: "=Sheet2!B5"
    
  validation:
    after_save:
      1. Run scripts/recalc.py to force recalculation
      2. Reopen and check for formula errors
      3. Verify no #REF!, #DIV/0!, #NAME?, #VALUE! errors
      
  recalc_command: |
    python3 scripts/recalc.py "{output_path}"
```

---

## Step 5: Save & Verify

```yaml
SAVE_AND_VERIFY:
  1_SAVE:
    command: wb.save("{output_path}")
    
  2_RECALC:
    command: python3 scripts/recalc.py "{output_path}"
    purpose: Force Excel to recalculate all formulas on next open
    
  3_VERIFY:
    script: |
      wb = openpyxl.load_workbook("{output_path}")
      for ws in wb.worksheets:
        for row in ws.iter_rows():
          for cell in row:
            if isinstance(cell.value, str) and cell.value.startswith("="):
              # Check formula is valid syntax
              pass
      print(f"✅ {ws.title}: {ws.max_row} rows × {ws.max_column} cols")
    
  4_REPORT:
    format: |
      ✅ File Excel đã tạo:
      - Đường dẫn: {output_path}
      - Kích thước: {file_size}
      - Số sheet: {sheet_count}
      - Tổng hàng: {total_rows}
      - Công thức: {formula_count} ô
      - Màu sắc: 🔵 inputs, ⚫ formulas, 🟢 cross-sheet
```

---

## Error Handling

```yaml
ERRORS:
  formula_error:
    detect: "#REF!", "#DIV/0!", "#NAME?", "#VALUE!"
    action: |
      1. Identify the problematic cell(s)
      2. Fix formula reference
      3. Re-save and re-verify
    message: "⚠️ Lỗi công thức tại {cell}: {error}. Đang sửa..."
    
  data_type_error:
    detect: Non-numeric data in formula range
    action: Clean data or adjust formula range
    
  file_permission:
    detect: PermissionError on save
    action: Try alternative path or ask user to close file
    message: "❌ Không thể ghi file. File có đang mở không?"
    
  missing_recalc:
    detect: scripts/recalc.py not found
    action: Create recalc.py with standard content
```

---

## What This Skill Does NOT Do

- Does NOT read/parse existing Excel files — that's thu-thap's job
- Does NOT create charts from data — that's tao-hinh's job
- Does NOT synthesize content — that's bien-soan's job
- Does NOT install dependencies — redirects to /cai-dat
