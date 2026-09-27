# BUILD-PROMPT — Why 630, Not 665?

Run from the activated brutalist.art checkout (`source .venv/bin/activate`), normal permissions.
`REEL=~/Applications/info-7375-prompt-engineering-for-generative-ai/youtube/week-01-video-atharva-c`

```bash
python3 runtime/scripts/generate_audio_kokoro.py "$REEL"   # measured narration (af_bella)
./art run "$REEL" --height 1080                              # review cut + gates
./art todo "$REEL"                                           # open-beat ledger
# after human review of the cut:
./art final "$REEL" --height 1080 --out "$REEL/final"
```

Paste-ready Claude Code prompt:

> In the brutalist.art checkout, rebuild the reel at the path above from its beat_sheet.json. Do not edit narration without my approval; regenerate audio with Kokoro af_bella, run `./art run --height 1080`, then sample frames at 15/50/85 % of every beat, read them, and log defects in `_qc/REPORT.md`. Fix root causes and re-render. No paid calls, no permission bypass, no publishing. Report the actual output path.
