# Solution Design: gen-audio CLI TTS Skill

## 0.1 Request Analysis

### Problem Statement
InsightEngine can synthesize content and export to Word, Excel, PDF, PowerPoint, HTML, and images — but has no audio output capability. The `gen-audio/` skill folder exists but is empty. BetterBox-TTS provides excellent Vietnamese TTS via OmniVoice and Viterbox engines, but is locked into a Gradio UI — unusable as a Copilot skill.

### Context
- **Current state**: No TTS capability in InsightEngine. gen-audio/ folder is empty placeholder.
- **Desired state**: Copilot calls `python scripts/tts_generate.py --text "..." --output output/audio.wav` and gets WAV + SRT output. Fits into synthesize pipeline.

### Affected Areas
- **InsightEngine only** — single root, no cross-root impact
- New files: `scripts/tts_generate.py`, `.github/skills/gen-audio/SKILL.md`, `tools/tts/` engine code
- Modified files: `scripts/check_deps.py` (add TTS to optional deps), `requirements.txt` (uncomment torch)

### Assumptions
1. OmniVoice is the default engine (auto-downloads from HuggingFace, portable)
2. Viterbox is optional (requires manual model download)
3. TTS deps (torch, torchaudio ~1.4GB) are separate/optional — won't break existing users
4. Model weights cached in `~/.cache/huggingface/` (not in repo)
5. Reference voice files in `input/voices/`
6. OmniVoice code vendored (not pip-installable as standalone package)

## 0.2 Solution Research

### Existing Patterns Found
- **gen-image skill**: Already handles optional torch dependency. Uses `scripts/gen_image.py` CLI pattern with argparse. Good model to follow.
- **scripts/ convention**: All scripts use `#!/usr/bin/env python3`, docstring with usage, print output path + size as last line.
- **check_deps.py**: Has OPTIONAL_PYTHON list with torch, diffusers, etc. Can add torchaudio, librosa.
- **requirements.txt**: Already has commented-out torch section.

### Dependencies
- **Must add**: `torchaudio`, `librosa`, `soundfile`, `pydub`, `pedalboard`, `s3tokenizer`, `conformer`, `resemble-perth`, `omegaconf`, `einops`
- **Already in requirements.txt (commented)**: `torch`, `diffusers`, `transformers`, `accelerate`
- **System**: `libsndfile`, `ffmpeg` (brew install)

## 0.3 Solution Design

### Solution Overview
Extract OmniVoice inference pipeline from BetterBox-TTS into `tools/tts/` as a vendored library. Create a thin CLI script `scripts/tts_generate.py` that Copilot calls. Create `gen-audio/SKILL.md` that teaches Copilot when/how to use it.

### Approach Comparison

| Aspect | Option A: Vendored copy | Option B: Git submodule | Option C: pip package |
|--------|------------------------|------------------------|----------------------|
| Portability | ✅ Clone and run | ❌ Submodule complexity | ❌ Package not published |
| Maintainability | ⚠️ Manual sync | ⚠️ Submodule updates | ✅ Version pinned |
| Simplicity | ✅ Self-contained | ❌ Git knowledge needed | ❌ Publishing overhead |
| **Chosen** | **✅ Yes** | No | No |

**Decision: Option A (vendored copy)** — OmniVoice is not published as a pip package, and the code needs modifications (remove Gradio deps, fix offline mode, simplify imports). A clean vendored copy in `tools/tts/` is the simplest portable solution.

### Component Responsibilities

```
scripts/tts_generate.py          # CLI entrypoint (argparse, orchestration)
  └── tools/tts/
      ├── __init__.py             # Package init
      ├── omni_engine.py          # OmniVoice loading + inference wrapper
      ├── audio_utils.py          # segment_text, normalize, VAD, SRT, silence fix
      └── silero_vad/             # Local Silero VAD model (~11MB, vendored)
```

### Error Handling
- Missing torch: Clear error message + install instructions
- Missing model: Auto-download from HuggingFace on first run
- No GPU: Fallback to CPU with warning (slower but works)
- No reference voice: Use bundled default voice from `input/voices/`

### Rollback Plan
- All new files, nothing modified in existing code except check_deps.py
- `git revert` or delete new files to rollback
