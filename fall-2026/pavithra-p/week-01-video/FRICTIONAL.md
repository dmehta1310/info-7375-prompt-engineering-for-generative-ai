# Frictional — Week 01 video

Pavithra Prasad · INFO 7375 · Week 01 video ("Thousands of Years, Divided")

> **How this log was written:** events are dated on the day they happened. Claude and I wrote it together from our working session, and I reviewed every entry. On 2026-09-25 we reorganised it into the course's entry format, because the first version described Claude's technical fixes as if I had done them.

---

## 2026-09-22 — Understanding the assignment and picking a topic

- **I tried:** reading the brief and asking Claude for a plan. I asked which Chapter 1 topic would be easy to explain and still meet the rubric.
- **What happened:** Claude listed the eligible topics. It recommended "subtracting the maximum" (Part 2) first, then "expected 665.24 vs observed 630" (Part 2) as the easiest.
- **What I did:** I picked the 665.24 vs 630 topic and asked Claude to check it against the rubric before going further.
- **What Claude contributed:** the topic list, a rubric comparison, and a real run of `lessons/01-.../code/main.py` (counts 102 / 268 / 630 at seed 7). It also found that seed 7 is the lowest of seeds 0–99.
- **Unsure at this point:** which topic to pick. I wanted one I could explain without going too deep, and I couldn't tell whether Part 1 (mostly theory) or Part 2 (mostly numbers) would suit that better.

## 2026-09-23 — Switching from Part 2 to Part 1

- **Friction:** when I read the Part 2 beat sheet and the explanation of the 8 beats, I could not follow it. It was too many probabilities for me to defend every claim, and the rubric requires that.
- **What I did:** I said so, and asked whether a Part 1 topic could still score well. I chose **"a training-scale slogan restated as a division with a hidden assumption"** because it only needs multiplication and division.
- **What Claude contributed:** a comparison of the Part 1 topics against the rubric, and a run of `research/llm_scale.py` confirming the chapter's numbers (1,426.0 / 1,711.2 / 2,138.9 / 2,851.9 years). It also suggested an extra hidden assumption: reading 24 hours a day.
- **Accepted / changed:** I accepted the Part 1 topic and the 8-hours-a-day extension, on condition it is labelled on screen as an extension. The Part 2 draft files were deleted, not submitted.
- **Evidence:** `evidence.py`, `evidence.json`.

## 2026-09-23 — Reviewing the beat plan and narration

- **I tried:** reading the beat plan and full narration before any audio was made.
- **What I did:** I brought a set of wording suggestions and asked Claude whether to use them: B01 ("reported starting number"), B02 ("the chapter's approximation"), B04, B05 (label the extension clearly) and B06 (the unique-tokens limit). I skipped the Claude-screen opening, since it would need a real, dated Claude response.
- **Changed, not just accepted:** Claude agreed with them but reworded one. For B04 it pointed out that "a difference of 1,426 years" would sound identical to the 300-wpm answer (also 1,426), so we used "the slowest reader's answer is twice the fastest" instead.
- **Two corrections I required before approving:**
  - B00: "It isn't a measurement" → "an estimate produced by division". The 300 billion tokens is *reported*; only the reading time is *estimated*.
  - B06: "describes how much text went in" → "translates a reported training-token count into hypothetical human reading time". The old line contradicted the sentence before it.
- **Also caught:** Claude said the script was ~450 words. The real count was 393 at that point, and 403 after my two corrections (~2:30 of speech).
- **Evidence:** `beat_sheet.json` → `metadata.review` (approved 2026-09-23).

## 2026-09-23 — Tool problems (Claude Code handled these; I followed along)

I asked Claude to build the video and not commit or push anything. It hit these problems and handled them.

- Homebrew refused to install ffmpeg because of an unrelated MongoDB tap on my Mac. Claude skipped that check with environment flags instead of changing Homebrew's trust settings.
- Manim needed the cairo/pango libraries (`brew install cairo pkg-config pango`).
- Brutalist's `./setup` stopped on its own example files ("ElevenLabs reference found"). Claude ran the same readiness checks by hand; the Kokoro voice test passed.
- The toolkit's quality gates rejected scenes several times: text a hair past the margin, too much empty space mid-scene, overlapping captions. Each was fixed and only that scene re-rendered.
- **I asked:** whether all of this was free (yes: Kokoro, Manim and ffmpeg run locally; $0), and what Claude had installed or changed outside my folder (listed in chat; nothing in the course repo was edited).
- **What I don't fully understand:** most of the setup terms (Homebrew taps, cairo/pango, the quality gates) were new to me. I followed what Claude did and checked the results, but I couldn't have fixed those errors on my own yet.

