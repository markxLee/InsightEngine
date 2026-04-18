---
name: design
description: |
  Create professional visual designs programmatically — cover pages, posters, certificates,
  infographic layouts, title pages, invitations, and artistic compositions. Uses reportlab Canvas
  and Pillow to draw shapes, typography, and patterns directly in code, with 80+ bundled fonts.
  Output: PNG or PDF.
  Always use this skill when the user wants a designed visual composition with typography,
  layout, and artistic intent — "tạo poster", "thiết kế bìa", "làm certificate", "tạo thiệp",
  "thiết kế cover page", "tạo bằng khen", "tạo banner", "design a poster", "make a cover",
  "tạo infographic", "tạo hình bìa báo cáo" — even without saying "design".
  Do NOT use for data charts (use tao-hinh) or AI-generated illustrations (use tao-hinh image mode).
argument-hint: "[type: poster|cover|certificate|infographic|invitation|banner|artistic] [style hints]"
version: 1.1
compatibility:
  requires:
    - Python >= 3.10
    - reportlab >= 4.1.0
    - Pillow (for PNG output)
  assets:
    - canvas-fonts/ (80+ TTF files with OFL licenses)
  tools:
    - run_in_terminal
license: Apache-2.0 (see LICENSE.txt). Fonts under SIL OFL (see canvas-fonts/*.txt).
---

# Thiết Kế — Programmatic Visual Design

**References:** `references/design-principles.md`
**Bundled fonts:** `canvas-fonts/` (80+ TTF files with OFL licenses)

This skill creates visual compositions by writing Python code that draws directly onto a canvas
(reportlab Canvas for PDF, Pillow for PNG). The difference from tao-hinh is fundamental:
tao-hinh generates **data charts** and **AI images**, while thiet-ke creates **designed layouts**
where typography, shapes, color, and whitespace work together as a deliberate composition. Think
of it as the difference between a bar chart and a poster — one visualizes data, the other
communicates through design.

All responses to the user are in Vietnamese.

---

## Bundled Template Scripts

For common design types, use the bundled scripts as a starting point. They handle font
registration, layout structure, and color palettes — you only need to customize content:

```yaml
SCRIPTS:
  gen_poster.py:
    purpose: Event poster (A3/A4)
    styles: modern | classic | bold
    usage: python3 .github/skills/design/scripts/gen_poster.py --title "Event" --style modern --output poster.pdf
    input: --title, --subtitle, --body, --footer, or --input data.json

  gen_certificate.py:
    purpose: Certificate / bằng khen (A4 landscape)
    styles: formal | modern | elegant
    usage: python3 .github/skills/design/scripts/gen_certificate.py --name "Nguyễn Văn A" --title "Chứng Nhận" --output cert.pdf
    input: --name, --title, --course, --date, --issuer, or --input data.json

  gen_cover.py:
    purpose: Report cover page (A4)
    styles: corporate | academic | creative
    usage: python3 .github/skills/design/scripts/gen_cover.py --title "Annual Report" --author "Team" --output cover.pdf
    input: --title, --subtitle, --author, --date, or --input data.json
```

For designs that don't fit these templates (infographics, invitations, custom artistic
compositions), write a custom script following Steps 1-4 below. The templates serve as
code references for font registration, color handling, and layout patterns.

---

## When to Use This Skill (vs tao-hinh)

| User wants | Skill | Why |
|---|---|---|
| Bar/line/pie chart from data | tao-hinh | Data-driven, matplotlib |
| AI-generated illustration | tao-hinh | Needs diffusers/SD-Turbo |
| Report cover page | **thiet-ke** | Typography + layout composition |
| Event poster | **thiet-ke** | Artistic design with text hierarchy |
| Certificate / bằng khen | **thiet-ke** | Formal layout with decorative elements |
| Infographic layout | **thiet-ke** | Structured information design |
| Invitation / thiệp | **thiet-ke** | Decorative composition |
| Abstract art piece | **thiet-ke** | Creative shapes + typography |

---

## Step 1: Design Philosophy

Before drawing, establish the visual direction. This is not a template — it is an aesthetic
framework that guides every decision (colors, fonts, spacing, shapes).

### Purpose & Audience Analysis (do this first)

Design serves a purpose — and the purpose shapes every visual decision. Before choosing
aesthetics, analyze what the design needs to accomplish:

**1. Communication goal:**
- What is the single most important message? (This becomes the visual focal point)
- What emotion should it evoke? (Authority, excitement, warmth, urgency, celebration)
- What action should the viewer take? (Attend event, feel recognized, read report)

**2. Audience:**
- Corporate executives → clean, restrained, serif fonts, muted palette
- Young/creative audience → bold colors, modern sans-serif, dynamic composition
- Academic/formal → traditional layout, serif typography, structured grid
- General public → high contrast, large text, immediately clear message

**3. Context of use:**
- Will it be printed? → CMYK-safe colors, high DPI, check readability at print size
- Digital display? → RGB is fine, consider screen sizes
- Large format (poster)? → Test readability at 3m distance — title should be readable
- Small format (card/badge)? → Simplify, fewer elements, larger relative text

**4. Content hierarchy:**
Rank every piece of text by importance (1 = most important):
- Rank 1: Main title or name → largest, most prominent
- Rank 2: Key supporting info (date, subtitle) → medium, clear
- Rank 3: Details (organization, location, fine print) → smallest, but still readable
- Don't give everything equal visual weight — that creates visual noise, not design

Report the analysis:
```
🎨 Phân tích thiết kế:
- Mục tiêu: {communication_goal}
- Cảm xúc: {target_emotion}
- Đối tượng: {audience_type}
- Sử dụng: {usage_context}
- Focal point: {main_message}
```

### Aesthetic Direction

**Name the aesthetic** (1–2 words): e.g., "Concrete Poetry", "Chromatic Silence", "Metabolist Dreams"

**Articulate the philosophy** (3–4 paragraphs) covering:
- Space and form — how elements occupy the canvas
- Color and material — palette, texture, visual weight
- Typography — font choices, scale, role of text (accent vs content)
- Composition — rhythm, balance, visual hierarchy

The philosophy should feel like a manifesto for an art movement. Keep it generic enough to
adapt to the specific piece, but specific enough to actually constrain choices. Save it as
`tmp/design_philosophy.md` for reference.

### Philosophy Examples (condensed)

**"Concrete Poetry"** — Monumental form, bold geometry. Massive color blocks, sculptural
typography, Brutalist spatial divisions. Text as rare, powerful gesture — only essential
words integrated into the visual architecture.

**"Chromatic Language"** — Color as primary information system. Geometric precision where
color zones create meaning. Minimal typography — small sans-serif labels letting chromatic
fields communicate. Josef Albers meets data visualization.

**"Geometric Silence"** — Pure order and restraint. Grid-based precision, dramatic negative
space. Swiss formalism meets Brutalist material honesty. Structure communicates, not words.

---

## Step 2: Choose Tools and Canvas

**PDF output** (vector, crisp at any zoom):
```python
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm, cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
```

**PNG output** (raster, web-friendly):
```python
from PIL import Image, ImageDraw, ImageFont
```

Canvas dimensions:
- A4 portrait: 210×297mm (PDF) or 2480×3508px at 300dpi (PNG)
- A4 landscape: 297×210mm or 3508×2480px
- Poster: 1920×2560px (PNG) or custom
- 16:9 slide cover: 1920×1080px (PNG)
- Square social: 1080×1080px (PNG)

Register fonts from `canvas-fonts/` directory:
```python
font_dir = ".github/skills/design/canvas-fonts"
pdfmetrics.registerFont(TTFont('WorkSans', f'{font_dir}/WorkSans-Regular.ttf'))
pdfmetrics.registerFont(TTFont('WorkSans-Bold', f'{font_dir}/WorkSans-Bold.ttf'))
```

---

## Step 3: Create the Composition

Write a Python script that draws the design. The script should be self-contained and saved
to `tmp/gen_design.py`. Run it via:
```bash
python3 tmp/gen_design.py --output output/design.pdf --title "Your Title"
```

### Composition Principles

**Typography is art, not just text.** Use different fonts at dramatically different scales.
A single huge word can anchor the composition while tiny labels provide context. Browse the
80+ fonts in `canvas-fonts/` — each has a distinct personality:
- **Serif display**: YoungSerif, Gloock, LibreBaskerville, CrimsonPro
- **Sans modern**: WorkSans, Outfit, InstrumentSans, BricolageGrotesque
- **Mono/tech**: GeistMono, JetBrainsMono, IBMPlexMono, DMMono, RedHatMono
- **Display/art**: Boldonse, EricaOne, PoiretOne, NationalPark, Silkscreen, PixelifySans
- **Elegant**: Italiana, Lora, InstrumentSerif, IBMPlexSerif, Jura
- **Handwritten**: NothingYouCouldDo, ArsenalSC

**Shapes and patterns build rhythm.** Repeating geometric elements (circles, lines, grids)
create visual texture. Use them intentionally, not decoratively.

**Color palette is limited and intentional.** Pick 3–5 colors max. Let one dominate, one
accent, rest neutral. Use hex colors in reportlab: `canvas.setFillColor(HexColor('#2D3436'))`.

**Whitespace is a design element.** Empty space creates breathing room and draws attention
to what is present. Do not fill every corner.

**Nothing overlaps unintentionally.** Check that all text and shapes have clear separation.
Every element should be within canvas boundaries with proper margins.

---

## Step 4: Refine

After the first render, take a critical pass:
- Does the composition feel cohesive or cluttered?
- Is the typography hierarchy clear (what reads first, second, third)?
- Are colors harmonious and intentional?
- Is there enough whitespace?
- Does it look like a professional designer made it?

Refine the code — adjust spacing, font sizes, colors, element positions. Do not add more
elements; instead make existing ones work better together.

---

## Step 5: Verify & Report

1. Confirm output file exists and size is reasonable (PDF > 5KB, PNG > 50KB)
2. Report: `✅ Thiết kế hoàn tất: {path} ({size})`
3. If called from tong-hop pipeline, return `{path, type, width, height}` to the caller

---

## Multi-Page Option

When the user requests multiple pages (e.g., a full booklet or card set), create each page
as a variation on the same design philosophy — same palette and typography family but distinct
compositions. Bundle them in a single PDF. Each page should feel like part of a cohesive series.

---

## Examples

**Example 1 — Report cover page:**
Input: "Thiết kế bìa báo cáo 'Annual Report 2026' cho Team Analytics"
Output: `gen_cover.py --title "Annual Report 2026" --author "Team Analytics" --style corporate` → cover.pdf (A4, 25 KB)

**Example 2 — Event poster:**
Input: "Tạo poster cho workshop AI, ngày 15/5, phong cách modern"
Output: `gen_poster.py --title "AI Workshop" --subtitle "May 15, 2026" --style modern` → poster.pdf (A3, 35 KB)

**Example 3 — Certificate:**
Input: "Làm bằng khen cho Nguyễn Văn A hoàn thành khóa Data Science"
Output: `gen_certificate.py --name "Nguyễn Văn A" --course "Data Science" --style formal` → cert.pdf (A4 landscape, 20 KB)

**Example 4 — Custom infographic (no template):**
Input: "Tạo infographic layout cho 5 bước quy trình tuyển dụng"
Output: Custom script `tmp/gen_design.py` → infographic.pdf (A4, 45 KB), follows Steps 1-4

---

## What This Skill Does NOT Do

- Does NOT create data-driven charts — use tao-hinh (matplotlib)
- Does NOT generate AI images from prompts — use tao-hinh (diffusers/torch)
- Does NOT create interactive or animated content — use tao-html
- Does NOT install dependencies — redirects to setup
- Does NOT copy existing artists' work — all designs are original compositions