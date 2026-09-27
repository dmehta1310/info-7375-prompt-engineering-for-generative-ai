"""scenes.py — Manim scenes for three-scores-not-three-chances.

Concept (Chapter 1, Part 2): three scores are not yet three chances.

Every number on screen is COMPUTED here by importing the course's own
lessons/01-randomness-and-first-prompts/code/main.py. Nothing is typed in by
hand. [1, 2, 3] is the lesson's demo input; [-1, 2, 3] is a CONSTRUCTED
example and is labelled that way on screen.

Timing: each scene reads its beat's measured narration length and its
narration text from beat_sheet.json, and places each visual event at the
point in the sentence where the words land. Never hand-tune durations:
regenerate audio and re-render.

No LaTeX (Text only), so the reel does not need a TeX toolchain.
Palette: cream ground, warm ink, one terracotta accent per scene.
"""
import importlib.util
import json
import math
from pathlib import Path

from manim import *

HERE = Path(__file__).resolve().parent
# The toolkit's static pre-flight (GATE A) runs a COPY of this file from a temp
# folder with a stubbed manim, where main.py and beat_sheet.json are not beside
# it. Only then do we fall back to a verbatim copy of probabilities() and fixed
# placeholder timing; the real render always imports main.py and the sheet.
PREFLIGHT = not (HERE / "beat_sheet.json").exists()

if not PREFLIGHT:
    COURSE = HERE.parents[2]
    MAIN_PY = COURSE / "lessons/01-randomness-and-first-prompts/code/main.py"
    _spec = importlib.util.spec_from_file_location("lesson_main", MAIN_PY)
    lesson = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(lesson)
    probabilities = lesson.probabilities
else:
    def probabilities(logits, temperature=1.0):  # verbatim from main.py, pre-flight only
        peak = max(logits)
        weights = [math.exp((x - peak) / temperature) for x in logits]
        total = sum(weights)
        return [weight / total for weight in weights]

REAL = [1, 2, 3]            # lesson demo input (main.py demo())
CONSTRUCTED = [-1, 2, 3]    # our own example, labelled CONSTRUCTED on screen


def weights_of(scores):
    """Step 1 exactly as main.py does it at temperature 1."""
    peak = max(scores)
    return [x - peak for x in scores], [math.exp(x - peak) for x in scores]


P_REAL = probabilities(REAL)
P_CON = probabilities(CONSTRUCTED)
SHIFT_REAL, W_REAL = weights_of(REAL)
SHIFT_CON, W_CON = weights_of(CONSTRUCTED)

# Refuse to render if anything drifts from the saved evidence.
assert [round(p, 3) for p in P_REAL] == [0.090, 0.245, 0.665], P_REAL
assert [round(p, 3) for p in P_CON] == [0.013, 0.265, 0.721], P_CON
assert round(sum(W_REAL), 3) == 1.503 and round(sum(W_CON), 3) == 1.386

if not PREFLIGHT:
    SHEET = json.loads((HERE / "beat_sheet.json").read_text())
    BEATS = {b["beat_id"]: b for b in SHEET["beats"]}
else:
    BEATS = {}

BG = "#FAF9F5"
INK = "#3D3929"
MUTED = "#8A8470"
ACCENT = "#D97757"
WARN = "#A44A32"
SERIF = "EB Garamond"
MONO = "Menlo"

config.background_color = BG


def T(s, size=40, color=INK, font=SERIF, **kw):
    return Text(s, font=font, font_size=size, color=color, **kw)


def fmt(x, places=3):
    return f"{x:.{places}f}"


def tag(label):
    """The on-screen honesty label for anything we made up."""
    txt = T(label, 26, WARN, weight="BOLD")
    box = SurroundingRectangle(txt, color=WARN, buff=0.14, stroke_width=2.5)
    return VGroup(box, txt)


def check_mark(color=INK):
    return VMobject(color=color, stroke_width=8).set_points_as_corners(
        [[-0.22, 0.0, 0], [-0.05, -0.18, 0], [0.26, 0.22, 0]])


def cross_mark(color=ACCENT):
    return VGroup(Line([-0.2, -0.2, 0], [0.2, 0.2, 0]), Line([-0.2, 0.2, 0], [0.2, -0.2, 0])
                  ).set_stroke(color, 8)


