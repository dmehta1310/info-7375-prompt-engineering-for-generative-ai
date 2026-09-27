# FRICTIONAL — Prasad S, week-01 video
 
Process log for the week-01 explainer video (lesson 01, randomness and first prompts). Short dated entries, written during the session.
 
---
 
## Entries
 
### 2026-09-25 — brutalist.art setup: the ElevenLabs guard blocks its own toolkit
 
- **Date and what I was working on:** Setting up the external `brutalist.art` checkout (sibling of this course repo) per `prerequisites/brutalist-video.md`, so I can later build an ai-explainer reel. Toolkit revision: `6a8380ae169cca81e0633664a65c958f5c12ab4b`.
- **I tried / expected:** Ran `./setup --install` then `./setup` in a fresh venv. I expected the readiness table the prerequisite and HOW-TO describe, with some rows possibly blocked by missing system tools.
- **What happened:**
  - No table at all. Both runs exited 1 at the ElevenLabs guard, listing 10 files, all under the toolkit's own `youtube/brutalist/` example reels.
  - How the guard works (Claude Code read this in `setup`, lines 102–116, and reported it to me). Before any dependency check, it runs `grep -rqiE` over the whole checkout for four patterns: the ElevenLabs API-key env var name, the ElevenLabs domain, `"engine": "elevenlabs"` in JSON, and the `xi-api-key` header. Its own comment says *functional* ElevenLabs references are bugs and prose mentions are allowed. On any hit it prints the files and `exit 1`, so the readiness table is never reached.
  - The guard has no ignore or exclude mechanism. The only exclusions are hard-coded: `.git`, `node_modules`, `__pycache__`, `.claude`, `CHANGELOG*`, and `setup` itself. There's no flag, no ignore file, and no env var. `art` has nothing either.
  - Why these 10 are false positives with respect to the guard's intent:
    - 6 files are narration and prompts for the toolkit's own film *about* `setup`: `claude-liam-brutalist-command-setup/{SCRIPT.md, PROMPTS.md, beat_sheet.json, vertical/PROMPTS.md, vertical/beat_sheet.json}` and `shorts/claude-liam-brutalist-command-setup-short/PROMPTS.md`. They quote the guard's own pattern list and code on screen. That's documentation of the guard, and the guard matches its own description.
    - 4 files are demo fixtures holding legacy beat sheets with `"engine": "elevenlabs"`: `claude-liam-brutalist-runtime-brand-variant/demo/{canonical/beat_sheet.json, book-example/lectures/chap01-lecture/beat_sheet.json}` and `claude-liam-brutalist-skill-your-turn/demo/{fixture-beat_sheet.json, fixture-beat_sheet.applied.json}`. These are literal functional-looking config, but they are inputs to recorded demos, not live settings.
    - Reachability check (Claude Code ran this at my instruction; I reviewed the result rather than running the greps by hand): grepped `skills/make/ai-explainer/`, `runtime/scripts/`, `art`, and `setup` for every flagged folder and file name. **Zero hits.** A repo-wide grep found references only inside those same example reel folders (their README, build-state, CHECKS-REPORT, RUN-LOG) and the `youtube/brutalist/` index files (`WATCH.md`, `playlist.json`). No code path I use loads them.
