# Frictional — Week 01 video

Varnika M · INFO 7375 · Concept: *Three scores are not yet three chances*

Entries are dated on the day they happened. Claude Code (NEU-provisioned) organized
these notes from the session; the experiences and the "what I understand" lines are mine.

---

### 2026-09-26 — Setting up Brutalist on my Mac

- **Date and what I was working on:** Getting the brutalist.art toolkit (revision
  `6a8380ae169cca81e0633664a65c958f5c12ab4b`) ready to render, following
  `prerequisites/brutalist-video.md`. MacBook, Apple Silicon, macOS 26.6.
- **I tried / expected:** I expected to run `./setup --install` and get a green table.
- **What happened:** My Mac was missing most prerequisites: no Homebrew, no Node, no
  FFmpeg, and Python was 3.9.6 (the course needs 3.11+).
- **What I did:** Installed Homebrew myself in Terminal (it needed my password, so
  Claude could not do it). Claude then ran `brew install python@3.12 node ffmpeg` and
  created a Python 3.12 virtual environment (`.venv`) inside the toolkit.
- **Evidence:** `python3.12 --version` → 3.12.14, `node -v` → v26.10.0,
  `ffmpeg -version` → 9.0.2.

### 2026-09-26 — `./setup --install` stopped on its own ElevenLabs guard

- **What happened:** The installs ran, but setup exited before printing the readiness
  table: "ElevenLabs reference found — this toolkit is Kokoro-only for narration." The
  files it flagged are the toolkit's own tutorial files under `youtube/brutalist/`, not
  anything I added.
- **What I did:** Did not edit the toolkit. Claude made a scratch copy of `setup` with
  only that guard removed and ran the same readiness checks from it.
- **What I understand now:** This looks like a bug in the toolkit (the guard checks its
  own documentation), not a problem with my machine.

### 2026-09-26 — Python packages failed to compile (pycairo, manimpango)

- **What happened:** `pip install -r requirements.txt` failed on `pycairo` with
  "Compiler cc cannot compile programs." A one-line C test program also failed to link:
  `libSystem.tbd … unknown architecture arm64e.x1-macos` in the MacOSX27.0 SDK.
- **What I did:** Claude tested each SDK installed with the Command Line Tools. 15.4 and
  26.5 compiled; 27.0 did not. We reran the install with
  `SDKROOT=/Library/Developer/CommandLineTools/SDKs/MacOSX26.5.sdk` (matching my macOS
  26.6) for that command only; no system setting was changed. `pycairo` then needed the
  Cairo library and `manimpango` needed Pango, so we ran `brew install cairo pkgconf pango`.
- **Result:** pip finished with exit 0.

### 2026-09-26 — Readiness table and a real test render

- **Readiness (from the guard-free copy):** audio (Kokoro), captions, Manim beats,
  Remotion beats, slates/compile, fonts all ✅. **Manim equation beats ❌** (no LaTeX).
  I am not installing LaTeX: the course guide says to avoid equation beats in the first
  video.
- **`./art smoke` failed:** `[kokoro] REFUSED: metadata.slug must be a filename, not a
  path`. The test fixture's slug is `_smoke`, and the toolkit's own rule in
  `runtime/scripts/build_safety.py` rejects names starting with `_`.
- **What I did:** Ran a scratch copy of the smoke test that renames the slug to `smoke`.
  It passed: 13.9 s MP4, video + audio streams decode, mean volume −24.2 dB
  (floor −40 dB).
- **Still not proven:** the smoke video is two plain slates, so it never rendered a
  Remotion scene. I will find out whether Remotion renders when I build my first beat.
- **Toolkit changes:** none by hand. `git status` shows only the new `.venv/` and a
  3-line `runtime/remotion/package-lock.json` sync written by `npm install`.

### 2026-09-26 — Choosing the concept

- **I tried / expected:** I asked for the easiest concept. Claude suggested several:
  the training-scale slogan, expected vs observed count (665 vs 630), roles as text.
  I did not find the scale slogan easy to follow, so I chose
  **"Three scores are not yet three chances."**
- **Why:** `main.py` prints the real numbers (`[1, 2, 3]` → 0.090, 0.245, 0.665), it
  needs no Claude transcript, and it is the first piece of Assignment 1 (probability
  normalization).
- **What Claude contributed:** listed options, checked which concepts classmates had
  already posted, and verified the worked numbers by running the lesson code.
- **What I understand / still do not understand:** see the final entry below.
- **Next step:** Review the narration and beat sheet before anything is rendered.

### 2026-09-26 — Narration approved, first build

- **What I did:** Read the narration draft (11 beats; a working file, since deleted — the
  approved text is in `beat_sheet.json`) and approved it unchanged,
  including the short "subtracts the top score" line in step 1.
- **Evidence saved first:** `evidence/main_py_output.txt` (real `main.py` output, Python
  3.12.14) and `evidence/worked_steps.txt` (every intermediate number). Lesson tests:
  6/6 OK.
- **Audio:** Kokoro `am_onyx`, 11 beats, 140.67 s measured. Shorter than the ~3 min I
  estimated, because Kokoro speaks faster than a person reading aloud. Still inside 2–4 min.
