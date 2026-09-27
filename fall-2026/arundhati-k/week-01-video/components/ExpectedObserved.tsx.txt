/**
 * ExpectedObserved.tsx — body illustrations for the reel
 * `claude-liam-expected-vs-observed` (INFO 7375 Week 1).
 *
 * WHAT THIS FILE IS
 * -----------------
 * Five C3 concept illustrations carrying ONE idea: an expected count (665.24)
 * and an observed count (630) disagree, and that disagreement is sampling —
 * not evidence the probabilities are wrong.
 *
 * EVERY NUMBER HERE IS REAL.
 * Source: lessons/01-randomness-and-first-prompts/code/main.py, unmodified,
 * seed=7, count=1000, logits [1,2,3], temperature 1.0. Verified 2026-09-26:
 *
 *   probabilities -> [0.09003057317038046, 0.24472847105479764, 0.6652409557748218]
 *   counts        -> {1: 268, 2: 630, 0: 102}          (printed key order)
 *   expected      -> 0.6652409557748218 * 1000 = 665.2409557748218
 *   gap           -> 665.2409557748218 - 630 = 35.2409557748218  (5.297%)
 *   exp intermediates -> exp(-2)=0.1353, exp(-1)=0.3679, exp(0)=1.0, sum=1.5032
 *
 * Do not "tidy" these constants. If they ever disagree with main.py, main.py
 * wins and the beat sheet is wrong.
 *
 * THE ONE SCHEMATIC. <WhatWouldSettleIt> draws a spread of repeated runs that
 * WERE NOT PERFORMED. It is generated from a seeded hash (never Math.random),
 * is dimmed to 45%, and is captioned NOT RUN IN THIS VIDEO on screen. It must
 * never read as collected data. <TheGap> is likewise labelled CONSTRUCTED
 * ILLUSTRATION for its full duration — its two numbers are real, its shape
 * is authored.
 *
 * LAWS KEPT
 * ---------
 *  • ONE terracotta accent per beat (CLAUDE.SPARK) — the focal number only.
 *  • Pure function of useP(). No timers, no CSS transitions, no Math.random().
 *  • Wrapped in <IlluStage spark="…"> (SPARK-LINE LAW).
 *  • 1920×1080; everything essential inside SAFE (x 96–1824, y 54–1026).
 *  • FILL-THE-CANVAS: type is sized to read across a room, not to a floor.
 */
import React from 'react';
import { z } from 'zod';
import { CLAUDE } from '../tokens/claude';
import { SAFE } from '../tokens/layout';
import { SERIF, SANS, MONO, clamp, remap, ease, useP, IlluStage } from '../illustrations/kit';

const INK = CLAUDE.INK;
const SOFT = CLAUDE.INK_SOFT;
const ACCENT = CLAUDE.SPARK;          // fills only — bars, spans, rules
// Terracotta TEXT on cream is 2.74:1 and fails type-spec §8.3 (WCAG 4.5:1).
// #A2442A is the same hue darkened to 5.42:1 on the #F2F0E9 stage, so the
// accent stays terracotta and the text stays legible. Fills keep CLAUDE.SPARK
// because WCAG text contrast does not govern a solid shape.
const ACCENT_TEXT = '#A2442A';

/** Verified constants — see header. */
export const REAL = {
  logits: [1, 2, 3],
  shifted: [-2, -1, 0],
  exps: [0.1353, 0.3679, 1.0],
  sum: 1.5032,
  probs: [0.09, 0.2447, 0.6652],
  probFull: '0.6652409557748218',
  counts: [102, 268, 630],
  expected: 665.24,
  gap: 35.24,
  gapPct: 5.3,
  // Binomial(1000, 0.6652409557748218): sd = sqrt(n p (1-p)) = 14.9230,
  // z = (630 - 665.2410) / 14.9230 = -2.3615, P(X <= 630) = 0.010364.
  // 630 is UNUSUAL (~1 run in 50), not ordinary. Verified 2026-09-26.
  sd: 14.92,
  z: 2.4,
  oneIn: 50,
} as const;

