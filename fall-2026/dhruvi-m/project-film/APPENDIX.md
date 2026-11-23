# BEAT-PLAN — Ghost-Job Trust Radar project film (show-tell)

Source for `beat_sheet.json`. Skill: **show-tell** (Brutalist). Voice: `af_bella`. Target: 3:30–4:00. Check the real length after audio.
Four parts, in this order: Executive summary → Introduction → Methods → Evaluation.

Rules for this build:
- No instructor name, persona, voice or outro credit line anywhere (override toolkit defaults).
- Every unbuilt part gets an on-screen **PLANNED** tag.
- Every statistic shows its source as an on-screen caption.
- No "how" in Part 1 (no APIs, scripts, Greenhouse, Claude).

---

## PART 1 — Executive summary (~35 s)

**Beat 1 — Title**
- Visual: Title card "Ghost-Job Trust Radar", subtitle "Dhruvi Mehta · INFO7375 project film".
- Narration: "I'm Dhruvi, an international student at Northeastern, and I'm building the Ghost-Job Trust Radar."

**Beat 2 — Three questions**
- Visual: Three stacked questions appear one at a time: 1) Is this job still real? 2) Does it fit my CPT timeline? 3) Has this company sponsored visas before?
- Narration: "It checks if a job is real, fits my CPT, and if they've sponsored before."

**Beat 3 — Why it matters**
- Visual: A calendar with weeks crossing off while a job card fades out; then "less guessing → right jobs".
- Narration: "Why does that matter? Because our CPT and visa clock keeps running while we chase dead jobs. If it works, there's less guessing, and more applying to the right jobs."

## PART 2 — Introduction (~50 s)

**Beat 4 — The problem is real**
- Visual: Two big numbers. "~70% of companies on Greenhouse posted a ghost job" (caption: Greenhouse internal review, Q2 2024, via Entrepreneur). "40% of companies admitted posting a fake job" (caption: Resume Builder survey, 2024). Use screenshots 01 and 02.
- Narration: "Ghost jobs are a real problem. Almost 70 percent of companies on Greenhouse posted at least one ghost job. And in a 2024 survey, 40 percent of companies admitted posting a fake job."

**Beat 5 — What already exists**
- Visual: Screenshot 03 (GhostJob) with tag "no visa / CPT", screenshot 04 (Subspace) with tag "no sponsorship", screenshot 05 (MyVisaJobs) with the Stripe name list, "Stripe, Llc (219)" highlighted over "Stripe, Inc. (45)".
- Narration: "Some tools already try to catch them. GhostJob gives LinkedIn posts a 0 to 100 trust score, but nothing on visas or CPT. Subspace's scanner checks lots of signals, but nothing about visa sponsorship. And on MyVisaJobs, most of Stripe's filings are under Stripe LLC, 219 of them, not Stripe Inc., which has 45."

**Beat 6 — The gap**
- Visual: The three tools as separate boxes; then one box "Liveness → CPT → Sponsorship" in order, liveness highlighted.
- Narration: "So no one tool answers all three questions. That's the gap, and it's why mine checks liveness first: if the job is gone, nothing else matters."

## PART 3 — Methods (~75 s)

**Beat 7 — Data sources**
- Visual: Three source icons: "Company job board (Greenhouse public API)", "MyVisaJobs", "My program dates".
- Narration: "Here's the plan. The data comes from public places: a company's job board through Greenhouse's public API, MyVisaJobs for sponsorship history, and my program dates for the CPT check."

**Beat 8 — Pipeline overview**
- Visual: Five-step pipeline diagram: Watch → Liveness gate → CPT check → Sponsorship lookup → Two judges. Each step tagged BUILT or PLANNED as below.
- Narration: "There are five steps."

**Beat 9 — Steps 1–2**
- Visual: Step 1 tagged BUILT; counter "Oct 27: 714 postings → Oct 28: 720 postings, 16 new" (source: evidence/reports/ in JS1 folder). Step 2 tagged BUILT, with a "fix PLANNED" note.
- Narration: "Step one is the watch. The agent fetches one board, saves the raw response, and remembers which postings it's seen. That's built. I ran it on Stripe's board on October 27 and 28: the first run saw 714 postings, and the second saw 720, with 16 new ones. Step two is the liveness gate: before anything else, confirm the posting still exists."

**Beat 10 — Steps 3–5**
- Visual: Step 3 tagged BUILT ("6 passing tests"). Step 4 tagged BUILT ("10 passing tests"), with "name-variant matching PLANNED". Step 5 tagged BUILT (rule + Claude + validator). Small note: "JS2: loop with budgets + permission gate — BUILT".
- Narration: "Step three is the CPT check, which compares the job's start date and length against my program window. That's built, with 6 passing tests. Step four is the sponsorship lookup, built with 10 more. Step five is two judges: my hand-checkable rule, and Claude in a fixed format checked by a validator. Those came from my first agent assignment, and the second one added a loop with budgets and a permission gate."

