"""Pre-flight copy of the two course-repo CI rules that apply to this folder
(scripts/validate_course.py): no .js/.ts/.tsx/.jsx/.rs/.jl/.go files, every .py
parses, and every relative markdown link resolves. Exit 1 on any failure."""
import ast, re, sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parents[1])
fails = []
for path in root.rglob("*"):
    if any(p in {".git", ".venv", "learning-artifacts", "__pycache__"} for p in path.parts):
        continue
    if path.suffix in {".js", ".ts", ".tsx", ".jsx", ".rs", ".jl", ".go"}:
        fails.append(f"Non-Python implementation: {path.relative_to(root)}")
    if path.suffix == ".py":
        ast.parse(path.read_text(), filename=str(path))
    if path.suffix == ".md":
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if "://" in target or target.startswith("#"):
                continue
            target = target.split("#")[0]
            if target and not (path.parent / target).exists():
                fails.append(f"Broken local link in {path.relative_to(root)}: {target}")
print("\n".join(fails) or "repo rules: OK")
sys.exit(1 if fails else 0)
