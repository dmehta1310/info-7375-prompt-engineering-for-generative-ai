# PROMPTS — token-not-word

Beat-prefixed prompts for open (human-filled) slots. This reel has **two**, both
in B05, both screenshots of real dated Claude answers. There are no gen-AI
prompts in this reel: every other beat is drawn by `scenes.py`, and the two
images below must be genuine captures — a generated or re-typed mock would make
B05's evidence claim false.

---

## B05 — `media/B05-claude-strawberry.png`

**What to capture.** A screenshot of a real Claude conversation, dated
22 Sep 2026, in which Claude is asked how many times the letter **r** appears in
**strawberry**, and answers **3** — with the visible rationale
"3 times … in straw, ber, and ry".

**Why this exact frame.** B05 shows this capture as one of the two correct,
dated answers. It is also the sole source for B06, which turns on the gap between
Claude's narrated split (`straw` / `ber` / `ry`) and the tokenizer's actual split
(`str` / `aw` / `berry`). The rationale text must be legible in the capture or
B06's central claim is unsupported.

**Framing.** Crop to the question and the answer. Roughly 16:9 or 4:3, landscape;
the scene fits it into a 4.9 × 2.7 unit frame and will letterbox rather than
stretch. Keep the date visible if your UI shows it. No personal information.

**Drop at.** `media/B05-claude-strawberry.png` — the scene picks it up
automatically on the next render; no beat-sheet edit needed.

---

## B05 — `media/B05-claude-blueberry.png`

**What to capture.** A screenshot of a real Claude conversation, dated
22 Sep 2026, asked how many times **r** appears in **blueberry**, answering
**twice**, with the visible letter-by-letter working "b-l-u-e-b-e-r-r-y".

**Why this exact frame.** It is the second correct answer, and it is what stops
the reel from overclaiming: two correct answers on the record are why B05 says
tokenization explains *unreliability*, not failure.

**Framing.** As above.

**Drop at.** `media/B05-claude-blueberry.png`.

---

## Until they land

`B05_DidItFail` renders a labelled empty frame for each missing file, printing
the filename it expects, so the review cut shows exactly what is outstanding.
The beat is a real rendered Manim beat, not a slate, and `./art run` will not
block on it.