export const expectedObservedSchema = z.object({
  sparkLine: z.string().default('Expected, observed.'),
  durationSeconds: z.number().optional(),
});
export type ExpectedObservedProps = z.infer<typeof expectedObservedSchema>;

/** Deterministic [0,1) hash — replaces Math.random so renders are identical. */
const hash01 = (n: number): number => {
  const x = Math.sin(n * 12.9898 + 78.233) * 43758.5453;
  return x - Math.floor(x);
};

/** A number that counts up to `to` and settles, easing out. */
const useCount = (to: number, start: number, end: number, decimals = 0): string => {
  const p = useP();
  const v = to * ease(remap(p, start, end, 0, 1));
  return v.toFixed(decimals);
};

/* ==================================================================== *
 * B02 · SoftmaxInOneBeat                                               *
 * Four rows: logits -> peak-subtracted -> exponentiated -> normalized. *
 * Scope guard: this beat SOURCES 0.6652 and hands off. It does not     *
 * teach the max-subtraction — that is a different concept.             *
 * ==================================================================== */
export const SoftmaxInOneBeat: React.FC<ExpectedObservedProps> = (props) => {
  const p = expectedObservedSchema.parse(props);
  const t = useP();

  const rows = [
    { label: 'scores', vals: REAL.logits.map((v) => String(v)) },
    { label: 'subtract the largest', vals: REAL.shifted.map((v) => String(v)) },
    { label: 'exponentiate', vals: REAL.exps.map((v) => v.toFixed(4)) },
    { label: `divide by ${REAL.sum}`, vals: REAL.probs.map((v) => v.toFixed(4)) },
  ];

  const LABEL_X = SAFE.x + 8;
  const COL_W = 340;
  const COL_GAP = 30;
  const COLS_X = SAFE.x + 600;
  const ROW_Y = [196, 392, 588, 784];

  return (
    <IlluStage spark={p.sparkLine} sparkSize={62}>
      {rows.map((row, ri) => {
        const appear = remap(t, 0.03 + ri * 0.10, 0.15 + ri * 0.10, 0, 1);
        const o = ease(appear);
        const dy = (1 - o) * 34;
        return (
          <div key={row.label}>
            <div
              style={{
                position: 'absolute', left: LABEL_X, top: ROW_Y[ri] + dy,
                width: 566, height: 150, display: 'flex', alignItems: 'center',
                justifyContent: 'flex-end', paddingRight: 30,
                fontFamily: SANS, fontSize: 44, color: SOFT, opacity: o,
                textAlign: 'right',
              }}
            >
              {row.label}
            </div>
            {row.vals.map((v, ci) => {
              const isFocal = ri === 3 && ci === 2;
              const focal = isFocal ? ease(remap(t, 0.50, 0.58, 0, 1)) : 0;
              return (
                <div
                  key={ci}
                  style={{
                    position: 'absolute',
                    left: COLS_X + ci * (COL_W + COL_GAP),
                    top: ROW_Y[ri] + dy,
                    width: COL_W, height: 150,
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    fontFamily: MONO,
                    fontSize: 72,
                    fontWeight: isFocal ? 700 : 500,
                    color: isFocal && focal > 0 ? ACCENT_TEXT : INK,
                    background: CLAUDE.CARD,
                    border: `2px solid ${isFocal && focal > 0 ? ACCENT : CLAUDE.BORDER}`,
                    borderRadius: 10,
                    opacity: o,
                  }}
                >
                  {v}
                </div>
              );
            })}
          </div>
        );
      })}

      {/* the divisor rule — drawn, not stated */}
      <div
        style={{
          position: 'absolute', left: COLS_X, top: ROW_Y[2] + 168,
          width: (COL_W + COL_GAP) * 3 - COL_GAP,
          height: 4, background: INK,
          transform: `scaleX(${ease(remap(t, 0.38, 0.47, 0, 1))})`,
          transformOrigin: 'left center',
        }}
      />

      {/* scope handoff */}
      <div
        style={{
          position: 'absolute', left: SAFE.x, top: 958, width: SAFE.w,
          textAlign: 'center', fontFamily: SANS, fontSize: 44, color: SOFT,
          opacity: ease(remap(t, 0.60, 0.70, 0, 1)),
        }}
      >
        this video uses <span style={{ color: ACCENT_TEXT, fontWeight: 700 }}>one</span> of these numbers
      </div>
    </IlluStage>
  );
};