## 2026-09-24 — I spotted uneven letter spacing

- **What happened:** watching the video full screen, I noticed gaps inside words: "slo gan", "parap hrased", "co urse". None of the automated checks had caught it, and neither had Claude's frame check.
- **What I did:** I sent a screenshot and asked about it. I also asked whether I needed an intro (Claude said no: B00 already works as one, and extra time would be padding).
- **What Claude contributed:** the cause (a known Manim text-spacing issue at small sizes) and the fix (render text 4× larger, then shrink it). In the same round it flipped the B04 slider to match the bar order and added my name under the title.
- **Decision:** I asked for all fixes in one round and said this would be the last version.
- **Evidence:** final `thousands-of-years-divided.mp4` (2:28), in the Canvas zip.


## 2026-09-25 — Local commit, and the video/GitHub question

- **What happened:** when staging my folder, only 18 of 30 files were picked up. The course repo's `.gitignore` blocks all `.mp4` and `.mp3` files ("Keep generated audio/video out of Git"), but the assignment asks for the mp4 on GitHub.
- **Decision:** I chose to follow the professor's repo rule. The video goes only in the Canvas zip, and `README.md` explains why it isn't on GitHub.
- **Did:** committed my folder locally on branch `pavithra-p/week-01-video`, with nothing pushed.
- **Evidence:** commit `ef322f2` (first local commit; a later commit adds these final log edits).

## 2026-09-27 — Final correction to B05, before submitting

- **What happened:** a review of my zip pointed out that in B05 the clock reached "8 hours" while the bars still showed the 24-hour numbers, and the bars then grew through values like 2,702 that match no real assumption. It also said my Finder zip had about 30 hidden Mac files, and that my log's word count (393) was out of date.
- **What I did:** asked Claude to check each point against the actual files before changing anything, then approved the fix. Three were right: the B05 mismatch, the 30 `__MACOSX`/`._` files, and the word count (403 after my corrections). One was wrong: it said B00 had a duplicated animation line, but that line appears only once in `scenes.py`, so I didn't change anything there.
- **What Claude contributed:** rewrote B05 so one `hours` tracker drives the clock, bars and numbers together. Every value on screen is now `years_at(wpm) × 24 / hours`, using the same whole hour the clock label shows (e.g. at 23 hours, 300 wpm shows 1,488.0). Only B05's code changed. The other seven scenes were re-rendered from unchanged code and compared frame by frame with the previous version.
- **Evidence:** `scenes.py` (B05), final `thousands-of-years-divided.mp4` and its SHA-256 in `README.md`. Next: push to GitHub and submit the zip on Canvas.

---

## What I understand now

- "Thousands of years to read" is not a measured fact. It is an estimate: reported tokens × words per token ÷ reading speed.
- The only reported number is ~300 billion training tokens, from the GPT-3 paper. Everything after that is a choice someone made.
- There are three hidden guesses: reading speed, 0.75 words per token, and reading 24 hours a day with no sleep.
- Half the reading speed means double the years (150 wpm gives twice the years of 300 wpm), and reading 8 hours a day instead of 24 triples every answer.
- Every version is still far more than a lifetime, so the slogan's basic point survives. But the calculation says nothing about whether the model understood anything or is accurate.
- A token is a chunk of text, not a word, which is why the 0.75 conversion is needed at all.
- Automated checks don't catch everything. The uneven letter spacing passed every quality gate, and I only saw it by watching the video full screen.

## What I still don't understand / next step

- Whether all ~300 billion training tokens were different text, or whether some was repeated during training. If so, the *unique* text is smaller than the slogan suggests.
- Where 0.75 words per token comes from, and how much it changes for other languages or code.
- Next step: check the 300 billion figure in the GPT-3 paper myself. I only used it as cited by the course script.
