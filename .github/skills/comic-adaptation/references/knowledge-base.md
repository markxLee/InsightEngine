# Comic Adaptation — Development Knowledge Base

> Consolidated from Copilot repo memory. All knowledge needed to continue development
> on any machine. Read this file before starting new work on comic-adaptation skill.

---

## 1. MPS (Apple Silicon) SDXL Constraints

### NaN Bug
- UNet fp16 on MPS produces all-zero latents (intermittent, session-dependent)
- PyTorch MPS backend bug with SDXL — NOT thermal/memory
- Basic MPS ops (randn, matmul) work fine — only SDXL UNet affected

### Safe Resolutions
- **OK:** 768x1024 (portrait), 1024x768 (landscape)
- **NaN:** 1024x1024, 768x768, 1024x576, 576x1024 — ALL broken on MPS
- Detection: `np.array(image).max() == 0` or file size < 10KB

### NaN Fix (v5)
- Retry 3 seeds (seed+7, +31, +97) → if all fail → CPU fallback
- CPU: ~33s/step (vs ~8s/step MPS) but 100% reliable
- **Warning:** CPU fallback generates differently than MPS — avoid for canonical face

### MPS Performance
- SDXL Base 1.0: ~7-11s/step on MPS (varies with thermal)
- Thermal throttle after ~30min: 7s/step → 28s/step
- Shader graph cache "out of space" errors when disk < 5GB — non-blocking

### MPS Pipeline Rules
- Use `StableDiffusionXLPipeline` — NOT `AutoPipelineForText2Image`
- Keep `EulerDiscreteScheduler` — DDIMScheduler is 50-100x slower on MPS
- Generator device must be "cpu" when pipeline is on MPS

---

## 2. IP-Adapter Face Lock

### Setup
- Model: `ip-adapter-plus-face_sdxl_vit-h.safetensors` from `h94/IP-Adapter` `sdxl_models/`
- Image encoder: `h94/IP-Adapter` subfolder `models/image_encoder` (ViT-H, 1280 dim)
- **NOT** `sdxl_models/image_encoder` (ViT-bigG, 1664 dim) — dimension mismatch

### Critical Rules
- Load IP-Adapter BEFORE `enable_attention_slicing()`
- Do NOT re-enable slicing after loading — overwrites `IPAdapterAttnProcessor2_0`
- Once IP-Adapter loaded, `image_embeds` REQUIRED for every generation call
- 2-phase pipeline: Phase A (plain SDXL → canonical) → Phase B (load IP-Adapter → face-locked)

### Scale Tuning (v5 — tested)
| Sheet type | IP scale |
|------------|:--------:|
| Face turnaround | 0.7 |
| Face closeup | 0.7 |
| Expression | 0.55 |
| Hair reference | 0.45 |
| Body turnaround | 0.4 |
| Costume reference | 0.35 |
| Composite | 0.35 |
| Accessories | 0.3 |

- v4 used 0.6 for composites → caused bald head override (too strong)
- CLIP 77-token limit applies — keep prompts ≤60 tokens, critical keywords first

---

## 3. Version History Summary

| Version | Approach | Result |
|---------|----------|--------|
| v1 | Text-only planning + reportlab PDF | No AI images |
| v2 | SDXL txt2img + img2img reference | Face inconsistent — pixel blending doesn't preserve identity |
| v3 | IP-Adapter Face Lock | Face consistency good. MPS NaN bugs discovered |
| v4/4.1 | IP-Adapter + scale tuning | Better composites. Expression sheet added |
| v5 | 14 sheet types + CPU fallback | Full pipeline. Pose control still impossible |
| v6 | ControlNet OpenPose + SDXL | MPS+CN=NaN. CPU fp32 works but slow. MPS fp32 untested |

### v5 Quality (Linh character, seed 42)
- Technical quality: 8/10, Face consistency: 7/10
- Hair accuracy: 5/10, Costume accuracy: 6/10, Pose variety: 5/10
- **Main issues:** side/back composites show front view, twin braids inconsistent, custom props missing

---

## 4. ControlNet OpenPose + SDXL (v6)

