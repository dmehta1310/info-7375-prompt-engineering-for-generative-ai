"""scenes.py — Manim beats for `temperature-is-concentration` (INFO 7375, Week 1).

Four GRAPHIC beats from beat_sheet.json:
    B01A_ContrastSlider    the everyday analogy: a contrast slider rescales
                           differences and never reorders them
    B02_ScoresToProbs      three scores -> one distribution at T = 1
    B04_RatioCollapse      the shared total cancels, leaving the ratio identity;
                           the identity, collapsing across T
    B05_ConcentrationLimit the boundary: concentration is not correctness

EVIDENCE. Every figure on screen was reproduced locally from
chapter1-course/lessons/01-randomness-and-first-prompts/code/main.py
(scores [1, 2, 3], seed 7, n = 1000). Nothing here is invented or rounded up:
probabilities carry 4 dp as printed, ratios 10 dp, and p0 at T = 0.1 is the
exact 2.061060e-09. The one deliberate exaggeration -- the outcome-0 sliver in
B05, which is 2e-09 tall and would be invisible at true scale -- is captioned
on screen as exaggerated, per the assignment's constructed-illustration rule.

PALETTE. Claude fidelity, Manim variant: white canvas, warm ink, ONE terracotta
accent per scene (ai-explainer SKILL.md sec. Step 4/C). No gradients, no glows.

EQUATIONS. Unicode serif, never MathTex -- LaTeX is deliberately not installed,
so nothing here can degrade to raw TeX. Every glyph used (subscripts, e^n,
Sigma, div, times, !=, minus) was verified present in EB Garamond.

GATES. Authored against run.sh gates A/W/B: all text inside the house safe area
(+-6.3, +-3.4), no two text boxes overlapping at any steady state, and no stroke
crossing a label's centerline (run.sh passes --curve-strict).

TIMING. Audio is the master clock. Each scene is built to its MEASURED narration
duration from mp3/timings.json via SETTLE() -- never hand-tuned.
"""
from manim import *

# -- palette ------------------------------------------------------------------
BG    = ManimColor("#FFFFFF")   # white canvas (Manim variant of the cream page)
INK   = ManimColor("#3D3929")   # warm ink -- all body text and bars
ACC   = ManimColor("#D97757")   # terracotta -- ONE accent per scene
SOFT  = ManimColor("#6E6A57")   # secondary labels (contrast 5.4:1 on white)
PAGE  = ManimColor("#FAF9F5")   # Claude page cream -- the B08 brand card only

SERIF = "EB Garamond"           # Claude serif (bundled in runtime/fonts)
MONO  = "PT Mono"               # real error text reads as mono

# -- measured narration durations (mp3/timings.json) = the master clock -------
DUR = {"B01A": 26.18, "B02": 22.42, "B04": 31.25, "B05": 26.30, "B08": 2.47}

# -- verified figures (main.py, scores [1, 2, 3]) ----------------------------
P_T1 = (0.0900305732, 0.2447284711, 0.6652409558)   # T = 1, sums to 1.000000
RATIOS = ("54.5981500331", "7.3890560989", "2.7182818285")   # p2/p0 = e^4/e^2/e^1
P0_AT_T01 = "2.061060e-09"                          # small, not zero


def T_(txt, size=32, color=INK, font=SERIF):
    """House label: serif, ink by default, single line (no italic on multi-word)."""
    return Text(txt, font_size=size, color=color, font=font)


def P(s, *anims, rt=1.0, **kw):
    """play() that books its own run_time against the beat's clock."""
    s.play(*anims, run_time=rt, **kw)
    s._t = getattr(s, "_t", 0.0) + rt


def W(s, t):
    s.wait(t)
    s._t = getattr(s, "_t", 0.0) + t


def SETTLE(s, target, floor=0.5):
    """Hold the settled figure so the beat lands exactly on its measured audio."""
    W(s, max(floor, round(target - getattr(s, "_t", 0.0), 3)))


