---
name: tao-hinh
description: |
  Generate professional charts from data using matplotlib + seaborn (Agg backend).
  Supports bar, line, pie, radar, scatter charts with consistent color palettes.
  Output PNG at dpi=160 with Vietnamese label support.
  Uses bundled scripts/gen_chart.py for all chart types.
  Use when user says "tạo biểu đồ", "vẽ chart", "create chart", or "/tao-hinh".
argument-hint: "[chart type: bar|line|pie|radar|scatter] [data source: Excel/CSV/inline]"
---

# Tạo Hình — Chart & Data Visualization

**References:** `references/chart-templates.md` | `references/image-generation.md`

```yaml
MODE: Script-based via terminal
LANGUAGE: All Copilot responses in Vietnamese
OUTPUT: PNG files at dpi=160, bbox_inches='tight'
BACKEND: matplotlib Agg (headless, no display)
CRITICAL: Always call matplotlib.use('Agg') BEFORE any other matplotlib import
```

---

## Trigger Conditions

Use this skill when user:
- Says "tạo biểu đồ", "vẽ chart", "tạo chart", "create chart", "visualize data"
- Uses command `/tao-hinh`
- Requests data visualization for reports or presentations
- Asks to embed charts into Word/PPT (chained from tao-word/tao-slide)

---

## Supported Chart Types

```yaml
CHART_TYPES:
  bar:     Comparing categories, ranking, before/after (vertical/horizontal/grouped/stacked)
  line:    Trends over time, continuous data (single/multi-series/area fill)
  pie:     Proportions, composition (max 8 slices — group rest as "Khác")
  radar:   Multi-dimensional comparison, skill profiles, scoring
  scatter: Correlation, distribution, clustering (optional trend line)
```

---

## Step 1: Identify Data Source

1. Detect source type: .xlsx/.xlsm (openpyxl/pandas) | .csv/.tsv (pandas) | inline dict/list | chained from previous skill
2. Parse headers vs data rows; handle Vietnamese column names (UTF-8)
3. Convert numeric strings to float; skip empty rows/columns
4. If column mapping is ambiguous → ask user which columns for X/Y axis

---

## Step 2: Configure Chart

1. Determine chart type (from request or infer from data shape: time series → line, categories → bar)
2. Confirm title (suggest from data), axis labels, series mapping
3. Apply defaults: figsize=[10,6], dpi=160, title_fontsize=16, grid=True (alpha=0.3)
4. Use professional PALETTE from `references/chart-templates.md` (maintain same color→series mapping across related charts)

---

## Step 3: Generate Chart

**Primary method** — Use bundled `gen_chart.py`:
```yaml
SCRIPT: .github/skills/tao-hinh/scripts/gen_chart.py
USAGE: |
  python3 .github/skills/tao-hinh/scripts/gen_chart.py \
    --input data.json --output chart.png --type bar
JSON_FORMAT: |
  {
    "title": "Chart Title",
    "x_label": "X", "y_label": "Y", "type": "bar",
    "data": {"labels": ["Q1","Q2","Q3"], "series": {"Doanh thu": [100,150,200]}}
  }
  // pie: data = { "labels": [...], "values": [...] }
  // radar: data = { "categories": [...], "series": { "Name": [...] } }
  // scatter: data = { "x": [...], "y": [...], "label": "Series" }
```

**Alternative** — Inline script (for custom/complex charts):
- See `references/chart-templates.md` for complete code templates per chart type
- ALWAYS: `matplotlib.use('Agg')` first | `plt.close()` after saving | `dpi=160, bbox_inches='tight'`
- NEVER call `plt.show()`

---

## Step 4: Execute & Verify

1. Run chart script via terminal
2. Verify output file exists and size > 1KB
3. On error: show full traceback; common fixes: missing font → fallback to DejaVu Sans, data type mismatch → add type conversion
4. Report: "✅ Saved: {path} ({size} KB, {type}, {W}×{H}px)"

---

## Step 5: Embed in Documents (Chain Support)

See `references/chart-templates.md` — EMBED_WORD / EMBED_PPTX / EMBED_HTML patterns.
Return chain output dict: `{path, width_px, height_px, chart_type}` to calling skill.

---

## Image Generation (Apple Silicon Only)

Basic text-to-image via SD-Turbo on Apple Silicon MPS.
For advanced modes (i2i, face preservation, FaceID), use `gen-image` skill instead.
See `references/image-generation.md` for full SD-Turbo script and style presets.

---

## File Naming

```yaml
charts:  "{name}_{chart_type}_{timestamp}.png"
images:  "{name}_{style}_{timestamp}.png"
directory: Same as source data, user-specified, or tmp/
```

---

## What This Skill Does NOT Do

- Does NOT display charts interactively (headless Agg only)
- Does NOT render text inside images (SD limitation)
- Does NOT call plt.show()
- Does NOT install dependencies — redirects to /cai-dat
