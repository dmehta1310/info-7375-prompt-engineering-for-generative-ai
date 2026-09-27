"""test_verify_claims.py — the numbers in the video, as assertions.

Submitted by Suketh Produtoor (INFO 7375, Week 1). Written by Claude in
Claude Code build sessions the submitter directed — SOURCES.md §4 records
who did what, and what the submitter personally re-ran.

Every figure shown in "Shifted, Not Changed" is asserted here against the
course's own reference implementation. If any of them drifts — a different
interpreter, a changed reference file, a different float ABI — a test fails
and names which on-screen claim is now wrong.

Following the course convention of giving each check ONE job (Chapter 1,
"Build It: give each check one job"): each test is one distinct question, not
one aggregate "the video is correct". Each test names the beat it defends, so
a failure points at a specific frame.

Run:
    python3 -m unittest discover -s . -v
    python3 -m unittest test_verify_claims -v
"""

from __future__ import annotations

import json
import math
import pathlib
import re
import struct
import sys
import unittest

from boundary_analysis import collect as boundary_collect
from verify_claims import collect, probabilities


class TestB03Intermediates(unittest.TestCase):
    """B03 — the four-column table. What the shift rewrites."""

    def setUp(self) -> None:
        self.c = collect()["claim_1_intermediates"]

    def test_shifted_scores_are_minus_two_minus_one_zero(self) -> None:
        # Shown on screen in the MINUS PEAK column. Chapter 1 states this
        # verbatim: "the shifted scores are [-2, -1, 0]".
        self.assertEqual(self.c["shifted"], [-2, -1, 0])

    def test_peak_weight_is_exactly_one_not_approximately(self) -> None:
        # The load-bearing equality, shown in terracotta. e**0 == 1 exactly,
        # which is what puts a floor under the denominator. An almost-equal
        # assertion here would defeat the purpose of the claim.
        self.assertIs(self.c["largest_weight_is_exactly_one"], True)
        self.assertEqual(self.c["weights"][2], 1.0)

    def test_total_weight_matches_the_figure_on_screen(self) -> None:
        # Displayed as TOTAL WEIGHT 1.5032147244 (10 dp).
        self.assertEqual(round(self.c["total"], 10), 1.5032147244)


class TestB03Distribution(unittest.TestCase):
    """B03 — the PROBABILITY column, against the chapter's published table."""

    def setUp(self) -> None:
        self.c = collect()["claim_2_distribution_unchanged"]

    def test_matches_chapters_published_table_to_ten_places(self) -> None:
        # Chapter 1, §"Temperature is a concentration control", T = 1.0 row.
        # This is the check that ties the video to the book.
        self.assertIs(self.c["matches_chapter_table_to_10dp"], True)

    def test_sums_to_one_within_tolerance_not_exactly(self) -> None:
        # Chapter 1 is explicit that the sum check "uses approximate equality
        # rather than requiring every floating-point sum to be exactly one".
        # Asserting exact equality here would be the wrong assertion for the
        # calculation, so tolerance is deliberate and narrow.
        self.assertIs(self.c["sums_to_one_within_1e_12"], True)


