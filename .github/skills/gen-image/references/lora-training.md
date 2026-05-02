# LoRA Training Reference — Character Consistency Pipeline

> Train a small LoRA adapter (~6 MB) that teaches SD 1.5 to reproduce a specific character
> consistently across any pose, scene, or composition using a trigger token.

---

## Pipeline Overview

```
┌──────────────────────────────────────────────────────────────────┐
│               CHARACTER LoRA TRAINING PIPELINE                   │
│                                                                  │
│  1. REFERENCE — Generate canonical character image               │
│     └─ SD 1.5 + ControlNet OpenPose (or user-provided art)      │
│                                                                  │
│  2. MULTI-ANGLE — Generate consistent multi-view dataset         │
│     └─ IP-Adapter keeps character identity across poses          │
│     └─ Front, side, back, three-quarter views                    │
│                                                                  │
│  3. DATASET — Prepare image + caption pairs                      │
│     └─ Each .png paired with .txt containing trigger + tags      │
│                                                                  │
│  4. TRAIN — LoRA fine-tuning on UNet attention layers            │
│     └─ rank 8, 500 steps, lr 1e-4, ~60 min on Apple Silicon     │
│                                                                  │
│  5. INFERENCE — Test trained LoRA with trigger token              │
│     └─ Compare baseline (no LoRA) vs LoRA output                │
│     └─ cross_attention_kwargs={"scale": 0.8} for LoRA strength  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Prerequisites

| Component | Version | Purpose |
|-----------|---------|---------|
| Python | >= 3.10 | Runtime |
| torch | >= 2.2.0 | Tensor computation |
| diffusers | >= 0.27.0 | SD pipeline, ControlNet, IP-Adapter |
| peft | >= 0.10.0 | LoRA adapter management |
| transformers | >= 4.35.0 | CLIP tokenizer/text encoder |
| safetensors | >= 0.4.0 | Weight serialization |
| Pillow | >= 10.0 | Image loading/processing |

**Models to download (one-time):**

```bash
# SD 1.5 (~5 GB) — download to /tmp/sd15/
git clone https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-v1-5 /tmp/sd15

# ControlNet OpenPose (~1.4 GB) — for pose-guided generation
git clone https://huggingface.co/lllyasviel/control_v11p_sd15_openpose /tmp/controlnet-sd15-openpose

# IP-Adapter (~200 MB) — for character identity transfer
git clone https://huggingface.co/h94/IP-Adapter /tmp/ip-adapter
```

---

## Step 1: Generate Reference Character

The pipeline starts with a single high-quality reference image. This can be:
- **User-provided artwork** — any character image the user already has
- **AI-generated** — SD 1.5 + ControlNet for pose-controlled generation

### AI Generation with ControlNet OpenPose

```python
import torch
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, EulerDiscreteScheduler

# Load models (fp32 required on MPS)
controlnet = ControlNetModel.from_pretrained(
    "/tmp/controlnet-sd15-openpose", torch_dtype=torch.float32
)
pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "/tmp/sd15", controlnet=controlnet, torch_dtype=torch.float32,
    safety_checker=None
).to("mps")
pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config)

# Generate with pose image
pose_image = load_image("pose_reference.png")  # OpenPose skeleton
gen = torch.Generator(device="cpu").manual_seed(42)
image = pipe(
    prompt="manga boy, monochrome, clean lineart, full body, front view",
    negative_prompt="blurry, low quality, deformed, extra limbs",
    image=pose_image,
    num_inference_steps=25,
    guidance_scale=7.5,
    generator=gen,
    width=512, height=768,
).images[0]
image.save("reference.png")
```

**Tips for reference generation:**
- Front-facing neutral pose works best as the canonical view
- Keep the prompt simple — focus on character traits, not complex scenes
- Use `seed` for reproducibility so you can regenerate if needed
- 512×768 is the sweet spot for SD 1.5 character quality

---

## Step 2: IP-Adapter Multi-Angle Generation

IP-Adapter preserves the character's visual identity while generating different poses.
This is the key step that creates a diverse training dataset from a single reference.

### Setup IP-Adapter with SD 1.5 + ControlNet

```python
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, EulerDiscreteScheduler
from transformers import CLIPVisionModelWithProjection
import torch

