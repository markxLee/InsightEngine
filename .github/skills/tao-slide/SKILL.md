---
name: tao-slide
description: |
  Create professional PowerPoint (.pptx) presentations from synthesized content.
  Supports 5 template styles: corporate, academic, minimal, dark-modern, creative.
  Uses pptxgenjs (Node.js). Triggers on "tạo slide", "làm thuyết trình",
  "create powerpoint", or "/tao-slide".
argument-hint: "[content from bien-soan or direct text] [style: corporate|academic|minimal|dark-modern|creative]"
---

# Tạo Slide — PowerPoint Output Skill

Generates professionally designed `.pptx` presentations from structured content.

```yaml
MODE: Interactive (asks style) or Pipeline (style from tong-hop)
LANGUAGE: Copilot responds in Vietnamese
INPUT: Structured Markdown from bien-soan or user text
OUTPUT: .pptx file saved to user-specified path
LIBRARY: pptxgenjs (Node.js)
LAYOUT: 16:9 (LAYOUT_WIDE)
```

---

## Trigger Conditions

Use this skill when user:
- Says "tạo slide", "làm thuyết trình", "tạo file powerpoint", "tạo file .pptx"
- Says "create slides", "create powerpoint", "make presentation"
- Uses command `/tao-slide`
- Pipeline (tong-hop) routes content here for PPT output

---

## Pre-Flight Check

```yaml
PRE_FLIGHT:
  1. Check pptxgenjs installed:
     command: node -e "require('pptxgenjs')" 2>&1
     if_fail: "Chạy: npm install -g pptxgenjs"
     
  2. Check content available:
     - From pipeline: content variable from bien-soan
     - From user: raw text or file path
     if_missing: Ask user for content or redirect to thu-thap + bien-soan
     
  3. Determine style:
     - If user specified: use that style
     - If pipeline: use inferred style from tong-hop
     - If neither: ask user to choose (corporate / academic / minimal / dark-modern / creative)
     
  4. Determine output path:
     - If user specified: use that path
     - Default: ./<presentation-title>.pptx in current working directory
```

---

## Step 1: Plan Slide Structure

```yaml
STRUCTURE:
  from_markdown:
    - H1 → Presentation title (title slide)
    - H2 → Section divider slides
    - H3 → Content slide titles
    - Bullet lists → Slide bullet content
    - Tables → Table slides
    - Images → Image slides or embedded visuals
    - Key data → Highlight/callout slides
    
  slide_types:
    title: Opening slide with presentation title + subtitle
    section_divider: Section transition with section name + brief description
    content_bullets: Title + bullet points + visual element
    content_table: Title + formatted table
    content_image: Title + large image + caption
    highlight: Key statistic or quote, large centered text
    closing: Thank you / Q&A / contact info
    
  planning:
    - Map content sections to slide types
    - Ensure variety (no 3+ consecutive bullet slides)
    - Target 1 slide per key point (avoid text-heavy slides)
    - Present plan to user (if interactive):
      format: |
        📊 Kế hoạch slide ({N} slides):
        1. Title: "{title}"
        2. Section: "{section_1}"
        3. Content: "{point_1}" (bullets + icon)
        ...
        
        Bạn muốn điều chỉnh gì không?
```

---

## Step 2: Generate Node.js Script

```yaml
SCRIPT:
  location: scripts/ (ephemeral, generated per task)
  
  CRITICAL_RULES:
    colors:
      - NEVER use # prefix: use "FF5733" not "#FF5733"
      - pptxgenjs silently fails with # prefix
      
    layout:
      - Always set: layout: "LAYOUT_WIDE" (16:9)
      
    visual_requirement:
      - EVERY slide MUST have a visual element
      - Options: shape, icon placeholder, accent bar, background gradient
      - No text-only slides allowed
      
    fonts:
      - Use style-specific font pairings (see references/)
      - Heading font + body font defined per style
      
    text_overflow:
      - Max 6 bullet points per slide
      - Max 8 words per bullet line
      - If content exceeds: split into multiple slides
      
    slide_master:
      - Define master slide with consistent footer/branding
      - Page number on every slide except title
```

---

## Step 3: Apply Style

