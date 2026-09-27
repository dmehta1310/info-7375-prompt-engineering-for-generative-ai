"""make_srt.py — build the caption sidecar from the toolkit's word clock.

Submitted by Suketh Produtoor (INFO 7375, Week 1). Written by Claude in
Claude Code build sessions the submitter directed — SOURCES.md §4 records
who did what, and what the submitter personally re-ran.

The public brutalist.art cut ships `align.py` (which writes the word clock,
`mp3/words.json`) but not the SRT writer — that lived in the publishing module
that was removed from the free toolkit. This script closes that gap.

Cue timing comes from the ALIGNED word clock, not from estimates: align.py used
faster-whisper for word-level timing and sequence-aligned the known narration
onto it (11 beats aligned, 0 fallback). Word frames are beat-local at 24fps, so
each beat's offset is the running sum of the MEASURED mp3 durations from
beat_sheet.json — the same master clock the video conforms to.

Captions are a sidecar, never burned in (the toolkit's caption policy).

Run from the reel folder:
    python3 evidence/make_srt.py
"""

from __future__ import annotations

import json
from pathlib import Path

REEL = Path(__file__).resolve().parent.parent
WORDS = REEL / "mp3" / "words.json"
SHEET = REEL / "beat_sheet.json"
OUT = REEL / "final" / "week-01-shifted-not-changed.srt"

# Cue shape: short enough to read at a glance, long enough not to flicker.
MAX_WORDS = 9
MAX_SECONDS = 4.0
MIN_SECONDS = 1.0
BREAK_AFTER = (".", "?", "!", ":", "—")


def ts(seconds: float) -> str:
    """SRT timestamp: HH:MM:SS,mmm."""
    if seconds < 0:
        seconds = 0.0
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main() -> int:
    words = json.loads(WORDS.read_text())
    sheet = json.loads(SHEET.read_text())
    fps = float(words.get("fps") or 24)

    # Beat offsets from the measured audio — the master clock.
    offsets: dict[str, float] = {}
    t = 0.0
    for beat in sheet["beats"]:
        offsets[beat["beat_id"]] = t
        t += float(beat.get("actual_duration_s") or beat.get("estimated_duration_s") or 0)
    total = t

    cues: list[tuple[float, float, str]] = []

    for beat in sheet["beats"]:
        bid = beat["beat_id"]
        toks = words.get("beats", {}).get(bid) or []
        if not toks:
            continue
        base = offsets[bid]
        group: list[dict] = []

        def flush() -> None:
            if not group:
                return
            start = base + group[0]["startFrame"] / fps
            end = base + group[-1]["endFrame"] / fps
            if end - start < MIN_SECONDS:
                end = start + MIN_SECONDS
            cues.append((start, end, " ".join(w["text"] for w in group)))
            group.clear()

        for w in toks:
            group.append(w)
            span = (group[-1]["endFrame"] - group[0]["startFrame"]) / fps
            if (
                len(group) >= MAX_WORDS
                or span >= MAX_SECONDS
                or w["text"].rstrip().endswith(BREAK_AFTER)
            ):
                flush()
        flush()

    # Never let a cue outlive its successor or the film.
    for i in range(len(cues) - 1):
        s, e, txt = cues[i]
        cues[i] = (s, min(e, cues[i + 1][0]), txt)
    if cues:
        s, e, txt = cues[-1]
        cues[-1] = (s, min(e, total), txt)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as fh:
        for i, (start, end, text) in enumerate(cues, 1):
            fh.write(f"{i}\n{ts(start)} --> {ts(end)}\n{text}\n\n")

    print(f"wrote {OUT.relative_to(REEL)}")
    print(f"  {len(cues)} cues over {total:.2f}s ({int(total//60)}m {total%60:.0f}s)")
    if cues:
        print(f"  first: {ts(cues[0][0])} {cues[0][2]!r}")
        print(f"  last:  {ts(cues[-1][0])} {cues[-1][2]!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
