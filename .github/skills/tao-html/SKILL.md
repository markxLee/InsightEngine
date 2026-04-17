---
name: tao-html
description: |
  Create professional static HTML pages OR reveal.js presentations from synthesized content.
  Two modes: "page" (static page with inline CSS) and "presentation" (reveal.js slides).
  8 styles with light/dark variants. Transitions (slide/fade/zoom/convex/concave), fragment animations,
  per-slide backgrounds, code syntax highlighting. Use when user says "tạo trang web", "tạo html", or "/tao-html".
argument-hint: "[content] [style: corporate|academic|minimal|dark-modern|creative|warm-earth|dark-neon|dark-elegant] [mode: page|presentation]"
---

# Tạo HTML — Static HTML Page & Presentation Output Skill

**References:** `references/presentation-styles.md`

```yaml
MODES:
  page: Static HTML with inline CSS (jinja2)
  presentation: reveal.js slide deck via scripts/gen_reveal.py

MODE_DETECTION:
  presentation_triggers: "tạo slide html", "html presentation", "reveal.js", "slide deck html"
  page_triggers: "tạo trang web", "static page", "html report"
  default: page

LANGUAGE: Copilot responds in Vietnamese
INPUT: Structured Markdown from bien-soan or user text
OUTPUT: Single self-contained .html file
```

---

## Trigger Conditions

Use this skill when user:
- Says "tạo trang web", "tạo html", "tạo file html"
- Says "create html page", "static site", "create website"
- Uses command `/tao-html`
- Pipeline (tong-hop) routes content here for HTML output

---

## Style Selection

8 styles available: `corporate` | `academic` | `minimal` | `dark-modern` | `creative` | `warm-earth` | `dark-neon` | `dark-elegant`

Auto-infer: formal → corporate | research → academic | tech → dark-modern | creative/marketing → creative | default: corporate

Full color/font specs: `references/presentation-styles.md`

---

## Static Page Mode (page)

### Step 1: Pre-flight Check

1. Check: `python3 -c "import jinja2"` → if fail: "Chạy: pip install --user jinja2"
2. Confirm content available (from pipeline or ask user)
3. Determine style

### Step 2: Parse Content & Generate HTML

1. Convert Markdown → HTML elements:
   - Headings → `<h1>/<h2>/<h3>`; Paragraphs → `<p>`; Bold/italic → `<strong>/<em>`
   - Code blocks → `<pre><code>`; Tables → `<table>`; Lists → `<ul>/<ol><li>`
   - Images → `<img>` responsive; Charts → base64 embedded `<img src="data:image/png;base64,..."/>`

2. Render via Jinja2 template:
   ```python
   from jinja2 import Template
   html = Template(skeleton).render(title=title, inline_css=css, content_html=body)
   ```

3. CSS rules (all inline in `<style>` tag — NO external files or CDN):
   - box-sizing: border-box; responsive images (max-width 100%)
   - Color scheme from selected style
   - Table: border-collapse, alternating rows; Code: overflow-x auto
   - Print styles (@media print); NO JavaScript required

### Step 3: Save & Verify

1. Write UTF-8 file; verify: file exists, contains `<!DOCTYPE html>`, `<meta charset="UTF-8">`, no external refs
2. Report: "✅ File HTML: {path} ({size}) | Style: {style} | {section_count} phần | Portable: Yes"

---

## Presentation Mode (reveal.js)

### Content → Slides Mapping

```yaml
H1 → Title slide (centered, large)
H2 → Section divider slide
H3 → Content slide title
bullet_list → Slide bullets (max 6 per slide, split if more)
table → Data slide  |  image → Image slide  |  code_block → Code slide
blockquote → Quote slide  |  auto: closing slide "Cảm ơn!"
```

### Step 1: Prepare Slide JSON

```yaml
JSON_FORMAT: |
  {
    "title": "...", "subtitle": "...", "author": "...",
    "date": "2026-04-16", "style": "corporate",
    "slides": [
      {"type": "title", "title": "...", "subtitle": "..."},
      {"type": "section", "title": "Section Name"},
      {"type": "content", "title": "...", "bullets": ["..."], "notes": "Talking points"},
      {"type": "image", "title": "...", "image_path": "...", "caption": "..."},
      {"type": "quote", "text": "...", "author": "..."},
      {"type": "code", "title": "...", "language": "python", "code": "..."},
      {"type": "table", "title": "...", "headers": ["Col1"], "rows": [["a"]]},
      {"type": "closing", "title": "Cảm ơn!", "subtitle": "Questions?"}
    ]
  }
```

### Step 2: Run Script

```
python3 .github/skills/tao-html/scripts/gen_reveal.py --input data.json --output out.html --style corporate
python3 gen_reveal.py --input data.json --output out.html --style dark-neon --transition zoom --no-fragments
```

For transitions, custom backgrounds, speaker notes, PDF export:
→ See `references/presentation-styles.md`

---

## Error Handling

```yaml
ERRORS:
  template_error: Check Jinja2 syntax; escape special characters
  encoding_error: Ensure UTF-8 in meta tag and file write
  image_embed_error: Skip image on base64 failure; add alt text placeholder
  large_output: Warn if HTML > 5MB (many embedded images)
```

---

## What This Skill Does NOT Do

- Does NOT create multi-page websites (single .html file only)
- Does NOT synthesize content — that is bien-soan
- Does NOT install dependencies — redirects to /cai-dat
- Presentation mode requires internet on first load (CDN for reveal.js)
