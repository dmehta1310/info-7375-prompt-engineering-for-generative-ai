from manim import *

config.background_color = WHITE

TEXT_COLOR = "#1A1A1A"
SOURCE_COLOR = "#666666"

RED, ORANGE, BLUE = "#E4572E", "#F3A712", "#2E86AB"
COLORS = [RED, ORANGE, BLUE]
LOGITS = [1, 2, 3]
PROBS = [0.09003057317038046, 0.24472847105479764, 0.6652409557748218]
COUNTS_SEED7 = {0: 102, 1: 268, 2: 630}
COUNTS_SEED42 = {0: 76, 1: 253, 2: 671}
COUNTS_SEED99 = {0: 93, 1: 267, 2: 640}
EXPECTED = {i: p * 1000 for i, p in enumerate(PROBS)}


def source_label(text):
    return Text(text, font_size=18, color=SOURCE_COLOR).to_corner(DOWN + RIGHT, buff=0.25)


class BeatIntro(Scene):
    def construct(self):
        ACCENT = "#C1652F"
        DARK = "#26251F"
        CREAM = "#F5F0E8"
        self.camera.background_color = CREAM

        kicker = Text(
            "INFO 7375 · WEEK 1 · EXPECTED VS OBSERVED",
            font_size=30, color=ACCENT, weight=BOLD
        ).to_corner(UP + LEFT, buff=0.8)

        name_line = Text(
            "Pavan Jayant Majji - 002376453",
            font_size=40, color=DARK, weight=BOLD, font="Georgia"
        )
        name_line.to_edge(DOWN, buff=1.2)
        name_line.align_to(kicker, LEFT)

        self.play(FadeIn(kicker, shift=DOWN * 0.2))
        self.wait(0.5)
        self.play(Write(name_line))
        self.wait(3)


class Beat00Hook(Scene):
    def construct(self):
        dots = VGroup(*[
            Circle(radius=0.5, fill_color=c, fill_opacity=1, stroke_width=0).shift(RIGHT * 2 * (i - 1))
            for i, c in enumerate(COLORS)
        ])
        q = Text("How many blues in 1000 tries?", font_size=32, color=TEXT_COLOR).to_edge(DOWN)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.3))
        self.play(Write(q))
        self.wait(3)


class Beat01Setup(Scene):
    def construct(self):
        logit_bars = VGroup(*[
            Rectangle(width=1.2, height=v, fill_color=COLORS[i], fill_opacity=0.9, stroke_width=0)
                .move_to(RIGHT * 2.5 * (i - 1) + UP * (v / 2 - 2))
            for i, v in enumerate(LOGITS)
        ])
        logit_labels = VGroup(*[
            Text(f"logit = {v}", font_size=24, color=TEXT_COLOR).next_to(logit_bars[i], DOWN)
            for i, v in enumerate(LOGITS)
        ])
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in logit_bars], lag_ratio=0.2))
        self.play(Write(logit_labels))
        self.wait(1)

        prob_bars = VGroup(*[
            Rectangle(width=1.2, height=p * 6, fill_color=COLORS[i], fill_opacity=0.9, stroke_width=0)
                .move_to(RIGHT * 2.5 * (i - 1) + UP * (p * 6 / 2 - 2))
            for i, p in enumerate(PROBS)
        ])
        prob_labels = VGroup(*[
            Text(f"{p:.3f}", font_size=24, color=TEXT_COLOR).next_to(prob_bars[i], DOWN)
            for i, p in enumerate(PROBS)
        ])
        softmax_label = Text("softmax", font_size=28, color=TEXT_COLOR).to_edge(UP)
        self.play(Write(softmax_label))
        self.play(
            *[Transform(logit_bars[i], prob_bars[i]) for i in range(3)],
            *[Transform(logit_labels[i], prob_labels[i]) for i in range(3)],
            run_time=2
        )
        self.wait(0.5)
        self.play(FadeIn(source_label("Source: main.py -- logits=[1, 2, 3]")))
        self.wait(3)


class Beat02Expected(Scene):
    def construct(self):
        eq = Text("0.6652 x 1000 = 665.24", font_size=44, color=TEXT_COLOR)
        self.play(Write(eq))
        self.wait(1.5)
        note = Text("You can never observe a fraction of a trial", font_size=28, color=BLUE).next_to(eq, DOWN, buff=0.8)
        self.play(FadeIn(note))
        self.play(FadeIn(source_label("Source: main.py -- softmax(logits=[1, 2, 3])")))
        self.wait(3)


