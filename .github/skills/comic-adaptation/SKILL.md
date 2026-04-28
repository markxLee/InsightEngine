---
name: comic-adaptation
description: |
  Turn stories, folktales, or existing prose into a comic production package. Use when the user
  asks to chuyển thể truyện tranh, create a manga/anime-style adaptation, build character
  prototypes, write a character bible, plan comic pages, storyboard scenes, or keep visual
  continuity across a comic series. Also use when the user wants the workflow to go from
  story analysis → character design → page plan → visual reference sheet for reuse.

  Always use this skill when the user says: "chuyển thể truyện tranh", "vẽ thành manga",
  "tạo character sheet", "nguyên mẫu nhân vật", "thiết kế nhân vật truyện tranh",
  "tạo bảng tham chiếu nhân vật", "storyboard truyện tranh", "page plan", "kế hoạch page",
  "character bible", "giữ nhất quán nhân vật", "vẽ nhân vật", "comic adaptation",
  "manga adaptation", "anime character design" — even if they don't say "comic-adaptation".
version: 4.0
compatibility:
  requires:
    - Python >= 3.10
    - reportlab >= 4.1.0
  optional:
    - torch >= 2.2.0, diffusers >= 0.25.0 (IP-Adapter Face Lock)
    - transformers (CLIPVisionModelWithProjection)
    - Apple Silicon (MPS) or CUDA GPU for AI character generation
    - controlnet_aux (ControlNet preprocessors — v6 multi-pass)
    - kohya_ss or ai-toolkit (LoRA training — v6 custom concepts)
  tools:
    - run_in_terminal
    - read_file
---

# Comic Adaptation — Story-to-Comic Production Pipeline

**Governance:** Read and follow `.github/RULE.md` — it overrides all instructions below.

**References:** `references/anime-archetypes.md`, `references/ip-adapter-face-lock.md`
**Bundled scripts:** `scripts/gen_character_sheet.py`
**Shared assets:** Uses `design` skill's `canvas-fonts/` for typography.
**Changelog:** `CHANGELOG.md` — full development history, failed approaches, lessons learned.

This skill turns a source story into a **production-ready comic adaptation package**.
The difference from a simple summary is fundamental: the goal is not to retell the story
in text, but to prepare every element an artist or an AI illustration pipeline needs to
produce consistent comic pages — cast definitions, visual prototypes, page breakdowns,
and continuity rules.

The skill produces both **planning artifacts** (markdown) and **visual artifacts** (PDF
prototype sheets) in a single workflow. This avoids the pattern where planning lives in
one skill and production lives in another, forcing the user to bridge them manually.

All responses to the user are in Vietnamese.

---

## Step 0: State Read-Back

Call `save_state.py read-context comic-adaptation` as first action. Check `relevant_artifacts[]`
for upstream story content or previously generated character work.

---

## Step 1: Analyze the Source Story

Read the source material. If the user dropped a file, use `gather` to read it. If the user
named a well-known story, work from knowledge.

Extract:

1. **Plot beats** — the key narrative moments in order.
2. **Cast list** — every named or significant character.
3. **Story functions** — what each character DOES in the plot (trigger, obstacle, anchor, etc.).
4. **Cultural identity** — elements that must stay recognizable in the adaptation.

Report to user:

```
📖 Phân tích truyện gốc:
- {N} nhịp chính trong cốt truyện
- {M} nhân vật cần thiết kế
- Bản sắc cần giữ: {cultural_elements}
```

---

## Step 2: Map Characters to Anime Archetypes

Load `references/anime-archetypes.md` and follow the mapping protocol:

1. For each character, match their story function to the closest archetype.
2. Override archetype defaults with story-specific or cultural details.
3. Verify no two characters share the same silhouette + color combo.
4. For characters with multiple states (e.g., child → hero), define shared identity
   first, then state-specific differences.

Output a character bible with these fields per character:

- Name and role
- Anime archetype
- Silhouette and body type
- Eye style (from archetype reference)
- Hair shape and color
- Clothing, props, signature accessories
- Color palette (3–5 hex values)
- Default expression + peak expression
- Signature pose
- Consistency rules (what must NOT change between pages)

Save as `output/<project>/character-bible.md`.

---

## Step 3: Generate Prototype Sheet

