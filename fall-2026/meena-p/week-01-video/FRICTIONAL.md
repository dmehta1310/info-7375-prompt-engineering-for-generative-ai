# FRICTIONAL.md — why-subtract-the-max (Week 01 video)

Format follows the seven entry prompts in `prerequisites/frictional.md`.

**Attribution, stated once up front:** Claude Code (Opus 5) did the bulk of the
hands-on build in this assignment — it authored `scenes.py` and
`beat_sheet.json`, ran the course's `main.py`, diagnosed every gate failure
below, and drafted the paperwork. I directed it, made the decisions recorded in
the "What Claude contributed" lines, and rejected or redirected its output where
noted. Each entry below bounds who did what rather than leaving it implied.

---

## Entry

**Date and what I was working on:** 2026-09-14 *(retrospective, written 2026-09-26)* — standing up the `brutalist.art` toolkit on Windows before any of this reel existed.

**I tried / expected:** Cloned the toolkit and ran `./setup --install`, expecting it to install everything and report green. The README presents it as one command, so I expected one command's worth of work.

**What happened:** Six separate defects, none of them in my work. `./setup` reported every Python feature missing even after installing them, because `python3` resolved to the Microsoft Store stub and every `pip install` printed "Python was not found". `manim>=0.18,<0.19` could not install at all — every 0.18.x release caps at `Requires-Python <3.13` — and because pip resolves before installing, that one pin aborted the whole `requirements.txt` batch. `compile.py` then failed with `Error parsing filterchain` because it interpolated a raw Windows font path into an ffmpeg `drawtext` filter, which ate the backslashes and split on the drive colon. Writing any file containing an em dash crashed with `'charmap' codec can't encode character`.

