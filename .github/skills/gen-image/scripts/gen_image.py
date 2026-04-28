#!/usr/bin/env python3
"""
AI Image Generation v2.0 — Multi-model with quality tiers.

Models:
  turbo   — SDXL-Turbo, 4 steps, ~6s on MPS. Backgrounds, landscapes, slides.
  quality — SDXL Base 1.0, 25 steps, ~60s on MPS. Characters, detailed art.
            Supports negative prompts and higher resolution.
  legacy  — SD-Turbo (v1 backward compat).

Modes:
  txt2img — Text-to-image (default)
  img2img — Text + reference image (--reference). For character consistency:
            generate canonical view → reuse as ref for other poses.

Usage:
  # Fast background (turbo auto-selected)
  python3 gen_image.py --prompt "fantasy forest" --style landscape-fantasy --output bg.png

  # Quality anime character (quality auto-selected for character styles)
  python3 gen_image.py --prompt "warrior boy" --style character-anime-male --output char.png

  # Consistent pose from reference image
  python3 gen_image.py --prompt "same warrior, fighting" --style character-anime-male \
    --reference char.png --strength 0.55 --output char_fight.png

  # Force turbo for speed
  python3 gen_image.py --prompt "warrior boy" --style character-anime --model turbo --output fast.png
"""
import argparse
import os
import sys
import time

# ─── Model tiers ─────────────────────────────────────────────────────────────
MODELS = {
    "turbo": {
        "id": "stabilityai/sdxl-turbo",
        "steps": 4,
        "guidance": 0.0,
        "negative_ok": False,
    },
    "quality": {
        "id": "stabilityai/stable-diffusion-xl-base-1.0",
        "steps": 25,
        "guidance": 7.5,
        "negative_ok": True,
    },
    "legacy": {
        "id": "stabilityai/sd-turbo",
        "steps": 4,
        "guidance": 0.0,
        "negative_ok": False,
    },
}

# ─── Default negative prompts by category ────────────────────────────────────
NEG_CHARACTER = (
    "ugly, bad anatomy, deformed face, deformed body, extra limbs, extra fingers, "
    "mutated hands, poorly drawn face, poorly drawn hands, blurry, low quality, "
    "wrong gender, duplicate, cropped, watermark, text, signature, lowres, "
    "bad proportions, disfigured, extra arms, extra legs, fused fingers"
)
NEG_GENERAL = "blurry, low quality, watermark, text, ugly, deformed, lowres"

# ─── Style presets ───────────────────────────────────────────────────────────
# Format: (prompt_suffix, width, height, neg_category, model_hint)
PRESETS = {
    # ── Characters — default to quality model ──
    "character-anime": (
        "anime style, masterpiece, best quality, highly detailed, "
        "sharp facial features, detailed eyes, clean linework, vibrant colors, "
        "professional anime illustration, single character, solid clean background",
        768, 1024, "character", "quality",
    ),
    "character-anime-male": (
        "anime style male character, masculine, masterpiece, best quality, highly detailed, "
        "sharp jawline, determined eyes, strong build, clean linework, vibrant colors, "
        "professional anime illustration, 1boy, single male character, solid clean background",
        768, 1024, "character", "quality",
    ),
    "character-anime-female": (
        "anime style female character, feminine, masterpiece, best quality, highly detailed, "
        "beautiful eyes, graceful features, clean linework, vibrant colors, "
        "professional anime illustration, 1girl, single female character, solid clean background",
        768, 1024, "character", "quality",
    ),
    "character-cartoon": (
        "cartoon character illustration, flat design, clean linework, vibrant colors, "
        "white background",
        512, 512, "character", "turbo",
    ),
    "character-realistic": (
        "digital illustration, professional art style, soft shading, "
        "highly detailed face, sharp features, plain background",
        768, 1024, "character", "quality",
    ),
    # ── Backgrounds — turbo is fine ──
    "background-abstract": (
        "abstract geometric background, modern design, smooth gradients",
        768, 768, "background", "turbo",
    ),
    "background-gradient": (
        "soft color gradient background, smooth blending, professional, minimal",
        768, 768, "background", "turbo",
    ),
    "background-texture": (
        "subtle texture background, paper or fabric texture, muted tones",
        768, 768, "background", "turbo",
    ),
    # ── Landscapes ──
    "landscape-nature": (
        "beautiful natural landscape, mountains and forest, wide panoramic, "
        "concept art, masterpiece, best quality",
        768, 512, "landscape", "turbo",
    ),
    "landscape-urban": (
        "modern city skyline, urban landscape, professional photography style",
        768, 512, "landscape", "turbo",
    ),
    "landscape-fantasy": (
        "fantasy landscape illustration, magical environment, vivid colors, "
        "concept art style, masterpiece, best quality",
        768, 512, "landscape", "turbo",
    ),
    # ── Slide assets ──
    "slide-bg-corporate": (
        "professional corporate slide background, clean geometric shapes, "
        "blue and white palette, 16:9 format",
        1280, 720, "slide", "turbo",
    ),
    "slide-bg-dark": (
        "elegant dark presentation background, subtle gradient, "
        "minimal abstract design, 16:9 format",
        1280, 720, "slide", "turbo",
    ),
    "slide-bg-creative": (
        "creative colorful presentation background, modern design, "
        "dynamic shapes, 16:9",
        1280, 720, "slide", "turbo",
    ),
    "slide-bg-nature": (
        "soft nature-inspired slide background, leaves and light, calm colors, 16:9",
        1280, 720, "slide", "turbo",
    ),
    "slide-frame-minimal": (
        "minimal decorative border frame, thin elegant lines, white center space",
        1280, 720, "slide", "turbo",
    ),
    "slide-frame-ornate": (
        "ornate decorative border frame, classical style, gold tones, "
        "transparent center",
        1280, 720, "slide", "turbo",
    ),
}


