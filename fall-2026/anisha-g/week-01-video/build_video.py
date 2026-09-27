#!/usr/bin/env python3
"""Render the seed/repeatability explainer with local audio and original motion graphics."""
from __future__ import annotations

import json
import math
import re
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"
W, H, FPS = 1280, 720, 20
WHITE, INK, GRAY = "#FFFFFF", "#33261E", "#707070"
RED, GOLD, LIGHT, GREEN = "#C8102E", "#D48B00", "#F4F4F4", "#287A49"


def run(*args: str) -> None:
    subprocess.run(args, check=True)


def duration(path: Path) -> float:
    return float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path)
    ], text=True).strip())


def font(size: int, bold=False, serif=False, mono=False):
    family = "DejaVuSansMono" if mono else ("DejaVuSerif" if serif else "DejaVuSans")
    weight = "-Bold" if bold else ""
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{family}{weight}.ttf", size)


def ease(x):
    x = max(0.0, min(1.0, x))
    return x*x*(3-2*x)


def reveal(t, at, span=.12):
    return ease((t-at)/span)


def centered(d, x, y, text, fnt, fill=INK):
    bb = d.textbbox((0, 0), text, font=fnt)
    d.text((x-(bb[2]-bb[0])/2, y-(bb[3]-bb[1])/2), text, font=fnt, fill=fill)


def box(d, bounds, label, value="", color=INK, fill=WHITE, thick=3, value_size=27):
    x1, y1, x2, y2 = bounds
    d.rectangle(bounds, fill=fill, outline=color, width=thick)
    d.text((x1+16, y1+12), label, font=font(14, True), fill=GRAY)
    if value:
        centered(d, (x1+x2)/2, (y1+y2)/2+12, value, font(value_size, True), color)


def arrow(d, x1, y1, x2, y2, color=INK, width=4):
    d.line((x1, y1, x2, y2), fill=color, width=width)
    a = math.atan2(y2-y1, x2-x1)
    for q in (2.55, -2.55):
        d.line((x2, y2, x2+15*math.cos(a+q), y2+15*math.sin(a+q)), fill=color, width=width)


def base(beat, index, total, t):
    im = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(im)
    d.text((55, 34), beat["title"], font=font(38, True, serif=True), fill=INK)
    d.text((57, 88), beat["act"], font=font(18, True), fill=RED)
    d.text((1110, 46), f"{index+1:02d} / {total:02d}", font=font(16, True, mono=True), fill=GRAY)
    d.line((55, 125, W-55, 125), fill="#D8D8D8", width=2)
    d.line((55, 624, W-55, 624), fill=GOLD, width=4)
    centered(d, W/2, 663, beat["takeaway"], font(18), GRAY)
    d.rectangle((55, 612, 55+int((W-110)*t), 616), fill=RED)
    return im, d


def count_bars(d, counts, x, y, width, label, progress=1.0, color_last=True):
    d.text((x, y-42), label, font=font(16, True), fill=GRAY)
    for i, count in enumerate(counts):
        yy = y+i*78
        d.text((x, yy+6), f"label {i}", font=font(18, True), fill=INK)
        bar = int(width*(count/700)*progress)
        d.rectangle((x+108, yy, x+108+bar, yy+36), fill=RED if color_last and i == 2 else GRAY)
        d.text((x+120+bar, yy+5), str(count), font=font(18, True, mono=True), fill=INK)


