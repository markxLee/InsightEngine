# Image Generation Reference — Cross-Platform AI Images

> Covers: characters, backgrounds, landscapes, slide backgrounds, slide frames.
> For advanced image-to-image restyling or face preservation, use the `gen-image` skill instead.

---

## GPU Auto-Detection

The generation script detects the best available device automatically:

```python
import torch

def get_device():
    if torch.cuda.is_available():
        return "cuda"                     # NVIDIA GPU — fastest
    elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
        return "mps"                      # Apple Silicon — fast
    else:
        return "cpu"                      # Any machine — slow (~2–10 min)
```

Always warn the user before starting a CPU run: expected time is 2–10 minutes for 4 inference steps.

---

## Style Presets

Choose the preset that best fits the user's request, or suggest options if unsure.

```yaml
CHARACTER:
  character-cartoon:
    prompt_suffix: "cartoon character illustration, flat design, clean linework, vibrant colors, white background, no text"
    size: [512, 512]
  character-realistic:
    prompt_suffix: "digital illustration of a person, professional art style, soft shading, plain background, no text"
    size: [512, 512]
  character-anime:
    prompt_suffix: "anime style character illustration, detailed, colorful, clean background, no text"
    size: [512, 512]

BACKGROUND:
  background-abstract:
    prompt_suffix: "abstract geometric background, modern design, smooth gradients, no text, no people"
    size: [768, 768]
  background-gradient:
    prompt_suffix: "soft color gradient background, smooth blending, professional, minimal, no text"
    size: [768, 768]
  background-texture:
    prompt_suffix: "subtle texture background, paper or fabric texture, muted tones, no text"
    size: [768, 768]

LANDSCAPE:
  landscape-nature:
    prompt_suffix: "beautiful natural landscape, mountains and forest, wide panoramic view, photorealistic, no text"
    size: [768, 512]
  landscape-urban:
    prompt_suffix: "modern city skyline, urban landscape, professional photography style, no text"
    size: [768, 512]
  landscape-fantasy:
    prompt_suffix: "fantasy landscape illustration, magical environment, vivid colors, concept art style, no text"
    size: [768, 512]

SLIDE_BACKGROUND:
  slide-bg-corporate:
    prompt_suffix: "professional corporate slide background, clean geometric shapes, blue and white palette, 16:9 format, no text"
    size: [1280, 720]
  slide-bg-dark:
    prompt_suffix: "elegant dark presentation background, subtle gradient, minimal abstract design, 16:9 format, no text"
    size: [1280, 720]
  slide-bg-creative:
    prompt_suffix: "creative colorful presentation background, modern design, dynamic shapes, 16:9, no text"
    size: [1280, 720]
  slide-bg-nature:
    prompt_suffix: "soft nature-inspired slide background, leaves and light, calm colors, 16:9, no text"
    size: [1280, 720]

SLIDE_FRAME:
  slide-frame-minimal:
    prompt_suffix: "minimal decorative border frame, thin elegant lines, white center space, no text"
    size: [1280, 720]
  slide-frame-ornate:
    prompt_suffix: "ornate decorative border frame for presentation, classical style, gold tones, transparent center, no text"
    size: [1280, 720]
```

---

## Generation Script (gen_image.py)