This is where the skill produces a real visual artifact instead of just text.

**Prepare the character data JSON:**

Build a JSON file matching the schema expected by `scripts/gen_character_sheet.py`:

```json
{
    "title": "Story Title",
    "subtitle": "Anime adaptation character prototype sheet",
    "characters": [
        {
            "name": "Character Name",
            "role": "Story role",
            "archetype": "shonen_hero",
            "palette": ["#C11F2C", "#E2BF54", "#1F4E8C"],
            "accent": "#E2BF54",
            "skin": "#E7C7A8",
            "hair_color": "#1A1822",
            "eye_style": "hero",
            "hair_shape": "long_flow",
            "notes": ["Visual note 1", "Visual note 2"]
        }
    ]
}
```

**Run the generator:**

```bash
python3 .github/skills/comic-adaptation/scripts/gen_character_sheet.py \
    --input tmp/<project>_characters.json \
    --output output/<project>/character-prototype-sheet.pdf
```

**Verify output:**

- File exists and > 5 KB
- Page count matches ceil(character_count / 6)
- Open with pypdf to confirm it renders

Register artifact:

```bash
python3 scripts/save_state.py register-artifact \
    --step comic-adaptation \
    --path output/<project>/character-prototype-sheet.pdf \
    --type draft_output \
    --summary "Character prototype sheet for <project>" \
    --retention keep
```

---

## Step 4: Build the Page Plan

Translate story beats into pages. For each page define:

| Field | Description |
|-------|-------------|
| Page number | Sequential |
| Goal | What the page accomplishes narratively |
| Characters | Who appears (reference prototype sheet) |
| Key action | The main visual moment |
| Emotional beat | What the reader should feel |
| Composition notes | Camera angle, panel layout suggestions |
| Continuity deps | Which prototype rules apply here |

Structure the page plan to follow a natural comic rhythm:

1. Establish the world (wide establishing shot)
2. Introduce protagonist in their normal state
3. Inciting incident (close-ups, dramatic shift)
4. Montage or escalation (panel rhythm speeds up)
5. Transformation or turning point (splash page or full-bleed)
6. Climax (dynamic action, speed lines, high contrast)
7. Resolution (slow down, wide shots, emotional close)

Save as `output/<project>/page-plan.md`.

---

## Step 5: Self-Review

Before delivery, check:

1. **Story identity preserved** — is the source recognizable?
2. **Cast consistency** — does every character in the page plan match the bible?
3. **Prototype reusability** — could someone use the sheet without reading the bible?
4. **Page rhythm** — does the beat structure feel like a comic, not a list?
5. **No placeholders** — every character has concrete visual specs, not "TBD".
6. **Cultural integrity** — cultural elements are adapted, not erased.

If any check fails, fix it before delivery. Max 2 revision passes per RULE-2.

---

## Step 6: Delivery

Present to user:

```
✅ Bộ chuyển thể truyện tranh hoàn tất:
- 📖 Character Bible: output/<project>/character-bible.md
- 🎨 Prototype Sheet: output/<project>/character-prototype-sheet.pdf
- 📋 Page Plan: output/<project>/page-plan.md

Bước tiếp theo có thể làm:
1. Chuyển từng page thành storyboard chi tiết (4-6 panel mỗi page)
2. Tạo prompt hình ảnh AI cho từng nhân vật hoặc từng page
3. Xuất thành slide hoặc PDF hoàn chỉnh
```

---

## Downstream Handoffs

| Need | Target Skill | How |
|------|-------------|-----|
| Illustrated character art (AI) | `gen-image` | Pass character description + `--style character-anime-male/female` + `--model quality` |
| **Consistent character set (recommended)** | `gen-image` | **IP-Adapter Face Lock** — see protocol v4 below |
| Consistent character set (fallback) | `gen-image` | img2img: canonical view → `--reference` + `--strength 0.55` for other poses |
| Designed reference poster | `design` | Pass character specs, use reportlab Canvas |
| Full comic pages (AI) | `gen-image` | Pass page plan scene descriptions as prompts |
| Presentation of the adaptation | `gen-slide` | Pass page plan + prototype sheet as source |

### Character Image Generation Protocol (v5.0) — IP-Adapter Face Lock

