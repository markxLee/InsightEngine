# Comic Adaptation Skill — Changelog

Track development history to avoid repeating past approaches.

---

## v1.0 — Baseline (2026-04-22)
**Approach:** Text-only planning + reportlab PDF prototype sheets
- Character bible (markdown), page plan, prototype sheets (color swatches only)
- No AI image generation — purely planning artifacts
- **Limitation:** No visual output for characters, no consistency mechanism

## v2.0 — img2img Reference (2026-04-24)
**Approach:** SDXL Base 1.0 txt2img + img2img for consistency
- Added `gen_image.py` v2.0 with 3-tier model system (turbo/quality/legacy)
- Canonical front view → img2img `--reference --strength 0.55` for other poses
- Gender-specific presets: `character-anime-male`, `character-anime-female`
- **Results:** Better than v1 but face consistency poor — img2img preserves style/color but NOT face identity
- **Lesson:** img2img pixel-level blending is fundamentally limited for face consistency

### v2 — Thánh Gióng test (2026-04-24)
- Sharper images, better color consistency, some hairstyle/gender consistency
- **Failed:** Face varies per generation, costumes not identical, compositing = pasting (unnatural)
- **Root cause:** txt2img without reference = no face memory between generations

## v3.0 — IP-Adapter Face Lock (2026-04-25)
**Approach:** SDXL + IP-Adapter Plus Face (`ip-adapter-plus-face_sdxl_vit-h`)
- 2-phase pipeline: Phase A (plain SDXL → canonical) → Phase B (IP-Adapter loaded → face-locked)
- CLIP ViT-H image encoder (1280 dim) from `h94/IP-Adapter`
- `gen_character_sheet_v3.py` — 4 sheets (face turnaround, expression, body, costume)
- **Results:** Face consistency dramatically improved vs v2
- **MPS issues discovered:** NaN on square sizes (1024x1024, 768x768), only 768x1024 / 1024x768 safe

### v3 — Critical MPS rules established
- EulerDiscreteScheduler only (DDIM 50-100x slower on MPS)
- Load IP-Adapter BEFORE attention_slicing
- Use `models/image_encoder` (ViT-H) NOT `sdxl_models/image_encoder` (ViT-bigG)
- NaN detection: `np.array(image).max() == 0`

## v4.0 — Scale Tuning (2026-04-25)
**Approach:** IP-Adapter with per-sheet-type scale tuning
- `gen_character_sheet_v4.py` — tuned IP scales per sheet type
- Face turnaround: 0.7, Expression: 0.55, Body: 0.4, Composite: 0.35
- v3 used 0.6 for composites → caused bald head override (too strong face lock)
- **Results:** Better composite quality, hair and costume visible

### v4.1 — Expanded sheets (2026-04-26)
- `gen_character_sheet_v4.1.py` — added expression sheet, with-hair canonical, 20 steps default
- Lower composite scale (0.35) lets hair/costume through
- Thánh Gióng character: 7/7 images OK on MPS, ~35 min total

## v5.0 — Multi-character + Extended Sheet Set (2026-04-28)
**Approach:** Full character sheet pipeline with 14 image types + NaN CPU fallback
- `gen_character_sheet_v5.py` — character definitions in code, CLI-driven
- **New sheet types:** face closeup, hair reference, costume reference, accessories reference, 4 composite angles (front/3-quarter/side/back)
- **CPU fallback:** After 3 MPS NaN seed retries → move pipe to CPU → generate → move back to MPS
- **Character tested:** "Linh" (CHAR-002) — 14/14 images generated, seed 42, ~421 min total

### v5 — Quality assessment (Linh character)
| Criteria | Score | Notes |
|----------|-------|-------|
| Technical quality | 8/10 | Clean manga lineart, no artifacts |
| Face consistency | 7/10 | IP-Adapter works well across sheets |
| Hair accuracy | 5/10 | Twin braids only in some sheets, bob in others |
| Costume accuracy | 6/10 | White dress + green collar visible, skirt pattern missing |
| Pose variety | 5/10 | Side/back composites show front view instead |
| Character identity | 7/10 | Overall recognizable across sheets |

### v5 — Key issues identified
1. **Canonical face not bald** — CPU fallback generated with hair (prompt ignored by CPU)
2. **Pose control impossible with prompt-only** — side/back views default to front
3. **Monochrome-only** — cannot verify color attributes (pink eyes, green collar, skirt pattern)
4. **Custom props (fan) not generated** — SDXL doesn't understand "ba tieu fan"
5. **Twin braids inconsistent** — face turnaround uses bob/ponytail instead

### v5 — Approaches that DON'T work (avoid repeating)
- ❌ img2img for face consistency → pixel blending, not identity preservation
- ❌ SD-Turbo for characters → blurry faces, no negative prompt support
- ❌ DDIMScheduler on MPS → 50-100x slower than Euler
- ❌ Square resolutions on MPS → always NaN (1024x1024, 768x768)
- ❌ High IP-Adapter scale (>0.5) for composites → bald head override
- ❌ Prompt-only pose control → SDXL ignores "side view", "back view" in most cases
- ❌ Long prompts (>60 tokens) → CLIP truncation loses critical details
- ❌ CPU fallback for canonical → different generation characteristics than MPS

