"""Audio utilities for TTS pipeline.

Extracted from BetterBox-TTS general/general_tool_audio.py + general/noise_detect_VAD.py
Provides: text segmentation, normalization, silence handling, VAD trim, SRT generation.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import List, Optional

import numpy as np

# ── Pause config ──────────────────────────────────────────
_PUNCT_PAUSE_MS = {
    ".": 450, "!": 450, "?": 450, "。": 450, "！": 450, "？": 450,
    ",": 200, "，": 200, "、": 200,
    ";": 250, "；": 250,
    ":": 200, "：": 200,
    "/": 150, "…": 300, "-": 120, "—": 150, "–": 150,
}

SEGMENT_TEXT = "text"
SEGMENT_PAUSE = "pause"


def _pause_ms_for(punct: str) -> int:
    return _PUNCT_PAUSE_MS.get(punct, 200)


def segment_text(text: str) -> List[dict]:
    """Split text into spoken segments and punctuation pauses."""
    if not text or not text.strip():
        return []

    punct_pattern = r'(\.{2,}|…+|[.!?,;:/—–\-，。？！、；：])'
    raw_parts = re.split(punct_pattern, text)

    segments: List[dict] = []
    for part in raw_parts:
        part_stripped = part.strip()
        if not part_stripped:
            continue

        if re.fullmatch(punct_pattern, part_stripped):
            punct_key = "…" if re.fullmatch(r'\.{2,}|…+', part_stripped) else part_stripped
            segments.append({
                "type": SEGMENT_PAUSE,
                "content": punct_key,
                "pause_ms": _pause_ms_for(punct_key),
            })
        else:
            segments.append({"type": SEGMENT_TEXT, "content": part_stripped})

    # Merge very short text fragments
    MIN_CHARS = 1
    merged: List[dict] = []
    for seg in segments:
        if (
            seg["type"] == SEGMENT_TEXT
            and len(seg["content"]) < MIN_CHARS
            and merged
            and merged[-1]["type"] == SEGMENT_TEXT
        ):
            merged[-1]["content"] = merged[-1]["content"] + " " + seg["content"]
        else:
            merged.append(seg)

    return merged


def clear_text(text: str) -> str:
    """Clean text: lowercase, remove special chars, keep words."""
    text = text.casefold()
    original = text
    text = re.sub(r'[!@#$%^&*()_+\-=\[\]{};\'":\\|,.<>/?`~\.…]+', ', ', text)
    text = " ".join(text.split())
    text = text.strip()
    text = text.strip(", ")
    if not text:
        text = original.strip()
    return text


def normalize_text(text: str, language: str = "vi") -> str:
    """Normalize text (currently pass-through)."""
    return text


def add_config_text(text: str) -> str:
    """Add natural pause padding around text for better TTS output."""
    return " . " + text + " . "


def get_cut_silent_ms(duration_ms: float, threshold_ms: int) -> float:
    if duration_ms <= threshold_ms:
        return 0.0
    return duration_ms - threshold_ms


def fix_silent_and_speed_audio(
    audio: np.ndarray,
    sr: int,
    threshold_ms: int = 50,
    silence_threshold_db: float = -60.0,
) -> np.ndarray:
    """Trim excessive silence from audio segments."""
    if len(audio) == 0:
        return audio

    import librosa

    frame_size = int(0.01 * sr)
    frames = [audio[i:i + frame_size] for i in range(0, len(audio), frame_size)]
    threshold_linear = 10 ** (silence_threshold_db / 20.0)

    is_silent = []
    for frame in frames:
        rms = np.sqrt(np.mean(frame ** 2)) if len(frame) > 0 else 0
        is_silent.append(rms < threshold_linear)

    # Group into segments
    segments = []
    current_type = is_silent[0]
    current_start = 0
    for idx in range(1, len(is_silent)):
        if is_silent[idx] != current_type:
            segments.append({
                'silent': current_type,
                'start': current_start * frame_size,
                'end': min(idx * frame_size, len(audio)),
            })
            current_type = is_silent[idx]
            current_start = idx
    segments.append({
        'silent': current_type,
        'start': current_start * frame_size,
        'end': len(audio),
    })

    result_parts = []
    for seg in segments:
        chunk = audio[seg['start']:seg['end']]
        if len(chunk) == 0:
            continue

        if seg['silent']:
            dur_ms = len(chunk) / sr * 1000
            cut_ms = get_cut_silent_ms(dur_ms, threshold_ms)
            if cut_ms > 0:
                cut_samples = int(cut_ms / 1000.0 * sr)
                new_len = max(0, len(chunk) - cut_samples)
                chunk = chunk[:new_len]
            result_parts.append(chunk)
        else:
            result_parts.append(chunk)

    if not result_parts:
        return audio

    return np.concatenate(result_parts)


# ── VAD Trim ──────────────────────────────────────────────

_VAD_MODEL = None
_VAD_UTILS = None


def _get_vad_model():
    """Load Silero VAD model from local vendored path (singleton)."""
    global _VAD_MODEL, _VAD_UTILS
    if _VAD_MODEL is not None:
        return _VAD_MODEL, _VAD_UTILS

    import torch

    vad_dir = Path(__file__).parent / "silero_vad"
    model_path = vad_dir / "data" / "silero_vad.jit"

    if not model_path.exists():
        print(f"⚠️ Silero VAD model not found at {model_path}")
        return None, None

    try:
        import sys
        parent_dir_str = str(vad_dir.parent)
        if parent_dir_str not in sys.path:
            sys.path.insert(0, parent_dir_str)

        from silero_vad.utils_vad import init_jit_model
        from silero_vad import (
            get_speech_timestamps, read_audio,
            save_audio, VADIterator, collect_chunks, drop_chunks
        )

        model = init_jit_model(str(model_path))
        _VAD_UTILS = (get_speech_timestamps, save_audio, read_audio, VADIterator, collect_chunks, drop_chunks)
        _VAD_MODEL = model
    except Exception as e:
        print(f"⚠️ Could not load Silero VAD: {e}")
        return None, None

    return _VAD_MODEL, _VAD_UTILS


def vad_trim(audio: np.ndarray, sr: int, margin_s: float = 0.05) -> np.ndarray:
    """Trim non-speech using Silero VAD. Falls back to energy-based trim."""
    if len(audio) == 0:
        return audio

    import torch
    import librosa

    model, utils = _get_vad_model()
    if model is None:
        trimmed, _ = librosa.effects.trim(audio, top_db=20)
        return trimmed

    (get_speech_timestamps, _, _, _, collect_chunks, _) = utils

    try:
        vad_sr = 16000
        if sr != vad_sr:
            wav_16k = librosa.resample(audio, orig_sr=sr, target_sr=vad_sr)
        else:
            wav_16k = audio
        wav_tensor = torch.tensor(wav_16k, dtype=torch.float32)

        timestamps = get_speech_timestamps(
            wav_tensor, model, sampling_rate=vad_sr,
            threshold=0.5, neg_threshold=0.30,
            min_speech_duration_ms=80, min_silence_duration_ms=100,
            speech_pad_ms=20, max_speech_duration_s=10.0,
        )

        if not timestamps:
            return np.zeros(0, dtype=audio.dtype)

        speech_audio = collect_chunks(timestamps, wav_tensor)
        speech_np = speech_audio.numpy()

        if sr != vad_sr:
            speech_np = librosa.resample(speech_np, orig_sr=vad_sr, target_sr=sr)

        return speech_np

    except Exception as e:
        print(f"⚠️ VAD Error: {e}")
        trimmed, _ = librosa.effects.trim(audio, top_db=20)
        return trimmed


# ── SRT Generation ────────────────────────────────────────

def _format_srt_time(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def create_srt_file(timing_items: List[dict], output_path: str) -> str:
    """Create SRT subtitle file from timing items."""
    output_path = Path(output_path)
    srt_lines = []
    for idx, item in enumerate(timing_items, start=1):
        start = _format_srt_time(item["startTime"])
        end = _format_srt_time(item["endTime"])
        text = item["text"]
        srt_lines.append(f"{idx}")
        srt_lines.append(f"{start} --> {end}")
        srt_lines.append(f"{text}")
        srt_lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_lines))

    return str(output_path)


def get_reference_sound(voices_dir: Path) -> Optional[Path]:
    """Get reference voice file from directory."""
    if not voices_dir.exists():
        return None

    priority_file = voices_dir / "reference_sound.wav"
    if priority_file.exists():
        return priority_file

    voices = list(voices_dir.glob("*.wav"))
    if voices:
        import random
        return random.choice(voices)

    return None
