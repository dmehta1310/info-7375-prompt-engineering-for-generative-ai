# Job-Search Agent 1: The Contract and the Watch

Watches Stripe's public Greenhouse board for **new** postings and judges each one for **Priya Nair**, a fictional persona (`persona/priya_nair.json`, @example.com, 555 phone).
Every new posting gets two verdicts:
- a **record** from my written rule (`CONTRACT.md`), which anyone can recompute, and
- a **judgment** from Claude under a prompt contract (`prompts/judge_v1.txt`), which must pass `agent/validate.py`.

## How to run
- `python3 agent/watch.py` fetches the live board, diffs it against `state/seen_ids.json`, and writes a report
- `python3 agent/watch.py --from-file FILE` runs from a saved response (labeled SEEDED)
- `python3 -m unittest discover -s tests -b` runs the 15 tests
- `python3 agent/validate.py FILE --id ID` checks one Claude reply

## Where things are
| What | File(s) |
|---|---|
| Contract (written before code) | `CONTRACT.md` (commit 5da420b) |
| Watch: baseline + real 2nd-day run | `evidence/reports/` (run 1: 714 postings, 0 new; run 2 on 2026-10-28: 720 postings, 16 new), `evidence/raw/`, `state/seen_ids.json` |
| Tests | `tests/test_agent.py`, `tests/test_validator.py`, `tests/hand_checks.json` |
| Sampling report | `SAMPLING_REPORT.md` |
| Prompt experiment | `EXPERIMENT_REPORT.md`, `LABELING_RULE.md`, `experiment/` |
| Action-surface comparison | `ACTION_SURFACE.md` |
| My friction log | `FRICTIONAL.md` |
| Sources / help used | `SOURCES.md` |

## Sign-off

**Checked, and how**
- The rule gives the verdicts I computed by hand on 3 postings → `tests/hand_checks.json`, test `test_wrong_version_1_pairing`.
- The fetcher refuses hosts outside the allow-list → `test_allow_list_blocks_other_hosts`.
- A real baseline and a real second-day run (not seeded) → `evidence/reports/` (commits c467916, 3c78e13).
- Claude's replies follow the fixed format → validator plus 6 tests; all 20 sampling replies and all 30 experiment replies were VALID.
- Claude's sampled verdicts vs. my hand labels → 20/20 agree (`SAMPLING_REPORT.md`). My rule agreed 4/5.
- v1 vs v2 on held-out postings that I labeled before any Claude run → both 10/10 (`EXPERIMENT_REPORT.md`).
- 15 tests pass (`python3 -m unittest discover -s tests -b`).

**Not checked**
1. **Which Claude model answered.** I took no screenshots of the sampling and experiment chats, so I can't prove which model or settings were used.
2. **Prompt injection and a corrupted state file.** Posting text is untrusted and could contain instructions aimed at Claude; I never tested this. I also never tested what happens if `state/seen_ids.json` is damaged.
3. **Years of experience.** My rule never checks them, which is why it wrongly marked 8026689 (5–10 years) as relevant. There is no test for this gap.

**Not claiming**
- That Claude's verdicts are **correct**. They were consistent (same verdict 4/4 on every sampled posting), but consistency is not correctness, and my labels cover only 25 postings.
- That **v2 is better than v1**. They tied 10/10 on held-out, and the held-out set had no "relevant" postings.

**Signed:** Dhruvi Mehta, 2026-10-28

## Driver's seat: what Claude did vs. what stayed mine
| Part | Claude | Me | Proof |
|---|---|---|---|
| CONTRACT.md (rule, wrong versions, failure sentence) | Asked questions, pressure-tested | Wrote it, before any code | commit 5da420b (before any `agent/` code in c467916) |
| Persona | Suggested the fields | Changed target titles; decided "Remote-Canada" counts as US | `persona/priya_nair.json` history; `FRICTIONAL.md` |
| All code (`agent/`, `tests/`) | Wrote it | Ran every command and test myself | commits c467916, 4ce1b40, 7db91b4 |
| Hand labels (3 + 5 + 20) | Printed the requirement text | Read each posting and chose every label | `tests/hand_checks.json`, `labels/`, `experiment/labels.json` |
| Labeling rule | Turned my picks into sentences | Picked the thresholds (≤2 years, US only) and the v2 title change | `LABELING_RULE.md` (ca38de4, 07577f0) |
| v2 prompt change | Wrote the sentence | Chose what to change | commit d711cfe |
| Claude-judge runs | Was the judge | Ran every chat in incognito and saved each reply | `responses/log.csv`, `experiment/log.csv` |
| Least-autonomy choice | Listed the options | Chose option 3 | `ACTION_SURFACE.md` |
| Reports | Drafted the factual sections from my results | Picked the conclusions and reflections; checked the facts | `SAMPLING_REPORT.md`, `EXPERIMENT_REPORT.md` |