# -----------------------------------------------------------------------------
#  B01A -- THE CONTRAST SLIDER (the everyday analogy)
#  Three grey swatches under a contrast slider. Sliding up spreads them apart,
#  sliding down washes them toward one flat grey -- and the terracotta marker
#  pinned to the brightest one never moves. That is the whole point: a contrast
#  slider rescales how much things DIFFER and never touches which one is on top,
#  exactly as temperature rescales the log-ratio without reordering anything.
#
#  HONESTY. The brightnesses here are ILLUSTRATIVE, not the measured
#  probabilities -- so no figure from main.py appears in this beat, and the foot
#  caption says so on screen. The ordering claim the analogy makes IS faithful:
#  v = mid + (b - mid) * k is a positive affine map, which cannot reorder its
#  inputs for any k > 0, which is why the marker can be pinned honestly.
# -----------------------------------------------------------------------------
B_BASE = (0.22, 0.44, 0.74)          # relative brightness of outcomes 0, 1, 2
B_MID  = 0.46                        # the grey every swatch washes toward
K_LO, K_HI, K_BASE = 0.15, 1.70, 1.00   # slider travel (no clipping at either end)


class B01A_ContrastSlider(Scene):

    def construct(self):
        self.camera.background_color = BG
        self._t = 0.0

        title = T_("The Contrast Slider", 46).move_to([0.0, 3.02, 0.0])
        cap   = T_("high contrast  \u00b7  low temperature", 28, SOFT).move_to([0.0, 2.16, 0.0])

        k = ValueTracker(K_BASE)

        y_c, w, h, xs = 0.05, 3.2, 2.6, (-3.7, 0.0, 3.7)
        top, bot = y_c + h / 2.0, y_c - h / 2.0

        def shade(b):
            """Contrast as a positive affine rescale about the mid grey."""
            v = B_MID + (b - B_MID) * k.get_value()
            return interpolate_color(INK, WHITE, min(0.97, max(0.03, v)))

        swatches = VGroup(*[
            Rectangle(width=w, height=h, stroke_width=2, stroke_color=INK,
                      fill_color=shade(b), fill_opacity=1.0).move_to([x, y_c, 0.0])
            for x, b in zip(xs, B_BASE)])
        names = VGroup(*[T_("outcome %d" % i, 24, SOFT).move_to([x, bot - 0.45, 0.0])
                         for i, x in enumerate(xs)])

        # the pin: terracotta, on the brightest swatch, never moved once placed
        mk_y = top + 0.30
        marker = Polygon([xs[2] - 0.24, mk_y + 0.22, 0.0],
                         [xs[2] + 0.24, mk_y + 0.22, 0.0],
                         [xs[2], mk_y - 0.18, 0.0],
                         stroke_width=0, fill_color=ACC, fill_opacity=1.0)

        track_y = -2.35
        track = Line([-3.0, track_y, 0.0], [3.0, track_y, 0.0], color=INK, stroke_width=2)
        knob  = Dot(radius=0.15, color=INK).move_to([0.0, track_y, 0.0])
        lo_lb = T_("low contrast", 22, SOFT).move_to([-3.0, track_y - 0.45, 0.0])
        hi_lb = T_("high contrast", 22, SOFT).move_to([3.0, track_y - 0.45, 0.0])
        foot  = T_("analogy \u2014 illustrative, not measured", 20, SOFT).move_to([0.0, -3.20, 0.0])

        def knob_x():
            return -3.0 + 6.0 * (k.get_value() - K_LO) / (K_HI - K_LO)

        # Timed to the words in mp3/words.json, not to feel. The first cut of this
        # scene ran ~3s behind the voice: "slide it up" was spoken at 2.5s and the
        # slider did not move until 6.0s. Each event now lands on its phrase.
        def swap_cap(old, text, color=SOFT, rt=0.6):
            """Cross-fade the caption. NOT Transform(): morphing between Text
            mobjects with different glyph counts renders an unreadable pile of
            letters mid-change (caught in visual QC, 2026-09-22)."""
            new = T_(text, 28, color).move_to([0.0, 2.16, 0.0])
            P(self, FadeOut(old, shift=UP * 0.10), FadeIn(new, shift=UP * 0.10), rt=rt)
            return new

        P(self, Write(title), rt=1.0)                                   # "Think of the contrast slider
        P(self, FadeIn(swatches, shift=UP * 0.2), FadeIn(names), FadeIn(foot),
          Create(track), FadeIn(knob), FadeIn(lo_lb), FadeIn(hi_lb), rt=1.0)  #  on a photo."
        for rect, b in zip(swatches, B_BASE):
            rect.add_updater(lambda m, b=b: m.set_fill(color=shade(b), opacity=1.0))
        knob.add_updater(lambda m: m.move_to([knob_x(), track_y, 0.0]))
        P(self, FadeIn(marker, shift=DOWN * 0.2), rt=0.4)               # pinned before anything moves
        W(self, 0.1)

        P(self, FadeIn(cap), rt=0.5)                                     # 2.5s "Slide it up,
        P(self, k.animate.set_value(K_HI), rt=1.8)                       #  bright parts get brighter
        W(self, 2.8)                                                     #  ... everything pops."

        cap = swap_cap(cap, "low contrast  \u00b7  high temperature")    # 7.7s "Slide it down,
        P(self, k.animate.set_value(K_LO), rt=1.8)                       #  it all washes toward
        W(self, 1.2)                                                     #  the same flat grey."

        cap = swap_cap(cap, "the brightest never changes", INK)          # 11.3s "But the brightest
        W(self, 0.4)                                                     #  pixel stays the brightest."
        P(self, k.animate.set_value(K_BASE), rt=1.4)
        W(self, 1.6)

        cap = swap_cap(cap, "lower temperature  \u2192  higher contrast", INK)  # 15.3s "run backwards:
        W(self, 0.7)
        P(self, k.animate.set_value(K_HI), rt=1.4)                       # 16.6s "lower temperature,
        W(self, 0.9)                                                     #  higher contrast."

        P(self, k.animate.set_value(K_BASE), rt=1.4)                     # 18.9s "It changes how much
        W(self, 2.7)                                                     #  ... never which one is on top."

        cap = swap_cap(cap, "a sharper photo is not a truer photo", INK, rt=0.7)  # 23.0s "And a high-contrast photo

        knob.clear_updaters()
        for rect in swatches:
            rect.clear_updaters()
        SETTLE(self, DUR["B01A"])


