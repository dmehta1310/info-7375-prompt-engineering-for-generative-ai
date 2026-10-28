"""Save Claude's reply from the clipboard to responses/ and validate it."""
import argparse, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from validate import validate

ap = argparse.ArgumentParser()
ap.add_argument("--id", type=int, required=True)
ap.add_argument("--version", default="v1")
ap.add_argument("--run", type=int, required=True)
a = ap.parse_args()
text = subprocess.run("pbpaste", capture_output=True, text=True).stdout
if text.lstrip().startswith("You are judging") or "(base) " in text or "python3 " in text:
    print("NOT SAVED: clipboard holds the prompt or terminal text, not Claude's reply. Copy Claude's answer and try again.")
    sys.exit(1)
out = Path(f"responses/{a.version}_{a.id}_run{a.run}.json")
if out.exists():
    print(f"NOT SAVED: {out} already exists (use a new --run number)")
    sys.exit(1)
out.write_text(text)
ok, errs, obj = validate(text, a.id)
print(("VALID" if ok else "REJECTED") + f": {out}" + (f" -> JUDGMENT (model): {obj['verdict']}" if ok else ""))
for e in errs:
    print("  -", e)
