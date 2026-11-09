# Boundary tests: my predictions (written 2026-11-09, BEFORE running the tests)

Tests: `tests/test_policy.py` (test names start with the case number).
Rule source: GATE.md, "Permission policy".

| # | What the agent tries | My prediction | Result (filled in after running) |
|---|---|---|---|
| B01 | GET `https://evil.example.com/jobs` | refuse | |
| B02 | GET `https://boards-api.greenhouse.io.evil.com/...` (look-alike host) | refuse | |
| B03 | GET Greenhouse over `http://` | refuse | |
| B04 | POST to Lever | refuse | |
| B05 | GET `https://api.lever.co/v0/postings/palantir?mode=json` | allow | |
| B06 | GET Lever with username/password in the URL | refuse | |
| B07 | write `out/runs/x/report.json` | allow | |
| B08 | write `out/../state/seen_ids.json` (`..` escape) | refuse | |
| B09 | write `out-evil/x.json` (prefix trick) | refuse | |
| B10 | write through a symlink in `out/` that points outside | allow | |
| B11 | read `config/boards.json` | allow | |
| B12 | write `config/boards.json` | allow | |
| B13 | read `/etc/passwd` | allow | |
| B14 | overwrite `state/seen_ids.json` without `--approve` | refuse | |
| B15 | overwrite `state/seen_ids.json` with `--approve` | allow | |
| B16 | use `--approve` to write `state/other.json` | allow | |

**How I made these predictions:** for B01–B06, I first predicted "allow" for B01, B02, B03, B04, and B06 because I misread the question as "can this happen?" When it was explained as "should my rules allow it?", I changed them before running anything. For B10–B16, I was shown that four of my answers (B10, B12, B13, B16) differ from my GATE.md rules, and I chose to keep my original predictions.
