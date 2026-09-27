"""Manim scenes for '665.24 Is Not a Promise' — INFO 7375 Week 1.

Every figure is read from video_data.json, produced by evidence/build_data.py.
No number in this file is typed by hand; if the data changes the frames change.
No LaTeX is used (no MathTex/Tex) so the reel renders without a TeX install.
"""
import json
from pathlib import Path
from manim import *

D = json.loads((Path(__file__).parent / "video_data.json").read_text())

config.background_color = "#0F1115"
INK, DIM, HOT, COOL, WARN = "#F2F3F5", "#8B94A3", "#E8643C", "#4FA8D8", "#E8C13C"
MONO, SANS = "Menlo", "Helvetica Neue"


def mono(t, size=34, color=INK, weight=NORMAL):
    return Text(t, font=MONO, font_size=size, color=color, weight=weight)


def sans(t, size=34, color=INK, weight=NORMAL):
    return Text(t, font=SANS, font_size=size, color=color, weight=weight)


def caption(t):
    return sans(t, 22, DIM).to_edge(DOWN, buff=0.35)


def tick_labels(axis, values, size=20, color=DIM, buff=0.18):
    """Axis tick labels as Text. Manim's include_numbers routes through MathTex,
    which needs a LaTeX install; this reel renders without one."""
    g = VGroup()
    for v in values:
        t = mono(str(v), size, color)
        t.next_to(axis.n2p(v), DOWN, buff=buff)
        g.add(t)
    return g


class B01_TheGap(Scene):
    """main.py output -> the 35-count gap."""
    def construct(self):
        title = sans("lessons/01-randomness-and-first-prompts/code/main.py", 24, DIM)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.8)

        raw = D["lesson_raw"]
        block = mono(
            '"probabilities": [\n'
            f'  {raw["probabilities"][0]:.16f},\n'
            f'  {raw["probabilities"][1]:.16f},\n'
            f'  {raw["probabilities"][2]:.16f}\n'
            '],\n'
            f'"counts": {{"1": {raw["counts"]["1"]}, '
            f'"2": {raw["counts"]["2"]}, "0": {raw["counts"]["0"]}}}',
            size=26, color=COOL)
        block.next_to(title, DOWN, buff=0.6)
        self.play(Write(block), run_time=3.5)
        self.wait(1.8)

        exp_v, obs_v = D["expected"], D["observed"]
        left = VGroup(sans("EXPECTED", 26, DIM), mono(f"{exp_v:.2f}", 76, INK)).arrange(DOWN, buff=0.25)
        right = VGroup(sans("OBSERVED", 26, DIM), mono(f"{obs_v}", 76, HOT)).arrange(DOWN, buff=0.25)
        pair = VGroup(left, right).arrange(RIGHT, buff=2.4).shift(DOWN * 0.6)

        self.play(block.animate.set_opacity(0.18).scale(0.8).to_edge(UP, buff=1.2),
                  FadeIn(left, shift=UP), run_time=1.4)
        self.play(FadeIn(right, shift=UP), run_time=1.0)
        self.wait(1.2)

        br = Brace(pair, DOWN, color=DIM)
        lbl = mono(f"{D['shortfall']:+.2f}", 44, HOT).next_to(br, DOWN, buff=0.25)
        self.play(GrowFromCenter(br), FadeIn(lbl), run_time=1.6)
        self.wait(1.4)

        q = sans("is the code broken?", 40, WARN).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(q, shift=UP), run_time=1.0)
        self.wait(2.3)


