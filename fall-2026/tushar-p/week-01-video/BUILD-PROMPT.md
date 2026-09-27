# BUILD-PROMPT

This reel was built in a two-tool loop. Claude (claude.ai chat) wrote each prompt, I passed it to Claude Code in VS Code, and I brought the report back for review before the next step. Part A is enough to rebuild the video. Part B is the prompt history that produced it.

## Part A: Commands that rebuild the video

Run these from the Brutalist toolkit root, with this folder placed at `youtube/brutalist/token-not-word/`:

```bash
source .venv/bin/activate
pip install tiktoken==0.14.0

# 1. Reproduce the token data (the source of every on-screen number)
python3 - <<'PY'
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")  # GPT-4's tokenizer, not Claude's
for w in ["strawberry", " strawberry", "unbelievable", "raspberry",
          "Thank you!", "Thank you", " Thank you!"]:
    ids = enc.encode(w)
    print(f"{w!r}: {len(w)} chars -> {len(ids)} tokens {ids} pieces={[enc.decode([i]) for i in ids]}")
PY

# 2. Narration first; measured durations are the clock
python3 runtime/scripts/generate_audio_kokoro.py youtube/brutalist/token-not-word

# 3. Review cut, then 4K master
./art run youtube/brutalist/token-not-word
./art final youtube/brutalist/token-not-word
```

`beat_sheet.json` holds the final narration. `scenes.py` holds every visual.

## Part B: Prompt log

These are listed in order. Where a narration block was later replaced, it is marked **[abridged]** and points to the version that superseded it, since the final text lives in `beat_sheet.json`.

### Prompt 1: Explore the beat sheet format (no building)

> I'm building one short explainer video with this toolkit. Before we generate anything, I need you to report back the real format so I don't guess it. Please:
> 1. Print the full contents of `runtime/schema/beat_sheet.schema.json` and summarize, in plain English, every required field and what it expects.
> 2. Find any existing `beat_sheet.json` instance in the repo (not the schema, not in `.venv`) and show me one complete real example.
> 3. Look at `runtime/scripts/beat_plan.py` and tell me how a beat sheet is consumed: how beat IDs (like `B00`, `B01`) map to the narration mp3s, and whether narration audio is generated from the JSON or has to exist already.
> 4. Tell me which render path this toolkit uses for a beat sheet (Manim, Remotion, or both) and the exact command that turns a finished `beat_sheet.json` into a video.
>
> Don't build anything yet. Just report these four things.

### Prompt 2: Choose the rendering path for typography and number animation

> I'm authoring one explainer reel. Every animated beat is typography and numbers in motion: no photos, no AI video, no archival. I need to render: a word (`strawberry`) splitting into 3 labelled boxes `str` / `aw` / `berry` with token IDs; counters "characters: 10" vs "tokens: 3"; specific letters highlighted inside the boxes; the same word with a leading space collapsing from 3 boxes to 1; and `unbelievable` splitting into `un` / `belie` / `vable`.
>
> Given the fill-plan routing in `beat_plan.py` and the actual renderers, tell me which path is most reliable for this, with evidence from the code: (1) a generic `graphic.production_viz` spec, (2) a hand-authored named Manim scene via `graphic.manim`, or (3) a Remotion pattern with props. Then (a) recommend one path and say why the others are worse for this case; (b) show one minimal beat, valid for the current code (not the stale schema), that renders a test frame down that path; (c) list exactly what files a fresh reel folder needs to clear Gate F and `./art run`, and the folder path to use. Don't build the full reel yet.

*Outcome:* hand-authored Manim scenes in a reel-local `scenes.py`, proven with a one-beat test render.

### Prompt 3: Build the reel (review cut)

> Build one explainer reel using the proven path: hand-authored Manim scenes in a reel-local `scenes.py`, classes named `<BEAT_ID>_<Something>` subclassing exactly `(Scene)`, routed via `graphic.manim`. **Invent nothing.** Every number on screen must come from the data block below; if a beat needs a number that isn't there, stop and ask.
>
> Reel slug: `token-not-word` at `youtube/brutalist/token-not-word/`.
>
> Real data (tiktoken 0.14.0, `cl100k_base` = GPT-4): `strawberry` → 10 chars, `[496, 675, 15717]`, `['str','aw','berry']`; `' strawberry'` → 11 chars, `[73700]`; `unbelievable` → 12 chars, `[359, 32898, 24694]`, `['un','belie','vable']`; `raspberry` → 9 chars, `[13075, 79, 15717]`, `['ras','p','berry']`. Real dated Claude responses (22 Sep 2026): strawberry → 3 ("straw, ber, and ry"); blueberry → 2.
>
> r-highlight indices: word `strawberry` at 2, 7, 8; box `str` → (2,); `aw` → (); `berry` → (2,3).
>
> `narration_text` is the spoken line only (Kokoro reads it verbatim). All beats: GRAPHIC / own / manim, Kokoro voice `am_onyx`.
>
> **[abridged: seven beats (B00–B05, BOUT) with narration and visual notes, superseded by Prompts 4–6; final text in `beat_sheet.json`.]**
>
> Gate files: `FACTCHECK.md` (every on-screen number with its source; state that cl100k_base is GPT-4's tokenizer, not Claude's; cite the dated screenshots), `SHOTLIST.md`, `PROMPTS.md`.
>
> Then run `python3 runtime/scripts/generate_audio_kokoro.py token-not-word` and `./art run token-not-word`. Report measured durations, gate results, and look at frames to confirm: the B01 counters show correct values, B02 highlights exactly three r's, and B03's 3→1 collapse renders. No 4K final.

