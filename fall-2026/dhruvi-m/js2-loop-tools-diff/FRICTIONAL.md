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
