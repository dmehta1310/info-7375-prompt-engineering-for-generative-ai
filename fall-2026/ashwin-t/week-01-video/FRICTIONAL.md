# FRICTIONAL.md

Ashwin Thankachan — INFO 7375, Week 1 Explainer Video

The first two entries are my own notes. From the toolkit build (2026-09-23, ~21:50) onward,
Claude Code organised the entries from the session record (commands, printed output, file
timestamps) and my answers in chat. Understanding and decisions are mine, in my words.

---

## 2026-09-23 — Choosing the concept

- **Tried / expected:** expected to pick a topic quickly and build the same evening.
- **Happened:** couldn't pick; logits, softmax, temperature and seeds were just words to me. I also
  mixed up the 25-pt Week 1 video with the 100-pt Assignment 01 and looked for code points in
  the video rubric. There are none (15 explanation / 2.5 Frictional / 2.5 GitHub / 5 RQ).
- **Did:** worked the mechanism bottom-up (scores → percentages → weighted draw). Chose the
  shared-offset concept because I could explain it completely.
- **Claude:** explained the two assignments apart, ran the softmax comparisons, proposed the beat
  structure and the Beat 5 boundary. Accepted.
- **Understand / don't:** thought the offset disappears *because softmax subtracts the max*
  (corrected below). Still don't know why exponential is the right transform rather than just
  dividing raw scores by their total.

## 2026-09-23 — Prerequisite check

