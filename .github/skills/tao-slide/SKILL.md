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

**References:** `references/template-styles.md`

```yaml
MODE: Interactive (asks style) or Pipeline (style from tong-hop)
LANGUAGE: Copilot responds in Vietnamese
INPUT: Structured Markdown from bien-soan or user text
OUTPUT: .pptx file (16:9 LAYOUT_WIDE)
LIBRARY: pptxgenjs (Node.js) — NEVER use # prefix for colors!
```

---

## Trigger Conditions

Use this skill when user:
- Says "tạo slide", "làm thuyết trình", "tạo file powerpoint", "tạo file .pptx"
- Says "create slides", "create powerpoint", "make presentation"
- Uses command `/tao-slide`
- Pipeline (tong-hop) routes content here for PPT output

---

## Available Templates

```yaml
LIGHT:
  corporate-blue:    "Professional navy/blue — business reports"
  corporate-red:     "Bold red — executive summaries, annual reports"
  academic-serif:    "Scholarly serif — research, lectures, thesis"
  minimal-white:     "Clean whitespace — product demos, pitches"
  minimal-gray:      "Soft gray — internal memos, team updates"
  creative-gradient: "Purple-amber — marketing, launch events"
  creative-warm:     "Earthy warm — non-profit, community events"
  tech-modern:       "Teal/blue — product launches, SaaS demos"

DARK:
  dark-gradient:     "Indigo/cyan — tech conferences, engineering"
  dark-neon:         "Neon cyan/magenta — gaming, hackathons"

STYLE_ALIASES:
  corporate → corporate-blue  |  academic → academic-serif
  minimal → minimal-white     |  dark-modern → dark-gradient
  creative → creative-gradient
```

Full color/font specs: `references/template-styles.md`

---

## Step 1: Pre-flight Check

1. Check pptxgenjs: `node -e "require('pptxgenjs')"` → if fail: "Chạy: npm install -g pptxgenjs"
2. Confirm content available; if missing: redirect to thu-thap + bien-soan
3. Determine style (user-specified, pipeline-inferred, or ask)
4. Determine output path (default: `./<title>.pptx`)

---

## Step 2: Plan Slide Structure

Map content to slide types:
- H1 → title slide; H2 → section divider; H3 → content slide title
- Bullet lists → content bullets (max 6/slide); Tables → table slide; Images → image slide
- Key data points → highlight/callout slide; Auto-add closing slide "Cảm ơn!"

Present plan to user (interactive):
```
📊 Kế hoạch slide ({N} slides):
1. Title: "{title}"
2. Section: "{section_1}"
3. Content: "{point_1}" (bullets)
...
Bạn muốn điều chỉnh gì không?
```

---

## Step 3: Prepare Data & Run Script

1. Prepare content as JSON → save to `tmp/{timestamp}_slides.json`
2. Select template from STYLE_ALIASES or user-specified name
3. Run script:
   ```
   node .github/skills/tao-slide/scripts/<template>.js --input <json> --output <output.pptx>
   ```
4. JSON format:
   ```json
   {
     "title": "...",
     "slides": [
       {"type": "title", "title": "...", "subtitle": "..."},
       {"type": "section", "title": "..."},
       {"type": "content", "title": "...", "bullets": ["..."], "notes": "Talking points"},
       {"type": "two-column", "title": "...", "left": ["..."], "right": ["..."]},
       {"type": "table", "title": "...", "headers": ["Col1"], "rows": [["a"]]},
       {"type": "image", "title": "...", "image_path": "..."},
       {"type": "quote", "text": "...", "author": "..."},
       {"type": "closing", "title": "Cảm ơn!", "subtitle": "Questions?"}
     ]
   }
   ```
5. Notes field: optional on any slide → written as PowerPoint speaker notes (View → Notes)
6. Auto-generate notes when tong-hop sets `include_notes: true` (bien-soan provides notes)

---

## Step 4: Verify & Report

1. Check exit code; on error: read traceback, fix data, retry (max 2)
2. Clean up tmp JSON file
3. Report:
   ```
   ✅ File PowerPoint đã tạo:
   📄 {output_path}  |  📏 {file_size}  |  🎨 {style}  |  📊 {slide_count} slides
   ```

---

## What This Skill Does NOT Do

- Does NOT read input files — that's thu-thap
- Does NOT synthesize content — that's bien-soan
- Does NOT generate Word/PDF/HTML — use respective tao-* skills
- Does NOT install dependencies — redirects to /cai-dat
- Does NOT generate chart images — that's tao-hinh (receives chart PNGs as input)
