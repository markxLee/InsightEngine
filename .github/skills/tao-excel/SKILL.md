---
name: tao-excel
description: |
  Create professional Excel (.xlsx) files with data, formulas, and formatting.
  Uses openpyxl for formatting/formulas, pandas for data operations.
  Runs scripts/recalc.py after generation to force formula recalculation.
  Always use this skill when the user needs a spreadsheet, table with calculations, or data export
  — even casual requests like "làm cái bảng tính", "tạo file excel", "xuất ra bảng", "tính toán
  và lưu thành file", or "cho tôi bảng so sánh" where tabular data with formulas fits, even
  without saying "/tao-excel" or ".xlsx".
argument-hint: "[data from bien-soan or direct input] [output path]"
version: 1.1
---

# Tạo Excel — Excel Spreadsheet Output Skill

Generates professionally formatted `.xlsx` files with working formulas and color-coded cells.
See `references/formatting-conventions.md` for column width standards, color codes, and cell format patterns.

This skill uses openpyxl for formatting and formulas, and pandas for data operations. The
most important rule: never hardcode calculated values — always use Excel formulas. This
ensures the spreadsheet stays interactive so users can modify input data and see results
update automatically.

All responses to the user are in Vietnamese.

---

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

1. Check openpyxl: `python3 -c "import openpyxl"` → if fail: "Chạy: pip install --user openpyxl"
2. Check pandas: `python3 -c "import pandas"` → if fail: "Chạy: pip install --user pandas"
3. Confirm recalc.py exists at `scripts/recalc.py` → if missing: create from template
4. Confirm data available from pipeline or ask user

---

## Step 1: Analyze Data Structure

Before generating, understand what the spreadsheet needs:
- How many sheets? What are column headers and data types?
- Which values should be formulas vs static data?
- Summary rows/columns needed (SUM, AVERAGE, COUNT)?
- Cross-sheet references if multi-sheet?

Data can come from: Markdown tables (bien-soan output), CSV/TSV files, user-described
structure, or numbers extracted from synthesized text.

Present the plan to user (interactive mode):
```
📊 Kế hoạch tạo Excel:
- Số sheet: {N}
- Sheet 1: {name} — {rows} hàng × {cols} cột
- Công thức: {formula_count} ô tính toán
- Định dạng: {format_description}

Bạn muốn điều chỉnh gì không?
```
Pipeline mode: auto-approve, proceed immediately.

---

## Step 2: Generate Excel via CLI Script

Use the bundled CLI script as the primary generation method. Prepare data as JSON, save to
a tmp file, then run the script. This approach is preferred over writing ephemeral scripts
because gen_xlsx.py already handles styles, formulas, formatting, and edge cases.

```bash
python3 .github/skills/tao-excel/scripts/gen_xlsx.py --input data.json --output output.xlsx --style corporate
```

For complex cases that go beyond what gen_xlsx.py supports (e.g., conditional formatting,
data validation dropdowns, or pivot-table-like structures), extend the script or write a
focused helper — but still use openpyxl directly, not pandas to_excel (which lacks
formatting control).

---

## Step 3: Apply Formatting Rules

Color coding helps users understand which cells they can edit vs which are calculated:
- **Blue font** (`0000FF`) — input cells (user-editable raw data)
- **Black font** (`000000`) — formula cells (calculated, don't edit manually)
- **Green font** (`008000`) — cross-sheet references (data from another sheet)
- **Headers** — bold, light gray background, centered

Number formats: currency `#,##0`, percentage `0.0%`, date `YYYY-MM-DD`, decimal `#,##0.00`

Layout: freeze panes at A2 (header row visible while scrolling), auto-filter enabled,
column widths auto-fit (min 10, max 40), page setup A4 landscape for wide tables.

---

## Step 4: Formula Rules

The single most important rule for Excel generation: **never hardcode calculated values.**
When a cell should show a sum, average, or any derived value, write an Excel formula instead
of computing the number in Python and writing the result. This matters because users will
edit input data after receiving the file — hardcoded values won't update, but formulas will.

Common formula patterns:
- Sum: `=SUM(B2:B10)` | Average: `=AVERAGE(C2:C10)` | Count: `=COUNTA(A2:A100)`
- Percentage: `=B2/B$11` | Conditional: `=IF(C2>100,"Cao","Thấp")`
- Cross-sheet: `=VLOOKUP(A2,Sheet2!A:B,2,FALSE)` or `=Sheet2!B5`

After saving, always run recalc to mark formulas as needing recalculation:
```bash
python3 scripts/recalc.py "{output_path}"
```
Then verify no formula errors (#REF!, #DIV/0!, #NAME?, #VALUE!) in the output.

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
