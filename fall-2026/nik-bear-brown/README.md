# nik-bear-brown

A place for the public work of Nik Bear Brown's examples — INFO 7375, Fall 2026.

## Executive summary

**What this is.** Professor Bear's worked examples, and a step-by-step **recipe for finding a "dream job"**: here, Designer Advocate or education-advocate work, ideally on flexible terms (summer, contract, part-time), such as running or developing workshops for universities.

**Why read it.** The recipe is the Reallocation Engine's method applied to one real search.
- **Record first:** check the job board and the CV as records before anyone forms an opinion.
- **Gates are human:** a person makes every decision.
- **The payoff is time:** it spends the search on networking and building, not on applying all day.

It also lines up with Assignment 2 ("Plan Your Madison Project Like a Pro"): each step says which part of that assignment it feeds.

**Where it stands.**
- **Step 1 is done for Figma:** 2 Designer Advocate roles, both full-time, none on flexible terms.
- **Step 2 has a first gap table:** the CV shows strong teaching and program-building, but never mentions Figma, design systems, certification programs, or conference talks.
- **Steps 3–8 are planned.**

| Folder or file | What it is |
|---|---|
| [`figma/`](figma/) | Figma's open jobs saved by date, the scan, the two relevant postings, and the Figma-only recipe |
| [`greenhouse-watch-demo/`](greenhouse-watch-demo/) | The Reallocation Engine's job-board watcher run on Figma with Professor Bear's CV: what's new, what matches, and what the rules miss |
| [`facts/`](facts/) | Professor Bear's CV as structured JSON, personal information removed, checked by him on 2026-09-23 |
| [`FRICTIONAL.md`](FRICTIONAL.md) | The process log: what was tried, what went wrong, who did what, and every push |
| [`CLAUDE.md`](CLAUDE.md) | Rules Claude Code follows in this folder |

---

## Recipe: find a dream job (advocate and education work)

```yaml
status: DRAFT          # step 1 runs for one company; steps 3–8 not built
todos_open: 7
last_gate: null
attestation: null
recipe_version: 0.1.0
```

**The rule for every step:** every value is labeled.
- **Record:** it came from a saved file or the CV facts.
- **Judgment:** a person or Claude read the records and decided something.
- **Your input:** something only Professor Bear knows or decides.

Nothing is invented. Anything not built yet is a typed TODO.

### Step 0 — The CV as facts  ✅ done

- **Input:** the CV.
- **Output:** [`facts/professor-bear-cv.json`](facts/professor-bear-cv.json), with personal information removed and `attested: true` (checked by Professor Bear, 2026-09-23).
- **Why first:** the gap analysis in step 2 compares job requirements against *this file*, not against memory.

### Step 1 — Watch one company: Figma  ✅ done for 2026-09-23 · feeds **Assignment 2, Part 1** (the dream job)

1. **Save the day's board** as readable JSON: [`figma/figma-jobs-2026-09-23.json`](figma/figma-jobs-2026-09-23.json) (160 postings).
2. **Scan it** with [`figma/find_roles.py`](figma/find_roles.py) for three things: role words in titles (advocate, educator, enablement…), topic words in the text (university, workshop, educate…), and flexible-terms words (part-time, contract, summer…). The report is [`figma/roles-2026-09-23.md`](figma/roles-2026-09-23.md).
3. **Keep the relevant postings** with [`figma/pick_postings.py`](figma/pick_postings.py) → [`figma/professor-bear-figma.json`](figma/professor-bear-figma.json) and [`.md`](figma/professor-bear-figma.md).

**What it found (record):**
- **Advocate roles:** 2 Designer Advocate roles. The main one states it is **full time** from a US hub, with travel up to 25%. Both list $153,000–$317,000.
- **Universities:** no posting mentions universities or campuses.
- **Flexible terms:** no posting offers part-time, contract, or temporary terms.

