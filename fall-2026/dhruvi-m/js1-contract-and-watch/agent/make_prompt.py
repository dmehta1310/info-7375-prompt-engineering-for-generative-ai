"""Fill a prompt contract for one posting and copy it to the clipboard (macOS pbcopy)."""
import argparse, json, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import watch

ap = argparse.ArgumentParser()
ap.add_argument("--id", type=int, required=True)
ap.add_argument("--version", default="v1")
ap.add_argument("--snapshot", default="evidence/manual-snapshots/stripe_2026-10-27T232715Z.json")
a = ap.parse_args()
persona = json.loads(Path("persona/priya_nair.json").read_text())
job = [j for j in json.loads(Path(a.snapshot).read_text())["jobs"] if j["id"] == a.id][0]
text = (Path(f"prompts/judge_{a.version}.txt").read_text()
        .replace("{{PERSONA}}", json.dumps(persona, indent=2))
        .replace("{{POSTING_ID}}", str(job["id"]))
        .replace("{{TITLE}}", job["title"])
        .replace("{{LOCATION}}", job["location"]["name"])
        .replace("{{CONTENT}}", watch.clean(job["content"]).strip()))
out = Path(f"prompts/filled/{a.version}_{a.id}.txt")
out.write_text(text)
subprocess.run("pbcopy", input=text.encode())
print(f"wrote {out} and copied it to the clipboard ({len(text)} characters)")
