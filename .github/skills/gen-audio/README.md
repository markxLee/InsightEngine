# gen-audio — Text-to-Speech Skill

Generate professional Vietnamese/English speech audio from text. Runs **100% locally** on Apple Silicon — $0 cost, no cloud API.

---

## Engines

| Engine | Best for | Voice quality | Speed (MPS) |
|--------|----------|--------------|-------------|
| `omni` (default) | Quick jobs, short reference (3-10s WAV) | Good | ~1-2s/phrase |
| `viterbox` | Maximum voice similarity | Excellent | ~1-2s/phrase |

---

## Quick Start

```bash
cd /path/to/InsightEngine
source /path/to/venv/bin/activate

# Vietnamese TTS — OmniVoice (fast)
python3 scripts/tts_generate.py --text "Xin chào Việt Nam" --output output/hello.wav

# Viterbox — highest voice fidelity
python3 scripts/tts_generate.py \
  --engine viterbox \
  --voice tools/tts/voices/Phong_Dao.conds.pt \
  --text "Nội dung cần đọc" \
  --output output/result.wav
```

---

## Full CLI Reference

```bash
python3 scripts/tts_generate.py [OPTIONS]
```

### Required (one of)
| Arg | Description |
|-----|-------------|
| `--text TEXT` | Text to speak inline |
| `--file PATH` | Read text from file |

### Common Options
| Arg | Default | Description |
|-----|---------|-------------|
| `--output PATH` | `output/tts_output.wav` | Output WAV file path |
| `--engine` | `omni` | TTS engine: `omni` or `viterbox` |
| `--voice PATH` | auto | `.wav` ref (omni) or `.conds.pt` profile (viterbox) |
| `--lang` | `vi` | Language: `vi` or `en` |
| `--speed` | `1.0` | Speech speed: 0.7 (slow) → 1.5 (fast) |
| `--pitch` | `1.0` | Pitch shift: 0.5 (low) → 2.0 (high) |
| `--device` | auto | `mps` / `cuda` / `cpu` |

### Viterbox-only Options
| Arg | Default | Description |
|-----|---------|-------------|
| `--exaggeration` | `2.0` | Emotion intensity: 0.5 (flat) → 3.0 (very expressive) |
| `--emotion` | `neutral` | Post-processing emotion profile (see below) |

---

## Emotion & EQ System (Both Engines)

Cả 2 engine đều hỗ trợ 2-layer emotion system:

### Layer 1 — `--exaggeration` (model-level)
Controls how much the TTS model deviates from flat, neutral delivery.

| Value | Effect |
|-------|--------|
| `0.5` | Very flat, robotic |
| `1.0` | Calm, measured |
| `2.0` | Natural expressive (**default**) |
| `3.0` | Highly dramatic |

```bash
# Calm narration
python3 scripts/tts_generate.py --exaggeration 1.0 \
  --text "Đây là nội dung bình thường" --output output/calm.wav

# Dramatic reading
python3 scripts/tts_generate.py --exaggeration 3.0 \
  --text "Đây là khoảnh khắc quan trọng!" --output output/dramatic.wav
```

### Layer 2 — `--emotion` (post-processing amplitude envelope)
Applied **after** generation via Pedalboard on **both engines**. Changes volume dynamics, not voice character.

| Profile | Effect | Use case |
|---------|--------|----------|
| `neutral` (default) | No change | Standard narration |
| `sad` | Volume fades -10% over sentence | Melancholic tone |
| `question` | Volume surges +40% at last 20% of sentence | Rising intonation for questions |

```bash
# Sad/melancholic reading (both engines)
python3 scripts/tts_generate.py --emotion sad \
  --text "Câu chuyện buồn..." --output output/sad.wav

# Question intonation (both engines)
python3 scripts/tts_generate.py --emotion question \
  --text "Thật không đấy?" --output output/question.wav
```

### Layer 2 — EQ (automatic with emotion)
When `--emotion` is set (non-neutral), audio automatically goes through Pedalboard on **both engines**:
- **HighpassFilter** at 40Hz — removes DC/rumble
- **Limiter** at -1dBFS — prevents clipping

