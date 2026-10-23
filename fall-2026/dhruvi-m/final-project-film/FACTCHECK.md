# FACTCHECK.md

| # | Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|---|
| 1 | BIDEA | This is Dhruvi Mehta's final project pitch, titled Ghost-Job Trust Radar | PASS | plan/PROJECT-BRIEF.md header | |
| 2 | BIDEA | If something already ran, it is shown; everything else is a plan | PASS | Film's own rule; B06 and B07 are the only REAL beats, see SOURCES.md | |
| 3 | BDEFS | CPT is work authorization tied to a degree program | PASS | Definition in plan/BEAT-PLAN.md; matches the brief's use of CPT | Confirm wording against the school's CPT page before submitting |
| 4 | BDEFS | A ghost job is a posting that's already filled, or never really open | EXEMPT | Working definition used by this project | |
| 5 | BDEFS | Liveness means whether a posting still accepts applications | EXEMPT | Working definition used by this project | |
| 6 | BDEFS | A sponsorship record (shown on screen as "Sponsor record") is a public filing showing a company sponsored a visa before | PASS | plan/PROJECT-BRIEF.md section 2 (MyVisaJobs past H-1B and green-card filings) | |
| 7 | B01 | An international student on CPT can spend an hour researching a posting that turns out filled or misfit | EXEMPT | Illustrative scenario from the brief's section 7; the on-screen "1 hour" is an example, not a measured figure | |
| 8 | B02 | The tool will check liveness, CPT timeline fit, and sponsorship record | PASS | plan/PROJECT-BRIEF.md section 1 | CORRECTED: dropped "public" from the B02 narration |
| 9 | B02 | The finished artifact will be a GitHub repo with one command, tests, and an evaluation log | PASS | plan/PROJECT-BRIEF.md section 1 ("Will exist") | |
| 10 | B03 | MyVisaJobs shows who sponsored before | PASS | plan/PROJECT-BRIEF.md section 2, reviewed 2026-10-10 | Open MyVisaJobs and check one company before filming (FRICTIONAL.md) |
| 11 | B03 | Nothing I saw on MyVisaJobs checks whether a posting is live or fits a CPT window | PASS | plan/PROJECT-BRIEF.md section 2, reviewed 2026-10-10; worded as "nothing I saw" | Same open check |
| 12 | B03 | The manual checklist from career guides is four or five steps across tabs, with no record kept | PASS | plan/PROJECT-BRIEF.md section 2, F1Jobs guide | |
| 13 | B04 | The tool will check liveness first and stop if the posting is dead, before research starts | PASS | plan/PROJECT-BRIEF.md section 2; liveness check is under "Will exist" | CORRECTED to future tense ("Mine will check") |
| 14 | B04 | Every value will carry its source; missing data will read "no record in this dataset" | PASS | Design per brief; build_roles_json.py already labels source on each field and uses NoRecordInSample (break-test-2026-10-10.txt) | CORRECTED to future tense; the full report does not exist yet |
| 15 | B05 | The reader is a hiring manager for a data analyst role | PASS | plan/PROJECT-BRIEF.md section 3 | |
| 16 | B05 | In sixty seconds they will open the README, run one command, and see every line's source | EXEMPT | Planned reader journey, not yet built; the picture is labeled Constructed | |
| 17 | B06 | Last assignment I built a CPT timeline gate and a sponsorship-data builder | PASS | timeline_gate.py and build_roles_json.py in the PR | |
| 18 | B06 | Sixteen offline tests pass | PASS | pantry/evidence/tests-2026-10-10.txt: Ran 6 tests OK + Ran 10 tests OK = 16 | |
| 19 | B06 | I checked one run by hand against the raw data | PASS | plan/PROJECT-BRIEF.md section 4 and "Exists today" | Not re-verified in this session; confirm you still have the notes of that check |
| 20 | B07 | A company not in the dataset was tried | PASS | pantry/evidence/break-test-2026-10-10.txt (Zzyzx Quantum Analytics Corp, absent per grep) | |
| 21 | B07 | The tool reported "no record" instead of inventing an answer | PASS | Same file: tier NoRecordInSample, company_found_in_sample false, funding fields null | |
| 22 | B08 | The project will show verification, source grounding, evaluation, and prompt contracts | PASS | plan/PROJECT-BRIEF.md section 4 | |
| 23 | B08 | A reviewer could conclude I build checks that fail safely, but not that it's accurate on real postings; not yet tested | PASS | plan/PROJECT-BRIEF.md section 4 | |
| 24 | B09 | It won't tell anyone whether to apply and won't give legal or immigration advice | PASS | plan/PROJECT-BRIEF.md section 5 | |
| 25 | B09 | First step: one command runs every check on a synthetic posting, writes a report, a test checks it, a dated run log is committed | PASS | plan/PROJECT-BRIEF.md section 5 ("First") | |
| 26 | B10 | The sponsorship data is an incomplete historical sample | PASS | plan/PROJECT-BRIEF.md section 6; build_roles_json.py docstring says "sample" | |
| 27 | B10 | Every lookup will print the dataset's date range next to the answer | PASS | plan/PROJECT-BRIEF.md section 6 (future) | build_roles_json.py does not print a date range today; narration says "will", which is correct |
| 28 | B11 | Python and data cleaning I already have, with last assignment's scripts as evidence; prompt contracts and evaluation logs are new | PASS | plan/PROJECT-BRIEF.md section 7 | |
| 29 | B12 | Today: a recipe, two scripts, 16 passing tests, and a break test, in an open PR not yet reviewed | PASS | plan/PROJECT-BRIEF.md "Exists today" (PR open, 14 commits, 16 files, checked 2026-10-10) | PR status was last checked 2026-10-10 in the brief; re-check before submitting |
| 30 | B12 | The single command, live check, and evaluation log come later | PASS | plan/PROJECT-BRIEF.md "Will exist" | |
| 31 | B12 | The film does not establish that the tool works on real postings | PASS | plan/PROJECT-BRIEF.md section 4 | |
| 32 | BHTF | Before researching a posting, check whether it is still accepting applications and whether the start date fits your work window, noting where each answer came from | EXEMPT | Advice framed as the viewer's own checks; no figures. Narration reads the composer prompt in full | |
| 33 | BOUT | Title Ghost-Job Trust Radar; narrator Dhruvi Mehta | PASS | plan/PROJECT-BRIEF.md header | |

