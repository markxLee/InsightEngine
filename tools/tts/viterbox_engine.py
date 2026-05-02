"""Viterbox TTS engine wrapper for InsightEngine — STANDALONE.

No dependency on BetterBox-TTS. All code lives in tools/tts/viterbox/ and tools/tts/general/.
Model weights downloaded from HuggingFace on first run (~3.2GB, cached locally).

Voice profile strategy (best quality):
  1. Pre-built <voice>.conds.pt in tools/tts/voices/ (built from long audio)
     → loaded once, reused for all calls (audio_prompt=None)
  2. Fallback: encode reference_audio WAV directly (short ref, lower quality)

Usage:
    python3 scripts/tts_generate.py --engine viterbox --voice Phong_Dao --text "..."

To build a new voice profile:
    cd tools/tts/viterbox && python3 pretrain_voice_builder.py --copy_to_model
"""

import sys
from pathlib import Path
from typing import Optional, Tuple

# ── Path bootstrap — make tools/tts/ importable as package root ───────────────
_TTS_ROOT = Path(__file__).resolve().parent   # tools/tts/
_HF_REPO  = "dolly-vn/viterbox"
_MODEL_DIR = _TTS_ROOT / "viterbox" / "modelViterboxLocal"
_VOICES_DIR = _TTS_ROOT / "voices"

def _ensure_paths():
    tts_root = str(_TTS_ROOT)
    if tts_root not in sys.path:
        sys.path.insert(0, tts_root)


def _ensure_model():
    """Download model weights from HuggingFace if not present."""
    _MODEL_DIR.mkdir(parents=True, exist_ok=True)
    required = ["ve.pt", "s3gen.pt", "t3_ml24ls_v2.safetensors", "tokenizer_vi_expanded.json"]
    missing = [f for f in required if not (_MODEL_DIR / f).exists()]
    if missing:
        print(f"📥 Downloading Viterbox model from HuggingFace ({_HF_REPO})…")
        print(f"   Missing: {missing}")
        from huggingface_hub import snapshot_download
        snapshot_download(
            repo_id=_HF_REPO,
            local_dir=str(_MODEL_DIR),
            local_dir_use_symlinks=False,
            ignore_patterns=["*.git*", "conds.pt"],
        )
        print("✅ Model downloaded")


def _find_conds(voice: Optional[str]) -> Optional[Path]:
    """Find conds.pt for a given voice name (e.g. 'Phong_Dao' → voices/Phong_Dao.conds.pt)."""
    if voice:
        # Try exact name
        p = _VOICES_DIR / f"{voice}.conds.pt"
        if p.exists():
            return p
        # Try stripping extension if user passed filename
        stem = Path(voice).stem
        p = _VOICES_DIR / f"{stem}.conds.pt"
        if p.exists():
            return p
    # Auto-pick first .conds.pt
    conds_files = list(_VOICES_DIR.glob("*.conds.pt"))
    return conds_files[0] if conds_files else None


# ── Engine class ───────────────────────────────────────────────────────────────

class ViterboxEngine:
    """Standalone Viterbox TTS engine for InsightEngine."""

    def __init__(self, device: Optional[str] = None):
        _ensure_paths()
        import torch
        if device is None:
            if torch.backends.mps.is_available():
                device = "mps"
            elif torch.cuda.is_available():
                device = "cuda"
            else:
                device = "cpu"
        self.device = device
        self._model = None
        self._loaded_conds_name: Optional[str] = None

    def _load_model(self, voice: Optional[str] = None):
        if self._model is None:
            _ensure_model()
            from viterbox.tts import Viterbox
            from viterbox.tts_helper.tts_TTSConds import TTSConds
            print(f"🔈 Loading Viterbox on {self.device}…")
            self._model = Viterbox.load_local_model(str(_MODEL_DIR), device=self.device)
            print("✅ Viterbox loaded")

        # Load / switch voice profile (conds.pt) if needed
        conds_path = _find_conds(voice)
        if conds_path and str(conds_path) != self._loaded_conds_name:
            from viterbox.tts_helper.tts_TTSConds import TTSConds
            self._model.conds = TTSConds.load(str(conds_path), self.device)
            self._loaded_conds_name = str(conds_path)
            print(f"✅ Loaded voice profile: {conds_path.name}")
        elif conds_path is None and self._model.conds is None:
            print("⚠️  No .conds.pt found — will use audio_prompt fallback")

        return self._model


def generate_speech_viterbox(
    engine: ViterboxEngine,
    text: str,
    reference_audio: Optional[str] = None,
    language: str = "vi",
    speed: float = 1.0,
    pitch_shift: float = 1.0,
    exaggeration: float = 2.0,
    emotion: Optional[str] = None,
    voices_dir: Optional[Path] = None,
) -> Tuple[Optional[Tuple[int, any]], str, Optional[list]]:
    """
    Generate speech via Viterbox.

    Voice resolution order:
      1. <voice>.conds.pt matching reference_audio stem → best quality
      2. First .conds.pt in voices_dir → fallback pre-built
      3. reference_audio WAV directly (encode on-the-fly) → lowest quality

    emotion: None/"neutral" = no post-processing
             "sad"      = amplitude fade-out 10% at end (quiet, melancholic)
             "question" = amplitude surge +40% at last 20% (rising intonation)

    Returns:
        (sample_rate, audio_np), status_msg, None
    """
    # Determine voice name from reference_audio path
    voice_hint = Path(reference_audio).stem if reference_audio else None
    # Normalise emotion: None and "neutral" both mean no post-processing
    use_emotion = emotion if emotion and emotion != "neutral" else None

    try:
        model = engine._load_model(voice=voice_hint)

        # Apply emotional profile if requested
        if use_emotion:
            model.switch_emotional_profile(use_emotion)
        elif model.emotional_profile is not None:
            # Reset to neutral — clear any previously-set profile
            model.emotional_profile = None
            model.board = None
        use_audio_prompt = None
        voice_label = "conds.pt"
        if model.conds is None:
            if reference_audio:
                use_audio_prompt = str(Path(reference_audio).resolve())
                voice_label = Path(use_audio_prompt).name
                print(f"⚠️  No conds.pt — using audio_prompt fallback: {voice_label}")
            else:
                return None, "❌ No voice profile (.conds.pt) and no reference_audio", None
        else:
            conds_path = _find_conds(voice_hint)
            voice_label = conds_path.name if conds_path else "conds.pt"

        wav, _status, _srt = model.generate(
            text=text.strip(),
            language=language,
            audio_prompt=use_audio_prompt,
            advance_tts=False,   # False = phrase-level generation → connected, natural prosody
            skip_processing=not use_emotion,   # False = run EQ+envelope when emotion set
            exaggeration=exaggeration,
            cfg_weight=2.0,
            temperature=0.8,
            top_p=0.9,
            repetition_penalty=1.0,
            speed=speed,
            pitch_shift=pitch_shift,
        )

        audio_np = wav[0].cpu().numpy()
        duration = len(audio_np) / model.sr
        emotion_tag = f" | emotion={use_emotion}" if use_emotion else ""
        msg = f"✅ Viterbox | {duration:.2f}s | {language.upper()} | voice={voice_label}{emotion_tag}"
        return (model.sr, audio_np), msg, None

    except Exception as e:
        import traceback
        traceback.print_exc()
        return None, f"❌ Viterbox error: {e}", None
