# The unit is a token, not a word

**Student:** FIRSTNAME LASTNAME  ← *fill this in before submitting*
**Course:** INFO 7375 — Prompt Engineering for Generative AI
**Week:** 1 · **Lesson:** `lessons/01-randomness-and-first-prompts/`
**Status:** review cut — **not yet reviewed by a human.** See `REVIEW.md`.
**Final runtime:** 3:01.75 (181.75 s) · 1920×1080 · 24 fps · h264 + AAC stereo
**Final file:** `final/week-01-token-not-word.mp4` (7.0 MB) — see REVIEW.md before treating it as a reviewed final

## The concept

**The unit is a token, not a word — and why that breaks letter-counting prompts.**

Chosen because chapter 1 states the claim in one line — character tasks ask the
model "to reason about a unit it does not natively see" — and that claim can be
checked directly with a real tokenizer in a way a viewer can watch happen.

## What the video shows

In the prompt *"How many r's are in strawberry?"* the word arrives as **one
token**, id `73700`. The letter `r` is separately present as its own token
(id `436`). So the question names the letter, while the thing being asked about
is a single opaque integer whose spelling is not part of it.

The answer Claude gave was **correct**. The video does not claim a failure,
because none was observed. It shows that getting it right requires *recalling*
that token 73700 is spelled s-t-r-a-w-b-e-r-r-y — a stored fact about the token,
not something readable from the input.

## Contents

| File | What it is |
|---|---|
| `README.md` | this file |
| `SCRIPT.md` | the narration script, with the rev-2 framing note |
| `beat_sheet.json` | the reviewed 11-beat plan |
| `scenes.py` | the 11 Manim scenes |
| `BUILD-PROMPT.md` | the prompt and every command run |
| `SOURCES.md` | credits, licences, synthetic-narration disclosure |
| `FACTCHECK.md` | every on-screen claim mapped to its evidence file |
| `SHOTLIST.md` | typed work order (no open human slots) |
| `PROMPTS.md` | generation prompts (none) and the one real model prompt |
| `FRICTIONAL.md` | dated build log + **sections you must write yourself** |
| `REVIEW.md` | build re-checks + **your review decision, unfilled** |
| `evidence/` | the three demo scripts, their raw stdout, and the dated Claude response |
| `final/` | the rendered MP4 |

## Evidence

| File | Establishes |
|---|---|
| `evidence/token_split_demo.{py,txt}` | `strawberry` → `str`/`aw`/`berry` (cl100k) and `st`/`raw`/`berry` (o200k); r's at 2, 7, 8 |
| `evidence/prompt_tokens_demo.{py,txt}` | the full prompt is 8 tokens; the word is 1 token, id 73700 |
| `evidence/id_is_arbitrary_demo.{py,txt}` | 73699 = `' Smoking'`, 73701 = `' CMP'`, `' straw'` = 31107 |
| `evidence/claude_response.md` | the verbatim dated response shown in B01 |

The three `.txt` files are unedited stdout and print their own run date.

## Rebuild from this folder

Requires the **brutalist.art** toolkit checked out separately (it is
deliberately not vendored here). Revision used:
`ba2d0e0f043f5b3b35a50d336e0fc66fbfecfc0c`.

```bash
# 1. toolkit env (Python 3.11 — the system default Anaconda 3.13 breaks the manim pin)
cd /path/to/brutalist.art
source .venv/bin/activate
./setup                      # expect 7/7 features ready

# 2. the one extra dependency, into the TOOLKIT venv (never the course repo)
pip install tiktoken

# 3. regenerate the evidence (optional — the .txt files are committed)
cd /path/to/course/youtube/week-01-token-not-word/evidence
python3 token_split_demo.py     | tee token_split_demo.txt
python3 prompt_tokens_demo.py   | tee prompt_tokens_demo.txt
python3 id_is_arbitrary_demo.py | tee id_is_arbitrary_demo.txt

# 4. narration first — audio duration is the master clock
cd /path/to/brutalist.art
REEL=/path/to/course/youtube/week-01-token-not-word
python3 runtime/scripts/generate_audio_kokoro.py "$REEL"

# 5. review cut, then the verified master
./art run   "$REEL" --height 1080
./art final "$REEL" --height 1080 --out "$REEL/final"
```

`./art todo "$REEL"` reports any incomplete beats. There should be none.

## Cost and access

**$0.00.** Kokoro narration is local, Manim renders locally, no API key was
used for any media, no account is required, and nothing was uploaded.
No Claude API call was made by the build; the single model response in the
video was obtained by the student in claude.ai web chat.

## Honesty notes

- **Narration is synthetic** (Kokoro `af_bella`). Not a human voice.
- **B07 is the only constructed illustration**, stamped as such on screen.
- **The tokenizers are OpenAI's**, because Anthropic does not publish Claude's.
  The video states on screen that it therefore does not establish how Claude
  splits this word, nor that tokenization caused the observed answer.
