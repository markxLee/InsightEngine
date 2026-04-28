---
name: gen-image
description: |
  Generate charts and AI illustration images for reports, presentations, and documents.
  Chart mode (matplotlib): bar, line, pie, radar, scatter — from Excel/CSV/inline data, output PNG.
  Image generation mode (AI): characters (nhân vật), backgrounds, landscapes, and slide
  backgrounds/frames — auto-detects GPU (CUDA/MPS/CPU), no special hardware required.
  Always use this skill when the user wants any visual asset: data charts, illustration images,
  background images for slides, characters or scenes for documents, slide frames, or anything
  visual to make content look more professional — even casual requests like "tạo hình nền",
  "vẽ nhân vật", "cần ảnh minh họa", "làm slide đẹp hơn", "tạo background", "vẽ cái gì đó",
  "tạo biểu đồ", "vẽ chart", or "gen-image", even without naming a specific skill.
argument-hint: "[mode: chart|image] [chart type: bar|line|pie|radar|scatter] [image type: character|background|landscape|slide-bg|slide-frame]"
version: 2.0
compatibility:
  requires:
    - Python >= 3.10
    - matplotlib >= 3.8.0, seaborn >= 0.13.0 (charts)
  optional:
    - torch >= 2.2.0, diffusers >= 0.27.0 (AI image generation)
    - Apple Silicon (MPS) or CUDA GPU recommended for image mode
    - ~7GB disk for SDXL-Turbo model, ~7GB for SDXL quality model
  tools:
    - run_in_terminal
---

# Tạo Hình — Charts & AI Images

**References:** `references/chart-templates.md` | `references/image-generation.md`

**Governance:** Read and follow `.github/RULE.md` — it overrides all instructions below.

**Quality loop (RULE-2):** After generating output, self-review + auditor gate (>80/100).
Pivot strategies: 1) different chart type/style, 2) adjust data presentation, 3) different color palette.

This skill handles two distinct visual output modes:
- **Charts** (matplotlib): data-driven bar, line, pie, radar, scatter charts from Excel/CSV/inline data
- **AI images** (diffusers/torch): generated illustrations, backgrounds, and slide assets

Chart output: PNG at dpi=160, `bbox_inches='tight'`, matplotlib Agg backend (headless).
Image output: PNG, auto GPU detection — CUDA > MPS > CPU (works everywhere, CPU is slower).

`matplotlib.use('Agg')` must be called before any other matplotlib import so the chart
renders without requiring a display server — this is what makes charts work in headless/CLI
environments.

All responses to the user are in Vietnamese.

---

## Step 1: Determine Mode

Identify which mode the user needs — clarify if ambiguous:

```yaml
CHART mode: User provides numerical data and wants a chart/graph
  → bar, line, pie, radar, scatter
  
IMAGE mode: User wants an AI-generated illustration
  → character: person, figure, illustrated character
  → background: abstract background, gradient, texture
  → landscape: nature scene, city view, environment
  → slide-bg: 16:9 widescreen background for presentations
  → slide-frame: decorative border or frame overlay for slides
```

---

## Chart Mode — Steps 2–5

### Step 2: Identify Data

1. Detect source: .xlsx/.xlsm → openpyxl/pandas | .csv/.tsv → pandas | inline dict/list | chained from previous skill
2. Parse headers vs data rows; handle Vietnamese column names (UTF-8)
3. If column mapping ambiguous → ask user which columns for X/Y

### Step 2.5: Data Story Analysis

Before generating a chart, analyze the data to understand what story it tells. A chart that
just displays numbers is a table with extra steps — a good chart reveals insights. This step
is what makes the difference between "here's a bar chart of your data" and "here's a chart
that highlights the 3x revenue growth in Q4."

**1. Identify the data story type:**

| Story type | Signal in data | Best chart | Why |
|---|---|---|---|
| Trend over time | Sequential dates/months/years in X | Line chart | Shows direction and pace of change |
| Comparison | Categories with single metric | Horizontal bar | Easy to compare lengths |
| Composition | Parts of a whole (percentages/shares) | Pie (≤5 items) or stacked bar (>5) | Shows proportions |
| Distribution | Many data points, continuous variable | Histogram or box plot | Shows spread and outliers |
| Relationship | Two continuous variables | Scatter plot | Shows correlation |
| Ranking | Categories sorted by value | Horizontal bar (sorted) | Clear visual ranking |
| Multi-dimension | Multiple metrics per category | Radar chart (≤7 axes) | Shows profile/shape |

Don't just default to what the user says — if they say "bar chart" but the data is clearly
a time series with 24 monthly data points, suggest a line chart instead (but still offer the
bar chart if they prefer). Explain why: "Dữ liệu theo thời gian thường hiển thị tốt hơn bằng
biểu đồ đường vì nó thể hiện xu hướng rõ ràng hơn."

**2. Identify key insights to annotate:**

