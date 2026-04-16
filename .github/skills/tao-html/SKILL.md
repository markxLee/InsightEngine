---
name: tao-html
description: |
  Create professional static HTML pages OR reveal.js presentations from synthesized content.
  Two modes: "page" (static page with inline CSS) and "presentation" (reveal.js slides).
  8 styles with light/dark variants. Transitions (slide/fade/zoom/convex/concave), fragment animations,
  per-slide backgrounds, code syntax highlighting. Use when user says "tạo trang web", "tạo html", or "/tao-html".
argument-hint: "[content] [style: corporate|academic|minimal|dark-modern|creative|warm-earth|dark-neon|dark-elegant] [mode: page|presentation] [--transition slide|fade|zoom|convex|concave|none] [--background ...]"
---

# Tạo HTML — Static HTML Page & Presentation Output Skill

Generates self-contained `.html` files — either static pages (inline CSS) or reveal.js presentations.

```yaml
MODES:
  page: Static HTML page with inline CSS (original mode)
  presentation: reveal.js slide deck with CDN, keyboard nav, transitions

MODE_DETECTION:
  presentation_triggers:
    - "tạo slide html", "html presentation", "trình chiếu html"
    - "reveal.js", "slide deck html", "presentation html"
    - Content has clear slide structure (numbered sections, short bullets)
  page_triggers:
    - "tạo trang web", "static page", "html report"
    - Content is long-form narrative (paragraphs, articles)
  default: page (unless content/intent clearly suggests presentation)

LANGUAGE: Copilot responds in Vietnamese
INPUT: Structured Markdown from bien-soan or user text
OUTPUT: Single .html file (self-contained)
LIBRARIES: jinja2 (page mode), scripts/gen_reveal.py (presentation mode)
```

---

## Trigger Conditions

Use this skill when user:
- Says "tạo trang web", "tạo html", "tạo file html"
- Says "create html page", "create website", "static site"
- Uses command `/tao-html`
- Pipeline (tong-hop) routes content here for HTML output

---

## Pre-Flight Check

```yaml
PRE_FLIGHT:
  1. Check jinja2 installed:
     command: python3 -c "import jinja2" 2>&1
     if_fail: "Chạy: pip install --user jinja2"
     
  2. Check content available:
     - From pipeline: content variable from bien-soan
     - From user: raw text or file path
     if_missing: Ask user for content or redirect to thu-thap + bien-soan
     
  3. Determine style:
     - If user specified: use that style
     - If pipeline: use inferred style from tong-hop
     - Default: corporate
```

---

## Template Styles

```yaml
STYLES:
  corporate:
    description: Professional business style with blue accent
    colors:
      primary: "#1a365d"
      secondary: "#2b6cb0"
      background: "#ffffff"
      text: "#2d3748"
      accent: "#3182ce"
    fonts:
      heading: "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
      body: "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
    layout:
      max_width: 900px
      sidebar: false
      header: Full-width blue gradient banner
      
  academic:
    description: Clean serif style for research and papers
    colors:
      primary: "#1a202c"
      secondary: "#4a5568"
      background: "#fafafa"
      text: "#1a202c"
      accent: "#744210"
    fonts:
      heading: "Georgia, 'Times New Roman', serif"
      body: "Georgia, 'Times New Roman', serif"
    layout:
      max_width: 750px
      sidebar: false
      header: Simple centered title with rule line
      
  minimal:
    description: Ultra-clean whitespace-focused design
    colors:
      primary: "#111827"
      secondary: "#6b7280"
      background: "#ffffff"
      text: "#374151"
      accent: "#059669"
    fonts:
      heading: "'Inter', 'Helvetica Neue', Arial, sans-serif"
      body: "'Inter', 'Helvetica Neue', Arial, sans-serif"
    layout:
      max_width: 680px
      sidebar: false
      header: Minimal top-left title

  dark-modern:
    description: Dark background, neon accents, tech/startup vibe
    colors:
      primary: "#6366f1"
      secondary: "#22d3ee"
      background: "#0f172a"
      text: "#f1f5f9"
      accent: "#22d3ee"
    fonts:
      heading: "'Inter', 'SF Pro Display', sans-serif"
      body: "'Inter', 'SF Pro Text', sans-serif"
    layout:
      max_width: 900px
      sidebar: false
      header: Full-width gradient banner (indigo → cyan)
    css_extras: |
      /* Glow effect on headings */
      h1, h2 { text-shadow: 0 0 20px rgba(99, 102, 241, 0.3); }
      /* Code blocks with dark theme */
      pre { background: #1e293b; border-left: 3px solid #22d3ee; }
      /* Cards with subtle border glow */
      .card { border: 1px solid #334155; box-shadow: 0 0 15px rgba(99, 102, 241, 0.1); }

  creative:
    description: Vibrant gradients, playful shapes, event/marketing style
    colors:
      primary: "#8b5cf6"
      secondary: "#f59e0b"
      background: "#fffbeb"
      text: "#1e1b4b"
      accent: "#f59e0b"
    fonts:
      heading: "'Poppins', 'Nunito', sans-serif"
      body: "'Open Sans', 'Nunito', sans-serif"
    layout:
      max_width: 960px
      sidebar: false
      header: Full-width gradient banner (purple → amber)
    css_extras: |
      /* Rounded shapes and playful feel */
      .card, blockquote { border-radius: 16px; }
      /* Gradient text for main heading */
      h1 { background: linear-gradient(135deg, #8b5cf6, #f59e0b); -webkit-background-clip: text; color: transparent; }
      /* Bold callout boxes */
      .callout { background: linear-gradient(135deg, #ede9fe, #fef3c7); border-radius: 16px; padding: 1.5rem; }
```