# Load CLIP image encoder for IP-Adapter
image_encoder = CLIPVisionModelWithProjection.from_pretrained(
    "/tmp/ip-adapter/models/image_encoder", torch_dtype=torch.float32
)

# Load ControlNet + SD 1.5 pipeline
controlnet = ControlNetModel.from_pretrained(
    "/tmp/controlnet-sd15-openpose", torch_dtype=torch.float32
)
pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "/tmp/sd15", controlnet=controlnet,
    image_encoder=image_encoder,
    torch_dtype=torch.float32, safety_checker=None
).to("mps")

# Load IP-Adapter weights
pipe.load_ip_adapter(
    "/tmp/ip-adapter", subfolder="models",
    weight_name="ip-adapter_sd15.bin"
)
pipe.set_ip_adapter_scale(0.6)  # 0.5-0.7 range works well
pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config)

# CRITICAL: Do NOT use pipe.enable_attention_slicing() with IP-Adapter
# They conflict and produce black/corrupted images.
```

### Generate Multi-Angle Views

```python
reference_image = load_image("reference.png")
pose_prompts = {
    "front": "front view, standing, full body",
    "side": "side view, standing, full body, profile",
    "back": "back view, standing, full body, from behind",
    "three_quarter": "three quarter view, standing, full body, slight angle",
}

for view_name, pose_desc in pose_prompts.items():
    pose_image = load_image(f"pose_{view_name}.png")  # OpenPose skeleton
    gen = torch.Generator(device="cpu").manual_seed(42)
    result = pipe(
        prompt=f"manga boy, monochrome, clean lineart, {pose_desc}, white background",
        negative_prompt="blurry, deformed, extra limbs, color, realistic",
        image=pose_image,
        ip_adapter_image=reference_image,
        num_inference_steps=25,
        guidance_scale=7.5,
        generator=gen,
        width=512, height=768,
    ).images[0]
    result.save(f"ip_{view_name}.png")
```

**IP-Adapter tips:**
- Scale 0.5–0.7: good identity preservation with pose flexibility
- Higher scale (>0.7): stronger identity but may fight the pose prompt
- Always use the SAME reference image for all angles — consistency comes from IP-Adapter
- Negative prompts help avoid style drift

---

## Step 3: Dataset Preparation

Each training image needs a matching `.txt` caption file with the trigger token.

### Directory Structure

```
dataset/
├── ref_front.png
├── ref_front.txt        → "bwmanga_boy, manga, monochrome, front view, standing, full body"
├── locked_front.png
├── locked_front.txt     → "bwmanga_boy, manga, monochrome, front view, full body"
├── locked_side.png
├── locked_side.txt      → "bwmanga_boy, manga, monochrome, side view, profile, full body"
├── locked_back.png
├── locked_back.txt      → "bwmanga_boy, manga, monochrome, back view, full body"
├── locked_three_quarter.png
└── locked_three_quarter.txt → "bwmanga_boy, manga, monochrome, three quarter view, full body"
```

### Caption Format Rules

1. **Trigger token first** — always start captions with the trigger token
2. **Descriptive tags** — include style tags (manga, monochrome) and view tags (front, side, etc.)
3. **Keep under 77 tokens** — CLIP tokenizer truncates at 77 tokens
4. **Consistent style tags** — use the same style descriptors across all captions
5. **Unique trigger token** — choose something that doesn't exist in CLIP's vocabulary
   (e.g., `bwmanga_boy`, `sks_character`, `my_char_01`)

### Dataset Size Guidelines

| Dataset Size | Quality | Training Steps | Use Case |
|:---:|:---:|:---:|---|
| 3–5 images | Baseline | 300–500 | Quick prototype, style transfer |
| 8–15 images | Good | 500–800 | Character with moderate consistency |
| 20+ images | Best | 800–1500 | High-fidelity character reproduction |

5 images (1 reference + 4 IP-Adapter angles) is the minimum for a functional LoRA.
More angles and expressions improve quality significantly.

---

## Step 4: LoRA Training

### Training Script

```bash
python3 .github/skills/gen-image/scripts/train_lora.py \
  --dataset path/to/dataset/ \
  --output path/to/lora/ \
  --trigger "bwmanga_boy" \
  --steps 500 \
  --lr 1e-4 \
  --rank 8 \
  --resolution 512 \
  --save-every 100 \
  --sd-path /tmp/sd15