**Beat 11 — Still planned + resources**
- Visual: PLANNED list: 404 → dead; company name variants; one combined run. Then a checklist: Claude Pro + Claude Code ✓, GitHub ✓, public APIs (no key) ✓, laptop / Python 3.12 ✓.
- Narration: "Still planned: making a 404 come back as dead, matching company name variants, and joining the steps into one run. And I have what I need: Claude Pro with Claude Code, GitHub, public data that needs no key, and my laptop running Python 3.12 with no extra packages."

## PART 4 — Evaluation (~50 s)

**Beat 12 — Liveness test**
- Visual: Two columns: "10 known-gone (404)" / "10 known-open". Pass line: "all 10 gone → dead". Current result: "Stripe 404 → uncertain ✗".
- Narration: "I'll check three things. Liveness: I'll run 10 postings I know are gone, because they return a 404, and 10 I know are open. It works if all 10 gone ones come back dead. Right now, a Stripe job link that returns a 404 still comes back uncertain, not dead, so that's the first test that has to pass."

**Beat 13 — Sponsorship + judging tests**
- Visual: "Stripe: 4 name variants → find all 4". Then "Held-out: mix of relevant + not relevant · agree ≥ 9 of 10" and "same answer across repeated runs".
- Narration: "Sponsorship: Stripe appears in MyVisaJobs under four different company names. It works if the lookup finds all four, not just one. Judging: I'll hold out 10 postings with both relevant and not relevant ones. It works if the agent agrees with me on at least 9 of them, and Claude gives the same answer across repeated runs."

**Beat 14 — What this does not establish**
- Visual: Plain card, two lines: "Not advice on whether to apply." "Not a promise of sponsorship — only past history."
- Narration: "If something fails, I'll report it as a failure. And what this doesn't establish: it doesn't tell anyone whether to apply, and it doesn't promise a company will sponsor them. It only shows whether it has before."

**Beat 15 — Close**
- Visual: Recap of the four parts on one card; GitHub folder path; "Appendix: pipeline steps, commits, screenshots, Claude vs. me table".
- Narration: "That's the Radar: what I'm building, what's out there, how I'll build it, and how I'll know it worked."

---

## Appendix (submit with the film, not in it)
- Step-by-step pipeline detail and commands
- Links to JS1 and JS2 folders + commit hashes
- Screenshots I took: Greenhouse board JSON, MyVisaJobs Stripe lookup, Entrepreneur and Resume Builder articles, GhostJob and Subspace extension pages
- Test list (16 CPT/sponsorship tests, JS1/JS2 tests)
- Table: what Claude did vs. what I did

### My research notes (Nov 21, 2026 — I opened each source and took the screenshot)
| # | Source | Screenshot | What I noticed |
|---|---|---|---|
| 1 | Entrepreneur (Greenhouse internal review) | 01-entrepreneur.png | Almost 70% of companies on Greenhouse posted at least one ghost job |
| 2 | Resume Builder survey | 02-resumebuilder.png | 40% of companies admitted posting a fake job (2024 survey) |
| 3 | GhostJob extension (Chrome) | 03-ghostjob-extension.png | It gives LinkedIn posts a 0–100 trust score, but nothing on visas or CPT |
| 4 | Subspace Ghost Job Scanner (Firefox) | 04-subspace-scanner.png | It checks lots of signals, but nothing about visa sponsorship |
| 5 | MyVisaJobs — Stripe | 05-myvisajobs-stripe.png | Most filings are under "Stripe, Llc" (219), not "Stripe, Inc." (45); 4 names total |

### My pass marks and why
| Check | Pass mark | Why |
|---|---|---|
| Liveness | All 10 known-gone postings return "dead" (10/10) | A 404 is a clear yes/no, so there's no excuse to miss one |
| Sponsorship | Lookup finds all 4 Stripe names | Missing a name means telling a student "never sponsored" when they have |
| Judging | Agrees with my labels on 9+ of 10 held-out | 10 is a small set, so 1 miss is the most I can accept |

### What Claude did vs. what I did
| Part | Claude | Me |
|---|---|---|
| Structure / beat plan | Drafted the four-part beat plan and visuals | Reviewed and approved it |
| Executive summary | Offered wording options, added connecting phrases | Chose the wording |
| Introduction | Suggested sources to check | Opened all 5 sources, took screenshots, chose each note |
| Evaluation | Offered pass-mark options | Chose the pass marks and the reasons |
| Build | Claude Code rendered the film | Ran the build, reviewed narration at GATE P, checked frames with ffmpeg |

### Notes
- FRICTIONAL.md: Claude offered options; I chose them and added my own words.
- Watch runs: 714 + 16 new ≠ 720, so 10 postings from run 1 were no longer listed in run 2.
