"""scenes.py — Manim scenes for token-not-word.

Palette: cream #F2F0E9, ink #3D3929, terracotta #D97757 (ONE accent per scene).
Numbers appear on screen ONLY with their citation line (see FACTCHECK.md).
Every token id and count is cl100k_base via tiktoken 0.14.0 — GPT-4's
tokenizer, NOT Claude's. No slant=ITALIC on multi-word text (Pango collapses
spaces).

Layout law: Gate V samples each beat at 50% and 85% of its span and requires the
content bbox to cover >= 55% of the safe area. Every scene therefore reaches its
full-width steady state before the halfway mark and holds it to the end. The
top rail (_rail) spans x -6.0..6.0 to anchor that width.

Terracotta is applied ONLY via indexed set_color on already-built glyphs, never
as a Text(color=...) over cream — #D97757 on #F2F0E9 is 2.73:1 and would trip
Gate W's W2 contrast rule.
"""
import json
from pathlib import Path

from manim import *

BG   = ManimColor("#F2F0E9")   # claude cream
INK  = ManimColor("#3D3929")   # warm ink — all body text
ACC  = ManimColor("#D97757")   # terracotta — ONE accent per scene
SOFT = ManimColor("#6E6A57")   # secondary / muted text
CARD = ManimColor("#FFFFFF")   # white card surface

MEDIA = Path(__file__).resolve().parent / "media"
_SHEET = Path(__file__).resolve().parent / "beat_sheet.json"

try:
    _DUR = {b["beat_id"]: float(b.get("actual_duration_s")
                                or b.get("estimated_duration_s") or 0.0)
            for b in json.loads(_SHEET.read_text())["beats"]}
except (OSError, ValueError, KeyError):   # pre-audio authoring / Gate A mock
    _DUR = {}


def _hold(scene, beat_id, minimum=0.5, fade_out=0.0):
    """Audio-first tail: hold the composed frame until the scene is as long as
    its measured narration mp3. compile.py SLOWS a short clip to fit the beat
    (setpts, never a freeze), so a scene that runs short would ship as slow-mo.
    Matching the clock here keeps every beat at 1.0x.

    fade_out > 0 spends the LAST fade_out seconds of that same clock fading
    everything to the ground. The fade sits inside the measured mp3 — the
    pipeline has no silent-tail mechanism, and this does not invent one — so
    only use it where the mp3's own trailing silence covers the fade."""
    target = float(_DUR.get(beat_id) or 0.0)
    try:
        elapsed = float(scene.renderer.time)
    except Exception:                      # Gate A's mock has no renderer clock
        elapsed = 0.0
    scene.wait(max(target - elapsed - fade_out, minimum))
    if fade_out > 0 and scene.mobjects:
        scene.play(FadeOut(*scene.mobjects), run_time=fade_out)


# Pango quantises glyph advances when Text is built at a small point size:
# at font_size=20 "cl100k_base" renders as "cl 100k_bas e" and the space before
# a middot collapses. Building every Text at one large reference size and
# scaling it down to the size we actually want removes the quantisation — the
# same string at _TEXT_REF scaled to 20 is evenly spaced. Never pass a small
# font_size straight to Text in this file; go through _label / _mono.
_TEXT_REF = 96.0

# Resolved explicitly rather than via the generic "monospace" alias, which is
# not a real family (Pango has no lowercase entry) and is silently resolved —
# here to Menlo. Naming it removes the silent-fallback risk.
MONO = "Menlo"


def _label(text, size=22, color=None, weight=None):
    kw = {"font_size": _TEXT_REF, "color": color or INK}
    if weight:
        kw["weight"] = weight
    return Text(text, **kw).scale(size / _TEXT_REF)


def _mono(text, size=44, color=None):
    return Text(text, font=MONO, font_size=_TEXT_REF,
                color=color or INK).scale(size / _TEXT_REF)


def _rail(kicker, right=""):
    """Top rail: kicker left, optional right label, hairline rule at y=2.92."""
    g = VGroup()
    k = _label(kicker, size=15, color=SOFT)
    k.move_to([-6.0 + k.width / 2, 3.18, 0])
    g.add(k)
    if right:
        r = _label(right, size=15, color=SOFT)
        r.move_to([6.0 - r.width / 2, 3.18, 0])
        g.add(r)
    g.add(Line([-6.0, 2.92, 0], [6.0, 2.92, 0], color=SOFT, stroke_width=1.2))
    return g