def bar(value, x, base, unit, width=1.3, color=INK):
    h = max(abs(value) * unit, 0.02)
    r = Rectangle(width=width, height=h, stroke_width=0, fill_color=color, fill_opacity=1)
    if value >= 0:
        r.move_to([x, base + h / 2, 0])
    else:
        r.move_to([x, base - h / 2, 0])
    return r


# The toolkit run.sh discovers scenes by regex: each beat class must subclass a class
# literally named Scene, so the timing helpers live on a subclass that keeps that name.
ManimScene = Scene


class Scene(ManimScene):
    BID = ""

    def setup(self):
        self._timing()

    def _timing(self):
        # Also called lazily: the pre-flight stub Scene never runs setup().
        b = BEATS.get(self.BID)
        if b is None:  # pre-flight copy: placeholder timing, layout is what is checked
            self.D, self.words = 12.0, None
        else:
            self.D = float(b["actual_duration_s"]) + float(b.get("lead_silence_s", 0) or 0)
            self.words = b["narration_text"]
        self.t = 0.0

    def cue(self, phrase):
        if not hasattr(self, "D"):
            self._timing()
        """Fraction of the beat at which `phrase` is spoken (by character position)."""
        if self.words is None:
            return min(self.t / self.D + 0.05, 0.95)
        i = self.words.find(phrase)
        assert i >= 0, f"{self.BID}: cue phrase not in narration: {phrase!r}"
        return i / len(self.words)

    def at(self, phrase_or_frac, *anims, run_time=0.8):
        if not hasattr(self, "D"):
            self._timing()
        frac = self.cue(phrase_or_frac) if isinstance(phrase_or_frac, str) else phrase_or_frac
        gap = frac * self.D - self.t
        if gap > 0.02:
            self.wait(gap)
            self.t += gap
        if anims:
            self.play(*anims, run_time=run_time)
            self.t += run_time

    def finish(self):
        if not hasattr(self, "D"):
            self._timing()
        rest = self.D - self.t
        if rest > 0.02:
            self.wait(rest)


# ── B02 — the scores are not chances ──────────────────────────────────────────
class B02_ScoresNotChances(Scene):
    BID = "B02"

    def construct(self):
        base, unit, xs = -2.4, 1.35, [-5.0, -3.2, -1.4]
        head = T("Three scores", 52).to_edge(UP, buff=0.6).to_edge(LEFT, buff=0.9)
        axis = Line([-6.1, base, 0], [-0.3, base, 0], color=INK, stroke_width=3)
        bars = [bar(s, x, base, unit) for s, x in zip(REAL, xs)]
        nums = [T(str(s), 48, weight="BOLD").next_to(b, UP, 0.15) for s, b in zip(REAL, bars)]
        labs = [T(f"option {'ABC'[i]}", 30, MUTED).move_to([x, base - 0.45, 0]) for i, x in enumerate(xs)]

        rules_head = T("Chances must obey:", 44).move_to([3.6, 2.2, 0])
        r1 = T("1.  none negative", 40).move_to([3.3, 1.0, 0]).align_to(rules_head, LEFT)
        r2 = T("2.  add up to 1", 40).move_to([3.3, -0.1, 0]).align_to(rules_head, LEFT)
        ok1 = check_mark().next_to(r1, RIGHT, 0.5)
        total = ValueTracker(0)
        counter = always_redraw(lambda: T(f"total = {total.get_value():.0f}", 56, weight="BOLD")
                                .move_to([3.6, -1.7, 0]))
        bad = cross_mark().next_to(r2, RIGHT, 0.5)
        ring = SurroundingRectangle(VGroup(r2, bad), color=ACCENT, buff=0.2)

        self.add(head, axis, *labs)
        self.at(0.0, *[GrowFromEdge(b, DOWN) for b in bars], *[FadeIn(n) for n in nums], run_time=1.2)
        self.at("The third option", Indicate(VGroup(bars[2], nums[2]), color=INK, scale_factor=1.08))
        self.at("But chances follow", FadeIn(rules_head))
        self.at("None can be negative", FadeIn(r1), Create(ok1))
        self.at("And together", FadeIn(r2))
        self.add(counter)
        self.at("Watch the total", total.animate.set_value(sum(REAL)), run_time=1.8)
        self.at("So they're not", Create(bad), Create(ring))
        self.finish()