- **What I did:**
  - First (Claude's attempt, which I later reviewed): it tried to run a scratch copy of `setup` with the guard block cut out, just to see the table. Claude Code's permission system refused that as weakening a safety check. We didn't try another workaround, and I agree with that call: it would have hidden the finding rather than dealt with it.
  - Then, on my instruction, Claude Code deleted exactly those 10 files from my local clone and **did not edit `setup`**. `git diff HEAD -- setup` is empty, and `git status` shows only the 10 `D` lines plus the untracked `.venv/`.
  - Why this keeps the guard's intent instead of weakening it: the pattern list, the grep scope, the exclusions, and `exit 1` are all unchanged. Any new functional ElevenLabs reference anywhere in the checkout, including my own reel if it lives inside the toolkit, still fails setup. Claude Code removed only inert example content that was matching its own documentation, at my direction — I set the boundary that detection logic in `setup` itself was not to be touched. Suppressing the check with an exclude or a patch would have blinded it for everything.
  - Rerun result: `./setup` now gets past the guard and prints the table. Fonts are ready. Everything else is blocked on real missing dependencies (ffmpeg, Node ≥ 20/npm, Python packages; see the next entry).
- **What Claude or another person contributed:** The approach here — root-cause the guard rather than patch around it, verify reachability before deleting anything, and hold the line at "don't touch detection logic" — was worked out first in a planning conversation with Claude (chat), before I gave the instruction to Claude Code. Claude Code (Opus 5.5) then read `setup`, ran the greps, sorted the hits into "quotes the guard" and "legacy fixture", and ran the deletion and reruns. I chose deletion over patching, set the boundary, and asked for the reachability grep before deleting anything. I accepted Claude's classification based on its report of the matched lines. 
- **What I understand now / still do not understand:**
  - Now: the guard is a repo-wide content scan, not a check on what the runtime actually uses. So it can't tell a film *about* the guard from a violation of it.
  - Still open:
    - Upstream still ships these files, so every fresh clone at this revision will fail the same way. This should go to the instructor rather than be fixed silently.
    - The deleted files leave those three example reels (and the one short) incomplete in my local copy.
    - The guard scans `.venv/` too (not excluded), and the prerequisite puts the venv inside the checkout. A third-party package that ever contained one of the patterns would trip it.
- **Evidence and next step:**
  - Evidence: `git -C ../brutalist.art status --short` (the 10 deletions). The first failing `./setup` output lists the same 10 paths, and the post-deletion readiness table is recorded in the next entry.
  - To restore the files: `git -C ../brutalist.art checkout -- youtube/brutalist`.
  - Next: install Python 3.11, Node 20, and ffmpeg, rebuild the venv, and get a green table.
### 2026-09-25 — Python 3.9 can't install the voice engine
 
- **Date and what I was working on:** Same session. Getting `./setup --install` to actually install the Python dependencies.
- **I tried / expected:** A venv from the default `python3`. I expected pip to install `requirements.txt`.
- **What happened:** The only Python on the machine is the macOS system 3.9.6. pip couldn't resolve `kokoro-onnx>=0.4`: every 0.4.x needs `onnxruntime>=1.20.1`, which doesn't install on 3.9. There was also no `npm`, `node`, `ffmpeg`, or Homebrew. `setup`'s own Python check is only `command -v python3`, so it would mark 3.9 as fine even though its hint says "3.10+". The course prerequisite says 3.11+.
- **What I did:** Approved Python 3.11 — identified, in a planning conversation with Claude, as satisfying both the 3.10+ and 3.11+ mentions — as the fix. The plan is Homebrew, then `brew install python@3.11 node@20 ffmpeg`, then rebuild `.venv` with `python3.11`. Homebrew's installer needs my macOS password (sudo), so I ran that step myself.
- **What Claude or another person contributed:** Claude Code found the version conflict in the pip output and pointed out that `setup`'s Python check doesn't enforce the version its own hint gives. The reconciliation — that 3.11 satisfies both documents' stated minimums — came out of a separate planning discussion with Claude (chat); I approved it and made the final call to proceed on that version.
- **What I understand now / still do not understand:** A readiness check that only tests "is it installed" can pass on a version that can't install the rest of the stack. I don't yet know whether `faster-whisper` and `manim<0.19` are fine on 3.11. The next `--install` run will show it.
- **Evidence and next step:** Readiness table after the guard fix, still on 3.9:
```text
  audio (Kokoro Bella/Onyx)    ❌ blocked   (ffmpeg, kokoro-onnx, Kokoro synth smoke test)
  captions + word clock        ❌ blocked   (ffmpeg, faster-whisper)
  Manim beats                  ❌ blocked   (ffmpeg, manim, Pillow)
  Manim equation beats         ❌ blocked   (ffmpeg, manim, LaTeX + dvisvgm)
  Remotion beats + bookends    ❌ blocked   (Node >= 20, npm install)
  slates / previz / compile    ❌ blocked   (ffmpeg, Pillow)
  fonts (EB Garamond + Oswald) ✅ ready
```
 
  Next: rerun `./setup --install` and `./setup` on 3.11 and record the table.
 
### 2026-09-25 — Rebuilt on Python 3.11: six of seven features ready
 
- **Date and what I was working on:** Same session. Installed the toolchain and rebuilt the toolkit venv on 3.11.
- **I tried / expected:** Installed Homebrew myself (it needs my password). Then had Claude Code run `brew install python@3.11 node@20 ffmpeg`, `rm -rf .venv && python3.11 -m venv .venv`, and `./setup --install`. I expected a green table apart from the LaTeX row.
- **What happened:**
  - Installed versions: Python 3.11.16, Node v20.20.2 (npm 10.8.2), ffmpeg 9.0.2. `node@20` is keg-only in Homebrew, so it isn't on PATH by default. The runs used `PATH=/opt/homebrew/opt/node@20/bin:$PATH`.
  - The first `--install` on 3.11 still failed pip. `pycairo` (pulled in by `manim<0.19`) couldn't build: `Did not find pkg-config` and `Dependency lookup for cairo ... failed`. The npm install for Remotion succeeded.
- **What I did:** Approved `brew install pkgconf cairo pango`, which Claude Code identified as the missing system libraries after reading the pycairo build failure. Neither the prerequisite nor HOW-TO lists these. On the rerun, pip installed everything. `npm install` rewrote the tracked `runtime/remotion/package-lock.json`; that's a local change I'm leaving uncommitted.
- **What Claude or another person contributed:** Claude Code ran the installs, read the pycairo meson log to find the missing `pkg-config` and cairo, and proposed `pkgconf cairo pango` as an extra step. I approved that step, approved the Homebrew install, and ran the Homebrew installer myself.
- **What I understand now / still do not understand:** "Python 3.10+, Node 20, ffmpeg" is not the full list of system prerequisites on a clean Mac. cairo, pango, and pkg-config are also needed for Manim. The ElevenLabs guard still passes with the new `.venv/` inside the checkout. I haven't checked whether `setup_smoke_kokoro.py` passing means a full reel renders. `./art smoke` is the documented proof, and I haven't run it yet.
- **Evidence and next step:** `./setup` on 3.11 (exit 1 only because of the equation row):
```text
  audio (Kokoro Bella/Onyx)    ✅ ready
  captions + word clock        ✅ ready
  Manim beats                  ✅ ready
  Manim equation beats         ❌ blocked   (LaTeX + dvisvgm — not used for this reel)
  Remotion beats + bookends    ✅ ready
  slates / previz / compile    ✅ ready
  fonts (EB Garamond + Oswald) ✅ ready
```
 
  Per the prerequisite, I'm recording the equation row honestly as blocked and not using equation beats in the first video. Next: draft the evidence packet for expected vs. observed counts.

### 2026-09-25 — Running lesson 01 at temperature 0.5 without editing main.py

- **Date and what I was working on:** Same day. Building the evidence packet: comparing expected and observed top-class counts at temperature 1.0 (the shipped demo) and 0.5, with seed 7 and n=1000 held fixed.
- **I tried / expected:** I wanted to run `lessons/01-randomness-and-first-prompts/code/main.py` at temperature 0.5, changing only the temperature. I expected there to be a supported switch for it, like a CLI argument or an environment variable.
- **What happened:** There isn't one. At my instruction, Claude Code read `docs/en.md` and the full `code/main.py` before running anything. `__main__` just prints `demo()`, and `demo()` calls `probabilities([1, 2, 3])` and `sample([1, 2, 3])` with no temperature argument, so the shipped script always runs at the default 1.0. There's no `argparse`, no `sys.argv`, no `os.environ`, and no config file. `docs/en.md` asks for a comparison at 0.5 and 2.0 but doesn't document a way to run one.
- **What I did:**
  - I set the rule that `main.py` must not be edited. The supported route is the `temperature=` keyword that both public functions already take.
  - Claude Code imported the unchanged module and called `probabilities([1, 2, 3], temperature=0.5)` and `sample([1, 2, 3], count=1000, seed=7, temperature=0.5)` directly, using the same system Python 3.9.6 as the first run. `git status` showed no changes under `lessons/`.
  - Saved both runs as `evidence/temp-1.0.json` and `evidence/temp-0.5.json`. Before committing, Claude Code re-ran both calls and checked that the saved files match a fresh run exactly (both matched).
- **What Claude or another person contributed:** Claude Code read the source and docs, confirmed there's no temperature option, wrote and ran the direct-call command, and computed the expected counts (probability × 1000) and the one-standard-deviation spread for 1,000 draws. I decided not to edit `main.py`, chose to hold seed and n fixed, and set the comparison (temperature 1.0 vs 0.5). I wrote the prediction, verdict, reasoning, and limitation in `evidence/ANALYSIS.md` myself. Claude Code copied them in word for word.
- **What I understand now / still do not understand:** The lesson's "compare at 0.5 and 2.0" step assumes you'll call the functions yourself. The shipped script only demonstrates temperature 1.0. I haven't run 2.0 yet, so the pattern in `ANALYSIS.md` is two data points, not a trend.
- **Evidence and next step:** `evidence/temp-1.0.json`, `evidence/temp-0.5.json`, `evidence/ANALYSIS.md`. The exact command is in the chat session; it imports `main` from `lessons/01-randomness-and-first-prompts/code` and prints the JSON. Next: decide whether to add the 2.0 run before building the beat sheet.

### 2026-09-25 — `./art smoke` can't pass at this revision; pipeline checked with a worked example instead

- **Date and what I was working on:** Same day. Getting positive proof that the brutalist.art pipeline actually renders (audio generated, video compiled) before I build my own reel. A green `./setup` table only proves the dependencies import.
- **I tried / expected:** `./art smoke`, the toolkit's documented end-to-end proof. It builds `examples/_smoke/` in a temp folder and checks the decoded mp4. I expected it to pass now that setup was 6/7 green.
- **What happened:**
  - Smoke failed at the first gate, and so did two of the three things we tried next:
    - **Smoke:** it failed at the very first gate. Real output: `[kokoro] REFUSED: metadata.slug must be a filename, not a path` → `[smoke] FAIL: generate_audio_kokoro.py failed`. The fixture's slug is `"_smoke"` (`examples/_smoke/beat_sheet.json:4`). `runtime/scripts/build_safety.py:185-187` only allows slugs matching `[A-Za-z0-9][A-Za-z0-9._-]*`. `_smoke` isn't a path; it's rejected only because it starts with an underscore. So GATE 0 (narration) never runs, nothing is rendered, and the smoke test proves nothing either way about real reels. The error message is also misleading.
    - **`claude-debunked`**, the first worked example I asked for: it failed the same safety module in a different way. `metadata.voice and voice_kokoro disagree`. Its metadata still has a legacy `"voice": "NikBearBrown"` (plus a leftover `voice_env` naming the old paid provider) next to `voice_kokoro: am_onyx`.
    - **`claude-liam-algorithmic-art`** (12 beats, similar size) was used instead. Kokoro audio worked on the first try: 12 MP3s, `voice=am_onyx`, 17.8 s to 37.2 s per beat, "cost $0.00".
    - The first `./art run` stopped at GATE F: `has no FACTCHECK.md`. The worked example doesn't ship its paperwork set.
  - The second run, with the toolkit's documented previz-only exception `ART_FACTS=0`, rendered all 12 Remotion scenes (`[remotion] B00: ok … BOUT: ok`). It compiled `claude-liam-algorithmic-art-slate.mp4`: 319.7 s, H.264 1920×1080 at 24 fps plus AAC audio, 23.1 MB, mean volume −27.1 dB. Then **GATE V (frame-level visual QC) failed** on 24 sampled frames: 10 BLOCKER `edge-bleed` (B02–B04, B06, B07) and 4 MAJOR `low-contrast`. `./art run` exited 2.
- **What I did:**
  - I didn't fix the `_smoke` slug or the `claude-debunked` metadata. I didn't disable GATE V. I didn't build anything inside the toolkit folder: the example was copied to a scratch folder, which CLAUDE.md rule 3 requires.
  - `ART_FACTS=0` was used only for this pipeline test on a study copy, never for my own reel. My reel will carry its own FACTCHECK/SHOTLIST paperwork.
  - Result: **the pipeline test passed.** Audio generation, Remotion scene rendering, and compiling into an mp4 with an audio track all work on this machine. I spot-checked the compiled video myself: the audio is clear, the video renders correctly, and there's no corruption. That's the positive proof the smoke test couldn't give.
  - GATE V still reported 14 flags. They're on the toolkit's own sample content (`claude-liam-algorithmic-art`), not on anything of mine. On the contact sheet, the B02–B04 edge-bleed flags sit on full-frame generative flow-field art that seems meant to run off the edges. My decision: they aren't ours to fix. My own reel still has to pass GATE V on its own merits.
- **What Claude or another person contributed:** Claude Code ran the smoke test, traced the refusal to the regex in `build_safety.py`, found the `claude-debunked` voice conflict, picked the other example when that one failed (my instruction allowed "whichever worked example"), chose to render in a scratch copy at `--height 1080`, used `ART_FACTS=0`, probed the mp4 with ffprobe and volumedetect, and read the GATE V report and contact sheet. I decided the smoke failure needed a real render as a replacement rather than just being written down, and set the standard of showing actual output, not exit codes. I spot-checked the compiled cut (audio, video, corruption) and decided the pipeline test passed, and that the GATE V flags on the sample content are out of scope.
- **What I understand now / still do not understand:**
  - Now: three pieces of toolkit content at this revision (`_smoke`, `claude-debunked`, the example's missing paperwork) predate newer safety checks in the same toolkit. The checks are stricter than the bundled examples, so "the example fails" doesn't mean "the pipeline is broken."
  - Still open: whether my own reel will pass GATE V. I didn't settle whether the edge-bleed check is a false positive for full-bleed art in general; I only decided it doesn't matter for this test.
- **Evidence and next step:**
  - Evidence: the smoke output above; toolkit revision `6a8380ae169cca81e0633664a65c958f5c12ab4b`. The render lives in the session scratch folder (not committed; generated media): `claude-liam-algorithmic-art-slate.mp4`, `_qc/REPORT.md`, `_qc/contact_sheet.png`.
  - Next: report the `_smoke` slug and the `claude-debunked` metadata to the instructor, then start my own reel's beat sheet.

### 2026-09-26 — First review cut: two toolkit rendering limits (documented, not fixed upstream)

- **Date and what I was working on:** Building the first review cut of "Less Room to Wander" after signing off the narration (PEDAGOGY.md). Kokoro `af_bella` audio: 11 beats, 237.0 s. Toolkit revision `6a8380ae169cca81e0633664a65c958f5c12ab4b`.
- **I tried / expected:** After I signed the narration, Claude Code ran `./art run <reel> --height 1080` with every gate on. The expectation was that each scene would animate across its whole narration: the table rows landing on their spoken numbers, and the Beat 2 writer correcting its sentence on screen.
- **What happened:**
  - The cut compiled (237.2 s, 11/11 beats filled). GATE V reported 0 BLOCKER and 6 MAJOR (`underfill` on B01, B05, BOUT). Looking at the frames showed two worse problems the gate didn't flag.
  - **Bug 1: fixed-length compositions.** `runtime/scripts/remotion_scenes.py` renders each scene at the length registered in `Root.tsx`, then freeze-holds the last frame (`tpad=stop_mode=clone`) to fill the narration. Only compositions with a `calculateMetadata` that reads `durationSeconds` can match the audio. `ExecutedData` is fixed at 450 frames (15 s), so table rows timed after 15 s never appear. In B04, at 21 s, only 2 of 4 rows were showing. `ReqBars` (14 s) and `FormACard` (10 s) are also fixed; they're static after their intro, so that's harmless there. The Beat 2 writer defaults to 20.2 s, so B01's performance was cut at 11.1 s.
  - **Bug 2: single-word triggers.** `BrutalistHesitantWriter` splits its text on whitespace and matches `triggerWords` one token at a time. A multi-word trigger ("gets more accurate") never fires, so the correction never happens. The ai-explainer SKILL.md's own worked example, which recommends the whole phrase `list of topics` as a trigger, would hit the same bug. Separately, every comma or period adds a 0.4–0.8 s pause, so four lines take about 11 s to type.
  - `FormACard` also caps its title at about 7% of frame height, so a short card can't reach GATE V's 55% fill minimum. The toolkit's approved "Form A" card and its own visual QC disagree.
- **What I did:** I chose the recommended options; Claude Code applied them.
  - **Durations:** Claude Code set `durationSeconds` to the measured audio on every composition that accepts it (B00, B01, B02, B07, BVDT, BHTF), and turned on `largeText` for the composer and code beats.
  - **Tables (2a):** Claude Code kept every `ExecutedData` row inside 15 s. In B04, rows 3–4 now appear as "At 0.5" is spoken, 2–4 s before their numbers; in B06, about 0.3–1.2 s early. Rows 1–2 still land on their spoken numbers (faster-whisper word timestamps).
  - **B05 (3a):** Claude Code moved B05 to `WantQuote`, with my two ANALYSIS.md sentences joined by an ellipsis.
  - **Upstream:** I decided not to patch the toolkit upstream. Both limits are logged here to report to the instructor.
- **What Claude or another person contributed:** Claude Code found both bugs by reading the rendered frames and then the toolkit source (`remotion_scenes.py`, `Root.tsx`, `BrutalistHesitantWriter.tsx`), and it proposed the options. I chose 1a/2a/3a, asked for a flag if the B01 fix looked confusing, and asked for these limits to be documented rather than fixed upstream.
- **What I understand now / still do not understand:** A green gate and a correct film are different things: GATE V passed B04's frames even though half its table never appeared. I haven't decided the B01 wording yet. Option 1a would briefly show "the sample gets less accurate." mid-correction, a different wrong claim, so Claude Code flagged it before rendering.
- **Evidence and next step:** `_qc/REPORT.md` and `_qc/contact_sheet.png` from the first cut (not committed; generated). Next: decide B01, re-render, and re-run GATE V.

### 2026-09-26 — Fixing the review cut, pronunciation, and the first `./art final` attempt

- **Date and what I was working on:** Same day. Clearing the review-cut defects, fixing how the narrator says "Namaste" and "Prasad", and exporting a 1080p final.
- **I tried / expected:** Claude Code applied my three decisions (single-word B01 trigger, table rows inside 15 s, bigger cards for B05/BOUT), then ran `./art final --height 1080 --out final/`. The expectation was that GATE T would pass once GATE V was clean.
- **What happened:**
  - **B01:** my first choice ("more" → "less", "accurate" → "room to wander") would have shown "the sample gets less accurate." for about a second mid-correction, a different wrong claim. Claude Code flagged it before rendering. I chose "accurate" → "tightly bunched" instead. Claude Code reduced the writer's pauses so the four lines finish by about 8 s of the 11.1 s beat.
  - **B05:** the bigger quote card, `WantQuote`, turned out to print a hardcoded "Data: Anthropic, What 81,000 People Want from AI (2026)" line under my quote, a false attribution. It showed up in the rendered frames, not in the props. Claude Code reverted B05 to `FormACard`. Every other larger card Claude Code checked had `@NikBearBrown`, an "ACT ·" label, or unreadably small type baked in.
  - **Underfill:** so B05 and BOUT stay `FormACard` and still fail GATE V's 55% fill minimum. I approved running with `ART_STRICT=0` (MAJOR → warning, BLOCKERs still enforced), with the justification logged in BUILD-LOG.md. GATE V: 0 BLOCKER, 4 MAJOR (all that exception).
  - **Pronunciation:** espeak-ng says "Namaste" as nˈæmæst and "Prasad" as pɹˈæsæd. The toolkit script has no pronunciation control, but kokoro-onnx accepts phonemes. `tools/kokoro_phoneme_override.py` swaps only those words (nˌʌməstˈeɪ, pɹəsˈɑːd). With the swap off, it is sample-identical to the stock script. Only B00 and BOUT audio and scenes changed (checksums checked); B00 grew 0.15 s.
  - **`./art final`:** exited 2 with no video. GATE T FAIL ×3:
    - B02 and B07 `card-clip`: a false positive. The checker scans every column the code card spans, and the brand label below the card lined up with its right edge. Claude Code removed the label on those two beats and shortened their titles, which fixed both.
    - B03 `contrast`: `ReqBars` always draws the temperature-0.5 numbers in terracotta text, 2.74:1 on cream (below 4.5:1). Still open.
- **What Claude or another person contributed:** Claude Code rendered each round, inspected frames by eye (that's how the false credit, the clipped B07 code line and the B01 wording problem were caught), read the toolkit and kokoro-onnx source to find the phoneme route, and wrote and verified the wrapper. I made each decision: the B01 wording, keeping FormACard under ART_STRICT=0, the phoneme override. A speech-recognition spot check heard "Namaste" and BOUT's "Prasad" correctly but B00's "Prasad" as "preside"; I still need to judge that by ear.
- **What I understand now / still do not understand:** Three checks (GATE V, GATE T, and Claude Code inspecting the frames by eye) caught different things. GATE V missed the clipped code and the false credit; GATE T's card-clip check gave a false positive. I don't yet know which B03 fix is best.
- **Evidence and next step:** `TYPECHECK.md` (1 FAIL remaining: B03), `_qc/REPORT.md`, BUILD-LOG.md, `tools/kokoro_phoneme_override.py`. Next: decide B03, re-run `./art final`.

### 2026-09-26 — B03 accessibility fix, the final-path gate bug, and the exported final

- **Date and what I was working on:** Same day, closing out. Clearing the last GATE T failure (B03) and exporting the 1080p final into `final/`.
- **I tried / expected:** I chose to move B03 from `ReqBars` to `ExecutedData` in probability mode: four rows (top token at 1.0 and 0.5; the other two tokens at 1.0 and 0.5, labeled "(sum of tokens 0 and 1)"), with the narration unchanged. Claude Code then re-ran GATE T and `./art final`. The expectation was that a clean GATE T would let the final export.
- **What happened:**
  - **B03 contrast.** `ReqBars` always draws its second-series numbers and legend in terracotta text, 2.74:1 on cream, below GATE T's 4.5:1 WCAG minimum, and the component has no colour prop.
  - **Why my exact spec didn't fit.** In probability mode, four label-plus-bar rows and the 0–100% scale ran past the bottom of the frame and pushed the source note off screen, even with the title removed. GATE T still passed, because it checks type, not layout against the frame; Claude Code caught it by measuring the frames. Table mode with the long labels wrapped and reached 97.9% of the frame height. What fits: table mode with short row labels and "Other two = sum of tokens 0 and 1 · evidence/temp-\*.json" in the on-screen note. A 16-word note first failed GATE T's 12-word limit, so it was shortened to 11. Content now ends at 91% of the height, the same as B04. GATE T: PASS on all 11 beats.
  - **Final, second failure.** `./art final` then exited 2 again with `final/` empty, for a different reason. The final compile (`runtime/scripts/compile.py`) runs GATE V through its own hardcoded call to `qc/final_frame_check.py` and ignored `ART_STRICT=0`. So the four B05/BOUT `underfill` MAJORs, which the review path (`run.sh`) already let through under my approved exception, refused the final.
  - **Final, third failure.** Claude Code's first patch passed `--lenient` under `ART_STRICT=0`, but the final was still refused. With `--lenient` the checker returns exit 1 ("warnings only"); `run.sh` fails only on exit ≥ 2, but `compile.py`'s `sh()` failed on any non-zero exit.
- **What I did:**
  - I accepted the table-mode B03, which differs from my spec in two ways: no bars, and the "sum of tokens 0 and 1" wording is in the note, not the row labels.
  - I approved a local patch to `compile.py` so the final path honors `ART_STRICT` the same way `run.sh` does, with BLOCKERs still enforced either way.
  - Claude Code wrote the patch in two iterations: first `--lenient` under `ART_STRICT=0`, then treating exit 1 as a pass (failing only on exit ≥ 2).
  - BUILD-LOG.md records the exact diff and the justification. The review path already honored the approved exception; the final path had a separate hardcoded check that ignored the same flag; the patch fixes that inconsistency and doesn't create a new exception.
  - BUILD-LOG.md also states the one side effect: in strict mode, a MINOR-only result now passes the final too, as it already did in `run.sh`.
  - Result: `ART_STRICT=0 ./art final --height 1080 --out final/` exited 0 and wrote `final/less-room-to-wander.mp4` (237.4 s, 1920×1080 H.264 + AAC, sha256 `cf92ac21e352926c681cd5b401b7fd8781d53327f0b51a4b5cf10407ec4557d1`) with its `verified.json` receipt. GATE V on the final candidate: 0 BLOCKER, 4 MAJOR (the B05/BOUT exception).
  - Claude Code checked the final's frames: no burned-in beat labels, and the new B03 table is present.
  - I watched the review cut with sound after the pronunciation fix and approved it.
- **What Claude or another person contributed:**
  - Claude Code rendered each B03 variant, measured where the content ended against the title-safe line, and read `compile.py`, `run.sh` and `final_frame_check.py` to find both final-path problems.
  - It wrote and tested both patch iterations, updated BUILD-LOG.md, SOURCES.md, README.md and BUILD-PROMPT.md, and verified the exported file (streams, duration, volume, frames).
  - I made the decisions: option (a) for B03, accepting the table-mode deviation, the `compile.py` patch and how it's framed, and approving the review cut.
- **What I understand now / still do not understand:**
  - A gate's exit-code contract matters as much as its flags. The same checker run in two places gave two verdicts, because one caller treated "warnings only" as failure.
  - Every accessibility or layout fix here traded something visible (B03's bars, B05/BOUT's fill), and those trades are mine to own.
  - Still open: the toolkit's local changes (10 removed example files, the regenerated `package-lock.json`, the `compile.py` patch) aren't reported upstream yet. Neither is the list of toolkit bugs from these entries.
- **Evidence and next step:** `final/less-room-to-wander.mp4` and `final/less-room-to-wander.verified.json` (not committed; the MP4 goes to Canvas), BUILD-LOG.md, `TYPECHECK.md` (PASS). Checkpoint 3 is commit `2eb73eb288510528a096016c8f96664fee7b578c`. Next: submit the final MP4 and commit hash on Canvas, and send the instructor the toolkit bug list.
