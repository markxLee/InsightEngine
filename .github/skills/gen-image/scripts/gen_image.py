#!/usr/bin/env python3
"""
Cross-platform AI image generation via SD-Turbo.
Auto-detects best available device: CUDA > MPS > CPU.

Usage:
  python3 gen_image.py --prompt "..." --style slide-bg-corporate --output output/img.png
  python3 gen_image.py --prompt "..." --width 1280 --height 720 --output output/img.png
  python3 gen_image.py --list-styles

Styles: character-cartoon, character-realistic, character-anime,
        background-abstract, background-gradient, background-texture,
        landscape-nature, landscape-urban, landscape-fantasy,
        slide-bg-corporate, slide-bg-dark, slide-bg-creative, slide-bg-nature,
        slide-frame-minimal, slide-frame-ornate
"""
import argparse
import os
import sys
import time

PRESETS = {
    "character-cartoon": (
        "cartoon character illustration, flat design, clean linework, vibrant colors, white background",
        512, 512,
    ),
    "character-realistic": (
        "digital illustration of a person, professional art style, soft shading, plain background",
        512, 512,
    ),
    "character-anime": (
        "anime style character illustration, detailed, colorful, clean background",
        512, 512,
    ),
    "background-abstract": (
        "abstract geometric background, modern design, smooth gradients",
        768, 768,
    ),
    "background-gradient": (
        "soft color gradient background, smooth blending, professional, minimal",
        768, 768,
    ),
    "background-texture": (
        "subtle texture background, paper or fabric texture, muted tones",
        768, 768,
    ),
    "landscape-nature": (
        "beautiful natural landscape, mountains and forest, wide panoramic view, photorealistic",
        768, 512,
    ),
    "landscape-urban": (
        "modern city skyline, urban landscape, professional photography style",
        768, 512,
    ),
    "landscape-fantasy": (
        "fantasy landscape illustration, magical environment, vivid colors, concept art style",
        768, 512,
    ),
    "slide-bg-corporate": (
        "professional corporate slide background, clean geometric shapes, blue and white palette, 16:9 format",
        1280, 720,
    ),
    "slide-bg-dark": (
        "elegant dark presentation background, subtle gradient, minimal abstract design, 16:9 format",
        1280, 720,
    ),
    "slide-bg-creative": (
        "creative colorful presentation background, modern design, dynamic shapes, 16:9",
        1280, 720,
    ),
    "slide-bg-nature": (
        "soft nature-inspired slide background, leaves and light, calm colors, 16:9",
        1280, 720,
    ),
    "slide-frame-minimal": (
        "minimal decorative border frame, thin elegant lines, white center space",
        1280, 720,
    ),
    "slide-frame-ornate": (
        "ornate decorative border frame, classical style, gold tones, transparent center",
        1280, 720,
    ),
}


def get_device():
    try:
        import torch
    except ImportError:
        print("❌ torch not installed. Run: pip3 install --user torch diffusers transformers accelerate")
        sys.exit(1)

    if torch.cuda.is_available():
        return "cuda", torch.float16
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "mps", torch.float16
    return "cpu", torch.float32


def generate(prompt, style, width, height, output_path, seed=None):
    import torch
    from diffusers import AutoPipelineForText2Image

    device, dtype = get_device()
    print(f"🖥️  Device: {device} | Size: {width}x{height}")
    if device == "cpu":
        print("⚠️  CPU mode detected — generation may take 2–10 minutes.")

    # Build full prompt
    if style and style in PRESETS:
        suffix, preset_w, preset_h = PRESETS[style]
        # Use preset dimensions as defaults if user did not override
        if width == 768 and height == 768:  # detect "not overridden" defaults
            width, height = preset_w, preset_h
        full_prompt = f"{prompt}, {suffix}, no text, no letters, no words"
    else:
        full_prompt = f"{prompt}, no text, no letters, no words"

    # Load model
    variant = "fp16" if device != "cpu" else None
    pipe = AutoPipelineForText2Image.from_pretrained(
        "stabilityai/sd-turbo",
        torch_dtype=dtype,
        variant=variant,
    ).to(device)

    generator = None
    if seed is not None:
        generator = torch.Generator(device=device).manual_seed(seed)

    t0 = time.time()
    image = pipe(
        prompt=full_prompt,
        guidance_scale=0.0,
        num_inference_steps=4,
        width=width,
        height=height,
        generator=generator,
    ).images[0]

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    image.save(output_path)

    size_kb = os.path.getsize(output_path) // 1024
    elapsed = time.time() - t0
    print(f"✅ Saved: {output_path} ({size_kb} KB, {width}x{height}px, {elapsed:.0f}s, device: {device})")


def main():
    parser = argparse.ArgumentParser(description="Cross-platform AI image generation (SD-Turbo)")
    parser.add_argument("--prompt", help="Text description of the image to generate")
    parser.add_argument("--style", default=None, help="Style preset name (see --list-styles)")
    parser.add_argument("--width", type=int, default=768)
    parser.add_argument("--height", type=int, default=768)
    parser.add_argument("--output", help="Output PNG file path")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    parser.add_argument("--list-styles", action="store_true", help="List all available style presets")
    args = parser.parse_args()

    if args.list_styles:
        print("Available styles:")
        for name, (suffix, w, h) in PRESETS.items():
            print(f"  {name:<25} ({w}x{h}) — {suffix[:60]}…")
        return

    if not args.prompt:
        parser.error("--prompt is required")
    if not args.output:
        parser.error("--output is required")

    generate(args.prompt, args.style, args.width, args.height, args.output, args.seed)


if __name__ == "__main__":
    main()