def _cite(text):
    """Bottom citation rail. Single line — safe from Pango italic collapse."""
    t = _label(text, size=15, color=SOFT)
    t.move_to([0.0, -3.18, 0])
    return t


def _token_box(piece, tok_id, hi_idx=(), size=44, min_w=1.15):
    """One labeled token box: white card, mono glyphs, token ID beneath.
    hi_idx = indices of characters inside `piece` to stamp terracotta.

    tok_id None renders the card WITH NO ID LINE. That case is for a grouping
    that is not a tokenizer output (B06's top row, Claude's spoken
    straw/ber/ry): printing an id under it would assert it is a real token,
    which is false. Never pass a made-up id to fill the slot."""
    glyphs = _mono(piece, size=size)
    for i in hi_idx:
        glyphs[i].set_color(ACC)
    box = RoundedRectangle(
        corner_radius=0.10,
        width=max(glyphs.width + 0.62, min_w), height=1.22,
        color=SOFT, fill_color=CARD, fill_opacity=1.0, stroke_width=2.0,
    )
    glyphs.move_to(box.get_center())
    if tok_id is None or tok_id == "":
        return VGroup(box, glyphs)
    idl = _mono(str(tok_id), size=20, color=SOFT)
    idl.next_to(box, DOWN, buff=0.16)
    return VGroup(box, glyphs, idl)


def _boundaries(row):
    """Mid-x of each internal gap in a row of cards — where this split cuts."""
    return [ (float(row[i][0].get_right()[0]) + float(row[i + 1][0].get_left()[0])) / 2.0
             for i in range(len(row) - 1) ]


def _count_updater(tracker, x, y):
    """Keep an Integer pinned to its tracker and to its slot as digits grow."""
    def _update(mob):
        mob.set_value(int(round(tracker.get_value())))
        mob.move_to([x, y - 0.18, 0])
    return _update


def _counter(caption, x, y, size=54):
    """A live count-up readout. Returns (group, number, tracker) — play
    tracker.animate.set_value(n) to drive the number.

    NB: the count is driven by a ValueTracker + updater rather than by
    manim's decimal-change animation, which Gate A's mock manim does not
    define; the mock supports this idiom."""
    lbl = _label(caption, size=19, color=SOFT)
    num = Integer(0, font_size=size, color=INK)
    lbl.move_to([x, y + 0.62, 0])
    num.move_to([x, y - 0.18, 0])
    tracker = ValueTracker(0.0)
    num.add_updater(_count_updater(tracker, x, y))
    return VGroup(lbl, num), num, tracker


def _shot_slot(filename, caption, x, y, w=4.9, h=2.7):
    """A dated screenshot slot. Renders the real PNG once it is dropped into
    media/; until then it draws a labelled empty frame naming the file it wants,
    so the beat still renders and the open slot is visible in review."""
    path = MEDIA / filename
    if path.is_file():
        img = ImageMobject(str(path))
        # scale_to_fit_* (methods), not the .height/.width setters: ImageMobject
        # exposes height read-only under Gate A's mock manim, and the setter form
        # takes the whole scene down at pre-flight.
        img.scale_to_fit_height(h)
        if img.width > w:
            img.scale_to_fit_width(w)
        img.move_to([x, y, 0])
        frame = Rectangle(width=img.width + 0.14, height=img.height + 0.14,
                          color=SOFT, stroke_width=2.0)
        frame.move_to([x, y, 0])
        body = Group(frame, img)
    else:
        box = Rectangle(width=w, height=h, color=SOFT, fill_color=CARD,
                        fill_opacity=1.0, stroke_width=2.0)
        box.move_to([x, y, 0])
        tag = _label("SCREENSHOT SLOT", size=18, color=SOFT)
        tag.move_to([x, y + 0.32, 0])
        sub = _mono(filename, size=13, color=SOFT)
        sub.move_to([x, y - 0.36, 0])
        body = Group(box, tag, sub)
    cap = _label(caption, size=16, color=SOFT)
    cap.move_to([x, y - h / 2 - 0.44, 0])
    return Group(body, cap)


