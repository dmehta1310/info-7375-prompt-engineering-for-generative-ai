# Prompt experiment report (v1 vs v2)

**Date run:** 2026-10-28 (UTC times in `experiment/log.csv`)
**Where:** claude.ai, a new incognito chat for every reply. **Model:** not recorded (no screenshots).
**Postings:** 20 from the 2026-10-27 snapshot, none reused from sampling. 14 data-titled + 6 US non-data "Analyst" roles, chosen with Claude's help.
**Split:** seeded shuffle (seed 7375) into 10 DEV / 10 HELDOUT → `experiment/split.json` (commit 10e8ee8)
**Hand labels:** `experiment/labels.json` using `LABELING_RULE.md` (commit 07577f0). All 20 labeled **before** any Claude run.
**Scores:** `experiment/results.txt` (made by `agent/experiment_score.py`)

## Steps, in order (commits prove the order)
1. Labeled all 20 postings by hand. → 07577f0
2. Ran **v1** on the 10 DEV postings. → 052d643
3. Wrote **v2** = v1 + one sentence, and committed it **before** any held-out run. → d711cfe
4. Ran **v1 and v2** on the 10 HELDOUT postings. → 7c160a8

## The one change in v2
> Extra rule (v2): if the posting is an internship or requires the candidate to be currently enrolled in a degree program, the verdict is "not relevant", because the candidate is a working professional, not a student.

**Why:** on DEV, v1's only disagreement with me was 8194291 (Data Analyst, Intern, US). I labeled it "relevant" because it passed my 3 checks. v1 said "not relevant" because the job needs current degree enrollment. After reading Claude's reason, I agreed with Claude, so v2 makes that reasoning an explicit rule. I did **not** change my label afterwards, to keep the test fair.

## Results
| | Matches my labels |
|---|---|
| v1 on DEV | **9/10** (missed 8194291) |
| v1 on HELDOUT | **10/10** |
| v2 on HELDOUT | **10/10** |
| v1 vs v2 on HELDOUT | **same verdict on 10/10** |

All 30 replies passed the validator. On 2 held-out postings (8194283, 8194285), v2's reason mentioned "the v2 rule" by name, so the sentence was read. v1 reached the same verdict on both without it.

## What I can and cannot conclude
- **Can:** both prompts matched my labels on every held-out posting.
- **Can:** the v2 change made **no measurable difference** to verdicts here.
- **Cannot:** say v2 is better or worse. They tied.
- **Cannot:** say anything about catching real matches. HELDOUT has **0** postings I labeled "relevant", so a prompt that always says "not relevant" would also score 10/10.
- Note: v2 pushes verdicts **toward** "not relevant" on internships, which is the **opposite** of my label on 8194291. I did not run v2 on DEV, so this is not measured.

## Limits
- Only 20 postings, and 19 of them labeled "not relevant". Many fail simply on location (Singapore, Bengaluru, Toronto).
- One model, one interface, one day. The model and settings were not recorded.
- Labeling had slips: I first labeled several postings wrong and corrected them after re-reading the text, and I changed my title rule mid-labeling (rule v2, dated in `LABELING_RULE.md`). In the end, that change altered no label.
- Replies were saved by pasting them into my tutoring chat, then a heredoc command. The log shows **save time**, not reply time.

## In my own words
My v2 change made no measurable difference, and both prompts matched my labels on the held-out set. Next time I would add a "must be a student" check to my own labeling rule, and pick postings so that both sets include some jobs that should be "relevant".

*(I picked these points from a list of options; Claude turned them into sentences and wrote the factual sections from my results.)*
