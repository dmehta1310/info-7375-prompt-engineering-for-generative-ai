#!/usr/bin/env python3
"""Job-Search Agent 1: watch one Greenhouse board, report postings new since
the last run, and judge each by the written rule in CONTRACT.md."""
import argparse, html, json, re, sys, urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ALLOWED_HOSTS = {"boards-api.greenhouse.io"}
BOARD = "stripe"
BOARD_URL = f"https://boards-api.greenhouse.io/v1/boards/{BOARD}/jobs?content=true"

# Rule 3 (CONTRACT.md)
US_TAGS = ["US", "US-Remote", "New York", "NYC", "NY", "SF", "San Francisco",
           "Seattle", "SEA", "WA", "Chicago", "CHI", "IL", "Atlanta", "Georgia"]
EXACT_OK = {"remote", "n/a"}
CONTAINS_OK = ["north america", "us / canada", "remote-canada"]
# Rule 2 (CONTRACT.md)
MIN_SKILLS = 3


class Refused(Exception):
    pass


def fetch(url):
    host = urlparse(url).hostname
    if host not in ALLOWED_HOSTS:
        raise Refused(f"host not on allow-list: {host}")
    req = urllib.request.Request(url, headers={"User-Agent": "INFO7375-JS1-student-agent"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def validate_persona(p):
    problems = []
    if p.get("fictional") is not True:
        problems.append('missing "fictional": true')
    if not str(p.get("email", "")).endswith("@example.com"):
        problems.append("email must end in @example.com")
    if not str(p.get("phone", "")).startswith("555"):
        problems.append("phone must start with 555")
    for k in ("target_titles", "skills", "locations"):
        if not isinstance(p.get(k), list) or not p[k]:
            problems.append(f"{k} must be a non-empty list")
    if problems:
        raise Refused("persona rejected: " + "; ".join(problems))
    return p


def has_word(text, term):
    """Whole-word, case-insensitive match (so Excel != excellent, SQL != NoSQL)."""
    pattern = r"(?<![A-Za-z0-9])" + re.escape(term) + r"(?![A-Za-z0-9])"
    return re.search(pattern, text, re.IGNORECASE) is not None


def clean(content):
    t = html.unescape(html.unescape(content or ""))
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", t)


def location_check(loc):
    s = (loc or "").strip()
    low = s.lower()
    if low in EXACT_OK:
        return True, f'location is exactly "{s}"'
    for c in CONTAINS_OK:
        if c in low:
            return True, f'location contains "{c}"'
    for tag in US_TAGS:
        if has_word(s, tag):
            return True, f'location names US tag "{tag}"'
    return False, "no US place or tag; not exactly Remote or N/A; no North America, US / Canada, or Remote-Canada"


def judge(job, persona):
    title = job.get("title", "")
    loc = (job.get("location") or {}).get("name", "")
    text = clean(job.get("content", ""))
    t_hits = [t for t in persona["target_titles"] if t.lower() in title.lower()]
    s_hits = [s for s in persona["skills"] if has_word(text, s)]
    l_ok, l_why = location_check(loc)
    checks = {
        "title": {"pass": bool(t_hits), "resume_field": "target_titles",
                  "posting_field": "title", "posting_value": title, "matched": t_hits},
        "skills": {"pass": len(s_hits) >= MIN_SKILLS, "resume_field": "skills",
                   "posting_field": "content", "matched": s_hits,
                   "count": len(s_hits), "needed": MIN_SKILLS},
        "location": {"pass": l_ok, "resume_field": "locations",
                     "posting_field": "location.name", "posting_value": loc, "why": l_why},
    }
    verdict = "relevant" if all(c["pass"] for c in checks.values()) else "not relevant"
    return {"posting_id": job["id"], "title": title, "location": loc,
            "rule_verdict": verdict, "rule_justification": checks,
            "claude_verdict": None}


def new_since(jobs, seen_ids):
    seen = set(seen_ids)
    return [j for j in jobs if j["id"] not in seen]


def main(argv=None):
    ap = argparse.ArgumentParser(description="Job-Search Agent 1")
    ap.add_argument("--persona", default="persona/priya_nair.json")
    ap.add_argument("--state", default="state/seen_ids.json")
    ap.add_argument("--from-file", help="SEEDED run: use a saved raw response instead of fetching")
    ap.add_argument("--out", default="evidence")
    a = ap.parse_args(argv)
    try:
        persona = validate_persona(json.loads(Path(a.persona).read_text()))
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
        out = Path(a.out)
        if a.from_file:
            raw = Path(a.from_file).read_bytes()
            mode, raw_saved = "SEEDED", a.from_file
        else:
            raw = fetch(BOARD_URL)
            (out / "raw").mkdir(parents=True, exist_ok=True)
            raw_path = out / "raw" / f"stripe_{ts}.json"
            raw_path.write_bytes(raw)
            mode, raw_saved = "LIVE", str(raw_path)
    except Refused as e:
        print(f"REFUSED: {e}")
        return 2
    jobs = json.loads(raw)["jobs"]
    sp = Path(a.state)
    if sp.exists():
        state = json.loads(sp.read_text())
        new, kind = new_since(jobs, state["seen_ids"]), "FOLLOW-UP"
    else:
        state, new, kind = {"seen_ids": [], "runs": []}, [], "BASELINE"
    results = [judge(j, persona) for j in new]
    state["seen_ids"] = sorted(set(state["seen_ids"]) | {j["id"] for j in jobs})
    summary = {"run_at_utc": ts, "kind": kind, "mode": mode, "raw_response": raw_saved,
               "total_postings": len(jobs), "new_postings": len(new)}
    state["runs"].append(summary)
    sp.parent.mkdir(parents=True, exist_ok=True)
    sp.write_text(json.dumps(state, indent=2))
    (out / "reports").mkdir(parents=True, exist_ok=True)
    report_path = out / "reports" / f"run_{ts}_{kind.lower()}.json"
    report_path.write_text(json.dumps({**summary, "results": results}, indent=2))
    print(f"{kind} ({mode}) at {ts} UTC: {len(jobs)} postings, {len(new)} new")
    for r in results:
        print(f"  {r['posting_id']} | {r['rule_verdict']:12} | {r['title']} | {r['location']}")
    print(f"report: {report_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