/* ==================================================================== *
 * B03 · ExpectedCount                                                  *
 * One multiplication performs itself, then is explicitly bounded:      *
 * it is a long-run average, not a prediction about this run.           *
 * ==================================================================== */
export const ExpectedCount: React.FC<ExpectedObservedProps> = (props) => {
  const p = expectedObservedSchema.parse(props);
  const t = useP();
  const counted = useCount(REAL.expected, 0.25, 0.42, 2);

  const showProb = ease(remap(t, 0.03, 0.11, 0, 1));
  const showMul = ease(remap(t, 0.12, 0.20, 0, 1));
  const ruleW = ease(remap(t, 0.20, 0.27, 0, 1));
  const strike = ease(remap(t, 0.46, 0.55, 0, 1));
  const showNew = ease(remap(t, 0.57, 0.66, 0, 1));

  return (
    <IlluStage spark={p.sparkLine} sparkSize={62}>
      {/* full printed precision — no rounding on screen */}
      <div
        style={{
          position: 'absolute', left: SAFE.x, top: 150, width: SAFE.w,
          textAlign: 'center', fontFamily: MONO, fontSize: 108, color: INK,
          opacity: showProb, letterSpacing: -1,
        }}
      >
        {REAL.probFull}
      </div>

      <div
        style={{
          position: 'absolute', left: SAFE.x, top: 288, width: SAFE.w,
          textAlign: 'center', fontFamily: MONO, fontSize: 92, color: SOFT,
          opacity: showMul,
        }}
      >
        × 1000 draws
      </div>

      <div
        style={{
          position: 'absolute', left: SAFE.x + SAFE.w / 2 - 700, top: 404,
          width: 1400, height: 7, background: INK,
          transform: `scaleX(${ruleW})`, transformOrigin: 'center',
        }}
      />

      <div
        style={{
          position: 'absolute', left: SAFE.x, top: 440, width: SAFE.w,
          textAlign: 'center', fontFamily: MONO, fontSize: 336, fontWeight: 700,
          color: ACCENT_TEXT, opacity: ease(remap(t, 0.25, 0.32, 0, 1)),
          letterSpacing: -4,
        }}
      >
        {counted}
      </div>

      {/* the bound: struck through, then replaced, on the spoken word */}
      <div
        style={{
          position: 'absolute', left: SAFE.x, top: 782, width: SAFE.w,
          textAlign: 'center', fontFamily: SERIF, fontSize: 66,
          color: SOFT, opacity: showProb * (1 - showNew * 0.55),
        }}
      >
        <span style={{ position: 'relative', display: 'inline-block' }}>
          what this run will do
          <span
            style={{
              position: 'absolute', left: 0, top: '52%', height: 4,
              width: '100%', background: ACCENT,
              transform: `scaleX(${strike})`, transformOrigin: 'left center',
            }}
          />
        </span>
      </div>

      <div
        style={{
          position: 'absolute', left: SAFE.x, top: 892, width: SAFE.w,
          textAlign: 'center', fontFamily: SERIF, fontSize: 78, color: INK,
          opacity: showNew,
        }}
      >
        the average over many runs
      </div>
    </IlluStage>
  );
};

/* ==================================================================== *
 * B04 · ObservedCounts                                                 *
 * The verbatim printed JSON beside bars that grow to the real counts.  *
 * The printed key order (1, 2, 0) is preserved, not sorted.            *
 * ==================================================================== */