- **Decisions Claude proposed and I accepted:**
  - The opening Claude-style screen shows the real `main.py` numbers with the label
    "Reconstructed interface · not a Claude reply", so it cannot be mistaken for a real
    Claude transcript.
  - The toolkit's outro card hardcodes `@NikBearBrown`. I did not edit the toolkit;
    `scenes.py` has its own end card with my name and the synthetic-voice note.
  - `scenes.py` imports the real `main.py` to compute every number on screen and refuses
    to render if they drift from the saved evidence.
- **Friction:** the first test frames had overlaps: the CONSTRUCTED tag on top of the
  title (B03, B06), "all positive" cut off the edge (B04), a label colliding with a bar
  value (B05), a tick on top of a caption (B07). Fixed and re-checked frame by frame
  before the full build.

### 2026-09-26 — Getting the build through the toolkit's gates

- **What happened (in order):**
  1. `./art run` refused to render: GATE F wanted `FACTCHECK.md`, `SHOTLIST.md`,
     `PROMPTS.md`. Claude wrote them from the evidence; the toolkit's own
     `factcheck_check.py` passed (18 claims, all PASS or EXEMPT).
  2. It then found no scenes. The toolkit discovers Manim scenes by the literal text
     `(Scene)` in each class line, and my scenes subclassed a helper. Renamed.
  3. A code comment containing an example class name was detected as a fake scene.
     Reworded.
  4. GATE A runs a temporary *copy* of `scenes.py` with a stub Manim, so the scenes could
     not find `main.py` or `beat_sheet.json` there, and the stub has no `BOLD`. Made the
     scenes work in both places; the real render still imports `main.py`.
  5. GATE B held back B03 for text slightly outside the safe area (±6.3 × ±3.4). Claude
     moved every edge placement inside it and ran the layout audit on all scenes locally
     before rebuilding.
  6. GATE V (frame QC) found the typing beat (B01) never finished its second line before
     the beat ended, and the end card was too small. The writer also replaced the word
     "Chances" on line 2 (the trigger match ignores case) and paused after every
     punctuation mark. Final B01 text: "A model's scores are its ranking — not its
     chances. / Probabilities must be positive and add up to one".
- **Left as is:** GATE V still reports "underfill" (too much empty space) on the two
  text-only frames, B01 and B10. They are readable text cards; I accepted this as a design
  choice rather than cramming more onto them.
- **Result:** review cut `three-scores-not-three-chances-slate.mp4`, 140.8 s, 11/11
  beats filled.
- **Next step:** watch the whole review cut with sound and note anything to fix.

### 2026-09-26 — Questioning the "Liam, narrating for Varnika" line

- **I questioned:** why the video opened with "This is Liam… narrating for Varnika". I asked
  whether the assignment requires that disclosure and where it is written.
- **What we found:** the Canvas brief does not mention it. The course's Brutalist guide does:
  `prerequisites/brutalist-video.md` lines 96–97 ("disclose synthetic narration") and line 135
  (lists the "synthetic-narration disclosure" among the submitted files). It does not require
  the disclosure to be spoken in the video; saying it aloud was Claude's stricter reading.
- **My decision:** remove the spoken line; disclose in `SOURCES.md` and keep a small note on the
  end card. Regenerated audio for B00 and B10 only; runtime is now 135.8 s.

### 2026-09-26 — Watching the review cut: labels did not match the narration

- **I noticed:** in B02 the voice says "the third option has the highest", but the bars were
  labelled option 0, option 1, option 2 (Python counts from zero). A viewer hears "third" and
  sees "option 2".
- **Options Claude gave:** relabel the bars A, B, C, or change the narration to "option two,
  which has score three". I chose **A, B, C**: clearer for a beginner, and no audio change.
- **Changed:** labels in B02, B05, B07; B07's hypothetical now reads "answer key: option A is
  correct". FACTCHECK.md and SOURCES.md updated to match.
- **Also decided while watching:** keep the Claude-style opening screen (allowed by the guide
  if labelled, line 95) and keep the B01 wording "every one has to become positive".
- **Also learned:** VS Code's built-in preview plays this MP4 with no sound; QuickTime plays
  the narration. The file's audio track is fine (mean −26.8 dB).
- **End card:** kept the code source caption in B04 ("main.py · probabilities() · lines
  14–17") so the code can be traced; shortened the end-card voice note to "Narration:
  synthetic voice (Kokoro am_onyx)". While checking it, the credit line was still fading in
  during the last frame of the 3-second end card, so the animation was sped up to finish by
  ~1.5 s and hold.

### 2026-09-26 — Final render

- **What happened:** `./art final` refused the first attempt. Its final frame check treats "too
  much empty space" as blocking, and the typing scene (B01) only had one or two lines of text in
  the middle of the frame. The review build had only warned about this.
- **What I did:** Claude used two options the writer scene already has: a heading
  ("Scores → Chances") and three cards along the bottom (Scores / Rule 1 / Rule 2) that stay on
  screen while the sentence types. The frame check then reported 0 blockers, 0 major issues.
- **Result:** `final/three-scores-not-three-chances.mp4`, 135.8 s, 1920×1080, 24 fps, H.264/AAC,
  5.5 MB, narration at mean −26.8 dB, no review labels.
- **What I understand now:** a model's scores only show the order of the options; they are
  not chances.
- **What I still do not understand:** why exp is used to make the numbers positive, rather
  than some other way.
