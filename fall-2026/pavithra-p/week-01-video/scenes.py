"""Manim scenes for "Thousands of Years, Divided" (one Scene per beat).

Numbers: every figure below is checked against evidence.json (written by
evidence.py from the course's research/llm_scale.py) whenever that file is
next to this one. A mismatch stops the render.

Timing: each scene reads its beat's measured narration length and narration
text from beat_sheet.json, and places visual cues at the point in the audio
where the matching phrase is spoken (estimated from text position).

Rendered by Brutalist:  ./art run <this folder>
Plain text only (no MathTex / DecimalNumber), so no LaTeX install is needed.
"""
import json
from pathlib import Path

from manim import *
import numpy as np

HERE = Path(__file__).resolve().parent

# ── palette (all text colours >= 4.5:1 on BG) ───────────────────────────────
BG = "#FAF9F5"
INK = "#1F1E1D"        # 15.8:1
MUTED = "#5E5D59"      # 6.26:1
ACCENT = "#B5421A"     # 5.3:1
BLUE = "#2F5D8A"       # 6.53:1
SOFT = "#E9E4D8"       # fills only, never text
ACCENT_SOFT = "#F6E3D9"  # fills only; INK on it = 13.4:1
FONT = "Helvetica Neue"
config.background_color = BG

KICKER = "INFO 7375 · SCALE, IN UNITS YOU CAN CHECK"

# ── the numbers (verified against evidence.json below) ──────────────────────
TOKENS = 300_000_000_000
WPT = 0.75
WORDS = 225_000_000_000
SECONDS_PER_YEAR = 31_557_600
MINUTES_PER_YEAR = 525_960            # 31,557,600 / 60 (365.25-day year)
RATES = [300, 250, 200, 150]
NONSTOP = {300: 1426.0, 250: 1711.2, 200: 2138.9, 150: 2851.9}   # script output
EIGHT_H = {300: 4277.9, 250: 5133.5, 200: 6416.8, 150: 8555.8}   # extension


def _verify():
    ev_path = HERE / "evidence.json"
    if not ev_path.is_file():
        return
    ev = json.loads(ev_path.read_text())
    so, ext = ev["script_output"], ev["extension"]
    assert so["gpt3_train_tokens"] == TOKENS and so["words_per_token"] == WPT
    assert so["seconds_per_year"] == SECONDS_PER_YEAR == MINUTES_PER_YEAR * 60
    assert ev["derived_steps"]["words"] == WORDS
    for r in RATES:
        assert so["reading_years_by_rate"][str(r)] == NONSTOP[r], r
        assert ext["reading_years_by_rate"][str(r)] == EIGHT_H[r], r


_verify()


def years_at(wpm):
    return WORDS / max(wpm, 1) / MINUTES_PER_YEAR


# ── timing from the beat sheet ──────────────────────────────────────────────
def _load_sheet():
    p = HERE / "beat_sheet.json"
    if not p.is_file():
        return {}, {}
    beats = json.loads(p.read_text())["beats"]
    dur = {b["beat_id"]: float(b.get("actual_duration_s") or 0) for b in beats}
    txt = {b["beat_id"]: b.get("narration_text", "") for b in beats}
    return dur, txt


DUR, NARR = _load_sheet()


def _weight(s):
    # speech time ~ characters, plus pauses at punctuation
    return (len(s) + 6 * s.count(".") + 3 * s.count(",") + 4 * s.count(":")
            + 6 * s.count("?"))


class Clock:
    """Tracks elapsed scene time so cues can land on spoken phrases."""

    def __init__(self, scene, bid):
        self.s, self.bid, self.t = scene, bid, 0.0

    def play(self, *anims, rt=1.0, **kw):
        self.s.play(*anims, run_time=rt, **kw)
        self.t += rt

    def wait(self, d):
        if d > 0.02:
            self.s.wait(d)
            self.t += d

    def at(self, phrase, lead=0.2):
        text = NARR.get(self.bid, "")
        i = text.find(phrase)
        if i < 0 or not DUR.get(self.bid):
            return
        self.wait(DUR[self.bid] * _weight(text[:i]) / _weight(text) - lead - self.t)

    def finish(self):
        self.wait(max(DUR.get(self.bid, 0.0) - self.t, 0.0) + 0.4)


