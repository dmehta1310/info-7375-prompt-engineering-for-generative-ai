# GATE.md: exits, budgets, and policy (written before any code)
Author: Dhruvi Mehta · Date: 2026-11-09 · Persona: Priya Nair (fictional)

## Boards
| Board | System | Endpoint | Expected |
|---|---|---|---|
| stripe | Greenhouse | boards-api.greenhouse.io/v1/boards/stripe/jobs | jobs |
| palantir | Lever | api.lever.co/v0/postings/palantir?mode=json | jobs |
| linear | Ashby | api.ashbyhq.com/posting-api/job-board/linear | jobs |
| this-board-does-not-exist-js2 | Greenhouse | boards-api.greenhouse.io/v1/boards/this-board-does-not-exist-js2/jobs | **fails on purpose (404)** |

I opened all four in my browser on 2026-11-09 (screenshots in `evidence/browser_checks/`).

## Exits: every way a run can end
A loop that stops is not a loop that succeeded. Every run ends with exactly one status:
| Status | When | What the report must show |
|---|---|---|
| `finished` | Every board was attempted **and** every board returned a valid, non-suspicious response | per-board job counts, new IDs, requests used, seconds |
| `incomplete` | All boards were attempted, but at least one failed **or** was suspicious (see "empty board" below) | which boards failed and why; no invented values for them |
| `budget-exhausted` | A budget ran out before every board was attempted | which boards were never attempted |
| `error` | Something unexpected: bad config, a crash, or an action the permission policy refused | the error message; no partial results reported as success |

**Empty board rule:** a board that answers 200 with **0 jobs**, when it had jobs on the last run, is **suspicious, not "no new jobs."** It makes the run `incomplete`.

## Budgets (per run)
- Max **5 boards**, max **10 HTTP requests** (retries count), max **60 seconds**.
- I asked Claude to choose these numbers, and I accepted them.
- A budget changes **only** through a new dated entry in this file, written by me. The code reads the budget from config and never raises it itself.

## Repeat rule
- "The same action" = the same **method + full URL** in the same run.
- A second identical request is **refused** and recorded as `repeat-blocked`.
- The **only** allowed repeat is one retry under the error policy below.

## Error policy (per board)
- **404 / not found:** no retry. The board does not exist, so asking again cannot help. Mark the board `failed: not-found`, move on.
- **Timeout or 5xx server error:** retry **once** (these can be temporary), then mark `failed` and move on.
- **Any other error** (bad JSON, unexpected shape): no retry; mark `failed: bad-response`.
- A failed board **never** gets an invented value (no "0 jobs", no "no new jobs"). After the run, I review failed boards myself (escalation = they are listed in the report for me).

## Permission policy (enforced in code, not in a prompt)
- **Hosts allowed:** exactly `boards-api.greenhouse.io`, `api.lever.co`, `api.ashbyhq.com` (exact match; HTTPS only). Anything else is refused.
- **Method:** GET only. No POST/PUT/DELETE.
- **Writes:** only inside `out/`. The real path (after resolving `..` and symlinks) must be inside `out/`. Look-alike folders such as `out-evil/` are refused.
- **Reads:** allowed in `out/` and `config/` only.
- **Needs my approval:** overwriting `state/seen_ids.json`. The agent writes a proposal to `out/`; the state file changes only when I run the command with `--approve`.
- **Never:** apply to jobs, email, message anyone, log in, or use credentials.

## Wrong versions my tests must catch
1. An empty 200 response reported as `finished` / "no new jobs."
2. A failed board counted as a success (so the run says `finished`).
3. A path check using "starts with" text, which lets `out-evil/` pass for `out/`.
4. A path check that does not resolve symlinks, so a link inside `out/` can point outside it.
5. A host check using "contains," which lets `boards-api.greenhouse.io.evil.com` pass.
6. Retrying a 404, or retries not counted against the request budget.
7. The state file overwritten without `--approve`.

*(Decisions are mine: the boards, the error policy, the approval rule, and accepting the budget Claude proposed. Claude turned my picks into these sentences.)*
