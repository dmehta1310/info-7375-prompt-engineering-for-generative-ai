# Less Room to Wander

- **Author:** Prasad S · INFO 7375, Fall 2026
- **Lesson / concept:** Lesson 01, Randomness and first prompts: does the gap between a sample's expected and observed count shrink as one outcome becomes more dominant (lower temperature)?
- **Intended audience:** INFO 7375 students
- **Narration:** synthetic Kokoro `af_bella` voice (disclosed in the video). Not Prasad's voice, not Bear, not an official or endorsed video.
- **Status:** reviewed local final. Prasad watched the review cut with sound and approved it. The 1080p final was exported on 2026-09-26: `./art final` exited 0, GATE T passed on all 11 beats, and GATE V showed 0 BLOCKER and 4 MAJOR (the B05/BOUT underfill exception in BUILD-LOG.md). Not published anywhere.
- **Final video:** `final/less-room-to-wander.mp4` (237.4 s, 1920×1080, sha256 `cf92ac21…57d1`; receipt in `final/less-room-to-wander.verified.json`). The MP4 goes to Canvas, not Git (media is git-ignored here).

## What's in this folder

| Path | What it is |
|---|---|
| `evidence/` | The run outputs (`temp-1.0.json`, `temp-0.5.json`) and Prasad's `ANALYSIS.md` |
| `beat_sheet.json` | The 11-beat plan the toolkit renders from |
| `PEDAGOGY.md` | Narration sign-off (signed by Prasad S, 2026-09-26) |
| `FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md`, `SOURCES.md`, `CHECKS-REPORT.md` | Toolkit paperwork (FACTCHECK / SHOTLIST / PROMPTS are required by `./art final`) |
| `BUILD-LOG.md` | The logged `ART_STRICT=0` exception for B05/BOUT underfill |
| `BUILD-PROMPT.md` | How this was actually built, step by step |
| `FRICTIONAL.md` | Process log |
| `tools/kokoro_phoneme_override.py` | Local pronunciation override for "Namaste" / "Prasad" (audio only) |

## Rebuild from this folder

Prerequisites: Git, Homebrew Python 3.11, Node 20, ffmpeg, plus `pkgconf cairo pango` for Manim (see FRICTIONAL.md for why each was needed).

```bash
# 1. The toolkit, as a sibling of the course repo, at the recorded revision
cd <parent-of-course-repo>
git clone https://github.com/nikbearbrown/brutalist.art.git
cd brutalist.art
git checkout 6a8380ae169cca81e0633664a65c958f5c12ab4b
python3.11 -m venv .venv && source .venv/bin/activate
export PATH="/opt/homebrew/opt/node@20/bin:$PATH"
./setup --install && ./setup
```

At this revision, `./setup` stops at its ElevenLabs guard because 10 of the toolkit's own example files trip it. The files removed locally, and why, are listed in FRICTIONAL.md (2026-09-25).

```bash
# 2. Build the reel from this folder's beat_sheet.json (ai-explainer path)
REEL=<course-repo>/fall-2026/prasad-s/week-01-video
python3 runtime/scripts/generate_audio_kokoro.py "$REEL"
python3 "$REEL/tools/kokoro_phoneme_override.py" "$REEL" --only B00 BOUT
ART_STRICT=0 ./art run "$REEL" --height 1080     # review cut; exception scope in BUILD-LOG.md
ART_STRICT=0 ./art final "$REEL" --height 1080 --out "$REEL/final"   # needs the local compile.py patch (BUILD-LOG.md)
```

`./art ai-explainer --help` shows the skill doctrine this beat sheet follows. The command doesn't generate a film by itself. No step uses a paid service or publishes anything.
