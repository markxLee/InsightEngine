"""OmniVoice engine wrapper for CLI TTS.

Extracted from BetterBox-TTS OmniVoice/omnivoice_inference/ttsOmni.py
Provides: model loading, voice cloning, speech generation — without Gradio dependency.
"""
from __future__ import annotations

import gc
import hashlib
import json
import math
import os
import sys
import warnings
from pathlib import Path
from typing import Any, Optional, cast

import numpy as np

# Suppress HF telemetry
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")

import logging
logging.getLogger("transformers").setLevel(logging.ERROR)

from .audio_utils import (
    SEGMENT_TEXT,
    add_config_text,
    clear_text,
    create_srt_file,
    fix_silent_and_speed_audio,
    normalize_text,
    segment_text,
    vad_trim,
)


def _best_device() -> str:
    import torch
    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def _import_omnivoice_class():
    """Import OmniVoice model class, trying pip install first then local."""
    try:
        from omnivoice.models.omnivoice import OmniVoice as OmniVoiceClass
        return OmniVoiceClass
    except ModuleNotFoundError:
        raise ImportError(
            "OmniVoice not installed. Run: pip3 install --user omnivoice\n"
            "Or install from: https://github.com/k2-fsa/OmniVoice"
        )


# ── Voice Clone Prompt Cache ─────────────────────────────

_voice_clone_cache: dict[str, Any] = {}


def _get_file_fingerprint(file_path: str) -> str:
    try:
        stat = os.stat(file_path)
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                hasher.update(chunk)
        return f"{stat.st_size}:{stat.st_mtime}:{hasher.hexdigest()}"
    except Exception:
        return ""


def _get_cache_key(ref_audio: str, ref_text: Optional[str]) -> str:
    fp = _get_file_fingerprint(ref_audio)
    return hashlib.md5(f"{fp}:{ref_text or ''}".encode()).hexdigest()


def _get_voice_clone_prompt(
    reference_audio: str,
    ref_text: Optional[str],
    model: Any,
    language: str = "vi",
) -> Any:
    """Get or create voice clone prompt with in-memory caching."""
    import torch
    cache_key = _get_cache_key(reference_audio, ref_text)

    if cache_key in _voice_clone_cache:
        cached = _voice_clone_cache[cache_key]
        try:
            from omnivoice.models.omnivoice import VoiceClonePrompt
            return VoiceClonePrompt(
                ref_audio_tokens=torch.tensor(cached['ref_audio_tokens'], dtype=torch.long),
                ref_text=cached['ref_text'],
                ref_rms=cached['ref_rms'],
            )
        except Exception:
            pass

    print(f"🆕 Creating voice clone prompt for: {Path(reference_audio).name}")
    prompt = model.create_voice_clone_prompt(
        ref_audio=reference_audio,
        ref_text=ref_text,
        preprocess_prompt=True,
        language=language,
    )

    _voice_clone_cache[cache_key] = {
        'ref_audio_tokens': prompt.ref_audio_tokens.cpu().tolist(),
        'ref_text': prompt.ref_text,
        'ref_rms': prompt.ref_rms,
    }

    return prompt


# ── Omni Model Wrapper ───────────────────────────────────

class OmniEngine:
    """Lazy-loaded OmniVoice model for CLI usage."""

    def __init__(self, model_path: Optional[str] = None, device: Optional[str] = None):
        self.device = device or _best_device()
        self.model_path = model_path or "k2-fsa/OmniVoice"
        self._model: Optional[Any] = None
        self._sampling_rate: Optional[int] = None

    def _load_model(self) -> Any:
        if self._model is None:
            import torch
            print(f"🔄 Loading OmniVoice model from {self.model_path} on {self.device}...")
            cls = _import_omnivoice_class()
            model = cls.from_pretrained(self.model_path, dtype=torch.float32)
            model = model.to(self.device)
            self._model = model
            self._sampling_rate = model.sampling_rate
            print(f"✅ Model loaded (sample rate: {self._sampling_rate})")
        return self._model

    @property
    def sampling_rate(self) -> int:
        if self._sampling_rate is None:
            self._load_model()
        return cast(int, self._sampling_rate)

    def _infer(
        self,
        text: str,
        reference_audio: str,
        ref_text: Optional[str] = None,
        language: str = "vi",
        speed: float = 1.0,
        class_temperature: float = 0.0,
    ) -> list:
        """Run inference on a single text segment."""
        lang = "vietnamese" if language in (None, "vi") else language

        # Add config padding
        text = add_config_text(text)

        model = self._load_model()

        prompt = _get_voice_clone_prompt(
            reference_audio=reference_audio,
            ref_text=ref_text,
            model=model,
            language=lang,
        )

        return model.generate(
            text=text,
            language=lang,
            voice_clone_prompt=prompt,
            speed=speed,
            num_step=64,
            guidance_scale=5.0,
            t_shift=0.1,
            layer_penalty_factor=10.0,
            position_temperature=0.0,
            class_temperature=class_temperature,
            denoise=True,
            preprocess_prompt=True,
            postprocess_output=False,
            audio_chunk_duration=0.0,
            audio_chunk_threshold=60.0,
        )