```python
#!/usr/bin/env python3
"""Cross-platform AI image generation via SD-Turbo. Auto-detects CUDA/MPS/CPU."""
import argparse, os, time
import torch
from diffusers import AutoPipelineForText2Image

PRESETS = {
    "character-cartoon": ("cartoon character illustration, flat design, clean linework, vibrant colors, white background", 512, 512),
    "character-realistic": ("digital illustration of a person, professional art style, soft shading, plain background", 512, 512),
    "background-abstract": ("abstract geometric background, modern design, smooth gradients", 768, 768),
    "background-gradient": ("soft color gradient background, smooth blending, professional, minimal", 768, 768),
    "landscape-nature": ("beautiful natural landscape, mountains and forest, wide panoramic view, photorealistic", 768, 512),
    "landscape-urban": ("modern city skyline, urban landscape, professional photography style", 768, 512),
    "slide-bg-corporate": ("professional corporate slide background, clean geometric shapes, blue and white palette, 16:9 format", 1280, 720),
    "slide-bg-dark": ("elegant dark presentation background, subtle gradient, minimal abstract design, 16:9 format", 1280, 720),
    "slide-bg-creative": ("creative colorful presentation background, modern design, dynamic shapes, 16:9", 1280, 720),
    "slide-frame-minimal": ("minimal decorative border frame, thin elegant lines, white center space", 1280, 720),
    "slide-frame-ornate": ("ornate decorative border frame, classical style, gold tones, transparent center", 1280, 720),
}

def get_device():
    if torch.cuda.is_available(): return "cuda"
    if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available(): return "mps"
    return "cpu"

def generate(prompt, style, width, height, output_path, seed=None):
    device = get_device()
    dtype = torch.float16 if device != "cpu" else torch.float32
    print(f"🖥️  Device: {device} | Size: {width}x{height}")
    if device == "cpu":
        print("⚠️  CPU mode: generation may take 2–10 minutes.")

    pipe = AutoPipelineForText2Image.from_pretrained(
        "stabilityai/sd-turbo",
        torch_dtype=dtype,
        variant="fp16" if device != "cpu" else None
    ).to(device)

    if style and style in PRESETS:
        suffix, _, _ = PRESETS[style]
        full_prompt = f"{prompt}, {suffix}, no text, no letters, no words"
    else:
        full_prompt = f"{prompt}, no text, no letters, no words"

    generator = torch.Generator(device=device).manual_seed(seed) if seed else None
    t0 = time.time()
    image = pipe(
        prompt=full_prompt,
        guidance_scale=0.0,
        num_inference_steps=4,
        width=width,
        height=height,
        generator=generator
    ).images[0]

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    image.save(output_path)
    size_kb = os.path.getsize(output_path) // 1024
    elapsed = time.time() - t0
    print(f"✅ Saved: {output_path} ({size_kb} KB, {width}x{height}px, {elapsed:.0f}s, device: {device})")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--prompt", required=True)
    p.add_argument("--style", default=None, help="Preset name from PRESETS dict")
    p.add_argument("--width", type=int, default=768)
    p.add_argument("--height", type=int, default=768)
    p.add_argument("--output", required=True)
    p.add_argument("--seed", type=int, default=None)
    args = p.parse_args()
    generate(args.prompt, args.style, args.width, args.height, args.output, args.seed)
```

---

## Example Usage

```bash
# Slide background — corporate style
python3 .github/skills/gen-image/scripts/gen_image.py \
  --prompt "business meeting, professional" \
  --style slide-bg-corporate \
  --width 1280 --height 720 \
  --output output/slide_bg.png

# Character illustration
python3 .github/skills/gen-image/scripts/gen_image.py \
  --prompt "friendly teacher explaining to students" \
  --style character-cartoon \
  --output output/character.png

# Nature landscape for report header
python3 .github/skills/gen-image/scripts/gen_image.py \
  --prompt "green mountains at sunrise" \
  --style landscape-nature \
  --output output/landscape.png
```

---

## Important Rules

- Always append `no text, no letters, no words` to prompts — SD-Turbo cannot reliably render text
- For `slide-bg` and `slide-frame`, use exactly 1280×720 to match 16:9 presentation format
- Use `torch.float16` on CUDA/MPS and `torch.float32` on CPU (fp16 not supported on CPU)
- Model (~2GB) auto-downloads on first run to `~/.cache/huggingface/` and caches permanently
- On OOM (Out of Memory): reduce width/height by 256 and retry
- `--seed` enables reproducibility — same seed + prompt = same image