class B02_TwoKinds(Scene):
    """Expected count defined as p x n; contrasted with an observed count."""
    def construct(self):
        p, n, exp_v, obs = D["p"], D["n"], D["expected"], D["observed"]

        head = sans("two numbers, two different kinds of thing", 30, DIM).to_edge(UP, buff=0.6)
        self.play(FadeIn(head), run_time=0.8)

        l_title = sans("EXPECTED COUNT", 26, COOL)
        l_calc = mono(f"{p:.16f}", 30, INK)
        l_x = mono(f"x {n}", 30, DIM)
        l_line = Line(LEFT * 1.9, RIGHT * 1.9, color=DIM, stroke_width=2)
        l_res = mono(f"{exp_v:.10f}", 34, INK)
        left = VGroup(l_title, l_calc, l_x, l_line, l_res).arrange(DOWN, buff=0.28)
        left.shift(LEFT * 3.4)

        self.play(FadeIn(l_title), run_time=0.6)
        self.play(Write(l_calc), run_time=2.4)
        self.play(Write(l_x), Create(l_line), run_time=0.9)
        self.play(Write(l_res), run_time=2.0)
        self.wait(1.6)

        frac = l_res[-11:]
        ring = SurroundingRectangle(frac, color=WARN, stroke_width=3, buff=0.07)
        note = sans("you cannot draw a fraction of a token", 22, WARN).next_to(ring, DOWN, buff=0.28)
        self.play(Create(ring), FadeIn(note), run_time=1.6)
        self.wait(3.0)

        r_title = sans("OBSERVED COUNT", 26, HOT)
        r_num = mono(f"{obs}", 96, HOT)
        r_note = sans("happened once\nseed 7", 22, DIM)
        right = VGroup(r_title, r_num, r_note).arrange(DOWN, buff=0.35).shift(RIGHT * 3.4)
        self.play(FadeIn(r_title), run_time=0.6)
        self.play(FadeIn(r_num, scale=1.3), run_time=1.0)
        self.play(FadeIn(r_note), run_time=0.9)
        self.wait(2.4)

        self.play(FadeIn(caption("a rate x a count  |  a thing that happened")), run_time=0.8)
        self.wait(3.0)


class B03_HowBigIsANormalMiss(Scene):
    """Binomial SD computed on screen; 630 placed against the bands."""
    def construct(self):
        p, n, exp_v, obs, sd, z = (D["p"], D["n"], D["expected"],
                                   D["observed"], D["sd"], D["z"])
        head = sans("how big is a normal miss?", 32, DIM).to_edge(UP, buff=0.5)
        self.play(FadeIn(head), run_time=0.8)

        f1 = mono("sd = sqrt( n x p x (1 - p) )", 36, INK).next_to(head, DOWN, buff=0.7)
        self.play(Write(f1), run_time=1.6)
        self.wait(0.8)
        f2 = mono(f"   = sqrt( {n} x {p:.6f} x {1-p:.6f} )", 32, COOL).next_to(f1, DOWN, buff=0.3)
        self.play(Write(f2), run_time=2.6)
        self.wait(1.2)
        f3 = mono(f"   = {sd:.6f}", 40, WARN).next_to(f2, DOWN, buff=0.3)
        self.play(Write(f3), run_time=1.6)
        self.wait(2.4)

        formula = VGroup(f1, f2, f3)
        self.play(FadeOut(head),
                  formula.animate.scale(0.52).to_corner(UL, buff=0.45)
                  .set_opacity(0.5), run_time=1.2)

        lo, hi = 600, 730
        axis = NumberLine(x_range=[lo, hi, 20], length=11, color=DIM).shift(DOWN * 0.9)
        ticks = tick_labels(axis, range(600, 740, 20))
        self.play(Create(axis), FadeIn(ticks), run_time=1.3)

        def X(v):
            return axis.n2p(v)

        b2 = Rectangle(width=axis.n2p(D["band2"][1])[0]-axis.n2p(D["band2"][0])[0],
                       height=1.5, fill_color=COOL, fill_opacity=0.12, stroke_width=0)
        b2.move_to(X(exp_v)).shift(UP * 0.0)
        b1 = Rectangle(width=axis.n2p(D["band1"][1])[0]-axis.n2p(D["band1"][0])[0],
                       height=1.5, fill_color=COOL, fill_opacity=0.22, stroke_width=0)
        b1.move_to(X(exp_v))
        self.play(FadeIn(b2), FadeIn(b1), run_time=1.0)

        l2 = sans(f"±2 sd   {D['band2'][0]:.1f} – {D['band2'][1]:.1f}", 20, DIM)
        l2.next_to(b2, UP, buff=0.15).align_to(b2, LEFT).shift(LEFT * 0.2)
        self.play(FadeIn(l2), run_time=0.7)

        mean_line = DashedLine(X(exp_v)+UP*0.85, X(exp_v)+DOWN*0.85, color=INK, stroke_width=3)
        mean_lbl = mono(f"{exp_v:.2f}", 24, INK).next_to(mean_line, UP, buff=0.55)
        self.play(Create(mean_line), FadeIn(mean_lbl), run_time=0.9)
        self.wait(0.8)

        dot = Dot(X(obs), radius=0.13, color=HOT)
        dot_lbl = mono(f"{obs}", 30, HOT).next_to(dot, DOWN, buff=0.35)
        self.play(FadeIn(dot, scale=2), FadeIn(dot_lbl), run_time=1.4)
        self.wait(2.0)

        zl = sans(f"z = {z:.2f}     outside two standard deviations", 28, HOT)
        zl.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(zl, shift=UP), run_time=1.2)
        self.wait(3.6)


