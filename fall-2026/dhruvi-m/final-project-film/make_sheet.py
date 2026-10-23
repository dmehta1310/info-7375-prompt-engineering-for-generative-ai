#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for the Ghost-Job Trust Radar pitch film (show-tell).

Narration, pictures and labels come word for word from plan/BEAT-PLAN.md.
Assignment overrides applied: voice af_bella, narrator is Dhruvi Mehta, no instructor persona,
no instructor handle or portraits, no Claude answer anywhere (the composer shows a prompt only).
B06 data rows are the real lines saved in pantry/evidence/tests-2026-10-10.txt.
"""
import json
import subprocess
from pathlib import Path
HERE = Path(__file__).resolve().parent
SLUG = "ghost-job-radar-pitch"
TITLE = "Ghost-Job Trust Radar"
NAME = "Dhruvi Mehta"
VOICE = "af_bella"

def est(narration):
    return round(len(narration.split()) / 2.5, 1)

def beat(bid, narration, cls, image, show):
    return {"beat_id": bid, "act": "show-tell", "lane": "manim", "proof_gate": "SHOW",
            "narration_text": narration, "estimated_duration_s": est(narration),
            "voice": VOICE, "engine": "kokoro",
            "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": image, "show": show, "manim": {"class": cls},
                     "motion_claim": image}}

def remotion(bid, act, narration, pattern, props, show, gate="SHOW", **extra):
    b = {"beat_id": bid, "act": act, "lane": "bookend", "proof_gate": gate,
         "narration_text": narration, "estimated_duration_s": est(narration),
         "voice": VOICE, "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": show, "remotion": {"pattern": pattern, "props": props}}}
    b.update(extra)
    return b

def card(bid, narration, props, show, motion_claim):
    props = dict(props, durationSeconds=max(2, est(narration)))
    return remotion(bid, "show-tell", narration, "ShowTellCard", props, show, gate="CARD",
                    lane="card", motion_claim=motion_claim)

OPEN = [
 remotion("BIDEA", "the question",
    "Hi, I'm Dhruvi Mehta, an international master's student in Information Systems at Northeastern. My final project is Ghost-Job Trust Radar: it checks whether a job ad is still real and fits a student's visa timeline, before they spend time on it. If something already ran, I'll show it. Everything else is a plan.",
    "BrutalistHesitantWriter",
    {"text": "Is this job worth applying to?", "triggerWords": "worth applying to",
     "replacementWords": "live and CPT-feasible",
     "fontSize": 70, "charMs": 22, "hesitateBetween": 6, "hesitateWithin": 1, "mistakeRate": 2, "jitter": 20,
     "seed": SLUG, "banner": ""},
    [{"at": 0.0, "event": "types 'Is this job worth applying to?'"}, {"at": 0.6, "event": "backspaces 'worth applying to' and retypes 'live and CPT-feasible'"}],
    lead_silence_s=0.8, motion_claim="CONSTRUCTED. The writer types the naive question and corrects it to 'live and CPT-feasible'.",
    qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer bookend: the correction is the motion."}),
 remotion("BDEFS", "terms",
    "Four terms. CPT: permission for an international student to work during their degree. A ghost job: an ad that's already filled, or never really open. Liveness: is the ad still taking applications? A sponsor record: proof a company sponsored work visas before.",
    "ClaudeDefinitions",
    {"title": "Terms In This Film",
     "terms": [{"term": "CPT", "meaning": "permission to work during the degree"},
               {"term": "Ghost job", "meaning": "an ad that's already filled, or never really open"},
               {"term": "Liveness", "meaning": "is the ad still taking applications?"},
               {"term": "Sponsor record", "meaning": "proof a company sponsored work visas before"}],
     "folderLabel": "", "meaningSize": 54},
    [{"at": 0.1, "event": "'CPT' lands"}, {"at": 0.35, "event": "'Ghost job' lands"}, {"at": 0.6, "event": "'Liveness' lands"}, {"at": 0.8, "event": "'Sponsor record' lands"}], gate="CARD",
    qc={"sparse_by_design": True, "sparse_reason": "TERMS card: four prerequisites, one line each."}),
]

B = [
 beat("B01", "An international student on CPT finds a data analyst posting and spends an hour researching the company. Then she learns it was already filled, or the start date doesn't fit her CPT window. That hour is gone.",
      "B01_Problem", "CONSTRUCTED. A posting box on a desk; browser tabs stack up beside it; then the posting box greys out. Labels: 'Posting', '1 hour'.",
      [{"at": 0.1, "event": "posting box on desk, label 'Posting'"}, {"at": 0.4, "event": "tabs stack up, label '1 hour'"}, {"at": 0.75, "event": "posting box greys out"}]),
 beat("B02", "Ghost-Job Trust Radar will be a command-line tool: one command, three checks, like a checkpoint for a job ad. Is it open? Does the timeline fit CPT? Has the company sponsored before? It will live in a GitHub repository with tests and an evaluation log.",
      "B02_Gates", "CONSTRUCTED. A conveyor carries the posting box through three gates into a report. Labels: 'Live?', 'CPT fit?', 'Sponsor record?'. A 'Planned' tag in the corner (2026-10-22).",
      [{"at": 0.2, "event": "conveyor and three gates, labels"}, {"at": 0.5, "event": "box rides through each gate"}, {"at": 0.85, "event": "report lands"}]),
 beat("B03", "I checked two alternatives myself. On MyVisaJobs, Stripe appears under four company names, and nothing says whether a posting is still open. Checking one posting by hand took me three tabs and twenty minutes, and left no record except my own screenshots.",
      "B03_Alternatives", "CONSTRUCTED. Two stations: a database cabinet and a desk of scattered tabs. Labels: 'MyVisaJobs', 'Manual check'.",
      [{"at": 0.15, "event": "cabinet, label 'MyVisaJobs'"}, {"at": 0.55, "event": "scattered tabs, label 'Manual check'"}]),
 beat("B04", "Mine will ask the cheapest question first: is the ad still open? I already ran my class engine's live check on a real Stripe posting, and it came back active. A made-up job number came back 'uncertain', not 'dead', so anything except 'active' will stop the check.",
      "B04_StopEarly", "CONSTRUCTED. The conveyor again; the first gate turns red and the later gates go dim. Then a report box with a tag. Labels: 'Stop early', 'No record'. A 'Planned' tag in the corner (2026-10-22).",
      [{"at": 0.2, "event": "first gate turns red, label 'Stop early'"}, {"at": 0.4, "event": "later gates dim"}, {"at": 0.75, "event": "report box with tag, label 'No record'"}]),
 beat("B05", "My reader is a hiring manager for a data analyst role. In sixty seconds, they'll run one command on a sample posting and see where every answer came from. This picture is a mock-up.",
      "B05_Reader", "CONSTRUCTED. A person at a laptop; a README sheet, one command, a report with a source tag on each line. A 'Constructed' tag sits in the corner. Labels: 'Hiring manager', 'Constructed'.",
      [{"at": 0.15, "event": "person at laptop, label 'Hiring manager'"}, {"at": 0.45, "event": "README, command, report with source tags"}, {"at": 0.7, "event": "'Constructed' tag"}]),
 card("B06", "Here's what exists. I built two scripts: one checks the visa timeline, one pulls sponsorship history from the class data. Sixteen automatic tests pass, and I checked one run by hand against the raw data.",
      {"kind": "focus", "heading": "Real output · 2026-10-10",
       "items": [{"label": "Ran 6 tests in 0.003s", "value": "OK", "sub": ""},
                 {"label": "Ran 10 tests in 0.002s", "value": "OK", "sub": ""},
                 {"label": "total (6 + 10)", "value": "16", "sub": ""}],
       "focus": 2, "valueFont": "Helvetica Neue, Arial, sans-serif"},
      [{"at": 0.1, "event": "first real line"}, {"at": 0.35, "event": "second real line"}, {"at": 0.6, "event": "total 16"}],
      "REAL. The lens moves down the two real test lines from the 2026-10-10 run to the total, 16."),
 beat("B07", "Then I tried to break it, with a company that isn't in the dataset. It reported 'no record' instead of inventing an answer.",
      "B07_BreakTest", "REAL result, CONSTRUCTED drawing. A posting box for a company that isn't in the cabinet; the report shows a 'no record' tag instead of a made-up value. Labels: 'Not in data', 'No record'.",
      [{"at": 0.2, "event": "posting box beside the cabinet, label 'Not in data'"}, {"at": 0.6, "event": "report with tag, label 'No record'"}]),
 beat("B08", "What does this prove? Four course skills: checking results against the source, labeling where answers came from, testing how it fails, and writing rules it must follow. A reviewer could say my checks fail safely, but not yet that it's accurate on real postings.",
      "B08_Skills", "CONSTRUCTED. Four blocks light up one by one. Labels: 'Verify', 'Source', 'Evaluate'.",
      [{"at": 0.15, "event": "block 1 lights, label 'Verify'"}, {"at": 0.4, "event": "block 2 lights, label 'Source'"}, {"at": 0.65, "event": "block 3 lights, label 'Evaluate'"}, {"at": 0.85, "event": "block 4 lights"}]),
 beat("B09", "What's out: it won't say whether to apply, or give legal advice, and it doesn't read experience levels yet; the Stripe posting I tested asks for six-plus years. First, one command will run every check on a synthetic posting and save a report, a test, and a dated run log.",
      "B09_InOutFirst", "CONSTRUCTED. A crossed-out 'apply?' sign, then one command running a single synthetic posting into a report and a log. Labels: 'Not advice', 'First run'. A 'Planned' tag in the corner (2026-10-22).",
      [{"at": 0.15, "event": "'apply?' sign crossed out, label 'Not advice'"}, {"at": 0.5, "event": "command runs one posting"}, {"at": 0.8, "event": "report and log appear, label 'First run'"}]),
 beat("B10", "The biggest risk: the sponsorship data is an incomplete, historical sample, so 'no record' could be misread as 'doesn't sponsor.' Every lookup will print the data's date range next to the answer.",
      "B10_Misread", "CONSTRUCTED. A 'no record' tag with an arrow to 'doesn't sponsor', crossed out; a date-range tag clips on beside it. Labels: 'Misread', 'Date range'. A 'Planned' tag in the corner (2026-10-22).",
      [{"at": 0.2, "event": "arrow from 'no record' to 'doesn't sponsor', label 'Misread'"}, {"at": 0.45, "event": "arrow crossed out"}, {"at": 0.75, "event": "date-range tag clips on, label 'Date range'"}]),
 beat("B11", "Why this project? It's a problem I live with as an international student. Python and data cleaning I already have, with my scripts as evidence; prompt contracts and evaluation logs are new to me.",
      "B11_Shelves", "CONSTRUCTED. Two shelves: one with tools I already have, one with new boxes being added. Labels: 'Already have', 'Learning'.",
      [{"at": 0.2, "event": "shelf of tools, label 'Already have'"}, {"at": 0.6, "event": "new boxes added, label 'Learning'"}]),
 card("B12", "So, where things stand. Today: two scripts, sixteen passing tests, a break test, and one live check on a real posting, in an open pull request. Still to build: one command, name matching, and an evaluation log. This film doesn't show it works on real postings in general.",
      {"kind": "tabs", "labels": ["Exists", "Will exist"],
       "items": [{"label": "2 scripts, 16 tests", "value": "", "sub": ""},
                 {"label": "Break test", "value": "", "sub": ""},
                 {"label": "Live run + open PR", "value": "", "sub": ""}],
       "items2": [{"label": "One command", "value": "", "sub": ""},
                  {"label": "Name matching", "value": "", "sub": ""},
                  {"label": "Evaluation log", "value": "", "sub": ""}],
       "cues": [0.55]},
      [{"at": 0.1, "event": "'Exists' panel rows"}, {"at": 0.55, "event": "tab slides to 'Will exist'"}],
      "CONSTRUCTED. The tab switches from what exists today to what will exist."),
]

SPARSE_REASON = ("show-tell style: one drawn object or scene on a cream stage per beat, minimal labels, with the voice carrying the explanation. The negative space is the style, so only underfill and clustered are waived; edge-bleed, empty-frame and contrast still apply.")
for b in B:
    if b["lane"] == "manim":
        b["qc"] = {"sparse_by_design": True, "sparse_reason": SPARSE_REASON}

YT_PROMPT = ("Before researching your next posting: is it still accepting applications, and does the start date fit your work window? "
             "Note where each answer came from.")
YOURTURN = remotion("BHTF", "your turn",
    "Your turn. " + YT_PROMPT,
    "ClaudeComposerAsk",
    {"greeting": "Your turn.", "topic": "YOUR TURN", "tag": "Constructed", "segment": "Check A Posting", "command": YT_PROMPT,
     "runningText": "paste this into Claude…",
     "output": ["Still live?", "Start date fits?"],
     "folderLabel": NAME, "modelLabel": "", "effortLabel": "", "largeText": True},
    [{"at": 0.0, "event": "Composer opens, 'Your turn.'"}, {"at": 0.1, "event": "the prompt types in full"}, {"at": 0.8, "event": "two check lines land"}],
    motion_claim="CONSTRUCTED. Prompt only; no Claude answer is shown. The two output lines are the viewer's own checks.")

B = OPEN + B + [YOURTURN]
BOUT_NARRATION = f"{TITLE}. {NAME}."
B.append({"beat_id": "BOUT", "act": "outro", "lane": "bookend", "proof_gate": "SHOW",
          "narration_text": BOUT_NARRATION, "estimated_duration_s": 4.0, "voice": VOICE, "engine": "kokoro",
          "shot": {"type": "REMOTION", "source": "own", "show": [{"at": 0.0, "event": "title restates; name; mascot"}],
                   "remotion": {"pattern": "ClaudeTitleOutro", "props": {"title": TITLE, "slug": SLUG, "handle": NAME, "subline": ""}}},
          "kind": "outro_voice", "tail_silence_s": 1.0})

def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True, check=True).stdout.strip()
    return round(float(out), 2)

for b in B:
    mp3 = HERE / "mp3" / f"beat-{b['beat_id']}.mp3"
    if mp3.exists():
        b["audio_file"] = f"mp3/beat-{b['beat_id']}.mp3"
        b["actual_duration_s"] = probe(mp3)
        props = b["shot"].get("remotion", {}).get("props", {})
        if b["beat_id"] == "BDEFS" or props.get("kind") in ("focus", "tabs"):
            props["durationSeconds"] = b["actual_duration_s"]

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "JOB SEARCH · CPT", "skill": "show-tell", "style_preset": "show-tell",
    "channel": "dhruvi-mehta", "channel_title": NAME, "voice": VOICE, "voice_kokoro": VOICE, "engine": "kokoro",
    "clock": "narration", "palette": "claude", "register": "Plain", "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160,
    "caption_policy": "none", "greeting_language": "English (narrator introduces herself)",
    "bookend_exempt": ["cold-open", "bvdt"],
    "bookend_exempt_reason": "show-tell style: opens on the hesitant writer + terms card, no verdict card; Your Turn is the composer showing a prompt only; spoken outro stays.",
    "audience": "a hiring manager for a data analyst role",
    "source_doc": "plan/PROJECT-BRIEF.md; pantry/evidence/tests-2026-10-10.txt; pantry/evidence/break-test-2026-10-10.txt",
    "playlist": "INFO7375 Final Project Pitch", "chapter_number": 0,
    "tags": ["Ghost-Job Trust Radar", "CPT", "international students", "job search", "data analyst", "Dhruvi Mehta"]},
    "beats": B}
(HERE / "beat_sheet.json").write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
print(len(B), "beats; est", round(sum(b["estimated_duration_s"] for b in B)), "s")
if all("actual_duration_s" in b for b in B):
    print("measured", round(sum(b["actual_duration_s"] for b in B), 2), "s")
