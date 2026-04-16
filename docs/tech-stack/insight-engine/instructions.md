---
applyTo: "**"
---

# InsightEngine Instructions

## Overview

- InsightEngine is a **Copilot skill system**, NOT a web application — no server, no database, no deployment
- Runs entirely within VS Code + GitHub Copilot (Claude as reasoning engine)
- Architecture: skill SKILL.md files trigger Python/Node.js scripts via `run_in_terminal`
- All user-facing text (skill names, triggers, copilot responses) in **Vietnamese**
- Skill internal content (SKILL.md instructions to Copilot) in **English** for performance
- Each skill ≤ 400 lines; split agents into `agents/` and references into `references/` when needed
- Skill triggers must be **bilingual** (Vietnamese primary, English secondary)
- Primary pipeline skill: `tong-hop` — orchestrates all other skills

## Architecture & Patterns

### Skill System Architecture
- Skills live in `.github/skills/<ten-skill>/SKILL.md`
- Registered in `.github/copilot-instructions.md` under `## Skills Available`
- Pipeline skill (`tong-hop`) knows all sub-skills; routes based on user intent
- Sub-skills are invocable independently or via pipeline
- Each skill has: purpose, triggers, workflow steps, tool usage, output spec

### Script Execution Pattern
- Copilot writes Python/Node.js script to `scripts/` → executes via `run_in_terminal` → reads output
- Scripts are **ephemeral helpers** (Copilot generates per-task, not permanent)
- Permanent reusable scripts: `scripts/recalc.py` (Excel recalc), `scripts/with_server.py` (local server)
- All scripts must accept CLI arguments (no hardcoded paths)
- Always print output file path + size as final line

### Input Ingestion Pattern (thu-thap skill)
- Local files: use `markitdown` to convert any format → Markdown text
- URL fetching: use Copilot built-in `fetch_webpage` tool first; fallback to `httpx` + `beautifulsoup4`
- Google search: use `vscode-websearchforcopilot_webSearch` tool → fetch top 3-5 URLs → extract content
- Large files: chunk by section/page → process incrementally → merge summaries

### Content Synthesis Pattern (bien-soan skill)
- Always confirm output format and length with user before generating
- For multi-source: extract key points per source → identify overlaps → resolve conflicts → synthesize
- Translation: translate section by section, preserve formatting and structure
- Chunking threshold: if combined content > 50,000 words, use incremental synthesis

### Output Generation Pattern
- Each output skill (`tao-word`, `tao-excel`, `tao-slide`, `tao-pdf`, `tao-html`) has a `references/` folder with templates
- Templates are pre-built starter files or Jinja2 templates
- 3 style variants per format: `corporate`, `academic`, `minimal`
- User selects style explicitly OR pipeline infers from context (formal → corporate, research → academic, etc.)
- Always save output to user-specified path; default: current working directory

### Chaining Pattern
- Pipeline skill supports chaining: output of one skill becomes input of next
- Example: Excel data → chart images → PPT slides
- Always show user the chain plan before executing
- Store intermediate files in `tmp/` and clean up after

## Stack Best Practices

### Python Environment
- Use `pip install --user <package>` (no venv needed for script-level execution)
- Required packages: `markitdown[all]`, `python-docx`, `openpyxl`, `pandas`, `reportlab`, `pypdf`, `pdfplumber`, `matplotlib`, `seaborn`, `jinja2`, `httpx`, `beautifulsoup4`
- Optional (Apple Silicon only): `torch`, `diffusers`, `transformers`, `accelerate`
- Check package availability before use: `python3 -c "import <package>" 2>&1`

### Node.js Environment
- Required for PPT generation: `npm install -g pptxgenjs`
- Check availability: `node -e "require('pptxgenjs')" 2>&1`

### markitdown (File Reading)
- Install: `pip install --user "markitdown[all]"`
- Usage: `from markitdown import MarkItDown; md = MarkItDown(); result = md.convert("file.pdf"); print(result.text_content)`
- Supports: .docx, .xlsx, .pptx, .pdf, .html, .csv, .md, .txt, .jpg, .png
- For Excel: markitdown extracts table data as Markdown tables
- Fallback strategy if markitdown fails or output is garbled:
  - `.docx` → use `python-docx` directly: `doc = Document(path); [p.text for p in doc.paragraphs]`
  - `.xlsx` → use `openpyxl`: `wb = load_workbook(path); ws = wb.active`
  - `.pdf` → use `pdfplumber`: `with pdfplumber.open(path) as pdf: [p.extract_text() for p in pdf.pages]`
  - `.pptx` → use `python-pptx`: `prs = Presentation(path); [shape.text for slide in prs.slides for shape in slide.shapes]`