```

### Training Parameters

| Parameter | Default | Range | Notes |
|-----------|---------|-------|-------|
| `--rank` | 8 | 4–32 | Higher = more capacity, more overfitting risk |
| `--lr` | 1e-4 | 5e-5 – 5e-4 | Lower for larger datasets, higher for small |
| `--steps` | 500 | 300–1500 | Scale with dataset size (see table above) |
| `--resolution` | 512 | 512 | SD 1.5 native resolution, don't change |
| `--batch-size` | 1 | 1–2 | MPS memory limited, stay at 1 |
| `--save-every` | 100 | 50–200 | Checkpoint frequency |

### Architecture Details

```yaml
base_model: stable-diffusion-v1-5
lora_config:
  rank: 8
  alpha: 8                    # alpha = rank is standard practice
  target_modules:
    - to_k                    # Key projection in cross-attention
    - to_q                    # Query projection
    - to_v                    # Value projection
    - to_out.0                # Output projection
  init_weights: gaussian

optimizer: AdamW
  lr: 1e-4
  weight_decay: 1e-2
scheduler: DDPMScheduler       # For training noise schedule
loss: MSE (predict noise)
gradient_clipping: 1.0
mps_cache_cleanup: every 50 steps
```

### What to Expect During Training

- **Speed**: ~5–8 s/step on Apple Silicon M4 (24 GB RAM)
- **Loss curve**: starts ~0.13, drops to ~0.05–0.08 by step 500
- **Total time**: ~40–60 min for 500 steps
- **Thermal throttling**: speed may slow in last ~100 steps (MPS thermal management)
- **Output**: checkpoints every N steps + final weights in `.safetensors` format

### Monitoring Training

```
Step  100/500 | loss=0.0845 | 5.2s/step | ETA 2080s
Step  200/500 | loss=0.0721 | 5.3s/step | ETA 1590s
Step  300/500 | loss=0.0632 | 5.8s/step | ETA 1160s
Step  400/500 | loss=0.0601 | 6.5s/step | ETA  650s
Step  500/500 | loss=0.0588 | 7.5s/step | ETA    0s
```

Loss should generally decrease but will fluctuate — this is normal with small datasets.
If loss plateaus above 0.10 after 300 steps, consider: more training images, lower learning rate,
or higher LoRA rank.

---

## Step 5: Inference Test

### Inference Script

```bash
python3 .github/skills/gen-image/scripts/lora_inference.py \
  --lora path/to/lora/final/ \
  --trigger "bwmanga_boy" \
  --output path/to/inference/ \
  --steps 25 \
  --seed 42 \
  --lora-scale 0.8 \
  --num-images 4