- **Happened:** `Python 3.9.6` (below the 3.11 minimum; it's the macOS system Python) and
  `zsh: command not found: ffmpeg`. git 2.51.0, node v25.8.0, npm 11.11.0 OK.
- **Planned:** Homebrew `python@3.12` + `ffmpeg`, leaving the system Python alone.
- **Claude:** identified 3.9.6 as the system Python.

> *Correction (2026-09-24):* those installs were planned, not done. At ~21:50 `python3.12` and
> `ffmpeg` were still "not found". See the next entry.

## 2026-09-23 (~21:50–22:05) — Toolkit install

- **Expected:** toolkit, evidence folder, Python 3.12 and ffmpeg already in place, as my build brief said.
- **Happened:** none existed. The toolkit's own doctor stopped on "ElevenLabs reference found" and
  its smoke test failed with `metadata.slug must be a filename, not a path` (fixture slug
  `_smoke`), both upstream bugs.
- **Did:** approved one global install, `brew install ffmpeg` (9.0.2). Used the existing Python
  3.13.7 (`kokoro-onnx` needs <3.14); everything else stayed local in `brutalist.art/`.
- **Claude:** found and ran all of this. Honestly, for me this part was straightforward because
  Claude did the installs; I didn't hit the problems myself.
- **Evidence:** toolkit commit `6a8380ae169cca81e0633664a65c958f5c12ab4b`.

## 2026-09-23 (21:58) — Evidence files

- **Happened:** `reference-output.txt` and `offset-output.txt` matched my brief digit for digit
  (`0.09003057317038046, 0.24472847105479764, 0.6652409557748218`, `bitwise identical?  True`),
  and were byte-identical under Python 3.9.6.
- **Claude:** generated all three files and added `intermediates_evidence.py`: both inputs become
  `[-2, -1, 0]` after subtracting the max, and all 1001 offsets 0..1000 are bitwise identical,
  covering every frame of the Beat 3 count-up. Accepted.
- **Not yet done:** I haven't re-run these myself (as of 2026-09-24 morning).

## 2026-09-23 — Script defensibility

- **Happened:** Claude flagged that Beat 3 credited the cancellation to max-subtraction (the same
  thing I wrote above), and that Beat 1 said "percentages that add up to one".
- **Did:** accepted a rewritten Beat 3 (same factor top and bottom → cancels; max-subtraction →
  the exact same digits) and "probabilities" in Beat 1.
- **Understand now:** if we add 1000, the size of the scores doesn't matter, because it cancels
  out in the numerator and the denominator.
- **Evidence:** `FACTCHECK.md` rows B03C, B03D.

## 2026-09-23 (22:05–22:23) — Audio and draft 1

- **Happened:** narration measured 137.06 s (2:17), under my 2:45 target. Draft 1 compiled (16/16
  beats) but Gate V failed: 3 MAJOR "underfill", B01A 49% and B05 26%/35% of the safe area (min 55%).
- **Claude:** wrote the `SoftmaxOffset` component and build/sync/verify tools (110/110 on-screen
  numbers traced); fixed a 15 s cutoff that hid Beat 5's last line.
- **Evidence:** draft-1 Gate V report (build folder, not kept here; the final one is `QC-GATE-V.md`); commit `7d8b432`.

## 2026-09-24 — Watching draft 1 (revision)

- **Expected:** a finished explainer.
- **Happened:** I followed that it's about logits and how the next token is predicted, but had
  no clue what softmax actually is or what the whole video was for. The start and the end felt abrupt.
- **Did:** asked Claude to explain softmax from scratch; it walked through e^score → add up →
  divide, with a slider demo where adding 1000 didn't move the bars. Asked for three changes:
  name and define softmax in Beat 1, add an intro that asks the question, and add a closing recap.
  These make the video longer, but for a reason a viewer gave, not padding.
- **Evidence:** commit "week-01-video: revise after draft-1 review". Folder decided: `fall-2026/ashwin-t/week-01-video/`.
  Still open: fork vs. direct push.

## 2026-09-24 — Drafts 2 and 3 (Gate V again)

- **Expected:** the revision plus the B01A/B05 fixes would pass Gate V.
- **Happened:** draft 2 failed with 5 MAJOR underfill defects, now on the text cards: B00 29%,
  B05 34%, B06 42% of the safe area at mid-beat. They reveal one line per sentence, so halfway
  through they are mostly empty. B01A (faint outline boxes) passed.
- **Did:** made the cards genuinely larger, and declared the line-by-line reveal to the toolkit
  (`qc.sparse_by_design` with a written reason in `beat_sheet.json`) instead of switching the
  check off. Draft 3: Gate V clean, 36 frames, 0 defects. Runtime 2:38.
- **Claude:** found the toolkit's documented option and made both changes.

## 2026-09-26 — Understanding the topic; checking the numbers myself

- **Happened:** after draft 3 I still didn't see the point of adding big numbers "to make them
  small", or what the topic is called and how it connects to Chapter 1.
- **Claude:** explained there are two different changes: +1000 is a *test* of whether size
  matters, and subtracting the max is the code's *safety trick* against overflow. The topic is
  softmax shift invariance; Chapter 1 covers it in "The subtraction that changes nothing
  important". Also showed which Part 2 concepts sit next to mine, so the video doesn't drift.
- **Did:** ran `main.py` myself. The numbers match `reference-output.txt`.
- **Still open:** why the exponential is the right transform in the first place (from my first entry).

## 2026-09-26 — Draft 4: one palette

- **Did:** asked for one consistent palette. B05 was the only dark card; now it's cream like
  every other beat. Skipped an extra "softmax arithmetic" beat on Claude's recommendation, to stay
  on one concept. Gate V clean again (0 defects).
- **Evidence:** commit "week-01-video: revise after draft-1 review".

## 2026-09-26 — Final render blocked by Gate T

- **Expected:** `./art final` to pass, since every draft had passed Gate V.
- **Happened:** Gate T (the typography check, which runs only on the final) failed 9 beats:
  the terracotta accent `#D97757` on cream measured 2.74:1 contrast (WCAG needs 4.5:1), labels
  were below the 41px minimum, and text crossed the title-safe edge. After the first fix, 5 were
  left: a 3-pixel title overhang in B03C/B03D, and the short grey `→` arrows in B04 read as tiny
  text. Moving the top label also dropped the B01 pipeline beats to 54% fill (Gate V needs 55%).
- **Did:** deepened the accent to `#A84A28` (5.42:1), same palette, raised labels to 32px, moved
  text inside the safe area, enlarged the arrows, made the pipeline boxes taller. Gate V 0
  defects, Gate T PASS 18/18, final master 158.5 s.
- **Understand now:** the gates check different things, and fixing one can break another, so
  all of them re-run every time.
- **Evidence:** `QC-GATE-V.md`, `QC-GATE-T.md`; commit "week-01-video: add final video and QC reports".

## 2026-09-27 — Checking the final frames myself

- **Did:** paused the final at B02C and B03B (1:11) and checked them. The numbers match the
  evidence files and `bitwise identical?  True` matches the printout. Asked for every em dash
  to be removed from on-screen text and narration.
- **Claude:** found 4 em dashes in the narration (B01D, B03B, B03D, B04C) and 6 on screen, and
  replaced them with a colon, full stops or commas, same meaning. Also spotted in my frames that
  the titles sat 12px right of the label above (left over from the Gate T margin fix) and
  aligned them. Regenerated the audio for those 4 beats; in B03B "Not approximately." became
  its own sentence, so the `bitwise identical?  True` box moved to the next pause (3.86 s).
- **Evidence:** commit "week-01-video: add final video and QC reports".

## 2026-09-27 — The video was invisible to git

- **Happened:** after copying the final into this folder, `git status` didn't list
  `w1-softmax-offset.mp4`. `git check-ignore -v` showed the root `.gitignore` line 33,
  `*.[mM][pP]4`, a blanket rule keeping audio and video out of the repo.
- **Did:** saw that classmates' week-01 videos are on `main`, added with `git add -f`, and planned
  to do the same. Before committing, TA Aravind Balaji answered in the class chat (2026-09-27,
  2:33 PM): the mp4 goes to Canvas only, all other files to GitHub. So I left it out of git. The
  video is in the Canvas zip; the GitHub folder has everything else.
- **Evidence:** commit "week-01-video: add final video and QC reports" (no mp4 in it).