# ── B03 — the shortcut breaks ─────────────────────────────────────────────────
class B03_ShortcutBreaks(Scene):
    BID = "B03"

    def construct(self):
        base, unit, xs = -0.9, 3.4, [-3.2, 0.0, 3.2]
        rule = T("chance = score ÷ total", 48).to_edge(UP, buff=0.7)
        scores_line = T("scores 1, 2, 3   ·   total 6", 40, MUTED).next_to(rule, DOWN, 0.3)
        axis = Line([-5.2, base, 0], [5.2, base, 0], color=INK, stroke_width=3)
        zero = T("0", 30, MUTED).next_to(axis, LEFT, 0.2)
        div = [s / sum(REAL) for s in REAL]
        bars = [bar(v, x, base, unit) for v, x in zip(div, xs)]
        vals = [T(fmt(v), 44, weight="BOLD").next_to(b, UP, 0.15) for v, b in zip(div, bars)]
        summ = T("adds up to 1", 36).to_corner(DR, buff=0.9)

        self.add(rule, axis, zero)
        self.at("divide each score", FadeIn(scores_line))
        self.at("One sixth", *[GrowFromEdge(b, DOWN) for b in bars], *[FadeIn(v) for v in vals], run_time=1.4)
        self.at("That works here", FadeIn(summ))

        con = [s / sum(CONSTRUCTED) for s in CONSTRUCTED]
        stamp = tag("CONSTRUCTED EXAMPLE").to_corner(DL, buff=0.9)
        scores2 = T("scores −1, 2, 3   ·   total 4", 40, MUTED).move_to(scores_line)
        bars2 = [bar(v, x, base, unit, color=(WARN if v < 0 else INK)) for v, x in zip(con, xs)]
        vals2 = [T(fmt(v, 2), 44, WARN if v < 0 else INK, weight="BOLD")
                 .next_to(b, DOWN if v < 0 else UP, 0.15) for v, b in zip(con, bars2)]
        self.at("Take minus one", FadeIn(stamp), FadeOut(summ), Transform(scores_line, scores2))
        self.at("The total is four", *[Transform(a, b) for a, b in zip(bars[1:], bars2[1:])],
                *[Transform(a, b) for a, b in zip(vals[1:], vals2[1:])])
        self.at("minus one divided", Transform(bars[0], bars2[0]), Transform(vals[0], vals2[0]), run_time=1.2)
        flag = T("a negative chance", 44, ACCENT, weight="BOLD").next_to(bars2[0], RIGHT, 0.4).shift(DOWN * 0.3)
        self.at("A negative chance", Write(flag))
        self.finish()


# ── B04 — step 1: positive weights ────────────────────────────────────────────
CODE = [
    "peak = max(logits)",
    "weights = [math.exp((x - peak) / temperature) for x in logits]",
    "total = sum(weights)",
    "return [weight / total for weight in weights]",
]


