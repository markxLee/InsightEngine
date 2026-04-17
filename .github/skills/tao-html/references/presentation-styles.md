# Presentation Styles & Transitions — Full Reference (US-4.2.1, 4.2.2, 4.2.3)

## 8 Presentation Styles

```yaml
LIGHT_STYLES:
  corporate:
    reveal_theme: white
    background: "#ffffff"
    heading: "#1a365d"
    accent: "#3182ce"
    fonts: "Segoe UI / Segoe UI"
    use_for: Business reports, formal docs

  academic:
    reveal_theme: simple
    background: "#fafafa"
    heading: "#1a202c"
    accent: "#744210"
    fonts: "Georgia / Georgia"
    use_for: Research papers, journals

  minimal:
    reveal_theme: white
    background: "#ffffff"
    heading: "#111827"
    accent: "#059669"
    fonts: "Inter / Inter"
    use_for: Clean/simple docs, product demos

  creative:
    reveal_theme: moon
    background: "#fffbeb"
    heading: "#8b5cf6"
    accent: "#f59e0b"
    fonts: "Poppins / Open Sans"
    use_for: Marketing, events, creative

  warm-earth:
    reveal_theme: simple
    background: "#fdf8f3"
    heading: "#92400e"
    accent: "#b45309"
    fonts: "Playfair Display / Source Sans Pro"
    use_for: Nature, organic, community

DARK_STYLES:
  dark-modern:
    reveal_theme: night
    background: "#0f172a"
    heading: "#6366f1"
    accent: "#22d3ee"
    fonts: "Inter / Inter"
    use_for: Tech, startup, engineering

  dark-neon:
    reveal_theme: night
    background: "#0a0a0a"
    heading: "#00ffc8"
    accent: "#ff3cac"
    fonts: "JetBrains Mono / Inter"
    use_for: Gaming, hackathons, bold tech

  dark-elegant:
    reveal_theme: night
    background: "#1a1a2e"
    heading: "#e0a458"
    accent: "#e0a458"
    fonts: "Playfair Display / Lato"
    use_for: Premium, luxury, gala events

STYLE_DETECTION:
  formal/business → corporate
  research/paper → academic
  clean/simple → minimal
  marketing/fun → creative
  nature/organic → warm-earth
  tech/modern → dark-modern
  gaming/bold → dark-neon
  luxury/premium → dark-elegant
```

---

## Transitions (US-4.2.2)

```yaml
TRANSITION_TYPES:
  none:     Instant switch (no animation)
  slide:    Horizontal slide (corporate default)
  fade:     Crossfade (academic, dark-modern default)
  convex:   3D convex rotation (warm-earth default)
  concave:  3D concave rotation (dark-elegant default)
  zoom:     Zoom in/out (creative, dark-neon default)

STYLE_DEFAULTS:
  corporate: slide  |  academic: fade  |  minimal: none  |  creative: zoom
  warm-earth: convex  |  dark-modern: fade  |  dark-neon: zoom  |  dark-elegant: concave

PRIORITY: CLI --transition flag > JSON "transition" key > style default > "slide"

PER_SLIDE: Add "transition" key to individual slide JSON object

FRAGMENTS:
  default: true (bullets appear one-by-one on arrow/space)
  disable: --no-fragments CLI flag OR "fragments": false in JSON

CLI_EXAMPLES: |
  python3 gen_reveal.py --input data.json --output out.html --style corporate --transition fade
  python3 gen_reveal.py --input data.json --output out.html --style dark-neon --no-fragments
```

---

## Custom Backgrounds (US-4.2.3)

```yaml
BACKGROUND_TYPES:
  solid:    {"background": "#1a365d"}
  gradient: {"background": {"gradient": "linear-gradient(135deg, #667eea, #764ba2)"}}
  image:    {"background": {"image": "https://example.com/bg.jpg", "opacity": 0.3}}
  local:    {"background": {"image": "/path/to/bg.png", "size": "cover"}}
  video:    {"background": {"video": "https://example.com/bg.mp4", "opacity": 0.5}}

OPTIONS:
  opacity: 0.0-1.0  |  size: cover|contain  |  position: center|top|bottom

GLOBAL: Use --background CLI flag
PER_SLIDE: Add "background" key to slide JSON object
```

---

## Speaker Notes & PDF Export (US-4.5.2)

```yaml
SPEAKER_NOTES:
  how: Add "notes" key to any slide JSON object
  view: Press "S" in browser to open Speaker View
  example: '{"type": "content", "title": "...", "bullets": [...], "notes": "Talking points..."}'
  auto_generate: bien-soan generates notes when tong-hop sets include_notes: true

PDF_EXPORT:
  with_notes:    python3 gen_reveal.py --input data.json --output slides.html --print-notes
  without_notes: python3 gen_reveal.py --input data.json --output slides.html
  then: Open HTML in browser → Ctrl+P → Save as PDF
```

---

## reveal.js CDN Config

```yaml
REVEALJS:
  version: "5.1.0"
  base_url: "https://cdn.jsdelivr.net/npm/reveal.js@5.1.0"
  plugins: RevealNotes, RevealHighlight
  keyboard:
    arrows/space: Navigate  |  escape: Overview  |  f: Fullscreen  |  s: Speaker notes
```