export const ObservedCounts: React.FC<ExpectedObservedProps> = (props) => {
  const p = expectedObservedSchema.parse(props);
  const t = useP();

  const jsonLines = [
    '{',
    '  "counts": {',
    '    "1": 268,',
    '    "2": 630,',
    '    "0": 102',
    '  }',
    '}',
  ];

  const BAR_X = SAFE.x + 680;
  const BAR_MAX_W = 840;
  const SCALE_MAX = 700; // headroom so the 665.24 rule sits inside the plot
  const BAR_Y = [286, 486, 686];
  const BAR_H = 140;

  const ruleX = BAR_X + (REAL.expected / SCALE_MAX) * BAR_MAX_W;
  const showRule = ease(remap(t, 0.46, 0.55, 0, 1));

  return (
    <IlluStage spark={p.sparkLine} sparkSize={62}>
      {/* verbatim source output */}
      <div
        style={{
          position: 'absolute', left: SAFE.x, top: 286, width: 600,
          fontFamily: MONO, fontSize: 40, lineHeight: 1.7, color: INK,
          background: CLAUDE.CARD, border: `2px solid ${CLAUDE.BORDER}`,
          borderRadius: 12, padding: '26px 30px',
          opacity: ease(remap(t, 0.03, 0.10, 0, 1)),
        }}
      >
        {jsonLines.map((l, i) => (
          <div key={i} style={{ whiteSpace: 'pre' }}>{l}</div>
        ))}
        <div style={{ marginTop: 20, fontFamily: SANS, fontSize: 42, color: SOFT }}>
          main.py · seed=7 · 1000 draws
        </div>
      </div>

      {/* bars, drawn in index order and labelled */}
      {REAL.counts.map((c, i) => {
        const start = 0.12 + i * 0.10;
        const grow = ease(remap(t, start, start + 0.09, 0, 1));
        const isFocal = i === 2;
        const w = (c / SCALE_MAX) * BAR_MAX_W * grow;
        return (
          <div key={i}>
            <div
              style={{
                position: 'absolute', left: BAR_X - 118, top: BAR_Y[i] + 26,
                width: 100, textAlign: 'right',
                fontFamily: MONO, fontSize: 48, color: SOFT,
                opacity: ease(remap(t, start - 0.04, start + 0.04, 0, 1)),
              }}
            >
              [{i}]
            </div>
            <div
              style={{
                position: 'absolute', left: BAR_X, top: BAR_Y[i],
                width: w, height: BAR_H,
                background: isFocal ? ACCENT : '#8A8675',
                border: `2px solid ${isFocal ? ACCENT : SOFT}`,
                borderRadius: 8,
              }}
            />
            <div
              style={{
                position: 'absolute', left: BAR_X + w + 26, top: BAR_Y[i] + 36,
                fontFamily: MONO, fontSize: 64, fontWeight: isFocal ? 700 : 500,
                color: INK,
                opacity: grow,
              }}
            >
              {Math.round(c * grow)}
            </div>
          </div>
        );
      })}

      {/* the expected-count rule the favourite stops short of */}
      <div
        style={{
          position: 'absolute', left: ruleX, top: BAR_Y[0] - 56,
          width: 0, height: BAR_Y[2] + BAR_H + 30 - (BAR_Y[0] - 56),
          borderLeft: `4px dashed ${INK}`,
          opacity: showRule * 0.85,
        }}
      />
      <div
        style={{
          position: 'absolute', left: ruleX - 150, top: BAR_Y[0] - 100,
          width: 300, textAlign: 'center',
          fontFamily: SANS, fontSize: 44, color: INK, opacity: showRule,
        }}
      >
        expected 665.24
      </div>
    </IlluStage>
  );
};

/* ==================================================================== *
 * B05 · TheGap  — CONSTRUCTED ILLUSTRATION                             *
 * The two numbers are real. The number line around them is authored    *
 * for this video, and says so on screen for the full duration.         *
 * ==================================================================== */