# ─────────────────────────────────────────────────────────────────────────────
#  B00_TenLetters — the question, and the word whole.
# ─────────────────────────────────────────────────────────────────────────────
class B00_TenLetters(Scene):

    def construct(self):
        self.camera.background_color = BG
        self.play(FadeIn(_rail("TOKEN, NOT WORD")), run_time=0.5)

        q = _label("how many r's in strawberry?", size=34, weight="BOLD")
        q.move_to([0.0, 1.95, 0])
        self.play(Write(q), run_time=1.0)

        word = _mono("strawberry", size=92)
        word.move_to([0.0, 0.25, 0])
        self.play(FadeIn(word), run_time=0.8)

        underline = Line([-3.55, -0.78, 0], [3.55, -0.78, 0],
                         color=ACC, stroke_width=3.0)
        self.play(Create(underline), run_time=0.7)

        you = _label("you see ten letters", size=25, color=SOFT)
        you.move_to([0.0, -1.45, 0])
        them = _label("to answer, the model first chops the word into pieces", size=22, color=SOFT)
        them.move_to([0.0, -2.25, 0])
        self.play(FadeIn(you), run_time=0.5)
        self.play(FadeIn(them), run_time=0.6)
        self.add(_cite("and those pieces are not letters"))
        _hold(self, "B00")


# ─────────────────────────────────────────────────────────────────────────────
#  B01_ThreeTokens — strawberry -> str / aw / berry, with the 10 -> 3 readout.
# ─────────────────────────────────────────────────────────────────────────────
class B01_ThreeTokens(Scene):

    def construct(self):
        self.camera.background_color = BG
        self.add(_rail("TOKEN, NOT WORD", "tiktoken 0.14.0"))

        word = _mono("strawberry", size=52)
        word.move_to([0.0, 2.05, 0])
        self.play(FadeIn(word), run_time=0.6)

        pieces = [("str", 496, ()), ("aw", 675, ()), ("berry", 15717, ())]
        boxes = VGroup(*[_token_box(p, t, h, size=52) for p, t, h in pieces])
        boxes.arrange(RIGHT, buff=1.05).move_to([0.0, 0.42, 0])
        self.play(TransformFromCopy(word, boxes), run_time=1.5)
        self.wait(1.6)

        chars_g, chars_n, chars_vt = _counter("characters in", -3.75, -2.05)
        toks_g, toks_n, toks_vt = _counter("tokens out", 3.75, -2.05)
        arrow = Arrow([-1.55, -2.23, 0], [1.55, -2.23, 0], color=ACC,
                      stroke_width=3.0, tip_length=0.24, buff=0)
        self.play(FadeIn(chars_g), FadeIn(toks_g), GrowArrow(arrow), run_time=0.7)
        self.play(chars_vt.animate.set_value(10),
                  toks_vt.animate.set_value(3), run_time=1.4)
        self.add(_cite("GPT-4 tokenizer · cl100k_base"))
        _hold(self, "B01")