# -----------------------------------------------------------------------------
#  B02 -- THE WHOLE MACHINE
#  Three score chips, the softmax line, three bars rising while their values
#  count up, the sum settling at 1.000000 (the beat's one terracotta moment).
# -----------------------------------------------------------------------------
class B02_ScoresToProbs(Scene):

    def construct(self):
        self.camera.background_color = BG
        self._t = 0.0

        title   = T_("The Whole Machine", 46).move_to([0.0, 3.02, 0.0])
        formula = T_("p  =  exp(z / T)  ÷  Σ exp(z / T)", 32, SOFT).move_to([0.0, 2.16, 0.0])

        base_y, scale, xs = -2.05, 4.4, (-4.3, 0.0, 4.3)
        axis = Line([-6.0, base_y, 0.0], [6.0, base_y, 0.0], color=INK, stroke_width=2)

        chips, names = VGroup(), VGroup()
        for i, (x, z) in enumerate(zip(xs, ("1", "2", "3"))):
            chips.add(T_(z, 36).move_to([x, base_y - 0.42, 0.0]))
            names.add(T_("outcome %d" % i, 22, SOFT).move_to([x, base_y - 0.95, 0.0]))

        # one tracker drives bars AND numbers, so the rise and the count are
        # the same motion (MOTION.md: a value counts up, it never bounces).
        grow = ValueTracker(0.0)

        def bar(x, p):
            def build():
                h = max(1e-4, p * scale * grow.get_value())
                r = Rectangle(width=1.5, height=h, stroke_width=0,
                              fill_color=INK, fill_opacity=0.92)
                return r.move_to([x, base_y + h / 2.0, 0.0])
            return always_redraw(build)

        def readout(x, p):
            def build():
                v = p * grow.get_value()
                h = max(1e-4, p * scale * grow.get_value())
                return T_("%.4f" % v, 30).move_to([x, base_y + h + 0.42, 0.0])
            return always_redraw(build)

        bars = VGroup(*[bar(x, p) for x, p in zip(xs, P_T1)])
        vals = VGroup(*[readout(x, p) for x, p in zip(xs, P_T1)])

        sumline = T_("Σ p  =  1.000000", 34, ACC).move_to([0.0, 2.16, 0.0])
        tlabel  = T_("T = 1  ·  baseline", 28, SOFT).move_to([0.0, 1.55, 0.0])

        P(self, Write(title), rt=1.1)
        W(self, 0.3)
        P(self, Create(axis), FadeIn(chips, shift=UP * 0.2), rt=1.0)
        P(self, FadeIn(names), rt=0.8)
        W(self, 0.4)
        P(self, Write(formula), rt=1.9)
        W(self, 0.8)
        self.add(bars, vals)
        P(self, grow.animate.set_value(1.0), rt=6.4)
        W(self, 1.3)
        P(self, Transform(formula, sumline), rt=1.6)
        W(self, 1.1)
        P(self, FadeIn(tlabel), rt=1.0)
        SETTLE(self, DUR["B02"])


