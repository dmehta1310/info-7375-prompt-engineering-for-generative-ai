"""One sampling run: copy prompt -> you ask Claude in a fresh chat -> save + validate reply."""
import argparse, json, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import watch
from validate import validate

ap = argparse.ArgumentParser()
ap.add_argument("--id", type=int, required=True)
ap.add_argument("--run", type=int, required=True)
ap.add_argument("--version", default="v1")
ap.add_argument("--snapshot", default="evidence/manual-snapshots/stripe_2026-10-27T232715Z.json")
a = ap.parse_args()
out = Path(f"responses/{a.version}_{a.id}_run{a.run}.json")
if out.exists():
    sys.exit(f"STOP: {out} already exists (use the next --run number)")
persona = json.loads(Path("persona/priya_nair.json").read_text())
job = [j for j in json.loads(Path(a.snapshot).read_text())["jobs"] if j["id"] == a.id][0]
prompt = (Path(f"prompts/judge_{a.version}.txt").read_text()
          .replace("{{PERSONA}}", json.dumps(persona, indent=2))
          .replace("{{POSTING_ID}}", str(job["id"]))
          .replace("{{TITLE}}", job["title"])
          .replace("{{LOCATION}}", job["location"]["name"])
          .replace("{{CONTENT}}", watch.clean(job["content"]).strip()))
Path(f"prompts/filled/{a.version}_{a.id}.txt").write_text(prompt)
subprocess.run("pbcopy", input=prompt.encode())
print(f"Prompt for {a.id} ({a.version}, run {a.run}) is in your clipboard.")
print("1) New INCOGNITO chat on claude.ai  2) Cmd+V, Enter  3) Screenshot  4) Copy Claude's reply")
input("5) Come back here and press Enter... ")
while True:
    text = subprocess.run("pbpaste", capture_output=True, text=True).stdout
    bad = (text.lstrip().startswith("You are judging") or "python3 " in text
           or "(base) " in text or "agent/sample.py" in text or not text.strip())
    if not bad:
        break
    print("That is not Claude's reply (looks like the prompt, a command, or terminal text). Nothing saved.")
    input("Copy Claude's reply from the incognito chat, then press Enter... ")
out.write_text(text)
ok, errs, obj = validate(text, a.id)
stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
with open("responses/log.csv", "a") as f:
    f.write(f"{stamp},{a.version},{a.id},{a.run},{'VALID' if ok else 'REJECTED'},{obj['verdict'] if ok else ''}\n")
print(("VALID" if ok else "REJECTED") + f": {out}" + (f" -> JUDGMENT (model): {obj['verdict']}" if ok else ""))
for e in errs:
    print("  -", e)
