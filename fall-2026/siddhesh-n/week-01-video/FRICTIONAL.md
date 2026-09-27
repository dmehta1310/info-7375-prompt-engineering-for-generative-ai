# Frictional — Week 1 Explainer Video

**Student:** Siddhesh Nikam

**Assignment:** Week 1 Explainer Video — Explain One Concept from Chapter 1

**Course:** INFO 7375

This is an honest build record. Codex organized the entries from the actual work in this session; it did not invent personal effort, a test result, or a difficulty that did not occur.

## 2026-09-26 — Choosing one concept and protecting the deadline

**Date and what I was working on:** 2026-09-26, selecting and scoping the explainer concept.

**I tried / expected:** I asked for a complete submission within about one hour. I expected the main risk to be finishing all required files and a working MP4 before the deadline.

**What happened:** The assignment warned against summarizing the whole chapter. The max-subtraction idea was small enough to explain with one worked calculation, one proof, and one limitation.

**What I did:** I accepted the narrow concept: why subtracting the maximum changes intermediate values but not the distribution. I rejected a broader Chapter 1 tour.

**What Claude or another person contributed:** Claude was not used. OpenAI Codex proposed the narrow concept, drafted the first beat sheet, wrote the calculation and rendering code, and assembled the required files. I requested that the video be improved rather than submitting the first draft.

**What I understand now / still do not understand:** I can explain that a shared offset preserves the gaps between scores and becomes a common exponential factor. I still need to practice explaining the cancellation without reading the formula.

**Evidence and next step:** `beat_sheet.json`, `code/softmax_demo.py`, and commit subject `Add Week 1 softmax explainer video`. Next: compare the first render with the professor's course visuals.

## 2026-09-26 — Toolkit setup stopped, then Kokoro worked manually

**Date and what I was working on:** 2026-09-26, local narration and rendering.

**I tried / expected:** The public toolkit was cloned and `./setup` was run. I expected its readiness check to continue into normal installation.

**What happened:** The check stopped on `ElevenLabs reference found — this toolkit is Kokoro-only for narration` and listed legacy references inside the toolkit's own example files. The first emergency render therefore used FFmpeg's local flite voice. That render worked, but the voice was noticeably robotic.

**What I did:** I kept the working fallback so the deadline was protected, then installed the documented `kokoro-onnx` package and downloaded the documented free model files manually. The second render used Kokoro `am_onyx`.

**What Claude or another person contributed:** Codex diagnosed that the top-level check was failing on repository examples, installed the documented dependency and model, regenerated every narration beat, and retained the failure instead of hiding it. I listened conceptually through the result and reported that the voice still sounded too hard.

**What I understand now / still do not understand:** I understand that the audio files define the timing for the visuals. I do not know why the toolkit's current repository-wide check rejects its own archived examples; resolving that upstream is outside this submission.

**Evidence and next step:** `mp3/timings.json`, the dated setup error above, and commit subject `Upgrade narration and animate softmax mechanism`. Next: try the supported `af_bella` voice at a slightly slower speed.

## 2026-09-26 — Revising from the professor's actual materials

**Date and what I was working on:** 2026-09-26, visual and evidence revision after reviewing the professor's GitHub figure.

**I tried / expected:** I compared the second render with the professor's diagram. I expected mostly cosmetic changes.

**What happened:** The screenshot showed a clearer course language: white background, serif title, dark outlined process boxes, gray supporting text, red emphasis, and a gold footer rule. More importantly, the actual course repository was available. Its `main.py` prints probabilities for `[1,2,3]`, and its official test checks `[1000,1000] → [0.5,0.5]`. Those are stronger evidence than the constructed `[1000,999,998]` input in the earlier draft.

**What I did:** I rejected the earlier constructed example, replaced it with the course program's real output and official test, changed the graphics to an original course-aligned diagram style, switched narration to supported Kokoro `af_bella` at speed `0.94`, and kept the explicit boundary about what the transformation does not establish.

**What Claude or another person contributed:** Codex cloned and inspected the actual course repository, ran `lessons/01-randomness-and-first-prompts/code/main.py`, read the relevant Chapter 1 section and test file, rewrote the evidence script and narration, and rebuilt the video. I supplied the professor screenshot and requested a clearer voice and closer professional style.

**What I understand now / still do not understand:** I understand why the official `[1,2,3]` example is better: it connects every screen value directly to the course source. I still must watch the final MP4 myself and be ready to defend the algebra and the AI-assistance disclosure.

**Evidence and next step:** `code/course_main_output.txt`, `code/softmax_output.txt`, `SOURCES.md`, the final MP4, and the final commit. Next: watch the full file, upload the matching folder to GitHub, and paste that folder URL and final remote commit hash into Canvas.