def get_device():
    try:
        import torch
    except ImportError:
        print("❌ torch not installed. Run: pip install torch diffusers transformers accelerate")
        sys.exit(1)

    if torch.cuda.is_available():
        return "cuda", torch.float16
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "mps", torch.float16
    return "cpu", torch.float32


def resolve_config(args):
    """Resolve model, dimensions, prompts from args + preset defaults."""
    style = args.style
    model_key = args.model  # may be None (auto-select)

    # Defaults from preset
    suffix = ""
    neg_cat = "general"
    model_hint = "turbo"
    pw, ph = None, None

    if style and style in PRESETS:
        suffix, pw, ph, neg_cat, model_hint = PRESETS[style]

    # Dimensions: user override > preset > fallback
    if args.width is not None or args.height is not None:
        width = args.width or (pw or 768)
        height = args.height or (ph or 768)
    elif pw and ph:
        width, height = pw, ph
    else:
        width, height = 768, 768

    # Auto-select model from style hint; user --model overrides
    if model_key is None:
        model_key = model_hint
    model_cfg = MODELS.get(model_key, MODELS["turbo"])

    # Custom model ID overrides everything
    model_id = args.model_id or model_cfg["id"]

    # Build full prompt
    parts = [args.prompt]
    if suffix:
        parts.append(suffix)
    parts.append("no text, no letters, no words, no watermark")
    full_prompt = ", ".join(parts)

    # Build negative prompt (only for models that support it)
    negative = args.negative
    if negative is None and model_cfg["negative_ok"]:
        negative = NEG_CHARACTER if neg_cat == "character" else NEG_GENERAL
    if not model_cfg["negative_ok"]:
        negative = None  # turbo models ignore negative prompts

    # Steps: user override > model default
    steps = args.steps if args.steps else model_cfg["steps"]

    return {
        "model_id": model_id,
        "model_key": model_key,
        "full_prompt": full_prompt,
        "negative_prompt": negative,
        "width": width,
        "height": height,
        "steps": steps,
        "guidance": model_cfg["guidance"],
    }


def _is_nan_image(image):
    """Check if generated image is NaN/corrupted (all-zero pixels)."""
    import numpy as np
    arr = np.array(image)
    return arr.max() == 0


def _run_txt2img(config, seed, device, dtype):
    """Run txt2img pipeline on specified device. Returns (image, pipe)."""
    from diffusers import AutoPipelineForText2Image
    import torch

    w, h = config["width"], config["height"]
    variant = "fp16" if device != "cpu" else None
    d_type = dtype if device != "cpu" else torch.float32

    pipe = AutoPipelineForText2Image.from_pretrained(
        config["model_id"],
        torch_dtype=d_type,
        variant=variant,
        safety_checker=None,
    )
    pipe = pipe.to(device)

    if hasattr(pipe, "enable_attention_slicing"):
        pipe.enable_attention_slicing()

    generator = None
    if seed is not None:
        gen_device = "cpu" if device == "mps" else device
        generator = torch.Generator(device=gen_device).manual_seed(seed)

    kwargs = {
        "prompt": config["full_prompt"],
        "guidance_scale": config["guidance"],
        "num_inference_steps": config["steps"],
        "width": w,
        "height": h,
        "generator": generator,
    }
    if config["negative_prompt"]:
        kwargs["negative_prompt"] = config["negative_prompt"]

    image = pipe(**kwargs).images[0]
    del pipe
    return image


