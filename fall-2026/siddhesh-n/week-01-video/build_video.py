#!/usr/bin/env python3
"""Render the Week 1 beat sheet in an original INFO 7375 course-aligned style."""
from __future__ import annotations

import json
import math
import re
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"
W, H, FPS = 1280, 720, 20
WHITE, INK, GRAY = "#FFFFFF", "#33261E", "#707070"
RED, GOLD, LIGHT = "#C8102E", "#D48B00", "#F4F4F4"


def run(*args: str) -> None:
    subprocess.run(args, check=True)


def duration(path: Path) -> float:
    return float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path)
    ], text=True).strip())


def font(size: int, bold=False, serif=False, mono=False):
    family = "DejaVuSansMono" if mono else ("DejaVuSerif" if serif else "DejaVuSans")
    weight = "-Bold" if bold else ""
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{family}{weight}.ttf", size)


def ease(x):
    x = max(0.0, min(1.0, x))
    return x*x*(3-2*x)


def reveal(t, at, span=.12):
    return ease((t-at)/span)


def centered(d, x, y, text, fnt, fill=INK):
    box = d.textbbox((0, 0), text, font=fnt)
    d.text((x-(box[2]-box[0])/2, y-(box[3]-box[1])/2), text, font=fnt, fill=fill)


def box(d, bounds, label, value="", color=INK, fill=WHITE, thick=3):
    x1,y1,x2,y2=bounds
    d.rectangle(bounds, fill=fill, outline=color, width=thick)
    d.text((x1+18,y1+14), label, font=font(15,True), fill=GRAY)
    if value:
        centered(d,(x1+x2)/2,(y1+y2)/2+13,value,font(28,True),color)


def arrow(d,x1,y1,x2,y2,color=INK,width=4):
    d.line((x1,y1,x2,y2),fill=color,width=width)
    a=math.atan2(y2-y1,x2-x1)
    for q in (2.55,-2.55):
        d.line((x2,y2,x2+15*math.cos(a+q),y2+15*math.sin(a+q)),fill=color,width=width)


def base(beat,index,total,t):
    im=Image.new("RGB",(W,H),WHITE); d=ImageDraw.Draw(im)
    d.text((55,34),beat["title"],font=font(39,True,serif=True),fill=INK)
    d.text((57,88),beat["act"],font=font(18,True),fill=RED)
    d.text((1110,46),f"{index+1:02d} / {total:02d}",font=font(16,True,mono=True),fill=GRAY)
    d.line((55,125,W-55,125),fill="#D8D8D8",width=2)
    d.line((55,624,W-55,624),fill=GOLD,width=4)
    centered(d,W/2,663,beat["takeaway"],font(19),GRAY)
    d.rectangle((55,612,55+int((W-110)*t),616),fill=RED)
    return im,d