- Always try markitdown first; if result is empty or < 100 chars, switch to format-specific fallback

### python-docx (Word Output)
- Always set page size explicitly: `section.page_width = Inches(8.27)` for A4
- Use separate `Paragraph` objects instead of `\n` for line breaks
- Tables: use `WidthType.DXA` (never `PERCENTAGE` — breaks in Google Docs)
- Tables need both `columnWidths` array AND cell `width` property
- Bullets: use `LevelFormat.BULLET` (never Unicode bullet characters)
- Page breaks: must be inside a Paragraph object
- Images: use `add_picture(path, width=Inches(x))` — always set explicit width

### openpyxl + pandas (Excel Output)
- Use Excel formulas, NEVER hardcode calculated values
- Color coding convention: blue text = user inputs, black = formulas, green = cross-sheet links
- After writing formulas, run `scripts/recalc.py` to force recalculation
- Verify no formula errors after recalc: #REF!, #DIV/0!, #VALUE!, #N/A, #NAME?
- For data analysis: use pandas DataFrame → write to Excel with openpyxl for formatting

### pptxgenjs (PPT Output via Node.js)
- Colors: do NOT use `#` prefix (use `"FF5733"` not `"#FF5733"`)
- Layout: 16:9 default (`layout: "LAYOUT_WIDE"`)
- Every slide needs a visual element (image, chart, shape — no text-only slides)
- Font pairing: Georgia + Calibri (formal), Arial Black + Arial (modern), Cambria + Calibri (academic)
- Anti-patterns: avoid centering body text, avoid repeating layouts, avoid blue-only palettes
- QA: if screenshots available, verify text doesn't overflow slide boundaries

### reportlab (PDF Output)
- Use `Platypus` for complex layouts (headers, tables, multi-column)
- Use `Canvas` only for simple single-page documents
- Subscript/superscript: use `<sub>` and `<super>` XML tags (NEVER Unicode — renders as black boxes)
- Always embed fonts for special characters
- For structured data: generate Excel first → convert to PDF via reportlab table styles

### matplotlib (Chart Generation)
- ALWAYS include `matplotlib.use('Agg')` as first matplotlib import (required for headless/terminal)
- Standard figsize: `(10, 6)` at `dpi=160` → 1600×960px (safe for both screen and print)
- Use consistent color palette across all charts in a document
- Save as PNG: `plt.savefig(path, dpi=160, bbox_inches='tight')`
- Vietnamese labels: use transliteration or install `fonts-noto` for proper rendering
- Chart types by use case: bar (comparison), line (trend), pie (proportion), radar (multi-dimensional), scatter (correlation)

### Jinja2 (HTML Output)
- Templates stored in `.github/skills/tao-html/references/templates/`
- 3 styles: `corporate.html`, `academic.html`, `minimal.html`
- Each template is a complete single-file HTML (CSS inline, no external dependencies)
- Use `{{ variable }}` for content, `{% for item in items %}` for loops
- Generate static HTML — no JavaScript frameworks, no build step required
- Charts: embed as base64 PNG `<img src="data:image/png;base64,...">` for portability

### gen-image / diffusers (Image Generation — Apple Silicon only)
- ALWAYS use `matplotlib.use('Agg')` before any matplotlib import
- SD-Turbo settings: `guidance_scale=0.0`, `num_inference_steps=4`, strength=0.4-0.6 (i2i)
- Face modes: `guidance_scale=7.5`, `num_inference_steps=20-50`, `ip_scale ≤ 0.9`
- Cache location: `~/.cache/huggingface/` (first run downloads model)
- Style presets: `flat-icon`, `dark-tech`, `cartoon`, `minimal`, `watercolor`, `realistic`
- Anti-pattern: never ask SD-Turbo to render text inside images (unreadable)
- Output: save PNG at `512×512` minimum; `768×768` for presentation images

## Anti-Patterns

- **DO NOT** hardcode file paths in scripts — always use CLI arguments or variables
- **DO NOT** use `\n` inside python-docx paragraphs — create separate Paragraph objects
- **DO NOT** use `PERCENTAGE` width in python-docx tables — use `WidthType.DXA`
- **DO NOT** use `#` prefix for hex colors in pptxgenjs
- **DO NOT** hardcode calculated values in Excel — always use `=FORMULA()`
- **DO NOT** render text inside SD-Turbo images — text won't be readable
- **DO NOT** use Unicode bullets in python-docx — use `LevelFormat.BULLET`
- **DO NOT** use synchronous web requests for multiple URLs — use `asyncio` + `httpx.AsyncClient`
- **DO NOT** skip formula verification after Excel generation — always run recalc + check errors
- **DO NOT** make a skill > 400 lines — split into `agents/` subfiles if needed
- **DO NOT** hardcode Vietnamese text in scripts — pass as arguments from Copilot
- **DO NOT** create output files in script directory — always write to user-specified or CWD path