**For Assignment 2, Part 1: one real posting.**
- **Suggested pick (judgment):** *Designer Advocate, Partnerships* at Figma ([posting](https://boards.greenhouse.io/figma/jobs/6114301004?gh_jid=6114301004)). It is the only role that builds **certification and enablement programs** and represents Figma **at workshops**, so it's the closest to teaching.
- **Its top 3 technical requirements (record, quoted from the posting):**
  1. "Demonstrate deep, hands-on expertise in Figma, with experience embedding the platform within product teams"
  2. "building, managing, and leveraging design systems, design tokens, and AI-assisted design or prototyping while partnering closely with engineers"
  3. "Translate technical design decisions into practical development outcomes"
- **Why this role (your input):** `[TODO: DEFINE]` one sentence, in Professor Bear's words.
- **Excellence: the hiring manager and team (your input, by hand):** research on LinkedIn. Keep names and notes **out of this public repo**; they go on the Figma board only. The job data lists its department as Marketing (record).

### Step 2 — Gap analysis against the CV  🟡 first pass · feeds **Assignment 2, Part 2**

**How to read the columns:**
- **They want:** quoted from the posting (record).
- **I have:** quoted from `facts/professor-bear-cv.json` (record); "not in the CV" means a word search of the facts file found nothing.
- **Gap to fill** and **Madison could help by:** judgments and proposals. Professor Bear confirms or rewrites them.

| They want (Designer Advocate, Partnerships) | I have (CV facts) | Gap to fill (judgment) | Madison could help by… (proposal) |
|---|---|---|---|
| "deep, hands-on expertise in Figma" | Not in the CV (the word *Figma* never appears) | Public, visible Figma work | Building the Madison project's own board and design in Figma, and publishing it as a worked example |
| "design systems, design tokens, and AI-assisted design or prototyping" | Not in the CV. Closest: MS, Information Design and Visualization | A design-system or AI-prototyping artifact to show | An agent that audits a design file against a small design system, as the Week 3 build |
| "Build, evolve, and deliver certification programs, and scalable enablement programs" for partners | "Co-developed and filmed INFO 6205… full Coursera platform course (13 modules)"; "ENGR 0201… 700+ learners"; "Designed and deployed 25+ AI-powered course assistants" | Mostly a **strength**. The gap is the word: none of it is framed as *certification* or *partner enablement* | A Madison agent that turns one Figma workflow into a short certification module (lesson, quiz, rubric) |
| "delivering compelling presentations and effectively engaging audiences of all sizes" | Workshops (Institute for Experiential AI); a 700+ learner course; conference *papers* (ICLR, BMVC) | No **talks** or community events are listed in the CV | A content-planning agent that turns each course film into a meetup-talk outline |
| "travel of up to 25%" and full-time terms | "Associate Teaching Professor," 2022–present (the CV doesn't state hours) | **Terms, not skills**: this is the flexible-work gap | Nothing to build. This is a networking question (step 6) |

`[TODO: DEFINE]` Professor Bear to confirm the gaps, and to add anything the CV leaves out. For example, the original CV names a YouTube channel that the facts file does not carry.

### Step 3 — Find similar roles at other companies  ⬜ planned

- Run the same scan on other design and creative-tool companies. The Reallocation Engine's `greenhouse-watch` skill reads **Greenhouse, Ashby, and SmartRecruiters** boards, and has already been run on Canva, Miro, Webflow, Notion, Writer, and Jasper (its run log, 2026-09-19).
- **Output:** one folder per company, shaped like `figma/`: dated JSON, a scan report, and kept postings.
- `[TODO: DEV]` Make `find_roles.py` take any saved board, not only Figma's file layout, and check that the Ashby and SmartRecruiters formats scan the same way.

### Step 4 — Gaps across roles, not just one  ⬜ planned

- Pool the requirement lines from every kept posting, and count how often each requirement shows up (record: a count).
- The gaps that recur across companies come first. A gap that appears once is one employer's taste.
- `[TODO: DEV]` A small script that reads every `*-figma.json`-style kept file and prints the requirement counts next to the CV matches.

### Step 5 — Close the top gaps with credibility work  ⬜ planned · the "3 hours building" of the 3-3-2 day

- Build one public artifact per top gap. Start with the Madison project from Assignment 2: Figma-native, AI-assisted, documented, including what it can't do.
- Log each one in `FRICTIONAL.md` as it ships.

### Step 6 — Network where the terms aren't posted  ⬜ planned · the "3 hours networking"

- Figma's board shows the team (its Advocacy team, named in the Designer Advocate posting) but not flexible terms. A conversation is the route, not an application.
- `[TODO: DEFINE]` who to contact and how, done by hand. Names and notes stay private, never in this repo.

### Step 7 — Apply only when the terms fit  ⬜ planned · the "2 hours applying"

- **Apply** when a kept posting's stated terms fit (for example summer, contract, or part-time). Otherwise **network** or **skip**. Only Professor Bear clears this gate.
- `[TODO: DEV]` A day-over-day diff, so a new advocate or flexible posting stands out the day it appears.

### Step 8 — Log every run  ♻️ ongoing

- Each substantive change goes in [`FRICTIONAL.md`](FRICTIONAL.md), per [`CLAUDE.md`](CLAUDE.md).

---

## Assignment 2 ("Plan Your Madison Project Like a Pro"): what this recipe gives you

The assignment lives on a **Figma board**. This folder supplies checked material for it; the board, the writing, and the choices are Professor Bear's.

| Assignment part | From this recipe | Still his to do |
|---|---|---|
| **1. Dream job (10)** | Step 1: the posting, link, and top 3 requirements, quoted | The "why this role" sentence; the hiring-manager research (excellence) |
| **2. Gap analysis (20)** | Step 2: 5 rows, requirements quoted, CV evidence quoted | Confirm the gaps. Excellence needs research into Figma's actual stack and tools beyond the posting, with sources |
| **3. PRD (40)** | The problem, from the posting: Figma needs "scalable enablement programs" for service and distribution partners. The users: partners and their customers. | Write the PRD, and find real industry metrics with sources. Don't invent numbers. |
| **4. Technical architecture (30)** | A proposal to adapt (below) | Choose, research the n8n nodes, draw the diagram |

**A starting proposal for Part 4 (judgment; adapt or replace):**

- **Agent 1, Board Watcher:** fetches one company's public job board daily and saves it as readable JSON (step 1.1).
- **Agent 2, Role Scout:** scans the saved board for role, topic, and flexible-terms words, and keeps the relevant postings (steps 1.2–1.3).
- **Agent 3, Gap Analyst:** compares kept postings' requirements against the CV facts and drafts the gap table, with every row labeled record or judgment (step 2).
- **How they talk:** each hands the next a JSON file. The formats already exist: `figma-jobs-*.json` → `professor-bear-figma.json` → a gap table. Those are the "data schema between agents" the excellence points ask for.
- **n8n MVP (one workflow):** Schedule Trigger → HTTP Request (the Greenhouse boards API) → Code (the scan) → IF (anything new and relevant?) → a notification or a sheet row. `[TODO: DEFINE]` Confirm each node against n8n's own documentation before it goes on the board.
- **Won't build in Week 3:** multi-company sweeps, automatic applying, or anything that contacts people.
