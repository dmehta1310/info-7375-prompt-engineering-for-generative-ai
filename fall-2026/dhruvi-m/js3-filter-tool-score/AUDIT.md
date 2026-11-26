# Reject audit (filter v1, Chapter 7)

**What I judged:** 69 postings, by hand, as Priya (fictional data analyst, 2 years' experience, US-based). The sample was drawn with seed 7375 **before** I judged anything (`a877084`); the filter's own verdict was **hidden** from me while judging. 1 posting was judged one-at-a-time in the terminal, the other 68 from a one-line-per-posting sheet (`agent/fast_sheet.py`); every verdict and reason code is mine (`37efc38`). The reason codes (1–8) were suggested by Claude; I chose every verdict and code.

| Group | Size | Filter wrong (by my verdict) | 95% Wilson interval |
|---|---|---|---|
| Random sample of rejects | 30 (of 1,078 rejected) | **2** | 2%–21% |
| Closest calls (passed the title rule, failed on location; or near-miss title words) | 10 | 1 | 2%–40% |
| Everything the filter kept | 27 (all) | **2** | 2%–23% |
| Everything the filter said "cannot tell" | 2 (all) | n/a (I said yes to both) | n/a |

Full output: `audit/v1_report.txt`. Hand verdicts: `audit/v1_hand_verdicts.json`.

## What this sample can honestly show
2 wrong out of 30 random rejects is consistent with a true miss rate anywhere from **about 2% to 21%** of the 1,078 rejected postings, roughly 20 to 230 jobs I might want. **This is an estimate from a sample of 30, not a measured rate for all rejects.** A sample this small cannot tell a 2% miss rate from a 20% one.

## What the filter got wrong
- **Missed** (rejected, I said yes): *Marketing Operations Manager, AMER Events* and *Senior Identity Security Engineer* (no target word in the title), and *Analytics Engineer | North America* (location not counted as US).
- **Wrongly kept** (kept, I said no): *Mobility Tax Analyst* (my code 2: "Analyst" but not data work) and *Internal Audit Data Analytics Lead* (8026689). For 8026689 my reason code was 3 ("not in the US"), but its location lists New York, San Francisco, Atlanta and Seattle; when asked, I chose to keep that code. My "no" stands; my stated reason does not match the location field.

## The false friend
**"Analyst"** in ***Mobility Tax Analyst*** (Palantir, Palo Alto). The filter kept it only because the title has the word "Analyst"; the posting is payroll-tax compliance and accounting reporting, not data work. I judged it "not worth Priya's time" (code 2).

## Rules added, cut, or rejected after measuring
On my 34 **dev** labels (split before any change, `8de1202`), one change at a time (`9cef31e`):

| Filter | Agree | Shown, I said no | Hidden, I said yes | Decision |
|---|---|---|---|---|
| v1 (baseline) | 31/34 | 0 | 3 | baseline |
| A: "North America" = US | 32/34 | 0 | 2 | **added → v2** |
| B: years ≤ 2 | 20/34 | 0 | 14 | **rejected** |
| C: cut bare "Analyst" | 22/34 | 0 | 12 | **rejected** |
| D: 3+ skills | 20/34 | 0 | 14 | **rejected** |

On the 35 **held-out** labels, used once (`d66395f`): v1 31/35, v2 31/35. **Held-out cannot tell v1 and v2 apart**: the one posting v2 fixes is in the dev half, and no held-out posting says "North America."