# ─────────────────────────────────────────────────────────────────────────────
#  B02_ScatteredRs — the three r's light up: str(1), aw(0), berry(2).
# ─────────────────────────────────────────────────────────────────────────────
class B02_ScatteredRs(Scene):

    def construct(self):
        self.camera.background_color = BG
        self.add(_rail("TOKEN, NOT WORD", "tiktoken 0.14.0"))

        word = _mono("strawberry", size=52)
        word.move_to([0.0, 2.05, 0])
        self.add(word)

        spec = [("str", 496, (2,)), ("aw", 675, ()), ("berry", 15717, (2, 3))]
        plain = VGroup(*[_token_box(p, t, (), size=52) for p, t, _ in spec])
        plain.arrange(RIGHT, buff=1.05).move_to([0.0, 0.42, 0])
        hot = VGroup(*[_token_box(p, t, h, size=52) for p, t, h in spec])
        hot.arrange(RIGHT, buff=1.05).move_to([0.0, 0.42, 0])
        self.add(plain)
        self.play(ReplacementTransform(plain, hot), run_time=1.0)
        self.wait(1.2)

        tallies = VGroup()
        for box, txt in zip(hot, ["one r", "no r", "two r"]):
            t = _label(txt, size=20, color=SOFT)
            t.next_to(box[0], UP, buff=0.24)
            tallies.add(t)
        self.play(FadeIn(tallies), run_time=0.6)

        ticks = VGroup()
        for box_i, glyph_i in ((0, 2), (2, 2), (2, 3)):
            g = hot[box_i][1][glyph_i]
            ticks.add(Line(g.get_corner(DL) + DOWN * 0.09,
                           g.get_corner(DR) + DOWN * 0.09,
                           color=ACC, stroke_width=3.2))
        self.play(Create(ticks), run_time=0.7)

        self.play(word[2].animate.set_color(ACC),
                  word[7].animate.set_color(ACC),
                  word[8].animate.set_color(ACC), run_time=0.8)

        note = _label("scattered inside chunks the model treats as single symbols",
                      size=21, color=SOFT)
        note.move_to([0.0, -2.15, 0])
        self.play(FadeIn(note), run_time=0.6)
        self.add(_cite("you are asking about a unit it does not natively see"))
        _hold(self, "B02")


# ─────────────────────────────────────────────────────────────────────────────
#  B03_SpaceCollapse — a leading space collapses three tokens into one (73700).
# ─────────────────────────────────────────────────────────────────────────────
class B03_SpaceCollapse(Scene):

    def construct(self):
        self.camera.background_color = BG
        self.add(_rail("TOKEN, NOT WORD", "tiktoken 0.14.0"))

        lead = _label("no leading space", size=21, color=SOFT)
        lead.move_to([0.0, 2.15, 0])
        self.add(lead)

        spec = [("str", 496, ()), ("aw", 675, ()), ("berry", 15717, ())]
        three = VGroup(*[_token_box(p, t, h, size=52) for p, t, h in spec])
        three.arrange(RIGHT, buff=1.05).move_to([0.0, 0.55, 0])
        self.play(FadeIn(three), run_time=0.7)

        chars_g, chars_n, chars_vt = _counter("characters in", -3.75, -2.05)
        toks_g, toks_n, toks_vt = _counter("tokens out", 3.75, -2.05)
        arrow = Arrow([-1.55, -2.23, 0], [1.55, -2.23, 0], color=ACC,
                      stroke_width=3.0, tip_length=0.24, buff=0)
        self.add(chars_g, toks_g, arrow)
        self.play(chars_vt.animate.set_value(10),
                  toks_vt.animate.set_value(3), run_time=0.9)
        self.wait(2.6)

        one = _token_box("' strawberry'", 73700, (), size=52)
        one.move_to([0.0, 0.55, 0])
        now = _label("one leading space", size=21, color=SOFT)
        now.move_to([0.0, 2.15, 0])
        self.play(ReplacementTransform(three, one),
                  ReplacementTransform(lead, now), run_time=1.5)
        self.play(chars_vt.animate.set_value(11),
                  toks_vt.animate.set_value(1), run_time=0.9)

        note = _label("words almost always follow a space, so that sequence earned its own entry",
                      size=20, color=SOFT)
        note.move_to([0.0, -0.95, 0])
        self.play(FadeIn(note), run_time=0.6)
        self.add(_cite("the split tracks frequency, not spelling"))
        _hold(self, "B03")