### MPS Compatibility (TESTED — v6.1 diagnostic)
- **ControlNet + MPS fp16 = 100% NaN** at ALL conditioning scales (0.8, 0.5, 0.2)
- MPS fp16 WITHOUT ControlNet = OK ✅ (SDXL works fine alone)
- CPU fp32 + ControlNet = works but extremely slow (~3-5min/step)
- **Root cause:** ControlNet conditioning introduces fp16 precision overflow on MPS
- **MPS fp32 + ControlNet:** UNTESTED — potential middle ground (less NaN risk, faster than CPU)

### ControlNet Model
- Repo: `dimitribarbot/controlnet-openpose-sdxl-1.0-safetensors` (~2.5GB safetensors)
- **NOT** `diffusers/controlnet-openpose-sdxl-1.0` (private/401) or `r3gm/...fp16` (no weight files)
- Load with `ControlNetModel.from_pretrained()` + `StableDiffusionXLControlNetPipeline`

### OpenPose Skeleton Generation
- Hand-drawn stick figures on black background (Pillow ImageDraw)
- 4 poses: front, side, back, three_quarter
- Resolution: 768x1024 (portrait, MPS-safe)

### v6 Script: `tmp/test_controlnet_v6.py`
- 3 modes: `diagnose` (5 quick tests), `full` (4 poses with NaN resilience), `cpu-only`
- NaN resilience: Tier 1 (3 seeds) → Tier 2 (lower cn_scale) → Tier 3 (CPU fp32 fallback)
- CLI: `--output`, `--steps`, `--seed`, `--cn-scale`, `--mode`

---

## 5. Approaches That DON'T Work (Never Repeat)

| Approach | Why it fails |
|----------|-------------|
| img2img `--reference --strength` | Pixel-level, not identity preservation |
| SD-Turbo for characters | 4 steps → blurry, guidance=0.0 → no negatives |
| DDIMScheduler on MPS | 50-100x slower |
| Square resolutions on MPS | Always NaN |
| IP scale >0.5 for composites | Bald override |
| Prompt-only pose control | SDXL ignores side/back view directions |
| Long prompts (>60 tokens) | CLIP truncation |
| CPU fallback for canonical | Different gen characteristics |
| Separate char + BG compositing | Unnatural pasting, not natural integration |
| **ControlNet + MPS fp16** | **100% NaN at all cn_scales (0.8→0.2) — v6 tested** |

---

## 5. gen-image Skill Notes

- 3-tier model system: turbo (SDXL-Turbo), quality (SDXL Base 1.0), legacy (SD-Turbo)
- Character presets: `character-anime-male`, `character-anime-female`
- SD-Turbo fundamentally unsuitable for character art
- Always specify gender explicitly in character presets

---

## 6. Data Collection Lessons

- RULE-8: fabrication prohibition + feasibility pre-check
- RULE-9: subagents must receive file paths + requirements in prompt
- Search SKILL: keyword validation + JS-rendered site detection
- Anti-dilution: keep instructions general, don't create case-specific refs

---

## 7. Skill Architecture Principles

- Comic/anime adaptation = production workflow, not prose planning
- Visual skills require asset path: scripts, templates, or companion skill
- Prose-only comic skills insufficient without reusable visual artifacts
- Keep narrative layer separate from production layer

---

## 8. Script Locations

| Script | Version | Status |
|--------|---------|--------|
| `tmp/gen_character_sheet_v5.py` | v5 | Latest — 14 sheets + CPU fallback |
| `tmp/gen_character_sheet_v4.1.py` | v4.1 | Superseded |
| `tmp/gen_character_sheet_v4.py` | v4 | Superseded |
| `.github/skills/gen-image/scripts/gen_image.py` | v2.0 | gen-image skill script |
| `.github/skills/comic-adaptation/SKILL.md` | v4.0 | Skill definition |
| `.github/skills/comic-adaptation/CHANGELOG.md` | — | Full version history |
| `.github/skills/comic-adaptation/references/ip-adapter-face-lock.md` | — | IP-Adapter reference |
