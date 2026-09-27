#!/usr/bin/env python3
"""make_srt.py — build an SRT caption track for this reel.

The toolkit deliberately has no publish step (CLAUDE.md rule 5: "never publish
— render instead"), and its SRT writer lives in a stage_publish.py that ships
with the publishing skills rather than with the free pipeline. So this reel
emits its own captions from the two artifacts the pipeline DOES produce:

    mp3/words.json   word-level timing per beat, BEAT-LOCAL frames at 24 fps,
                     written by runtime/scripts/align.py (faster-whisper for
                     timing, SequenceMatcher to snap the KNOWN narration text
                     onto it, so the caption text is exact, never a transcript
                     guess).
    clips/<id>.mp4   the conformed per-beat video, in beat-sheet order.

Beat offsets come from the CLIP durations, not from beat_sheet.json's
actual_duration_s. Those differ by a frame or two per beat (the clock is
continuous, the render is quantised to 24 fps), and across ten beats the drift
reaches ~0.33s — enough to visibly lag by the outro. The clips are what the
master is concatenated from, so the clips are the truth.

Usage:  python3 make_srt.py [reel_dir]    ->  <slug>.srt
"""
import json
import subprocess
import sys
from pathlib import Path

MAX_LINE = 42          # characters per caption line
MAX_LINES = 2
MAX_CUE_S = 6.0        # never hold one cue longer than this
MIN_CUE_S = 1.0        # ...nor flash one shorter


def clip_seconds(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def wrap(words):
    """Balance a word list across at most MAX_LINES lines.

    A naive greedy wrap overflows: it fills line 1 to 42 chars, then dumps the
    remainder into line 2 regardless of length. Instead pick the split that
    minimises the LONGEST line, so a 2-line cue reads as two even lines.
    """
    text = " ".join(words)
    if len(text) <= MAX_LINE or len(words) < 2:
        return [text]
    best, best_cost = None, None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        cost = max(len(a), len(b))
        if best_cost is None or cost < best_cost:
            best, best_cost = [a, b], cost
    return best


def stamp(t):
    t = max(0.0, t)
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return "%02d:%02d:%02d,%03d" % (int(h), int(m), int(s), round((s % 1) * 1000))


def main():
    reel = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    sheet = json.loads((reel / "beat_sheet.json").read_text())
    words = json.loads((reel / "mp3" / "words.json").read_text())
    fps = float(words.get("fps", 24))
    slug = sheet["metadata"]["slug"]

    cues, offset = [], 0.0
    for beat in sheet["beats"]:
        bid = beat["beat_id"]
        ws = words["beats"].get(bid) or []
        dur = clip_seconds(reel / "clips" / f"{bid}.mp4")

        buf = []

        def flush():
            if buf:
                cues.append((offset + buf[0]["startFrame"] / fps,
                             offset + buf[-1]["endFrame"] / fps,
                             [x["text"] for x in buf]))
                del buf[:]

        for w in ws:
            # Test the candidate BEFORE committing it. Flushing after the fact
            # lets a cue overshoot by one word, which is how 51-character
            # lines got past the 42-char budget on the first pass.
            cand = buf + [w]
            span = (cand[-1]["endFrame"] - cand[0]["startFrame"]) / fps
            # Budget against the WRAPPED lines, not the raw string: a cue can
            # be under 2*42 characters and still wrap to a 44-char line,
            # because the split has to land on a word boundary.
            lines = wrap([x["text"] for x in cand])
            too_wide = len(lines) > MAX_LINES or max(len(l) for l in lines) > MAX_LINE
            if buf and (too_wide or span >= MAX_CUE_S):
                flush()
            buf.append(w)
            if w["text"].rstrip().endswith((".", "?", "!")):
                flush()
        flush()
        offset += dur

    # enforce the floor, and never let a cue run into the next one
    out = []
    for i, (start, end, ws) in enumerate(cues):
        if end - start < MIN_CUE_S:
            end = start + MIN_CUE_S
        if i + 1 < len(cues):
            end = min(end, cues[i + 1][0] - 0.001)
        if end > start:
            out.append((start, end, ws))

    srt = reel / f"{slug}.srt"
    with srt.open("w", encoding="utf-8") as fh:
        for i, (start, end, ws) in enumerate(out, 1):
            fh.write("%d\n%s --> %s\n%s\n\n"
                     % (i, stamp(start), stamp(end), "\n".join(wrap(ws))))
    print(f"[srt] {srt}  ({len(out)} cues, {offset:.2f}s timeline)")


if __name__ == "__main__":
    main()