# ─────────────────────────────────────────────────────────────────────────────
#  B04_NotMeaning — unbelievable splits against meaning; berry (15717) recurs.
# ─────────────────────────────────────────────────────────────────────────────
class B04_NotMeaning(Scene):

    def construct(self):
        self.camera.background_color = BG
        self.add(_rail("TOKEN, NOT WORD", "tiktoken 0.14.0"))

        # Positioned with to_edge/next_to rather than width arithmetic inside a
        # coordinate literal: Gate A's mock manim does not apply .scale(), so a
        # literal built from .width reads as off-frame there and blocks the build.
        w1 = _mono("unbelievable", size=32)
        w1.set_y(1.72).to_edge(LEFT, buff=1.11)
        row1 = VGroup(*[_token_box(p, t, (), size=44) for p, t in
                        [("un", 359), ("belie", 32898), ("vable", 24694)]])
        row1.arrange(RIGHT, buff=0.8)
        row1.next_to(w1, RIGHT, buff=0.55).set_y(1.58)
        self.play(FadeIn(w1), run_time=0.4)
        self.play(TransformFromCopy(w1, row1), run_time=1.2)

        against = _label("not un · believe · able", size=21, color=SOFT)
        against.match_x(row1).set_y(0.42)
        self.play(FadeIn(against), run_time=0.5)
        self.wait(2.2)

        w2 = _mono("raspberry", size=32)
        w2.set_y(-1.28).to_edge(LEFT, buff=1.11)
        row2 = VGroup(*[_token_box(p, t, (), size=44) for p, t in
                        [("ras", 13075), ("p", 79), ("berry", 15717)]])
        row2.arrange(RIGHT, buff=0.8)
        row2.next_to(w2, RIGHT, buff=0.55).set_y(-1.42)

        # Geometry of the berry card, captured as plain floats BEFORE the
        # transform. Transform-family animations align submobject counts and
        # MUTATE the target group, so row2[2] stops pointing at the berry card
        # once TransformFromCopy has run — indexing it afterwards rings the
        # wrong token.
        berry_card = row2[2][0]
        berry_c = berry_card.get_center().copy()
        berry_w = float(berry_card.width)
        berry_h = float(berry_card.height)

        self.play(FadeIn(w2), run_time=0.4)
        self.play(TransformFromCopy(w2, row2), run_time=1.2)

        ring = RoundedRectangle(corner_radius=0.10,
                                width=berry_w + 0.24, height=berry_h + 0.24,
                                color=ACC, stroke_width=3.0)
        ring.move_to(berry_c)
        same = _label("15717 — the same token as in strawberry", size=20, color=SOFT)
        same.match_x(row2).set_y(-2.62)
        self.play(Create(ring), FadeIn(same), run_time=0.8)
        self.add(_cite("one reusable fragment from a fixed vocabulary, picked by frequency"))
        _hold(self, "B04")


# ─────────────────────────────────────────────────────────────────────────────
#  B05_DidItFail — the two dated Claude answers, and the split that differs.
#  Both screenshots are open slots (see PROMPTS.md); the scene renders labelled
#  frames until the PNGs land in media/.
# ─────────────────────────────────────────────────────────────────────────────
class B05_DidItFail(Scene):

    def construct(self):
        self.camera.background_color = BG
        self.add(_rail("TOKEN, NOT WORD", "asked 22 Sep 2026"))

        ask = _label("so does the model actually fail this?", size=27, weight="BOLD")
        ask.move_to([0.0, 2.32, 0])
        self.play(Write(ask), run_time=0.9)

        left = _shot_slot("B05-claude-strawberry.png",
                          "Claude · strawberry · 22 Sep 2026 · correct",
                          -3.25, 0.62)
        right = _shot_slot("B05-claude-blueberry.png",
                           "Claude · blueberry · 22 Sep 2026 · correct",
                           3.25, 0.62)
        self.play(FadeIn(left), run_time=0.6)
        self.wait(3.4)
        self.play(FadeIn(right), run_time=0.6)
        self.wait(3.4)

        verdict = _label("both correct — it can route around the limit",
                         size=22, color=SOFT)
        verdict.move_to([0.0, -1.64, 0])
        self.play(FadeIn(verdict), run_time=0.6)
        self.wait(3.6)

        # The boundary of the claim, on screen. What the evidence does NOT
        # establish is stated as plainly as what it does.
        does = _label("this explains why counting is unreliable", size=21, color=SOFT)
        does.move_to([0.0, -2.30, 0])
        does_not = _label("it does not establish that a model gets it wrong today",
                          size=23)
        does_not.move_to([0.0, -2.80, 0])
        self.play(FadeIn(does), run_time=0.5)
        self.wait(1.2)
        self.play(FadeIn(does_not), run_time=0.7)

        self.add(_cite("GPT-4 tokenizer · cl100k_base — Claude's vocabulary differs"))
        _hold(self, "B05")