Read the actual data values and find:
- **Max/min**: the highest and lowest values — annotate them on the chart
- **Trends**: is the data going up, down, or flat? Add a trend line if useful
- **Outliers**: values that are significantly different from the rest — highlight with color
- **Crossover points**: where two series intersect (e.g., costs exceed revenue) — mark it
- **Thresholds**: if there's a meaningful boundary (e.g., 100% target), add a reference line

**3. Smart defaults based on data:**

```yaml
SMART_DEFAULTS:
  time_series_data:
    chart: line
    add: trend_line, annotate_max_min, x_date_format
  
  few_categories_one_metric:  # ≤ 7 categories
    chart: horizontal_bar (sorted descending)
    add: value_labels_on_bars, highlight_top_1
  
  many_categories_one_metric:  # > 7 categories
    chart: horizontal_bar (top 10 + "Others")
    add: value_labels, note about truncation
  
  parts_of_whole:
    chart: pie (≤5) or stacked_bar (>5)
    add: percentage_labels, explode_largest_slice
  
  two_numeric_columns:
    chart: scatter
    add: correlation_coefficient_in_subtitle, trend_line
  
  multi_series_categories:
    chart: grouped_bar or radar (if ≤7 axes)
    add: legend, consistent_colors_per_series
```

Report the analysis:
```
📊 Phân tích dữ liệu:
- Loại câu chuyện: {story_type}
- Đề xuất biểu đồ: {recommended_chart} (lý do: {why})
- Insights chính: {key_insights}
- Annotations: {planned_annotations}
```

### Step 3: Configure & Generate

- Infer chart type from data shape when not specified (time series → line, categories → bar)
- Confirm title and axis labels; suggest from data context
- Defaults: figsize=[10,6], dpi=160, title_fontsize=16, grid=True (alpha=0.3)
- **Color-blind safe mode**: when user mentions accessibility, color-blind, or the chart will
  be printed in B&W, use the color-blind friendly palette: `['#0072B2', '#E69F00', '#009E73',
  '#CC79A7', '#D55E00', '#56B4E9', '#F0E442', '#000000']` (Okabe-Ito palette). Pass
  `--palette colorblind` to gen_chart.py to activate.
- **Batch charts**: when multiple charts are needed (e.g., pipeline produces 3 datasets),
  loop through data items and generate each chart sequentially. Name files with index:
  `{name}_{chart_type}_{index}_{date}.png`
- Use bundled `gen_chart.py` as primary method:

```bash
python3 .github/skills/gen-image/scripts/gen_chart.py \
  --input data.json --output chart.png --type bar
```

JSON input format: `{"title":"…","x_label":"…","y_label":"…","type":"bar","data":{"labels":[…],"series":{"Series":[…]}}}`
For pie: `"data":{"labels":[…],"values":[…]}` | radar: `"data":{"categories":[…],"series":{"Name":[…]}}`

See `references/chart-templates.md` for inline script templates and color palettes.

### Step 4: Verify & Report

1. Confirm output file exists and size > 1KB
2. Common fixes: missing font → DejaVu Sans fallback; data type mismatch → add type conversion
3. Report: `✅ Saved: {path} ({size} KB, {type}, {W}×{H}px)`

### Step 5: Embed in Documents

See `references/chart-templates.md` EMBED_WORD / EMBED_PPTX / EMBED_HTML patterns.
Return `{path, width_px, height_px, chart_type}` to calling skill when chained.

---

## Image Generation Mode — Steps 2–5

See `references/image-generation.md` for full script, style presets, and example prompts.

**v2.0 — Multi-model with quality tiers.** The script now supports SDXL-Turbo (fast) and
SDXL Base (quality) models. Character styles auto-select the quality model for better faces,
anatomy, and prompt adherence. Use `--model turbo` to force fast mode when speed matters.

### Step 2: Choose Model Tier & Configure

**Model selection — critical for character quality:**

```yaml
turbo:
  model: SDXL-Turbo (stabilityai/sdxl-turbo)
  steps: 4 | speed: ~6s on MPS | negative_prompt: NO
  use_for: backgrounds, landscapes, slides, previews
  quality: good for non-face content, weak for character faces

quality:
  model: SDXL Base 1.0 (stabilityai/stable-diffusion-xl-base-1.0)
  steps: 25 | speed: ~60s on MPS | negative_prompt: YES
  use_for: characters, portraits, detailed art, final assets
  quality: much better faces, anatomy, prompt adherence
  first_run: ~7GB model download (one-time)

legacy:
  model: SD-Turbo (stabilityai/sd-turbo)
  steps: 4 | speed: ~6s | negative_prompt: NO
  use_for: backward compatibility only — DO NOT use for characters
```

**Style presets auto-select the right model:**
- `character-anime`, `character-anime-male`, `character-anime-female`, `character-realistic` → quality
- `landscape-*`, `background-*`, `slide-*` → turbo

**Dimensions by type:**