class Beat03Observed(Scene):
    def construct(self):
        title = Text("1000 real draws, seed = 7", font_size=32, color=TEXT_COLOR).to_edge(UP)
        self.play(Write(title))

        positions = {0: LEFT * 4, 1: ORIGIN, 2: RIGHT * 4}
        dots = VGroup()
        for i in range(3):
            for k in range(min(COUNTS_SEED7[i], 60)):
                d = Dot(radius=0.06, color=COLORS[i]).move_to(
                    positions[i] + UP * (k // 10) * 0.15 + RIGHT * (k % 10) * 0.15 + DOWN * 2
                )
                dots.add(d)
        self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.3) for d in dots], lag_ratio=0.01), run_time=3)

        counts_text = VGroup(*[
            Text(f"{COUNTS_SEED7[i]}", font_size=36, color=COLORS[i]).move_to(positions[i] + UP * 1.5)
            for i in range(3)
        ])
        self.play(Write(counts_text))
        self.play(FadeIn(source_label("Source: main.py -- 1000 samples, seed=7")))
        self.wait(2)


class Beat04SecondSeeds(Scene):
    def construct(self):
        title = Text("Same probabilities, different seeds", font_size=32, color=TEXT_COLOR).to_edge(UP)
        self.play(Write(title))

        rows_data = [("seed = 7", COUNTS_SEED7[2]), ("seed = 42", COUNTS_SEED42[2]), ("seed = 99", COUNTS_SEED99[2])]
        group = VGroup()
        count_texts = []
        for i, (label, count) in enumerate(rows_data):
            label_text = Text(label, font_size=28, color=TEXT_COLOR).set_x(-3)
            count_text = Text(str(count), font_size=32, color=BLUE).set_x(1)
            row = VGroup(label_text, count_text).arrange(RIGHT, buff=1.5).shift(UP * (1 - i))
            group.add(row)
            count_texts.append(count_text)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in group], lag_ratio=0.3))
        self.wait(1)

        target = DashedLine(LEFT * 5, RIGHT * 5, color="#555555").shift(DOWN * 1.6)
        target_label = Text("expected: 665.24", font_size=24, color="#555555").next_to(target, DOWN)
        self.play(Create(target), Write(target_label))
        self.play(FadeIn(source_label("Source: main.py -- seeds 42 & 99")))
        self.wait(1)

        expected_val = EXPECTED[2]
        order = [0, 1, 2, 0, 1, 2]

        box = SurroundingRectangle(count_texts[order[0]], color=BLUE, buff=0.15)
        diff = rows_data[order[0]][1] - expected_val
        diff_label = Text(f"{diff:+.2f}", font_size=26, color=BLUE).next_to(count_texts[order[0]], UP, buff=0.2)
        self.play(Create(box), Write(diff_label))
        self.wait(1.6)

        for i in order[1:]:
            new_box = SurroundingRectangle(count_texts[i], color=BLUE, buff=0.15)
            diff = rows_data[i][1] - expected_val
            new_label = Text(f"{diff:+.2f}", font_size=26, color=BLUE).next_to(count_texts[i], UP, buff=0.2)
            self.play(Transform(box, new_box), Transform(diff_label, new_label), run_time=1.2)
            self.wait(1.6)

        self.wait(1)


class Beat05Coin(Scene):
    def construct(self):
        title = Text("Why the gap isn't a bug", font_size=32, color=TEXT_COLOR).to_edge(UP)
        self.play(Write(title))

        coins = VGroup(*[Circle(radius=0.3, fill_color="#EEEEEE", fill_opacity=1, stroke_color=TEXT_COLOR) for _ in range(10)])
        coins.arrange(RIGHT, buff=0.3).shift(UP * 0.5)
        self.play(LaggedStart(*[GrowFromCenter(c) for c in coins], lag_ratio=0.1))

        labels = VGroup(*[Text("H" if i % 2 == 0 else "T", font_size=20, color=TEXT_COLOR).move_to(coins[i]) for i in range(10)])
        self.play(Write(labels))

        note = Text("expect 5 heads -- getting 4 or 6 doesn't mean it's broken", font_size=24, color=TEXT_COLOR).next_to(coins, DOWN, buff=0.8)
        self.play(FadeIn(note))
        self.wait(4)