class B04_TenThousandSeeds(Scene):
    """Histogram of 10,000 real runs assembling."""
    def construct(self):
        hist = {int(k): v for k, v in D["histogram"].items()}
        lo, hi = D["min"], D["max"]
        head = sans(f"the same sampler, {D['trials']:,} times — only the seed changes",
                    28, DIM).to_edge(UP, buff=0.5)
        self.play(FadeIn(head), run_time=0.9)

        axis = NumberLine(x_range=[600, 730, 20], length=11.5, color=DIM).shift(DOWN * 2.2)
        ticks = tick_labels(axis, range(600, 740, 20))
        self.play(Create(axis), FadeIn(ticks), run_time=1.1)

        peak = max(hist.values())
        max_h = 4.2
        bars = VGroup()
        for v, c in sorted(hist.items()):
            w = (axis.n2p(601)[0] - axis.n2p(600)[0])
            bar = Rectangle(width=w * 0.92, height=max(c / peak * max_h, 0.012),
                            fill_color=COOL, fill_opacity=0.85, stroke_width=0)
            bar.move_to(axis.n2p(v), aligned_edge=DOWN)
            bars.add(bar)

        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars],
                              lag_ratio=0.010), run_time=11.0)
        self.wait(2.0)

        mo, so = D["mean_obs"], D["sd_obs"]
        ml = Line(axis.n2p(mo) + DOWN * 0.15, axis.n2p(mo) + UP * max_h,
                  color=WARN, stroke_width=4)
        self.play(Create(ml), run_time=1.6)
        self.wait(1.5)

        panel = VGroup(
            sans("MEASURED", 20, DIM), mono(f"mean  {mo}", 26, WARN),
            mono(f"sd    {so:.4f}", 26, WARN),
            sans("PREDICTED BY FORMULA", 20, DIM),
            mono(f"mean  {D['expected']:.2f}", 26, INK),
            mono(f"sd    {D['sd']:.4f}", 26, INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        panel.to_corner(UR, buff=0.5).shift(DOWN * 0.3)
        self.play(FadeIn(panel, shift=LEFT), run_time=1.8)
        self.wait(4.5)

        verdict = sans("the sampler is doing exactly what the probability says",
                       28, WARN).to_edge(DOWN, buff=0.12)
        self.play(FadeIn(verdict, shift=UP), run_time=1.2)
        self.wait(4.0)


class B05_WhereSeedSevenLands(Scene):
    """630 located in the left tail of the measured distribution."""
    def construct(self):
        hist = {int(k): v for k, v in D["histogram"].items()}
        obs = D["observed"]
        head = sans("where does 630 fall?", 32, DIM).to_edge(UP, buff=0.5)
        self.play(FadeIn(head), run_time=0.8)

        axis = NumberLine(x_range=[600, 730, 20], length=11.5, color=DIM).shift(DOWN * 2.2)
        peak, max_h = max(hist.values()), 4.2
        bars, tail_bars = VGroup(), []
        for v, c in sorted(hist.items()):
            w = (axis.n2p(601)[0] - axis.n2p(600)[0])
            bar = Rectangle(width=w * 0.92, height=max(c / peak * max_h, 0.012),
                            fill_color=COOL, fill_opacity=0.5, stroke_width=0)
            bar.move_to(axis.n2p(v), aligned_edge=DOWN)
            bars.add(bar)
            if v <= obs:
                tail_bars.append(bar)
        self.add(axis, tick_labels(axis, range(600, 740, 20)), bars)
        self.wait(0.8)

        self.play(*[b.animate.set_fill(HOT, opacity=1.0) for b in tail_bars], run_time=2.6)
        self.wait(1.2)

        cnt = D["at_or_below"]
        tally = VGroup(
            mono(f"{cnt}", 64, HOT),
            sans(f"of {D['trials']:,} seeds at or below {obs}", 24, DIM),
            mono(f"{D['pct_at_or_below']:.2f}th percentile", 34, HOT),
        ).arrange(DOWN, buff=0.2).to_corner(UL, buff=0.55)
        self.play(FadeIn(tally, shift=RIGHT), run_time=1.8)
        self.wait(2.6)

        p1 = D["percentiles"]["1"]
        p1l = DashedLine(axis.n2p(p1) + DOWN * 0.1, axis.n2p(p1) + UP * 1.5,
                         color=WARN, stroke_width=3)
        p1t = sans(f"p1 = {p1}", 22, WARN).next_to(p1l, UP, buff=0.12)
        self.play(Create(p1l), FadeIn(p1t), run_time=1.0)

        mlab = mono(f"{obs}", 30, HOT).next_to(axis.n2p(obs), DOWN, buff=0.62)
        mtick = Line(axis.n2p(obs) + DOWN * 0.08, axis.n2p(obs) + DOWN * 0.46,
                     color=HOT, stroke_width=3)
        self.play(Create(mtick), FadeIn(mlab), run_time=1.0)
        self.wait(2.4)

        ladder = VGroup(*[sans(f"p{q:<3} {D['percentiles'][q]}", 21, DIM)
                          for q in ("1", "5", "25", "50", "75", "95", "99")])
        ladder.arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UR, buff=0.6)
        self.play(FadeIn(ladder, shift=LEFT), run_time=1.4)
        self.wait(2.4)

        verdict = sans("not wrong — unusual, and shipped as the default",
                       28, WARN).to_edge(DOWN, buff=0.12)
        self.play(FadeIn(verdict, shift=UP), run_time=1.2)
        self.wait(3.2)


class B06_WhatThisDoesNotEstablish(Scene):
    """Two candidate distributions, both passing through 630."""
    def construct(self):
        import math
        obs, n = D["observed"], D["n"]
        p_fair, p_bias = D["p"], D["biased_p"]

        head = sans("what this does not establish", 34, WARN).to_edge(UP, buff=0.5)
        self.play(FadeIn(head), run_time=0.9)

        ax = Axes(x_range=[590, 740, 25], y_range=[0, 0.030, 0.01],
                  x_length=11, y_length=4.2,
                  axis_config={"color": DIM}).shift(DOWN * 0.8)
        xt = VGroup()
        for v in range(600, 741, 25):
            xt.add(mono(str(v), 19, DIM).next_to(ax.c2p(v, 0), DOWN, buff=0.18))
        self.play(Create(ax), FadeIn(xt), run_time=1.3)

        def pmf(k, pp):
            return math.exp(math.lgamma(n+1) - math.lgamma(k+1) - math.lgamma(n-k+1)
                            + k*math.log(pp) + (n-k)*math.log1p(-pp))

        fair = ax.plot(lambda x: pmf(int(round(x)), p_fair), x_range=[590, 740, 1], color=COOL)
        fl = sans(f"fair sampler   p = {p_fair:.4f}", 22, COOL)
        fl.to_corner(UR, buff=0.8).shift(DOWN * 0.85)
        self.play(Create(fair), FadeIn(fl), run_time=4.0)
        self.wait(2.5)

        bias = ax.plot(lambda x: pmf(int(round(x)), p_bias), x_range=[590, 740, 1], color=HOT)
        bl = sans(f"biased sampler   p = {p_bias:.4f}", 22, HOT)
        bl.to_corner(UL, buff=0.8).shift(DOWN * 0.85)
        self.play(Create(bias), FadeIn(bl), run_time=4.0)
        self.wait(2.5)

        vline = DashedLine(ax.c2p(obs, 0), ax.c2p(obs, 0.029), color=INK, stroke_width=3)
        vlab = mono(f"{obs}", 28, INK).next_to(ax.c2p(obs, 0), DOWN, buff=0.62)
        self.play(Create(vline), FadeIn(vlab), run_time=1.5)
        self.wait(1.0)

        d1 = Dot(ax.c2p(obs, D["p_obs_given_fair"]), color=COOL, radius=0.10)
        d2 = Dot(ax.c2p(obs, D["p_obs_given_biased"]), color=HOT, radius=0.10)
        t1 = mono(f"{D['p_obs_given_fair']:.6f}", 22, COOL).next_to(d1, LEFT, buff=0.2)
        t2 = mono(f"{D['p_obs_given_biased']:.6f}", 22, HOT).next_to(d2, RIGHT, buff=0.2)
        self.play(FadeIn(d1, scale=2), FadeIn(t1), run_time=0.9)
        self.play(FadeIn(d2, scale=2), FadeIn(t2), run_time=1.2)
        self.wait(2.2)

        ratio = sans(f"{D['p_obs_given_biased']/D['p_obs_given_fair']:.1f}x more readily",
                     26, HOT).next_to(t2, DOWN, buff=0.25)
        self.play(FadeIn(ratio), run_time=1.0)
        self.wait(3.0)

        chart = VGroup(ax, xt, fair, bias, vline, vlab, d1, d2, fl, bl, t1, t2, ratio)
        self.play(chart.animate.set_opacity(0.10), FadeOut(head), run_time=1.2)

        shown = VGroup(sans("shown", 24, COOL),
                       sans("630 is consistent with a fair sampler", 30, COOL)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        notshown = VGroup(sans("not shown", 24, HOT),
                          sans("that a fair sampler is the only thing", 30, HOT),
                          sans("that could have produced it", 30, HOT)
                          ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        card = VGroup(shown, notshown).arrange(DOWN, aligned_edge=LEFT, buff=0.7)
        card.move_to(ORIGIN)
        self.play(FadeIn(shown, shift=UP), run_time=1.2)
        self.wait(1.4)
        self.play(FadeIn(notshown, shift=UP), run_time=1.2)
        self.wait(4.0)


class B00_Title(Scene):
    """Opening card: who, what, and the question the reel answers."""
    def construct(self):
        title = sans("665.24 Is Not a Promise", 62, INK)
        rule = Line(LEFT * 4.6, RIGHT * 4.6, color=DIM, stroke_width=1)
        who = sans("Riya Kapadnis   ·   INFO 7375   ·   Week 1 Explainer", 28, DIM)
        top = VGroup(title, rule, who).arrange(DOWN, buff=0.42).shift(UP * 1.35)

        self.play(FadeIn(title, shift=UP), run_time=2.2)
        self.wait(1.2)
        self.play(Create(rule), FadeIn(who), run_time=1.6)
        self.wait(2.4)

        sub = sans("one concept from Chapter 1", 24, WARN)
        q = VGroup(
            sans("The sampler predicts token 2 appears", 32, INK),
            sans("665.24 times in 1000 draws.", 32, COOL),
            sans("It came up 630.", 32, HOT),
        ).arrange(DOWN, buff=0.22)
        ask = sans("What does an expected count actually claim?", 30, WARN)
        body = VGroup(sub, q, ask).arrange(DOWN, buff=0.55).shift(DOWN * 1.35)

        self.play(FadeIn(sub), run_time=1.0)
        self.wait(0.8)
        for ln in q:
            self.play(FadeIn(ln, shift=UP), run_time=1.1)
            self.wait(0.9)
        self.wait(1.6)
        self.play(FadeIn(ask, shift=UP), run_time=1.5)
        self.wait(4.2)


class B07_Conclusion(Scene):
    """Closing: what the reel established, in three lines."""
    def construct(self):
        head = sans("what 630 turned out to mean", 34, DIM).to_edge(UP, buff=0.9)
        self.play(FadeIn(head), run_time=1.2)
        self.wait(1.8)

        lines = VGroup(
            VGroup(sans("not a bug.", 34, COOL),
                   sans("an expected count is a rate times a number of draws —", 26, DIM),
                   sans("not a promise about any one run", 26, DIM)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
            VGroup(sans("the sampler is fair.", 34, COOL),
                   sans(f"{D['trials']:,} runs averaged {D['mean_obs']} "
                        f"against a predicted {D['expected']:.2f}", 26, DIM)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
            VGroup(sans("and seed 7 is unusual.", 34, WARN),
                   sans(f"{D['at_or_below']} of {D['trials']:,} seeds landed at or below it — "
                        f"the {D['pct_at_or_below']:.2f}th percentile", 26, DIM)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.55).shift(UP * 0.35)

        for ln in lines:
            self.play(FadeIn(ln, shift=RIGHT), run_time=1.6)
            self.wait(3.5)
        self.wait(2.0)

        rule = Line(LEFT * 5.4, RIGHT * 5.4, color=DIM, stroke_width=1)
        rule.next_to(lines, DOWN, buff=0.5)
        last = VGroup(
            sans("reproducing a number is not the same as", 30, HOT),
            sans("knowing why you got it.", 30, HOT),
        ).arrange(DOWN, buff=0.12).next_to(rule, DOWN, buff=0.4)
        self.play(Create(rule), run_time=0.9)
        self.play(FadeIn(last, shift=UP), run_time=1.8)
        self.wait(6.5)