# ── small helpers ───────────────────────────────────────────────────────────
TEXT_OVERSAMPLE = 4   # Manim/Pango mis-kerns small text ("slo gan"); render big, scale down


def T(s, size=32, color=INK, weight="NORMAL"):
    t = Text(s, font=FONT, font_size=size * TEXT_OVERSAMPLE, color=color, weight=weight)
    return t.scale_to_fit_width(t.width / TEXT_OVERSAMPLE)   # == scale(1/4)


def fit(m, max_w):
    if m.width > max_w:
        m.scale_to_fit_width(max_w)
    return m


def chrome(scene, footer=None):
    k = T(KICKER, 18, MUTED)
    k.move_to([-6.1 + k.width / 2, 3.15, 0])
    scene.add(k)
    if footer:
        f = T(footer, 18, MUTED)
        f.move_to([6.1 - f.width / 2, -3.15, 0])
        scene.add(f)


def fmt1(x):
    return f"{x:,.1f}"


def chip(label, w, h=0.62, size=22, fill=SOFT, stroke=MUTED, color=INK):
    box = RoundedRectangle(corner_radius=0.12, width=w, height=h,
                           fill_color=fill, fill_opacity=1, stroke_color=stroke,
                           stroke_width=2)
    txt = fit(T(label, size, color), w - 0.3)
    txt.move_to(box.get_center())
    return VGroup(box, txt)


# ════════════════════════════════════════════════════════════════════════════
class B00_Hook(Scene):
    def construct(self):
        c = Clock(self, "B00")
        chrome(self)
        lines = VGroup(
            T("“It would take a human", 50),
            T("thousands of years to read", 50, weight="BOLD"),
            T("everything GPT-3 was trained on.”", 50),
        ).arrange(DOWN, buff=0.28)
        lines.move_to([0, 1.1, 0])
        tag = T("the slogan, paraphrased from the course text", 22, MUTED)
        tag.move_to([0, -0.55, 0])
        for ln in lines:
            c.play(FadeIn(ln, shift=UP * 0.15), rt=0.9)
        c.play(FadeIn(tag), rt=0.5)

        c.at("It sounds like a directly measured fact")
        q = T("a directly measured fact?", 36, MUTED)
        q.move_to([0, -1.6, 0])
        c.play(FadeIn(q), rt=0.6)

        c.at("It is an estimate")
        est = VGroup(T("an estimate:", 36, ACCENT, "BOLD"), T("text", 36),
                     T("÷", 44, ACCENT, "BOLD"), T("reading speed", 36)).arrange(RIGHT, buff=0.3)
        est.move_to([0, -1.6, 0])
        c.play(ReplacementTransform(q, est), rt=0.8)
        guesses = T("…with guesses hidden inside", 26, MUTED)
        guesses.move_to([0, -2.45, 0])
        c.play(FadeIn(guesses), rt=0.6)

        c.at("Let's open it up")
        title = T("Thousands of Years, Divided", 66, INK, "BOLD")
        title.move_to([0, 0.9, 0])
        fit(title, 12)
        c.play(FadeOut(lines), FadeOut(tag), rt=0.5)
        c.play(Write(title), est.animate.move_to([0, -0.6, 0]),
               guesses.animate.move_to([0, -1.5, 0]), rt=1.2)
        by = T("Pavithra P.  ·  INFO 7375  ·  Week 01", 24, MUTED)
        by.move_to([0, -2.6, 0])
        c.play(FadeIn(by), rt=0.5)
        c.finish()


