# FILTER.md: what reaches me, and why (written before any code)
Author: Dhruvi Mehta · Persona: Priya Nair (fictional; data analyst, 2 years of experience, US-based)
Started from: my Job-Search Agent 2 (`../js2-loop-tools-diff/`) and its saved raw responses from 2026-11-09 (Stripe/Greenhouse, Palantir/Lever, Linear/Ashby).

## Version history
| Version | Date | Change | Why |
|---|---|---|---|
| v1 | 2026-11-20 | Title words + US location only | Start simple, so every later rule is added as one measured change |

*(Later versions are added here only after measuring, with the result. Rules I try and reject are recorded too.)*

## v1 rules: a posting is **relevant** only if both pass
| # | Rule | Reason |
|---|---|---|
| R1 | **Title** contains one of: *Analyst*, *Data Scientist*, *Data Science*, *Analytics*, matched as **whole words, ignoring case** | The title is the posting's own summary of the job. I accept **any analyst title** (not only "Data Analyst"), because analyst roles in other areas can still use Priya's data skills; the audit will show which of them are false friends. Whole words so a target word can't match inside another word; ignoring case so "data analyst" still counts. |
| R2 | **Location** is in the US: any part of the location field is a US place (a US city or state, "United States", "US", "USA", or "Remote" that names the US) | Priya is US-based. For a multi-city posting, one US city is enough, because she could take that office. |

**Deliberately not in v1:** years of experience (in my JS2 rule) and 3+ skills. I'll add them one at a time later and measure each change on held-out labels (Chapter 9), instead of assuming they help.

## Evidence rules: labeling each claim in a shortlist justification
Each claim is checked **only against the posting's own text** (title, location, description), never against outside knowledge.
- **Supported:** the posting text states it directly (I can point to the words).
- **Contradicted:** the posting text states the opposite (e.g. the claim "needs ≤ 2 years" when the text says "5+ years").
- **Insufficient:** the posting text doesn't say either way.

## When the agent must say "I cannot tell"
1. The posting's **description or location is missing or empty**.
2. A **deciding fact isn't stated** in the text, e.g. a location that says only "Remote" with no country, or (once years is a rule) no number of years at all.

In both cases the agent reports "I cannot tell" plus the missing field. It never guesses, and never counts an unknown as a pass.

## Expected sources
| Board | System | Fields the agent should read | If a field is missing |
|---|---|---|---|
| stripe | Greenhouse | `title`, `location.name`, `content` (HTML) | "I cannot tell" + which field |
| palantir | Lever | `text` (title), `categories.location`, `descriptionPlain` + `lists` | same |
| linear | Ashby | `title`, `location`, `descriptionPlain` | same |
| a board that failed in the run | any | none | no postings from it are judged, and the report says the board is missing (never "0 relevant") |

## Wrong versions my tests must catch
1. **US check by "contains us" text**, so "Brussels" or "Australia" would pass as US.
2. **Missing location treated as US**, instead of "I cannot tell."
3. **Case-sensitive title match**, which misses "data analyst" or "ANALYST" written in a different case.
4. **Title match as a substring**, so "analyst" inside another word (e.g. "Psychoanalyst") passes.

*(The decisions are mine: what to keep and drop, widening R1 to any "Analyst" title, when to say "I cannot tell," and which wrong versions to test. Claude suggested starting from my JS2 agent, which I accepted, suggested the "Remote alone = I cannot tell" detail, and turned my picks into these sentences.)*
