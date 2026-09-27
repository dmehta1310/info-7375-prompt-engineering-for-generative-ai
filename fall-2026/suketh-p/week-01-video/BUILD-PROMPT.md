# BUILD-PROMPT — week-01-shifted-not-changed

The single paste-ready Claude Code prompt that rebuilds this film end to end. Required by
`skills/make/ai-explainer/SKILL.md` step 6: *"A reel without its build prompt is
unfinished."*

Run it from an activated `brutalist.art` checkout with **normal permissions**. Do not
copy the `--dangerously-skip-permissions` flag from the toolkit's own docs: the course
prerequisite is explicit that this beginner path keeps permission prompts and bounded
folders.

---

## Environment (the recipe that works — arrived at the hard way)

Four install failures stand between a fresh clone and a working build on macOS/arm64. All
four are logged in [`FRICTIONAL.md`](FRICTIONAL.md); this is the route around them.

```bash
# 1. pycairo needs pkg-config. cairo alone is not enough. Because
#    `pip install -r requirements.txt` is one transaction, this single missing
#    system package aborts the whole install — taking Kokoro and faster-whisper
#    down with it and reporting "audio blocked", which is a symptom, not the cause.
brew install pkgconf

# 2. A dedicated venv on Python 3.12. NOT the Anaconda base env (the prerequisite
#    says avoid the system Python), and NOT 3.14 — manim<0.19 has no build for it.
cd /path/to/brutalist.art
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip

# 3. Install what this film actually uses. Manim is deliberately omitted: the
#    prerequisite directs a first video to avoid equation beats and to record the
#    unused blocked feature honestly. All mathematics here renders as Remotion.
pip install "kokoro-onnx>=0.4" "mutagen>=1.47,<1.48" "Pillow>=10.2,<11" \
            "numpy>=2.0.2" "faster-whisper>=1.0,<2"
(cd runtime/remotion && npm install)

# 4. Confirm. Expected: Manim ❌ blocked (unused), everything else ✅.
./setup
```

Recorded environment of this build: Python 3.12.7 (CPython), macOS 26.6.2 arm64, Node
v22.11.0, npm 11.16.0, ffmpeg 8.1, `brutalist.art` @ `ba2d0e0`. The 2026-09-24 re-renders
ran on macOS 27.0 arm64 with the same Python, Node, npm, ffmpeg and toolkit commit.

---

## The prompt