# -----------------------------------------------------------------------------
#  B04 -- WATCH THE RATIO
#  First the WHY: p2/p0 written as two fractions over the same total, the total
#  cancels, and what is left is exp((z2 - z0)/T). Then the gap pins at 2 (the
#  accent) and the three ratios collapse down the frame -- each landing on its
#  exact power of e. Last, the conclusion the cancellation forces: T cannot turn
#  a positive gap negative, so the ordering can never flip.
# -----------------------------------------------------------------------------
class B04_RatioCollapse(Scene):

    def construct(self):
        self.camera.background_color = BG
        self._t = 0.0

        title    = T_("Watch The Ratio", 44).move_to([0.0, 3.02, 0.0])
        identity = T_("p\u2082 / p\u2080  =  exp((z\u2082 \u2212 z\u2080) / T)", 34).move_to([0.0, 2.10, 0.0])
        gapnote  = T_("z\u2082 \u2212 z\u2080  =  2   (fixed)", 32, ACC).move_to([0.0, 1.32, 0.0])

        # --- the cancellation (added 2026-09-26) -------------------------------
        # B02 defined p = exp(z/T) / Σ exp(z/T). Divide p2 by p0 and both carry the
        # SAME total underneath, so it cancels; what is left depends only on the
        # gap z2 - z0, divided by T. Earlier cuts only asserted this (as text on
        # B06); here it is shown. Gate-safe by design: the shared totals are BOXED
        # and faded, not struck through -- a stroke across a label is an ERROR
        # under --curve-strict, and the gate is not loosened. Σ is U+03A3, as in B02.
        FS, y_c, dy = 44, -0.20, 0.70
        lhs    = T_("p\u2082 / p\u2080  =", FS)
        num_a  = T_("exp(z\u2082 / T)", FS)
        num_b  = T_("\u00f7  \u03a3 exp(z / T)", FS)
        den_a  = T_("exp(z\u2080 / T)", FS)
        den_b  = T_("\u00f7  \u03a3 exp(z / T)", FS)
        result = T_("=  exp((z\u2082 \u2212 z\u2080) / T)", FS)
        # Explicit coordinates, not computed from Text.width: Gate A checks the
        # scene render-free, where widths are stand-ins, and a width-derived
        # position read as x = -7.5 (off frame). These are laid out from widths
        # MEASURED in EB Garamond at 44 pt -- lhs 1.95, exp(...) 2.45, the total
        # 3.23, the result 4.39 -- leaving 0.45 between parts and 0.20 inside the
        # rule. Before the cancel the expression spans -4.42..4.42; after it,
        # -5.05..5.05 -- both inside the +-6.3 safe width. Gate B checks the
        # rendered pixels, so a font that measured differently would be caught.
        lhs.move_to([-3.44, y_c, 0.0])
        rule = Line([-2.02, y_c, 0.0], [4.42, y_c, 0.0], color=INK, stroke_width=2)
        num_a.move_to([-0.59, y_c + dy, 0.0]); den_a.move_to([-0.59, y_c - dy, 0.0])
        num_b.move_to([2.60, y_c + dy, 0.0]);  den_b.move_to([2.60, y_c - dy, 0.0])
        box_n = SurroundingRectangle(num_b, color=SOFT, buff=0.10, stroke_width=2)
        box_d = SurroundingRectangle(den_b, color=SOFT, buff=0.10, stroke_width=2)

        # after the cancel: lhs | num_a / den_a | = exp((z2 - z0)/T), re-centred
        lhs_to = [-4.07, y_c, 0.0]
        r1, rw2, cx = -2.65, 2.85, -1.22
        result.move_to([2.85, y_c, 0.0])

        rows_y = (0.35, -0.65, -1.65)
        temps  = ("T = 0.5", "T = 1", "T = 2")
        powers = ("=  e\u2074", "=  e\u00b2", "=  e\u00b9")
        # the bar IS the exponent (z2 - z0)/T = 4, 2, 1 -- not a decorative scale.
        expos  = (4.0, 2.0, 1.0)
        BAR_X0, BAR_U = -4.0, 0.62

        tcol, vcol, ecol, bars = VGroup(), VGroup(), VGroup(), VGroup()
        for y, t, r, e, k in zip(rows_y, temps, RATIOS, powers, expos):
            tcol.add(T_(t, 32, SOFT).move_to([-5.2, y, 0.0]))
            vcol.add(T_(r + "  \u00d7", 34).move_to([0.8, y, 0.0]))
            ecol.add(T_(e, 32, SOFT).move_to([4.6, y, 0.0]))
            w = k * BAR_U
            bars.add(Rectangle(width=w, height=0.30, stroke_width=0,
                               fill_color=INK, fill_opacity=0.92
                               ).move_to([BAR_X0 + w / 2.0, y, 0.0]))

        legend = T_("bar length  =  (z\u2082 \u2212 z\u2080) / T", 22, SOFT
                    ).move_to([0.0, -2.30, 0.0])
        strip  = T_("ordering [2, 1, 0]  \u2014  unchanged at every T", 28, SOFT
                    ).move_to([0.0, -2.90, 0.0])

        # Timed to mp3/words.json. Comments give the phrase each play lands on.
        P(self, Write(title), rt=0.8)
        P(self, FadeIn(lhs), Create(rule), FadeIn(num_a), FadeIn(num_b),
          FadeIn(den_a), FadeIn(den_b), rt=1.2)                  # 0.0s  "Divide outcome two by outcome zero."
        W(self, 1.4)
        P(self, Create(box_n), Create(box_d), rt=0.8)            # 3.4s  "the same total underneath,"
        W(self, 0.6)
        P(self, FadeOut(num_b), FadeOut(den_b), FadeOut(box_n), FadeOut(box_d),
          lhs.animate.move_to(lhs_to),
          rule.animate.put_start_and_end_on([r1, y_c, 0.0], [r1 + rw2, y_c, 0.0]),
          num_a.animate.move_to([cx, y_c + dy, 0.0]),
          den_a.animate.move_to([cx, y_c - dy, 0.0]), rt=0.9)   # 4.8s  "so it cancels"
        W(self, 0.3)
        P(self, Write(result), rt=1.3)                           # 6.0s  "what is left depends only on the gap
        W(self, 2.1)
        P(self, FadeOut(VGroup(lhs, rule, num_a, den_a, result), shift=UP * 0.4),
          FadeIn(identity, shift=UP * 0.4), rt=1.0)              # 9.4s   ... divided by T."
        W(self, 0.4)
        P(self, FadeIn(gapnote, shift=DOWN * 0.15), rt=1.0)     # 10.8s "That gap is fixed at two."
        W(self, 0.8)
        # The TABLE FRAME lands before any value: three temperatures and the
        # invariant, spanning the frame top to bottom. Canvas-fill law -- the
        # figure must already occupy the safe area at its midpoint, and a
        # reader needs the axis of comparison before the numbers arrive.
        P(self, LaggedStart(*[FadeIn(t, shift=RIGHT * 0.2) for t in tcol],
                            lag_ratio=0.25), FadeIn(strip), rt=1.2)   # 12.6s "At temperature zero point five"
        W(self, 2.1)
        P(self, FadeIn(vcol[0]), GrowFromEdge(bars[0], LEFT), rt=1.2)  # 15.9s "fifty-four point six"
        W(self, 0.8)
        P(self, FadeIn(vcol[1]), GrowFromEdge(bars[1], LEFT), rt=1.2)  # 17.9s "seven point three nine"
        W(self, 1.3)
        P(self, FadeIn(vcol[2]), GrowFromEdge(bars[2], LEFT), rt=1.2)  # 20.4s "two point seven two"
        W(self, 0.2)
        P(self, FadeIn(legend), rt=0.6)
        P(self, LaggedStart(*[FadeIn(e) for e in ecol], lag_ratio=0.35), rt=2.6)  # 22.4s "exactly e to the fourth ..."
        W(self, 1.9)
        P(self, Indicate(gapnote, scale_factor=1.12, color=ACC), rt=0.8)          # 26.9s "a positive gap"
        W(self, 1.0)
        P(self, strip.animate.set_color(INK).scale(1.12), rt=0.9)               # 28.7s "no two outcomes ever swap places"
        SETTLE(self, DUR["B04"])


