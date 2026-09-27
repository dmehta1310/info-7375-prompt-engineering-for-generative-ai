# Token, Not Word: Why Letter-Counting Breaks

**Name:** Tushar Patel
**Course:** INFO7375 Prompt Engineering, Week 1 Explainer Video
**Concept (Chapter 1, Part 1):** The unit is a token, not a word, and why that breaks letter-counting prompts.
**Runtime:** 2:43 (163.29 s, 3840×2160, 24 fps)

## Why this concept

It is the smallest idea in Chapter 1 that I could show with real, reproducible numbers on screen. It also leads straight to the chapter's main distinction: a fluent, correct answer is not evidence that the underlying operation was easy.

## What the video claims, and what it does not

- **Shown with real data:** `strawberry` is 10 characters but 3 tokens (`str` / `aw` / `berry`, IDs 496 / 675 / 15717). The r's sit inside those chunks. Adding a leading space collapses the word to 1 token (73700). `unbelievable` splits as `un` / `belie` / `vable`. The token `berry` (15717) is reused in `raspberry`.
- **Real, dated AI responses:** On 22 Sep 2026, Claude answered both letter-counting questions correctly (strawberry: 3, blueberry: 2). The screenshots appear in the video with the macOS clock visible.
- **The boundary (what this does not establish):** Tokenization explains why letter-counting is *unreliable*. It does not establish that a model gets the answer wrong today, and my own test shows it getting it right. I also do not claim to know how Claude produced its correct answers.
- **Tokenizer caveat:** All token numbers come from `cl100k_base` (GPT-4's tokenizer), not Claude's. The phenomenon carries over, but the exact pieces would differ.
- **Labelled on screen:** In B06, "straw / ber / ry" is Claude's verbal grouping of the letters. It is shown with no token IDs and a "not tokenizer output" label.

## Folder contents

| File | Purpose |
|---|---|
| `token-not-word.mp4` | The rendered video |
| `beat_sheet.json` | Reviewed narration and visual plan (the source of truth for the build) |
| `BUILD-PROMPT.md` | The prompts and commands that rebuilt it |
| `SOURCES.md` | Tools, what I made, what Claude contributed, licences |
| `FRICTIONAL.md` | Dated log of what broke and what I did |
| `scenes.py` | Hand-authored Manim scenes, one class per beat |
| `FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md` | Citations for every on-screen number, the shot work order, and the open-slot prompts (required by the toolkit's Gate F) |
| `media/B05-claude-strawberry.png`, `media/B05-claude-blueberry.png` | The two real Claude screenshots used in B05 |

## How to rebuild

1. Clone the toolkit, then set up its environment:

   ```bash
   git clone https://github.com/nikbearbrown/brutalist.art
   cd brutalist.art
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   pip install tiktoken==0.14.0
   ```

   You also need:

   - ffmpeg/ffprobe and Manim 0.18.1.
   - LaTeX: TeX Live or MacTeX, including `dvisvgm`. Manim uses it to typeset the live counters in B01 and B03.
   - The Kokoro model files (`kokoro-v1.0.onnx` and `voices-v1.0.bin`, about 350 MB). Run `./setup --install` from the toolkit root: it downloads them if missing, installs the Python dependencies, and checks every dependency, including a real Kokoro test phrase.

   All of them run locally and free, with no API keys.

2. Copy this folder into the toolkit at `youtube/brutalist/token-not-word/`.

3. Optionally, reproduce the token numbers:

   ```bash
   python3 - <<'PY'
   import tiktoken
   enc = tiktoken.get_encoding("cl100k_base")
   for w in ["strawberry", " strawberry", "unbelievable", "raspberry", "Thank you!"]:
       ids = enc.encode(w)
       print(repr(w), len(w), ids, [enc.decode([i]) for i in ids])
   PY
   ```

4. Generate narration first, because the audio durations drive all the timing. Then render:

   ```bash
   python3 runtime/scripts/generate_audio_kokoro.py youtube/brutalist/token-not-word
   ./art run youtube/brutalist/token-not-word      # review cut
   ./art final youtube/brutalist/token-not-word    # 4K master
   ```

## GitHub

Posted at `fall-2026/tushar-p/week-01-video/` in https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai. The assignment text says `fall-2025/`; I used the `fall-2026/` folder that already exists for me in the course repo.
The final commit hash is in the Canvas submission.
