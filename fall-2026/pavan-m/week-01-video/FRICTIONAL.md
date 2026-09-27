# Frictional Log

## 2026-09-23 -- Toolkit setup

**Kokoro model files missing on first run.** `generate_audio_kokoro.py` needed
a one-time ~330MB model download before it could generate any narration.
Fixed by running the toolkit's documented download step.

**ffmpeg not installed.** Kokoro generated raw audio successfully, but the
mp3 conversion step failed with `FileNotFoundError: [Errno 2] No such file
or directory: 'ffmpeg'`. ffmpeg wasn't on the machine yet.

**Homebrew ffmpeg install blocked by a broken tap.** `brew install ffmpeg`
hit an unrelated broken/untrusted third-party tap error that blocked the
install entirely. Rather than fight Homebrew's tap state, used the ffmpeg
already bundled with the Anaconda distribution already installed on this
machine, which sidestepped the broken tap completely.

## 2026-09-24 -- First Manim render

**MathTex rendering failed -- no LaTeX distribution installed.** Beat02Expected
originally used Manim's `MathTex` (LaTeX-based equation renderer) for the
`0.6652 x 1000 = 665.24` line, which failed with
`FileNotFoundError: [Errno 2] No such file or directory: 'latex'`.
Installing MacTeX for one equation was overkill (multi-GB download), so
swapped `MathTex` for a plain `Text` object instead, which needs no LaTeX.

## 2026-09-25 -- Full pipeline and first assembled cut

Got narration, rendering, and the audio-pairing script all working together
and produced a first assembled cut. Reviewing that cut surfaced the next
day's main issue (see below) but no new build-breaking errors on this day.

## 2026-09-26 -- Fixing frozen-frame gaps and visual bugs

**Large frozen-frame gaps on 3 of 8 beats.** Reviewing the first assembled
cut showed B04, B06, and B07's narration ran 10-13 seconds longer than
their Manim animation, so the pairing script's freeze-padding left long
dead final frames. Fixed by adding real animated content to each scene (a
highlight cycling across seed rows, line-by-line text reveal, pulsing key
words) so the extra seconds are earned by motion instead of padding.

**Word-by-word text arrangement broke line alignment.** To pulse-highlight
specific words in the recap beat, initially built each line as separate
per-word `Text` objects arranged left-to-right. This left individual words
floating above or below the rest of the line, since arranging by bounding
box (even with `aligned_edge=DOWN`) doesn't account for ascenders/descenders
the way one real text layout does. Fixed by reverting to a single `Text`
object per line.

**Word-highlight indexing bug.** To highlight a specific word inside a
single `Text` object, used Python string-slice indices assuming one
submobject per character. This assumption was wrong: Manim skips whitespace
when building per-character submobjects, so the slice landed a few
characters off and highlighted half of two adjacent words instead of one
whole word. Diagnosed by checking `len(Text(...).submobjects)` against the
string length, which confirmed the actual offset, then recomputed the
correct slice indices from the non-space character counts.

**`get_part_by_text()` doesn't exist in this Manim version.** Tried this
method (meant to look up a word by its literal text instead of by index) as
a more robust alternative, but it isn't available in the installed Manim
Community v0.21.0, raising a `TypeError`. Reverted to corrected index
slicing instead.

**Sampling-variance brace rendered partially off-frame.** The `Brace` +
label in the comparison scene were positioned to the right of the tallest
bars, which pushed the label past the right edge of the frame. Fixed by
repositioning below the bars, where there was ample room.

**Brace spanned the wrong bars.** After the above fix, the brace still
bracketed from the Expected group all the way to the Observed group (since
it was built around both blue bars, which sit on opposite ends of the
chart with unrelated bars between them) instead of marking just the
observed count's variance. Fixed by scoping the `Brace` to a single bar.
