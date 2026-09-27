"""Regenerate selected beats' Kokoro audio with per-word pronunciation overrides.

Why: the toolkit's generate_audio_kokoro.py sends narration_text straight to
espeak-ng, which says "Namaste" as nˈæmæst and "Prasad" as pɹˈæsæd. kokoro-onnx
0.6.1 accepts a phoneme string (create(..., is_phonemes=True)), and after
phonemization its text and phoneme paths are the same code (_prepare). So this
wrapper phonemizes each beat exactly as the toolkit would, swaps only the listed
words' phonemes, and synthesizes the result. Everything else matches the stock
script: same normalize_for_tts, voice, lang, speed 1.0, write_mp3 (same mp3
encoding), measure(), and the same beat_sheet / mp3/timings.json updates.

The narration text and every on-screen string are unchanged. Only the audio
pronunciation differs. Re-running the stock generate_audio_kokoro.py on these
beats would undo the override; run this script again afterwards.

Usage (from anywhere, toolkit venv active):
    python3 tools/kokoro_phoneme_override.py <reel_dir> --only B00 BOUT [--check-identity]
"""
import argparse
import json
import os
import sys
from pathlib import Path

ART_HOME = Path(os.environ.get("ART_HOME") or
                Path(__file__).resolve().parents[5] / "brutalist.art")
sys.path.insert(0, str(ART_HOME / "runtime" / "scripts"))

from build_safety import (atomic_json, default_voice, validate_approvals,  # noqa: E402
                          validate_project, writable_path)
from generate_audio_kokoro import (lang_for, load_engine, measure,  # noqa: E402
                                   normalize_for_tts, write_mp3)

# espeak-ng output (en-us)  ->  intended pronunciation
OVERRIDES = {
    "Namaste": ("nˈæmæst", "nˌʌməstˈeɪ"),  # nuh-muh-STAY
    "Prasad": ("pɹˈæsæd", "pɹəsˈɑːd"),     # pruh-SAAD
}


def override_phonemes(phonemes: str, text: str) -> tuple[str, dict]:
    applied = {}
    for word, (espeak, wanted) in OVERRIDES.items():
        n_text, n_ph = text.count(word), phonemes.count(espeak)
        if n_text != n_ph:
            sys.exit(f"[override] {word!r}: {n_text} in text but {n_ph} espeak matches "
                     f"({espeak!r}) — refusing to guess")
        if n_text:
            phonemes = phonemes.replace(espeak, wanted)
            applied[word] = {"count": n_text, "from": espeak, "to": wanted}
    return phonemes, applied


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("reel", type=Path)
    ap.add_argument("--only", nargs="+", required=True)
    ap.add_argument("--check-identity", action="store_true",
                    help="synthesize WITHOUT overrides into a temp file and compare "
                         "samples with the stock text path; writes nothing")
    a = ap.parse_args()

    folder = a.reel.resolve()
    sheet_path = folder / "beat_sheet.json"
    sheet = json.loads(sheet_path.read_text())
    validate_project(sheet)
    validate_approvals(folder, sheet)
    selected_voice = default_voice(sheet)
    k = load_engine()

    timings_path = writable_path(folder, "mp3/timings.json")
    timings = json.loads(timings_path.read_text()) if timings_path.exists() else {}
    for b in sheet["beats"]:
        bid = b["beat_id"]
        if bid not in a.only:
            continue
        voice = b.get("voice") or selected_voice
        lang = lang_for(voice)
        text = normalize_for_tts((b.get("narration_text") or "").strip())
        phonemes = k.tokenizer.phonemize(text, lang)

        if a.check_identity:
            s_text, _ = k.create(text, voice=voice, speed=1.0, lang=lang)
            s_ph, _ = k.create(phonemes, voice=voice, speed=1.0, lang=lang, is_phonemes=True)
            same = len(s_text) == len(s_ph) and bool((s_text == s_ph).all())
            print(f"[override] {bid} identity check (no overrides): "
                  f"{'IDENTICAL samples' if same else 'DIFFERENT'} "
                  f"({len(s_text)} vs {len(s_ph)} samples)")
            continue

        phonemes, applied = override_phonemes(phonemes, text)
        samples, sr = k.create(phonemes, voice=voice, speed=1.0, lang=lang, is_phonemes=True)
        out = writable_path(folder, f"mp3/beat-{bid}.mp3")
        write_mp3(samples, sr, out)
        dur = measure(out)
        b["audio_file"] = f"mp3/beat-{bid}.mp3"
        b["actual_duration_s"] = round(dur, 2)
        b["tts_phoneme_overrides"] = applied
        timings[bid] = round(dur, 2)
        print(f"[override] beat-{bid}.mp3  {dur:.2f}s  voice={voice}  {applied}")

    if not a.check_identity:
        atomic_json(sheet_path, sheet)
        atomic_json(timings_path, timings)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
