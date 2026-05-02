#!/usr/bin/env python3
"""
LoRA inference — load trained LoRA weights and generate images with trigger token.
Generates baseline (no LoRA) + test images (with LoRA) for comparison.

Usage:
    python3 .github/skills/gen-image/scripts/lora_inference.py \
        --lora path/to/lora/final/ \
        --trigger "bwmanga_boy" \
        --output path/to/inference/ \
        --steps 25 --seed 42 --lora-scale 0.8

Requirements: diffusers, transformers, peft, torch, safetensors, Pillow
"""

import argparse
import os
import time
from pathlib import Path

import torch


def get_device():
    if torch.cuda.is_available():
        return "cuda"
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def main():
    parser = argparse.ArgumentParser(description="LoRA inference test")
    parser.add_argument("--lora", required=True, help="Path to LoRA weights directory")
    parser.add_argument("--trigger", type=str, default="bwmanga_boy", help="Trigger token")
    parser.add_argument("--prompt", type=str, default=None,
                        help="Custom prompt (trigger token auto-inserted if missing)")
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument("--steps", type=int, default=25, help="Inference steps")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--num-images", type=int, default=4, help="Number of test images")
    parser.add_argument("--sd-path", type=str, default="/tmp/sd15", help="SD 1.5 model path")
    parser.add_argument("--lora-scale", type=float, default=0.8, help="LoRA strength (0.0-1.0)")
    parser.add_argument("--width", type=int, default=512, help="Image width")
    parser.add_argument("--height", type=int, default=768, help="Image height")
    args = parser.parse_args()

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    device = get_device()
    # fp32 required on MPS; fp16 fine on CUDA
    dtype = torch.float16 if device == "cuda" else torch.float32

    print("=" * 60)
    print("LoRA Inference Test")
    print("=" * 60)
    print(f"  Device: {device}")
    print(f"  LoRA: {args.lora}")
    print(f"  Trigger: {args.trigger}")
    print(f"  LoRA scale: {args.lora_scale}")
    print()

    # Load SD 1.5 pipeline
    print("Loading SD 1.5...")
    t0 = time.time()

    from diffusers import (
        AutoencoderKL,
        EulerDiscreteScheduler,
        StableDiffusionPipeline,
        UNet2DConditionModel,
    )
    from transformers import CLIPTextModel, CLIPTokenizer

    tokenizer = CLIPTokenizer.from_pretrained(os.path.join(args.sd_path, "tokenizer"))
    text_encoder = CLIPTextModel.from_pretrained(
        os.path.join(args.sd_path, "text_encoder"), torch_dtype=dtype
    )
    vae = AutoencoderKL.from_pretrained(
        os.path.join(args.sd_path, "vae"), torch_dtype=dtype
    )
    unet = UNet2DConditionModel.from_pretrained(
        os.path.join(args.sd_path, "unet"), torch_dtype=dtype
    )
    # EulerDiscreteScheduler is required on MPS to avoid NaN
    scheduler = EulerDiscreteScheduler.from_pretrained(
        os.path.join(args.sd_path, "scheduler")
    )

    pipe = StableDiffusionPipeline(
        unet=unet, vae=vae, text_encoder=text_encoder,
        tokenizer=tokenizer, scheduler=scheduler,
        safety_checker=None, feature_extractor=None,
        requires_safety_checker=False,
    )
    print(f"  SD 1.5 loaded: {time.time() - t0:.1f}s")

    # Load LoRA weights
    print("Loading LoRA weights...")
    t0 = time.time()

    from peft import LoraConfig, set_peft_model_state_dict

    lora_config = LoraConfig(
        r=8, lora_alpha=8,
        init_lora_weights="gaussian",
        target_modules=["to_k", "to_q", "to_v", "to_out.0"],
    )
    pipe.unet.add_adapter(lora_config)

    lora_dir = Path(args.lora)
    weights_path = lora_dir / "lora_weights.safetensors"
    if weights_path.exists():
        from safetensors.torch import load_file
        state_dict = load_file(str(weights_path))
    else:
        weights_path = lora_dir / "lora_weights.pt"
        if weights_path.exists():
            state_dict = torch.load(str(weights_path), map_location="cpu")
        else:
            raise FileNotFoundError(f"No LoRA weights found in {lora_dir}")

    set_peft_model_state_dict(pipe.unet, state_dict)
    print(f"  LoRA loaded: {time.time() - t0:.1f}s")

    pipe = pipe.to(device)

    # Build prompts
    neg = "blurry, low quality, deformed, extra limbs, watermark, text, bad anatomy"

    if args.prompt:
        base_prompt = args.prompt
    else:
        base_prompt = f"{args.trigger}, manga, monochrome, greyscale, black and white, clean lineart, masterpiece"

    if args.trigger not in base_prompt:
        base_prompt = f"{args.trigger}, {base_prompt}"

    test_prompts = [
        f"{base_prompt}, full body, standing, front view, white background",
        f"{base_prompt}, full body, walking, side view, white background",
        f"{base_prompt}, upper body, portrait, looking at viewer",
        f"{base_prompt}, full body, sitting on chair, relaxed pose",
    ]

    # Generate baseline (no LoRA)
    print("\n--- Generating WITHOUT LoRA (baseline) ---")
    pipe.unet.disable_adapters()
    gen = torch.Generator(device="cpu").manual_seed(args.seed)
    t0 = time.time()
    baseline = pipe(
        prompt=test_prompts[0], negative_prompt=neg,
        num_inference_steps=args.steps, guidance_scale=7.5,
        generator=gen, width=args.width, height=args.height,
    ).images[0]
    elapsed = time.time() - t0
    baseline_path = out / "baseline_no_lora.png"
    baseline.save(baseline_path)
    fsize = os.path.getsize(baseline_path)
    print(f"  ✅ {baseline_path.name} ({fsize:,} bytes, {elapsed:.0f}s)")

    # Generate with LoRA
    print(f"\n--- Generating WITH LoRA (scale={args.lora_scale}) ---")
    pipe.unet.enable_adapters()

    for i, prompt in enumerate(test_prompts[:args.num_images]):
        gen = torch.Generator(device="cpu").manual_seed(args.seed + i)
        t0 = time.time()
        img = pipe(
            prompt=prompt, negative_prompt=neg,
            num_inference_steps=args.steps, guidance_scale=7.5,
            generator=gen, width=args.width, height=args.height,
            cross_attention_kwargs={"scale": args.lora_scale},
        ).images[0]
        elapsed = time.time() - t0

        fname = f"lora_test_{i:02d}.png"
        img.save(out / fname)
        fsize = os.path.getsize(out / fname)
        print(f"  ✅ {fname} ({fsize:,} bytes, {elapsed:.0f}s)")
        print(f"     Prompt: {prompt[:80]}...")

    print(f"\n{'=' * 60}")
    print(f"Inference complete! {args.num_images + 1} images generated")
    print(f"  Output: {out}")
    print(f"  Compare baseline vs LoRA images to evaluate training quality")


if __name__ == "__main__":
    main()
