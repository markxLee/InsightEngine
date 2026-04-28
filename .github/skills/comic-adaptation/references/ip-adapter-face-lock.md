# IP-Adapter Face Lock — Reference Guide

> Version: 1.0 | Source: v4 character sheet generator learnings
> For: SDXL Base 1.0 + IP-Adapter Plus Face (ViT-H) on Apple Silicon (MPS)

---

## Architecture Overview

IP-Adapter injects face identity via cross-attention embeddings. Unlike img2img (which
blends at the pixel level), IP-Adapter operates in the latent attention space, giving
much stronger identity preservation while allowing pose/costume/hair to change freely.

```
┌─────────────────────────────────────────────────┐
│  Phase A: Load SDXL Base 1.0 (plain)            │
│  Phase 0: txt2img → canonical face (bald, front)│
│  Phase B: Load IP-Adapter + ViT-H encoder       │
│  Phase 1: set_face_reference(canonical, scale)   │
│  Phase 2+: generate() with face_embeds injected  │
└─────────────────────────────────────────────────┘
```

---

## Required Models & Weights

| Component | Source | Subfolder | Size |
|-----------|--------|-----------|------|
| SDXL Base 1.0 | `stabilityai/stable-diffusion-xl-base-1.0` | — | ~6.5 GB |
| IP-Adapter Plus Face | `h94/IP-Adapter` | `sdxl_models/ip-adapter-plus-face_sdxl_vit-h.safetensors` | ~848 MB |
| CLIP ViT-H encoder | `h94/IP-Adapter` | `models/image_encoder` | ~2.5 GB |

**CRITICAL:** Use `models/image_encoder` (ViT-H, output dim 1280), NOT
`sdxl_models/image_encoder` (ViT-bigG, output dim 1664). The Plus Face weights
expect 1280-dim embeddings. Using ViT-bigG causes a dimension mismatch error.

---

## MPS-Specific Constraints (Apple Silicon)

### NaN-producing sizes — NEVER use on MPS

| Size | Status |
|------|--------|
| 768×768 | ❌ NaN — all-black output |
| 1024×1024 | ❌ NaN — all-black output |
| 512×512 | ❌ NaN (suspected) |

### Safe sizes

| Size | Orientation | Use for |
|------|------------|---------|
| 768×1024 | Portrait | Canonical face, face turnarounds, expressions |
| 1024×768 | Landscape | Body turnarounds, composites, multi-view sheets |

### Scheduler

- **Use:** `EulerDiscreteScheduler` (default) — ~70-120s/step with IP-Adapter on MPS
- **NEVER use:** `DDIMScheduler` — 546s/step on MPS (50-100x slower)

### Attention slicing

```python
# ✅ CORRECT ORDER
pipe = StableDiffusionXLPipeline.from_pretrained(...)
pipe.enable_attention_slicing()  # OK here, before IP-Adapter

# Load IP-Adapter
pipe.load_ip_adapter("h94/IP-Adapter", ...)

# ❌ NEVER do this after loading IP-Adapter:
# pipe.enable_attention_slicing()
# This overwrites IPAdapterAttnProcessor2_0 with SlicedAttnProcessor
# which cannot handle tuple encoder_hidden_states → crash
```

### Memory management

- IP-Adapter + SDXL needs ~12-14 GB RAM on MPS
- `enable_model_cpu_offload()` can help if RAM is tight but adds latency
- Pre-compute face embeddings once via `pipe.prepare_ip_adapter_image_embeds()`
  and reuse across all generations

---

## IP-Adapter Scale Guide

Scale controls how strongly the face reference influences the output.
Higher = more face consistency but less prompt responsiveness.

| Scale | Effect | Best for |
|:-----:|--------|----------|
| 0.3 | Light influence — prompt dominates | Composites with distinct hair/costume |
| 0.4 | Moderate — face recognizable, prompt strong | Body turnarounds, action poses |
| 0.5 | Balanced | Expression sheets, medium shots |
| 0.6 | Strong face lock | Close-up variations |
| 0.7 | Very strong — face dominates | Face turnaround sheets |
| 0.8+ | Over-lock — all outputs look identical | Almost never use |

**Key insight from v4:** Scale 0.6 on composites caused the canonical's bald head to
override all hair descriptions. Lowering to 0.3-0.4 for composites lets the prompt's
hair/costume instructions come through while maintaining face identity.

---

## Canonical Face Best Practices

1. **Always generate bald** — hair at canonical stage will bleed into all IP-locked images
2. **Front view, head+shoulders only** — tighter crop = cleaner face embedding
3. **Black and white lineart** — removes color bias from face embedding
4. **768×1024 portrait** — gives the face enough pixel detail for embedding quality

Example prompt:
```
black and white ink lineart, manga style, white background,
character portrait, ((front view)), ((bald)),
young boy face, large determined eyes, strong jawline,
Vietnamese features, head and shoulders, centered, clean lineart
```

---

## Prompt Strategy with IP-Adapter

IP-Adapter handles face identity, so prompts should NOT repeat face descriptions.
Focus on:
- **Pose** — "standing T-pose", "3/4 view from left", "action pose running"
- **Costume** — "wearing golden armor, dragon helmet" (put at START)
- **Hair** — "long black hair flowing" (put at START, before style tokens)
- **Layout** — "character turnaround sheet, 3 views side by side"

CLIP has a 77-token hard limit. With IP-Adapter, the effective limit is even tighter
because some attention is used for face embeddings. Keep prompts ≤60 tokens.

---

## Performance Benchmarks (Apple Silicon M-series, 16 GB)

| Mode | Steps | Time/step | Total/image |
|------|:-----:|:---------:|:-----------:|
| txt2img (no IP-Adapter) | 25 | 7-10s | ~3-4 min |
| IP-Adapter face-locked | 25 | 67-123s | ~28-50 min |
| IP-Adapter (20 steps) | 20 | 67-123s | ~22-40 min |

IP-Adapter is ~10x slower than plain txt2img on MPS. Plan accordingly:
- A 6-image character set takes ~3-4 hours
- Consider reducing to 20 steps for iteration (quality loss is minimal)
- Pre-compute face embeddings to avoid recomputation

---

## Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `'tuple' object has no attribute 'shape'` | `enable_attention_slicing()` called after IP-Adapter load | Don't call it after loading |
| `RuntimeError: mat1 dim 1 must match mat2 dim 1` | Using ViT-bigG (1664) instead of ViT-H (1280) | Use `models/image_encoder` not `sdxl_models/image_encoder` |
| All-black / NaN output | Square size on MPS (768×768, 1024×1024) | Use 768×1024 or 1024×768 |
| 546s/step | DDIMScheduler on MPS | Use default EulerDiscreteScheduler |
| `encoder_hid_dim_type` error at generate | IP-Adapter loaded but no `ip_adapter_image_embeds` passed | Always pass face_embeds after IP-Adapter is loaded |
| Bald in all images | Canonical was bald + IP scale too high | Lower IP scale to 0.3-0.4 for composites |

---

## Script Location

- **v4 script:** `tmp/gen_character_sheet_v4.py` (session, IP-Adapter face lock)
- **v1 script:** `.github/skills/comic-adaptation/scripts/gen_character_sheet.py` (bundled, PDF-based)
- **Bundled will be updated** to include IP-Adapter mode in future version