### Prompt 4: Split B05, add the "tell" beat (B06), re-render

> Split B05 into two beats. B05 keeps the reveal, the boundary, and the GPT-4 caveat. The new B06 carries the "tell": Claude grouped the letters as straw / ber / ry, which is not the tokenizer's str / aw / berry.
>
> **[abridged: B05/B06 narration, superseded by Prompt 5.]**
>
> B06 visual: the top row shows Claude's grouping `straw` / `ber` / `ry` as plain boxes with **no token IDs**, labelled "Claude's grouping (what it said)". The bottom row shows the real split with IDs 496 / 675 / 15717, labelled "actual tokens · cl100k_base". The differing boundaries must be obvious. **Critical honesty rule: no token IDs on the top row.**
>
> Drop `palette` and `style_preset` from the metadata. Update FACTCHECK.md (straw/ber/ry is Claude's spoken grouping, not tokenizer output) and SHOTLIST.md. Regenerate audio for B05 and B06, then run `./art run`. Report durations (must be above 2:00), gates, and frame checks. No 4K final.

### Prompt 5: Fix letter spacing, replace all narration

> Two changes, in order. Confirm the spacing fix on one frame before the full re-render.
>
> Step 1: Letters are unevenly spaced inside and between words. Diagnose before fixing. Check what `Text(font="monospace")` resolves to (Pango silently falls back when a font isn't installed) versus a sizing or kerning issue. Fix it, then render ONE frame of `B01_ThreeTokens` at low quality and look at it. Don't proceed until it's clean.
>
> Step 2: Replace every beat's `narration_text` with the new conversational script: personal open ("Hi, I'm Tushar…"), connective hand-offs between beats, and a closing callback to the strawberry question. **[abridged: full narration; B01–B04 and B06 were revised again in Prompt 6. Final text in `beat_sheet.json`.]** Keep the B05 screenshot pairing, B06's no-IDs top row, and every FACTCHECK claim unchanged.
>
> Step 3: Regenerate all audio, then run `./art run`. Step 4: Report the spacing cause, durations, gates, and frame checks. Also check pronunciation of `str`, `aw`, `berry`, `belie`, `vable`, and "space-strawberry"; report any problems but don't change the text.

*Outcome:* the spacing bug was Pango quantization at small point sizes. The fix was to build text at size 96 and scale it down, with Menlo pinned. Kokoro's phonemes showed three mispronunciations.

### Prompt 6: Fix the ending, add the thank-you beat, fix pronunciation and a false claim

Preface, used because this ran in a fresh Claude Code session:

> Context: I'm continuing work on an existing reel at `youtube/brutalist/token-not-word/`, built with this toolkit's Manim path. Before doing anything, read `CLAUDE.md` at the repo root, then the reel's `beat_sheet.json`, `scenes.py`, `FACTCHECK.md`, `SHOTLIST.md`, and `PROMPTS.md`. Established conventions: scene classes are `<BEAT_ID>_<Name>(Scene)`; every scene ends with `_hold(self, "<BEAT_ID>")`; text is built at `_TEXT_REF` size and scaled down (the spacing fix, so keep it); monospace is pinned to Menlo; B06's top row never shows token IDs; the B05 screenshots are correctly paired. Audio is generated before rendering. Never produce the 4K final unless asked.

Prompt:

> 1. Fix a false claim in B04: "belie" is a real English word. New narration: "And not meaning, either. Take unbelievable. You'd expect un, believe, able. But you get un, belie, vable. Belie happens to be a real word, but it has nothing to do with believing, and vable isn't a word at all. Meanwhile berry shows up whole inside raspberry, the same token reused. These are just frequency-shaped fragments from a fixed vocabulary. Which raises the real question: with all this working against it, does the model actually get my question wrong?" Also check B04's on-screen text for any "meaningless" claim.
> 2. Pronunciation: change the spoken text only, leaving on-screen cards as they are. Use Kokoro's G2P to test candidate spellings. `str` should sound like one syllable, "stur"; `ry` should sound like "ree"; in B03, replace "space-strawberry" with "strawberry with a space in front."
> 3. Rebuild BOUT's visual to match its callback narration: `strawberry` with r's 2, 7, 8 highlighted, a clear "3", and the token row str / aw / berry (496 / 675 / 15717) below, reading "same answer, different path." No new numbers.
> 4. Add a final beat `BTHX` / `BTHX_ThankYou(Scene)`. Run tiktoken first on `"Thank you!"`, `"Thank you"`, and `" Thank you!"`, and record the output in FACTCHECK.md. If it's a single token, stop and ask. Show `Thank you!` split into its real token boxes and IDs, make any leading space visible, and end with a gentle fade. Narration: "Thanks for watching. And since you made it this far, here's how a model reads my thank you." No token count in the narration.
> 5. Regenerate audio for B01, B02, B03, B04, B06, BOUT, and BTHX, then run `./art run`. Report the tiktoken output, phonemes, durations, gates, and frame checks. No 4K final.

*Outcome:* `Thank you!` → `[13359, 499, 0]` = `Thank` / ` you` / `!`. Runtime 2:43.

### Prompt 7: Final master

> The review cut is approved. (1) Fix the two stale lines in `PROMPTS.md` and `FACTCHECK.md`, and show before and after. (2) Run `./art final token-not-word` and report the output path. (3) Verify by looking: check ffprobe duration (~163.3 s), 3840×2160, and audio; pull frames from B01, B05, B06, BOUT, and BTHX; confirm the review-cut beat labels are gone, the B05 pairing is correct, B06's top row has no IDs, and the ending fades. (4) Report the file size and flag it if over 100 MB (GitHub's limit). Don't package yet.
