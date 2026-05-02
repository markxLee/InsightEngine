#!/usr/bin/env python3
"""
LoRA training for SD 1.5 — cross-platform (CUDA/MPS/CPU), fp32 on MPS.

Train a character LoRA from a small set of images (5-20) using a trigger token.
Produces a .safetensors adapter file (~6 MB) compatible with diffusers + peft.

Usage:
    python3 .github/skills/gen-image/scripts/train_lora.py \
        --dataset path/to/dataset/ \
        --output path/to/lora/ \
        --trigger "bwmanga_boy" \
        --steps 500 --lr 1e-4 --rank 8

Dataset structure:
    dataset/
        image1.png  +  image1.txt  (caption with trigger token)
        image2.png  +  image2.txt
        ...

Requirements: diffusers, transformers, peft, torch, safetensors, Pillow
"""

import argparse
import gc
import os
import time
from pathlib import Path

import torch
from PIL import Image


def get_device():
    if torch.cuda.is_available():
        return "cuda"
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def cleanup_device(device):
    gc.collect()
    if device == "mps" and torch.backends.mps.is_available():
        torch.mps.empty_cache()
    elif device == "cuda":
        torch.cuda.empty_cache()


class SimpleDataset(torch.utils.data.Dataset):
    """Load image-caption pairs from a directory."""

    def __init__(self, data_dir: str, tokenizer, size: int = 512):
        self.data_dir = Path(data_dir)
        self.tokenizer = tokenizer
        self.size = size

        self.items = []
        for img_path in sorted(self.data_dir.glob("*.png")):
            txt_path = img_path.with_suffix(".txt")
            if txt_path.exists():
                self.items.append((img_path, txt_path))

        if not self.items:
            raise ValueError(f"No image+caption pairs found in {data_dir}")
        print(f"  Dataset: {len(self.items)} image-caption pairs")

    def __len__(self):
        return len(self.items)

    def __getitem__(self, idx):
        img_path, txt_path = self.items[idx]

        img = Image.open(img_path).convert("RGB")
        img = img.resize((self.size, self.size), Image.LANCZOS)

        import numpy as np
        img_array = np.array(img).astype(np.float32) / 127.5 - 1.0
        img_tensor = torch.from_numpy(img_array).permute(2, 0, 1)

        caption = txt_path.read_text().strip()
        tokens = self.tokenizer(
            caption,
            padding="max_length",
            max_length=self.tokenizer.model_max_length,
            truncation=True,
            return_tensors="pt",
        )

        return {
            "pixel_values": img_tensor,
            "input_ids": tokens.input_ids.squeeze(0),
        }


