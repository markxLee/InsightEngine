# Design Principles — Programmatic Visual Design

> Core principles for creating professional visual compositions  
> with reportlab Canvas and Pillow.

---

## Visual Hierarchy

```yaml
HIERARCHY_RULES:
  typography_scale:
    # Each heading level should be visually distinct
    title: 36-48pt, bold, primary color
    subtitle: 24-30pt, regular or light, secondary color
    body: 12-14pt, regular, dark gray or black
    caption: 9-10pt, italic, muted color
    
  spacing:
    # Whitespace creates hierarchy — don't cram elements
    title_margin_bottom: 30-50pt
    section_gap: 20-30pt
    paragraph_gap: 10-14pt
    edge_margin: 40-60pt (never less than 30pt)
    
  color_weight:
    # Use accent colors sparingly — 80/20 rule
    base: 80% of surface area (white, light gray, or dark background)
    accent: 20% (brand color, highlights, CTAs)
    text: High contrast against background (WCAG AA minimum)
```

---

## Font Selection Guidelines

```yaml
FONT_PAIRING:
  # Use 2 fonts max per design. 3 fonts = visual chaos.
  heading_font: Bold sans-serif (Montserrat, Raleway, Poppins)
  body_font: Readable serif or sans-serif (Lora, Open Sans, Roboto)
  
  vietnamese_support:
    # Not all bundled fonts support Vietnamese diacritics
    safe_choices:
      - Roboto (full Vietnamese)
      - Open Sans (full Vietnamese)
      - Montserrat (full Vietnamese)
      - Lora (full Vietnamese)
    avoid: Fonts without Unicode Vietnamese block
    
  registration:
    # Always register fonts from canvas-fonts/ directory
    path: .github/skills/thiet-ke/canvas-fonts/
    method: pdfmetrics.registerFont(TTFont('FontName', 'path.ttf'))
```

---

## Design Type Best Practices

```yaml
POSTER:
  layout: Single focal point, top-down visual flow
  contrast: High — title must be readable from 2m distance
  image_area: 40-60% of total surface
  text_area: Keep minimal — poster is visual, not a document
  
COVER_PAGE:
  layout: Centered or asymmetric with strong alignment grid
  elements: Title, subtitle, author/org, date, optional logo
  style: Elegant restraint — less is more on cover pages
  avoid: Clip art, stock borders, excessive decoration
  
CERTIFICATE:
  layout: Formal, centered, landscape A4
  elements: Title, recipient, achievement, date, issuer, signature line
  decorative: Border pattern (thin, elegant), emblem/seal
  font: Formal serif for name, clean sans-serif for body
  
INFOGRAPHIC:
  layout: Vertical flow with clear sections
  data_viz: Icons + numbers > raw text
  sections: 3-5 max (more = overwhelming)
  color_coding: Each section a distinct but harmonious color
  
BANNER:
  layout: Wide format (3:1 or 4:1 ratio)
  focal_point: Left-center (where eyes land first)
  text: Large, bold, 7 words max for primary message
  CTA: If present, contrasting color button/text
```

---

## Color Palette Guidelines

```yaml
PALETTES:
  corporate:
    primary: "#1a365d"  # Deep navy
    accent: "#2b6cb0"   # Professional blue
    highlight: "#ed8936" # Warm orange for emphasis
    background: "#ffffff"
    text: "#2d3748"
    
  modern:
    primary: "#1a1a2e"  # Dark purple-black
    accent: "#e94560"   # Vibrant red-pink
    highlight: "#0f3460" # Deep blue
    background: "#16213e"
    text: "#eaeaea"
    
  warm:
    primary: "#5d4037"  # Warm brown
    accent: "#ff8f00"   # Amber
    highlight: "#4caf50" # Green
    background: "#faf3e0"
    text: "#3e2723"
    
  minimal:
    primary: "#212121"
    accent: "#757575"
    highlight: "#000000"
    background: "#fafafa"
    text: "#424242"
```