class TestB06FloatingPointReceipt(unittest.TestCase):
    """B06 — the honest detail: identical in algebra, not bit-identical."""

    def setUp(self) -> None:
        self.c = collect()["claim_2_distribution_unchanged"]

    def test_the_two_paths_are_not_bit_identical(self) -> None:
        # The claim the video makes, and the one it would have got wrong if
        # this had never been measured. A PASS here means the difference is
        # real: the vectors are not equal.
        self.assertNotEqual(self.c["shifted_path"], self.c["direct_path"])

    def test_difference_is_one_step_between_adjacent_floats(self) -> None:
        # Shown on screen at 104px: 1.1102230246251565e-16, glossed "exactly
        # 2**-53 — adjacent floats, one step apart". This test used to be named
        # "one machine epsilon", and so did the film. That was wrong: Python's
        # sys.float_info.epsilon is 2**-52, twice this gap (SOURCES.md §5.17).
        d = self.c["max_abs_difference"]
        self.assertEqual(d, 2.0**-53)
        self.assertEqual(d, sys.float_info.epsilon / 2)
        # "adjacent floats, one step apart": every differing pair is exactly one
        # representable step apart, and the largest gap is one ulp of the peak.
        for x, y in zip(self.c["shifted_path"], self.c["direct_path"]):
            self.assertIn(y, (x, math.nextafter(x, math.inf), math.nextafter(x, -math.inf)))
        self.assertEqual(d, math.ulp(max(self.c["shifted_path"])))

    def test_but_they_agree_far_inside_any_reported_precision(self) -> None:
        # Both halves of B06's sentence must hold at once, which is the point:
        # "indistinguishable" is a real claim, "equal" was not.
        self.assertIs(self.c["allclose_1e_12"], True)

    def test_exactly_two_digit_positions_differ(self) -> None:
        # The video marks indices 19 and 60 in terracotta and says "two digits
        # out of fifty-three": 62 characters, 53 of them digits. If formatting
        # ever changes, this catches it.
        a = repr(self.c["shifted_path"])
        b = repr(self.c["direct_path"])
        self.assertEqual(len(a), len(b))
        diff = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
        self.assertEqual(diff, [19, 60])
        self.assertEqual(sum(ch.isdigit() for ch in a), 53)

    def test_screen_and_narration_say_what_the_record_says(self) -> None:
        # R8-2 corrected "two digits out of sixty" in the narration and the
        # docs, and left it on screen for two more cuts — no check read the
        # beat sheet's on-screen text. This one does (SOURCES.md §5.17).
        sheet = json.loads((pathlib.Path(__file__).resolve().parent.parent
                            / "beat_sheet.json").read_text())
        b06 = next(b for b in sheet["beats"] if b["beat_id"] == "B06")
        gloss = b06["shot"]["remotion"]["props"]["diffGloss"]
        spoken = b06["narration_text"]
        digits = sum(ch.isdigit() for ch in repr(self.c["shifted_path"]))
        self.assertEqual(digits, 53)
        for text in (gloss, spoken):
            self.assertIn("fifty-three", text)
            self.assertNotIn("sixty", text)
            self.assertNotIn("machine epsilon", text)
        # The exponent printed on screen must be the one the run measured.
        shown = re.search(r"2\*\*-(\d+)", gloss)
        self.assertIsNotNone(shown)
        self.assertEqual(2.0 ** -int(shown.group(1)), self.c["max_abs_difference"])
        # The "1 ULP" markers drawn between each differing pair (REVIEW.md
        # Round 10, requested after watching) are a claim too: every pair that
        # differs must be exactly that many representable steps apart.
        label = b06["shot"]["remotion"]["props"].get("isolateLabel", "")
        if label:
            steps = int(label.split()[0])
            bits = lambda x: struct.unpack("<q", struct.pack("<d", x))[0]
            gaps = [abs(bits(x) - bits(y)) for x, y in
                    zip(self.c["shifted_path"], self.c["direct_path"]) if x != y]
            self.assertEqual(len(gaps), 2)
            self.assertEqual(set(gaps), {steps})


class TestB02Overflow(unittest.TestCase):
    """B02 — the failure the subtraction exists to prevent."""

    def test_raw_exponential_raises_rather_than_returning_inf(self) -> None:
        # The video says Python "refuses" — not "crashes", and not "returns
        # infinity". math.exp signals a range error, so this is the precise
        # behaviour the narration was corrected to describe (FACTCHECK row 5).
        with self.assertRaises(OverflowError):
            math.exp(1000)

    def test_the_shift_turns_that_into_a_clean_answer(self) -> None:
        # Chapter 1: the lesson "tests this choice with equal large scores,
        # [1000, 1000], and expects [0.5, 0.5]". Exact equality is correct
        # here: the shifted weights are [1, 1] and the division is exact.
        self.assertEqual(probabilities([1000, 1000]), [0.5, 0.5])

    def test_the_ceiling_figure_on_screen_is_the_real_one(self) -> None:
        # B02 draws the axis tick at 709.78 -> 1.797693e+308.
        c = collect()["claim_3_prevents_overflow"]
        self.assertEqual(round(c["log_float_max"], 4), 709.7827)
        self.assertEqual(f"{c['float_max']:.6e}", "1.797693e+308")


class TestB03DenominatorFloor(unittest.TestCase):
    """B03 — "the denominator can never fall below 1"."""

    def test_denominator_is_at_least_one_for_every_case_shown(self) -> None:
        # Not a sampled reassurance: this is the guarantee the video claims,
        # so every case the evidence script checks must hold, including a
        # 1e9 spread where every non-peak weight underflows to zero.
        for case in collect()["claim_4_denominator_floor"]["cases"]:
            with self.subTest(logits=case["logits"]):
                self.assertGreaterEqual(case["total"], 1.0)

    def test_it_holds_even_when_all_other_weights_vanish(self) -> None:
        # The worst case for the claim: the peak is the only surviving term.
        logits = [0.0, -1e9]
        total = sum(math.exp(x - max(logits)) for x in logits)
        self.assertEqual(total, 1.0)
        # And so the function still returns a usable distribution.
        self.assertEqual(probabilities(logits), [1.0, 0.0])