def draw_beat(d, bid, t):
    if bid == "B00":
        for i, lab in enumerate(("RUN A", "RUN B")):
            p = reveal(t, .08+i*.16)
            x = 95+i*440
            y = 205+int((1-p)*45)
            box(d, (x, y, x+355, y+170), f"{lab} · SEED 7", "102 · 268 · 630", RED if i else INK, LIGHT, 4 if i else 3, 25)
        if t > .46:
            d.line((450, 290, 535, 290), fill=GREEN, width=7)
            centered(d, 492, 266, "MATCH", font(14, True), GREEN)
        if t > .62:
            centered(d, 640, 455, "REPEATABLE  =  TRUE?", font(33, True, serif=True), INK)
            d.line((802, 434, 845, 475), fill=RED, width=7)
            d.line((845, 434, 802, 475), fill=RED, width=7)
        d.rectangle((865, 540, 1190, 585), fill=WHITE, outline=GRAY, width=2)
        centered(d, 1027, 562, "SYNTHETIC VOICE · KOKORO af_bella", font(13, True), GRAY)

    elif bid == "B01":
        stages = [
            ("INPUTS", "logits · count\nseed · temperature", INK),
            ("PROBABILITIES", "softmax(logits)", INK),
            ("LOCAL GENERATOR", "random.Random(seed)", RED),
            ("OBSERVED COUNTS", "weighted choices → Counter", INK),
        ]
        for i, (lab, val, col) in enumerate(stages):
            p = reveal(t, .05+i*.15)
            x = 42+i*310
            y = 245+int((1-p)*50)
            box(d, (x, y, x+245, y+160), lab, val, col, LIGHT if i % 2 == 0 else WHITE, 4 if col == RED else 3, 19)
            if i and p > .7:
                arrow(d, x-55, y+80, x-12, y+80, RED if i == 2 else INK)
        if t > .72:
            centered(d, 640, 520, "SEED STARTS THE GENERATOR · IT DOES NOT REWRITE THE PROBABILITIES", font(18, True), RED)

    elif bid == "B02":
        d.rectangle((65, 160, 1215, 570), fill="#FAFAFA", outline=INK, width=3)
        d.text((90, 180), "ACTUAL RUN · unmodified course main.py", font=font(18, True), fill=RED)
        d.text((90, 220), "COURSE CONSTRUCTED INPUT", font=font(14, True), fill=GRAY)
        d.text((90, 247), "logits=[1,2,3]   count=1000   temperature=1   seed=7", font=font(18, True, mono=True), fill=INK)
        count_bars(d, [102, 268, 630], 105, 340, 700, "OBSERVED COUNTS", reveal(t, .20, .50))
        d.text((850, 525), "total = 1000", font=font(18, True, mono=True), fill=INK)

    elif bid == "B03":
        rows = [("label 0", 102), ("label 1", 268), ("label 2", 630)]
        d.text((150, 165), "RUN A · seed 7", font=font(19, True), fill=INK)
        d.text((760, 165), "RUN B · seed 7", font=font(19, True), fill=INK)
        for i, (lab, val) in enumerate(rows):
            y = 220+i*94
            p = reveal(t, .08+i*.10)
            box(d, (105, y, 455, y+68), lab, str(val), INK, LIGHT, 3, 23)
            box(d, (715, y, 1065, y+68), lab, str(val), RED, WHITE, 4, 23)
            if p > .65:
                d.line((470, y+34, 700, y+34), fill=GREEN, width=5)
                centered(d, 585, y+17, "=", font(22, True), GREEN)
        if t > .58:
            d.rectangle((455, 525, 825, 580), fill="#EAF5EE", outline=GREEN, width=4)
            centered(d, 640, 551, "same_seed_equal: TRUE", font(22, True, mono=True), GREEN)

    elif bid == "B04":
        for i, txt in enumerate(("logits [1,2,3]", "count 1000", "temperature 1")):
            x = 70+i*260
            d.rectangle((x, 155, x+225, 195), fill=LIGHT, outline=INK, width=2)
            centered(d, x+112, 175, "LOCKED · "+txt, font(13, True), GRAY)
        d.rectangle((850, 150, 1190, 205), fill=WHITE, outline=RED, width=4)
        centered(d, 1020, 176, "ONLY SEED: 7 → 8", font(19, True), RED)
        count_bars(d, [102, 268, 630], 70, 300, 410, "SEED 7 · OBSERVED", 1.0, True)
        count_bars(d, [76, 239, 685], 690, 300, 410, "SEED 8 · OBSERVED", reveal(t, .22, .45), True)
        if t > .7:
            centered(d, 640, 570, "SAME DISTRIBUTION · DIFFERENT FINITE SAMPLE", font(20, True), RED)

    elif bid == "B05":
        d.rectangle((80, 165, 1200, 415), fill="#FAFAFA", outline=INK, width=3)
        d.text((105, 185), "CHAPTER 1 REPEATABILITY TEST", font=font(17, True), fill=RED)
        d.text((105, 250), "sample([1.0, 2.0])", font=font(26, True, mono=True), fill=INK)
        centered(d, 640, 263, "==", font(28, True, mono=True), RED)
        d.text((730, 250), "sample([1.0, 2.0])", font=font(26, True, mono=True), fill=INK)
        d.text((105, 330), "default seed = 7", font=font(18, mono=True), fill=GRAY)
        d.text((730, 330), "default seed = 7", font=font(18, mono=True), fill=GRAY)
        if t > .42:
            d.rectangle((480, 455, 800, 520), fill="#EAF5EE", outline=GREEN, width=4)
            centered(d, 640, 486, "PASS · REPEATABLE", font(24, True), GREEN)
        if t > .68:
            centered(d, 640, 570, "NO ANSWER KEY WAS CONSULTED", font(18, True, mono=True), RED)

    elif bid == "B06":
        d.text((90, 160), "ACCEPTED INPUTS", font=font(17, True), fill=GRAY)
        accepted = ["logits", "count", "seed", "temperature"]
        for i, item in enumerate(accepted):
            x = 70+i*210
            p = reveal(t, .05+i*.08)
            box(d, (x, 210, x+175, 300), f"INPUT {i+1}", item, INK, LIGHT, 3, 20)
            if p > .7:
                arrow(d, x+175, 255, 920, 370, INK, 3)
        box(d, (920, 320, 1195, 430), "SAMPLE FUNCTION", "selected labels", RED, WHITE, 4, 22)
        d.text((90, 385), "NOT ACCEPTED", font=font(17, True), fill=RED)
        for i, item in enumerate(("source", "answer key", "verifier")):
            x = 80+i*255
            d.rectangle((x, 435, x+210, 500), fill=WHITE, outline=RED, width=3)
            centered(d, x+105, 466, item, font(20, True), INK)
            d.line((x+14, 444, x+196, 491), fill=RED, width=5)
        if t > .67:
            centered(d, 640, 565, "REPEATING A MISTAKE PRESERVES THE MISTAKE", font(20, True), RED)

    elif bid == "B07":
        d.rectangle((60, 170, 585, 540), fill=LIGHT, outline=INK, width=3)
        d.rectangle((695, 170, 1220, 540), fill=WHITE, outline=RED, width=4)
        centered(d, 322, 215, "ESTABLISHES", font(19, True), INK)
        centered(d, 957, 215, "DOES NOT ESTABLISH", font(19, True), RED)
        for i, text in enumerate(("same starting state", "replayable sequence", "repeatable observed counts")):
            y = 290+i*78
            d.text((110, y), "✓", font=font(27, True), fill=GREEN)
            d.text((165, y+3), text, font=font(21, True), fill=INK)
        for i, text in enumerate(("truth", "correctness", "factual support")):
            y = 290+i*78
            d.text((750, y), "×", font=font(29, True), fill=RED)
            d.text((805, y+3), text, font=font(21, True), fill=INK)
        d.line((640, 153, 640, 562), fill=GOLD, width=5)
        if t > .66:
            centered(d, 640, 585, "SEED = REPLAY CONTROL · NOT A TRUTH CHECK", font(18, True, mono=True), RED)


