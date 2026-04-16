---
name: tao-html
description: |
  Create professional static HTML pages from synthesized content.
  Uses jinja2 templates with inline CSS (no external dependencies).
  5 styles: corporate, academic, minimal, dark-modern, creative. Single-file portable output.
  Use when user says "tạo trang web", "tạo html", or "/tao-html".
argument-hint: "[content from bien-soan or direct text] [style: corporate|academic|minimal|dark-modern|creative]"
---

# Tạo HTML — Static HTML Page Output Skill

Generates self-contained `.html` files with inline CSS for maximum portability.

```yaml
MODE: Interactive (asks style) or Pipeline (from tong-hop)
LANGUAGE: Copilot responds in Vietnamese
INPUT: Structured Markdown from bien-soan or user text
OUTPUT: Single .html file with all CSS inline
LIBRARY: jinja2
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
- Does NOT include JavaScript interactivity
- Does NOT host or deploy the HTML file
- Does NOT synthesize content — that is bien-soan job
- Does NOT install dependencies — redirects to /cai-dat
