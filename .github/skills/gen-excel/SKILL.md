---
name: gen-excel
description: |
  Create professional Excel (.xlsx) files with data, formulas, and formatting.
  Uses openpyxl for formatting/formulas, pandas for data operations.
  Runs scripts/recalc.py after generation to force formula recalculation.
  Always use this skill when the user needs a spreadsheet, table with calculations, or data export
  — even casual requests like "làm cái bảng tính", "tạo file excel", "xuất ra bảng", "tính toán
  và lưu thành file", or "cho tôi bảng so sánh" where tabular data with formulas fits, even
  without saying "gen-excel" or ".xlsx".
argument-hint: "[data from bien-soan or direct input] [output path]"
version: 1.1
compatibility:
  requires:
    - Python >= 3.10
    - openpyxl >= 3.1.0
    - pandas >= 2.2.0
  tools:
    - run_in_terminal
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
  3. Run: python3 .github/skills/gen-excel/scripts/gen_xlsx.py --input data.json --output output.xlsx --style <style>
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

### Data Intelligence — Think Before You Build

Don't just dump data into cells. Analyze the data to make the spreadsheet genuinely useful.
A well-designed spreadsheet anticipates what questions the user will ask and provides the
formulas and formatting to answer them immediately.

**1. Suggest derived columns the user didn't ask for (but will want):**

| Data pattern | Derived column suggestion | Formula example |
|---|---|---|
| Revenue + Cost columns | Profit, Profit Margin % | `=Revenue-Cost`, `=Profit/Revenue` |
| Monthly data over time | YoY Change %, MoM Change % | `=(B3-B2)/B2` |
| Categories with values | Rank, % of Total | `=RANK(B2,B$2:B$20)`, `=B2/SUM(B$2:B$20)` |
| Dates + Status | Days elapsed, Overdue flag | `=TODAY()-A2`, `=IF(D2>deadline,"Quá hạn","OK")` |
| Scores/ratings | Average, Min, Max, Std Dev | Summary row with aggregate formulas |
| Multiple items with prices | Subtotal, Tax, Grand Total | `=SUMPRODUCT(qty,price)` |

When suggesting, explain briefly: "Tôi đã thêm cột Profit Margin (%) vì khi có Revenue và Cost,
đây là chỉ số phân tích quan trọng nhất."

**2. Smart conditional formatting suggestions:**

Conditional formatting transforms a wall of numbers into actionable intelligence:
- **Data bars**: for columns where relative magnitude matters (revenue, scores)
- **Color scales** (green→red): for performance metrics (high=good=green, low=bad=red)
- **Icon sets**: for status indicators (✓/⚠/✗)
- **Top/Bottom N**: highlight top 3 and bottom 3 values in key columns
- **Threshold rules**: if there's a target/budget, color cells that exceed or fall short

Apply the most relevant 2-3 rules — don't over-format. The goal is to make the most
important patterns jump out visually.

**3. Dashboard/summary sheet (when data is complex):**

If the spreadsheet has 50+ rows or multiple data dimensions, add a Summary sheet as the
first sheet. This sheet should contain:
- Key metrics as large, prominent cells (total revenue, average score, etc.)
- A mini-table with top/bottom performers
- Formula references to detailed data sheets (so it auto-updates)

Think of it as an executive dashboard — someone should be able to open the file, see the
Summary sheet, and understand the key story without scrolling through data.

**4. Flag potential chart candidates:**

After analyzing the data, note which data would benefit from visualization. Report to the
pipeline (or user): "Dữ liệu này phù hợp để tạo biểu đồ {type} — bạn muốn tạo biểu đồ
không?" This helps tong-hop decide whether to chain tao-hinh.

Present the enhanced plan to user (interactive mode):
```
📊 Kế hoạch tạo Excel:
- Số sheet: {N} (bao gồm {summary_if_applicable})
- Sheet 1: {name} — {rows} hàng × {cols} cột
- Công thức: {formula_count} ô tính toán
- Cột bổ sung đề xuất: {derived_columns}
- Conditional formatting: {formatting_rules}
- Đề xuất biểu đồ: {chart_recommendation or "Không cần"}

Bạn muốn điều chỉnh gì không?
```
Pipeline mode: auto-approve, proceed immediately.

