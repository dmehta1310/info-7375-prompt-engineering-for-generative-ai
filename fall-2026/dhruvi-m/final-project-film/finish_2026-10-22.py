#!/usr/bin/env python3
"""finish_2026-10-22.py: copy the re-rendered film and its paperwork into the submission folder,
and add revision notes (drafted by Claude in chat, run by Dhruvi). FRICTIONAL.md is NOT touched:
Dhruvi writes that entry herself."""
import shutil, subprocess, re
from pathlib import Path
H = Path.home() / "Documents/final-project-film"
R = H / "dhruvi/youtube/ghost-job-radar-pitch"
S = H / "submission/final-project-film"
master = R / "exports/landscape/ghost-job-radar-pitch.mp4"
def probe(args):
    return subprocess.run(["ffprobe", "-v", "error"] + args + [str(master)], capture_output=True, text=True).stdout.strip()
wh = probe(["-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0"])
dur = float(probe(["-show_entries", "format=duration", "-of", "csv=p=0"]))
mb = master.stat().st_size / 1e6
print(f"master: {wh}, {dur:.1f} s, {mb:.1f} MB")
assert wh == "3840,2160" and dur < 240 and mb < 95, "master check failed, stopping"
shutil.copy2(master, S / "ghost-job-radar-pitch.mp4")
for f in ["make_sheet.py", "scenes.py", "beat_sheet.json", "FACTCHECK.md", "SHOTLIST.md", "PEDAGOGY.md"]:
    shutil.copy2(R / f, S / f)
g = S / "gate-reports/2026-10-22-revision"; g.mkdir(parents=True, exist_ok=True)
pairs = [(H / "art-run-2026-10-22.log", "art-run_1_reused-stale-clips_NOT-USED.log"),
         (H / "art-run-2026-10-22-v2.log", "art-run_2_fresh-render_all-gates.log"),
         (H / "art-final-2026-10-22.log", "art-final_GATE-T-PASS.log"),
         (R / "TYPECHECK.md", "gate-T_TYPECHECK.md"), (R / "_qc/REPORT.md", "gate-V_REPORT.md"),
         (R / "layout_audit.md", "gate-B_layout_audit.md"), (R / "qc-sheet.png", "qc-sheet_contact.png")]
for src, name in pairs:
    if src.exists(): shutil.copy2(src, g / name)
    else: print("missing (skipped):", src)
ap = Path.home() / "Downloads/apply_2026-10-22.py"
if ap.exists(): shutil.copy2(ap, S / "apply_2026-10-22.py")
shutil.copy2(Path(__file__), S / "finish_2026-10-22.py")
def append(name, text):
    p = S / name; p.write_text(p.read_text().rstrip() + "\n\n" + text.strip() + "\n"); print("appended:", name)
append("README.md", f"""## Revision 2026-10-22 (after TA feedback)
- Runtime is now {dur:.1f} s (about {int(dur//60)}:{int(dur%60):02d}), 3840x2160.
- Changes: narrator says who she is; plain-language terms; real findings added (live Stripe check from the Mode Build, the 'uncertain' result, Stripe's four filing names, the six-plus-years posting); 'Planned' tags on B02, B04, B09, B10.
- To rebuild this version: run `python3 apply_2026-10-22.py` on the 2026-10-10 reel, re-run `make_sheet.py`, regenerate audio, pad BOUT with 1.0 s of silence, move the old clips aside, then `art run` and `art final` (exact commands in BUILD-PROMPT.md).""")
append("BUILD-PROMPT.md", """## Revision 2026-10-22 (done by hand; Claude Code was unavailable)
Run from ~/Documents/final-project-film unless noted.
```
python3 ~/Downloads/apply_2026-10-22.py                       # narration, card text, 'Planned' tags, revision notes
cd dhruvi/youtube/ghost-job-radar-pitch && python3 make_sheet.py
cd ~/Documents/final-project-film && python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py dhruvi/youtube/ghost-job-radar-pitch
cd dhruvi/youtube/ghost-job-radar-pitch
cp mp3/beat-BOUT.mp3 _superseded/2026-10-22/beat-BOUT-unpadded.mp3
ffmpeg -y -loglevel error -i _superseded/2026-10-22/beat-BOUT-unpadded.mp3 -af "apad=pad_dur=1.0" -c:a libmp3lame -q:a 2 mp3/beat-BOUT.mp3
python3 make_sheet.py
# art run reuses existing clips, so move the changed beats' renders aside first:
D=_superseded/2026-10-22/render-old; mkdir -p $D/manim $D/media $D/clips
for b in B02 B03 B04 B05 B08 B09 B10 B11; do mv manim/$b.mp4 $D/manim/; done
for b in BIDEA BDEFS B06 B12; do mv media/$b.mp4 $D/media/; done
for b in BIDEA BDEFS B02 B03 B04 B05 B06 B08 B09 B10 B11 B12; do mv clips/$b.mp4 $D/clips/; done
mv media/videos $D/media-videos-cache
python3 make_sheet.py
cd ~/Documents/final-project-film && export PATH="$HOME/Documents/final-project-film/.venv/bin:$PATH"
./brutalist.art/art run dhruvi/youtube/ghost-job-radar-pitch --height 2160
./brutalist.art/art final dhruvi/youtube/ghost-job-radar-pitch --height 2160 --out dhruvi/youtube/ghost-job-radar-pitch/exports/landscape
python3 ~/Downloads/finish_2026-10-22.py                      # copies the master and paperwork into the submission folder
```""")
append("SOURCES.md", "- 2026-10-22 revision: Claude (chat) drafted the revised narration, which I read and approved, and wrote apply_2026-10-22.py and finish_2026-10-22.py. I ran every command myself, listened to the new audio, and watched the new cut.")
b = S / "PROJECT-BRIEF.md"; t = b.read_text()
if "## Will exist" in t and "2026-10-19" not in t:
    t = t.replace("## Will exist", "- A live liveness run with the class engine (npm run ats:liveness) on one real Stripe posting, plus a made-up job number that came back 'uncertain' (2026-10-19, Reallocation Engine PR #57, which replaces PR #1)\n\n## Will exist", 1)
    b.write_text(t); print("PROJECT-BRIEF.md: added the 2026-10-19 live run to 'Exists today'")
else:
    print("PROJECT-BRIEF.md: left unchanged (check it by hand)")
hits = [str(p.relative_to(S)) for p in S.rglob("*") if p.is_file() and p.suffix in (".md", ".json", ".txt", ".log", ".py")
        and re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", p.read_text(errors="ignore"))]
print("files containing an email-like string:", hits or "none")
print("DONE. Now add your own FRICTIONAL.md entry.")