class B04_PositiveWeights(Scene):
    BID = "B04"

    def construct(self):
        head = T("Step 1  ·  make every weight positive", 46).to_edge(UP, buff=0.7)
        lines = VGroup(*[T(s, 22, font=MONO) for s in CODE]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        panel = SurroundingRectangle(lines, color=MUTED, buff=0.22, stroke_width=2)
        src = T("main.py · probabilities() · lines 14–17", 24, MUTED).next_to(panel, DOWN, 0.15, aligned_edge=LEFT)
        code = VGroup(panel, lines, src)
        if code.width > 12.3:
            code.scale_to_fit_width(12.3)
        code.next_to(head, DOWN, 0.3)

        cols = [0.9, 3.1, 5.3]
        labels = ["scores", "minus the top score (3)", "exp  →  weights"]
        rows_vals = [(REAL, 0), (SHIFT_REAL, 0), (W_REAL, 3)]
        top = code.get_bottom()[1] - 0.45
        grid = VGroup()
        for k, (lab, (vals, places)) in enumerate(zip(labels, rows_vals)):
            y = top - k * 0.64
            l = T(lab, 36, MUTED).move_to([0, y, 0]).align_to([-6.2, 0, 0], LEFT)
            cells = VGroup(*[T(fmt(v, places) if places else str(v), 42, weight="BOLD").move_to([x, y, 0])
                             for v, x in zip(vals, cols)])
            grid.add(VGroup(l, cells))
        c3 = grid[2][1]
        hl1 = SurroundingRectangle(lines[0], color=INK, buff=0.07, stroke_width=3)
        hl2 = SurroundingRectangle(lines[1], color=ACCENT, buff=0.07, stroke_width=3)
        pos = T("all positive", 32, ACCENT, weight="BOLD").next_to(c3, DOWN, 0.15)

        self.add(head)
        self.at(0.0, FadeIn(code), run_time=1.0)
        self.at("turn every score", FadeIn(grid[0]))
        self.at("subtracts the top score", Create(hl1), FadeIn(grid[1]))
        self.at("applies the exponential", ReplacementTransform(hl1, hl2), FadeIn(grid[2]))
        self.at("A bigger score", Write(pos))
        self.finish()


# ── B05 — step 2: divide by the total ─────────────────────────────────────────
class B05_DivideByTotal(Scene):
    BID = "B05"

    def construct(self):
        head = T("Step 2  ·  divide by the total", 46).to_edge(UP, buff=0.7)
        tot = sum(W_REAL)
        sum_line = T(f"{fmt(W_REAL[0])} + {fmt(W_REAL[1])} + {fmt(W_REAL[2])}  =  {fmt(tot)}", 44
                     ).next_to(head, DOWN, 0.45)
        base, unit, xs = -2.6, 3.9, [-5.2, -3.3, -1.4]
        axis = Line([-6.2, base, 0], [-0.4, base, 0], color=INK, stroke_width=3)
        bars = [bar(p, x, base, unit) for p, x in zip(P_REAL, xs)]
        vals = [T(fmt(p), 40, weight="BOLD").next_to(b, UP, 0.15) for p, b in zip(P_REAL, bars)]
        labs = [T(f"option {'ABC'[i]}", 28, MUTED).move_to([x, base - 0.4, 0]) for i, x in enumerate(xs)]
        rule = T("each weight ÷ " + fmt(tot), 34, MUTED).move_to([-3.3, 1.45, 0])

        printed = VGroup(
            T("main.py printed:", 30, MUTED),
            T('"probabilities": [', 26, font=MONO),
            T(f"  {P_REAL[0]!r},", 26, font=MONO),
            T(f"  {P_REAL[1]!r},", 26, font=MONO),
            T(f"  {P_REAL[2]!r}", 26, font=MONO),
            T("]", 26, font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.4, -0.5, 0])
        box = SurroundingRectangle(printed, color=MUTED, buff=0.3, stroke_width=2)
        total_line = T(f"total = {fmt(sum(P_REAL))}", 48, ACCENT, weight="BOLD").next_to(box, DOWN, 0.4)

        self.add(head, axis, *labs)
        self.at("add the weights", FadeIn(sum_line))
        self.at("divide each one", FadeIn(rule), *[GrowFromEdge(b, DOWN) for b in bars], run_time=1.2)
        self.at("Point zero nine", *[FadeIn(v) for v in vals])
        self.at("Exactly what main", FadeIn(box), FadeIn(printed))
        self.at("they add up to one", Write(total_line))
        self.finish()


# ── B06 — the broken case, fixed ──────────────────────────────────────────────
class B06_BrokenCaseFixed(Scene):
    BID = "B06"

    def construct(self):
        stamp = tag("CONSTRUCTED EXAMPLE").to_corner(DL, buff=0.9)
        head = T("scores  −1, 2, 3", 50).to_edge(UP, buff=0.7)
        step1 = T("step 1  →  weights  " + ",  ".join(fmt(w) for w in W_CON), 38).next_to(head, DOWN, 0.4)
        step2 = T(f"step 2  →  ÷ {fmt(sum(W_CON))}", 38).next_to(step1, DOWN, 0.3)
        base, unit, xs = -2.3, 3.2, [-3.2, 0.0, 3.2]
        axis = Line([-5.2, base, 0], [5.2, base, 0], color=INK, stroke_width=3)
        bars = [bar(p, x, base, unit) for p, x in zip(P_CON, xs)]
        vals = [T(fmt(p), 44, weight="BOLD").next_to(b, UP, 0.15) for p, b in zip(P_CON, bars)]
        total = T(f"all positive  ·  total = {fmt(sum(P_CON))}", 40, ACCENT, weight="BOLD"
                  ).to_corner(DR, buff=0.9)

        self.add(stamp, head, axis)
        self.at("broke the shortcut", FadeIn(step1))
        self.at("becomes about", FadeIn(step2), *[GrowFromEdge(b, DOWN) for b in bars], run_time=1.2)
        self.at("point zero one three", *[FadeIn(v) for v in vals])
        self.at("Every chance positive", Write(total))
        self.finish()


# ── B07 — what this does not tell you ─────────────────────────────────────────
class B07_NotATruthCheck(Scene):
    BID = "B07"

    def construct(self):
        head = T("What the conversion does not check", 48).to_edge(UP, buff=0.7)
        base, unit, xs = -1.8, 3.8, [-3.2, 0.0, 3.2]
        axis = Line([-5.2, base, 0], [5.2, base, 0], color=INK, stroke_width=3)
        bars = [bar(p, x, base, unit) for p, x in zip(P_REAL, xs)]
        vals = [T(fmt(p), 42, weight="BOLD").next_to(b, UP, 0.15) for p, b in zip(P_REAL, bars)]
        labs = [T(f"option {'ABC'[i]}", 28, MUTED).move_to([x, base - 0.4, 0]) for i, x in enumerate(xs)]
        src = T("chances from main.py (real run)", 26, MUTED).next_to(head, DOWN, 0.2).to_edge(RIGHT, buff=0.9)

        stamp = tag("CONSTRUCTED HYPOTHETICAL").to_corner(UL, buff=0.9).shift(DOWN * 1.05)
        key = T("answer key: option A is correct", 34, weight="BOLD").next_to(stamp, RIGHT, 0.4)
        tick = check_mark().scale(1.1).next_to(labs[0], RIGHT, 0.25)
        wrong = T("most chance, wrong answer", 32, ACCENT, weight="BOLD").next_to(vals[2], LEFT, 0.4)
        foot = T("Adds up to 1.  Correctness never checked.", 38).to_edge(DOWN, buff=0.7)

        self.add(head, axis, *labs, src, *bars, *vals)
        self.at("It never checks", FadeIn(stamp), FadeIn(key), Create(tick))
        self.at("favour a wrong answer", Write(wrong), Indicate(bars[2], color=ACCENT, scale_factor=1.04))
        self.at("tidy chances", FadeIn(foot))
        self.finish()


# ── B10 — title outro (our own card: the toolkit outro hardcodes another handle) ─
class B10_TitleOutro(Scene):
    BID = "B10"

    def construct(self):
        title = VGroup(T("Three Scores Are Not Yet", 92), T("Three Chances", 92)).arrange(DOWN, buff=0.3).shift(UP * 0.6)
        dot = Dot(radius=0.1, color=ACCENT).next_to(title[1], RIGHT, 0.12).align_to(title[1], DOWN).shift(UP * 0.05)
        credit = T("Varnika M  ·  INFO 7375  ·  Week 01", 44, MUTED)
        voice = T("Narration: synthetic voice (Kokoro am_onyx)", 36, MUTED)
        foot = VGroup(credit, voice).arrange(DOWN, buff=0.25).next_to(title, DOWN, 1.0)
        rule = Line([-5.5, 0, 0], [5.5, 0, 0], color=MUTED, stroke_width=2).next_to(title, DOWN, 0.5)
        # B10's narration is only ~3 s, so everything lands by ~1.5 s and then holds.
        self.at(0.0, Write(title), GrowFromCenter(dot), run_time=0.9)
        self.at(0.0, Create(rule), FadeIn(foot, shift=UP * 0.3), run_time=0.6)
        self.finish()
