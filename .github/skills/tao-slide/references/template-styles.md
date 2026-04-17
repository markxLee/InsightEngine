# Template Style Specs — Full Reference

## corporate-blue

```yaml
fonts: {heading: "Arial Black", body: "Arial"}
colors:
  primary: "1F4E79"    # No # prefix in pptxgenjs!
  accent:  "E74C3C"
  bg:      "FFFFFF"
  text_dark: "2C3E50"
  text_light: "FFFFFF"
visual_elements:
  - Accent bar (left side, 0.3" width, primary color)
  - Section dividers with full-color background
  - Icon placeholders for bullet points
  - Bottom stripe with company branding area
```

## corporate-red

```yaml
fonts: {heading: "Arial Black", body: "Calibri"}
colors:
  primary: "C0392B"
  accent:  "1F4E79"
  bg:      "FFFFFF"
  text_dark: "2C3E50"
  text_light: "FFFFFF"
visual_elements: Bold red header bars, executive layout
```

## academic-serif

```yaml
fonts: {heading: "Georgia", body: "Calibri"}
colors:
  primary: "2C3E50"
  accent:  "2980B9"
  bg:      "FFFFFF"
  text_dark: "2C3E50"
  text_light: "FFFFFF"
visual_elements:
  - Thin top/bottom rules
  - Section numbers (1.0, 2.0, etc.)
  - Subtle background shapes (light circles)
  - Footnote area on content slides
```

## minimal-white

```yaml
fonts: {heading: "Helvetica Neue", body: "Helvetica Neue"}
colors:
  primary: "1A1A1A"
  accent:  "999999"
  bg:      "FAFAFA"
  text_dark: "1A1A1A"
  text_light: "FFFFFF"
visual_elements:
  - Large whitespace margins
  - Single accent line (thin, bottom)
  - Oversized numbers for data highlights
```

## minimal-gray

```yaml
fonts: {heading: "Helvetica Neue", body: "Helvetica Neue"}
colors:
  primary: "374151"
  accent:  "6B7280"
  bg:      "F3F4F6"
  text_dark: "111827"
  text_light: "FFFFFF"
visual_elements: Soft gray header bars, minimal decoration
```

## dark-gradient

```yaml
fonts: {heading: "Inter", body: "Inter"}
colors:
  primary: "6366F1"
  accent:  "22D3EE"
  bg:      "0F172A"
  text_dark: "0F172A"
  text_light: "F1F5F9"
visual_elements:
  - Dark slate background
  - Gradient accent bars (indigo → cyan)
  - Glow effects on key metrics (drop shadow)
  - Monospace font for code/data snippets
  - Thin neon accent lines as dividers
```

## dark-neon

```yaml
fonts: {heading: "Inter", body: "Inter"}
colors:
  primary: "00FFC8"
  accent:  "FF3CAC"
  bg:      "0A0A0A"
  text_dark: "0A0A0A"
  text_light: "E0E0E0"
visual_elements: Neon glow effects, bold high-contrast accents
```

## creative-gradient

```yaml
fonts: {heading: "Poppins", body: "Open Sans"}
colors:
  primary: "8B5CF6"
  accent:  "F59E0B"
  bg:      "FFFBEB"
  text_dark: "1E1B4B"
  text_light: "FFFFFF"
visual_elements:
  - Warm gradient backgrounds
  - Rounded blob shapes as decorative elements
  - Asymmetric layouts (text left, visual right)
  - Bold color blocks for callouts
```

## creative-warm

```yaml
fonts: {heading: "Poppins", body: "Open Sans"}
colors:
  primary: "B45309"
  accent:  "92400E"
  bg:      "FDF8F3"
  text_dark: "1C1917"
  text_light: "FFFFFF"
visual_elements: Earthy warm tones, organic shapes
```

## tech-modern

```yaml
fonts: {heading: "Inter", body: "Inter"}
colors:
  primary: "0D9488"
  accent:  "3B82F6"
  bg:      "F8FAFC"
  text_dark: "0F172A"
  text_light: "FFFFFF"
visual_elements: Modern teal/blue gradient bars, clean geometric shapes
```

---

## CRITICAL pptxgenjs Rules

```yaml
RULES:
  colors:
    - NEVER use # prefix: use "FF5733" not "#FF5733"
    - pptxgenjs silently fails/corrupts colors with # prefix

  layout:
    - Always set: layout: "LAYOUT_WIDE" (16:9)

  visual_requirement:
    - EVERY slide MUST have at least one visual element
    - Options: shape, icon placeholder, accent bar, background gradient
    - No text-only slides allowed

  text_overflow:
    - Max 6 bullet points per slide
    - Max 8 words per bullet line
    - Split into multiple slides if exceeded

  page_numbers:
    - Define in defineSlideMaster
    - Skip on title slide
```

---

## Script Template Skeleton

```javascript
const pptxgen = require("pptxgenjs");
const fs = require("fs");

function createPresentation(data, outputPath) {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE"; // 16:9

  pres.defineSlideMaster({
    title: "MAIN",
    background: { color: "FFFFFF" },
    objects: [
      // Accent bar, footer, page number placeholder
    ]
  });

  data.slides.forEach(s => {
    const slide = pres.addSlide({ masterName: "MAIN" });
    // render by s.type: title | section | content | table | image | quote | closing
    if (s.notes) slide.addNotes(s.notes);
  });

  pres.writeFile({ fileName: outputPath })
    .then(() => {
      const stats = fs.statSync(outputPath);
      console.log(`✅ Saved: ${outputPath} (${(stats.size/1024).toFixed(1)} KB)`);
    });
}

const args = process.argv.slice(2);
const inputPath = args[args.indexOf('--input') + 1];
const outputPath = args[args.indexOf('--output') + 1];
const data = JSON.parse(fs.readFileSync(inputPath, 'utf8'));
createPresentation(data, outputPath);
```