**Reference:** `references/ip-adapter-face-lock.md` for MPS gotchas and troubleshooting.
**Changelog:** `CHANGELOG.md` for full version history and failed approaches to avoid.

The IP-Adapter Face Lock protocol replaces img2img for multi-pose character sets.
It produces **significantly better face consistency** than img2img (`--reference --strength`)
because it injects face identity via cross-attention embeddings, not pixel-level blending.

**Architecture: 2-phase pipeline loading**

IP-Adapter requires `image_embeds` for every generation call once loaded. Therefore the
pipeline MUST be loaded in two phases:

```
Phase A: Load SDXL Base 1.0 (plain, no IP-Adapter)
Phase 0: Generate canonical face via txt2img (front view, bald, clear)
Phase B: Load IP-Adapter Plus Face on top of existing pipeline
Phase 1+: All subsequent images use face-locked generation
```

**Pipeline setup rules (MPS-critical):**

1. Use `StableDiffusionXLPipeline` — NOT `AutoPipelineForText2Image`
2. Keep default `EulerDiscreteScheduler` — DDIMScheduler is 50-100x slower on MPS
3. Image encoder: `h94/IP-Adapter` subfolder `models/image_encoder` (ViT-H, 1280 dim).
   Do NOT use `sdxl_models/image_encoder` (ViT-bigG, 1664 dim) — dimension mismatch.
4. IP-Adapter weights: `ip-adapter-plus-face_sdxl_vit-h.safetensors` from `sdxl_models/`
5. Load IP-Adapter BEFORE `enable_attention_slicing()`. Do NOT re-enable slicing after
   loading — it overwrites `IPAdapterAttnProcessor2_0` and causes `'tuple' has no attribute 'shape'`.
6. MPS NaN-safe sizes only: 1024x768, 768x1024. Square sizes (768x768, 1024x1024) cause NaN.

**IP-Adapter scale tuning by sheet type (v5 tested):**

| Sheet type | IP scale | Rationale |
|------------|:--------:|-----------|
| Face turnaround | 0.7 | Strong face lock — sheet is about the face |
| Face closeup | 0.7 | Strong face lock — detailed face portrait |
| Expression sheet | 0.55 | Medium — face identity but allow expression changes |
| Body turnaround | 0.4 | Lower — let body/anatomy come through |
| Hair reference | 0.45 | Medium-low — face lock + hair detail balance |
| Costume reference | 0.35 | Low — costume needs room to express |
| Accessories reference | 0.3 | Lowest — accessories are the focus, not face |
| Composite (full body) | 0.35 | Low — hair/costume/pose need room to express |

**Canonical face generation:**

```python
# Phase 0 — plain SDXL, no IP-Adapter loaded yet
prompt = (
    "black and white ink lineart, manga style, white background, "
    "character portrait, ((front view)), ((bald)), "
    "<face_identity_description>, "
    "head and shoulders, centered, clean lineart"
)
# Size: 768x1024 (portrait, MPS-safe). Steps: 25-30. Guidance: 7.5-8.0
```

**Face-locked generation:**

```python
# After IP-Adapter loaded + face reference set
pipe.set_ip_adapter_scale(scale)  # per-sheet type
image = pipe(
    prompt=prompt,
    negative_prompt=negative_prompt,
    ip_adapter_image_embeds=face_embeds,  # pre-computed
    width=w, height=h,
    num_inference_steps=25,
    guidance_scale=7.5,
    generator=generator,
).images[0]
```

**Prompt strategy with IP-Adapter:**

IP-Adapter handles face identity — prompts should focus on pose, layout, and costume.
Keep prompts SHORT (≤60 tokens) since CLIP 77-token limit still applies. Put the most
important content (hair, costume) at the START of the prompt after the style prefix.

### Character Image Generation Protocol (v2.0) — img2img fallback

Use this ONLY when IP-Adapter is not available (e.g., no CLIP encoder, disk too small).

1. **ALWAYS specify gender** in the style: `--style character-anime-male` or `--style character-anime-female`.

2. **Use quality model** (auto-selected for character styles).