---

## Step 1: Parse Content

```yaml
PARSE_MARKDOWN:
  convert_to:
    headings: <h1>, <h2>, <h3> tags
    paragraphs: <p> tags
    bold: <strong> tags
    italic: <em> tags
    code_inline: <code> tags
    code_block: <pre><code> tags with syntax highlighting CSS
    tables: <table> with styled headers
    lists: <ul>/<ol> with <li> elements
    blockquotes: <blockquote> with left border styling
    links: <a> tags (target="_blank" for external)
    images: <img> tags with responsive sizing
    
  charts_as_images:
    if_chart_png_available:
      - Read PNG file as base64
      - Embed as: <img src="data:image/png;base64,{encoded}" />
      - This makes HTML fully self-contained (no external files)
```

---

## Step 2: Generate HTML with Jinja2

```yaml
TEMPLATE_STRUCTURE:
  html_skeleton: |
    <!DOCTYPE html>
    <html lang="vi">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>{{ title }}</title>
      <style>
        {{ inline_css }}
      </style>
    </head>
    <body>
      <header>{{ header_html }}</header>
      <main class="container">
        {{ content_html }}
      </main>
      <footer>{{ footer_html }}</footer>
    </body>
    </html>
    
  inline_css_includes:
    - Reset/normalize styles
    - Typography (font faces, sizes, line heights)
    - Color scheme from selected style
    - Table styling (borders, alternating rows)
    - Code block styling (background, monospace)
    - Responsive design (max-width, mobile breakpoints)
    - Print styles (@media print)
```

---

## Step 3: CSS Per Style

```yaml
CSS_RULES:
  all_styles:
    - box-sizing: border-box on all elements
    - Responsive images: max-width 100%
    - Table: border-collapse, full-width
    - Code blocks: overflow-x auto, padding
    - Links: colored, underline on hover
    - Print: hide header/footer, adjust margins
    
  portability:
    - ALL CSS must be inline (in <style> tag)
    - NO external CSS files or CDN links
    - NO JavaScript required
    - NO external font imports (use system font stacks)
    - Charts/images embedded as base64 data URIs
```

---

## Step 4: Save and Verify

```yaml
SAVE_AND_VERIFY:
  1_RENDER:
    script: |
      from jinja2 import Template
      template = Template(html_skeleton)
      html_output = template.render(
          title=title,
          inline_css=css_content,
          header_html=header,
          content_html=body,
          footer_html=footer
      )
      
  2_SAVE:
    script: |
      with open(output_path, "w", encoding="utf-8") as f:
          f.write(html_output)
          
  3_VERIFY:
    checks:
      - File exists and size > 0
      - Contains <!DOCTYPE html>
      - Contains <meta charset="UTF-8">
      - No broken image references (all base64 embedded)
      - No external CSS/JS references
      
  4_REPORT:
    format: |
      File HTML created:
      - Path: {output_path}
      - Size: {file_size}
      - Style: {style_name}
      - Sections: {section_count}
      - Images embedded: {image_count}
      - Portable: Yes (single file, no dependencies)
```

---

## Presentation Mode (reveal.js) — US-4.2.1

When mode is "presentation", generate a reveal.js slide deck instead of a static page.

### Content → Slides Mapping

```yaml
SLIDE_MAPPING:
  H1_heading: Title slide (centered, large text)
  H2_heading: Section divider slide
  H3_heading: Content slide title
  bullet_list: Slide content (each bullet = one line)
  numbered_list: Slide content with ordered items
  paragraph: Slide content (split long paragraphs across slides)
  table: Data slide (styled table)
  image: Image slide (centered, responsive)
  blockquote: Quote slide (styled blockquote)
  code_block: Code slide (syntax highlighted)

SLIDE_RULES:
  - Each H2 creates a new horizontal section
  - Each H3 within H2 creates a new vertical slide within that section
  - Max ~6 bullet points per slide (split if more)
  - Max ~50 words per slide (move overflow to next slide)
  - Title slide is always first (from H1 or document title)
  - Closing slide auto-generated with "Cảm ơn!" / "Thank you!"
```