# -----------------------------------------------------------------------------
#  B05 -- WHAT THIS DOES NOT ESTABLISH
#  Push T down: outcome 2 dominates but never becomes certain. T = 0 is refused
#  outright. The beat ends on the one line the whole video exists to earn.
# -----------------------------------------------------------------------------
class B05_ConcentrationLimit(Scene):

    def construct(self):
        self.camera.background_color = BG
        self._t = 0.0

        title = T_("What This Does Not Establish", 38).move_to([0.0, 3.02, 0.0])
        tread = T_("T = 1.0", 34, INK).move_to([0.0, 2.15, 0.0])

        base_y, scale = -1.6, 3.6
        axis = Line([-5.6, base_y, 0.0], [5.6, base_y, 0.0], color=INK, stroke_width=2)

        def make_bar(x, h):
            r = Rectangle(width=1.9, height=max(0.05, h), stroke_width=0,
                          fill_color=INK, fill_opacity=0.92)
            return r.move_to([x, base_y + max(0.05, h) / 2.0, 0.0])

        # T = 1 -> T = 0.1. p0 falls 0.0900 -> 2.061060e-09 (a sliver, not zero).
        b0 = make_bar(-3.2, P_T1[0] * scale)
        b2 = make_bar(3.2, P_T1[2] * scale)
        b0_end = make_bar(-3.2, 0.06)
        b2_end = make_bar(3.2, 0.99995460 * scale)

        n0 = T_("outcome 0", 24, SOFT).move_to([-3.2, base_y - 0.45, 0.0])
        n2 = T_("outcome 2", 24, SOFT).move_to([3.2, base_y - 0.45, 0.0])
        honest = T_("sliver exaggerated for visibility", 20, SOFT
                    ).move_to([-3.2, base_y - 0.95, 0.0])

        tread_low = T_("T = 0.1", 34, INK).move_to([0.0, 2.15, 0.0])
        callout   = T_("p\u2080 = " + P0_AT_T01, 28).move_to([-3.2, 0.70, 0.0])
        smallnot  = T_("small, not zero", 26, ACC).move_to([-3.2, 0.15, 0.0])

        card = RoundedRectangle(width=9.4, height=2.6, corner_radius=0.12,
                                stroke_color=ACC, stroke_width=3,
                                fill_color=BG, fill_opacity=1.0).move_to([0.0, -0.20, 0.0])
        err1 = T_("ValueError", 30, ACC, font=MONO).move_to([0.0, 0.42, 0.0])
        err2 = T_("Need logits and a positive", 24, INK, font=MONO).move_to([0.0, -0.28, 0.0])
        err3 = T_("finite temperature", 24, INK, font=MONO).move_to([0.0, -0.86, 0.0])

        # The closing line lands BENEATH the refusal card rather than replacing
        # it: the refusal is the evidence for the claim, so they belong on
        # screen together, and the frame keeps its top-to-bottom span.
        closer = T_("concentration \u2260 correctness", 46).move_to([0.0, -2.55, 0.0])

        # --- the analogy, called back (see B01A) ------------------------------
        # The same three swatches, now at FULL contrast: the picture got
        # sharper and the answer did not get any more correct. Identical
        # encoding to B01A, and B01A already carried the "analogy --
        # illustrative, not measured" caption, so no figure is implied here.
        def _hi(b):
            v = B_MID + (b - B_MID) * K_HI
            return interpolate_color(INK, WHITE, min(0.97, max(0.03, v)))

        echo = VGroup(*[
            Rectangle(width=1.6, height=0.85, stroke_width=2, stroke_color=INK,
                      fill_color=_hi(b), fill_opacity=1.0).move_to([x, 2.05, 0.0])
            for x, b in zip((-2.2, 0.0, 2.2), B_BASE)])
        photoline = T_("a sharper picture of the wrong person", 28, SOFT
                       ).move_to([0.0, -3.12, 0.0])

        P(self, Write(title), rt=1.1)
        W(self, 0.3)
        P(self, Create(axis), FadeIn(tread), FadeIn(b0), FadeIn(b2), rt=1.2)
        P(self, FadeIn(n0), FadeIn(n2), rt=0.8)
        W(self, 0.7)
        P(self, Transform(b0, b0_end), Transform(b2, b2_end),
          Transform(tread, tread_low), rt=5.4)
        P(self, FadeIn(honest), rt=0.8)
        W(self, 0.5)
        P(self, FadeIn(callout, shift=UP * 0.15), rt=1.5)
        P(self, FadeIn(smallnot), rt=1.1)
        W(self, 2.6)
        # T = 0 is refused. Clear the figure and bring the card up in the SAME
        # play -- cross-fading, so no frame is ever left blank.
        P(self, FadeOut(b0), FadeOut(b2), FadeOut(axis), FadeOut(n0), FadeOut(n2),
          FadeOut(honest), FadeOut(callout), FadeOut(smallnot), FadeOut(tread),
          FadeIn(card), FadeIn(err1), FadeIn(err2), FadeIn(err3), rt=1.8)
        P(self, FadeIn(closer, shift=UP * 0.12), rt=1.6)
        W(self, 0.5)
        P(self, FadeIn(echo, shift=DOWN * 0.15), rt=1.0)
        W(self, 0.8)
        P(self, FadeIn(photoline), rt=1.2)
        SETTLE(self, DUR["B05"])


