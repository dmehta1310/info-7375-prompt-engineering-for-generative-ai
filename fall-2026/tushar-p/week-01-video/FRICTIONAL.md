# FRICTIONAL

Dated log of what broke, what I tried, and what I did. Every date was checked against evidence: file modification times (the reel folder and the toolkit's `.venv`), Claude Code session timestamps, and the macOS clock in my review screenshots. Where an entry spans two dates, the first is when the problem appeared and the second is when it was fixed.

## Pattern first

The most important finding of this build: **the automated QC gates checked structure, but only looking caught false content.** Five times, something passed or looked plausible in a report and was wrong on screen or in the data (entries 4, 6, 8, 11, and 15). This is Chapter 1's distinction between a fluent output and a supported claim, and it showed up inside my own build.

---

**1. 2026-09-22: tiktoken not installed.**
`import tiktoken` raised `ModuleNotFoundError`. I had both a conda `(base)` environment and the toolkit's `.venv` active. I confirmed with `echo $VIRTUAL_ENV` / `which python3` that `.venv` took priority, then installed tiktoken 0.14.0 there.

**2. 2026-09-22: toolkit schema out of date with its code.**
The beat-sheet schema documents an ElevenLabs `voice_id`, but ElevenLabs had been removed; the real field is `voice_kokoro`. It also advertises a `remotion` field in a place the renderer ignores. Claude Code found this by reading the code, not the schema. Lesson: validating against a schema is not the same as working.

**3. 2026-09-22: the "generic spec" render path renders nothing.**
`graphic.production_viz` looked like a way to describe visuals without code. In fact no renderer reads it, and the run script refuses to render the reel at all. I switched to hand-authored Manim scenes in a reel-local `scenes.py`, after a one-beat test render proved that path worked.

**4. 2026-09-22: real token IDs labelled "invented."**
During the test render, Claude Code called IDs 496 / 675 / 15717 "placeholders I invented." They matched my tiktoken run exactly, but a number whose stated provenance is "looked right" can't ship. I locked every on-screen number to my run and cited it in FACTCHECK.md.

**5. 2026-09-22: stray persona in the test slug.**
The test reel was named `claude-liam-tokenizer`, inherited from an example reel's persona. I renamed it to `token-not-word`.

**6. 2026-09-22: highlight ring on the wrong box.**
In B04, the terracotta ring sat around `ras` under a label reading "15717 — the same token as in strawberry." That is a false visual claim. Every static gate passed. It was caught only by frame review. The cause: Manim's `TransformFromCopy` mutates the target group, so the index pointed at the wrong card. The fix was to capture the position as plain numbers before the transform.

**7. 2026-09-22: short clips silently slowed.**
The compiler conforms a short clip to its audio by slowing it down. B05 would have shipped at 3.8× slow motion. Every scene now ends with a hold that reads the measured audio duration.

**8. 2026-09-23: I transposed the two screenshots.**
When I saved the files, the strawberry filename held the blueberry conversation and vice versa. The first B05 render captioned a blueberry answer "Claude · strawberry · correct." Claude Code caught it by reading the images rather than trusting the filenames, then renamed the files and verified them by checksum. This one was my error.

**9. 2026-09-23: untested code path failed on real data.**
Until the real PNGs existed, B05 had only ever drawn its placeholder. The image-loading path failed Gate A the moment real images arrived. It was fixed by using a different scaling method.

**10. 2026-09-22/23: runtime 1:45, under the 2:00 floor.**
I chose not to pad. Instead I pulled one real teaching point out of B05 into its own beat (B06): Claude's "straw, ber, ry" grouping is not the tokenizer's "str, aw, berry." That brought the runtime to 2:10.

**11. 2026-09-23: letter spacing broken, all gates clean.**
Watching the cut myself, I saw uneven spacing inside and between words ("tokeni zer," "cl100k_bas e"). Every gate had passed. The cause was that Pango quantizes glyph spacing when text is built at small point sizes. The fix: build all text at size 96 and scale it down. Claude Code also found that `"monospace"` is not a real font family, so it pinned Menlo.

**12. 2026-09-23: script felt like a slideshow.**
My watch-through notes: the open wasn't natural, the beats didn't lead into each other, and the ending was abrupt. I chose a conversational voice throughout and an ending that calls back to the opening question, and the script was rewritten.

**13. 2026-09-23/25: the ending visual didn't match the new narration.**
After the rewrite, BOUT's narration was the strawberry callback, but the screen still showed the old closing card. The prompt had said to keep all visuals unchanged. I caught it in a screenshot review. BOUT was rebuilt to show the callback, and I added my "Thank you!" token ending (3 real tokens: `Thank` / ` you` / `!`).

**14. 2026-09-23/25: mispronunciations.**
Kokoro spelled out `str` as "ess-tee-ar," read `ry` as "rye," and ran "space-strawberry" together. Only the spoken text was changed ("stur," "ree," "strawberry with a space in front"). On-screen cards still read `str` and `ry`.

**15. 2026-09-23/25: false claim in the AI-drafted script.**
The script said "belie and vable don't mean anything," but *belie* is a real English word. It was caught in review before the final and corrected: belie is a real word, but it has nothing to do with believing.

**16. 2026-09-25: a gate reported clean without checking.**
Gate W's scene filter requires a digit in the class name, so it silently skipped `BOUT_Closing` and `BTHX_ThankYou` on every run while reporting "clean." Claude Code ran the check on both by hand (0 errors). I did not patch the public toolkit; I'm noting it here as a known issue.

**17. 2026-09-25: pipeline limits the final fade.**
The compiler requires each clip to match its audio within 0.15 s, so no silent tail can be added. The closing fade had to fit in Kokoro's trailing silence, which gave 0.6 s.

**18. 2026-09-25: stale, oversized AI session.**
After two days idle, the Claude Code session would have re-sent about 346k tokens of history. I started a fresh session with a short preface listing the established conventions (spacing fix, no IDs on B06's top row, screenshot pairing). The durable context lived in the reel's files, not the chat.
