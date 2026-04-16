---
name: tao-slide
description: |
  Create professional PowerPoint (.pptx) presentations from synthesized content.
  10 templates with light/dark variants. Template preview and auto-selection.
  Uses pptxgenjs (Node.js). Triggers on "tạo slide", "làm thuyết trình",
  "create powerpoint", or "/tao-slide".
argument-hint: "[content] [template: corporate-blue|corporate-red|academic-serif|minimal-white|minimal-gray|dark-gradient|dark-neon|creative-gradient|creative-warm|tech-modern]"
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

## Template Preview and Selection (US-4.1.2)

### Available Templates

When user asks what templates are available, show this table:

```yaml
LIGHT_TEMPLATES:
  corporate-blue:      "Professional navy/blue — business reports, quarterly reviews"
  corporate-red:       "Bold red corporate — executive summaries, annual reports"
  academic-serif:      "Scholarly serif — research papers, lectures, thesis defense"
  minimal-white:       "Clean whitespace — product demos, startup pitches"
  minimal-gray:        "Soft gray tones — internal memos, team updates"
  creative-gradient:   "Purple-amber vibrant — marketing decks, launch events"
  creative-warm:       "Earthy warm tones — non-profit, community events"
  tech-modern:         "Teal/blue modern — product launches, SaaS demos"

DARK_TEMPLATES:
  dark-gradient:       "Indigo/cyan dark — tech conferences, engineering reviews"
  dark-neon:           "Neon cyan/magenta — gaming, hackathons, bold showcases"
```

### Preview Files

Preview .pptx files (7 slides each) at: `references/previews/preview-<template>.pptx`
Regenerate with: `node scripts/gen_previews.js`

### Auto-Selection Logic (AC4)

```yaml
AUTO_SELECT:
  # Copilot picks template based on content type / user context:
  formal_business: corporate-blue
  executive_annual: corporate-red
  research_academic: academic-serif
  simple_brief: minimal-white
  internal_team: minimal-gray
  tech_engineering: dark-gradient
  gaming_bold: dark-neon
  marketing_launch: creative-gradient
  community_wellness: creative-warm
  product_saas: tech-modern

  # Style aliases also work (routed by gen_slide.js):
  corporate → corporate-blue
  academic → academic-serif
  minimal → minimal-white
  dark-modern → dark-gradient
  creative → creative-gradient

SELECTION_WORKFLOW:
  1. If user specifies template name: use it directly
  2. If user specifies style (corporate/academic/etc): use alias mapping
  3. If no preference: auto-detect from content context
  4. Show selected template + brief description to user before generating
  5. User can switch: "dùng template dark-neon thay đi" → re-generate
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
SCRIPT_ARCHITECTURE:
  # US-4.1.3: SKILL.md acts as ROUTER — picks template, prepares JSON, calls script
  # Scripts are in .github/skills/tao-slide/scripts/
  # Each template is a standalone .js file accepting --input JSON --output .pptx
  
  AVAILABLE_TEMPLATES:
    corporate-blue:    Professional blue business style (Arial Black + Arial)
    corporate-red:     Bold red corporate style (Arial Black + Calibri)
    academic-serif:    Clean scholarly style (Georgia + Calibri)
    minimal-white:     Ultra-clean whitespace (Helvetica Neue)
    minimal-gray:      Soft gray tones (Helvetica Neue)
    dark-gradient:     Dark with indigo/cyan accents (Inter)
    dark-neon:         Dark with neon cyan/magenta (Inter)
    creative-gradient: Purple-to-amber vibrant style (Poppins + Open Sans)
    creative-warm:     Warm earthy tones (Poppins + Open Sans)
    tech-modern:       Modern teal/blue tech company (Inter)
  
  STYLE_TO_TEMPLATE_MAPPING:
    corporate: corporate-blue      # default corporate
    academic: academic-serif        # default academic
    minimal: minimal-white          # default minimal
    dark-modern: dark-gradient      # default dark
    creative: creative-gradient     # default creative
    # User can request specific template by name for more variety

  ROUTING_WORKFLOW:
    1. Determine style from user or pipeline
    2. Map style → template name (or use user-specified template)
    3. Prepare content as JSON data file:
       - Save to tmp/<timestamp>_slides.json
       - JSON structure matches slide-utils.js expected format
    4. Run template script:
       command: node .github/skills/tao-slide/scripts/<template>.js --input <json> --output <output.pptx>
    5. Check exit code and output
    6. Report result to user
    7. Clean up tmp JSON file

  JSON_DATA_FORMAT:
    {
      "title": "Presentation Title",
      "slides": [
        {"type": "title", "title": "...", "subtitle": "...", "notes": "Talking point for title slide"},
        {"type": "section", "title": "..."},
        {"type": "content", "title": "...", "bullets": ["...", "..."], "notes": "Expanded talking points here"},
        {"type": "two-column", "title": "...", "left": ["..."], "right": ["..."], "notes": "..."},
        {"type": "image", "title": "...", "image_path": "...", "caption": "..."},
        {"type": "chart", "title": "...", "chart_image": "..."},
        {"type": "table", "title": "...", "headers": ["..."], "rows": [["..."]]},
        {"type": "quote", "text": "...", "author": "..."},
        {"type": "closing", "title": "Cảm ơn!", "subtitle": "Questions?"}
      ]
    }
    # "notes" is optional on any slide type → written as PowerPoint speaker notes
    # View in PowerPoint: View → Notes or Alt+V N
    # bien-soan generates notes automatically when tong-hop sets include_notes: true

SCRIPT:
  location: .github/skills/tao-slide/scripts/
  
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
  1. Prepare JSON data from structured content → save to tmp/<ts>_slides.json
  2. Select template from STYLE_TO_TEMPLATE_MAPPING
  3. Run via run_in_terminal:
     command: node .github/skills/tao-slide/scripts/<template>.js --input <json_path> --output <output_path>
  4. Check exit code:
     - 0: Success → read output path and size
     - Non-zero: Read error → fix data → retry (max 2 retries)
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

## Speaker Notes Support

PowerPoint speaker notes are supported via the `"notes"` field in slide JSON.

```yaml
SPEAKER_NOTES:
  how_it_works:
    - Add "notes" key to any slide object in the JSON data
    - slide-utils.js calls slide.addNotes(s.notes) for each slide that has notes
    - Notes appear in PowerPoint's Notes panel (View → Notes, or Alt+V N)
    
  generation:
    - bien-soan generates notes when tong-hop sets include_notes: true
    - Notes contain expanded talking points, 2-4 sentences per slide
    - Conversational tone, not bullet points
    
  example:
    '{"type": "content", "title": "Q1 Revenue", "bullets": ["Up 15%", "Beat target"], "notes": "Revenue grew 15% YoY. B2B was the strongest driver. Note Q4 was already a record quarter."}'
    
  viewing:
    - PowerPoint desktop: View → Notes
    - Presenter view: Slide Show → Presenter View (shows notes during presentation)
    - Notes pane visible at bottom of normal view

COPILOT_MUST:
  - When tong-hop passes include_notes: true → ensure bien-soan generates notes per slide
  - When user says "thêm ghi chú", "add speaker notes" → set include_notes: true and re-generate
  - Notes field is optional — slides without "notes" key are unaffected
```

---

## What This Skill Does NOT Do

- Does NOT read input files — that's thu-thap's job
- Does NOT synthesize content — that's bien-soan's job
- Does NOT generate Word/PDF/HTML — use respective tao-* skills
- Does NOT install dependencies — redirects to /cai-dat
- Does NOT generate chart images — that's tao-hinh's job (can receive chart PNGs as input)