---

## Step 2: Generate Excel via CLI Script

Use the bundled CLI script as the primary generation method. Prepare data as JSON, save to
a tmp file, then run the script. This approach is preferred over writing ephemeral scripts
because gen_xlsx.py already handles styles, formulas, formatting, and edge cases.

```bash
python3 .github/skills/gen-excel/scripts/gen_xlsx.py --input data.json --output output.xlsx --style corporate
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

## Step 5: Save, Verify & Read-Back

```yaml
SAVE_AND_VERIFY:
  1_SAVE:
    command: wb.save("{output_path}")
    
  2_RECALC:
    command: python3 scripts/recalc.py "{output_path}"
    
  3_FORMULA_CHECK:
    verify: No #REF!, #DIV/0!, #NAME?, #VALUE! in any cell
    report: "✅ {ws.title}: {ws.max_row} rows × {ws.max_column} cols"
```

### Step 5.5: Post-Generation Content Verification (MANDATORY)

```
╔══════════════════════════════════════════════════════════════════╗
║  🔴 DO NOT SKIP: Read the generated .xlsx BEFORE reporting     ║
║  Script exit code 0 does NOT mean data is correct.             ║
╚══════════════════════════════════════════════════════════════════╝
```

1. **READ**: `read_file` the .xlsx (via markitdown or openpyxl in script)
2. **CHECK DATA**: Are cells populated with real data? (not empty rows, not "N/A" everywhere)
3. **VERIFY URLs**: If output contains URLs → `fetch_webpage` on 2-3 random URLs:
   - Is it the right page? (title matches expected item)
   - Is it accessible? (not 404, 403, or generic search page)
   - If URL is broken → fix in data → re-generate that cell/row
4. **VERIFY FORMULAS**: Do SUM/AVERAGE produce plausible numbers? (not 0, not #REF!)
5. **If issues found** → fix data/URLs → re-save → re-verify (max 2 retries)
6. **Report**:
   ```
   ✅ File Excel đã tạo:
   - Đường dẫn: {output_path}  |  📏 {file_size}
   - {sheet_count} sheets, {total_rows} hàng, {formula_count} công thức
   - Verified: URLs checked ✓, formulas valid ✓, data populated ✓
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

## Examples

**Example 1 — Sales report with formulas:**
Input: Monthly sales data, 12 rows × 5 columns, need SUM and AVERAGE
Output: corporate .xlsx, 1 sheet, freeze panes, SUM/AVERAGE formulas, blue inputs, 18 KB

**Example 2 — Multi-sheet comparison:**
Input: Product data from 3 sources, need cross-sheet VLOOKUP
Output: .xlsx with 3 data sheets + 1 summary sheet, VLOOKUP formulas, color-coded, 25 KB

**Example 3 — Budget template:**
Input: Department budget categories, need percentage and IF formulas
Output: .xlsx with conditional formulas, percentage format, auto-filter, 15 KB

---

## Step 5: Shared Auditor Agent Call (Post-Generation)

```yaml
AUDITOR_GATE:
  when: After formula recalc and verification
  how:
    1. READ .github/skills/shared-agents/auditor.md
    2. BUILD prompt with:
       user_request: original user request
       output_content: column headers + sample rows + formula summary from .xlsx
       output_format: "excel"
       required_fields: data fields user specified
    3. CALL runSubagent(prompt=<built_prompt>, description="Audit Excel output")
    4. PARSE response:
       IF VERDICT == PASS → deliver to user
       IF VERDICT == FAIL → fix data/formulas with IMPROVEMENTS guidance (max 2 retries)
  budget: Counts toward max 5 auditor calls per pipeline run
  skip_when: Standalone quick generation
```

---

## What This Skill Does NOT Do

- Does NOT read/parse existing Excel files — that's thu-thap's job
- Does NOT create charts from data — that's tao-hinh's job
- Does NOT synthesize content — that's bien-soan's job
- Does NOT install dependencies — redirects to setup
