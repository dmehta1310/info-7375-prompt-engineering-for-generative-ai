# FRICTIONAL — Week 1 explainer

The 2026-09-25 notes are from the files that session left and from the transcript of where it stopped. The 2026-09-26 notes are from the commands run that day. This is not a reconstructed diary of feelings.

## 2026-09-25 — first build

- Working on: one Chapter 1 concept, "a seed makes a run repeatable; it does not make the answer true."
- Tried: call the course `sample()` with seed 7 twice and seed 99 once, then build a seven-beat reel in `brutalist.art`.
- What happened: seed 7 printed `{0: 102, 1: 268, 2: 630}` both times. Seed 99 printed `{0: 93, 1: 267, 2: 640}`. A review cut, `yash-s-seed-repeatable-slate.mp4`, was written at 22:47. `TYPECHECK.md` at 23:05 was still a fail on B00, B02, and B06 (type smaller than the floor).
- What I did: the session enlarged card type and re-rendered some beats. It did not get a clean master.
- Claude: drafted the sheet, narration, and renders. I would still have to defend every line.
- Still open that night: GATE T, and no `./art final`.
- Evidence: `FACTCHECK.md`, the slate file, `TYPECHECK.md` before it was overwritten on 2026-09-26.
- Next: the session ended on an organization spend limit.

## 2026-09-26 — type gate, then the frame gate

- Working on: finish the master and the Canvas files.
- Tried: re-measure the frames the type checker actually samples.
- What happened: B02 and B06 were not failing on the footer. The short letters in the spark line ("m", "w") were 39px, and the floor at 2160p is 41px. B00 was 7680×4320 because `ShellSession` is already a 3840×2160 composition and the renderer scales by 2, so its floor is 82px. The `%` prompt's slash was a wide, short blob under that floor. The on-screen prompt also still said `SET IN BEAT SHEET`.
- What I did: raised the spark line, enlarged the terminal type, set the prompt to `yash chapter-1`, and replaced `%` with `|`. GATE T then passed.
- Next failure: `./art final` refused on frame fill. A white card on cream is invisible to that check, and a dark terminal on a black page only counts the glyphs, so every beat was under 55% of the safe area. B01 then failed local contrast at 1.17:1 because of the translucent highlight behind the counts.
- What I did next: gave the cards a dark rule and made them fill the safe area, put the terminal on a cream page, and dropped the highlight bar so the counts stay white on black. Re-rendered. `./art final` wrote the master.
- Claude, this session: did the measuring, the scene edits, the renders, and these write-ups. I accepted the concept and the counts. I watched the master. The comparison table was too tall for three rows and the header line broke at the center, so that card was resized and the master was rendered again.
- What I understand: same seed, same sequence. A different seed, different counts, same probabilities. Repetition does not show the result is true. What this still does not show: the same counts on another Python or another machine.
- Evidence: `TYPECHECK.md` (pass, 2026-09-26 15:05), `_qc/REPORT.md` (0 blockers, 0 majors), `yash-s-seed-repeatable.mp4` (137.8s).

## Checked again

```bash
python3 -c "import sys; sys.path.insert(0,'lessons/01-randomness-and-first-prompts/code'); from main import sample; print(sample([1,2,3], seed=7)); print(sample([1,2,3], seed=7)); print(sample([1,2,3], seed=99))"
```

Python 3.13.5, 2026-09-26: `{0: 102, 1: 268, 2: 630}` twice, then `{0: 93, 1: 267, 2: 640}`.