def generate_txt2img(config, output_path, seed, device, dtype):
    """Standard text-to-image generation with MPS NaN auto-fallback to CPU."""
    import torch

    w, h = config["width"], config["height"]
    print(f"🖥️  Device: {device} | Model: {config['model_key']} ({config['model_id'].split('/')[-1]}) "
          f"| Size: {w}x{h} | Steps: {config['steps']}")
    if device == "cpu":
        print("⚠️  CPU mode — generation may take 2–10 minutes.")
    if config["negative_prompt"]:
        print(f"🚫 Negative: {config['negative_prompt'][:80]}…")

    t0 = time.time()
    image = _run_txt2img(config, seed, device, dtype)

    # MPS NaN detection: if image is all-zero, fallback to CPU
    if device == "mps" and _is_nan_image(image):
        print("⚠️  MPS produced NaN image — falling back to CPU (slower but reliable)…")
        if hasattr(torch.backends, "mps") and hasattr(torch.mps, "empty_cache"):
            torch.mps.empty_cache()
        import gc; gc.collect()
        image = _run_txt2img(config, seed, "cpu", dtype)
        device = "cpu"

    os.makedirs(os.path.dirname(os.path.abspath(output_path)) or ".", exist_ok=True)
    image.save(output_path)

    size_kb = os.path.getsize(output_path) // 1024
    elapsed = time.time() - t0
    print(f"✅ Saved: {output_path} ({size_kb} KB, {w}x{h}px, {elapsed:.0f}s, device: {device})")
    return image


def generate_img2img(config, reference_path, strength, output_path, seed, device, dtype):
    """Image-to-image generation for character consistency.

    Workflow: generate a canonical character view first (txt2img), then use it
    as --reference for subsequent poses. Strength 0.45-0.65 preserves identity
    while allowing pose/expression changes.
    """
    from diffusers import AutoPipelineForImage2Image
    from diffusers.utils import load_image
    import torch

    w, h = config["width"], config["height"]
    print(f"🖥️  Device: {device} | Model: {config['model_key']} | Ref: {reference_path} "
          f"| Strength: {strength} | Steps: {config['steps']}")

    variant = "fp16" if device != "cpu" else None
    pipe = AutoPipelineForImage2Image.from_pretrained(
        config["model_id"],
        torch_dtype=dtype,
        variant=variant,
        safety_checker=None,
    )
    pipe = pipe.to(device)

    if hasattr(pipe, "enable_attention_slicing"):
        pipe.enable_attention_slicing()

    ref_image = load_image(reference_path).resize((w, h))

    generator = None
    if seed is not None:
        generator = torch.Generator(device=device).manual_seed(seed)

    kwargs = {
        "prompt": config["full_prompt"],
        "image": ref_image,
        "strength": strength,
        "guidance_scale": config["guidance"],
        "num_inference_steps": config["steps"],
        "generator": generator,
    }
    if config["negative_prompt"]:
        kwargs["negative_prompt"] = config["negative_prompt"]

    t0 = time.time()
    image = pipe(**kwargs).images[0]

    os.makedirs(os.path.dirname(os.path.abspath(output_path)) or ".", exist_ok=True)
    image.save(output_path)

    size_kb = os.path.getsize(output_path) // 1024
    elapsed = time.time() - t0
    actual_w, actual_h = image.size
    print(f"✅ Saved: {output_path} ({size_kb} KB, {actual_w}x{actual_h}px, {elapsed:.0f}s, device: {device})")
    return image


def main():
    parser = argparse.ArgumentParser(
        description="AI Image Generation v2.0 — SDXL multi-model",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--prompt", help="Text description of the image")
    parser.add_argument("--style", default=None, help="Style preset (see --list-styles)")
    parser.add_argument("--model", default=None, choices=["turbo", "quality", "legacy"],
                        help="Model tier: turbo (fast ~6s), quality (detailed ~60s), legacy (sd-turbo)")
    parser.add_argument("--model-id", default=None,
                        help="Custom HuggingFace model ID (overrides --model)")
    parser.add_argument("--negative", default=None,
                        help="Negative prompt (auto-set for quality model character styles)")
    parser.add_argument("--width", type=int, default=None)
    parser.add_argument("--height", type=int, default=None)
    parser.add_argument("--steps", type=int, default=None, help="Override inference steps")
    parser.add_argument("--seed", type=int, default=None, help="Random seed")
    parser.add_argument("--output", help="Output PNG path")
    parser.add_argument("--reference", default=None,
                        help="Reference image for img2img consistency mode")
    parser.add_argument("--strength", type=float, default=0.55,
                        help="img2img strength: 0.0=copy ref, 1.0=ignore ref (default: 0.55)")
    parser.add_argument("--list-styles", action="store_true")
    args = parser.parse_args()

    if args.list_styles:
        print("Available styles:")
        print(f"  {'NAME':<25} {'SIZE':>9}  {'MODEL':>7}  SUFFIX")
        print("  " + "─" * 80)
        for name, (suffix, w, h, _cat, model) in PRESETS.items():
            print(f"  {name:<25} {w}x{h:>4}  {model:>7}  {suffix[:50]}…")
        return

    if not args.prompt:
        parser.error("--prompt is required")
    if not args.output:
        parser.error("--output is required")

    device, dtype = get_device()
    config = resolve_config(args)

    if args.reference:
        generate_img2img(config, args.reference, args.strength,
                         args.output, args.seed, device, dtype)
    else:
        generate_txt2img(config, args.output, args.seed, device, dtype)


if __name__ == "__main__":
    main()
