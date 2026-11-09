# Review packet: one change made by Claude Code (2026-11-09)

## 1. The defect
GATE.md says a run may take at most 60 seconds. But `agent/loop.py` gave **every** request a fixed 15-second timeout, however much of the budget was left. So with 55 seconds used, the agent could still start a request that waits 15 more, and the run would last **70 seconds**, over budget.

## 2. Reproduced first, with a test written before the patch
- Test: `tests/test_review_timeout.py::test_R1_request_timeout_never_exceeds_time_left`. A fake network makes each request "take" 55 s; after the first board, only 5 s are left, so the second request's timeout must be ≤ 5 s.
- Ran **before** the fix → **FAILED**: `AssertionError: 15 not less than or equal to 5` (`evidence/review/1_before_fix.txt`).
- Committed **before** asking Claude Code: commit **7b921d3**.

## 3. What I asked Claude Code (Claude Code 2.1.303, 2026-11-09 15:37 EST)
- Exact prompt: `evidence/review/0_prompt_to_claude_code.txt`. Fix only this defect, **only edit `agent/loop.py`**, do not edit tests.
- It was allowed to **read and edit files only** (`--allowedTools "Read,Edit"`), not to run commands.
- Its full reply: `evidence/review/2_claude_code_output.txt`. It said itself that it **had not run any tests**.

## 4. The diff, read as a change in behavior (`evidence/review/3_diff.patch`)
- **Before:** every request (including retries) could wait 15 s.
- **After:** before every request and every retry, the loop computes `time_left = max_seconds - elapsed`.
  - If **less than 1 s** is left, the request is **not sent**; the run stops with `budget_hit = "max_seconds"`, so it ends as `budget-exhausted`, and that board is listed as never attempted.
  - Otherwise the timeout is **`min(15, time_left)`**, so no request can wait past the budget.
- Nothing else changed: no new exits, no change to retries, the repeat rule, or the policy.

## 5. Did it stay in scope?
**Yes.** `git status` showed only `agent/loop.py` modified: 6 lines (4 added, 1 changed). No test or other file was touched.

## 6. Commands I ran myself
- `python3 -m unittest tests.test_review_timeout -v` → FAILED before the fix
- `git status --short` and `git diff` → checked scope and read the change
- `python3 -m unittest discover -s tests -v` → **28 tests, all OK** after the fix (`evidence/review/4_after_fix_all_tests.txt`)

## 7. My decision: ACCEPT
Evidence: the test failed before and passes after; all 28 tests pass, so the 27 earlier ones still hold; the change stayed in `agent/loop.py` and matched what I asked for.

## 8. One case my test would still miss
Python's `urllib` timeout limits **each wait for data**, not the **total** download time. A server that sends a big response very slowly, a little at a time, could keep every single wait under 5 s and still take longer overall, pushing the run past 60 s. My test uses a fake network, so it cannot show this. It also does not count time spent *after* the last request (parsing and saving files).