def draw_beat(d,b,t):
    if b=="B00":
        vals=["1","2","3"]
        for i,v in enumerate(vals):
            p=reveal(t,.08+i*.12); y=205+int((1-p)*55)
            box(d,(70+i*225,y,245+i*225,y+120),f"SCORE {i+1}",v,RED if i==2 else INK,LIGHT)
        if t>.44:
            arrow(d,760,265,860,265)
            box(d,(880,205,1190,325),"COURSE CODE","subtract max = 3",RED,WHITE,4)
        if t>.68:
            d.text((445,420),"Why change every number first?",font=font(30,True,serif=True),fill=INK)
            d.text((445,475),"We will show the calculation, the proof, and the boundary.",font=font(20),fill=GRAY)
        d.rectangle((865,540,1190,585),fill=WHITE,outline=GRAY,width=2)
        centered(d,1027,562,"SYNTHETIC VOICE · KOKORO af_bella",font(13,True),GRAY)

    elif b=="B01":
        items=[("1","EXPONENTIATE","exp(score)",RED),("2","ADD","sum weights",INK),("3","DIVIDE","weight / total",RED)]
        for i,(n,name,val,col) in enumerate(items):
            p=reveal(t,.08+i*.20); x=80+i*405; y=245+int((1-p)*45)
            box(d,(x,y,x+285,y+155),f"STEP {n} · {name}",val,col,LIGHT)
            if i<2 and p>.75: arrow(d,x+305,322,x+385,322)
        if t>.67:
            centered(d,640,510,"The outputs are positive and add to 1.",font(25,True),RED)

    elif b=="B02":
        d.rectangle((65,170,1215,565),fill="#FAFAFA",outline=INK,width=3)
        d.text((90,192),"ACTUAL RUN · course main.py",font=font(18,True),fill=RED)
        probs=[.09003057317038046,.24472847105479764,.6652409557748218]
        for i,pv in enumerate(probs):
            y=280+i*82; r=reveal(t,.14+i*.12)
            d.text((100,y),f"score {i+1}",font=font(21,True),fill=INK)
            d.rectangle((240,y,240+int(760*pv*r),y+38),fill=RED if i==2 else (INK if i==1 else "#A0A0A0"))
            d.text((1020,y+4),f"{pv:.17f}",font=font(17,mono=True),fill=INK)
        d.text((90,525),"Recorded 2026-09-26 · Python standard library · offline run",font=font(16),fill=GRAY)

    elif b=="B03":
        left=[1,2,3]; right=[-2,-1,0]; p=reveal(t,.22,.42)
        for i in range(3):
            y=185+i*128
            box(d,(75,y,300,y+86),f"ORIGINAL z{i+1}",str(left[i]),INK,LIGHT)
            arrow(d,330,y+43,865,y+43,RED,4)
            centered(d,600,y+29,"− 3",font(24,True,mono=True),RED)
            x=900+int((1-p)*170)
            box(d,(x,y,x+230,y+86),f"SHIFTED z{i+1}",str(right[i]),RED,WHITE,4)
        if t>.65:
            d.line((120,580,1060,580),fill=INK,width=3)
            centered(d,590,560,"gap 1                 gap 1",font(18,True,mono=True),GRAY)

    elif b=="B04":
        weights=[.1353352832366127,.36787944117144233,1.0]
        probs=[.09003057317038046,.24472847105479764,.6652409557748218]
        phase=reveal(t,.38,.30)
        d.text((85,165),"SHIFTED SCORES",font=font(17,True),fill=GRAY)
        d.text((860,165),"NORMALIZED PROBABILITIES",font=font(17,True),fill=GRAY)
        for i,(z,w,pv) in enumerate(zip([-2,-1,0],weights,probs)):
            y=235+i*115
            box(d,(70,y,250,y+74),f"z{i+1}",str(z),INK,LIGHT)
            arrow(d,280,y+37,410,y+37)
            h=int(90*w*reveal(t,.08+i*.08)); d.rectangle((430,y+64-h,555,y+64),fill=RED if i==2 else GRAY)
            d.text((575,y+24),f"{w:.6f}",font=font(17,mono=True),fill=INK)
            arrow(d,720,y+37,835,y+37,RED)
            width=int(300*pv*phase); d.rectangle((860,y+18,860+width,y+56),fill=RED if i==2 else GRAY)
            d.text((1100,y+24),f"{pv:.4f}",font=font(17,True,mono=True),fill=INK)
        if t>.7:
            centered(d,640,575,"weight total = 1.503215",font(22,True,mono=True),RED)

    elif b=="B05":
        stages=[("INPUT","[1000, 1000]",INK),("SHIFT −1000","[0, 0]",RED),("EXPONENTIATE","[1, 1]",INK),("NORMALIZE","[0.5, 0.5]",RED)]
        for i,(lab,val,col) in enumerate(stages):
            p=reveal(t,.05+i*.16); x=45+i*310; y=260+int((1-p)*50)
            box(d,(x,y,x+240,y+150),lab,val,col,LIGHT if i%2==0 else WHITE,4 if col==RED else 3)
            if i and p>.7: arrow(d,x-55,y+75,x-12,y+75)
        if t>.7:
            centered(d,640,520,"OFFICIAL TEST: test_main.py · test_02",font(20,True,mono=True),GRAY)

    elif b=="B06":
        d.text((125,185),"exp(zᵢ − m)",font=font(34,True,mono=True),fill=INK)
        d.line((105,235,495,235),fill=INK,width=4)
        d.text((95,270),"Σⱼ exp(zⱼ − m)",font=font(34,True,mono=True),fill=INK)
        if t>.28:
            arrow(d,535,240,650,240,RED,5)
            d.text((700,185),"exp(zᵢ) · exp(−m)",font=font(29,True,mono=True),fill=INK)
            d.line((685,235,1170,235),fill=INK,width=4)
            d.text((680,270),"exp(−m) · Σⱼ exp(zⱼ)",font=font(29,True,mono=True),fill=INK)
        if t>.58:
            d.rectangle((842,172,1004,220),outline=RED,width=5)
            d.rectangle((670,258,832,307),outline=RED,width=5)
            d.line((670,160,1008,320),fill=RED,width=7)
            centered(d,640,480,"THE SHARED exp(−m) FACTOR CANCELS",font(27,True),RED)
            centered(d,640,535,"same normalized ratios",font(22),GRAY)

    elif b=="B07":
        d.rectangle((60,175,585,540),fill="#F5F5F5",outline=INK,width=3)
        d.rectangle((695,175,1220,540),fill=WHITE,outline=RED,width=4)
        centered(d,322,220,"ESTABLISHES",font(19,True),INK)
        centered(d,957,220,"DOES NOT ESTABLISH",font(19,True),RED)
        centered(d,322,350,"Avoids unnecessarily large",font(24,True),INK)
        centered(d,322,390,"positive exponentials here",font(24,True),INK)
        for j,txt in enumerate(["The scores are correct","The likely token is true","Every extreme input is safe"]):
            y=300+j*76
            d.text((735,y),"×",font=font(30,True),fill=RED)
            d.text((785,y+3),txt,font=font(21,True),fill=INK)
        d.line((640,158,640,565),fill=GOLD,width=5)
        centered(d,640,590,"THE CLAIM BOUNDARY",font(16,True,mono=True),GRAY)


