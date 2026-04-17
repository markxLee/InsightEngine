# Image Generation — Full Reference (US-3.1.2, Apple Silicon Only)

> For advanced image generation (i2i restyling, portrait/face preservation, FaceID, IP-Adapter),
> use the `gen-image` skill from a-z-copilot-flow instead.
> `tao-hinh` only covers basic text-to-image for inline illustrations.

## Availability Check

```python
import platform, sys
if platform.machine() != 'arm64' or platform.system() != 'Darwin':
    print("⚠️ Tạo hình ảnh chỉ hỗ trợ trên Apple Silicon Mac.")
    sys.exit(1)
import torch
if not torch.backends.mps.is_available():
    print("⚠️ MPS backend không khả dụng. Cần macOS 12.3+.")
    sys.exit(1)
print("✅ Apple Silicon + MPS sẵn sàng.")
# Install: pip3 install --user torch diffusers transformers accelerate
```

## Style Presets

```yaml
PRESETS:
  flat-icon:
    suffix: "flat design icon, simple shapes, solid colors, no text, white background"
    size: [512, 512]
  dark-tech:
    suffix: "dark technology background, neon glow, cyberpunk aesthetic, no text"
    size: [768, 768]
  cartoon:
    suffix: "cartoon illustration style, vibrant colors, clean lines, no text"
    size: [768, 768]
  minimal:
    suffix: "minimalist illustration, clean lines, muted colors, lots of whitespace, no text"
    size: [512, 512]
  watercolor:
    suffix: "watercolor painting style, soft colors, artistic, no text"
    size: [768, 768]
  realistic:
    suffix: "photorealistic, high quality, detailed, professional photography, no text"
    size: [768, 768]
```

## SD-Turbo Script

```python
import torch
from diffusers import AutoPipelineForText2Image

pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/sd-turbo",
    torch_dtype=torch.float16,
    variant="fp16"
)
pipe = pipe.to("mps")

# IMPORTANT: append style suffix and "no text, no letters, no words"
prompt = f"{user_prompt}, {style_suffix}, no text, no letters, no words"

image = pipe(
    prompt=prompt,
    guidance_scale=0.0,
    num_inference_steps=4,
    width=width,
    height=height
).images[0]

image.save(output_path)
print(f"Image saved: {output_path} ({width}x{height})")
# Model auto-downloads on first use (~2GB) to ~/.cache/huggingface/
```

## Rules

```yaml
RULES:
  - NEVER include text rendering in prompts — SD cannot render text reliably
  - Always append "no text, no letters, no words" to prompts
  - Use torch.float16 for memory efficiency on MPS
  - Minimum size: 512x512; presentation images: 768x768
  - Model caches after first download — subsequent runs are fast

NON_APPLE_BEHAVIOR:
  message: |
    ⚠️ Chức năng tạo hình ảnh từ prompt chỉ hỗ trợ trên Apple Silicon Mac.
    Bạn vẫn có thể sử dụng chức năng tạo biểu đồ (bar, line, pie, radar, scatter).
  action: Skip image generation, suggest alternatives
```
