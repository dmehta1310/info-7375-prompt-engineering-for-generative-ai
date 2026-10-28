"""Validate one Claude reply against the prompt contract. Rejects anything else."""
import argparse, json, sys
from pathlib import Path

KEYS = {"posting_id", "verdict", "cited_resume_fields", "cited_posting_fields", "reason"}
RESUME = {"target_titles", "skills", "locations", "years_experience"}
POSTING = {"title", "location", "description"}


def validate(text, expected_id):
    try:
        obj = json.loads(text)
    except Exception as e:
        return False, [f"not valid JSON on its own (fences or extra text?): {e}"], None
    if not isinstance(obj, dict):
        return False, ["not a JSON object"], None
    errs = []
    if set(obj) != KEYS:
        errs.append(f"keys must be exactly {sorted(KEYS)}, got {sorted(obj)}")
    if obj.get("posting_id") != expected_id:
        errs.append(f"posting_id {obj.get('posting_id')!r} does not match {expected_id}")
    if obj.get("verdict") not in ("relevant", "not relevant"):
        errs.append(f"verdict {obj.get('verdict')!r} is not 'relevant' or 'not relevant'")
    for k, allowed in (("cited_resume_fields", RESUME), ("cited_posting_fields", POSTING)):
        v = obj.get(k)
        if not isinstance(v, list) or not v:
            errs.append(f"{k} must be a non-empty list (a justification that cites nothing is rejected)")
        elif not set(v) <= allowed:
            errs.append(f"{k} has unknown fields {sorted(set(v) - allowed)}")
    r = obj.get("reason")
    if not isinstance(r, str) or not r.strip() or len(r) > 300:
        errs.append("reason must be a non-empty string under 300 characters")
    return not errs, errs, obj


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--id", type=int, required=True)
    a = ap.parse_args()
    ok, errs, obj = validate(Path(a.file).read_text(), a.id)
    if ok:
        print(f"VALID: {a.file} -> JUDGMENT (model): {obj['verdict']}")
        sys.exit(0)
    print(f"REJECTED: {a.file}")
    for e in errs:
        print("  -", e)
    sys.exit(1)
