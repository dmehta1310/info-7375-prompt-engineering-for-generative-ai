"""Sync each rendered scene to its measured narration, then concatenate.
Audio is the master clock: video is padded (last frame held) or trimmed to match."""
import json, subprocess, os, glob

T = json.load(open("audio/timings.json"))
SCENES = {"B00": "B00_Title", "B01": "B01_TheGap", "B02": "B02_TwoKinds",
          "B03": "B03_HowBigIsANormalMiss", "B04": "B04_TenThousandSeeds",
          "B05": "B05_WhereSeedSevenLands", "B06": "B06_WhatThisDoesNotEstablish",
          "B07": "B07_Conclusion"}
os.makedirs("render/segments", exist_ok=True)

def vdur(p):
    r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
                        "-of","default=nw=1:nk=1",p], capture_output=True, text=True)
    return float(r.stdout.strip())

segs = []
print(f"{'beat':<6}{'video':>9}{'audio':>9}{'action':>18}")
for bid, scene in SCENES.items():
    v = f"render/videos/scenes/1080p60/{scene}.mp4"
    a = T["beats"][bid]["file"]
    A, V = T["beats"][bid]["duration_s"], vdur(v)
    pad = max(0.0, A - V)
    out = f"render/segments/{bid}.mp4"
    act = f"hold {pad:.2f}s" if pad > 0.01 else f"trim {V-A:.2f}s"
    print(f"{bid:<6}{V:>8.2f}s{A:>8.2f}s{act:>18}")
    vf = f"tpad=stop_mode=clone:stop_duration={pad:.3f}" if pad > 0.01 else "null"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",v,"-i",a,
                    "-filter_complex",f"[0:v]{vf},fps=30[v]",
                    "-map","[v]","-map","1:a","-t",f"{A:.3f}",
                    "-c:v","libx264","-preset","medium","-crf","18",
                    "-pix_fmt","yuv420p","-c:a","aac","-b:a","192k",out], check=True)
    segs.append(out)

with open("render/concat.txt","w") as f:
    for s in segs: f.write(f"file '{os.path.abspath(s)}'\n")

FINAL = "riya-k-expected-is-not-a-promise.mp4"
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0",
                "-i","render/concat.txt","-c","copy",FINAL], check=True)
print(f"\nwrote {FINAL}  {vdur(FINAL):.2f}s")