export const TheGap: React.FC<ExpectedObservedProps> = (props) => {
  const p = expectedObservedSchema.parse(props);
  const t = useP();

  const LO = 600;
  const HI = 700;
  const AX_X = SAFE.x + 140;
  const AX_W = SAFE.w - 280;
  const AX_Y = 560;
  const xOf = (v: number) => AX_X + ((v - LO) / (HI - LO)) * AX_W;

  const axis = ease(remap(t, 0.06, 0.16, 0, 1));
  const marks = ease(remap(t, 0.16, 0.25, 0, 1));
  const span = ease(remap(t, 0.25, 0.38, 0, 1));
  const pct = ease(remap(t, 0.40, 0.50, 0, 1));
  const note = ease(remap(t, 0.56, 0.66, 0, 1));
  const gapCount = useCount(REAL.gap, 0.26, 0.40, 2);

  const xObs = xOf(630);
  const xExp = xOf(REAL.expected);

  return (
    <IlluStage spark={p.sparkLine} sparkPos="top" sparkSize={62}>
      {/* the label is present from frame 1 and never leaves */}
      <div
        style={{
          position: 'absolute', right: SAFE.x, top: 150,
          fontFamily: SANS, fontSize: 42, fontWeight: 700, letterSpacing: 1.6,
          color: CLAUDE.CARD, background: SOFT,
          padding: '10px 20px', borderRadius: 6,
        }}
      >
        CONSTRUCTED ILLUSTRATION
      </div>

      {/* axis */}
      <div
        style={{
          position: 'absolute', left: AX_X, top: AX_Y, width: AX_W, height: 4,
          background: INK, transform: `scaleX(${axis})`, transformOrigin: 'left center',
        }}
      />
      {[600, 625, 650, 675, 700].map((v) => (
        <div key={v}>
          <div style={{ position: 'absolute', left: xOf(v), top: AX_Y, width: 2, height: 20, background: SOFT, opacity: axis }} />
          <div
            style={{
              position: 'absolute', left: xOf(v) - 60, top: AX_Y + 30, width: 120,
              textAlign: 'center', fontFamily: MONO, fontSize: 44, color: SOFT, opacity: axis,
            }}
          >
            {v}
          </div>
        </div>
      ))}

      {/* the filled span between the two real numbers */}
      <div
        style={{
          position: 'absolute', left: xObs, top: AX_Y - 46, height: 46,
          width: (xExp - xObs) * span, background: ACCENT, opacity: 0.9,
        }}
      />

      {/* the two real marks */}
      {[
        { x: xObs, label: 'observed', value: '630' },
        { x: xExp, label: 'expected', value: '665.24' },
      ].map((m) => (
        <div key={m.label}>
          <div style={{ position: 'absolute', left: m.x - 2, top: AX_Y - 150, width: 5, height: 150, background: INK, opacity: marks }} />
          <div
            style={{
              position: 'absolute', left: m.x - 160, top: AX_Y - 232, width: 320,
              textAlign: 'center', fontFamily: MONO, fontSize: 60, fontWeight: 700,
              color: INK, opacity: marks,
            }}
          >
            {m.value}
          </div>
          <div
            style={{
              position: 'absolute', left: m.x - 160, top: AX_Y - 180, width: 320,
              textAlign: 'center', fontFamily: SANS, fontSize: 44, color: SOFT, opacity: marks,
            }}
          >
            {m.label}
          </div>
        </div>
      ))}

      {/* the gap itself */}
      <div
        style={{
          position: 'absolute', left: SAFE.x, top: 690, width: SAFE.w,
          textAlign: 'center', fontFamily: MONO, fontSize: 108, fontWeight: 700,
          color: INK, opacity: span,
        }}
      >
        {gapCount}
      </div>
      <div
        style={{
          position: 'absolute', left: SAFE.x, top: 806, width: SAFE.w,
          textAlign: 'center', fontFamily: SERIF, fontSize: 50, color: INK, opacity: pct,
        }}
      >
        draws short — {REAL.gapPct}% below expected, ≈ {REAL.z} standard deviations
      </div>

      <div
        style={{
          position: 'absolute', left: SAFE.x, top: 900, width: SAFE.w,
          textAlign: 'center', fontFamily: SANS, fontSize: 42, color: SOFT, opacity: note,
        }}
      >
        numbers real · diagram authored for this video
      </div>
    </IlluStage>
  );
};