def generate_speech(
    engine: OmniEngine,
    text: str,
    language: str = "vi",
    reference_audio: Optional[str] = None,
    ref_text: Optional[str] = None,
    speed: float = 1.0,
    pitch_shift: float = 1.0,
    exaggeration: float = 2.0,
    emotion: Optional[str] = None,
    voices_dir: Optional[Path] = None,
) -> tuple[Optional[tuple[int, np.ndarray]], str, Optional[str]]:
    """Generate speech from text.

    exaggeration: 0.5 (flat/robotic) → 2.0 (natural, default) → 3.0 (very expressive)
                  Maps to OmniVoice class_temperature: 0.5→0.0, 2.0→0.20, 3.0→0.40
    emotion:      None/"neutral" = no post-processing
                  "sad"      = amplitude fade-out 10% at end
                  "question" = amplitude surge +40% at last 20%

    Returns:
        (sample_rate, audio_array), status_string, srt_path_or_None
    """
    # Normalise emotion: None and "neutral" both mean no post-processing
    use_emotion = emotion if emotion and emotion != "neutral" else None
    # Map exaggeration (0.5–3.0) to OmniVoice class_temperature (0.0–0.40)
    # exaggeration 0.5 → 0.0 (flat), 2.0 → 0.20 (expressive), 3.0 → 0.40 (dramatic)
    class_temperature = max(0.0, (exaggeration - 0.5) / 2.5 * 0.40)
    import torch

    if not (text or "").strip():
        return None, "❌ Empty text", None

    # Resolve reference audio
    if not reference_audio:
        from .audio_utils import get_reference_sound
        vdir = voices_dir or Path("tools/tts/voices")
        ref_path = get_reference_sound(vdir)
        if ref_path is None:
            return None, "❌ No reference audio! Add .wav files to tools/tts/voices/", None
        reference_audio = str(ref_path)

    # Auto-load transcript from .txt file next to the voice WAV
    if not ref_text:
        txt_path = Path(reference_audio).with_suffix(".txt")
        if txt_path.exists():
            ref_text = txt_path.read_text(encoding="utf-8").strip()
            print(f"📄 Auto-loaded ref_text from {txt_path.name}: {ref_text[:60]}{'...' if len(ref_text) > 60 else ''}")

    # Preprocess text
    text = clear_text(text)
    text = normalize_text(text, language)

    # Segment
    segments = segment_text(text)
    if not segments:
        segments = [{"type": SEGMENT_TEXT, "content": text}]

    text_segs = [s for s in segments if s["type"] == SEGMENT_TEXT]
    print(f"📝 Text segmented: {len(segments)} items ({len(text_segs)} spoken)")

    # Build audio
    audio_pieces: list[np.ndarray] = []
    join_before: list[str] = []
    pending_join: str = "sentence"
    arr_srt: list[dict] = []
    current_time: float = 0.0

    sr = engine.sampling_rate
    print(f"\n🚩 Starting inference (speed={speed}, pitch={pitch_shift})")

    for seg in segments:
        if seg["type"] == SEGMENT_TEXT:
            spoken = seg["content"]
            print(f"\n  🔊 Generating: {spoken}")

            audios = engine._infer(
                text=spoken.strip(),
                reference_audio=reference_audio,
                ref_text=ref_text,
                language=language,
                speed=speed,
                class_temperature=class_temperature,
            )

            audio_np = audios[0]
            audio_np = vad_trim(audio_np, sr, margin_s=0.05)
            audio_np = fix_silent_and_speed_audio(audio_np, sr, threshold_ms=50, silence_threshold_db=-45)

            # Pitch shift with pedalboard
            if pitch_shift != 1.0:
                try:
                    from pedalboard import Pedalboard as PB, PitchShift
                    n_semitones = 12.0 * math.log2(max(0.5, min(2.0, float(pitch_shift))))
                    board = PB([PitchShift(semitones=n_semitones)])
                    audio_2d = audio_np.reshape(1, -1).astype(np.float32)
                    audio_np = board(audio_2d, sr).flatten()
                except Exception as e:
                    print(f"⚠️ Pitch shift failed: {e}")

            # SRT timing
            seg_duration = len(audio_np) / sr
            arr_srt.append({
                "startTime": current_time,
                "endTime": current_time + seg_duration,
                "text": spoken,
            })
            current_time += seg_duration

            print(f"  🎵 {len(audio_np)} samples | {current_time - seg_duration:.3f}s - {current_time:.3f}s")
            if len(audio_np) > 0:
                join_before.append(pending_join)
                audio_pieces.append(audio_np)
                pending_join = "sentence"

            if torch.cuda.is_available():
                torch.cuda.synchronize()
        else:
            pause_seconds = seg['pause_ms'] / 1000.0
            current_time += pause_seconds
            pending_join = f"pause:{seg['pause_ms']}"

    if not audio_pieces:
        return None, "❌ No audio generated", None

    # Concatenate
    result = audio_pieces[0].astype(np.float32)
    for i in range(1, len(audio_pieces)):
        rule = join_before[i]
        ms = int(rule.split(":")[1]) if isinstance(rule, str) and rule.startswith("pause:") else 0
        silence = np.zeros(int(sr * ms / 1000), dtype=np.float32)
        piece = audio_pieces[i].astype(np.float32)
        result = np.concatenate([result, silence, piece])

    # Trailing silence
    trailing = np.zeros(int(0.25 * sr), dtype=np.float32)
    result = np.concatenate([result, trailing])

    # Emotion post-processing (same pipeline as Viterbox)
    if use_emotion:
        try:
            from .general.EQ_emotion_config.eq_emotional_profiles import (
                get_emotional_audio_profile,
                apply_amplitude_envelope,
            )
            board = get_emotional_audio_profile(use_emotion)
            audio_2d = result.reshape(1, -1).astype(np.float32)
            result = board(audio_2d, sr).flatten()
            result = apply_amplitude_envelope(result, sr, use_emotion)
        except Exception as e:
            print(f"⚠️ Emotion post-processing failed: {e}")

    duration = len(result) / sr
    emotion_tag = f" | emotion={use_emotion}" if use_emotion else ""
    status = f"✅ Generated! | {duration:.2f}s | {language.upper()}{emotion_tag}"

    # Cleanup
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    gc.collect()

    return (sr, result), status, arr_srt