## Revision 2026-10-22 (after TA feedback)
| # | Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|---|
| R1 | BIDEA | Narrator is an international master's student in Information Systems at Northeastern | PASS | the narrator herself | none |
| R2 | BDEFS | CPT: permission for an international student to work during their degree | PASS (plain-language simplification) | general definition | simplified from "work authorization tied to a degree program" |
| R3 | B03 | On MyVisaJobs, Stripe appears under four company names, and nothing says whether a posting is still open | PASS | evidence/2026-10-22-my-checks/ (Stripe search, 269 results); FRICTIONAL.md 2026-10-22 | none |
| R4 | B03 | Checking one posting by hand took three tabs and about twenty minutes, no record except own screenshots | PASS (self-reported) | FRICTIONAL.md 2026-10-22 manual check | none |
| R5 | B04 | The class engine's live check (npm run ats:liveness) on a real Stripe posting came back active | PASS | the-reallocation-engine PR #57, assignments/submissions/dmehta1310/evidence/2026-10-19/04a-liveness-live.txt | none |
| R6 | B04 | A made-up job number came back 'uncertain', not 'dead' | PASS | same PR, evidence/2026-10-19/04b-liveness-dead-madeup-id.txt | none |
| R7 | B06 | One script pulls sponsorship history from the class data | PASS | build_roles_json.py reads the 80 Days to Stay CSV | none |
| R8 | B09 | The Stripe posting tested asks for six-plus years of experience | PASS | evidence/2026-10-22-my-checks/ (Greenhouse API screenshot) | none |
| R9 | B12 | One live check on a real posting, in an open pull request | PASS if PR #57 is still open on render day | github.com/nikbearbrown/the-reallocation-engine/pull/57 | re-check before submitting |