/* ==================================================================== *
 * B06 · WhatWouldSettleIt                                              *
 * Left: the one run this video has. Right: the repeated experiment it  *
 * does NOT have — dimmed to 45% and captioned as not performed.        *
 * ==================================================================== */
export const WhatWouldSettleIt: React.FC<ExpectedObservedProps> = (props) => {
  const p = expectedObservedSchema.parse(props);
  const t = useP();

  const MID = SAFE.x + SAFE.w / 2;
  const PANEL_W = SAFE.w / 2 - 50;
  const L_X = SAFE.x;
  const R_X = MID + 50;

  const left = ease(remap(t, 0.06, 0.18, 0, 1));
  const stamp = ease(remap(t, 0.22, 0.34, 0, 1));
  const right = ease(remap(t, 0.42, 0.56, 0, 1));
  const inside = ease(remap(t, 0.64, 0.74, 0, 1));
  const dim = ease(remap(t, 0.82, 0.92, 0, 1));

  // Schematic spread — seeded, never Math.random. NOT collected data.
  // Bin scale: SIGMA_BINS bins per standard deviation, so the 21 bins span
  // about ±3.5 sd. 630 is z = -2.36, which lands at bin 3 — in the LEFT TAIL,
  // not mid-pack. That placement is the point of the beat: the gap is unusual.
  const bins = 21;
  const centreBin = (bins - 1) / 2;
  const SIGMA_BINS = 3.0;
  const OBS_BIN = Math.round(centreBin - REAL.z * SIGMA_BINS); // -> 3
  const spread = Array.from({ length: bins }, (_, i) => {
    const d = (i - centreBin) / SIGMA_BINS;
    const bell = Math.exp(-0.5 * d * d);
    return bell * (0.82 + hash01(i + 1) * 0.36);
  });

  const PLOT_Y = 700;
  const PLOT_H = 300;
  const binW = PANEL_W / bins;
  const rightPanelOpacity = right * (1 - dim * 0.55); // floor 45%

  return (
    <IlluStage spark={p.sparkLine} sparkPos="top" sparkSize={62}>
      {/* ── LEFT: the one run ─────────────────────────────────────── */}
      <div
        style={{
          position: 'absolute', left: L_X, top: 168, width: PANEL_W,
          textAlign: 'center', fontFamily: SANS, fontSize: 44, color: SOFT, opacity: left,
        }}
      >
        what this video has
      </div>
      <div
        style={{
          position: 'absolute', left: L_X, top: 218, width: PANEL_W,
          textAlign: 'center', fontFamily: SERIF, fontSize: 52, color: INK, opacity: left,
        }}
      >
        one run of 1000
      </div>

      <div style={{ position: 'absolute', left: L_X + 40, top: PLOT_Y, width: PANEL_W - 80, height: 4, background: INK, opacity: left }} />
      <div style={{ position: 'absolute', left: L_X + PANEL_W / 2 - 3, top: PLOT_Y - 190, width: 7, height: 190, background: ACCENT, opacity: left }} />
      <div
        style={{
          position: 'absolute', left: L_X, top: PLOT_Y - 254, width: PANEL_W,
          textAlign: 'center', fontFamily: MONO, fontSize: 72, fontWeight: 700, color: INK, opacity: left,
        }}
      >
        630
      </div>

      <div
        style={{
          position: 'absolute', left: L_X, top: PLOT_Y + 40, width: PANEL_W,
          textAlign: 'center', fontFamily: SERIF, fontSize: 40, color: INK, opacity: stamp,
        }}
      >
        Can this refute 0.6652?
      </div>
      <div
        style={{
          position: 'absolute', left: L_X + PANEL_W / 2 - 90, top: PLOT_Y + 110,
          width: 180, textAlign: 'center',
          fontFamily: SANS, fontSize: 60, fontWeight: 800, letterSpacing: 3,
          color: CLAUDE.CARD, background: INK, borderRadius: 8, padding: '6px 0',
          opacity: stamp, transform: `scale(${0.9 + 0.1 * stamp})`,
        }}
      >
        NO
      </div>
      <div
        style={{
          position: 'absolute', left: L_X, top: PLOT_Y + 194, width: PANEL_W,
          textAlign: 'center', fontFamily: SANS, fontSize: 42, color: SOFT, opacity: stamp,
        }}
      >
        one seed, read after the fact — a reason to test, not a verdict
      </div>

      {/* divider */}
      <div style={{ position: 'absolute', left: MID, top: 180, width: 2, height: 700, background: CLAUDE.BORDER, opacity: right }} />

      {/* ── RIGHT: the experiment NOT run ─────────────────────────── */}
      <div style={{ opacity: rightPanelOpacity }}>
        <div
          style={{
            position: 'absolute', left: R_X, top: 168, width: PANEL_W,
            textAlign: 'center', fontFamily: SANS, fontSize: 44, color: SOFT,
          }}
        >
          what would settle it
        </div>
        <div
          style={{
            position: 'absolute', left: R_X, top: 218, width: PANEL_W,
            textAlign: 'center', fontFamily: SERIF, fontSize: 52, color: INK,
          }}
        >
          many runs of 1000
        </div>

        {spread.map((h, i) => {
          const rise = ease(remap(t, 0.44 + i * 0.006, 0.56 + i * 0.006, 0, 1));
          const isObs = i === OBS_BIN; // where 630 lands — the left tail
          return (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: R_X + i * binW + 3,
                top: PLOT_Y - h * PLOT_H * rise,
                width: binW - 6,
                height: h * PLOT_H * rise,
                background: isObs && inside > 0 ? ACCENT : CLAUDE.PILL,
                border: `1px solid ${CLAUDE.BORDER}`,
              }}
            />
          );
        })}
        <div style={{ position: 'absolute', left: R_X, top: PLOT_Y, width: PANEL_W, height: 4, background: INK }} />

        {/* 630 sits in the tail — marked where it actually falls */}
        <div
          style={{
            position: 'absolute', left: R_X + OBS_BIN * binW + binW / 2 - 100, top: PLOT_Y + 24,
            width: 200, textAlign: 'center',
            fontFamily: MONO, fontSize: 46, color: INK, fontWeight: 700, opacity: inside,
          }}
        >
          630
        </div>
        <div
          style={{
            position: 'absolute', left: R_X + centreBin * binW + binW / 2 - 100, top: PLOT_Y + 24,
            width: 200, textAlign: 'center',
            fontFamily: MONO, fontSize: 44, color: SOFT, opacity: inside,
          }}
        >
          665.24
        </div>
        <div
          style={{
            position: 'absolute', left: R_X, top: PLOT_Y + 74, width: PANEL_W,
            textAlign: 'center', fontFamily: SANS, fontSize: 42, color: SOFT, opacity: inside,
          }}
        >
          in the tail — about 1 run in {REAL.oneIn}, not mid-pack
        </div>
      </div>

      {/* the honesty rule over the panel that was never run */}
      <div
        style={{
          position: 'absolute', left: R_X, top: PLOT_Y + 150, width: PANEL_W,
          height: 4, background: ACCENT, opacity: dim,
        }}
      />
      <div
        style={{
          position: 'absolute', left: R_X, top: PLOT_Y + 166, width: PANEL_W,
          textAlign: 'center', fontFamily: SANS, fontSize: 44, fontWeight: 700,
          letterSpacing: 1.4, color: ACCENT_TEXT, opacity: dim,
        }}
      >
        NOT RUN IN THIS VIDEO
      </div>
    </IlluStage>
  );
};
