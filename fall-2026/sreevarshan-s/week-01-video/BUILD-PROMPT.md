# BUILD-PROMPT — week-01-token-not-word

## The assignment prompt given to Claude Code

Claude Code (Opus 5, Claude desktop app) was directed with the following brief.
Reproduced as given, lightly trimmed only where it repeated itself.

```text
GOAL: produce a complete, submittable Week 1 explainer video assignment on ONE
concept from Chapter 1: "The unit is a token, not a word — and why that breaks
letter-counting prompts."

This is a graded assignment with a strict standard: show the mechanism, don't
just narrate it; use only real, reproducible numbers; label any constructed
illustration as constructed; name one thing the explanation does NOT establish;
and if a Claude response appears on screen, it must be an actual response I
really got, with the date. Fabricating a cleaner-looking Claude transcript or
invented numbers is an academic integrity failure on this assignment, not a
style problem — do not do it under any circumstance, even if it would make the
video cleaner.

PHASE 0 — Orient: read lessons/01-randomness-and-first-prompts/ for anything on
tokenization. Locate the Brutalist toolkit's README and an example
beat_sheet.json and read its ACTUAL schema — do not guess. Read the prerequisite
guide, brutalist-video-sources.md (crediting rules), and the Frictional guide.
Confirm the free pipeline: Kokoro narration, Manim/Remotion render, no paid
generation, no API keys for media, no upload.

PHASE 1 — Build the real worked example: pick a concrete word for the
letter-counting case; use an actual tokenizer to print the REAL token split and
save raw output to a file; separately get a REAL Claude response to a
letter-counting prompt about that word. If no API access is configured here,
STOP and say so — do not simulate or approximate a response. Then state
precisely why the failure happens.

PHASE 2 — Script and beat sheet for a 2–4 minute video on this ONE concept.
Cold open on the puzzle, show the real tokenizer output with motion and labels,
explain why the token boundary breaks letter access, show the real dated Claude
transcript, then state one specific thing the explanation does NOT establish.
Label any constructed illustration. Build beat_sheet.json to the real schema.
STOP and show me before rendering.

PHASE 3 — Render with the toolkit's own documented commands. If anything fails,
do not silently work around it — log the failure in real time for FRICTIONAL.md.
Confirm final runtime is 2–4 minutes.

PHASE 4 — Deliverables: README.md, beat_sheet.json, BUILD-PROMPT.md, SOURCES.md,
FRICTIONAL.md, the rendered .mp4. No caches, credentials, or private transcripts
beyond the single dated Claude response used in the video.

PHASE 5 — Package as LastName_FirstName_INFO7375_Week01_Video.zip.
```

Two later instructions from the student:

```text
[provenance for B01]
Date received: September 22, 2026
Interface: claude.ai web chat
Model shown in UI: Claude Sonnet 5

Go-ahead confirmed: proceed to Phase 3.
```

## The one prompt sent to a model for content

Asked by the student in claude.ai web chat, not by the build:

```text
How many r's are in strawberry?
```

## Commands actually run

Environment. The toolkit lives beside the course repo; its `.venv` is Python
3.11 because the machine default is Anaconda 3.13, which cannot satisfy the
toolkit's `manim<0.19` pin.

```bash
cd /path/to/brutalist.art
source .venv/bin/activate          # Python 3.11
./setup                            # readiness check: 7/7 green
git rev-parse HEAD                 # ba2d0e0f043f5b3b35a50d336e0fc66fbfecfc0c
```

One dependency was added, into the **toolkit's** venv, never into the course
repo (the course is standard-library-only by policy):

```bash
pip install tiktoken               # 0.14.0
```

Evidence generation:

```bash
cd <reel>/evidence
python3 token_split_demo.py      | tee token_split_demo.txt
python3 prompt_tokens_demo.py    | tee prompt_tokens_demo.txt
python3 id_is_arbitrary_demo.py  | tee id_is_arbitrary_demo.txt
```

Library-first check before authoring any visual (CLAUDE.md rule 8):

```bash
./art scenes "word splitting into subword token chunks"
./art scenes "chat transcript with model response"
./art scenes "sentence broken into labelled boxes"
```

Build:

```bash
python3 runtime/scripts/generate_audio_kokoro.py "<reel>"
./art run   "<reel>" --height 1080
./art final "<reel>" --height 1080 --out "<reel>/final"
```

Gate debugging (used while fixing Gate A failures, see FRICTIONAL.md):

```bash
PYTHONPATH=runtime/manim python3 runtime/qc/static_scene_check.py "<reel>/scenes.py" --class B01_ClaudeTranscript
python3 runtime/qc/wcag_margin_check.py "<reel>/scenes.py" --class B01_ClaudeTranscript --quiet
python3 runtime/qc/beat_lint.py "<reel>/beat_sheet.json"
```

## What was NOT run

No Claude API call. No paid service. No upload. No `git push`.
