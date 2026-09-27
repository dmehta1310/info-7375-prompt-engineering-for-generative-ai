# SOURCES — week-01-token-not-word

Follows the crediting convention in
`prerequisites/brutalist-video-sources.md`: name the toolkit revision, disclose
synthetic narration, separate what was made here from what was reused.

## Revisions

| Thing | Revision |
|---|---|
| brutalist.art toolkit | `ba2d0e0f043f5b3b35a50d336e0fc66fbfecfc0c` |
| course repo | `9bc8b361fd290f6914a9aae375d5aa5f74f64009` |
| tiktoken | 0.14.0 |
| Python | 3.11.14 (Homebrew), in the toolkit's `.venv` |

## What I made for this video

| Artifact | What it is |
|---|---|
| `evidence/token_split_demo.py` + `.txt` | Written here. Prints the real token split of "strawberry" in two vocabularies, plus the letter ground truth. |
| `evidence/prompt_tokens_demo.py` + `.txt` | Written here. Tokenizes the exact prompt sentence. |
| `evidence/id_is_arbitrary_demo.py` + `.txt` | Written here. Shows neighbouring ids decode to unrelated strings. |
| `scenes.py` | Written here. All 11 Manim scenes. |
| `beat_sheet.json`, `SCRIPT.md` | Written here. |

The three `.txt` files are unedited stdout. Re-running the scripts regenerates
them; each prints its own run date.

## What I reused

| Source | Use | Licence / terms |
|---|---|---|
| [brutalist.art](https://github.com/nikbearbrown/brutalist.art) | Build pipeline: Kokoro TTS, Manim/Remotion render, QC gates, `./art` CLI | See repository LICENSE |
| [tiktoken](https://github.com/openai/tiktoken) | The tokenizer producing every split shown | MIT |
| `cl100k_base`, `o200k_base` | OpenAI BPE vocabularies (GPT-4, GPT-4o) | Distributed with tiktoken |
| Manim Community | Animation engine | MIT |
| Kokoro (`af_bella`) | Local speech synthesis | Model fetched by `./setup --install` |
| DejaVu Sans Mono | On-screen monospace | Bitstream Vera / DejaVu licence (permissive) |
| Course chapter 1 | The concept being explained | Course material; quoted as concept source, not reproduced on screen |

No stock footage, no generated imagery, no archival assets, no third-party
music. No paid service was used; total media cost $0.00.

## Model output

One model response appears in the video, in B01, verbatim:

> There are 3 r's in "strawberry" (strawberry).

Obtained by the student in **claude.ai web chat**, model shown in UI **Claude
Sonnet 5**, **September 22, 2026**. Recorded in `evidence/claude_response.md`
and shown on screen with that provenance. It is the only model output in the
reel and it was **not** altered, shortened or re-run for a cleaner result.

No Claude API call was made by the build. No API key exists in this
environment; this was checked before Phase 1 and recorded in `FRICTIONAL.md`.

## Synthetic narration disclosure

**All narration is synthetic.** It is local Kokoro `af_bella`, generated
offline by `runtime/scripts/generate_audio_kokoro.py`. It is not a human voice,
not the student's voice, and not the instructor's. It does not imply
endorsement by Anthropic, Northeastern, or the course staff.

## Claude's contribution to this submission

Claude Code (Opus 5, in the Claude desktop app) was used as a build assistant
throughout. Specifically it: read the repo and toolkit to find the schema,
wrote the three evidence scripts, drafted `SCRIPT.md` and `beat_sheet.json`,
wrote `scenes.py`, wrote this paperwork, and ran the build commands.

The student: chose the concept, obtained the real Claude response and attested
its provenance, and reviews and approves the cut. Claude flagged — rather than
hid — that the response came back **correct**, and the script was rewritten to
drop the rev-1 claim that a language model "cannot" count letters. That
rewrite is recorded in `FRICTIONAL.md` and in `SCRIPT.md`'s framing note.