def render_beat(beat,index,total,audio,out):
    seconds=duration(audio)+.55
    cmd=["ffmpeg","-y","-hide_banner","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i",str(audio),"-vf","scale=1920:1080:flags=lanczos","-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-af","loudnorm=I=-16:TP=-1.5:LRA=8,apad=pad_dur=0.55","-t",f"{seconds:.3f}","-movflags","+faststart",str(out)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE); frames=math.ceil(seconds*FPS)
    try:
        for n in range(frames):
            t=n/max(1,frames-1); im,d=base(beat,index,total,t); draw_beat(d,beat["beat_id"],t); proc.stdin.write(im.tobytes())
    finally: proc.stdin.close()
    if proc.wait()!=0: raise RuntimeError(f"render failed: {beat['beat_id']}")
    return seconds


def srt_time(s):
    ms=round(s*1000); h,ms=divmod(ms,3600000); m,ms=divmod(ms,60000); sec,ms=divmod(ms,1000)
    return f"{h:02d}:{m:02d}:{sec:02d},{ms:03d}"


def make_srt(beats,timeline,out):
    cues=[]; n=1
    for beat,span in zip(beats,timeline):
        sentences=[x.strip() for x in re.split(r"(?<=[.!?])\s+",beat["narration_text"]) if x.strip()]
        weights=[max(1,len(x)) for x in sentences]; total=sum(weights); cur=span["start"]
        for sentence,w in zip(sentences,weights):
            end=cur+(span["end"]-span["start"])*w/total
            cues.append(f"{n}\n{srt_time(cur)} --> {srt_time(end)}\n{sentence}\n"); n+=1; cur=end
    out.write_text("\n".join(cues))


def main():
    if not shutil.which("ffmpeg"): raise SystemExit("FFmpeg is required")
    BUILD.mkdir(exist_ok=True); data=json.loads((ROOT/"beat_sheet.json").read_text()); beats=data["beats"]
    clips=[]; timeline=[]; cursor=0.0
    for i,beat in enumerate(beats):
        audio=ROOT/"mp3"/f"beat-{beat['beat_id']}.mp3"; clip=BUILD/f"{beat['beat_id']}-course-style.mp4"
        if not audio.exists(): raise SystemExit(f"Missing {audio}")
        sec=render_beat(beat,i,len(beats),audio,clip); clips.append(clip)
        timeline.append({"beat_id":beat["beat_id"],"start":round(cursor,3),"end":round(cursor+sec,3)}); cursor+=sec
    concat=BUILD/"concat-course-style.txt"; concat.write_text("".join(f"file '{p.as_posix()}'\n" for p in clips))
    output=ROOT/"Nikam_Siddhesh_INFO7375_Week01_Video.mp4"
    run("ffmpeg","-y","-hide_banner","-loglevel","error","-f","concat","-safe","0","-i",str(concat),"-c","copy","-movflags","+faststart",str(output))
    (BUILD/"timeline.json").write_text(json.dumps({"runtime_seconds":round(cursor,3),"beats":timeline},indent=2))
    make_srt(beats,timeline,ROOT/"Nikam_Siddhesh_INFO7375_Week01_Video.srt")
    print(f"WROTE {output} ({cursor:.2f} seconds)")


if __name__=="__main__": main()