# ─────────────────────────────────────────────────────────────────────────────
#  B06_TellSplit — the tell. Claude's spoken grouping vs the real tokens.
#  HONESTY RULE: the top row carries NO token ids. straw/ber/ry is how Claude
#  narrated the word in the 22 Sep screenshot; it is not tokenizer output, and
#  an id under it would be a false claim. Only the bottom row is cl100k_base.
# ─────────────────────────────────────────────────────────────────────────────
class B06_TellSplit(Scene):

    def construct(self):
        self.camera.background_color = BG
        self.add(_rail("TOKEN, NOT WORD", "tiktoken 0.14.0"))

        said_lbl = _label("Claude's grouping (what it said)", size=21, color=SOFT)
        said_lbl.move_to([0.0, 2.52, 0])
        said = VGroup(*[_token_box(p, None, (), size=52)
                        for p in ("straw", "ber", "ry")])
        said.arrange(RIGHT, buff=0.30).move_to([0.0, 1.55, 0])
        not_tokens = _label("not tokenizer output — no token IDs", size=16, color=SOFT)
        not_tokens.move_to([0.0, 0.72, 0])

        self.play(FadeIn(said_lbl), run_time=0.5)
        self.play(FadeIn(said), run_time=0.9)
        self.play(FadeIn(not_tokens), run_time=0.4)
        self.wait(3.2)

        real_lbl = _label("actual tokens · cl100k_base", size=21, color=SOFT)
        real_lbl.move_to([0.0, -0.62, 0])
        real = VGroup(*[_token_box(p, t, (), size=52)
                        for p, t in (("str", 496), ("aw", 675), ("berry", 15717))])
        real.arrange(RIGHT, buff=0.30).move_to([0.0, -1.62, 0])

        self.play(FadeIn(real_lbl), run_time=0.5)
        self.play(FadeIn(real), run_time=0.9)
        self.wait(2.8)

        # Both rows hold the same ten letters and span the same width, so the
        # cut points can be read off one shared baseline: ticks up for what
        # Claude said, ticks down for where the tokenizer actually cuts.
        base_y = 0.18
        span = float(said.width) / 2.0
        ruler = Line([-span, base_y, 0], [span, base_y, 0],
                     color=SOFT, stroke_width=1.2)
        up = VGroup(*[Line([x, base_y, 0], [x, base_y + 0.30, 0],
                           color=ACC, stroke_width=3.2)
                      for x in _boundaries(said)])
        down = VGroup(*[Line([x, base_y, 0], [x, base_y - 0.30, 0],
                             color=ACC, stroke_width=3.2)
                        for x in _boundaries(real)])
        self.play(Create(ruler), run_time=0.5)
        self.play(Create(up), run_time=0.6)
        self.play(Create(down), run_time=0.6)

        self.add(_cite("the grouping it shows you is not the grouping it runs on"))
        _hold(self, "B06")


