---
name: gen-html
description: |
  Create professional static HTML pages OR reveal.js browser presentations from synthesized content.
  Two modes: "page" (static page with inline CSS) and "presentation" (reveal.js slides).
  8 styles with light/dark variants, transitions, fragment animations, code syntax highlighting.
  Note: presentation mode requires internet connection for reveal.js CDN.
  Always use this skill when the user wants a webpage, HTML report, or browser-based presentation
  — even casual requests like "tạo trang web", "làm slide trình chiếu trong trình duyệt",
  "xuất HTML", or "tạo cái gì đó mở được bằng Chrome" — even without saying "/tao-html".
argument-hint: "[content] [style: corporate|academic|minimal|dark-modern|creative|warm-earth|dark-neon|dark-elegant] [mode: page|presentation]"
version: 1.1
compatibility:
  requires:
    - Python >= 3.10
    - jinja2 >= 3.1.0 (page mode)
  optional:
    - Internet connection (presentation mode uses reveal.js CDN)
  tools:
    - run_in_terminal
---

# Tạo HTML — Static HTML Page & Presentation Output Skill

**References:** `references/presentation-styles.md` | `references/template-styles.md` | `references/speaker-notes-pdf.md`

Two output modes:
- **page**: Self-contained static HTML with inline CSS (jinja2). No JavaScript, no external
  dependencies — the file works offline and can be emailed as-is.
- **presentation**: reveal.js slide deck via `scripts/gen_reveal.py`. Requires internet on
  first load for CDN resources.

Mode detection: keywords like "slide html", "html presentation", "reveal.js" trigger
presentation mode; everything else defaults to page mode.

All responses to the user are in Vietnamese.

---

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

### Thin Content Guard (STRICT — reject and loop back)

HTML pages are often shared via link or email. A thin page with mostly whitespace and generic
text looks unprofessional and reflects poorly on the user.

**Automatic rejection criteria (when called from pipeline):**
- **< 800 words** for a multi-section page: REJECT. Signal back to tong-hop:
  "❌ Content quá mỏng ({word_count} từ) cho trang HTML. Cần biên soạn lại ở mức comprehensive."
- **Sections without substance**: If more than 30% of sections have only 1-2 sentences, REJECT.
- **Presentation mode with < 300 words**: REJECT — slides will be nearly empty.

**When called standalone:** warn the user and suggest enrichment.

### Step 2: Parse Content & Generate HTML

Before converting, analyze the content to make UX-aware decisions. HTML has more layout
flexibility than Word or PDF — use that advantage to create a reading experience, not just
a formatted text dump.

**Content-Aware Layout Decisions:**

1. **Navigation needs**: if the document has 5+ sections, add a sticky table of contents
   sidebar (or top nav) so readers can jump between sections. For shorter documents, skip
   the nav — it would be overhead.

2. **Content type → HTML treatment:**
   | Content pattern | Standard HTML | Intelligent HTML |
   |---|---|---|
   | Key finding | `<p>` | `<aside class="callout">` with accent border |
   | Comparison data | `<table>` | Responsive table + highlight best/worst cells |
   | Statistics | Inline text | `<div class="metric-card">` with large number + label |
   | Step-by-step | `<ol>` | Timeline layout with visual step indicators |
   | Long content (5000+ words) | Continuous scroll | Add "back to top" button + progress bar |
   | Code snippets | `<pre>` | Syntax-highlighted `<pre>` with copy button |

3. **Responsive intelligence**: the HTML file might be viewed on a phone, tablet, or
   desktop. Use responsive breakpoints:
   - Tables with 5+ columns → horizontally scrollable on mobile (`overflow-x: auto`)
   - Two-column layouts → stack to single column on narrow screens
   - Large images → `max-width: 100%` with aspect ratio preserved