**What I did:** Shimmed `python3` by copying `python.exe` to `python3.exe` in `Python313\`, which precedes `WindowsApps` on PATH. Relaxed the manim pin to `>=0.19,<0.20`. For the ffmpeg path, probed eight escaping forms against the actual binary and found the colon needs a **double** backslash — a filtergraph value is unescaped twice, so `\:` is stripped by the first pass. Abandoned single-escape and quoted variants after they failed the probe.

**What Claude contributed:** Did all six diagnoses and fixes. Two things I want on record. First, its initial encoding fix touched only the *write* side, which made the bug **worse** — reads still produced mojibake, which was then written back as UTF-8, double-encoded into bytes cp1252 could not decode, converting a warning into a hard crash. It caught and corrected this itself, widening to `PYTHONUTF8=1` (PEP 540) rather than patching 59 call sites. Second, when it offered to revert all its toolkit changes, I **rejected** the full revert and told it to keep the four Windows fixes, because reverting would have broken the render I was about to do. Accepted: all six fixes. Changed: the revert scope.

**What I understand now / still do not understand:** Understand that a POSIX-authored toolkit can be broken on Windows in ways that have nothing to do with my project — `python3` resolving to a Store stub, backslashes eaten by a filtergraph parser, cp1252 killing an em dash. Still do not understand why `setup` reports a dependency as present when the interpreter it checks isn't the one `pip` installed into.

**Evidence and next step:** `./setup` exits 0 with all seven features green. The six fixes remain **uncommitted** in the local `brutalist.art` checkout — they are not part of this submission and belong upstream. Next step: report items 3, 4 and 5 (below) to the toolkit maintainer.

---

## Entry

**Date and what I was working on:** 2026-09-22 — getting the real numbers out of the course's `main.py`.

**I tried / expected:** Ran `main.py` expecting it to print everything the video needed — I assumed a demo script for a lesson on softmax would show the intermediate steps, since that's what the lesson is about.

**What happened:** `python3 main.py` printed only two objects — `probabilities([1,2,3])` and the sampler `counts`. Three of my planned beats needed values it **never prints**: the intermediates, the unshifted path, and the `[1000,1000]` case. Byte-identical across three consecutive runs, so the sampler seed (`seed=7`) holds.

**What I did:** Rather than take numbers from the chapter text, imported the module and called its own `probabilities()`, checking every recomputed stage against that function's return value — max abs difference `0.0`. Recorded the split as Tier 1 (printed) and Tier 2 (derived) in SOURCES.md so a grader can audit which is which.

**What Claude contributed:** Ran both, and flagged the provenance problem to me *before* writing any beat sheet rather than quietly papering over it. It also found that my brief was **factually wrong**: I had asked for an "identity check" showing the shifted and direct paths produce *identical* probabilities. They do not — indices 0 and 2 differ in the last bit, max abs difference `1.1102230246251565e-16`, and `sum(probabilities)` is `0.9999999999999999`, not `1.0`. I **accepted** the correction; beat B03 now reads "agreement, not identity".

**What I understand now / still do not understand:** Understand that `probabilities()` computes `peak` and the shifted weights and then throws them away before returning — the intermediates exist only inside the function, which is why the video had to call it rather than read its output. Still do not understand whether the `1.1e-16` disagreement would grow with more logits or stay at one ulp; I only tested the one input.

**Evidence and next step:** FACTCHECK.md lists all 14 claims with verdict and source. `python3 main.py` at repo HEAD `8f590fa` reproduces the Tier 1 values exactly.

---

## Entry

**Date and what I was working on:** 2026-09-22 — first render attempt; the QC gates rejected it five times in a row.

**I tried / expected:** Ran `./art run` expecting it to render the seven Manim scenes and give me a rough but watchable cut I could react to.

**What happened, in order:**

1. **GATE F** — refused to render at all: `FACTCHECK.md`, `SHOTLIST.md` and `PROMPTS.md` must exist *before* rendering, not after.
2. **"nothing to render"** — all seven scenes were invisible. `run.sh` discovers them with the regex `class ([A-Z][A-Za-z0-9]*_\w+)\(Scene\)`, which requires inheriting `Scene` **directly**; I had factored the cream background onto a shared `_Base` class, so zero scenes matched and it would have compiled seven blank slates.
3. **GATE A** — `NameError: name 'NORMAL' is not defined`. The gate executes `construct()` against a *stub* `manim` module that defines geometry and animation names but not the text-weight constants. `weight=NORMAL` works in real manim and fails the gate.
4. **GATE A again** — "shapes never change" on B05. The gate scores shape *movement*, not presence. Adding one static shape to B00 and B06 made them **worse**: they went from a non-blocking "no shapes recorded" warning to a blocking "1 distinct shape-state" error.
5. **GATE W** — `INFO 7375 · CHAPTER 1 · …` tripped the rule banning chapter numbers on screen (`/\bchapter\b|\bch\.\s*\d/i` over every string constant in the class).

**What I did:** Wrote the three paperwork files first. Replaced the base class with a `page(scene)` function. Switched to string weights (`weight="NORMAL"`), which both real manim and the stub accept. Abandoned "add a static shape" in favour of markers that actually move. Renamed the kicker to name the topic instead of the chapter — the narration still says "Chapter One", since the rule governs the frame, not the voice.

**What Claude contributed:** Diagnosed all five. The `_Base` regex finding is the one I would not have found quickly — the failure surfaced as the bland message "nothing to render — recompiling only", with no mention of scene discovery. It read `run.sh` to locate the regex rather than guessing. I **accepted** every fix here unchanged.

**What I understand now / still do not understand:** Understand that the pipeline refuses to render before the paperwork exists, and that a scene can be silently invisible to it — my shared base class meant zero scenes matched its discovery regex and it would have compiled seven blank slates without erroring. Still do not understand why a discovery miss reports as "nothing to render" rather than naming the scenes it skipped.

**Evidence and next step:** `python3 runtime/qc/static_scene_check.py scenes.py --class B00_Hook` (repeat per class) — all seven report `1 clean · 0 warn · 0 error`.

---

## Entry

**Date and what I was working on:** 2026-09-22/23 — layout and timing, after the gates started passing.

**I tried / expected:** Expected the first watchable cut to be close to final — that once the gates passed, I'd be adjusting wording rather than rebuilding layouts.

**What happened:** Three more rounds. **GATE B** rejected four beats one at a time for safe-area breaches: the documented 5% inset (x ±6.4, y ±3.6) is not what the auditor enforces — `manim_layout_audit.py` reports **±6.3 x / ±3.4 y**. My kicker sat at y=3.45, five hundredths outside. B02's bottom band ran to **y=-4.12, off-frame entirely**, and its `arrange`/`shift` juggling put a value label on top of a bar. Then the compiler warned `B03: clip 8.9s slowed 3.6x into 31.9s beat — extreme slow-mo`: every beat was stretched 1.7×–3.6× because my animations were far shorter than their measured narration. Finally **GATE V** returned 14 `edge-bleed` BLOCKERs on every frame, and separately `underfill` on B02 (53%) and B06 (49%) against a 55% floor.

**What I did:** Rebuilt B02's band with explicit coordinates instead of layout helpers — arithmetic on known extents is easier to keep inside ±3.4 than `arrange()`. Rewrote every scene with holds sized to the measured narration, bringing slow-mo to 1.06×–1.18×. For underfill, added a `fill_safe()` helper, since the existing `fit()` only ever *shrinks* — a small block floating mid-page is never corrected by it.

**What Claude contributed:** All of the above. On the 14 edge-bleed blockers it established, by toggling only `ART_NO_DRAWTEXT=1`, that the cause was the toolkit's own review timecode burned 16px from the frame edge — **not** my scenes, which pass the layout audit with zero findings. Blockers went 14 → 0 with nothing else changed. I **accepted** that workaround for the build, understanding it is a workaround around a toolkit bug rather than a fix to this reel.

**What I understand now / still do not understand:** Understand that passing a gate is not the same as looking right: every beat was stretched 1.7×–3.6× because I'd written animations far shorter than the narration they had to cover, and nothing flagged that until the compiler warned about it. Still do not understand why the documented safe area (±6.4 / ±3.6) differs from the one the auditor actually enforces (±6.3 / ±3.4).

**Evidence and next step:** `./art run` exits 0; `_qc/REPORT.md` shows `BLOCKER: 0 · MAJOR: 0` across 14 sampled frames; `layout_audit.md` reports CLEAN.

---

## Entry

**Date and what I was working on:** 2026-09-26 — checking the finished video against the four assignment criteria.

**I tried / expected:** Expected this to be a formality — every gate was green and the reel had passed QC twice, so I expected to confirm the four criteria and move on.

**What happened:** Two real defects that **every automated gate had passed**, found only by extracting frames and looking at them. On B05 — the beat carrying the entire boundary-statement requirement — the kicker "WHAT THIS DOES NOT SHOW" printed *on top of* the statement's first line. Gate B checks text against *lines* and Gate V checks coverage and edge-bleed; neither tests text against text. On B01 the second arrow rendered as a degenerate stub, because the bars group's left edge sat 0.15 units from the softmax box while the arrow needed two 0.30 buffers — `Arrow()` drew it silently rather than erroring.

**What I did:** Fixed both, re-rendered those two beats only, and re-verified by looking rather than by re-reading the gate output.

**What Claude contributed:** Ran an AST audit over `scenes.py` confirming every on-screen digit-bearing string either interpolates a provenance constant or is one of seven hard-coded literals, each individually justified; re-ran `main.py` to confirm the numbers still reproduce; and verified `main.py` lines 14–15 match what B00 renders. It found both defects. I **accepted** both fixes. It also flagged a wording tension I have **not** resolved — see "Still open".

**What I understand now / still do not understand:** Understand that the gates and the rubric measure different things, and that two real defects survived every automated check — including a kicker printing on top of the boundary statement, on the one beat carrying that requirement. Still do not know how many more looking would find; I checked frames from four of the eight beats.

**Evidence and next step:** `_qc/REPORT.md`, `qc-sheet.png`, and the extracted frames. Gates were green *before* these two defects were found, which is the point.

---

## Entry

**Date and what I was working on:** 2026-09-26 — adding a title card, then submitting.

**I tried / expected:** Expected adding a 3-second card to be a small change, and expected the push to work — the professor had created `fall-2026/meena-p/`, so I assumed the folder existing meant I could write to it.

**What happened:** The title card went in cleanly as a new first beat — `compile.py` walks `beats` in array order rather than by sorted id, so inserting at index 0 renumbered nothing. Submission was harder. The first push was rejected `403 — Permission denied to meenuviji`; the professor having created my folder does not by itself grant write access. After I accepted the pending collaborator invite, the push failed again for an unrelated reason: 28 commits had landed upstream since the clone.

**What I did:** Accepted the invite, then rebased onto current `origin/main` — clean, no conflicts, nothing upstream touched my folder. Force-added the mp4 and pushed.

**What Claude contributed:** Staged and committed the submission, and verified the folder contained no caches, credentials or local paths — it caught two leaks of my Windows account path in BUILD-PROMPT.md and FRICTIONAL.md, and a private conversational aside in BUILD-PROMPT.md, and removed all three. It also **got something wrong and corrected it**: from the four-day-stale clone it concluded the mp4 should not be committed, because `.gitignore` blanket-excludes `*.mp4` and no mp4 was tracked. After the rebase it found three peers — `mayank-b`, `rithika-s`, `sreevarshan-s` — with committed mp4s, all merged, and **reversed its own advice**. I **accepted** the reversal: the mp4 is force-added, matching established practice, and both the README and the commit message explain why rather than leaving it looking careless. It separately checked my files against the course CI (`scripts/validate_course.py`) before pushing — no banned extensions, `scenes.py` parses, and zero local markdown links, so none of my files can break its repo-wide link check.

**What I understand now / still do not understand:** Understand that a folder being created for me and my having write access are two separate things on GitHub, and that a collaborator invitation has to be accepted before it grants anything. Still do not understand whether the mp4 should be force-added past `.gitignore` at all, or whether the blanket rule is simply stale — three classmates' mp4s are committed and merged, so the practice and the rule disagree.

**Evidence and next step:** Commit `637599f85a285817c358424c2bb88edf23b174fc`, pushed to `origin/main`, 11 files. Next step: confirm the Actions run goes green.

---

## Still open

- **An unexplained failure.** `./art run` once exited 4 with no Gate V verdict printed, while running the same gate standalone exited 2 and printed its report normally. The next run completed cleanly, so the cause is **unknown rather than fixed**. Recorded because it is unexplained. Next question: does `run.sh` mask the gate's exit code somewhere in its pipeline?
- **An internal contradiction I chose not to fix.** B01's footer says "they are all positive, and they sum to 1" while B02 displays `sum = 0.9999999999999999`. The reel states the mathematical property, then shows the floating-point reality one beat later. Arguably that gap *is* the subject — but it is a tension a grader could fairly pick at.
- **Four toolkit defects belong upstream**, not in this submission: the ffmpeg path escaping, the locale-encoding I/O, and the two that make `./art smoke` unable to pass as shipped on any platform where ffmpeg has the `drawtext` filter.
- The Manim LaTeX path (MiKTeX) was installed but **never exercised** — no beat in this reel uses `MathTex`.

---

## Appendix — full defect log

Kept from the working log; each item names a specific object.

| # | Defect | Specific object |
|---|---|---|
| 1 | `python3` was the Microsoft Store stub | `AppData\Local\Microsoft\WindowsApps\python3.exe` |
| 2 | manim pin uninstallable on 3.13 | `manim>=0.18,<0.19`, `Requires-Python <3.13` |
| 3 | Windows path destroyed in filtergraph | `compile.py:787`, needs `C\\:/path` |
| 4 | locale encoding on text I/O | `atomic_json`/`atomic_text`, 59 call sites, fixed via `PYTHONUTF8=1` |
| 5 | `./art smoke` cannot pass as shipped | fixture slug `_smoke` vs its own slug regex; review clock vs Gate V |
| 6 | `main.py` prints only 2 of the 5 things needed | Tier 1 / Tier 2 split in SOURCES.md |
| 7 | brief's "identical" claim is false | max abs diff `1.1102230246251565e-16` |
| 8 | GATE F blocks rendering without paperwork | `FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md` |
| 9 | all scenes invisible to the renderer | `class ([A-Z][A-Za-z0-9]*_\w+)\(Scene\)` |
| 10 | Gate A stub lacks text-weight constants | `NameError: name 'NORMAL' is not defined` |
| 11 | Gate A scores movement, not presence | "1 distinct shape-state" is worse than "no shapes" |
| 12 | chapter number banned on screen | `/\bchapter\b|\bch\.\s*\d/i` |
| 13 | safe area tighter than documented | enforced ±6.3 x / ±3.4 y, not ±6.4 / ±3.6 |
| 14 | every beat in slow-motion | `B03: clip 8.9s slowed 3.6x` |
| 15 | skin lint wanted Claude bookends | `palette: claude` → changed to `teardown` |
| 16 | 14 edge-bleed BLOCKERs from the review clock | `ART_NO_DRAWTEXT=1` takes it 14 → 0 |
| 17 | underfill on B02 (53%) and B06 (49%) | 55% floor; added `fill_safe()` |
| 18 | `./art run` exited 4 with no verdict | **unexplained** |
| 19 | kicker printed over the boundary statement | B05, body top y=3.25 vs kicker bottom ~3.17 |
| 20 | second arrow rendered as a stub | B01, 0.15 units of gap for two 0.30 buffers |

---

## Check before submitting

- [x] Every entry dated; retrospective entries labelled
- [x] At least one entry names a specific object, not a category
- [x] At least one thing that did not work, with why I moved off it
- [x] Every contribution says accepted / changed / rejected / still unclear
- [x] Something named as still unresolved, with a next question or step
- [x] Entries point at commits, tests, runs, or outputs a reviewer can open
- [x] No secrets or sensitive personal information anywhere in the log
- [x] Every entry's prompts answered in my own words
- [x] File is named `FRICTIONAL.md` and the Canvas version matches the pushed version
