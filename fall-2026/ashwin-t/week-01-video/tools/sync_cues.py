"""Resolve pause-based animation cues from the measured narration audio.

A cue like {"probsAtS": "p2+0.3"} means: set props.probsAtS to the moment the
2nd pause in this beat's mp3 ends (speech resumes), plus 0.3 s. Pauses are found
with ffmpeg silencedetect, so cues follow the audio clock — rerun this after
regenerating audio. Beat durations themselves are never touched here.

    python3 tools/sync_cues.py
"""
import json, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
SHEET = HERE / "beat_sheet.json"


def pauses(mp3):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(mp3), "-af",
                        "silencedetect=noise=-35dB:d=0.18", "-f", "null", "-"],
                       capture_output=True, text=True)
    return [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", r.stderr)]


def set_path(obj, path, value):
    keys = path.split(".")
    for k in keys[:-1]:
        obj = obj[int(k)] if k.isdigit() else obj[k]
    obj[keys[-1]] = value


sheet = json.loads(SHEET.read_text())
errors = 0
for b in sheet["beats"]:
    rem = b["shot"]["remotion"]
    rem["props"]["durationS"] = b["actual_duration_s"]    # clip length = measured narration
    cues = rem.get("cues")
    if not cues:
        continue
    mp3 = HERE / b["audio_file"]
    ps = pauses(mp3)
    for path, spec in cues.items():
        m = re.fullmatch(r"p(\d+)([+-][0-9.]+)?", spec)
        n = int(m.group(1))
        if n > len(ps):
            print(f"  {b['beat_id']}: {path}={spec} but only {len(ps)} pauses — narration changed? FIX")
            errors += 1
            continue
        t = round(ps[n - 1] + float(m.group(2) or 0), 2)
        t = min(t, b["actual_duration_s"] - 0.4)
        set_path(rem["props"], path, t)
        print(f"  {b['beat_id']}: {path:18} {spec:8} -> {t:5.2f}s  (of {b['actual_duration_s']:.2f}s)")
SHEET.write_text(json.dumps(sheet, indent=1, ensure_ascii=False) + "\n")
sys.exit(1 if errors else 0)