def main():
    parser = argparse.ArgumentParser(description="Train LoRA for SD 1.5")
    parser.add_argument("--dataset", required=True, help="Dataset directory (images + .txt captions)")
    parser.add_argument("--output", required=True, help="Output directory for LoRA weights")
    parser.add_argument("--trigger", type=str, default="bwmanga_boy", help="Trigger token")
    parser.add_argument("--steps", type=int, default=500, help="Training steps")
    parser.add_argument("--lr", type=float, default=1e-4, help="Learning rate")
    parser.add_argument("--rank", type=int, default=8, help="LoRA rank")
    parser.add_argument("--batch-size", type=int, default=1, help="Batch size")
    parser.add_argument("--save-every", type=int, default=100, help="Checkpoint interval")
    parser.add_argument("--resolution", type=int, default=512, help="Training resolution")
    parser.add_argument("--sd-path", type=str, default="/tmp/sd15", help="SD 1.5 model path")
    args = parser.parse_args()

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    device = get_device()
    # fp32 required on MPS (fp16 produces NaN); fp16 fine on CUDA
    dtype = torch.float16 if device == "cuda" else torch.float32

    print("=" * 60)
    print(f"LoRA Training — SD 1.5 on {device} {dtype}")
    print("=" * 60)
    print(f"  Device: {device}")
    print(f"  Dataset: {args.dataset}")
    print(f"  Trigger: {args.trigger}")
    print(f"  Steps: {args.steps}")
    print(f"  LR: {args.lr}")
    print(f"  LoRA rank: {args.rank}")
    print(f"  Resolution: {args.resolution}")
    print(f"  Output: {args.output}")
    print()

    # Load models
    print("Loading models...")
    t0 = time.time()

    from diffusers import AutoencoderKL, DDPMScheduler, UNet2DConditionModel
    from transformers import CLIPTextModel, CLIPTokenizer

    tokenizer = CLIPTokenizer.from_pretrained(os.path.join(args.sd_path, "tokenizer"))
    text_encoder = CLIPTextModel.from_pretrained(
        os.path.join(args.sd_path, "text_encoder"), torch_dtype=dtype
    ).to(device)
    vae = AutoencoderKL.from_pretrained(
        os.path.join(args.sd_path, "vae"), torch_dtype=dtype
    ).to(device)
    unet = UNet2DConditionModel.from_pretrained(
        os.path.join(args.sd_path, "unet"), torch_dtype=dtype
    ).to(device)
    noise_scheduler = DDPMScheduler.from_pretrained(
        os.path.join(args.sd_path, "scheduler")
    )

    print(f"  Models loaded: {time.time() - t0:.1f}s")

    # Freeze VAE and text encoder
    vae.requires_grad_(False)
    text_encoder.requires_grad_(False)

    # Add LoRA to UNet
    print(f"  Adding LoRA (rank={args.rank})...")
    from peft import LoraConfig

    lora_config = LoraConfig(
        r=args.rank,
        lora_alpha=args.rank,
        init_lora_weights="gaussian",
        target_modules=["to_k", "to_q", "to_v", "to_out.0"],
    )
    unet.add_adapter(lora_config)

    trainable = sum(p.numel() for p in unet.parameters() if p.requires_grad)
    total = sum(p.numel() for p in unet.parameters())
    print(f"  LoRA params: {trainable:,} / {total:,} ({100 * trainable / total:.2f}%)")

    # Setup dataset
    print("Loading dataset...")
    dataset = SimpleDataset(args.dataset, tokenizer, size=args.resolution)
    dataloader = torch.utils.data.DataLoader(
        dataset, batch_size=args.batch_size, shuffle=True, num_workers=0,
    )

    # Optimizer
    optimizer = torch.optim.AdamW(
        [p for p in unet.parameters() if p.requires_grad],
        lr=args.lr, weight_decay=1e-2,
    )

    # Training loop
    print(f"\nStarting training ({args.steps} steps)...")
    print("-" * 60)

    unet.train()
    global_step = 0
    total_loss = 0.0
    t_start = time.time()

    while global_step < args.steps:
        for batch in dataloader:
            if global_step >= args.steps:
                break

            pixel_values = batch["pixel_values"].to(device, dtype=dtype)
            input_ids = batch["input_ids"].to(device)

            with torch.no_grad():
                latents = vae.encode(pixel_values).latent_dist.sample()
                latents = latents * vae.config.scaling_factor

            noise = torch.randn_like(latents)
            bsz = latents.shape[0]
            timesteps = torch.randint(
                0, noise_scheduler.config.num_train_timesteps,
                (bsz,), device=device
            ).long()
            noisy_latents = noise_scheduler.add_noise(latents, noise, timesteps)

            with torch.no_grad():
                encoder_hidden_states = text_encoder(input_ids)[0]

            model_pred = unet(noisy_latents, timesteps, encoder_hidden_states).sample
            loss = torch.nn.functional.mse_loss(model_pred, noise, reduction="mean")

            loss.backward()
            torch.nn.utils.clip_grad_norm_(
                [p for p in unet.parameters() if p.requires_grad], 1.0
            )
            optimizer.step()
            optimizer.zero_grad()

            global_step += 1
            total_loss += loss.item()

            if global_step % 10 == 0:
                avg_loss = total_loss / 10
                elapsed = time.time() - t_start
                speed = elapsed / global_step
                eta = speed * (args.steps - global_step)
                print(f"  Step {global_step:4d}/{args.steps} | "
                      f"loss={avg_loss:.4f} | "
                      f"{speed:.1f}s/step | "
                      f"ETA {eta:.0f}s")
                total_loss = 0.0

            if args.save_every > 0 and global_step % args.save_every == 0:
                ckpt_dir = out / f"checkpoint-{global_step}"
                ckpt_dir.mkdir(exist_ok=True)
                unet.save_attn_procs(str(ckpt_dir))
                print(f"  💾 Checkpoint saved: {ckpt_dir}")

            if global_step % 50 == 0:
                cleanup_device(device)

    # Save final LoRA weights
    elapsed = time.time() - t_start
    print(f"\n{'=' * 60}")
    print(f"Training complete! {args.steps} steps in {elapsed:.0f}s ({elapsed/args.steps:.1f}s/step)")
    print(f"{'=' * 60}")

    final_dir = out / "final"
    final_dir.mkdir(exist_ok=True)

    from peft import get_peft_model_state_dict
    lora_state_dict = get_peft_model_state_dict(unet)
    torch.save(lora_state_dict, final_dir / "lora_weights.pt")

    try:
        from safetensors.torch import save_file
        save_file(lora_state_dict, final_dir / "lora_weights.safetensors")
        weights_path = final_dir / "lora_weights.safetensors"
    except ImportError:
        weights_path = final_dir / "lora_weights.pt"

    config_text = (
        f"trigger: {args.trigger}\n"
        f"rank: {args.rank}\n"
        f"lr: {args.lr}\n"
        f"steps: {args.steps}\n"
        f"resolution: {args.resolution}\n"
        f"dataset_size: {len(dataset)}\n"
        f"training_time: {elapsed:.0f}s\n"
        f"base_model: {args.sd_path}\n"
    )
    (final_dir / "config.txt").write_text(config_text)

    fsize = os.path.getsize(weights_path)
    print(f"  LoRA weights: {weights_path} ({fsize:,} bytes, {fsize/1024/1024:.1f} MB)")
    print(f"  Trigger token: '{args.trigger}'")
    print(f"  Output: {final_dir}")


if __name__ == "__main__":
    main()