### Script Execution

```yaml
PRESENTATION_WORKFLOW:
  1. Copilot prepares content as JSON:
     {
       "title": "Presentation Title",
       "subtitle": "Optional subtitle",
       "author": "Author name",
       "date": "2026-04-16",
       "style": "corporate",
       "slides": [
         {
           "type": "title",
           "title": "Main Title",
           "subtitle": "Subtitle text"
         },
         {
           "type": "section",
           "title": "Section Name"
         },
         {
           "type": "content",
           "title": "Slide Title",
           "bullets": ["Point 1", "Point 2", "Point 3"]
         },
         {
           "type": "image",
           "title": "Image Slide",
           "image_path": "path/to/image.png",
           "caption": "Image caption"
         },
         {
           "type": "quote",
           "text": "Quote text here",
           "author": "Quote author"
         },
         {
           "type": "code",
           "title": "Code Example",
           "language": "python",
           "code": "print('hello')"
         },
         {
           "type": "table",
           "title": "Data Table",
           "headers": ["Col1", "Col2"],
           "rows": [["a", "b"], ["c", "d"]]
         },
         {
           "type": "closing",
           "title": "Cảm ơn!",
           "subtitle": "Questions?"
         }
       ]
     }
     
  2. Save JSON to tmp file
  3. Run: python3 .github/skills/tao-html/scripts/gen_reveal.py --input data.json --output output.html --style corporate
  4. Verify output exists and contains reveal.js structure
  5. Report file path + size
```

### reveal.js CDN Configuration

```yaml
REVEALJS_CDN:
  version: "5.1.0"
  base_url: "https://cdn.jsdelivr.net/npm/reveal.js@5.1.0"
  css: "{base_url}/dist/reveal.css"
  theme: "{base_url}/dist/theme/{theme_name}.css"
  js: "{base_url}/dist/reveal.js"
  
  plugins_included:
    - RevealNotes (speaker notes)
    - RevealHighlight (code syntax highlighting)
    
  keyboard_navigation:
    arrows: Navigate slides
    space: Next slide
    escape: Overview mode
    f: Fullscreen
    s: Speaker notes view
    
  output_structure: |
    Single .html file containing:
    - CDN links to reveal.js CSS + JS
    - Inline custom CSS for the selected style
    - All slide content in <section> tags
    - Initialization script at bottom
```

### Presentation Styles (US-4.2.3)

8 themes with light/dark variants. Each theme has consistent typography, link colors,
table styling, blockquote borders, and code block backgrounds.

```yaml
PRESENTATION_STYLES:
  # ── Light variants ─────────────────────────────────
  corporate:     # Professional blue business — default for formal content
    reveal_theme: white
    background: "#ffffff"
    heading: "#1a365d"  |  accent: "#3182ce"
    fonts: Segoe UI / Segoe UI
    
  academic:      # Scholarly serif — default for research/papers
    reveal_theme: simple
    background: "#fafafa"
    heading: "#1a202c"  |  accent: "#744210"
    fonts: Georgia / Georgia
    
  minimal:       # Ultra-clean whitespace — default for clean/simple
    reveal_theme: white
    background: "#ffffff"
    heading: "#111827"  |  accent: "#059669"
    fonts: Inter / Inter
    
  creative:      # Purple-amber vibrant — default for marketing/creative
    reveal_theme: moon
    background: "#fffbeb"
    heading: "#8b5cf6"  |  accent: "#f59e0b"
    fonts: Poppins / Open Sans

  warm-earth:    # Warm earthy tones — for organic/natural content
    reveal_theme: simple
    background: "#fdf8f3"
    heading: "#92400e"  |  accent: "#b45309"
    fonts: Playfair Display / Source Sans Pro

  # ── Dark variants ──────────────────────────────────
  dark-modern:   # Indigo/cyan dark — default for tech/modern
    reveal_theme: night
    background: "#0f172a"
    heading: "#6366f1"  |  accent: "#22d3ee"
    fonts: Inter / Inter

  dark-neon:     # Neon cyan/magenta — for bold tech/gaming
    reveal_theme: night
    background: "#0a0a0a"
    heading: "#00ffc8"  |  accent: "#ff3cac"
    fonts: JetBrains Mono / Inter

  dark-elegant:  # Gold on navy — for premium/luxury
    reveal_theme: night
    background: "#1a1a2e"
    heading: "#e0a458"  |  accent: "#e0a458"
    fonts: Playfair Display / Lato

STYLE_DETECTION:
  formal/business: corporate
  research/paper: academic
  clean/simple: minimal
  marketing/fun: creative
  nature/organic: warm-earth
  tech/modern: dark-modern
  gaming/bold: dark-neon
  luxury/premium: dark-elegant
```

