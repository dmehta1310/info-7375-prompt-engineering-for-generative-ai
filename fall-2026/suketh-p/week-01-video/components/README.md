# components/ — deliberately NOT vendored

The seven reel-local Remotion scenes this film uses were written by Claude for this reel
(see `../SOURCES.md` §4), but the `.tsx` source is **not committed to this repository**.
That is not an omission; it is the repository's own rule, and it is enforced.

## Why

[`AGENTS.md`](../../../../AGENTS.md) is explicit:

> Brutalist video preparation is a separate media-tool exception: use an external
> `brutalist.art` checkout for its Node/Remotion and Python packages, **never vendor that
> stack into the course**.

And [`scripts/validate_course.py`](../../../../scripts/validate_course.py) enforces it — any
`.ts`, `.tsx`, `.js`, `.jsx`, `.rs`, `.jl` or `.go` file outside `learning-artifacts/`
is a hard failure:

```python
if path.suffix in {".js", ".ts", ".tsx", ".jsx", ".rs", ".jl", ".go"}:
    failures.append(f"Non-Python implementation: {path.relative_to(ROOT)}")
```

The build session found this by running the validator against the staged folder before
opening a PR. It exited **1** on `components/ShiftedNotChanged.tsx`. Since
`.github/workflows/course.yml` runs that validator on every push and pull request,
committing the file would have put a red CI check on the one category explicitly graded
for *proper* posting.

Writing the file out as `.tsx.txt` to slip past the check was the obvious workaround and
the wrong one — the rule is about keeping the Node/Remotion stack out of a
Python-and-Claude course, not about file extensions.

## Where the source actually lives

```
<your brutalist.art checkout>/runtime/remotion/src/ShiftedNotChanged.tsx   (1382 lines)
```

Registered in that checkout's `Root.tsx` under the folder `ShiftedNotChanged`, with seven
compositions: `ShiftOverflow`, `ShiftPipeline`, `ShiftCancellation`, `ShiftReceipt`,
`ShiftBoundary`, `ShiftComposer`, `ShiftOutro`. `ShiftComposer` wraps the toolkit's
unmodified `ClaudeComposerAsk` and overlays the on-screen disclosure pill.
[`../BUILD-PROMPT.md`](../BUILD-PROMPT.md) has the full rebuild recipe; `../SHOTLIST.md`
maps each beat to its component.

## What a reviewer needs to judge it, without the file

Excerpts below are documentation, not a vendored implementation. They are cut from the
real file at staging time, by marker, so they cannot drift from it.

**The contract the whole file is built around** — every figure arrives as a prop from the
beat sheet; the schema defaults exist only so a scene previews standalone:

```tsx
 * SOURCE CARE — the rule this file is built around: every figure the film
 * renders arrives as a PROP from beat_sheet.json. The same values also sit in
 * the Zod schemas as defaults, so each composition previews standalone in
 * Remotion Studio; the beat sheet overrides all of them at render time. Every
 * prop value was read out of
 *   youtube/week-01-shifted-not-changed/evidence/run-output.txt
 * which is the recorded output of verify_claims.py against the course's own
 * lessons/01-randomness-and-first-prompts/code/main.py. A wrong number is
 * therefore a beat-sheet fix, never a component fix.
```

**The palette, and one accessibility decision GATE T forced** (see `../TYPECHECK.md`):

```tsx
// -- Palette (claude fidelity: ink on cream, ONE terracotta) ------------------
const BG = '#F2F0E9';
const INK = '#3D3929';
const ACC = '#D97757';
const SOFT = '#73705F';
// GHOST is deliberately UNUSED as a text colour. It measures 1.98:1 on the
// cream stage — far below WCAG AA-large (3:1). GATE T caught it carrying the
// synthetic-narration disclosure, which is the last text that should be hard
// to read; all three uses moved to SOFT (4.37:1). See TYPECHECK.md. Kept here
// so the palette block stays a complete record of the brand's tokens.
const GHOST = '#B0AD9A';
const CARD = '#FFFFFF';
const BORDER = '#DDD9CC';
```

**The single clock.** Every scene is a pure function of the frame, so any frame
re-renders identically — which is what makes the film reproducible at all:

```tsx
/** Progress p in [0,1] across the beat. The one clock. */
const useP = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  return cl(frame / Math.max(1, durationInFrames - 1));
};
```

## Verify the component without reading it

The claims that matter about it are checked mechanically:

```bash
python3 ../evidence/gate_t_typecheck.py    # §8.3 contrast + §8.3b no colour-only meaning
```

That gate parses the real `.tsx` (from the external checkout, or from this folder if you
place a copy here) and reports WCAG ratios, the type floor, and whether every terracotta
element carries a non-colour signal.