# -----------------------------------------------------------------------------
#  B08 -- TITLE RESTATE + CREDIT (reel-local outro)
#  Renders the outro in-reel rather than depending on a toolkit composition.
#  The shipped Claude title card (ClaudeTitleOutro) is locked to the
#  @NikBearBrown handle by OUTRO-LOCK.md, and the other registered outros carry
#  other brands' palettes -- so crediting this reel to its actual author needed
#  either a new toolkit component or a reel-local scene. This is the reel-local
#  choice: the assignment stays self-contained and the toolkit stays untouched.
#
#  This is the ONE scene here that uses the Claude PAGE cream rather than the
#  white math canvas: it is the brand card, not a figure. OUTRO LAW's shape is
#  kept -- exact title restate, poster serif, terracotta terminal period as the
#  single accent -- and the locked elements (handle, mascot, seeded polarity)
#  are deliberately not borrowed.
# -----------------------------------------------------------------------------
class B08_TitleCredit(Scene):

    def construct(self):
        self.camera.background_color = PAGE
        self._t = 0.0

        # Sized from the rendered frame, not guessed: at 4K the Manim frame is
        # 270 px per unit, so a 29-character line at font_size 66 spans ~10.8
        # units = 84% of the safe width, and spreading the four elements across
        # 5.3 units fills 74% of its height (canvas-fill law).
        line1 = T_("Temperature Is Concentration,", 66).move_to([0.0, 2.55, 0.0])
        # t2c colours the terminal period only -- one object, so the accent can
        # never collide with the word beside it.
        line2 = Text("Not Truth.", font_size=66, color=INK, font=SERIF,
                     t2c={"[-1:]": ACC}).move_to([0.0, 1.50, 0.0])

        credit    = T_("Hemanth Rayudu", 56).move_to([0.0, -0.60, 0.0])
        subcredit = T_("INFO 7375  \u00b7  Week 1", 38, SOFT).move_to([0.0, -2.20, 0.0])

        # A 2.5s outro is sampled for QC at 1.2s, so every element has to be on
        # screen by then -- a staggered reveal leaves the frame half-built at the
        # only moment anyone measures it. Card lands fast, then holds.
        P(self, FadeIn(line1), FadeIn(line2), rt=0.45)
        P(self, FadeIn(credit, shift=UP * 0.10), FadeIn(subcredit), rt=0.45)
        SETTLE(self, DUR["B08"])
