# Templates Directory

Jinja2 templates for reveal.js HTML presentation generation.

## Files

| Template | Style | Category | Transition |
|----------|-------|----------|------------|
| base_reveal.html | Base template | (parent) | — |
| corporate-formal.html | Professional blue-gray | Light / Business | slide |
| academic-research.html | Scholarly serif | Light / Academic | fade |
| tech-dark.html | Dark indigo/cyan | Dark / Tech | convex |
| creative-colorful.html | Purple-amber vibrant | Light / Creative | zoom |
| minimal-clean.html | Ultra-clean whitespace | Light / Minimal | fade |
| warm-elegant.html | Earthy tones, elegant serif | Light / Warm | fade |

## Architecture

All presentation templates **extend** `base_reveal.html` using Jinja2 inheritance:

```
base_reveal.html          ← Defines structure: head, styles, slides, scripts
  ├── corporate-formal    ← Overrides: colors, fonts, extra CSS
  ├── academic-research   ← Overrides: serif fonts, footnote style
  ├── tech-dark           ← Overrides: dark bg, gradient headings, code style
  ├── creative-colorful   ← Overrides: gradient slides, vibrant accents
  ├── minimal-clean       ← Overrides: thin weight, dash bullets
  └── warm-elegant        ← Overrides: earth tones, underline headings
```

## Usage

Templates are used by `gen_reveal.py` when the `--template` flag is passed.
Without `--template`, gen_reveal.py uses its built-in Python string formatting.

```bash
# Using built-in styles (no Jinja2)
python3 gen_reveal.py --input data.json --output out.html --style corporate

# Using Jinja2 templates (future support)
python3 gen_reveal.py --input data.json --output out.html --template corporate-formal
```

## Variables

| Variable | Type | Description |
|----------|------|-------------|
| title | str | Presentation title |
| author | str | Author name |
| style | dict | Style configuration (colors, fonts) |
| slides_html | str | Pre-rendered slide HTML |
| cdn_base | str | reveal.js CDN base URL |
| global_bg_css | str | Optional global background CSS |
| bg_color | str | Background color for Reveal.initialize |
| parallax_cfg | str | Optional parallax background config |
