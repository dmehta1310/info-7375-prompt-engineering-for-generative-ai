# remotion-src

`TemperatureConcentration.tsx.txt` is the TypeScript source of the seven custom Remotion scenes
(B02–B08). It carries a `.txt` extension because the course repo's validator
(`scripts/validate_course.py`) rejects `.ts/.tsx/.js` files: the course stack is Python-only.
The file is otherwise byte-for-byte the component the video was rendered from.

To rebuild, copy it back into the toolkit with its real name:

```bash
cp TemperatureConcentration.tsx.txt ../../brutalist.art/runtime/remotion/src/TemperatureConcentration.tsx
```
