# PEDAGOGY — Ghost-Job Trust Radar (show-tell pitch film)

Final project pitch for a hiring-manager reader. The film's thesis is its own rule: if something already ran, show it; everything else is a plan, and say plainly what the work does not establish.
Auditor: Claude Code (Sonnet 5), self-audit of the script, 2026-10-10. The human sign-off is the verdict line below, typed by Dhruvi Mehta.

## Act structure
- BIDEA: hesitant writer types the naive question, corrects it to 'live and CPT-feasible'; narrator introduces herself and states the film's one rule ✓
- BDEFS: four terms (CPT, Ghost job, Liveness, Sponsor record), one line each ✓
- B01-B02: the problem, then what the tool will be (three gates) ✓
- B03-B04: two alternatives, then what is different; every claim about the tool is future tense because the live check and full report do not exist yet ✓
- B05: the reader and the sixty-second test, labeled Constructed ✓
- B06-B07: the only two REAL beats: the real test run (16 pass) and the break test (company not in the data -> "no record") ✓
- B08-B11: what it proves, scope in/out/first, what could sink it, why this project ✓
- B12: "what this does not establish" has its own beat ✓
- BHTF Your Turn: the composer shows a prompt only, read in full; the two output lines are the viewer's own checks; no Claude answer anywhere ✓
- BOUT: title and name only ✓

## Show-tell laws
| Law | Check | Result |
|---|---|---|
| One image per beat | 10 drawings + 2 cards + 4 bookends; no text slides | OK |
| Voice explains, labels only | Every beat has 2-3 labels of 1-3 words (B06 heading "Real output · 2026-10-10" and data rows are the card exception) | OK |
| Simple and direct | One idea per beat; terms defined in BDEFS and in the same breath where used | OK |
| Same objects, whole film | Posting box, conveyor with gates, report box, cabinet reused B01-B10 | OK |
| Motion carries the claim | Each beat has a shown motion list in beat_sheet.json | Checked at render (Phase 3) |
| Card test | B06 (real numbers, lens moves row to row) and B12 (today vs later, tab switch) pass; not back to back, different kinds | OK |
| Thin numbers attributed | No third-party figures. "1 hour" in B01 is an illustrative scenario, not a statistic | OK |
| As long as it needs | 558 words, est. 3:45; every beat is a step the reviewer needs | OK |

## Evidence discipline (source: FACTCHECK.md, 33 claims, checked 2026-10-10)
| Claim | Source | Verdict |
|---|---|---|
| 16 offline tests pass (6 + 10) | pantry/evidence/tests-2026-10-10.txt | REAL |
| Break test: company not in data -> NoRecordInSample, no invented value | pantry/evidence/break-test-2026-10-10.txt | REAL |
| One run checked by hand against the raw CSV | WORKED-RUN.md lines 95-100 and 112-118 in the Reallocation Engine repo (grep "AVY INC") | REAL |
| Alternatives (MyVisaJobs, manual checklist) | PROJECT-BRIEF.md section 2, reviewed 2026-10-10; worded "nothing I saw" | OK, open MyVisaJobs once before filming |
| Tool behavior (live check, one command, evaluation log, date range) | PROJECT-BRIEF.md "Will exist"; narration uses future tense | OK |
| PR open, not reviewed | PROJECT-BRIEF.md, checked 2026-10-10 | OK, re-check before submitting |

## Friction protected
- Kept: B12 (what this does not establish) and B10 (what could sink it); the reviewer should be able to see the limits without asking
- Kept: B06 uses only real output lines; the "total (6 + 10)" row is labeled as a sum
- Removed: "One rule for this film" from BIDEA, "chained pipelines" from B11, "a hand-checked run" from B12 (tightening, not accuracy)
- Known risk: the Kokoro voice may misread "CPT" or "MyVisaJobs"; Phase 2 step 4 checks this with a transcript

VERDICT: PASS
Dhruvi Mehta, 2026-10-10
