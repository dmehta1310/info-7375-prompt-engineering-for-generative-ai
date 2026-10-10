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
    "Hi, I'm Dhruvi Mehta, and this is my final project pitch: Ghost-Job Trust Radar. If something already ran, I'll show it. Everything else is a plan.",
    "BrutalistHesitantWriter",
    {"text": "Is this job worth applying to?", "triggerWords": "worth applying to",
     "replacementWords": "live and CPT-feasible",
     "fontSize": 70, "charMs": 22, "hesitateBetween": 6, "hesitateWithin": 1, "mistakeRate": 2, "jitter": 20,
     "seed": SLUG, "banner": ""},
    [{"at": 0.0, "event": "types 'Is this job worth applying to?'"}, {"at": 0.6, "event": "backspaces 'worth applying to' and retypes 'live and CPT-feasible'"}],
    lead_silence_s=0.8, motion_claim="CONSTRUCTED. The writer types the naive question and corrects it to 'live and CPT-feasible'.",
    qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer bookend: the correction is the motion."}),
 remotion("BDEFS", "terms",
    "Four terms. CPT: work authorization tied to a degree program. A ghost job: a posting that's already filled, or never really open. Liveness: whether it still accepts applications. A sponsorship record: a public filing showing a company sponsored a visa before.",
    "ClaudeDefinitions",
    {"title": "Terms In This Film",
     "terms": [{"term": "CPT", "meaning": "work authorization tied to a degree program"},
               {"term": "Ghost job", "meaning": "a posting that's already filled, or never really open"},
               {"term": "Liveness", "meaning": "whether it still accepts applications"},
               {"term": "Sponsor record", "meaning": "a public filing showing a company sponsored a visa before"}],
     "folderLabel": "", "meaningSize": 54},
    [{"at": 0.1, "event": "'CPT' lands"}, {"at": 0.35, "event": "'Ghost job' lands"}, {"at": 0.6, "event": "'Liveness' lands"}, {"at": 0.8, "event": "'Sponsor record' lands"}], gate="CARD",
    qc={"sparse_by_design": True, "sparse_reason": "TERMS card: four prerequisites, one line each."}),
]

