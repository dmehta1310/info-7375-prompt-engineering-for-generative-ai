# Boundary tests: my predictions (written 2026-11-09, BEFORE running the tests)

Tests: `tests/test_policy.py` (test names start with the case number).
Rule source: GATE.md, "Permission policy".

| # | What the agent tries | My prediction | Result (filled in after running) |
|---|---|---|---|
| B01 | GET `https://evil.example.com/jobs` | refuse | refused ✅ |
| B02 | GET `https://boards-api.greenhouse.io.evil.com/...` (look-alike host) | refuse | refused ✅ |
| B03 | GET Greenhouse over `http://` | refuse | refused ✅ |
| B04 | POST to Lever | refuse | refused ✅ |
| B05 | GET `https://api.lever.co/v0/postings/palantir?mode=json` | allow | allowed ✅ |
| B06 | GET Lever with username/password in the URL | refuse | refused ✅ |
| B07 | write `out/runs/x/report.json` | allow | allowed ✅ |
| B08 | write `out/../state/seen_ids.json` (`..` escape) | refuse | refused ✅ |
| B09 | write `out-evil/x.json` (prefix trick) | refuse | refused ✅ |
| B10 | write through a symlink in `out/` that points outside | allow | refused ❌ (I predicted allow) |
| B11 | read `config/boards.json` | allow | allowed ✅ |
| B12 | write `config/boards.json` | allow | refused ❌ (I predicted allow) |
| B13 | read `/etc/passwd` | allow | refused ❌ (I predicted allow) |
| B14 | overwrite `state/seen_ids.json` without `--approve` | refuse | refused ✅ |
| B15 | overwrite `state/seen_ids.json` with `--approve` | allow | allowed ✅ |
| B16 | use `--approve` to write `state/other.json` | allow | refused ❌ (I predicted allow) |

**How I made these predictions:** for B01–B06, I first predicted "allow" for B01, B02, B03, B04, and B06 because I misread the question as "can this happen?" When it was explained as "should my rules allow it?", I changed them before running anything. For B10–B16, I was shown that four of my answers (B10, B12, B13, B16) differ from my GATE.md rules, and I chose to keep my original predictions.

## Results (run 2026-11-09, `evidence/test_run_1.txt`: 27 tests, all OK)
- The agent did what GATE.md says on all 16 cases.
- My predictions matched on **12 of 16**. On **B10, B12, B13, B16** I predicted "allow," but the agent refused, which is what my own written policy requires. My predictions were wrong; the code followed the policy.
- Claude wrote these tests and ran them in its own sandbox while writing the code. My run above was the first run on my machine, after my predictions were committed (commit ab832d1).