No manual EQ knobs exposed (by design — keeps voice character authentic).

---

## Voice Profiles (Viterbox)

Pre-built `.conds.pt` files in `tools/tts/voices/`:

| File | Voice | Built from |
|------|-------|------------|
| `Phong_Dao.conds.pt` | Phong Dao (male, Vietnamese) | ~24s reference audio |

### Build a New Voice Profile

```bash
cd /path/to/InsightEngine

# 1. Put 1+ WAV files (clean speech, same speaker) in a folder
mkdir -p tmp/my_voice_wavs
# copy your WAV files into tmp/my_voice_wavs/

# 2. Build conds.pt
cd tools/tts/viterbox
PYTHONPATH=/path/to/BetterBox-TTS python3 pretrain_voice_builder.py \
  --pretrained_dir ../../../tmp/my_voice_wavs \
  --output_dir ../../../tmp/my_voice_output \
  --copy_to_model

# 3. Move conds.pt to voices/
cp ../../../tmp/my_voice_output/conds.pt ../voices/MySpeaker.conds.pt
```

> **Quality tip**: More audio = better voice similarity. 20+ minutes is ideal.

---

## Output

Every run produces:
- **`<output>.wav`** — 24kHz mono float32 audio
- **`<output>.srt`** — Subtitle file with timestamps
- **stdout last line**: `📁 output/file.wav (XXX KB, X.Xs)` — required by InsightEngine pipeline

---

## Pipeline Integration

```yaml
# compose text → gen-audio → embed in slide
compose: "Tổng hợp nội dung báo cáo" → output: tmp/report_text.txt
gen-audio:
  engine: viterbox
  file: tmp/report_text.txt
  voice: tools/tts/voices/Phong_Dao.conds.pt
  output: output/report_narration.wav
  speed: 1.0
  exaggeration: 2.0
```

---

## Technical Architecture

```
tts_generate.py (CLI entrypoint)
  ├── omni_engine.py       → OmniVoice (CosyVoice-based, zero-shot cloning)
  └── viterbox_engine.py   → Viterbox (Chatterbox-based, .conds.pt profiles)
       ├── tools/tts/viterbox/    (vendored package — no BetterBox-TTS dependency)
       │    ├── tts.py            (Viterbox main class)
       │    ├── tts_helper/
       │    │    ├── tts_extension.py   (EQ + emotion processing via Pedalboard)
       │    │    └── tts_TTSConds.py    (voice profile loader)
       │    └── modelViterboxLocal/     (model weights, gitignored)
       └── tools/tts/general/
            └── EQ_emotion_config/
                 └── eq_emotional_profiles.py  (Pedalboard chains + amplitude envelopes)
```

### Emotion Processing Flow
```
Text → Viterbox generate (exaggeration controls model expressiveness)
     → raw WAV chunks
     → [if emotion set] Pedalboard EQ (cleanup + safety)
     → [if emotion set] Amplitude envelope (sad/question dynamics)
     → concat chunks with silence padding
     → final WAV output
```

---

## Limitations

| Limitation | Workaround |
|------------|-----------|
| Voice similarity low with short ref (<30s) | Provide longer reference audio for `conds.pt` |
| First run downloads ~3.2GB model | Cached in `tools/tts/viterbox/modelViterboxLocal/` |
| Only 2 emotion profiles (`sad`, `question`) | Add new profiles in `general/EQ_emotion_config/eq_emotional_profiles.py` |
| Vietnamese primary; English less optimized | Use `--lang en` but expect lower quality |
| MPS (Apple Silicon) required for fast inference | CPU works but ~5-10x slower |

---

## Dependencies

```
torch + torchaudio    (~1.4GB)
soundfile
librosa
pedalboard            (EQ/audio processing)
safetensors
huggingface_hub       (model download)
pydub
```

Install: `pip install torch torchaudio soundfile librosa pedalboard safetensors huggingface_hub pydub`