class Beat06Comparison(Scene):
    def construct(self):
        D = 200
        exp_bars = VGroup(*[
            Rectangle(width=0.8, height=EXPECTED[i] / D, fill_color=COLORS[i], fill_opacity=0.4, stroke_width=2, stroke_color=COLORS[i])
                .move_to(LEFT * 3 + RIGHT * 1.2 * i + UP * (EXPECTED[i] / (2 * D)))
            for i in range(3)
        ])
        obs_bars = VGroup(*[
            Rectangle(width=0.8, height=COUNTS_SEED7[i] / D, fill_color=COLORS[i], fill_opacity=0.9, stroke_width=0)
                .move_to(RIGHT * 1.5 + RIGHT * 1.2 * i + UP * (COUNTS_SEED7[i] / (2 * D)))
            for i in range(3)
        ])
        exp_title = Text("Expected", font_size=28, color=TEXT_COLOR).next_to(exp_bars, DOWN, buff=0.5)
        obs_title = Text("Observed", font_size=28, color=TEXT_COLOR).next_to(obs_bars, DOWN, buff=0.5)

        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in exp_bars], lag_ratio=0.15), Write(exp_title))
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in obs_bars], lag_ratio=0.15), Write(obs_title))

        # Shift DOWN only -- do not next_to() against obs_title, since that
        # recenters horizontally on the whole Observed group (the yellow
        # bar's x-position) instead of keeping alignment under obs_bars[2].
        gap = Brace(obs_bars[2], direction=DOWN, color=TEXT_COLOR)
        gap.shift(DOWN * (gap.get_top()[1] - obs_title.get_bottom()[1] + 0.3))
        gap_label = Text("sampling variance", font_size=24, color=TEXT_COLOR).next_to(gap, DOWN, buff=0.2)
        self.play(GrowFromCenter(gap), Write(gap_label))
        self.play(FadeIn(source_label("Source: main.py -- expected vs. observed, seed=7")))
        self.wait(3)


class Beat07Boundary(Scene):
    def construct(self):
        line1 = Text("Boundary:", font_size=32, color=TEXT_COLOR)
        line2 = Text("repeatable != true", font_size=32, color=TEXT_COLOR)
        line3 = Text("doesn't show what deviation is normal", font_size=32, color=TEXT_COLOR)
        lines = VGroup(line1, line2, line3).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        lines.move_to(ORIGIN)

        self.play(FadeIn(line1, shift=UP * 0.3))
        self.wait(4)
        self.play(FadeIn(line2, shift=UP * 0.3))
        self.wait(4)
        self.play(FadeIn(line3, shift=UP * 0.3))
        self.wait(4.5)


class Beat08Recap(Scene):
    def construct(self):
        line1 = Text("Probability = a prediction over many trials", font_size=30, color=TEXT_COLOR)
        line2 = Text("Not a guarantee about any one trial", font_size=30, color=TEXT_COLOR)
        VGroup(line1, line2).arrange(DOWN, buff=0.5)

        self.play(Write(line1))
        self.wait(1)
        self.play(Write(line2))
        self.wait(1)

        # Manim skips spaces when building per-character submobjects, so
        # these indices count only non-space characters -- confirmed via
        # a diagnostic (37 submobjects for a 43-char string with 6 spaces).
        # "Probability"(11) + "="(1) + "a"(1) = 13 -> "prediction" starts at 13, len 10
        # "Not"(3) + "a"(1) = 4 -> "guarantee" starts at 4, len 9
        prediction_word = line1[13:23]
        guarantee_word = line2[4:13]

        self.play(Indicate(prediction_word, color=BLUE, scale_factor=1.15), run_time=1.2)
        self.wait(1.8)
        self.play(Indicate(guarantee_word, color=RED, scale_factor=1.15), run_time=1.2)
        self.wait(1.8)
        self.play(Indicate(prediction_word, color=BLUE, scale_factor=1.15), run_time=1.2)
        self.wait(1.8)
        self.play(Indicate(guarantee_word, color=RED, scale_factor=1.15), run_time=1.2)
        self.wait(2.5)

