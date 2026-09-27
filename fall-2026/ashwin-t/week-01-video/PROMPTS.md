# PROMPTS — w1-softmax-offset

The toolkit's Gate F asks for beat-prefixed generation prompts for any open slot.

**There are none.** No beat uses AI image or video generation, a pantry still, or
a screen capture. Every visual is drawn by the Remotion component `SoftmaxOffset`
from props in `beat_sheet.json`, and every number in those props is read from
`w1-evidence/*.txt` by `tools/build_beat_sheet.py`.

The prompts used to *build* the video (with Claude Code) are in `BUILD-PROMPT.md`.
