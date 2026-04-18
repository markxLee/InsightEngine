# Excel Formatting Conventions

## Color Coding

| Cell Type | Font Color | Hex | Description |
|-----------|-----------|-----|-------------|
| Input data | Blue | `0000FF` | User-editable cells |
| Formulas | Black | `000000` | Calculated values |
| Cross-sheet | Green | `008000` | References to other sheets |
| Headers | Black Bold | `000000` | Column/row headers |
| Errors | Red | `FF0000` | Validation errors |

## Header Style

```python
header_font = Font(bold=True, size=11, color="000000")
header_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
header_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
header_border = Border(
    bottom=Side(style="thin", color="000000")
)
```

## Number Formats

| Data Type | Format | Example |
|-----------|--------|---------|
| Currency (VND) | `#,##0` | 1,500,000 |
| Currency (USD) | `$#,##0.00` | $1,500.00 |
| Percentage | `0.0%` | 85.5% |
| Date | `YYYY-MM-DD` | 2026-04-16 |
| Decimal | `#,##0.00` | 1,234.56 |
| Integer | `#,##0` | 1,234 |

## Layout Rules

- Freeze panes at A2 (header row always visible)
- Auto-filter on header row
- Column width: auto-fit content, min 10, max 40
- Print area: set to data range
- Page orientation: landscape for > 5 columns