```

### How LoRA Inference Works

The inference script:
1. Loads SD 1.5 + adds LoRA adapter (peft)
2. Generates a **baseline** image WITHOUT LoRA for comparison
3. Enables LoRA and generates test images with the trigger token
4. Uses `cross_attention_kwargs={"scale": lora_scale}` to control LoRA strength

### LoRA Scale Guide

| Scale | Effect | Use Case |
|:-----:|--------|----------|
| 0.0 | No LoRA effect | Baseline comparison |
| 0.4–0.6 | Subtle character influence | Blending with different styles |
| 0.7–0.9 | Strong character identity | Default — recommended range |
| 1.0 | Maximum LoRA | May over-apply, test before using |

### Evaluating Results

Compare baseline vs LoRA images — the LoRA versions should show:
- ✅ Consistent character features (face shape, hair style, proportions)
- ✅ Style consistency (line weight, shading approach, level of detail)
- ✅ Trigger token working (character appears only when trigger is in prompt)
- ⚠️ Some variation in fine details is normal (exact hair strand placement, etc.)

---

## MPS / Apple Silicon Constraints

These constraints are critical for avoiding NaN errors and black images on Apple Silicon:

| Constraint | Reason | Solution |
|-----------|--------|----------|
| **fp32 only** | fp16 produces NaN on MPS | Always `torch_dtype=torch.float32` |
| **EulerDiscreteScheduler** | Other schedulers may NaN | Set scheduler explicitly for inference |
| **DDPMScheduler for training** | Standard training scheduler | Used automatically by train script |
| **Generator device = "cpu"** | MPS generator unreliable | `torch.Generator(device="cpu")` |
| **No attention_slicing + IP-Adapter** | They conflict | Never use together |
| **CLIP 77 token limit** | Tokenizer truncates | Keep prompts concise |
| **MPS cache cleanup** | Prevents memory pressure | Script does this every 50 steps |
| **Batch size = 1** | Limited unified memory | Don't increase on <32 GB machines |

---

## Troubleshooting

### NaN During Training
- Cause: fp16 on MPS, or learning rate too high
- Fix: Ensure `torch.float32` everywhere, reduce `--lr` to 5e-5

### Black/Corrupted Images with IP-Adapter
- Cause: `pipe.enable_attention_slicing()` conflicts with IP-Adapter
- Fix: Remove attention_slicing call, or don't use it with IP-Adapter

### Loss Not Decreasing
- Cause: Learning rate too low, or dataset too small/homogeneous
- Fix: Increase `--lr` to 2e-4, add more diverse training images

### Out of Memory (MPS)
- Cause: Resolution too high or batch size > 1
- Fix: Keep `--resolution 512`, `--batch-size 1`, close other apps

### Character Doesn't Appear in Generated Images
- Cause: Trigger token not in prompt, or LoRA scale too low
- Fix: Ensure trigger is the first token in prompt, increase `--lora-scale` to 0.9

### Thermal Throttling (Slow Last Steps)
- Cause: Normal MPS behavior on sustained GPU workload
- Fix: Not a bug — training still completes correctly, just slower

---

## Output Files

After training completes:

```
lora/
├── checkpoint-100/
│   └── pytorch_lora_weights.safetensors    # Intermediate checkpoint
├── checkpoint-200/
│   └── ...
├── checkpoint-500/
│   └── ...
└── final/
    ├── lora_weights.safetensors            # Final weights (use this)
    ├── lora_weights.pt                     # PyTorch format backup
    └── config.txt                          # Training configuration log
```

After inference test:

```
inference/
├── baseline_no_lora.png    # Generated WITHOUT LoRA (comparison)
├── lora_test_00.png        # Generated WITH LoRA — test pose 1
├── lora_test_01.png        # test pose 2
├── lora_test_02.png        # test pose 3
└── lora_test_03.png        # test pose 4
```

---

## Integration with Other Skills

- **gen-slide / gen-word / gen-pdf**: Use LoRA-generated character images as illustrations
- **comic-adaptation**: LoRA provides the character consistency that comic pages need
- **design**: Use LoRA characters in posters, covers, certificates
- **compose**: Reference LoRA outputs in synthesized documents

The trained LoRA adapter is portable — the `.safetensors` file can be shared, reused
across sessions, and loaded by any diffusers-compatible pipeline.
