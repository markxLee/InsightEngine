---
description: "Generate speech audio (WAV + SRT) from text using OmniVoice or Viterbox TTS — zero-shot voice cloning, Vietnamese-optimized, runs locally on Apple Silicon ($0 cost)"
triggers:
  - "tạo audio", "đọc text", "text to speech", "tts", "tạo giọng đọc"
  - "generate speech", "narrate", "voiceover", "đọc bài"
  - "tạo file wav", "tạo file âm thanh", "audio từ văn bản"
  - "clone giọng", "voice cloning", "giọng đọc tự động"
  - "đọc báo cáo", "đọc tài liệu", "audio cho slide"
---

# gen-audio — Text-to-Speech Skill

## Purpose

Generate speech audio from text with zero-shot voice cloning. Produces WAV audio + SRT subtitles.
Two engines available — both run locally on GPU/MPS ($0 cost):

| Engine | Best for | Voice quality | Speed |
|--------|----------|--------------|-------|
| `omni` (default) | Quick generation, short refs (3-10s WAV) | Good | Fast |
| `viterbox` | Highest similarity to target voice | Excellent | Slower (~2-5s/word) |

## When to Use

- User wants audio narration from text content
- User says "đọc", "tạo audio", "voiceover", "TTS", "text to speech"
- Pipeline needs audio output (compose → gen-audio)
- User wants to clone a specific voice

## When NOT to Use

- User wants to edit existing audio → use external audio editor
- User wants music or sound effects → not a TTS task
- User wants speech-to-text (reverse direction) → different tool

## Prerequisites

```bash
# TTS dependencies (heavy — ~1.4GB for torch)
pip3 install --user torch torchaudio soundfile librosa pedalboard omnivoice
```

Model auto-downloads from HuggingFace on first run (~3GB, cached in ~/.cache/huggingface/).

## CLI Reference

```bash
# Basic Vietnamese TTS (OmniVoice, default)
python3 scripts/tts_generate.py --text "Xin chào Việt Nam" --output output/hello.wav

# Viterbox engine — highest voice similarity (uses pre-built .conds.pt)
python3 scripts/tts_generate.py \
  --engine viterbox \
  --voice tools/tts/voices/Phong_Dao.conds.pt \
  --text "Nội dung cần đọc" --output output/result.wav

# Read from file
python3 scripts/tts_generate.py --file input/script.txt --output output/narration.wav

# OmniVoice with voice cloning (short WAV ref)
python3 scripts/tts_generate.py --text "Nội dung" --voice tools/tts/voices/my_voice.wav

# English with speed adjustment
python3 scripts/tts_generate.py --text "Hello world" --lang en --speed 1.2

# Full options (OmniVoice)
python3 scripts/tts_generate.py \
  --text "Văn bản cần đọc" \
  --output output/result.wav \
  --voice tools/tts/voices/ref.wav \
  --ref-text "Transcript của voice reference" \
  --lang vi \
  --speed 1.0 \
  --pitch 1.0 \
  --device mps
```

### Arguments

| Arg | Default | Description |
|-----|---------|-------------|
| `--text` | required* | Text to speak |
| `--file` | — | Read text from file (alternative to --text) |
| `--output` | `output/tts_output.wav` | Output WAV path |
| `--engine` | `omni` | TTS engine: `omni` or `viterbox` |
| `--voice` | auto from `tools/tts/voices/` | Reference voice WAV (omni) or `.conds.pt` path (viterbox) |
| `--ref-text` | None | Transcript of reference voice (omni only) |
| `--lang` | `vi` | Language: vi or en |
| `--speed` | `1.0` | Speech speed (0.7-1.5) |
| `--pitch` | `1.0` | Pitch shift (0.5-2.0) |
| `--model` | `k2-fsa/OmniVoice` | HuggingFace model ID |
| `--device` | auto | cuda / mps / cpu |

### Output

- **WAV file**: 24kHz mono float32 at specified `--output` path
- **SRT file**: Auto-generated at same path with `.srt` extension
- **Last stdout line**: File path + size (InsightEngine convention)

## Workflow Steps

### Step 1: Identify Input

Determine text source:
- Direct text from user → use `--text`
- File path provided → use `--file`
- Output from compose skill → read the composed text, pass via `--text` or save to tmp file

### Step 2: Select Engine & Voice

**OmniVoice (default, fast):**
- `--voice tools/tts/voices/<name>.wav` (3-10s clean speech)
- If no voice provided → auto-picks first WAV in `tools/tts/voices/`

**Viterbox (best quality, slower):**
- `--engine viterbox --voice tools/tts/voices/<name>.conds.pt`
- `.conds.pt` = pre-built voice profile from long audio (already in repo)
- Available: `Phong_Dao.conds.pt` (built from 20+ min Phong Dao audio)
- If user wants to add a new voice: run `tools/tts/viterbox/pretrain_voice_builder.py`

### Step 3: Generate

Run the CLI command. First run downloads model (~3GB).

```bash
cd /Users/trucle/Desktop/project/InsightEngine
python3 scripts/tts_generate.py --text "<text>" --output output/<name>.wav
```

### Step 4: Verify & Deliver

- Check output file exists and size > 0
- Report: file path, duration, file size
- If chained: pass WAV path to next skill

## Chaining Examples

```yaml
# Compose text → generate audio
compose: "Tổng hợp nội dung báo cáo" → output: tmp/report_text.txt
gen-audio: --file tmp/report_text.txt --output output/report_narration.wav

# Generate audio → embed in presentation (future)
gen-audio: --text "Slide 1 content" --output output/slide1_audio.wav
```

## Limitations

- First run requires ~3GB model download per engine (cached in `tools/tts/viterbox/modelViterboxLocal/` and `~/.cache/huggingface/`)
- torch + torchaudio ~1.4GB disk space
- GPU recommended (MPS on Mac, CUDA on Linux) — CPU works but slow
- **OmniVoice**: voice quality depends on reference WAV quality (3-10s clean speech ideal)
- **Viterbox**: best quality with pre-built `.conds.pt`; advance_tts mode ~2-5s per word on MPS
- Vietnamese is primary; English supported but less optimized
