# Specification: gen-audio CLI TTS Skill

## 1. Functional Requirements

### FR-1: CLI Text-to-Speech Generation
- The system SHALL accept text input via `--text` argument or `--file` (reads text file)
- The system SHALL generate a WAV audio file at the specified `--output` path
- The system SHALL auto-generate an SRT subtitle file alongside the WAV
- The system SHALL print the output file path and size as the last line of stdout

### FR-2: Voice Selection
- The system SHALL accept `--voice <path>` to specify a reference voice WAV file
- The system SHALL fall back to a default bundled voice if no `--voice` specified
- The system SHALL support voice cloning from any WAV file (3-10 seconds ideal)

### FR-3: Engine Selection
- The system SHALL default to OmniVoice engine
- The system SHALL accept `--model omni` or `--model viterbox` to select engine
- The system SHALL auto-download OmniVoice model from HuggingFace on first run

### FR-4: Audio Parameters
- The system SHALL accept `--speed` (0.7-1.5, default 1.0) for speech rate
- The system SHALL accept `--pitch` (0.5-2.0, default 1.0) for pitch shift
- The system SHALL accept `--lang` (vi/en, default vi) for language

### FR-5: SKILL.md Integration
- gen-audio/SKILL.md SHALL define triggers for Copilot
- Copilot SHALL be able to chain: compose output → gen-audio → deliver WAV

## 2. Non-Functional Requirements

### NFR-1: Portability
- SHALL work on fresh clone + pip install + run (no manual setup beyond deps)
- SHALL auto-detect GPU: CUDA > MPS > CPU

### NFR-2: Output Format
- WAV: 24kHz, mono, float32 (OmniVoice native rate)
- SRT: Standard SRT format with timing per spoken segment

### NFR-3: Performance
- First run: model download (~3-5GB, one-time)
- Subsequent runs: <30s for short text on GPU, <2min on CPU

## 3. Acceptance Criteria

- [ ] AC1: `python scripts/tts_generate.py --text "Xin chào" --output output/test.wav` creates playable WAV
- [ ] AC2: SRT file auto-created at `output/test.srt`
- [ ] AC3: `--voice input/voices/ref.wav` produces speech matching reference voice
- [ ] AC4: `--model omni` works (default)
- [ ] AC5: Works on fresh machine: clone → pip install → run
- [ ] AC6: Last stdout line: path + file size
- [ ] AC7: `--speed 1.2` produces faster speech
- [ ] AC8: `--lang en` generates English speech