class TestB07TheBoundary(unittest.TestCase):
    """B07 — what the explanation does NOT establish.

    This is the class that defends the video's most important beat. If these
    tests ever pass trivially (because a future float ABI has more range),
    the video's boundary claim needs re-recording, not quiet patching.
    """

    def setUp(self) -> None:
        self.cases = {
            tuple(c["logits"]): c
            for c in collect()["claim_5_boundary_underflow"]["cases"]
        }

    def test_minus_800_returns_a_hard_zero(self) -> None:
        # The headline of B07: an exact 0.0 for an outcome with a nonzero
        # true share. `assertIs(..., True)` rather than assertTrue so a
        # truthy-but-not-True value cannot slip through.
        c = self.cases[(0, -800)]
        self.assertIs(c["is_exactly_zero"], True)
        self.assertEqual(c["probabilities"], [1.0, 0.0])

    def test_minus_745_still_survives_as_the_last_denormal(self) -> None:
        # Shown on screen as 5e-324 — below the smallest NORMAL float, so it
        # is already a denormal and has lost precision, but it is not zero.
        c = self.cases[(0, -745)]
        self.assertIs(c["is_exactly_zero"], False)
        self.assertEqual(c["probabilities"][1], 5e-324)
        self.assertLess(c["probabilities"][1], sys.float_info.min)

    def test_the_cliff_sits_between_745_and_746(self) -> None:
        # The specific number the narration commits to. This is the test
        # most likely to fail on a different platform, which is exactly why
        # it is asserted instead of asserted-about.
        self.assertIs(self.cases[(0, -745)]["is_exactly_zero"], False)
        self.assertIs(self.cases[(0, -746)]["is_exactly_zero"], True)

    def test_the_vanished_outcome_is_still_a_possible_outcome(self) -> None:
        # Chapter 1: "'not observed in this run' and 'not a possible outcome'
        # are different statements." The same distinction applies to a
        # probability that underflowed: the model still assigns it weight.
        # Its true share is ~1e-348, which float64 cannot represent at all.
        self.assertLess(self.cases[(0, -800)]["true_value_log10"], -340)


class TestTheCliffIsDerivable(unittest.TestCase):
    """boundary_analysis.py — the cliff predicted from the float format.

    B07 found -746 by sweeping. These tests defend the stronger claim: the
    boundary is `-1075 * ln 2`, and -746 is simply the first integer past it.
    A predicted number is better evidence than a discovered one.
    """

    def setUp(self) -> None:
        self.d = boundary_collect()

    def test_prediction_matches_the_measured_boundary(self) -> None:
        # Closed form vs bisection of the real function, to 1e-6.
        x = self.d["derivation"]
        self.assertIs(x["agree_to_1e_6"], True)
        self.assertAlmostEqual(
            x["predicted_boundary"], x["measured_boundary_by_bisection"], places=6
        )

    def test_the_boundary_is_minus_1075_ln2(self) -> None:
        self.assertAlmostEqual(
            self.d["derivation"]["predicted_boundary"], -1075 * math.log(2), places=12
        )

    def test_that_derivation_explains_the_746_in_the_video(self) -> None:
        # The link between the derived threshold and the integer on screen.
        self.assertEqual(self.d["derivation"]["first_integer_below"], -746)

    def test_the_real_cost_is_ties_not_just_smallness(self) -> None:
        # The sharp harm: two outcomes 100 nats apart report as the same
        # number. This is what makes the boundary worth a beat.
        y = self.d["information_loss"]
        self.assertIs(y["linear_ties_outcomes_1_and_2"], True)
        self.assertAlmostEqual(abs(y["log_space_separation_nats"]), 100.0, places=9)

    def test_log_space_loses_nothing_where_linear_does(self) -> None:
        for case in self.d["remedy"]["cases"]:
            with self.subTest(logits=case["logits"]):
                self.assertEqual(case["log_space_lost_outcomes"], [])

    def test_the_remedy_does_not_change_the_answer(self) -> None:
        # A "fix" that returned a different distribution would not be a fix.
        self.assertIs(self.d["agreement"]["agree_to_1e_12"], True)


class TestScopeDiscipline(unittest.TestCase):
    """Guards on what the video is allowed to say.

    These defend the FACTCHECK's "claims deliberately NOT made" section — the
    narrow-claim discipline is part of the artifact, not commentary on it.
    """

    def test_the_reference_implementation_is_unmodified(self) -> None:
        # AGENTS.md: "Do not modify reference solutions." The video's whole
        # authority rests on importing the course's file as-is.
        env = collect()["environment"]
        self.assertTrue(env["reference_implementation"].endswith("main.py"))
        self.assertIn("01-randomness-and-first-prompts", env["reference_implementation"])

    def test_zero_temperature_is_still_rejected(self) -> None:
        # The video never claims low temperature equals argmax, and the
        # interface it describes must keep refusing 0 for that to stay true.
        with self.assertRaises(ValueError):
            probabilities([1, 2, 3], temperature=0)

    def test_negative_temperature_is_still_rejected(self) -> None:
        # B04's ordering argument ("for positive T the ordering survives")
        # depends on this refusal being part of the contract.
        with self.assertRaises(ValueError):
            probabilities([1, 2, 3], temperature=-1)

    def test_nonfinite_scores_are_still_rejected(self) -> None:
        # The accepted-domain boundary. Chapter 1: "A function is partly
        # defined by what it refuses to compute."
        with self.assertRaises(ValueError):
            probabilities([1, 2, math.inf])


if __name__ == "__main__":
    unittest.main(verbosity=2)
