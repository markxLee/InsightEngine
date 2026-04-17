---
name: tao-hinh
description: |
  Generate charts and AI illustration images for reports, presentations, and documents.
  Chart mode (matplotlib): bar, line, pie, radar, scatter — from Excel/CSV/inline data, output PNG.
  Image generation mode (AI): characters (nhân vật), backgrounds, landscapes, and slide
  backgrounds/frames — auto-detects GPU (CUDA/MPS/CPU), no special hardware required.
  Always use this skill when the user wants any visual asset: data charts, illustration images,
  background images for slides, characters or scenes for documents, slide frames, or anything
  visual to make content look more professional — even casual requests like "tạo hình nền",
  "vẽ nhân vật", "cần ảnh minh họa", "làm slide đẹp hơn", "tạo background", "vẽ cái gì đó",
  "tạo biểu đồ", "vẽ chart", or "/tao-hinh", even without naming a specific skill.
argument-hint: "[mode: chart|image] [chart type: bar|line|pie|radar|scatter] [image type: character|background|landscape|slide-bg|slide-frame]"
---

# Tạo Hình — Charts & AI Images

**References:** `references/chart-templates.md` | `references/image-generation.md`

```yaml
LANGUAGE: All Copilot responses in Vietnamese
CHART_OUTPUT: PNG at dpi=160, bbox_inches='tight', matplotlib Agg backend (headless)
IMAGE_OUTPUT: PNG, auto GPU: CUDA > MPS > CPU (works on all platforms, CPU is slower)
```

> matplotlib.use('Agg') must be called before any other matplotlib import so the chart
> renders without requiring a display server — this is what makes charts work in headless/CLI environments.

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

### Step 3: Configure & Generate

- Infer chart type from data shape when not specified (time series → line, categories → bar)
- Confirm title and axis labels; suggest from data context
- Defaults: figsize=[10,6], dpi=160, title_fontsize=16, grid=True (alpha=0.3)
- Use bundled `gen_chart.py` as primary method:

```bash
python3 .github/skills/tao-hinh/scripts/gen_chart.py \
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

### Step 2: Configure Image

Choose image type and dimensions:

```yaml
character:   512×512 or 768×768 — illustrated figure, person, character
background:  768×768 — abstract or textured background
landscape:   768×512 — nature/urban scene, horizontal orientation
slide-bg:    1280×720 — 16:9 widescreen, suitable as PPT/HTML slide background
slide-frame: 1280×720 — decorative border overlay, transparent center recommended
```

Confirm prompt and style with user; suggest a style from the presets in the reference if unsure.

### Step 3: Detect GPU & Generate

Run the bundled image generation script (auto-detects CUDA/MPS/CPU):

```bash
python3 .github/skills/tao-hinh/scripts/gen_image.py \
  --prompt "your prompt" --style slide-bg-corporate \
  --width 1280 --height 720 --output output/image.png
```

The script tries CUDA → MPS → CPU in order.
On CPU: generation takes 2–10 min for 4 inference steps — inform the user before running.
Model (~2GB) downloads automatically on first use to `~/.cache/huggingface/`.

### Step 4: Verify & Report

1. Confirm file exists and size > 100KB (AI images should not be tiny)
2. On CUDA/MPS OOM: lower width/height by 256px and retry
3. Report: `✅ Saved: {path} ({size} KB, {W}×{H}px, device: {cuda|mps|cpu})`

### Step 5: Embed or Deliver

- For slide-bg/slide-frame: mention which slide template accepts the image (tao-slide Step 3)
- For character/background used in Word: mention inserting via tao-word Step 3
- Save to `output/` by default; `tmp/` for intermediate files

---

## File Naming

```yaml
charts:  "{name}_{chart_type}_{YYYYMMDD}.png"
images:  "{name}_{image_type}_{YYYYMMDD}.png"
directory: output/ by default, or user-specified path
```

---

## What This Skill Does NOT Do

- Does NOT display charts or images interactively (headless only — no plt.show())
- Does NOT render text inside AI images (SD-Turbo cannot reliably render text)
- Does NOT do face preservation or image-to-image restyling — use `gen-image` skill for that
- Does NOT install dependencies — redirects to /cai-dat