3. **img2img consistency workflow:**
   ```bash
   # Step 1: Generate canonical front view
   python3 .github/skills/gen-image/scripts/gen_image.py \
     --prompt "<character description>, standing front view, neutral pose" \
     --style character-anime-male --seed 42 --output output/<project>/char_canonical.png

   # Step 2: Verify canonical looks correct before proceeding

   # Step 3: Generate each pose using canonical as reference
   python3 .github/skills/gen-image/scripts/gen_image.py \
     --prompt "<character description>, <pose description>" \
     --style character-anime-male \
     --reference output/<project>/char_canonical.png --strength 0.55 \
     --output output/<project>/char_<pose>.png
   ```

4. **Limitation:** img2img preserves style/color/shape but NOT face identity.
   For comic production requiring consistent faces across pages, use IP-Adapter protocol.

---

## Available Hair Shapes

`short_spike` | `long_flow` | `bun` | `topknot` | `crown` | `helmet` | `ponytail` | `short_neat`

## Available Eye Styles

`wide` (child/innocent) | `hero` (determined) | `warm` (guardian) | `sharp` (authority/messenger) | `slit` (enemy/hidden)

---

## v5 Extended Sheet Set

v5 generates **14 image types** per character (up from 7 in v4.1):

| Phase | Sheet | Size | Steps | IP Scale | Notes |
|-------|-------|------|-------|----------|-------|
| 0 | Canonical face (bald) | 768x1024 | 30 | N/A | Plain SDXL, no IP-Adapter |
| 0 | Canonical with hair | 768x1024 | 30 | N/A | Plain SDXL, no IP-Adapter |
| 1 | Face closeup | 768x1024 | 20 | 0.7 | Detailed face portrait |
| 1 | Face turnaround (horizontal) | 1024x768 | 20 | 0.7 | 5 angles in a row |
| 1 | Face turnaround (vertical) | 768x1024 | 20 | 0.7 | 3 angles stacked |
| 1 | Expression sheet | 1024x768 | 20 | 0.55 | 5 emotions |
| 2 | Body turnaround | 1024x768 | 20 | 0.4 | 4 angles, minimal clothing |
| 3 | Hair reference | 768x1024 | 20 | 0.45 | Hair detail from multiple angles |
| 4 | Costume reference | 768x1024 | 20 | 0.35 | Full outfit detail |
| 5 | Accessories reference | 768x1024 | 20 | 0.3 | Props and accessories |
| 6 | Composite front | 768x1024 | 20 | 0.35 | Full character, front view |
| 6 | Composite three-quarter | 768x1024 | 20 | 0.35 | Full character, 3/4 view |
| 6 | Composite side | 768x1024 | 20 | 0.35 | Full character, side profile |
| 6 | Composite back | 768x1024 | 20 | 0.35 | Full character, back view |

**Script:** `tmp/gen_character_sheet_v5.py` (multi-character CLI with `--character` flag)

### MPS NaN Resilience (v5)

v5 adds **CPU fallback** after MPS NaN seed retries fail:

```
MPS attempt (seed) → NaN? → retry seed+7 → NaN? → retry seed+31 → NaN? → retry seed+97
   ↓ all fail
CPU fallback (seed) → generate on CPU → move pipe back to MPS → continue
```

**Important:** CPU fallback generates differently than MPS (different numerical paths).
The canonical face should ideally succeed on MPS — if CPU fallback activates for canonical,
the face reference will have different characteristics than MPS-generated sheets.

---

## Known Limitations of v5 (Prompt-Only Approach)

These are documented to prevent repeating failed approaches. See `CHANGELOG.md` for full history.

1. **Pose control impossible** — SDXL ignores "side view"/"back view" in most cases. Composites
   for side and back angles render as front views. **Requires ControlNet for v6.**
2. **Custom props not understood** — SDXL has no concept of "ba tieu fan" or culture-specific
   objects. **Requires LoRA training for v6.**
3. **Hair inconsistency** — Twin braids appear in some sheets but bob/ponytail in others.
   IP-Adapter face lock doesn't control hair. **Requires LoRA or stronger prompt engineering.**
4. **Monochrome limitation** — Black/white mode cannot verify color attributes (eye color,
   costume colors, pattern colors). **Need at least 1 color validation pass.**

### Approaches that DON'T work (do NOT retry)

