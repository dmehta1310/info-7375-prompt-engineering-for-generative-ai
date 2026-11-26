"""Source-grounded shortlist (Chapter 7). Every claim is labeled against the posting's own text.

  python3 agent/shortlist.py --filter config/filter_v2.json
Writes out/shortlist/shortlist.json and SHORTLIST.md (claims, labels, quoted evidence).
Labels follow FILTER.md: supported / contradicted / insufficient.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "agent"))
from filter import judge, location_is_us, min_years, skills_found  # noqa: E402
from postings import load_raw_dir  # noqa: E402

RAW = ROOT.parent / "js2-loop-tools-diff/out/runs/2026-11-09T220326Z_LIVE/raw"
SKILLS = ["SQL", "Python", "Tableau", "dbt", "A/B testing", "Excel"]
DATA_WORK = re.compile(r"\b(data analysis|analy[sz]e data|analy[sz]ing data|dashboards?|metrics|SQL|"
                       r"statistic\w*|A/B test\w*|data models?|reporting|insights from data|data pipelines?)\b", re.I)
YEARS = re.compile(r"(\d{1,2})\s*\+?\s*(?:(?:-|–|to)\s*\d{1,2}\s*\+?\s*)?years?", re.I)
WORD_YEARS = re.compile(r"\b(one|two|three|four|five|six|seven|eight|nine|ten)\s*\+?\s*(?:or more\s*)?years?\b", re.I)


def quote(text, m, width=60):
    a, b = max(0, m.start() - width), min(len(text), m.end() + width)
    return ("…" if a else "") + text[a:b].strip() + ("…" if b < len(text) else "")


def claims_for(p, cfg, verdict):
    t = p["text"]
    out = []
    hit = verdict["checks"].get("title_word")
    out.append({"claim": "The title names a target role",
                "label": "supported" if hit else "insufficient",
                "evidence": f"title: \"{p['title']}\"" + (f" (matches '{hit}')" if hit else "")})
    us = location_is_us(p["location"], extra=tuple(x.lower() for x in cfg.get("extra_us_places", [])))
    out.append({"claim": "The job is in the US",
                "label": {True: "supported", False: "contradicted", None: "insufficient"}[us],
                "evidence": f"location: \"{p['location'] or '(missing)'}\""})
    y = min_years(t)
    ym = YEARS.search(t)
    if y is None:
        out.append({"claim": "It fits about 2 years of experience", "label": "insufficient",
                    "evidence": "no number of years found in the text"})
    else:
        m = next(mm for mm in YEARS.finditer(t) if int(mm.group(1)) == y) if ym else None
        out.append({"claim": "It fits about 2 years of experience",
                    "label": "supported" if y <= 2 else "contradicted",
                    "evidence": quote(t, m) if m else f"lowest stated: {y} years"})
    sk = skills_found(t, SKILLS)
    out.append({"claim": "It uses Priya's skills (SQL, Python, Tableau, dbt, A/B testing, Excel)",
                "label": "supported" if sk else "insufficient",
                "evidence": quote(t, re.search(re.escape(sk[0]), t, re.I)) if sk else "none of her skills named"})
    dm = DATA_WORK.search(t)
    out.append({"claim": "The work itself is data analysis",
                "label": "supported" if dm else "insufficient",
                "evidence": quote(t, dm) if dm else "no data-analysis wording found in the text"})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--filter", default=str(ROOT / "config/filter_v2.json"))
    a = ap.parse_args()
    cfg = json.loads(Path(a.filter).read_text())
    posts, _ = load_raw_dir(RAW)
    hand = json.loads((ROOT / "audit/v1_hand_verdicts.json").read_text())
    short, abstained = [], []
    for p in posts:
        v = judge(p, cfg)
        key = f"{p['board']}:{p['id']}"
        if v["verdict"] == "relevant":
            short.append({"key": key, "title": p["title"], "location": p["location"],
                          "my_verdict": hand.get(key, {}).get("verdict"), "claims": claims_for(p, cfg, v)})
        elif v["verdict"] == "cannot_tell":
            us_in_text = re.search(r"\b(United States|U\.S\.|US-based|based in the US|within the US)\b", p["text"])
            abstained.append({"key": key, "title": p["title"], "location": p["location"], "reason": v["reasons"][0],
                              "my_verdict": hand.get(key, {}).get("verdict"),
                              "text_says_us": quote(p["text"], us_in_text) if us_in_text else None})
    # relevance is not entailment: shortlisted, but the posting does not support "the work is data analysis"
    not_entailed = [s for s in short if s["claims"][4]["label"] != "supported"]
    word_years = []
    for p in posts:
        m = WORD_YEARS.search(p["text"])
        if m and min_years(p["text"]) is None:
            word_years.append({"key": f"{p['board']}:{p['id']}", "title": p["title"], "evidence": quote(p["text"], m)})
    d = ROOT / "out" / "shortlist"
    d.mkdir(parents=True, exist_ok=True)
    (d / "shortlist.json").write_text(json.dumps({"filter": cfg["version"], "shortlist": short, "abstained": abstained,
                                                  "relevance_not_entailment": [s["key"] for s in not_entailed],
                                                  "years_written_in_words": word_years}, indent=1))
    L = [f"# Source-grounded shortlist (filter {cfg['version']}, generated by `agent/shortlist.py`)", "",
         "Each claim in a posting's justification is labeled **only against that posting's own text** (FILTER.md evidence rules). "
         "Evidence is a short quote from the posting. *My verdict* is my hand label from the audit (blank = not in my sample).", ""]
    from collections import Counter
    c = Counter(cl["label"] for s in short for cl in s["claims"])
    L += [f"**{len(short)} shortlisted postings, {sum(c.values())} claims:** supported {c['supported']}, "
          f"contradicted {c['contradicted']}, insufficient {c['insufficient']}.", ""]
    for s in short:
        L += [f"## {s['title']} | {s['location']}  (`{s['key']}`, my verdict: {s['my_verdict'] or '—'})", "",
              "| Claim | Label | Evidence from the posting |", "|---|---|---|"]
        L += [f"| {cl['claim']} | **{cl['label']}** | {cl['evidence'].replace('|', '/')} |" for cl in s["claims"]]
        L.append("")
    L += ["## Relevance is not entailment", "",
          f"{len(not_entailed)} shortlisted postings match my filter's words, but their text does **not** support the claim "
          "\"the work itself is data analysis\":", ""]
    L += [f"- {s['title']} | {s['location']} — {s['claims'][4]['evidence']} (my verdict: {s['my_verdict'] or '—'})" for s in not_entailed]
    L += ["", "## Abstention (\"I cannot tell\") and its limits", "",
          "Rule (FILTER.md): abstain when the description or location is missing, or a deciding fact is not stated "
          "(e.g. location only says \"Remote\").", ""]
    for x in abstained:
        L.append(f"- Abstained: {x['title']} | {x['location']} — {x['reason']}. My verdict: {x['my_verdict'] or '—'}."
                 + (f" **The text does say:** {x['text_says_us']}" if x["text_says_us"] else " The text does not name a country either."))
    L += ["", "Years written in words (the parser only reads digits, so these count as \"no years stated\"):", ""]
    L += [f"- {w['title']} (`{w['key']}`): {w['evidence']}" for w in word_years[:5]] or ["- none found in these postings"]
    (ROOT / "SHORTLIST.md").write_text("\n".join(L) + "\n")
    print(f"shortlist: {len(short)} postings, claims {dict(c)}")
    print(f"relevance-not-entailment cases: {len(not_entailed)}")
    for x in abstained:
        print(f"abstained: {x['title']} | {x['location']} | text says US: {bool(x['text_says_us'])} | my verdict: {x['my_verdict']}")
    print(f"years written in words (missed by parser): {len(word_years)}")
    print("wrote SHORTLIST.md and out/shortlist/shortlist.json")


if __name__ == "__main__":
    main()