class B01_Reported(Scene):
    def construct(self):
        c = Clock(self, "B01")
        chrome(self)
        n = ValueTracker(0)
        big = always_redraw(lambda: T(f"{int(n.get_value()):,}", 88, INK, "BOLD").move_to([0, 1.35, 0]))
        unit = T("training tokens", 38, INK)
        unit.move_to([0, 0.2, 0])
        self.add(big)
        c.play(n.animate.set_value(TOKENS), FadeIn(unit), rt=2.8)
        rep = chip("REPORTED  ·  Brown et al. 2020, “Language Models are Few-Shot Learners”, arXiv:2005.14165",
                   11.6, size=22, fill=ACCENT_SOFT, stroke=ACCENT)
        rep.move_to([0, -0.75, 0])
        c.play(FadeIn(rep, shift=UP * 0.1), rt=0.8)

        c.at("A token is a chunk")
        word = T("unbelievable", 40)
        word.move_to([-3.3, -2.2, 0])
        c.play(FadeIn(word), rt=0.5)
        pieces = VGroup(*[chip(p, w, h=0.7, size=34, fill=SOFT, stroke=BLUE)
                          for p, w in (("un", 1.0), ("believ", 1.9), ("able", 1.4))])
        pieces.arrange(RIGHT, buff=0.14).move_to([-3.3, -2.2, 0])
        c.play(ReplacementTransform(word, pieces), rt=0.9)
        lab = VGroup(T("constructed illustration:", 20, ACCENT, "BOLD"),
                     T("not a real tokenizer's output", 20, MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        lab.move_to([2.6, -2.2, 0])
        c.play(FadeIn(lab), rt=0.5)
        c.finish()


class B02_Words(Scene):
    def construct(self):
        c = Clock(self, "B02")
        chrome(self, "numbers: research/llm_scale.py")
        l1 = VGroup(T("300,000,000,000", 56, INK, "BOLD"), T("tokens", 40, MUTED)).arrange(RIGHT, buff=0.35)
        l1.move_to([0, 1.7, 0])
        self.add(l1)

        c.at("approximation of zero point seven five")
        l2 = VGroup(T("×", 56, ACCENT, "BOLD"), T("0.75", 56, ACCENT, "BOLD"),
                    T("words per token", 40, MUTED)).arrange(RIGHT, buff=0.35)
        l2.move_to([0, 0.6, 0])
        c.play(FadeIn(l2, shift=LEFT * 0.2), rt=0.8)
        box = SurroundingRectangle(l2[1], color=ACCENT, buff=0.12, stroke_width=3)
        c.play(Create(box), rt=0.5)
        note = chip("0.75 is an approximation used by the course, not a measurement", 11.0,
                    h=0.62, size=24, fill=ACCENT_SOFT, stroke=ACCENT)
        note.move_to([0, -2.2, 0])
        c.play(FadeIn(note), rt=0.6)

        c.at("three hundred billion tokens becomes")
        rule = Line([-4.6, -0.05, 0], [4.6, -0.05, 0], color=INK, stroke_width=3)
        c.play(Create(rule), rt=0.4)
        l3 = VGroup(T("225,000,000,000", 56, INK, "BOLD"), T("words", 40, INK)).arrange(RIGHT, buff=0.35)
        l3.move_to([0, -0.85, 0])
        c.play(FadeIn(l3, shift=UP * 0.2), rt=0.9)
        c.finish()


class B03_Divide(Scene):
    def construct(self):
        c = Clock(self, "B03")
        chrome(self, "script output: research/llm_scale.py")
        s1 = VGroup(T("225,000,000,000 words", 40), T("÷", 46, ACCENT, "BOLD"),
                    T("250 words per minute", 40)).arrange(RIGHT, buff=0.3)
        s1.move_to([0, 2.05, 0])
        fit(s1, 12)
        c.at("two hundred and fifty words a minute")
        c.play(FadeIn(s1), rt=0.8)

        c.at("nine hundred million minutes")
        r1 = T("= 900,000,000 minutes", 46, INK, "BOLD")
        r1.move_to([0, 1.1, 0])
        c.play(FadeIn(r1, shift=UP * 0.15), rt=0.8)

        c.at("Turn that into years")
        s2 = VGroup(T("900,000,000 minutes", 40), T("÷", 46, ACCENT, "BOLD"),
                    T("525,960 minutes per year", 40)).arrange(RIGHT, buff=0.3)
        s2.move_to([0, -0.1, 0])
        fit(s2, 12)
        yr = T("(a 365.25-day year)", 22, MUTED)
        yr.move_to([0, -0.75, 0])
        c.play(FadeIn(s2), FadeIn(yr), rt=0.8)
        res = T("≈ 1,711.2 years", 80, ACCENT, "BOLD")
        res.move_to([0, -1.95, 0])
        c.play(FadeIn(res, scale=1.1), rt=0.9)
        c.finish()


class B04_Speed(Scene):
    def construct(self):
        c = Clock(self, "B04")
        chrome(self, "script output: research/llm_scale.py")
        # ── left: the reading-speed dial ──
        # same left-to-right order as the bars: 300 (fastest) on the left, 150 on the right
        x_of = lambda w: -5.7 + (300 - min(max(w, 150), 300)) / 150 * 4.6   # 300 → -5.7, 150 → -1.1
        head = T("reading speed (words per minute)", 24, MUTED)
        head.move_to([-3.4, 2.2, 0])
        track = Line([x_of(150), 1.3, 0], [x_of(300), 1.3, 0], color=MUTED, stroke_width=6)
        ticks = VGroup()
        for w in RATES:
            ticks.add(Line([x_of(w), 1.15, 0], [x_of(w), 1.45, 0], color=MUTED, stroke_width=3))
            lab = T(str(w), 24, MUTED)
            lab.move_to([x_of(w), 0.8, 0])
            ticks.add(lab)
        wpm = ValueTracker(250)
        knob = always_redraw(lambda: Circle(0.2, color=ACCENT, fill_color=ACCENT, fill_opacity=1)
                             .move_to([x_of(wpm.get_value()), 1.3, 0]))
        readout = always_redraw(lambda: T(fmt1(years_at(wpm.get_value())), 96, INK, "BOLD")
                                .move_to([-3.4, -0.6, 0]))
        sub = always_redraw(lambda: T(f"years, reading nonstop at {wpm.get_value():.0f} wpm",
                                      22, MUTED).move_to([-3.4, -1.75, 0]))
        self.add(head, track, ticks, knob, readout, sub)

        # ── right: one bar per speed ──
        base, hmax, xs = -2.4, 3.9, {300: 0.9, 250: 2.4, 200: 3.9, 150: 5.4}
        bars = {}

        def bar(w, color=BLUE):
            h = NONSTOP[w] / NONSTOP[150] * hmax
            r = Rectangle(width=1.0, height=h, fill_color=color, fill_opacity=1, stroke_width=0)
            r.move_to([xs[w], base + h / 2, 0])
            v = T(fmt1(NONSTOP[w]), 22, INK, "BOLD")
            v.move_to([xs[w], base + h + 0.25, 0])
            k = T(f"{w}", 22, MUTED)
            k.move_to([xs[w], base - 0.3, 0])
            return VGroup(r, v, k)

        axis = Line([0.2, base, 0], [6.1, base, 0], color=MUTED, stroke_width=2)
        self.add(axis)
        bars[250] = bar(250)
        c.play(GrowFromEdge(bars[250], DOWN), rt=0.8)

        c.at("Three hundred words a minute")
        c.play(wpm.animate.set_value(300), rt=1.2)
        bars[300] = bar(300)
        c.play(GrowFromEdge(bars[300], DOWN), rt=0.7)

        c.at("Two hundred:")
        c.play(wpm.animate.set_value(200), rt=1.4)
        bars[200] = bar(200)
        c.play(GrowFromEdge(bars[200], DOWN), rt=0.7)

        c.at("One hundred and fifty:")
        c.play(wpm.animate.set_value(150), rt=1.2)
        bars[150] = bar(150)
        c.play(GrowFromEdge(bars[150], DOWN), rt=0.7)

        c.at("twice the fastest")
        c.play(bars[300][0].animate.set_fill(ACCENT), bars[150][0].animate.set_fill(ACCENT), rt=0.6)
        ghost = VGroup(*[Rectangle(width=1.0, height=NONSTOP[300] / NONSTOP[150] * hmax,
                                   stroke_color=INK, stroke_width=3, fill_opacity=0)
                         .move_to([xs[150], base + (i + 0.5) * NONSTOP[300] / NONSTOP[150] * hmax, 0])
                         for i in range(2)])
        c.play(Create(ghost), rt=0.8)
        note = T("half the speed  →  twice the time", 26, ACCENT, "BOLD")
        note.move_to([3.15, 2.45, 0])
        c.play(FadeIn(note), rt=0.5)
        c.finish()


class B05_MoreGuesses(Scene):
    def construct(self):
        c = Clock(self, "B05")
        k = T(KICKER, 18, MUTED)
        k.move_to([-6.1 + k.width / 2, 3.15, 0])
        self.add(k)
        # ── the three guesses ──
        g1 = chip("guess #1  ·  reading speed", 3.9, size=22)
        g1.move_to([-4.15, 2.35, 0])
        g1s = T("shown in the last scene", 18, MUTED)
        g1s.move_to([-4.15, 1.8, 0])
        self.add(g1, g1s)
        g2 = chip("guess #2  ·  words per token", 3.9, size=22, fill=ACCENT_SOFT, stroke=ACCENT)
        g2.move_to([0, 2.35, 0])
        g2s = T("0.75 = a rule of thumb", 18, MUTED)
        g2s.move_to([0, 1.8, 0])
        g3 = chip("guess #3  ·  hours per day", 3.9, size=22, fill=ACCENT_SOFT, stroke=ACCENT)
        g3.move_to([4.15, 2.35, 0])
        g3s = T("assumed: 24 h, no sleep", 18, MUTED)
        g3s.move_to([4.15, 1.8, 0])

        # ── bars, starting at the nonstop (script output) values ──
        base, xs = -2.2, {300: 0.9, 250: 2.4, 200: 3.9, 150: 5.4}
        scale = 3.1 / EIGHT_H[150]
        # one tracker drives the clock, the bar heights and the numbers, so every
        # value on screen is years_at(wpm) x 24 / hours for the hours shown
        hours = ValueTracker(24)

        def make_bars():
            g = VGroup()
            for w in RATES:
                shown = years_at(w) * 24 / round(min(max(hours.get_value(), 8), 24))   # same whole hour as the label
                h = max(shown * scale, 0.01)
                col = ACCENT if w == 250 else BLUE
                r = Rectangle(width=1.0, height=h, fill_color=col, fill_opacity=1, stroke_width=0)
                r.move_to([xs[w], base + h / 2, 0])
                v = T(fmt1(shown), 20, INK, "BOLD")
                v.move_to([xs[w], base + h + 0.22, 0])
                g.add(r, v)
            return g

        bars = always_redraw(make_bars)
        axis = Line([0.2, base, 0], [6.1, base, 0], color=MUTED, stroke_width=2)
        wlabs = VGroup(*[T(f"{w} wpm", 20, MUTED).move_to([xs[w], base - 0.28, 0]) for w in RATES])
        self.add(axis, wlabs, bars)

        c.at("First, zero point seven five")
        c.play(FadeIn(g2, shift=DOWN * 0.1), FadeIn(g2s), rt=0.8)

        c.at("Second, the calculation")
        c.play(FadeIn(g3, shift=DOWN * 0.1), FadeIn(g3s), rt=0.8)
        # 24-hour clock (same `hours` tracker as the bars)
        ctr = np.array([-4.2, -0.55, 0])
        rim = Circle(1.3, color=MUTED, stroke_width=3).move_to(ctr)
        fill = always_redraw(lambda: AnnularSector(inner_radius=0.0, outer_radius=1.25,
                                                   angle=-TAU * hours.get_value() / 24,
                                                   start_angle=PI / 2, fill_color=ACCENT,
                                                   fill_opacity=0.85, stroke_width=0).shift(ctr))
        hl = always_redraw(lambda: T(f"{hours.get_value():.0f} hours of reading per day", 22, INK, "BOLD")
                           .move_to([-4.2, -2.3, 0]))
        c.play(Create(rim), FadeIn(fill), FadeIn(hl), rt=0.9)

        c.at("Read eight hours a day")
        banner = chip("CALCULATED EXTENSION  ·  course formula reading_years() × 24 / hours  ·  not printed by the original script",
                      12.2, h=0.55, size=19, fill=ACCENT_SOFT, stroke=ACCENT)
        banner.move_to([0, -3.1, 0])
        c.play(hours.animate.set_value(8), FadeIn(banner), rt=3.2)

        c.at("One thousand, seven hundred and eleven years becomes")
        hi = VGroup(T("250 words/min:", 22, MUTED), T("1,711.2", 26, INK, "BOLD"),
                    T("→", 26, ACCENT, "BOLD"), T("5,133.5 years", 26, ACCENT, "BOLD")).arrange(RIGHT, buff=0.18)
        fit(hi, 5.0)
        hi.move_to([-3.4, 1.15, 0])
        c.play(FadeIn(hi), rt=0.7)
        c.finish()


class B06_Boundary(Scene):
    def construct(self):
        c = Clock(self, "B06")
        chrome(self, "scope: the reading-time estimate in research/llm_scale.py")
        head = T("WHAT THIS DOES NOT ESTABLISH", 44, ACCENT, "BOLD")
        head.move_to([0, 2.4, 0])
        c.play(FadeIn(head, shift=DOWN * 0.1), rt=0.8)

        c.at("Every version still says")
        ok = VGroup(T("still true:", 26, BLUE, "BOLD"),
                    T("every version is far more than one lifetime (1,426+ years)", 26, INK)
                    ).arrange(RIGHT, buff=0.2)
        ok.move_to([0, 1.5, 0])
        fit(ok, 12)
        c.play(FadeIn(ok), rt=0.7)

        items = [("does not prove the model understood", "✗  that the model understood anything", 0.45),
                 ("or that its answers are accurate", "✗  that its answers are accurate", -0.35),
                 ("does not show that all three hundred billion", "✗  that all 300 billion tokens were unique text", -1.15)]
        for phrase, label, y in items:
            c.at(phrase)
            m = T(label, 34, INK)
            m.move_to([-5.6 + m.width / 2, y, 0])
            c.play(FadeIn(m, shift=RIGHT * 0.2), rt=0.7)

        c.at("It only translates")
        does = chip("What it does: turns a reported token count into\n"
                    "hypothetical human reading time, under stated assumptions", 12.2, h=1.05,
                    size=26, fill=SOFT, stroke=BLUE)
        does.move_to([0, -2.45, 0])
        c.play(FadeIn(does, shift=UP * 0.1), rt=0.8)
        c.finish()


class B07_Close(Scene):
    def construct(self):
        c = Clock(self, "B07")
        chrome(self)
        slogan = T("“thousands of years to read everything GPT-3 was trained on”", 28, MUTED)
        slogan.move_to([0, 2.3, 0])
        fit(slogan, 12)
        tags = VGroup(chip("reading speed", 3.4, size=22, fill=ACCENT_SOFT, stroke=ACCENT),
                      chip("words per token", 3.4, size=22, fill=ACCENT_SOFT, stroke=ACCENT),
                      chip("hours per day", 3.4, size=22, fill=ACCENT_SOFT, stroke=ACCENT))
        for t, x in zip(tags, (-4.0, 0, 4.0)):
            t.move_to([x, 1.3, 0])
        sig = T("Pavithra P.  ·  INFO 7375  ·  Week 01", 22, MUTED)
        sig.move_to([0, -2.7, 0])
        self.add(slogan, sig)
        c.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in tags], lag_ratio=0.25), rt=1.1)

        c.at("What is being divided?")
        q1 = T("What is being divided?", 50, INK, "BOLD")
        q1.move_to([0, -0.1, 0])
        u1 = Line([-3.2, -0.55, 0], [3.2, -0.55, 0], color=ACCENT, stroke_width=4)
        c.play(FadeIn(q1, shift=UP * 0.15), Create(u1), rt=0.7)

        c.at("And what did someone")
        q2 = T("What did someone assume to divide it?", 50, INK, "BOLD")
        q2.move_to([0, -1.25, 0])
        fit(q2, 12)
        u2 = Line([-5.0, -1.7, 0], [5.0, -1.7, 0], color=ACCENT, stroke_width=4)
        c.play(FadeIn(q2, shift=UP * 0.15), Create(u2), rt=0.7)
        c.finish()
