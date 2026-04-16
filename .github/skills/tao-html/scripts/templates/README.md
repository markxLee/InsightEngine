# Templates Directory

Jinja2 templates for reveal.js HTML presentation generation.

## Files

| Template | Purpose |
|----------|---------|
| base_reveal.html | Base reveal.js Jinja2 template with slide rendering |

## Usage

These templates are used by `gen_reveal.py` when `--use-jinja` flag is passed.
The default mode (without Jinja2) uses the built-in Python string formatting
in gen_reveal.py directly. The Jinja2 templates provide an alternative for
complex customizations.

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
