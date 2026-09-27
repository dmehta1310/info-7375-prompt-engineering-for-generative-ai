# Frictional Log — Real Bugs Encountered While Building This Video

This log documents genuine technical friction encountered while producing this
assignment with the Brutalist toolkit, in the order encountered.

1. **Missing system dependencies.** The toolkit required Homebrew plus
   `cairo`, `pkg-config`, `pango`, `node`, and `ffmpeg`, none of which were
   pre-installed. Each had to be installed manually before the toolkit would
   run at all.

2. **Hardcoded text truncation.** `compile.py` silently truncated on-screen
   text to 80 characters (`[:80]`), cutting off longer captions mid-word
   with no warning or error.

3. **Unregistered custom scenes.** New Manim/Remotion scene components were
   written as standalone files but never appeared in the render because they
   were not registered in Remotion's `Root.tsx` composition list. A stale
   scene index also needed regenerating (`./art scene-index`) after adding
   new scenes.

4. **Silent placeholder fallback (the biggest bug).** The beat sheet
   (`beat_sheet.json`) only stores props that differ from a scene's built-in
   defaults. Any prop left unset silently fell back to hardcoded example
   content (e.g., "The quick brown fox," "Photoelectric Effect") instead of
   raising an error. This was invisible in the compile logs and was only
   caught by extracting actual rendered frames with `ffmpeg` and visually
   inspecting them — text summaries claiming "all fixed" were wrong on
   multiple occasions before frame-level inspection confirmed the real state.

5. **Audio/visual duration mismatch.** The outro clip's narration audio ran
   longer than its visual duration, causing the audio to cut off before the
   sentence finished.

6. **Inconsistent background color across beats.** Newly authored scenes used
   a slightly different off-white shade than the toolkit's default system
   beats, creating a visible seam between beats. Traced to one component
   using a different hex value than the rest; unified to a single consistent
   color across all beats.

7. **Hardcoded author attribution.** The toolkit's default outro attribution
   was hardcoded to the toolkit author's own handle. Since this is an
   individual course assignment and not a Brutalist-branded series, this was
   replaced with the student's own name, and the cream background shade was
   also adjusted to be visually distinct from the toolkit's reference/demo
   video.

8. **Canvas-dimension mismatch across the render pipeline.** The final
   compiled video is produced at 1280×720, but several custom scene
   components had absolute pixel positions calculated assuming a 1920×1080
   canvas. This caused visual elements (card grids) to render off-center by
   a consistent ratio. Diagnosing this required tracing the actual dimension
   calculation in `compile.py` rather than guessing at corrected pixel
   values, since earlier attempts to "eyeball-correct" the positions
   repeatedly overshot or undershot the true center.