```text
Rebuild the INFO 7375 Week 1 explainer "Shifted, Not Changed" from its own folder.

Read first, completely, before touching anything:
  - CLAUDE.md, README.md, RENDER-TARGETS.md in this brutalist.art checkout
  - the whole of skills/make/ai-explainer/SKILL.md and the parent
    skills/make/explainer/ doctrine it inherits
  - OUTRO-LOCK.md — read its SCOPE clause, not just its rules
  - the reel's own beat_sheet.json, FACTCHECK.md, CHECKS-REPORT.md, SOURCES.md

Reel folder: /path/to/course/youtube/week-01-shifted-not-changed
Toolkit:     /path/to/brutalist.art  (venv activated, Python 3.12)

This is a STUDENT submission, not a channel episode. Five rules follow from that
and they override the worked examples:
  1. No @NikBearBrown handle, card, or mascot anywhere. OUTRO-LOCK.md scopes
     those to `claude-liam-*` reels: "Other channels ... NEVER get this card,
     handle, or mascot." The outro is this reel's own ShiftOutro.
  2. No IN-FOR-BEAR line. The narration never says "this is Liam, in for Bear",
     and the synthetic voice never claims to be the student or the instructor.
  3. The synthetic-narration disclosure stays on the outro card, on screen.
  4. Nothing implies endorsement by the channel, Northeastern, or Anthropic.
  5. NO FABRICATED CLAUDE RESPONSE. The brief: "If you show a Claude response,
     it must be a real one you actually got, with the date." B00, B05 and B09
     render through ShiftComposer with their disclosure pills, and B00's
     `output` stays EMPTY. The toolkit's COLD OPEN LAW asks for answer lines so
     the ask "lands answered" — do NOT add them. That law and the brief
     conflict here, and the brief is what is graded (SOURCES.md §5.16).

Numbers are load-bearing. Before rendering, run
  python3 <reel>/evidence/verify_claims.py
and diff its output against <reel>/evidence/run-output.txt. Every figure in the
beat sheet is a PROP taken from that run, and the beat sheet overrides every
figure-bearing schema default at render time (the components keep those values only as
Zod defaults, for standalone preview). If a figure has drifted, fix the beat sheet — never the component, and
never the reference implementation at
lessons/01-randomness-and-first-prompts/code/main.py, which is imported unmodified.
Do not invent a plausible-looking figure to fill a gap.

The seven reel-local components live in this checkout at
runtime/remotion/src/ShiftedNotChanged.tsx, registered in Root.tsx under the folder
"ShiftedNotChanged". Verify they resolve before building:
  ./art scenes --check ShiftPipeline
  ./art scenes --check ShiftBoundary
If Root.tsx has been regenerated and lost them, re-register and run
./art scene-index — a component missing from the index cannot be found by anyone.

Then build, in this order:
  python3 runtime/scripts/generate_audio_kokoro.py <reel>     # audio = the clock
  ./art run   <reel>                                          # review cut
  ./art todo  <reel>                                          # expect: no open slots
  ./art final <reel> --height 1080 --out <reel>/final         # the master

Audio is the master clock. If any narration changed, regenerate and re-measure
audio before recompiling; never patch timing by hand. If you changed a
beat's narration you must also re-pin that composition's durationInFrames in
Root.tsx to the new measured length, or the clip gets truncated to the audio
and loses its own ending.

TRAP — `./art run` will NOT re-render a beat whose props you just edited.
remotion_scenes.py skips any beat that still resolves as filled
("filled already (skip)"), and deleting media/<BEAT>.mp4 is not enough. The
run then reports 11/11 filled and compiles around the STALE clip. After
editing any beat's props or its component, force that beat:
  python3 runtime/scripts/remotion_scenes.py <reel> --only B01 --force
Then re-run ./art run to recompile and re-gate. The tell that you have hit
this: a Gate V number that is byte-identical to the previous round.

TRAP 2 — a beat render can report FAIL and the build will still export a
master. Observed 2026-09-20: B10 logged "FAIL: ShiftOutro", the pipeline
compiled around the STALE clip, Gate V passed (the old clip is visually
fine), and ./art final wrote a master. So after ANY multi-beat re-render:
  grep -E 'FAIL:' <the run log>
before trusting the output. A clean Gate V is not evidence that every beat
re-rendered. Re-running that one beat with --force cleared it.

TRAP 3 — the build REWRITES beat_sheet.json. remotion_scenes.py and
compile.py both stamp provenance and build state back into the sheet from
their own in-memory copy. Any hand edit you make to narration, props or
metadata WHILE a build is in flight is silently reverted when it finishes.
Observed twice on 2026-09-24: a metadata correction and a B04 narration trim
both vanished, and the B04 trim was only caught because the regenerated
audio came back at byte-identical duration — which it should not have, if
the text had really changed. Edit the sheet only when no build is running:
  pgrep -f 'remotion_scenes.py|run.sh|compile.py'   # must be empty first
Then regenerate audio and re-render. An unchanged duration after a narration
edit is the tell.

Finish with the frame-level VISUAL QC LAW pass, not an mp4 probe:
sample frames at >=2fps plus each beat at ~15/50/85% of its span, actually READ
the PNGs, and audit the 9-point rubric — edge bleed, title-safe margins,
container overflow, collision, offscreen anchors, legibility, brand-bug
placement, aspect, and CANVAS FILL. Log defects and fixes to _qc/REPORT.md, fix
root causes in the scene source, and re-render until zero BLOCKER and zero MAJOR
remain. Two known watch-items in this reel: B06's 62-character mono vectors must
not cross the SAFE inset, and B07's longest returned value
(9.85967654375977e-305) must not collide with the third column.

Constraints, all hard:
  - Free pipeline only. Kokoro am_onyx, local. No paid API, no Higgsfield, no
    ElevenLabs, no direct Anthropic API calls, no spend of any kind.
  - Never publish. No YouTube upload; the master stays in <reel>/final/.
  - Normal permissions. Do not pass --dangerously-skip-permissions.
  - Do not fabricate a test result, an approval, a citation, or a review. If a
    step fails, say "render blocked" and report the reason — do not report a
    completed video.
  - Report the real output path and the measured duration when done.
```

---

## What a correct build produces

| Artifact | Expected |
|---|---|
| `mp3/beat-B00.mp3` … `beat-B10.mp3` | 11 files. An empty `mp3/` is a FAILED BUILD, never a silent master. |
| Measured total | **195.72 s (3:16)** — inside the brief's 2–4 min target |
| B01 audio window | **≥ 9 s** (EXECUTIVE-SUMMARY LAW). Measured 16.36 s. |
| `media/B00.mp4` … `B10.mp4` | 11 per-beat renders, **0 slates** |
| `final/week-01-shifted-not-changed.mp4` | 1920×1080 master + `.srt` sidecar |
| `./art todo` | No open slots, no pantry requests |
| `_qc/REPORT.md` | Zero BLOCKER, zero MAJOR |

## Known deviations from doctrine (deliberate, not defects)

1. **`lead_silence_s: 0.8` on B01 is authored but inert.** The SKILL.md requires the
   field; `grep -rn "lead_silence" runtime/scripts/*.py` shows the free toolkit's audio
   script never reads it. Kept for doctrine; the ≥9 s window was earned by narration
   length instead. Do not "fix" this by shortening B01.
2. **The locked outro card is not used** — see rule 1 in the prompt above. This is the
   correct reading of `OUTRO-LOCK.md`'s scope clause, not an oversight.
3. **The COLD OPEN LAW is deliberately not met.** B00 shows no answer lines, because
   they would be a Claude response that was never given — see rule 5 in the prompt above
   and `SOURCES.md` §5.16. Do not "fix" this.
4. **Manim is blocked and never called.** Expected. Do not install Manim to make the
   readiness table green; this film has no equation beats and the prerequisite says to
   record the unused blocked feature honestly.