B = [
 beat("B01", "An international student on CPT finds a data analyst posting and spends an hour researching the company. Then she learns it was already filled, or the start date doesn't fit her CPT window. That hour is gone.",
      "B01_Problem", "CONSTRUCTED. A posting box on a desk; browser tabs stack up beside it; then the posting box greys out. Labels: 'Posting', '1 hour'.",
      [{"at": 0.1, "event": "posting box on desk, label 'Posting'"}, {"at": 0.4, "event": "tabs stack up, label '1 hour'"}, {"at": 0.75, "event": "posting box greys out"}]),
 beat("B02", "Ghost-Job Trust Radar will be a command-line tool that checks the posting first. Is it live? Does the timeline fit CPT? Is there a sponsorship record? The finished artifact will be a GitHub repository with one command, tests, and an evaluation log.",
      "B02_Gates", "CONSTRUCTED. A conveyor carries the posting box through three gates into a report. Labels: 'Live?', 'CPT fit?', 'Sponsor record?'.",
      [{"at": 0.2, "event": "conveyor and three gates, labels"}, {"at": 0.5, "event": "box rides through each gate"}, {"at": 0.85, "event": "report lands"}]),
 beat("B03", "I looked at two alternatives. MyVisaJobs shows who sponsored before, but nothing I saw checks whether a posting is live or fits a CPT window. The manual checklist from career guides works, but it's four or five steps across tabs, with no record kept.",
      "B03_Alternatives", "CONSTRUCTED. Two stations: a database cabinet and a desk of scattered tabs. Labels: 'MyVisaJobs', 'Manual check'.",
      [{"at": 0.15, "event": "cabinet, label 'MyVisaJobs'"}, {"at": 0.55, "event": "scattered tabs, label 'Manual check'"}]),
 beat("B04", "Mine will check liveness first and stop if the posting is dead, before research starts. Every value will carry its source. If the data has nothing, it will say 'no record in this dataset,' never 'doesn't sponsor.'",
      "B04_StopEarly", "CONSTRUCTED. The conveyor again; the first gate turns red and the later gates go dim. Then a report box with a tag. Labels: 'Stop early', 'No record'.",
      [{"at": 0.2, "event": "first gate turns red, label 'Stop early'"}, {"at": 0.4, "event": "later gates dim"}, {"at": 0.75, "event": "report box with tag, label 'No record'"}]),
 beat("B05", "My reader is a hiring manager for a data analyst role. In sixty seconds, they'll open the README, run one command on a sample posting, and see every line's source. This picture is a mock-up.",
      "B05_Reader", "CONSTRUCTED. A person at a laptop; a README sheet, one command, a report with a source tag on each line. A 'Constructed' tag sits in the corner. Labels: 'Hiring manager', 'Constructed'.",
      [{"at": 0.15, "event": "person at laptop, label 'Hiring manager'"}, {"at": 0.45, "event": "README, command, report with source tags"}, {"at": 0.7, "event": "'Constructed' tag"}]),
 card("B06", "Here's what exists. Last assignment, I built a CPT timeline gate and a sponsorship-data builder. This is the real test run: sixteen offline tests pass. I also checked one run by hand against the raw data.",
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
 beat("B08", "It will show four course skills: verification, source grounding, evaluation, and prompt contracts. A reviewer could fairly conclude I build checks that fail safely, but not that it's accurate on real postings. That isn't tested yet.",
      "B08_Skills", "CONSTRUCTED. Four blocks light up one by one. Labels: 'Verify', 'Source', 'Evaluate'.",
      [{"at": 0.15, "event": "block 1 lights, label 'Verify'"}, {"at": 0.4, "event": "block 2 lights, label 'Source'"}, {"at": 0.65, "event": "block 3 lights, label 'Evaluate'"}, {"at": 0.85, "event": "block 4 lights"}]),
 beat("B09", "What's out: it won't tell anyone whether to apply, and it won't give legal or immigration advice. First, I'll make one command run every check on a synthetic posting. You'll know it ran because it writes a report, a test checks it, and a dated run log goes in the repo.",
      "B09_InOutFirst", "CONSTRUCTED. A crossed-out 'apply?' sign, then one command running a single synthetic posting into a report and a log. Labels: 'Not advice', 'First run'.",
      [{"at": 0.15, "event": "'apply?' sign crossed out, label 'Not advice'"}, {"at": 0.5, "event": "command runs one posting"}, {"at": 0.8, "event": "report and log appear, label 'First run'"}]),
 beat("B10", "The biggest risk: the sponsorship data is an incomplete historical sample, so someone could read 'no record' as 'doesn't sponsor.' So every lookup will print the dataset's date range next to the answer.",
      "B10_Misread", "CONSTRUCTED. A 'no record' tag with an arrow to 'doesn't sponsor', crossed out; a date-range tag clips on beside it. Labels: 'Misread', 'Date range'.",
      [{"at": 0.2, "event": "arrow from 'no record' to 'doesn't sponsor', label 'Misread'"}, {"at": 0.45, "event": "arrow crossed out"}, {"at": 0.75, "event": "date-range tag clips on, label 'Date range'"}]),
 beat("B11", "Why this project? It's a real problem for international students like me, and it's a mix: Python and data cleaning I already have, with last assignment's scripts as evidence. Prompt contracts and evaluation logs are new to me.",
      "B11_Shelves", "CONSTRUCTED. Two shelves: one with tools I already have, one with new boxes being added. Labels: 'Already have', 'Learning'.",
      [{"at": 0.2, "event": "shelf of tools, label 'Already have'"}, {"at": 0.6, "event": "new boxes added, label 'Learning'"}]),
 card("B12", "So, where things stand. Today: a recipe, two scripts, sixteen passing tests, and a break test, in an open pull request not yet reviewed. The single command, live check, and evaluation log come later. This film does not establish that the tool works on real postings.",
      {"kind": "tabs", "labels": ["Exists", "Will exist"],
       "items": [{"label": "Recipe + 2 scripts", "value": "", "sub": ""},
                 {"label": "16 tests pass", "value": "", "sub": ""},
                 {"label": "Break test + open PR", "value": "", "sub": ""}],
       "items2": [{"label": "One command", "value": "", "sub": ""},
                  {"label": "Live check", "value": "", "sub": ""},
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
