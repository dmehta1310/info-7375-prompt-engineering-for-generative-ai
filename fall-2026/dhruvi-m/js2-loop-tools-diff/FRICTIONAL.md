# FRICTIONAL: my honest log (JS2)

## 2026-11-09: My predictions were wrong on 4 boundary cases
- **What happened:** before running the boundary tests, I predicted the agent would *allow* B10 (a symlink in `out/` pointing outside), B12 (writing `config/boards.json`), B13 (reading `/etc/passwd`), and B16 (using `--approve` on a different file). Claude pointed out that these go against my own GATE.md rules, and I chose to keep my predictions anyway. When I ran the tests, the agent **refused all four**, which is what my written policy says.
- **What I learned:** I wrote the rules, but I didn't apply them carefully when predicting. The code followed the policy more strictly than my guesses did. At first I also misread the question for B01–B06 ("can this happen?" instead of "should my rules allow it?") and changed those answers before running anything.
- **Traceability:** predictions in commit ab832d1; results in f05890c (`evidence/test_run_1.txt`).

## 2026-11-09: Claude Code did not run the tests, so I did
- **What happened:** I asked Claude Code to fix the timeout defect, letting it read and edit files only. Its reply said it had changed `agent/loop.py` but **had not run any tests**. I did not take its word: I ran the new test (failed before, passed after) and the full suite (28 OK), and checked with `git status` that only `agent/loop.py` changed.
- **Accepted / modified / rejected:** I **accepted** Claude Code's fix unchanged. I also **accepted** Claude's proposed budget, and I **kept** my own boundary predictions rather than changing them to match Claude's explanation.
- **Still unresolved:** the timeout does not limit total download time (REVIEW_PACKET.md §8).
- **Traceability:** test-first commit 7b921d3; fix + decision e5a3fef; evidence in `evidence/review/`.

## 2026-11-09: My screenshot copy grabbed the wrong (old) screenshots
- **What happened:** my command copied the 4 newest screenshots from my Desktop into `evidence/browser_checks/`, but they were old ones from Oct 24–28, not my browser checks from today. Claude pointed out the dates in the file names; I confirmed they were coursework/terminal screens, not private, and removed them. Then my Mac would not let Terminal take new screenshots, so I used the agent's saved raw responses as my evidence and corrected the line in GATE.md.
- **Accepted / changed:** I accepted Claude's suggestion to drop screenshots and rely on the raw responses.
- **Traceability:** commit "remove wrongly copied old screenshots" (77c120c); GATE correction in ab832d1.

## 2026-11-09: I thought JS2 was finished, but my JS1 feedback showed a gap
- **What happened:** after my first "done," I gave Claude my JS1 feedback list. Checking against it showed that JS2 had **no years-of-experience check**, the exact thing that made my JS1 rule wrongly mark posting 8026689 (5–10 years) as relevant. I wrote a dated GATE decision first, then added the rule with the years check.
- **Before → after, on the real JS1 posting:** `test_Y1_js1_bug_8026689_now_not_relevant` shows the JS1 version says *relevant* and the JS2 rule says *not relevant*. I also fixed my JS1 gap where "United States" was not on the US list (`test_L1`).
- **Accepted / changed:** I accepted Claude's rule code. The decision to add the years check, and that "no years stated" passes, came from my JS1 labeling rule.
- **Traceability:** GATE decision (46d8ddf), rule + tests (411323b), `evidence/test_run_rule.txt` (35 OK).

## 2026-11-09: Second live run — new jobs, but still no relevant one
- **What happened:** run 2 (`out/runs/2026-11-09T220326Z_LIVE/`) found **2 new Stripe jobs** since my approved run, and **0 relevant by the rule** on all three boards. The independent check passed.
- **Unresolved:** I still have not seen a real posting that my rule marks relevant. The "relevant" outcome is only shown by a constructed test job (`test_Y2`), so I can't yet say how the rule does on real relevant postings.
- **Traceability:** 45e8c37.

## 2026-11-09: I never chose Claude Code's model
- **What happened:** I ran Claude Code without `--model`. Its own session log shows the edit to `agent/loop.py` was made by **claude-sonnet-5-5** (2026-11-09 20:37 UTC). I only found this by reading the log afterwards (`evidence/review/5_claude_code_model.txt`).
- **What I'd change:** next time I'll pin the model with `--model` and record it before the run, not after.
