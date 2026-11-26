"""Claude as a judge, automated (Chapter 9). Every call is recorded with its model, settings, date and raw reply.

  python3 agent/claude_judge.py --label R1_base     --prompt prompts/judge_v1.txt --context full
  python3 agent/claude_judge.py --label R2_prompt   --prompt prompts/judge_v2.txt --context full
  python3 agent/claude_judge.py --label R3_context  --prompt prompts/judge_v1.txt --context title
Runs on my HELD-OUT labels by default. Claude runs from an empty temporary folder, so it cannot read my files
(including my hand verdicts); it only sees the prompt.
"""
import argparse
import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "agent"))
from postings import load_raw_dir  # noqa: E402
from shortlist import RAW  # noqa: E402

MAX_TEXT = 4000  # hand-set: enough for a posting's role and requirements, keeps each call small


def ask(prompt, model):
    with tempfile.TemporaryDirectory() as empty:
        p = subprocess.run(["claude", "-p", "--model", model, "--output-format", "json"],
                           input=prompt, capture_output=True, text=True, cwd=empty, timeout=180)
    return p.stdout, p.stderr, p.returncode


def parse(stdout):
    try:
        env = json.loads(stdout)
    except ValueError:
        return None, None, "reply was not JSON"
    text = env.get("result", "") if isinstance(env, dict) else ""
    m = re.search(r"\{.*\}", text, re.S)
    try:
        j = json.loads(m.group(0)) if m else {}
    except ValueError:
        j = {}
    v = str(j.get("verdict", "")).strip().lower()
    return env, (v if v in ("y", "n", "?") else None), j.get("reason")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--context", choices=["full", "title"], default="full")
    ap.add_argument("--model", default="claude-sonnet-5-5")
    ap.add_argument("--part", choices=["dev", "heldout"], default="heldout")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    tmpl = Path(a.prompt).read_text()
    split = json.loads((ROOT / "audit/label_split.json").read_text())
    hand = json.loads((ROOT / "audit/v1_hand_verdicts.json").read_text())
    posts = {f"{p['board']}:{p['id']}": p for p in load_raw_dir(RAW)[0]}
    keys = [k for k in split[a.part] if hand[k]["verdict"] in ("y", "n")]
    if a.limit:
        keys = keys[:a.limit]
    d = ROOT / "out" / "claude" / a.label
    d.mkdir(parents=True, exist_ok=True)
    settings = {"label": a.label, "prompt_file": a.prompt, "context": a.context, "model_requested": a.model,
                "max_text_chars": MAX_TEXT, "part": a.part, "cwd": "empty temp folder",
                "command": f"claude -p --model {a.model} --output-format json"}
    (d / "settings.json").write_text(json.dumps(settings, indent=1))
    agree = shown_n = hidden_y = unknown = 0
    for i, k in enumerate(keys, 1):
        p = posts[k]
        text = p["text"][:MAX_TEXT] if a.context == "full" else "(not provided)"
        prompt = tmpl.replace("{title}", p["title"]).replace("{location}", p["location"] or "(missing)").replace("{text}", text)
        when = datetime.now(timezone.utc).isoformat(timespec="seconds")
        out, err, code = ask(prompt, a.model)
        env, v, reason = parse(out)
        models_used = sorted((env or {}).get("modelUsage", {}).keys()) if isinstance(env, dict) else []
        rec = {"key": k, "asked_at": when, "settings": settings, "models_reported": models_used, "prompt": prompt,
               "raw_stdout": out, "stderr": err[-500:], "exit_code": code, "verdict": v, "reason": reason,
               "my_verdict": hand[k]["verdict"]}
        (d / (k.replace(":", "__") + ".json")).write_text(json.dumps(rec, indent=1))
        me = hand[k]["verdict"] == "y"
        shown = v == "y"
        unknown += v not in ("y", "n")
        agree += shown == me
        shown_n += shown and not me
        hidden_y += me and not shown
        print(f"[{a.label}] {i:2}/{len(keys)} {k[:40]:40} claude={v} me={hand[k]['verdict']}  {(reason or '')[:60]}")
    summary = dict(settings, n=len(keys), agree=agree, shown_but_me_n=shown_n, hidden_but_me_y=hidden_y,
                   unparsed_or_unsure=unknown, finished_at=datetime.now(timezone.utc).isoformat(timespec="seconds"))
    (d / "summary.json").write_text(json.dumps(summary, indent=1))
    print(f"\n[{a.label}] agree {agree}/{len(keys)}  shown,me=n {shown_n}  hidden,me=y {hidden_y}  '?'/unparsed {unknown}")


if __name__ == "__main__":
    main()
