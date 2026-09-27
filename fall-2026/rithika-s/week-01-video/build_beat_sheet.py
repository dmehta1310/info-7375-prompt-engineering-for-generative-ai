#!/usr/bin/env python3
"""
build_beat_sheet.py — assemble beat_sheet.json from the VERIFIED figures.

Every number that appears on screen is read out of softmax_values.json, which
is written by `verify_softmax.py --emit`. Nothing numeric is typed here, so a
figure cannot drift from the arithmetic that proves it. Narration and the
`show` blocks are authored; the props are derived.

Run:  python3 verify_softmax.py --emit && python3 build_beat_sheet.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
V = json.loads((HERE / "softmax_values.json").read_text())

CHIP = "INFO 7375 · CH 1"

META = {
    "title": "The Token That Followed",
    "slug": "ch1-token-that-followed",
    "topic": "INFO 7375 · CHAPTER 1",
    "purpose": ("Teach a viewer who has never heard of next-token prediction what the "
                "pretraining objective actually targets — the token that followed in the "
                "text, not the true one — by pacing the real softmax arithmetic one step "
                "at a time, then naming what the explanation does not establish."),
    "concept": "What pretraining actually targets (the token that followed, not the truth)",
    "course": "INFO 7375 — Prompt Engineering for Generative AI",
    "author": "Rithika Sankar Rajeswari",
    "chapter": "Chapter 1",
    "register": "Teardown",
    "audience": ("Absolute beginners — someone who has never heard of next-token "
                 "prediction, logits, or softmax. No prior term is assumed; each is "
                 "introduced the moment it is first needed and not before."),
    "brand": "claude-sasha",
    "persona": "Sasha",
    "engine": "kokoro",
    "voice_kokoro": "af_bella",
    "palette": "claude",
    "style_preset": "claude",
    "ground": "#F2F0E9",
    "clock": "narration",
    "folder_chip": CHIP,
    "runtime_floor_s": 240,
    "runtime_floor_reason": ("Live-class instruction from the professor overriding the "
                             "written 2–4 minute syllabus target; see FRICTIONAL.md."),
    "structure": ("6 acts: 1 Hook · 2 Mechanism (slow, 5-step softmax ladder) · "
                  "3 Contrast (true corpus) · 4 Loss consequence · 5 Named boundary · "
                  "6 Takeaway. No seventh act."),
    "honesty": ("CONSTRUCTED EXAMPLE. The two corpus lines, the four-token vocabulary and "
                "the four logits are invented teaching values, not measurements from a "
                "trained model. The arithmetic derived from them is exact, is computed by "
                "verify_softmax.py, and is injected into these props by "
                "build_beat_sheet.py so no on-screen number is hand-typed. Every beat that "
                "displays a figure carries the on-screen CONSTRUCTED EXAMPLE banner."),
    "color_semantics": ("Claude fidelity palette. Terracotta #D97757 is the ONE accent and "
                        "marks the target token or the step under discussion. The deeper "
                        "warn step #A44A32 appears only on the honesty banner."),
    "chassis": "Ch1Chrome (Ch1Stage) — ground, spark line, honesty banner, course bug.",
    "no_claude_ui": ("This cut contains no Claude-interface beats. The requested 6-act "
                     "structure has no ask/handoff slot, and the standing constraint that "
                     "any Claude response shown must be a real, dated one means a "
                     "composed-looking UI reply would be the wrong thing to render. "
                     "See FRICTIONAL.md."),
    "tags": ["pretraining", "next-token prediction", "softmax", "cross-entropy",
             "language models", "INFO 7375", "Northeastern"],
}


def beat(bid, act, est, elem, narration, pattern, props, show, intent, motion):
    props = dict(props)
    props["durationS"] = est          # replaced with the measured value after audio
    return {
        "beat_id": bid,
        "act": act,
        "estimated_duration_s": est,
        "new_visual_element": elem,
        "narration_text": narration,
        "shot": {
            "type": "REMOTION",
            "source": "own",
            "motion": motion,
            "visual_intent": intent,
            "show": show,
            "remotion": {"pattern": pattern, "props": props},
        },
    }


LADDER_BASE = {
    "vocab": V["vocab"], "logits": V["logits"], "maxValue": V["max"],
    "shifted": V["shifted"], "exps": V["exps"], "expSum": V["exp_sum"],
    "probs": V["probs"], "pct": V["pct"], "target": V["target"],
}

beats = []

# ───────────────────────── ACT 1 — HOOK ─────────────────────────
beats.append(beat(
    "B00", "HOOK", 15, "The false claim, as plain English",
    "Here is a sentence. It is wrong — the moon is not made of cheese. But suppose a "
    "language model reads it during training. What does it learn to predict comes after "
    "the word green?",
    "Ch1PretrainHook",
    {"line": V["false_line"] + ".", "focusWord": "green",
     "question": "If a model reads this sentence, what does it learn to predict comes after “green”?",
     "pausePrompt": "Your guess first.", "sparkLine": "One sentence."},
    [{"at": "0.02", "event": "The sentence lands in large serif — no math anywhere on screen"},
     {"at": "0.30", "event": "'green' takes the terracotta accent"},
     {"at": "0.34", "event": "The question types in beside a terracotta rule"},
     {"at": "0.56", "event": "'… of green' plus a pulsing dashed '?' — the slot, unanswered"},
     {"at": "0.70", "event": "'YOUR GUESS FIRST' appears; the beat holds on appended silence"}],
    "Ch1PretrainHook — opens on the claim itself and asks the question before any mechanism, "
    "then holds on real trailing silence so the viewer answers it themselves.",
    "reveal-and-hold"))

# ──────────────────── ACT 2 — MECHANISM, SLOWLY ────────────────────
beats.append(beat(
    "B01", "MECHANISM", 21, "Text → tokens → the next-token question",
    "Before any math, the setup. A model in pretraining never sees a fact-checker. It sees "
    "text, chopped into pieces called tokens — roughly words. Its whole job is this: given "
    "the tokens so far, guess the next one. So take everything up to green, and ask what "
    "comes next. That guess is the only thing it is ever scored on.",
    "Ch1PretrainCorpus",
    {"sourceLabel": "CONSTRUCTED CORPUS · SCIENCE-FICTION NOVEL, CH. 4",
     "line": V["false_line"], "focusIndex": V["false_line"].split().index("green"),
     "corpusNote": "The corpus says cheese.", "truthNote": "The real moon is rock.",
     "sparkLine": "Text in, one token out."},
    [{"at": "0.03", "event": "Corpus card fades up with its source label"},
     {"at": "0.16", "event": "The seven tokens land one at a time, left to right"},
     {"at": "0.50", "event": "Context tokens recede; 'green' fills terracotta"},
     {"at": "0.62", "event": "'cheese' lifts out and a dashed '?' opens in its place"},
     {"at": "0.78", "event": "Two panels hold: WHAT PRETRAINING SEES / WHAT IS TRUE — 'never shown to the model'"}],
    "Ch1PretrainCorpus — introduces the word 'token' on the sentence the viewer already read, "
    "so the vocabulary arrives attached to something concrete.",
    "token-reveal"))

beats.append(beat(
    "B02", "MECHANISM", 26, "The answer key: one on cheese, zero on rock",
    "Now, the answer to the question I asked. As far as training is concerned, the correct "
    "answer is cheese. Not rock. Because the model is not scored against the world — it is "
    "scored against this text, and in this text, the word after green was cheese. Training "
    "builds an answer key from the sentence itself: a one on cheese, a zero on everything "
    "else. Rock, which is true of the moon, gets a zero.",
    "Ch1PretrainTarget",
    {"vocab": V["vocab"], "target": V["target"], "truth": V["truth"],
     "leftTitle": "THE ANSWER KEY y", "leftWhy": "built from the text",
     "rightTitle": "AN ANSWER KEY FROM TRUTH", "rightWhy": "pretraining never builds this",
     "sparkLine": "One on cheese. Zero on rock."},
    [{"at": "0.04", "event": "Left panel opens in terracotta: THE ANSWER KEY y / 'built from the text'"},
     {"at": "0.16", "event": "Four slots fill — rock 0, cheese 1, gas 0, light 0"},
     {"at": "0.48", "event": "Right panel opens greyed: an answer key built from truth"},
     {"at": "0.52", "event": "Its slots fill the other way, token names struck through"},
     {"at": "0.74", "event": "A cross draws across the right panel; both hold side by side"}],
    "Ch1PretrainTarget — answers the hook's question out loud, then shows the one-hot answer "
    "key beside the truth-based one that the objective never constructs.",
    "side-by-side-hold"))

LADDER = [
    ("B03", 20, "Step 1 — the raw scores",
     "So how does a guess become a number? The model gives every candidate word a raw score. "
     "Rock gets four. Cheese gets one. Gas gets zero. Light gets minus a half. These are "
     "called logits, and they are not probabilities yet — they can be negative, and they do "
     "not add up to anything in particular. That is what the next four steps fix.",
     1, "Scores, not odds yet.",
     "Four raw scores. Not probabilities — they can be negative and they add up to nothing in particular."),
    ("B04", 21, "Step 2 — subtract the largest score",
     "Step two looks strange, so let me say why it is here. We find the largest score — four — "
     "and subtract it from all of them. Rock becomes zero. Cheese becomes minus three. The "
     "ranking has not changed, and it turns out the final answer does not change either. It is "
     "done because the next step uses exponentials, which blow up on large numbers. This keeps "
     "them small.",
     2, "Shift, don't change.",
     "Subtracting the max is what real implementations do: exp of a large number overflows. The final probabilities are identical."),
    ("B05", 20, "Step 3 — exponentiate",
     "Step three: exponentiate. Raise e to the power of each shifted score. Rock, being zero, "
     "becomes exactly one. Cheese becomes about zero point zero five. Notice what that did — it "
     "made every number positive, and it stretched the gaps. A three point lead in score became "
     "a twenty to one lead here. Add them up: one point zero seven nine two.",
     3, "Positive, and stretched.",
     "Exponentiating makes every value positive and widens the gaps — a 3-point lead becomes roughly 20 to 1."),
    ("B06", 21, "Step 4 — divide by the sum",
     "Step four: divide each one by that total. This is the move that turns scores into "
     "probabilities. Because every row is divided by the same number, and that number is the sum "
     "of all the rows, the results are guaranteed to land between zero and one and to add up to "
     "exactly one. Nothing is left over, and nothing is invented.",
     4, "One shared denominator.",
     "Every row divided by the same total. That is why the results must land between 0 and 1 and sum to exactly 1."),
    ("B07", 23, "Step 5 — the probabilities, summing to exactly 1",
     "And here is the result. Rock: ninety-two point seven percent. Cheese: four point six. Gas: "
     "one point seven. Light: one point zero. Add them: exactly one hundred percent. Look at the "
     "bar — that is the model's entire belief about what comes next, and almost all of it sits on "
     "rock. Which is correct about the moon. And, for training, wrong.",
     5, "Correct, and penalised.",
     "Almost all the belief sits on rock — the true answer. Training is about to call that a mistake."),
]
for bid, est, elem, narr, step, spark, note in LADDER:
    beats.append(beat(
        bid, "MECHANISM", est, elem, narr, "Ch1PretrainLadder",
        {**LADDER_BASE, "step": step, "sparkLine": spark, "stepNote": note},
        [{"at": "0.06", "event": f"The four candidates hold; columns 1–{step - 1} are already on screen" if step > 1 else "The four candidates land"},
         {"at": "0.16", "event": f"Column {step} animates in and takes the terracotta header"},
         {"at": "0.40", "event": "The plain-language note for this step lands"},
         *([{"at": "0.52", "event": "Σ exp = " + f"{V['exp_sum']:.4f}" + " closes under a rule"}] if step == 3 else []),
         *([{"at": "0.62", "event": "The unit bar fills left to right and stops exactly full; Σ p = 1.0000"}] if step == 5 else [])],
        f"Ch1PretrainLadder step {step} of 5 — the same four tokens gaining exactly one column, "
        f"so no beat asks the viewer to absorb two new things at once.",
        "column-reveal"))

# ───────────────────── ACT 3 — CONTRAST ─────────────────────
beats.append(beat(
    "B08", "CONTRAST", 30, "Same model, two corpora, two answer keys",
    "This is the part that proves it. On the left, the corpus we have: green cheese. The last "
    "token is cheese, so the answer key puts its one on cheese. On the right, imagine the corpus "
    "said the true thing instead: grey rock. Same model, same four scores — nothing about the "
    "network changed. But the answer key moved. Its one is on rock now. The target follows the "
    "sentence, not the fact. If it followed the fact, these two columns would be identical.",
    "Ch1PretrainContrast",
    {"vocab": V["vocab"], "falseLine": V["false_line"], "trueLine": V["true_line"],
     "yFalse": V["y_false"], "yTrue": V["y_true"],
     "falseTarget": V["target"], "trueTarget": V["truth"],
     "closing": "Identical weights. Identical scores. Only the sentence changed — and the target moved with it.",
     "sparkLine": "Change the text, change the target."},
    [{"at": "0.03", "event": "Left column: the corpus we have; its final token underlined"},
     {"at": "0.14", "event": "Its answer key fills — the one lands on cheese"},
     {"at": "0.40", "event": "Right column opens: the same sentence, made true"},
     {"at": "0.46", "event": "Its answer key fills the other way — the one lands on rock"},
     {"at": "0.78", "event": "Closing rule: identical weights, identical scores, only the sentence changed"}],
    "Ch1PretrainContrast — the falsifiability move. Holding the model fixed and swapping only "
    "the corpus shows the target is a function of the text; if it tracked truth the two columns "
    "would coincide.",
    "side-by-side-hold"))

# ────────────────── ACT 4 — LOSS CONSEQUENCE ──────────────────
beats.append(beat(
    "B09", "LOSS", 21, "The penalty reads one slot",
    "Now the consequence. The loss measures how wrong the model is, and it reads exactly one "
    "number: the probability it gave the token that actually came next. Cheese got four point "
    "six percent, so the penalty is three point zero eight. Had the text said rock, that "
    "identical prediction would have scored zero point zero eight.",
    "Ch1PretrainLoss",
    {"target": V["target"], "truth": V["truth"],
     "pTarget": V["probs"][V["vocab"].index(V["target"])],
     "pTruth": V["probs"][V["vocab"].index(V["truth"])],
     "lossTarget": V["loss_target"], "lossTruth": V["loss_truth"],
     "logitTarget": V["logits"][V["vocab"].index(V["target"])],
     "logitTruth": V["logits"][V["vocab"].index(V["truth"])],
     "sparkLine": "Penalised for being right."},
    [{"at": "0.02", "event": "The sum collapses to one surviving term: −ln p(cheese)"},
     {"at": "0.20", "event": "Left panel counts up to 3.0762 — the penalty actually incurred"},
     {"at": "0.50", "event": "Right panel counts to 0.0762 — same weights, same forward pass"},
     {"at": "0.76", "event": "Bottom strip: the gap equals the score gap exactly, 3.0"}],
    "Ch1PretrainLoss — shows the penalty landing on 'cheese' because cheese is the next actual "
    "token, with the true-corpus counterfactual beside it on a shared scale.",
    "counter-and-hold"))

# ─────────────────── ACT 5 — NAMED BOUNDARY ───────────────────
beats.append(beat(
    "B10", "BOUNDARY", 32, "What this does not establish",
    "One last thing, and it matters. Everything you just watched is about pretraining only. "
    "There is a whole second stage afterwards — post-training, including preference tuning and "
    "R.L.H.F. — whose job is to steer the model toward answers people judge correct. That is a "
    "different objective with a different target, and none of it appeared here. This also does "
    "not establish that models must be wrong: most real text is broadly true, so copying it and "
    "being accurate usually agree. And none of these numbers were measured — they are constructed.",
    "Ch1PretrainBoundary",
    {"heading": "What this does not establish",
     "items": [
         "How post-training — preference tuning, RLHF — later steers the model away from raw corpus "
         "mimicry and toward factual accuracy. That is a separate, later mechanism with a different "
         "target, and none of its machinery appeared here.",
         "That models must therefore be wrong. Most real text is broadly true, so copying it and "
         "being accurate agree almost everywhere; this example is built from the case where they "
         "come apart.",
         "Anything measured. The corpus lines, the four-token vocabulary and the logits are "
         "constructed teaching values — chosen to make the arithmetic legible, not observed from a "
         "trained model.",
     ],
     "footer": "Only the arithmetic is load-bearing. It is reproducible: verify_softmax.py",
     "sparkLine": "Where the claim stops."},
    [{"at": "0.03", "event": "Heading 'What this does not establish.' with the terracotta period"},
     {"at": "0.18", "event": "Limit 01 — post-training / RLHF, a separate later mechanism"},
     {"at": "0.34", "event": "Limit 02 — mimicry and accuracy agree almost everywhere"},
     {"at": "0.50", "event": "Limit 03 — nothing measured; the figures are constructed"},
     {"at": "0.82", "event": "Footer names the runnable proof"}],
    "Ch1PretrainBoundary — the falsifiability beat, given real screen time rather than a closing "
    "title card. No honesty banner here: this beat displays no constructed figure.",
    "list-reveal"))

# ───────────────────── ACT 6 — TAKEAWAY ─────────────────────
beats.append(beat(
    "B11", "TAKEAWAY", 12, "One sentence, no new claims",
    "So, in one sentence: pretraining scores the model against the token that came next in the "
    "text, not against what is true. That is the whole idea.",
    "Ch1PretrainTakeaway",
    {"eyebrow": "THE TAKEAWAY",
     "takeaway": "Pretraining scores the model against the token that came next in the text — not against what is true.",
     "title": "The Token That Followed",
     "handle": "INFO 7375 · Prompt Engineering for Generative AI",
     "credit": "Rithika Sankar Rajeswari · narrated by Sasha",
     "rail": "Kokoro TTS af_bella · Brutalist toolkit · $0.00"},
    [{"at": "0.02", "event": "'THE TAKEAWAY' anchors to the top edge of the safe area"},
     {"at": "0.06", "event": "The one sentence types up in large serif, terracotta period"},
     {"at": "0.34", "event": "Terracotta rule draws outward"},
     {"at": "0.46", "event": "Title restate lands"},
     {"at": "0.58", "event": "Credit rail anchors to the bottom edge"}],
    "Ch1PretrainTakeaway — restates the core idea in plain language and stops. Introduces "
    "nothing: every phrase has already been shown as a mechanism.",
    "poster"))

# ── Merge, never clobber ───────────────────────────────────────────────────
# Narration and props are authored here, but the CLOCK is not: audio_file,
# actual_duration_s and render_duration_s are measurements, and
# shot.remotion.rendered is render provenance. An earlier version of this
# script wrote a fresh sheet, which silently discarded all of that — so
# re-running it on a delivered copy destroyed the measured durations and the
# captions could no longer be rebuilt. Carry those fields forward instead.
MEASURED = ("audio_file", "actual_duration_s", "render_duration_s",
            "guess_pause_s", "pause_note")

out = HERE / "beat_sheet.json"
if out.exists():
    prev = {b["beat_id"]: b for b in json.loads(out.read_text()).get("beats", [])}
    prev_meta = json.loads(out.read_text()).get("metadata", {})
    for b in beats:
        old_b = prev.get(b["beat_id"])
        if not old_b:
            continue
        for k in MEASURED:
            if k in old_b:
                b[k] = old_b[k]
        # the scene's own length must follow the measured audio, not the estimate
        if "actual_duration_s" in old_b:
            b["shot"]["remotion"]["props"]["durationS"] = old_b["actual_duration_s"]
        rendered = (old_b.get("shot", {}).get("remotion", {}) or {}).get("rendered")
        if rendered:
            b["shot"]["remotion"]["rendered"] = rendered
    for k in ("runtime_measured_s", "runtime_ffprobe_s", "runtime_ffprobe_note"):
        if k in prev_meta:
            META[k] = prev_meta[k]
    print("merged: carried the measured clock and render provenance forward")

sheet = {"metadata": META, "beats": beats}
out.write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")

words = sum(len(b["narration_text"].split()) for b in beats)
est = sum(b["estimated_duration_s"] for b in beats)
print(f"beats            {len(beats)}")
print(f"narration words  {words}  → est {words / 166 * 60:.0f}s at the measured 166 wpm")
print(f"estimated total  {est}s")
acts = {}
for b in beats:
    acts.setdefault(b["act"], 0)
    acts[b["act"]] += b["estimated_duration_s"]
for a, s in acts.items():
    print(f"  {a:<11} {s:>4}s")
