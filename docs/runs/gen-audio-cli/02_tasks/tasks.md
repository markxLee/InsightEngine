# Task Plan: gen-audio CLI TTS Skill

## Task List

### T-001: Create tools/tts/ package with audio utilities
**Files**: `tools/tts/__init__.py`, `tools/tts/audio_utils.py`
**Source**: Extract from BetterBox-TTS `general/general_tool_audio.py` + `general/noise_detect_VAD.py`
**Scope**: segment_text, normalize_text, clearText, fix_silent_and_speed_audio, create_srt_file, VAD trim
**Blocked by**: None

### T-002: Create tools/tts/omni_engine.py
**Files**: `tools/tts/omni_engine.py`
**Source**: Extract from BetterBox-TTS `OmniVoice/omnivoice_inference/ttsOmni.py`
**Scope**: Omni class (model loading), generate_speech_omni function, remove Gradio dependencies
**Blocked by**: T-001

### T-003: Create scripts/tts_generate.py CLI
**Files**: `scripts/tts_generate.py`
**Scope**: argparse CLI, orchestrate engine call, save WAV+SRT, print summary
**Blocked by**: T-001, T-002

### T-004: Create .github/skills/gen-audio/SKILL.md
**Files**: `.github/skills/gen-audio/SKILL.md`
**Scope**: Skill definition with triggers, workflow steps, CLI reference
**Blocked by**: T-003

### T-005: Update dependency files + check_deps.py
**Files**: `requirements-tts.txt`, `scripts/check_deps.py`
**Scope**: Add TTS-specific dependencies, register optional deps in check_deps
**Blocked by**: None

### T-006: Copy Silero VAD model + bundle default voice
**Files**: `tools/tts/silero_vad/silero_vad.jit`, `input/voices/default.wav`
**Scope**: Copy VAD model from BetterBox-TTS, copy default ref voice
**Blocked by**: None

## Execution Order
T-001 → T-002 → T-003 → T-004 (sequential, dependent)
T-005, T-006 (parallel, independent)