### Custom Backgrounds (US-4.2.3)

Per-slide and global background support for reveal.js presentations.

```yaml
BACKGROUND_TYPES:
  solid_color:
    global: --background "#1a365d"
    per_slide: {"background": "#1a365d"}
    
  gradient:
    global: --background "linear-gradient(135deg, #667eea, #764ba2)"
    per_slide: {"background": {"gradient": "linear-gradient(135deg, #667eea, #764ba2)"}}
    
  image_url:
    global: --background "https://example.com/bg.jpg"
    per_slide: {"background": {"image": "https://example.com/bg.jpg", "opacity": 0.3}}
    
  local_image:
    per_slide: {"background": {"image": "/path/to/bg.png", "size": "cover"}}
    
  video_url:
    per_slide: {"background": {"video": "https://example.com/bg.mp4", "opacity": 0.5}}

BACKGROUND_OPTIONS:
  opacity: 0.0 - 1.0 (dim overlay intensity)
  size: cover | contain | custom (CSS background-size)
  position: center | top | bottom (CSS background-position)
  repeat: no-repeat | repeat (CSS background-repeat)

CLI_EXAMPLES:
  # Use dark-neon theme
  python3 gen_reveal.py --input data.json --output out.html --style dark-neon
  
  # Use corporate with gradient background
  python3 gen_reveal.py --input data.json --output out.html --style corporate --background "linear-gradient(135deg, #1a365d, #3182ce)"
  
  # Per-slide backgrounds in JSON data
  {"type": "title", "title": "Hello", "background": {"gradient": "linear-gradient(135deg, #667eea, #764ba2)"}}
  {"type": "content", "title": "Data", "bullets": [...], "background": {"image": "https://img.jpg", "opacity": 0.2}}
```

### Transitions and Animations (US-4.2.2)

Smooth slide transitions and fragment animations for professional presentations.

```yaml
TRANSITION_TYPES:
  none:     Instant switch (no animation)
  slide:    Horizontal slide (corporate default)
  fade:     Crossfade (academic, dark-modern default)
  convex:   3D convex rotation (warm-earth default)
  concave:  3D concave rotation (dark-elegant default)
  zoom:     Zoom in/out (creative, dark-neon default)

STYLE_DEFAULTS:
  corporate: slide
  academic: fade
  minimal: none
  creative: zoom
  warm-earth: convex
  dark-modern: fade
  dark-neon: zoom
  dark-elegant: concave

TRANSITION_PRIORITY:
  1. CLI --transition flag (highest)
  2. JSON data "transition" key (top-level)
  3. Style default (from STYLE_DEFAULTS)
  4. Fallback: "slide"

PER_SLIDE_TRANSITION:
  # Override transition for individual slides in JSON:
  {"type": "content", "title": "Special", "bullets": [...], "transition": "zoom"}
  
FRAGMENT_ANIMATIONS:
  # Bullet points appear one-by-one by default (class="fragment")
  # Disable globally with --no-fragments CLI flag
  # Or set "fragments": false in JSON data
  
  enabled_by_default: true
  applies_to: bullet list items in "content" slides
  effect: Items appear sequentially on spacebar/arrow press

CLI_EXAMPLES:
  # Corporate with fade transition
  python3 gen_reveal.py --input data.json --output out.html --style corporate --transition fade
  
  # Dark-neon with zoom, no fragments
  python3 gen_reveal.py --input data.json --output out.html --style dark-neon --transition zoom --no-fragments
  
  # Academic with default transition (fade)
  python3 gen_reveal.py --input data.json --output out.html --style academic
  
CODE_SYNTAX_HIGHLIGHTING:
  plugin: RevealHighlight (highlight.js via CDN)
  theme: monokai
  usage: |
    {"type": "code", "title": "Example", "language": "python", "code": "def hello():\n    print('hi')"}
  supported_languages: python, javascript, typescript, bash, json, html, css, sql, yaml, etc.
```

---

## Error Handling

```yaml
ERRORS:
  template_error:
    detect: Jinja2 rendering error
    action: Check template syntax, escape special characters
    
  encoding_error:
    detect: Vietnamese characters corrupted
    action: Ensure UTF-8 encoding in meta tag and file write
    
  image_embed_error:
    detect: Base64 encoding fails for chart image
    action: Skip image, add alt text placeholder
    
  large_output:
    detect: HTML file > 5MB (many embedded images)
    action: Warn user, suggest reducing image count or quality
```

---

## What This Skill Does NOT Do

- Does NOT create multi-page websites (single HTML file only)
- Does NOT host or deploy the HTML file
- Does NOT synthesize content — that is bien-soan's job
- Does NOT install dependencies — redirects to /cai-dat
- Presentation mode uses CDN for reveal.js — requires internet on first load