```yaml
STYLES:
  selection:
    - User chooses: "corporate", "academic", "minimal", "dark-modern", or "creative"
    - Pipeline infers: formal/business → corporate, research → academic, simple → minimal, tech/startup → dark-modern, marketing/event → creative

  corporate:
    description: Bold colors, geometric shapes, business-ready
    reference: references/style-corporate.md
    fonts:
      heading: Arial Black
      body: Arial
    colors:
      primary: "1F4E79"
      accent: "E74C3C"
      bg: "FFFFFF"
      text_dark: "2C3E50"
      text_light: "FFFFFF"
    visual_elements:
      - Accent bar (left side, primary color)
      - Section dividers with full-color background
      - Icon placeholders for bullet points
      - Bottom stripe with company branding area

  academic:
    description: Clean serif, structured, scholarly
    reference: references/style-academic.md
    fonts:
      heading: Georgia
      body: Calibri
    colors:
      primary: "2C3E50"
      accent: "2980B9"
      bg: "FFFFFF"
      text_dark: "2C3E50"
      text_light: "FFFFFF"
    visual_elements:
      - Thin top/bottom rules
      - Section numbers (1.0, 2.0, etc.)
      - Subtle background shapes (light circles)
      - Footnote area on content slides

  minimal:
    description: Maximum whitespace, modern, subtle
    reference: references/style-minimal.md
    fonts:
      heading: Helvetica Neue
      body: Helvetica Neue
    colors:
      primary: "1A1A1A"
      accent: "999999"
      bg: "FAFAFA"
      text_dark: "1A1A1A"
      text_light: "FFFFFF"
    visual_elements:
      - Large whitespace margins
      - Single accent line (thin, bottom)
      - Oversized numbers for data highlights
      - Fade-in image backgrounds (low opacity)

  dark-modern:
    description: Dark background, neon accents, tech/startup vibe
    reference: references/style-dark-modern.md
    fonts:
      heading: Inter
      body: Inter
    colors:
      primary: "6366F1"
      accent: "22D3EE"
      bg: "0F172A"
      text_dark: "0F172A"
      text_light: "F1F5F9"
    visual_elements:
      - Dark slate background (#0F172A)
      - Gradient accent bars (indigo → cyan)
      - Glow effects on key metrics (subtle drop shadow)
      - Monospace font for code/data snippets
      - Rounded corners on shapes (borderRadius)
      - Thin neon accent lines as dividers

  creative:
    description: Vibrant gradients, playful shapes, event/marketing style
    reference: references/style-creative.md
    fonts:
      heading: Poppins
      body: Open Sans
    colors:
      primary: "8B5CF6"
      accent: "F59E0B"
      bg: "FFFBEB"
      text_dark: "1E1B4B"
      text_light: "FFFFFF"
    visual_elements:
      - Warm gradient backgrounds (amber → purple soft)
      - Rounded blob shapes as decorative elements
      - Oversized emoji or icon accents
      - Asymmetric layouts (text left, visual right)
      - Bold color blocks for callouts
      - Playful section transitions (alternating bg colors)
```

---

## Step 4: Execute Script

```yaml
EXECUTE:
  1. Write script to scripts/gen_slide_<timestamp>.js
  2. Run via run_in_terminal:
     command: node scripts/gen_slide_<timestamp>.js
  3. Check exit code:
     - 0: Success → read output path and size
     - Non-zero: Read error → fix script → retry (max 2 retries)
  4. Report to user:
     format: |
       ✅ File PowerPoint đã tạo thành công:
       📄 Đường dẫn: {output_path}
       📏 Kích thước: {file_size}
       🎨 Style: {style_name}
       📊 Số slide: {slide_count}
       🖼️ Layout: 16:9 (widescreen)
```

---

## Step 5: Quality Checks

```yaml
QA:
  automated:
    - File exists and size > 0
    - No Node.js errors in output
    - Slide count matches plan
    
  visual_check:
    - Offer to take screenshot via webapp-testing skill (if available)
    - Or list slide titles for user verification
    
  common_issues:
    colors_with_hash: Remove # prefix from all color values
    text_overflow: Split slides with >6 bullets
    missing_visuals: Add accent shape to any text-only slide
    font_fallback: Use Arial if custom font unavailable
```

---

## Script Template Reference

```javascript
// Template structure — Copilot generates full script based on this
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

function createPresentation(content, style, outputPath) {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE"; // 16:9
  
  // Define master slide
  pres.defineSlideMaster({
    title: "MAIN",
    background: { color: "FFFFFF" },
    objects: [
      // Accent bar, footer, page number...
    ]
  });
  
  // Title slide
  const titleSlide = pres.addSlide();
  titleSlide.addText("Presentation Title", {
    x: 1, y: 2, w: 8, h: 1.5,
    fontSize: 36, bold: true,
    color: "1F4E79", // NO # prefix!
    fontFace: "Arial Black"
  });
  // Visual element (required)
  titleSlide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 0.3, h: 7.5,
    fill: { color: "1F4E79" }
  });
  
  // Content slides...
  
  pres.writeFile({ fileName: outputPath })
    .then(() => {
      const stats = fs.statSync(outputPath);
      console.log(`✅ Saved: ${outputPath} (${stats.size.toLocaleString()} bytes)`);
    });
}

// Parse args and run
const outputPath = process.argv[2] || "presentation.pptx";
const style = process.argv[3] || "corporate";
createPresentation(null, style, outputPath);
```

---

## What This Skill Does NOT Do

- Does NOT read input files — that's thu-thap's job
- Does NOT synthesize content — that's bien-soan's job
- Does NOT generate Word/PDF/HTML — use respective tao-* skills
- Does NOT install dependencies — redirects to /cai-dat
- Does NOT generate chart images — that's tao-hinh's job (can receive chart PNGs as input)