4. **Reading comfort**: optimize for sustained reading:
   - Line length: 60-80 characters per line (use `max-width: 70ch` on text containers)
   - Font size: 16-18px body text (not the default 14px which is too small for reading)
   - Line height: 1.6-1.8 for body text
   - Adequate paragraph spacing

**Convert Markdown → HTML elements:**

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

1. Write UTF-8 file; verify: file exists, contains `<!DOCTYPE html>`, `<meta charset="UTF-8">`
2. **READ BACK (mandatory)**: `read_file` the HTML → verify all sections present, content not empty,
   styles applied. For presentation mode: verify slide count matches plan. If broken → re-generate.
3. Report: "✅ File HTML: {path} ({size}) | Style: {style} | {section_count} phần | Verified ✓"

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
python3 .github/skills/gen-html/scripts/gen_reveal.py --input data.json --output out.html --style corporate
python3 gen_reveal.py --input data.json --output out.html --style dark-neon --transition zoom --no-fragments
```

For transitions, custom backgrounds, speaker notes, PDF export:
→ See `references/presentation-styles.md`

---

## Error Handling

Common issues and fixes:
- **Template error**: check Jinja2 syntax; escape special characters in user content
- **Encoding error**: ensure UTF-8 in both the meta tag and the Python file write call
- **Image embed error**: skip the image on base64 failure; add alt text placeholder so the
  document still makes sense without the image
- **Large output**: warn if HTML > 5MB (many embedded images); suggest external image files

---

## Accessibility

HTML output should be usable by everyone, including people using screen readers or who have
visual impairments. These practices don't add much effort but significantly improve usability:

1. **Semantic HTML**: use `<h1>` through `<h6>` in order (no skipping levels), `<nav>`,
   `<main>`, `<article>`, `<section>` where appropriate. Screen readers use heading hierarchy
   to navigate.
2. **Alt text for images**: every `<img>` tag needs a descriptive `alt` attribute. For charts,
   describe what the chart shows (e.g., "Bar chart showing Q4 revenue by region").
3. **Color contrast**: ensure text-to-background contrast ratio ≥ 4.5:1 (WCAG AA). The
   built-in styles already meet this — be careful when users request custom colors.
4. **Keyboard navigation**: for presentation mode, reveal.js handles this natively. For static
   pages, ensure links and interactive elements are reachable via Tab key.
5. **Language attribute**: set `<html lang="vi">` for Vietnamese content, `lang="en"` for
   English. This helps screen readers pronounce text correctly.

---

## Examples

**Example 1 — Static report page:**
Input: Synthesized content, 5 sections, corporate style
Output: Self-contained .html, inline CSS, no JS, works offline, portable, 25 KB

**Example 2 — Browser presentation:**
Input: Slide content, 12 sections, dark-neon style
Output: reveal.js .html, 18 slides, fragment animations, keyboard navigation, 35 KB

**Example 3 — Academic page with charts:**
Input: Research content + base64 chart images from tao-hinh
Output: academic .html, embedded charts, semantic headings, print-friendly, 80 KB

---

## Step 5: Shared Auditor Agent Call (Post-Generation)

```yaml
AUDITOR_GATE:
  when: After HTML generation and verification
  how:
    1. READ .github/skills/shared-agents/auditor.md
    2. BUILD prompt with:
       user_request: original user request
       output_content: HTML content (read the .html file)
       output_format: "html"
       required_fields: sections/topics user asked for
    3. CALL runSubagent(prompt=<built_prompt>, description="Audit HTML output")
    4. PARSE response:
       IF VERDICT == PASS → deliver to user
       IF VERDICT == FAIL → re-generate with IMPROVEMENTS guidance (max 2 retries)
  budget: Counts toward max 5 auditor calls per pipeline run
  skip_when: Standalone quick generation
```

---

## What This Skill Does NOT Do

- Does NOT create multi-page websites (single .html file only)
- Does NOT synthesize content — that is bien-soan
- Does NOT install dependencies — redirects to /cai-dat
- Presentation mode requires internet on first load (CDN for reveal.js)