| Approach | Why it fails |
|----------|-------------|
| img2img `--reference --strength` for face consistency | Pixel-level blending, not identity preservation |
| SD-Turbo for character art | 4 steps → blurry faces, guidance=0.0 → no negatives |
| DDIMScheduler on MPS | 50-100x slower than EulerDiscrete |
| Square resolutions on MPS (1024x1024, 768x768) | Always NaN |
| IP-Adapter scale >0.5 for composites | Bald head override — too strong face lock |
| Long prompts (>60 tokens) | CLIP truncation loses critical end details |
| CPU fallback for canonical face | Different generation characteristics than MPS |

---

## v6 Roadmap — Multi-Pass Pipeline + LoRA Training

### 5-Pass Generation Architecture

```
PASS 1 — Layout (rough sketch)
  Input: Stick figure / OpenPose skeleton
  Output: Composition + pose placement on canvas
  Tool: ControlNet OpenPose or Scribble conditioner
  Purpose: Force exact body pose (front/side/back/3-quarter)

PASS 2 — Character Refine (inpaint per character)
  Input: Pass 1 output + character-specific LoRA
  Method: Mask each character region → inpaint with LoRA identity
  Tool: SDXL inpainting pipeline + character LoRA
  Purpose: Apply trained character appearance to rough layout

PASS 3 — Face & Hand Fix (detail correction)
  Input: Pass 2 output
  Method: ADetailer auto-detection or manual mask for face/hands
  Tool: Face inpaint with IP-Adapter face lock + hand LoRA
  Purpose: Fix common SDXL weaknesses (distorted hands, inconsistent faces)

PASS 4 — Background (separate environment)
  Input: Pass 3 output with character region masked
  Method: Inpaint background separately from characters
  Tool: Background LoRA / depth-conditioned generation / manga BG style
  Purpose: Cinematic manga backgrounds without character interference

PASS 5 — Final Lineart & Upscale
  Input: Pass 4 complete image
  Method: Upscale 2-4x + line sharpening + artifact cleanup
  Tool: RealESRGAN / SDXL refinement pass + post-processing
  Purpose: Production-quality output at print resolution
```

### LoRA Training Strategy

**Purpose:** Teach SDXL concepts it doesn't know — custom props, character identities,
cultural elements, and consistent art style.

**Training stack:** `kohya_ss` or `ai-toolkit` for SDXL LoRA fine-tuning

| LoRA Type | Training Images | Steps | Use Case |
|-----------|:--------------:|:-----:|----------|
| Character identity | 10-20 face/body refs | 500-800 | Consistent character across all passes |
| Custom prop | 10-30 object photos/art | 500-1000 | ba tieu fan, jingle bells, cultural items |
| Art style | 20-50 manga pages | 1000-2000 | Consistent lineart style across series |
| Background style | 15-30 manga BGs | 800-1500 | Manga-specific environments |

**Character LoRA workflow:**
1. Generate best canonical images from IP-Adapter pipeline (v5)
2. Curate 10-20 best images as training set (crop, clean, caption)
3. Train SDXL LoRA with character trigger word (e.g., `linh_char`)
4. Use trained LoRA in Pass 2 inpainting for identity injection

**Custom prop LoRA workflow:**
1. Collect 10-30 reference images of the prop (photos, art, sketches)
2. Caption each image with trigger word (e.g., `ba_tieu_fan`)
3. Train prop-specific LoRA (~500 steps, low rank r=8-16)
4. Combine character LoRA + prop LoRA in generation for character holding prop

### ControlNet Models Needed

| Model | Purpose | Priority |
|-------|---------|----------|
| OpenPose | Skeleton → body pose control | HIGH — solves pose accuracy |
| Canny | Edge → preserve lineart structure | MEDIUM — refinement passes |
| Depth | Depth map → perspective backgrounds | MEDIUM — Pass 4 backgrounds |
| Scribble | Rough sketch → guided generation | LOW — optional for Pass 1 |

### Prerequisites Checklist

- [ ] Install ControlNet SDXL models (openpose, canny)
- [ ] Set up LoRA training environment (kohya_ss / ai-toolkit)
- [ ] Create reference image datasets for custom props
- [ ] Create OpenPose skeleton templates for standard character poses
- [ ] Test SDXL inpainting pipeline on MPS
- [ ] Evaluate ADetailer + MPS compatibility
- [ ] Test multi-LoRA loading (character + prop + style simultaneously)