# ─────────────────────────────────────────────────────────────────────────────
#  BOUT_Closing — the callback. Same answer (3), two paths: the letters you
#  read, and the cl100k_base tokens the model reads. Both paths point at the
#  one "3". No new numbers: 3 is strawberry.count('r'); the ids are B01's.
# ─────────────────────────────────────────────────────────────────────────────
class BOUT_Closing(Scene):

    def construct(self):
        self.camera.background_color = BG
        self.add(_rail("TOKEN, NOT WORD", "tiktoken 0.14.0"))

        q = _label("how many r's in strawberry?", size=30, weight="BOLD")
        q.move_to([-1.5, 2.38, 0])
        self.play(Write(q), run_time=0.8)

        # Your path: the word whole, its r's at indices 2, 7, 8.
        word = _mono("strawberry", size=72)
        word.move_to([-1.5, 1.32, 0])
        self.play(FadeIn(word), run_time=0.6)
        ticks = VGroup()
        for i in (2, 7, 8):
            g = word[i]
            ticks.add(Line(g.get_corner(DL) + DOWN * 0.10,
                           g.get_corner(DR) + DOWN * 0.10,
                           color=ACC, stroke_width=3.2))
        self.play(*[word[i].animate.set_color(ACC) for i in (2, 7, 8)],
                  Create(ticks), run_time=0.6)

        three = _label("3", size=150, weight="BOLD")
        three.move_to([4.7, 0.08, 0])
        rs = _label("r's", size=20, color=SOFT)
        rs.move_to([4.7, -1.02, 0])
        a_you = Arrow([2.05, 1.22, 0], [3.95, 0.42, 0], color=SOFT,
                      stroke_width=3.0, tip_length=0.22, buff=0)
        self.play(Write(three), GrowArrow(a_you), run_time=0.7)
        self.play(FadeIn(rs), run_time=0.3)
        self.wait(1.6)

        # The model's path: B01's three tokens, the same r's buried inside.
        row = VGroup(*[_token_box(p, t, h, size=48) for p, t, h in
                       [("str", 496, (2,)), ("aw", 675, ()), ("berry", 15717, (2, 3))]])
        row.arrange(RIGHT, buff=0.55).move_to([-1.5, -1.25, 0])
        self.play(TransformFromCopy(word, row), run_time=1.3)
        sees = _label("what the model sees · cl100k_base tokens", size=19, color=SOFT)
        sees.move_to([-1.5, 0.02, 0])
        self.play(FadeIn(sees), run_time=0.5)
        a_model = Arrow([2.25, -1.05, 0], [3.95, -0.28, 0], color=SOFT,
                        stroke_width=3.0, tip_length=0.22, buff=0)
        self.play(GrowArrow(a_model), run_time=0.7)

        self.add(_cite("same answer, different path"))
        _hold(self, "BOUT")


# ─────────────────────────────────────────────────────────────────────────────
#  BTHX_ThankYou — the sign-off, read the model's way. Every piece and id is
#  cl100k_base via tiktoken 0.14.0 (FACTCHECK S4): 'Thank' 13359 · ' you' 499 ·
#  '!' 0. Id 0 is real — '!' is the first entry in the vocabulary.
#  Pieces are quoted, as in B03, so the leading space inside ' you' is legible;
#  a terracotta underscore marks the space cell itself. Ends on a short fade
#  that lives inside the mp3's own trailing silence (see _hold).
# ─────────────────────────────────────────────────────────────────────────────
class BTHX_ThankYou(Scene):

    def construct(self):
        self.camera.background_color = BG
        self.add(_rail("TOKEN, NOT WORD", "tiktoken 0.14.0"))

        title = _label("thanks for watching", size=30, weight="BOLD")
        title.move_to([0.0, 2.30, 0])
        self.play(FadeIn(title), run_time=0.5)

        phrase = _mono("Thank you!", size=60)
        phrase.move_to([0.0, 1.15, 0])
        self.play(FadeIn(phrase), run_time=0.5)

        spec = [("'Thank'", 13359), ("' you'", 499), ("'!'", 0)]
        boxes = VGroup(*[_token_box(p, t, (), size=48) for p, t in spec])
        boxes.arrange(RIGHT, buff=0.9).move_to([0.0, -0.75, 0])

        # Text drops spaces from its glyph list, so ' you' is [' y o u ']: the
        # space cell is the gap between glyph 0 (quote) and glyph 1 (y).
        # Measured as plain floats BEFORE the transform — TransformFromCopy
        # mutates its target group (the B04 ring bug), and indexing boxes[1]
        # afterwards put this marker under 'Thank' in frame review.
        you = boxes[1][1]
        base_y = float(you[2].get_bottom()[1]) - 0.08   # 'o': baseline, no descender
        x0 = float(you[0].get_right()[0]) + 0.05
        x1 = float(you[1].get_left()[0]) - 0.05
        space = Line([x0, base_y, 0], [x1, base_y, 0], color=ACC, stroke_width=3.2)

        self.play(TransformFromCopy(phrase, boxes), run_time=1.2)
        note = _label("the space rides inside the second token", size=19, color=SOFT)
        note.move_to([0.0, -2.32, 0])
        self.play(Create(space), FadeIn(note), run_time=0.5)

        self.add(_cite("cl100k_base · GPT-4 tokenizer"))
        _hold(self, "BTHX", fade_out=0.6)
