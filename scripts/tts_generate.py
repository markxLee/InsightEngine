#!/usr/bin/env python3
"""Generate speech audio from text using OmniVoice TTS.

Usage:
    python3 scripts/tts_generate.py --text "Xin chào Việt Nam" --output output/hello.wav
    python3 scripts/tts_generate.py --file input/script.txt --output output/narration.wav
    python3 scripts/tts_generate.py --text "Hello world" --lang en --voice tools/tts/voices/english.wav
    python3 scripts/tts_generate.py --text "Nhanh hơn" --speed 1.3 --pitch 1.1

Options:
    --text TEXT          Text to speak
    --file PATH          Read text from file (alternative to --text)
    --output PATH        Output WAV path (default: output/tts_output.wav)
    --voice PATH         Reference voice WAV for cloning (default: tools/tts/voices/*)
    --ref-text TEXT       Transcript of reference voice (improves cloning accuracy)
    --lang LANG          Language: vi (default) or en
    --speed FLOAT        Speech speed 0.7-1.5 (default: 1.0)
    --pitch FLOAT        Pitch shift 0.5-2.0 (default: 1.0)
    --model PATH         HuggingFace model ID or local path (default: k2-fsa/OmniVoice)
    --device DEVICE      Force device: cuda, mps, cpu (default: auto-detect)
"""

import argparse
import sys
from pathlib import Path

# Ensure project root is in path for tools.tts imports
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))


def main():
    parser = argparse.ArgumentParser(
        description="Generate speech audio from text using OmniVoice TTS"
    )
    parser.add_argument("--text", type=str, help="Text to speak")
    parser.add_argument("--file", type=str, help="Read text from file")
    parser.add_argument("--output", type=str, default="output/tts_output.wav",
                        help="Output WAV path")
    parser.add_argument("--voice", type=str, default=None,
                        help="Reference voice WAV for cloning")
    parser.add_argument("--ref-text", type=str, default=None,
                        help="Transcript of reference voice")
    parser.add_argument("--lang", type=str, default="vi",
                        choices=["vi", "en"], help="Language")
    parser.add_argument("--speed", type=float, default=1.0,
                        help="Speech speed 0.7-1.5")
    parser.add_argument("--pitch", type=float, default=1.0,
                        help="Pitch shift 0.5-2.0")
    parser.add_argument("--model", type=str, default=None,
                        help="HuggingFace model ID or local path")
    parser.add_argument("--device", type=str, default=None,
                        choices=["cuda", "mps", "cpu"], help="Force device")
    parser.add_argument("--engine", type=str, default="omni",
                        choices=["omni", "viterbox"], help="TTS engine (default: omni)")
    parser.add_argument("--exaggeration", type=float, default=2.0,
                        help="Emotion intensity 0.5-3.0 (default: 2.0). Higher = more expressive. "
                             "Omni: maps to class_temperature. Viterbox: model-level exaggeration.")
    parser.add_argument("--emotion", type=str, default=None,
                        choices=["neutral", "sad", "question"],
                        help="Post-processing emotion profile (both engines). "
                             "sad=fade-out, question=rising intonation (default: neutral/none)")

    args = parser.parse_args()

    # Validate input
    if not args.text and not args.file:
        parser.error("Either --text or --file is required")

    # Read text from file if specified
    text = args.text
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"❌ File not found: {args.file}")
            sys.exit(1)
        text = file_path.read_text(encoding="utf-8").strip()

    if not text:
        print("❌ Empty text input")
        sys.exit(1)

    # Check dependencies
    try:
        import torch
        import numpy as np
        import soundfile as sf
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Run: pip3 install --user torch torchaudio soundfile librosa")
        sys.exit(1)

    # Import engine
    if args.engine == "viterbox":
        from tools.tts.viterbox_engine import ViterboxEngine, generate_speech_viterbox
        engine = ViterboxEngine(device=args.device)
        result, status, srt_data = generate_speech_viterbox(
            engine=engine,
            text=text,
            language=args.lang,
            reference_audio=args.voice,
            speed=args.speed,
            pitch_shift=args.pitch,
            exaggeration=args.exaggeration,
            emotion=args.emotion,
            voices_dir=Path("tools/tts/voices"),
        )
    else:
        from tools.tts.omni_engine import OmniEngine, generate_speech
        from tools.tts.audio_utils import create_srt_file
        engine = OmniEngine(model_path=args.model, device=args.device)
        result, status, srt_data = generate_speech(
            engine=engine,
            text=text,
            language=args.lang,
            reference_audio=args.voice,
            ref_text=args.ref_text,
            speed=args.speed,
            pitch_shift=args.pitch,
            exaggeration=args.exaggeration,
            emotion=args.emotion,
            voices_dir=Path("tools/tts/voices"),
        )

    if result is None:
        print(f"❌ Generation failed: {status}")
        sys.exit(1)

    sample_rate, audio_data = result

    # Save WAV
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(output_path), audio_data, sample_rate)

    # Save SRT
    srt_path = output_path.with_suffix(".srt")
    if srt_data:
        from tools.tts.audio_utils import create_srt_file
        create_srt_file(srt_data, str(srt_path))

    # Print summary (required by InsightEngine convention)
    wav_size = output_path.stat().st_size / 1024
    duration = len(audio_data) / sample_rate
    print(f"\n{status}")
    print(f"📁 {output_path} ({wav_size:.0f} KB, {duration:.1f}s)")
    if srt_path.exists():
        srt_size = srt_path.stat().st_size / 1024
        print(f"📁 {srt_path} ({srt_size:.1f} KB)")


if __name__ == "__main__":
    main()