```yaml
character (quality):  768×1024 — portrait orientation, better anatomy
background:           768×768  — square, abstract/textured
landscape:            768×512  — horizontal panoramic
slide-bg/frame:       1280×720 — 16:9 widescreen
```

**Character gender presets (ALWAYS use for characters):**
- `character-anime-male` — includes "masculine, 1boy" keywords
- `character-anime-female` — includes "feminine, 1girl" keywords
- `character-anime` — gender-neutral (specify gender in prompt)

### Step 3: Generate

**Standard text-to-image:**

```bash
# Quality character (auto-selects quality model + negative prompt)
python3 .github/skills/gen-image/scripts/gen_image.py \
  --prompt "warrior boy, red armor, determined expression" \
  --style character-anime-male --output output/char.png

# Fast background (auto-selects turbo)
python3 .github/skills/gen-image/scripts/gen_image.py \
  --prompt "fantasy forest" --style landscape-fantasy --output output/bg.png

# Force turbo for speed preview
python3 .github/skills/gen-image/scripts/gen_image.py \
  --prompt "warrior boy" --style character-anime --model turbo --output output/preview.png
```

**Character consistency via img2img (IMPORTANT for multi-pose sets):**

When generating the SAME character in multiple poses:
1. Generate canonical view first (front-facing, neutral pose)
2. Use that image as `--reference` for all subsequent poses
3. Strength 0.45-0.65: preserves identity while allowing pose changes

```bash
# Step 1: Generate canonical reference
python3 .github/skills/gen-image/scripts/gen_image.py \
  --prompt "warrior boy, red armor, standing front view" \
  --style character-anime-male --seed 42 --output output/char_ref.png

# Step 2: Generate other poses FROM the reference
python3 .github/skills/gen-image/scripts/gen_image.py \
  --prompt "same warrior boy, red armor, fighting action pose" \
  --style character-anime-male --reference output/char_ref.png \
  --strength 0.55 --output output/char_fight.png

python3 .github/skills/gen-image/scripts/gen_image.py \
  --prompt "same warrior boy, red armor, riding horse" \
  --style character-anime-male --reference output/char_ref.png \
  --strength 0.50 --output output/char_ride.png
```

**Negative prompts (auto-set for quality model):**

The quality model automatically applies negative prompts to avoid common defects:
- Characters: "ugly, bad anatomy, deformed face, wrong gender, extra limbs..."
- General: "blurry, low quality, watermark, text..."

Override with `--negative "custom negative prompt"` if needed.

The script tries CUDA → MPS → CPU in order.
First run downloads models to `~/.cache/huggingface/` (turbo: ~7GB, quality: ~7GB).

### Step 4: Verify & Report

1. Confirm file exists and size > 100KB (AI images should not be tiny)
2. **For characters: visually check face quality, gender, and consistency**
3. On CUDA/MPS OOM: use `--model turbo` or lower dimensions by 256px
4. Report: `✅ Saved: {path} ({size} KB, {W}×{H}px, {elapsed}s, device: {device})`

### Step 5: Embed or Deliver

- For slide-bg/slide-frame: mention which slide template accepts the image (gen-slide Step 3)
- For character/background used in Word: mention inserting via gen-word Step 3
- Save to `output/` by default; `tmp/` for intermediate files

---

## File Naming

```yaml
charts:  "{name}_{chart_type}_{YYYYMMDD}.png"
images:  "{name}_{image_type}_{YYYYMMDD}.png"
directory: output/ by default, or user-specified path
```

---

## Examples

**Example 1 — Bar chart from Excel data:**
Input: sales_data.xlsx with columns [Month, Revenue, Costs], bar chart requested
Output: bar chart PNG (1600×960px, dpi=160), labeled axes, professional palette, 85 KB

**Example 2 — Radar chart for comparison:**
Input: Inline data comparing 3 products across 5 criteria
Output: radar chart PNG, legend, gridlines, 70 KB

**Example 3 — AI slide background:**
Input: Prompt "abstract technology pattern, blue gradient, clean"
Output: 1280×720 PNG (slide-bg), generated via SDXL-Turbo on MPS, ~6 seconds, 180 KB

**Example 4 — Quality anime character (v2.0):**
Input: `--prompt "warrior boy, red armor" --style character-anime-male`
Output: 768×1024 PNG, SDXL quality model, 25 steps, negative prompts auto-applied, ~60s, 350 KB

**Example 5 — Consistent character set (v2.0):**
Input: Generate canonical front view, then 3 poses with `--reference` + `--strength 0.55`
Output: 4 character images with consistent appearance across all poses

---

## What This Skill Does NOT Do

- Does NOT display charts or images interactively (headless only — no plt.show())
- Does NOT render text inside AI images (diffusion models cannot reliably render text)
- Does NOT do fine-tuning or LoRA training — for that, user needs separate workflow
- Does NOT install dependencies — redirects to setup
- Does NOT guarantee pixel-perfect character consistency — img2img mode provides
  style/color/shape consistency but not identical faces across all poses
