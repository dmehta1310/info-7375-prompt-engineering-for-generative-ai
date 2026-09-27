"""Synthesize narration for each beat with Kokoro (local, free) and measure it.
Audio is the master clock: the measured durations drive the final edit."""
import json, wave, sys
import numpy as np
from kokoro_onnx import Kokoro

ROOT = "/Users/riyakapadnis/Documents/INFO7375/brutalist.art/runtime/models/kokoro"
k = Kokoro(f"{ROOT}/kokoro-v1.0.onnx", f"{ROOT}/voices-v1.0.bin")

sheet = json.load(open("beat_sheet.json"))
voice = sheet["metadata"]["voice"]
out = {}
for b in sheet["beats"]:
    bid, text = b["beat_id"], b["narration_text"]
    samples, sr = k.create(text, voice=voice, speed=1.0, lang="en-us")
    samples = np.asarray(samples, dtype=np.float32)
    path = f"audio/{bid}.wav"
    with wave.open(path, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((np.clip(samples, -1, 1) * 32767).astype(np.int16).tobytes())
    dur = len(samples) / sr
    out[bid] = {"file": path, "duration_s": round(dur, 3),
                "estimated_s": b.get("estimated_duration_s"), "words": len(text.split())}
    print(f"{bid}  {dur:6.2f}s  (estimated {b.get('estimated_duration_s')}s)  {len(text.split())} words")

total = sum(v["duration_s"] for v in out.values())
print(f"\nTOTAL NARRATION: {total:.2f}s = {int(total//60)}m{total%60:04.1f}s")
json.dump({"voice": voice, "beats": out, "total_s": round(total, 3)},
          open("audio/timings.json", "w"), indent=2)
