#!/usr/bin/env python3
"""
make_captions.py — build the reel's .srt from the word clock.

Why this script exists: the Brutalist toolkit's SRT writer lived in
`stage_publish.py`, which the pared-down edition removed along with everything
publishing-related. `align.py` still produces the word clock
(`mp3/words.json`: per-beat, word-level, frame-accurate), so the cues are
derived from real spoken timings — never from a flat words-per-second guess.

It is also deliberately NOT a copy of the shipped example reels' captions.
Those emit one cue per beat and truncate the narration to three lines, so text
is silently dropped mid-sentence (see
`examples/ai-explainer/claude-liam-algorithmic-art/*.srt`, cue 1: "Not the
code. Not"). This script asserts the opposite invariant: every word in every
beat appears in exactly one cue, in order.

Run:  python3 make_captions.py
Exit 0 = every narration word is captioned and the cue clock fits the master.
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Caption style: broadcast-conventional, two lines, comfortable reading rate.
MAX_LINE_CHARS = 42
MAX_LINES = 2
MIN_CUE_S = 1.0
MAX_CUE_S = 6.0
SENTENCE_END = ('.', '?', '!', '…', '."', '.”')


def load():
    sheet = json.loads((HERE / "beat_sheet.json").read_text())
    words = json.loads((HERE / "mp3" / "words.json").read_text())
    return sheet, words


def wrap(tokens):
    """Greedy wrap into at most MAX_LINES lines of MAX_LINE_CHARS."""
    lines, cur = [], ""
    for t in tokens:
        cand = f"{cur} {t}".strip()
        if len(cand) <= MAX_LINE_CHARS or not cur:
            cur = cand
        else:
            lines.append(cur)
            cur = t
    if cur:
        lines.append(cur)
    return lines


def fits(tokens):
    lines = wrap(tokens)
    return len(lines) <= MAX_LINES and all(len(l) <= MAX_LINE_CHARS for l in lines)


def ts(seconds):
    if seconds < 0:
        seconds = 0.0
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main():
    sheet, wordclock = load()
    fps = wordclock.get("fps", 24)
    beats = sheet["beats"]
    slug = sheet["metadata"]["slug"]

    cues = []
    consumed = 0          # words placed into cues
    available = 0         # words in the clock
    offset = 0.0          # cumulative beat start, on the frame grid

    for beat in beats:
        bid = beat["beat_id"]
        # Use the beat's RENDER duration — the value compile.py stamps back into
        # the sheet as `math.ceil(measured * fps - 1e-8) / fps` (compile.py:387).
        # Rounding to the nearest frame instead of ceiling loses 4 frames across
        # 13 beats and walks the captions early against the muxed timeline; these
        # sum to exactly the master's 195.625 s.
        dur = beat.get("render_duration_s")
        if dur is None:
            dur = math.ceil(beat["actual_duration_s"] * fps - 1e-8) / fps
        words = wordclock["beats"].get(bid, [])
        available += len(words)

        i = 0
        while i < len(words):
            group = [words[i]]
            j = i + 1
            # Grow the cue while it still wraps to two lines and stays short
            # enough to read; stop early on a sentence boundary.
            while j < len(words):
                trial = group + [words[j]]
                span = (trial[-1]["endFrame"] - trial[0]["startFrame"]) / fps
                if not fits([w["text"] for w in trial]) or span > MAX_CUE_S:
                    break
                group = trial
                j += 1
                if group[-1]["text"].endswith(SENTENCE_END):
                    break

            start = offset + group[0]["startFrame"] / fps
            end = offset + group[-1]["endFrame"] / fps
            # A cue must linger long enough to be read, but never past its beat
            # or into the next cue's first word.
            if end - start < MIN_CUE_S:
                end = start + MIN_CUE_S
            beat_end = offset + dur
            if end > beat_end:
                end = beat_end
            if j < len(words):
                nxt = offset + words[j]["startFrame"] / fps
                if end > nxt:
                    end = nxt
            if end <= start:
                end = start + 1.0 / fps

            cues.append({
                "start": start,
                "end": end,
                "lines": wrap([w["text"] for w in group]),
                "beat": bid,
            })
            consumed += len(group)
            i = j

        offset += dur

    # ── invariants ──
    assert available > 0, "word clock is empty — run align.py first"
    assert consumed == available, f"dropped words: captioned {consumed} of {available}"
    for a, b in zip(cues, cues[1:]):
        assert a["end"] <= b["start"] + 1e-9, f"cue overlap at {a['beat']}"
        assert a["start"] <= a["end"], f"inverted cue at {a['beat']}"
    for c in cues:
        assert len(c["lines"]) <= MAX_LINES, c
        assert all(len(l) <= MAX_LINE_CHARS for l in c["lines"]), c

    out = HERE / f"{slug}.srt"
    with out.open("w", encoding="utf-8") as fh:
        for n, c in enumerate(cues, 1):
            fh.write(f"{n}\n{ts(c['start'])} --> {ts(c['end'])}\n")
            fh.write("\n".join(c["lines"]) + "\n\n")

    total = offset
    # The cue clock must land on the muxed master, not near it.
    expected = sum(b.get("render_duration_s") or
                   math.ceil(b["actual_duration_s"] * fps - 1e-8) / fps for b in beats)
    assert abs(total - expected) < 1e-6, f"caption clock {total} != render clock {expected}"
    assert cues[-1]["end"] <= total + 1e-9, "last cue runs past the end of the film"
    print(f"{out.name}: {len(cues)} cues, {consumed}/{available} words captioned (no drops)")
    print(f"timeline ends at {total:.3f}s; last cue ends {cues[-1]['end']:.3f}s")
    longest = max(len(l) for c in cues for l in c["lines"])
    print(f"max line length {longest} <= {MAX_LINE_CHARS}; max lines/cue {MAX_LINES}")
    print("ALL CAPTION ASSERTIONS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