def render_beat(beat, index, total, audio, out):
    seconds = duration(audio) + .55
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "rawvideo",
           "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", str(audio),
           "-vf", "scale=1920:1080:flags=lanczos", "-c:v", "libx264", "-preset", "veryfast",
           "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
           "-af", "loudnorm=I=-16:TP=-1.5:LRA=8,apad=pad_dur=0.55", "-t", f"{seconds:.3f}",
           "-movflags", "+faststart", str(out)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    frames = math.ceil(seconds*FPS)
    try:
        for n in range(frames):
            t = n/max(1, frames-1)
            im, d = base(beat, index, total, t)
            draw_beat(d, beat["beat_id"], t)
            proc.stdin.write(im.tobytes())
    finally:
        proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError(f"render failed: {beat['beat_id']}")
    return seconds


def srt_time(s):
    ms = round(s*1000)
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    sec, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{sec:02d},{ms:03d}"


def make_srt(beats, timeline, out):
    cues, number = [], 1
    for beat, span in zip(beats, timeline):
        sentences = [x.strip() for x in re.split(r"(?<=[.!?])\s+", beat["narration_text"]) if x.strip()]
        weights = [max(1, len(x)) for x in sentences]
        total, cur = sum(weights), span["start"]
        for sentence, weight in zip(sentences, weights):
            end = cur+(span["end"]-span["start"])*weight/total
            cues.append(f"{number}\n{srt_time(cur)} --> {srt_time(end)}\n{sentence}\n")
            number += 1
            cur = end
    out.write_text("\n".join(cues))


def main():
    if not shutil.which("ffmpeg"):
        raise SystemExit("FFmpeg is required")
    BUILD.mkdir(exist_ok=True)
    data = json.loads((ROOT/"beat_sheet.json").read_text())
    beats = data["beats"]
    clips, timeline, cursor = [], [], 0.0
    for i, beat in enumerate(beats):
        audio = ROOT/"mp3"/f"beat-{beat['beat_id']}.mp3"
        clip = BUILD/f"{beat['beat_id']}.mp4"
        if not audio.exists():
            raise SystemExit(f"Missing {audio}")
        seconds = render_beat(beat, i, len(beats), audio, clip)
        clips.append(clip)
        timeline.append({"beat_id": beat["beat_id"], "start": round(cursor, 3), "end": round(cursor+seconds, 3)})
        cursor += seconds
    concat = BUILD/"concat.txt"
    concat.write_text("".join(f"file '{p.as_posix()}'\n" for p in clips))
    output = ROOT/"Gaikar_Anisha_INFO7375_Week01_Video.mp4"
    run("ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0",
        "-i", str(concat), "-c", "copy", "-movflags", "+faststart", str(output))
    (BUILD/"timeline.json").write_text(json.dumps({"runtime_seconds": round(cursor, 3), "beats": timeline}, indent=2))
    make_srt(beats, timeline, ROOT/"Gaikar_Anisha_INFO7375_Week01_Video.srt")
    print(f"WROTE {output} ({cursor:.2f} seconds)")


if __name__ == "__main__":
    main()
