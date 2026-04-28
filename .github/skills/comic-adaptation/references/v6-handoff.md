# v6 Multi-Pass Pipeline — Handoff Notes

> Session: 2026-04-28 | Machine: MacBook Apple Silicon (MPS)
> Next: Continue on a more powerful machine (CUDA GPU recommended)

---

## Current State

- **SKILL.md** v4.0 — updated with v5 protocol + v6 roadmap
- **CHANGELOG.md** — full v1→v5 history + failed approaches documented
- **knowledge-base.md** — all development knowledge consolidated
- **gen_character_sheet_v5.py** — working, 14/14 images generated for Linh character
- **output/linh-character/** — 14 images, seed 42, quality ~6.7/10

## What v5 Can Do (Current Capability)
- SDXL Base 1.0 + IP-Adapter Plus Face for face consistency
- 14 sheet types per character (canonical, face, body, hair, costume, accessories, 4 composites)
- MPS NaN resilience (seed retry + CPU fallback)
- CLI-driven multi-character support

## What v5 CANNOT Do (Motivation for v6)
1. **Pose control** — "side view"/"back view" prompts ignored by SDXL
2. **Custom props** — SDXL doesn't know "ba tieu fan" or culture-specific objects
3. **Consistent art style** — relies on prompt prefix, not trained style
4. **Detail fix** — no way to fix hands/faces after generation
5. **Background quality** — no separate background pass

---

## v6 Implementation Plan

### Phase 1: Environment Setup (do this first on new machine)

```bash
# 1. ControlNet for SDXL
pip install controlnet_aux
# Download ControlNet models:
# - diffusers/controlnet-openpose-sdxl-1.0
# - diffusers/controlnet-canny-sdxl-1.0

# 2. LoRA training
pip install kohya_ss  # or ai-toolkit
# Requires: CUDA GPU with ≥12GB VRAM for SDXL LoRA training

# 3. Inpainting pipeline
# diffusers StableDiffusionXLInpaintPipeline (included in diffusers)

# 4. Upscaling
pip install realesrgan
# or use SDXL refinement pipeline

# 5. ADetailer (face/hand fix)
pip install adetailer  # or use manual inpainting masks
```

### Phase 2: LoRA Training (Priority — enables custom props)

**Character LoRA** (Linh):
1. Curate best 10-20 images from `output/linh-character/` as training set
2. Add 5-10 manually drawn/collected reference images for variety
3. Caption each with trigger word `linh_char`
4. Train: `kohya_ss` SDXL LoRA, rank r=16, ~800 steps, lr=1e-4
5. Test: generate with trigger word, verify face/body consistency

**Prop LoRA** (ba tieu fan):
1. Collect 10-30 images of ba tieu fans (photos, artwork, sketches)
2. Caption with trigger word `ba_tieu_fan`
3. Train: rank r=8, ~500 steps (simpler concept)
4. Test: generate character holding `ba_tieu_fan`

**Style LoRA** (manga lineart):
1. Collect 20-50 manga pages in target art style
2. Caption with trigger word `manga_bw_style`
3. Train: rank r=32, ~1500 steps (complex style)
4. Apply to ALL passes for visual consistency

### Phase 3: ControlNet Integration (Priority — enables pose control)

**OpenPose skeleton templates to create:**
- Standing front view (arms at sides)
- Standing 3/4 view (slight turn)
- Standing side profile (full 90°)
- Standing back view (away from camera)
- Action pose (running, fighting)
- Sitting pose

**Pipeline code pattern:**
```python
from diffusers import ControlNetModel, StableDiffusionXLControlNetPipeline
from controlnet_aux import OpenposeDetector

controlnet = ControlNetModel.from_pretrained(
    "diffusers/controlnet-openpose-sdxl-1.0",
    torch_dtype=torch.float16
)
pipe = StableDiffusionXLControlNetPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    controlnet=controlnet,
    torch_dtype=torch.float16
)
# Generate with skeleton conditioning
image = pipe(prompt=..., image=skeleton_image, ...).images[0]
```

### Phase 4: Multi-Pass Pipeline Implementation

Create `gen_character_sheet_v6.py` with:

```
PASS 1 — Layout
  Input: OpenPose skeleton for target pose
  Tool: ControlNet OpenPose + SDXL
  Output: Rough character in correct pose

PASS 2 — Character Refine
  Input: Pass 1 + character LoRA
  Method: Full image generation with LoRA + ControlNet
  Or: Inpaint character region with LoRA identity

PASS 3 — Face & Hand Fix
  Input: Pass 2 output
  Method: Detect face/hand regions → inpaint with higher detail
  Tool: IP-Adapter face lock + manual mask or ADetailer

PASS 4 — Background
  Input: Pass 3 with character masked
  Method: Inpaint BG separately (manga environments)
  Tool: Background LoRA or depth-conditioned generation

PASS 5 — Upscale & Sharpen
  Input: Pass 4 complete image
  Method: RealESRGAN 2-4x + line sharpening
  Output: Production-quality image
```

### Phase 5: Testing & Integration
- Test each pass independently first
- Test LoRA + ControlNet + IP-Adapter combined loading
- Measure VRAM usage (CUDA) vs MPS feasibility
- Update SKILL.md and CHANGELOG.md with v6 results

---

## File Checklist for Commit

```
Must commit:
✅ .github/skills/comic-adaptation/SKILL.md (v4.0)
✅ .github/skills/comic-adaptation/CHANGELOG.md (new)
✅ .github/skills/comic-adaptation/references/knowledge-base.md (new)
✅ .github/skills/comic-adaptation/references/v6-handoff.md (this file)
✅ tmp/gen_character_sheet_v5.py (latest working script)
✅ output/linh-character/ (14 generated images + meta)

Optional (large files, may skip):
⚠️ output/thanh-giong-anime/ (older generations)
⚠️ tmp/gen_character_sheet_v4*.py (superseded)
```

---

## Quick Start on New Machine

```bash
# 1. Clone repo
git clone <repo> && cd InsightEngine

# 2. Create venv + install deps
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install torch diffusers transformers accelerate
pip install controlnet_aux kohya_ss realesrgan  # v6 deps

# 3. Read knowledge base
cat .github/skills/comic-adaptation/references/knowledge-base.md

# 4. Read this handoff
cat .github/skills/comic-adaptation/references/v6-handoff.md

# 5. Start with LoRA training (Phase 2) or ControlNet test (Phase 3)
```