---

## v6.0 — ControlNet OpenPose Experiments (2026-04-XX)
**Approach:** ControlNet OpenPose + SDXL for pose control (addresses v5's biggest gap)

### v6.0 — Initial test (ALL NaN)
- `tmp/test_controlnet_v6_old.py` — single seed, no fallback
- Model: `dimitribarbot/controlnet-openpose-sdxl-1.0-safetensors`
- All 4 poses (front/side/back/three_quarter) → NaN on MPS fp16
- No CPU fallback = no usable output

### v6.1 — NaN-resilient diagnostic (CURRENT)
- `tmp/test_controlnet_v6.py` — 3 modes (diagnose, full, cpu-only)
- NaN resilience: 3-seed retry → lower cn_scale → CPU fp32 fallback
- Hand-drawn OpenPose skeletons (Pillow stick figures, 768x1024)

#### v6.1 Diagnostic Results
| Test | Config | Result | Time |
|------|--------|--------|------|
| 1 | MPS fp16 + CN 0.8 | **NaN ❌** | 129s |
| 2 | MPS fp16 + CN 0.5 | **NaN ❌** | 236s |
| 3 | MPS fp16 + CN 0.2 | **NaN ❌** | 217s |
| 4 | MPS fp16 NO ControlNet | **OK ✅** | 194s |
| 5 | CPU fp32 + CN 0.8 | ⏳ running (~3-5min/step) | - |

#### Key Finding
- **ControlNet + MPS fp16 = fundamentally incompatible** (100% NaN at all scales)
- SDXL alone on MPS works fine → ControlNet conditioning is the NaN source
- Root cause: fp16 precision overflow during ControlNet residual addition in UNet
- CPU fp32 expected to work but extremely slow

### v6 — Approaches that DON'T work (avoid repeating)
- ❌ ControlNet + MPS fp16 → 100% NaN at all conditioning scales (0.8, 0.5, 0.2)
- ❌ `diffusers/controlnet-openpose-sdxl-1.0` → private repo (401 error)
- ❌ `r3gm/controlnet-openpose-sdxl-1.0-fp16` → no weight files (404)

### v6 — Architecture: 5-pass generation pipeline (ORIGINAL PLAN)

```
PASS 1 — Layout (rough sketch)
  Input: Stick figure / OpenPose skeleton
  Output: Composition + pose placement
  Tool: ControlNet OpenPose / Scribble

PASS 2 — Character Refine
  Input: Pass 1 output + character LoRA
  Method: Inpaint per character (mask character region)
  Tool: LoRA per character + inpainting pipeline

PASS 3 — Face & Hand Fix
  Input: Pass 2 output
  Method: ADetailer or targeted inpainting for face/hands
  Tool: Face inpaint with IP-Adapter face lock

PASS 4 — Background
  Input: Pass 3 output (character masked out)
  Method: Inpaint background region separately
  Tool: Manga background LoRA / depth-conditioned generation

PASS 5 — Final Lineart & Upscale
  Input: Pass 4 complete image
  Method: Upscale + line sharpening + artifact cleanup
  Tool: RealESRGAN / SDXL upscale + post-processing
```

### LoRA Training for Custom Elements
- **Purpose:** Teach model concepts it doesn't know (ba tieu fan, specific costume patterns, cultural props)
- **Method:** SDXL LoRA fine-tuning (~500-1000 steps, 10-30 reference images)
- **Training stack:** `kohya_ss` or `ai-toolkit` for SDXL LoRA
- **Target concepts:**
  - Character-specific LoRA (face + body + costume as one concept)
  - Prop-specific LoRA (ba tieu fan, jingle bells, specific weapons)
  - Style LoRA (consistent manga lineart style across all passes)

### ControlNet Integration
- **OpenPose:** Skeleton → force exact body pose (front/side/back/3-quarter)
- **Canny:** Edge detection → preserve line structure during refinement
- **Depth:** Depth map → proper perspective for backgrounds
- **Scribble:** Rough sketch → guided generation for layout pass

### Advantages over v5 (prompt-only)
- Pose accuracy: ControlNet skeleton → exact angles (solves side/back view problem)
- Character consistency: LoRA identity → stronger than IP-Adapter for trained characters
- Prop accuracy: LoRA-trained custom props → model actually "knows" ba tieu fan
- Quality: Multi-pass refinement → each pass fixes specific issues
- Background quality: Separate pass → cinematic manga backgrounds
- Detail: ADetailer pass → fixes hands and facial details

### Prerequisites for v6
- [ ] Install ControlNet models for SDXL (openpose, canny, depth)
- [ ] Set up LoRA training pipeline (kohya_ss / ai-toolkit)
- [ ] Create reference image dataset for custom props (10-30 images each)
- [ ] Create OpenPose skeleton templates for standard poses
- [ ] Test inpainting pipeline on MPS (mask generation + inpaint)
- [ ] Evaluate ADetailer compatibility with MPS