## Data Models

### Skill Structure
```
.github/skills/<ten-skill>/
  SKILL.md                  # Main skill (≤400 lines, English content)
  agents/                   # Sub-agents split from SKILL.md if needed
    <agent-name>.md
  references/               # Reference materials
    templates/              # Output templates (for output skills)
    <reference>.md
```

### Script Conventions
```python
# Standard script header pattern
import argparse
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="[Script purpose]")
    parser.add_argument("input", help="Input file or URL")
    parser.add_argument("--output", default="output", help="Output path")
    parser.add_argument("--style", choices=["corporate", "academic", "minimal"], default="corporate")
    args = parser.parse_args()
    # ... processing ...
    output_path = Path(args.output)
    print(f"✅ Saved: {output_path} ({output_path.stat().st_size / 1024:.1f} KB)")

if __name__ == "__main__":
    main()
```

### Skill Registration (copilot-instructions.md)
```yaml
SKILLS:
  <ten-skill>:
    purpose: "[Vietnamese description] / [English description]"
    location: ".github/skills/<ten-skill>/SKILL.md"
    triggers:
      - "Vietnamese trigger phrase"
      - "English trigger phrase"
      - "/command"
```

### Template Metadata (references/templates/)
```
templates/
  corporate/
    template.docx|xlsx|html   # Starter template file
    metadata.yaml             # Colors, fonts, layout info
  academic/
    ...
  minimal/
    ...
```

## Security & Configuration

- **No API keys required** — all AI reasoning via GitHub Copilot, search via built-in tools
- **No credentials stored** — scripts must not hardcode or log sensitive data
- **File path validation**: scripts should validate input paths exist before processing
- **No network requests in scripts** (except `httpx` for URL fetching) — web search via Copilot tools only
- **Output path sanitization**: use `Path().resolve()` to prevent path traversal
- **Temp files**: write to `tmp/` directory in repo root; clean up after use
- **No executable downloads**: scripts must not download and execute code from internet
- **Python packages**: install only from PyPI via pip (no untrusted sources)

## Commands & Scripts

### Setup (run once)
```bash
# Install Python dependencies
pip install --user "markitdown[all]" python-docx openpyxl pandas reportlab pypdf pdfplumber matplotlib seaborn jinja2 httpx beautifulsoup4

# Install Node.js dependency for PPT
npm install -g pptxgenjs

# Optional: Apple Silicon image generation
pip3 install --user torch diffusers transformers accelerate
```

### Permanent Scripts
```bash
# Excel formula recalculation (MANDATORY after writing Excel formulas)
python3 scripts/recalc.py <output.xlsx>

# Local server helper (for HTML preview)
python3 scripts/with_server.py --port 8080 --dir <html-output-dir>

# Verify all dependencies installed
# check_deps.py prints: ✅ <package> or ❌ <package> (not installed)
python3 scripts/check_deps.py
# Expected check_deps.py behavior:
#   checks: markitdown, docx, openpyxl, pandas, reportlab, pypdf, pdfplumber, matplotlib, jinja2, httpx, bs4
#   checks Node: node -e "require('pptxgenjs')"
#   prints summary: "X/Y dependencies ready"
#   exits 0 if all core deps present, exits 1 if missing critical deps
```

### Skill Execution Flow
```
User request (Vietnamese)
  → tong-hop skill reads intent
  → calls thu-thap (if input needed)
  → calls bien-soan (synthesis/translation)
  → calls tao-* (output generation)
  → run_in_terminal executes script
  → confirms output path + size to user
```

### Common Script Invocations
```bash
# Generate Word document
python3 scripts/gen_docx.py "input.md" --style corporate --output "report.docx"

# Generate Excel from data
python3 scripts/gen_xlsx.py "data.csv" --style corporate --output "report.xlsx"
python3 scripts/recalc.py "report.xlsx"

# Generate PPT
node scripts/gen_pptx.js --input "content.json" --style corporate --output "slides.pptx"

# Generate HTML
python3 scripts/gen_html.py "content.md" --style minimal --output "report.html"

# Generate PDF
python3 scripts/gen_pdf.py "content.md" --style academic --output "report.pdf"

# Generate chart
python3 scripts/gen_chart.py "data.csv" --type bar --output "chart.png"

# Generate image (Apple Silicon)
python3 scripts/gen_image.py "flat icon of data dashboard" --style flat-icon --output "icon.png"
```
