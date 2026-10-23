"""
scenes.py: Manim scenes for the Ghost-Job Trust Radar pitch film (show-tell).

The drawing kit below is the show-tell iso kit (core primitives and pacing helpers, pasted not imported,
because Gate A copies only scenes.py). The writing kit and the portrait helper were left out: no scene uses them.
Every body beat is one drawing in the Claude palette; labels sit beside objects; all motion ends by 70% of the
beat and all type is settled by 45%, so nothing is moving at the 50% midpoint that GATE T and Gate V sample.
"""
from manim import *
import numpy as np
import json as _json, os as _os

# ═════════════════════════════ ISO KIT (show-tell) ═════════════════════════════
STAGE = "#F2F0E9"; INK = "#3D3929"; TERRA = "#D97757"; DIM = "#8B8F96"; GHOST = "#D9D4C7"; CARD = "#FAF9F5"
BOX_TOP, BOX_L, BOX_R = "#F3E9D8", "#DCC9AA", "#C7AE86"
BOX_IN1, BOX_IN2, BOX_FLOOR = "#CDB894", "#BFA67E", "#B39A72"
DARK_TOP, DARK_L, DARK_R = "#3A3530", "#26221F", "#1E1B18"
PAGE_TOP, PAGE_L, PAGE_R = "#FFFFFF", "#ECE7DF", "#E2DCD2"
BAR1, BAR2, BAR3 = "#8B8F96", "#B4AFA6", "#D9D4C7"
SERIF = "EB Garamond"
C30 = 0.8660254
config.background_color = STAGE


def T(s, size=36, color=INK, bold=False):
    return Text(s, font=SERIF, color=color, font_size=size, weight="BOLD" if bold else "NORMAL")


class Iso:
    """Isometric projection: x runs right-up, y runs left-up, z runs up. (ox, oy) is where (0,0,0) lands."""
    def __init__(self, ox=0.0, oy=0.0, s=1.0):
        self.ox, self.oy, self.s = ox, oy, s

    def p(self, x, y, z=0.0):
        return np.array([self.ox + (x - y) * C30 * self.s, self.oy + (x + y) * 0.5 * self.s + z * self.s, 0.0])

    def v(self, dx, dy, dz=0.0):
        return self.p(dx, dy, dz) - self.p(0, 0, 0)

    def quad(self, pts, fill, stroke=INK, sw=4):
        return Polygon(*[self.p(*q) for q in pts], fill_color=fill, fill_opacity=1, stroke_color=stroke, stroke_width=sw)

    def box(self, x0, y0, z0, w, d, h, top=BOX_TOP, left=BOX_L, right=BOX_R, sw=4, stroke=INK):
        x1, y1, z1 = x0 + w, y0 + d, z0 + h
        return VGroup(
            self.quad([(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)], left, stroke, sw),
            self.quad([(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], right, stroke, sw),
            self.quad([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], top, stroke, sw))

    def page(self, x0, y0, z0, w=1.1, d=1.4):
        slab = self.box(x0, y0, z0, w, d, 0.06, PAGE_TOP, PAGE_L, PAGE_R, sw=1.5)
        zt = z0 + 0.06
        lines = VGroup(*[Line(self.p(x0 + 0.2, y0 + d * f, zt), self.p(x0 + w - 0.2, y0 + d * f, zt), color=GHOST, stroke_width=4)
                         for f in (0.3, 0.5, 0.7)])
        dot = Dot(self.p(x0 + 0.2, y0 + d * 0.86, zt), radius=0.06, color=TERRA)
        return VGroup(slab, lines, dot)


def ease_in(t):
    return t * t


def check(x, y, s=0.2, color=INK, w=7):
    return VGroup(Line([x - s, y, 0], [x - s * 0.3, y - s * 0.75, 0], color=color, stroke_width=w),
                  Line([x - s * 0.3, y - s * 0.75, 0], [x + s * 1.1, y + s * 0.85, 0], color=color, stroke_width=w))


try:
    _SHEET = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "beat_sheet.json")))
    _TARGET = {b["beat_id"]: float(b.get("actual_duration_s") or b.get("estimated_duration_s") or 0) for b in _SHEET["beats"]}
except Exception:
    _TARGET = {}


def _elapsed(self):
    rt = getattr(getattr(self, "renderer", None), "time", None)
    return float(rt) if isinstance(rt, (int, float)) else 0.0


def _dur(self):
    return _TARGET.get(type(self).__name__.split("_")[0], 0) or 12.0


def go(self, a, b, *anims, **kw):
    """Run `anims` from fraction a to fraction b of the beat. Never overlaps the 45-55% midpoint window; ends by 0.70."""
    assert b <= 0.70 and (b <= 0.45 or a >= 0.55), f"timing window {a}-{b} breaks the midpoint or 70% rule"
    d = _dur(self)
    gap = a * d - _elapsed(self)
    if gap > 0.02:
        self.wait(gap)
    self.play(*anims, run_time=max(0.1, (b - a) * d), **kw)


def finish(self):
    target = _TARGET.get(type(self).__name__.split("_")[0], 0)
    self.wait(max(0.3, target - _elapsed(self)) if target else 2.0)


# ═════════════════════════════ cast for this film ═════════════════════════════
DK = "#9C8462"          # deep kraft: belts, cables, small outlines
BELT_TOP, BELT_L, BELT_R = "#E8E3D6", "#D7CFBD", "#CBC1AB"


def ibox(iso, x0, y0, z0, w, d, h, top=BOX_TOP, left=BOX_L, right=BOX_R, stroke=INK, sw=4):
    return iso.box(x0, y0, z0, w, d, h, top, left, right, sw=sw, stroke=stroke)


def lab(text, pt, dx=0.0, dy=0.0, size=34, edge=None):
    """A label at screen point `pt` (+ offset). edge=LEFT puts the label's left edge at the point."""
    m = T(text, size)
    if edge is None:
        return m.move_to([pt[0] + dx, pt[1] + dy, 0])
    return m.move_to([pt[0] + dx, pt[1] + dy, 0], aligned_edge=edge)


def posting_box(iso, x, y, z=0.0):
    """The posting: a kraft box with a grey strap across its top and one terracotta seal dot on the top face."""
    body = ibox(iso, x, y, z, 1.0, 1.0, 0.8)
    strap = iso.quad([(x + 0.4, y, z + 0.8), (x + 0.6, y, z + 0.8), (x + 0.6, y + 1, z + 0.8), (x + 0.4, y + 1, z + 0.8)], BAR2, BAR2, 0)
    seal = Dot(iso.p(x + 0.5, y + 0.5, z + 0.8), radius=0.08, color=TERRA)
    g = VGroup(body, strap, seal)
    g.faces = [m for m in body]
    g.seal = seal
    return g


def grey_out(g):
    return AnimationGroup(*[f.animate.set_fill(GHOST).set_stroke(DIM) for f in g.faces], FadeOut(g.seal))


def conveyor(iso, length, w=1.7):
    belt = ibox(iso, 0, 0, 0, length, w, 0.18, BELT_TOP, BELT_L, BELT_R, stroke=DK, sw=3)
    dashes = VGroup(*[Line(iso.p(0.5 + i * 0.9, w / 2, 0.18), iso.p(0.9 + i * 0.9, w / 2, 0.18), color=GHOST, stroke_width=4)
                      for i in range(int((length - 0.5) / 0.9))])
    return VGroup(belt, dashes)


def gate(iso, x, w=1.7):
    """One dark post on the near side with a lamp (ghost until lit) and a kraft barrier arm across the belt."""
    post = ibox(iso, x, -0.45, 0, 0.28, 0.28, 1.5, DARK_TOP, DARK_L, DARK_R)
    arm = ibox(iso, x + 0.06, -0.3, 1.3, 0.16, w + 0.45, 0.14, BOX_TOP, BOX_L, BOX_R, stroke=DK, sw=2)
    lamp = Dot(iso.p(x + 0.14, -0.31, 1.72), radius=0.1, color=GHOST)
    g = VGroup(post, arm, lamp)
    g.post, g.arm, g.lamp = post, arm, lamp
    return g


def page_g(iso, x0, y0, z0, w=1.1, d=1.4):
    """A page with a deep-kraft outline, for pages lying inside an ink-outlined desk (GATE T reads ink-in-ink as stacked text)."""
    slab = iso.box(x0, y0, z0, w, d, 0.06, PAGE_TOP, PAGE_L, PAGE_R, sw=1.5, stroke=DK)
    zt = z0 + 0.06
    lines = VGroup(*[Line(iso.p(x0 + 0.2, y0 + d * f, zt), iso.p(x0 + w - 0.2, y0 + d * f, zt), color=GHOST, stroke_width=4) for f in (0.3, 0.5, 0.7)])
    dot = Dot(iso.p(x0 + 0.2, y0 + d * 0.86, zt), radius=0.06, color=TERRA)
    return VGroup(slab, lines, dot)


def tag_shape(iso, x, y, z=0.0, fill=BOX_TOP):
    """A small kraft tag lying flat (no text on it)."""
    return ibox(iso, x, y, z, 0.5, 0.34, 0.05, fill, BOX_L, BOX_R, stroke=DK, sw=2)


def cabinet(iso, x, y):
    """Database cabinet: a tall kraft box with three drawer lines and pulls on its front face."""
    body = ibox(iso, x, y, 0, 1.3, 1.1, 2.0)
    rows = VGroup()
    for i in range(3):
        z = 0.25 + i * 0.6
        rows.add(Line(iso.p(x, y + 0.15, z), iso.p(x, y + 0.95, z), color=DK, stroke_width=3))
        rows.add(Dot(iso.p(x, y + 0.55, z + 0.28), radius=0.05, color=DK))
    return VGroup(body, rows)


def desk(iso, x, y, w=3.0, d=2.0):
    top = ibox(iso, x, y, 0.5, w, d, 0.12)
    legs = VGroup(*[ibox(iso, x + dx, y + dy, 0, 0.14, 0.14, 0.5, BOX_TOP, BOX_L, BOX_R, stroke=DK, sw=2)
                    for dx, dy in ((0.1, 0.1), (w - 0.24, 0.1), (0.1, d - 0.24), (w - 0.24, d - 0.24))])
    return VGroup(legs, top)


def shelf(iso, x, y, w=3.6):
    board = ibox(iso, x, y, 0.9, w, 1.6, 0.14)
    legs = VGroup(*[ibox(iso, x + dx, y + dy, 0, 0.16, 0.16, 0.9, BOX_TOP, BOX_L, BOX_R, stroke=DK, sw=2)
                    for dx, dy in ((0.15, 0.15), (w - 0.31, 0.15), (0.15, 1.29), (w - 0.31, 1.29))])
    return VGroup(legs, board)


def laptop(iso, x, y):
    base = ibox(iso, x, y, 0.62, 1.6, 1.2, 0.1, stroke=DK, sw=3)
    screen = iso.quad([(x, y + 1.2, 0.72), (x + 1.6, y + 1.2, 0.72), (x + 1.6, y + 1.2, 2.0), (x, y + 1.2, 2.0)], DARK_L, INK, 4)
    return VGroup(base, screen)


def pill_cmd(cx, cy):
    """A command line: a white pill with a prompt chevron (no letters)."""
    body = RoundedRectangle(width=2.4, height=0.55, corner_radius=0.275, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([cx, cy, 0])
    chev = VGroup(Line([cx - 0.85, cy + 0.12, 0], [cx - 0.7, cy, 0], color=INK, stroke_width=4),
                  Line([cx - 0.7, cy, 0], [cx - 0.85, cy - 0.12, 0], color=INK, stroke_width=4))
    cur = Line([cx - 0.5, cy - 0.1, 0], [cx - 0.5, cy + 0.1, 0], color=INK, stroke_width=4)
    return VGroup(body, chev, cur)


def clip(pt):
    a = np.array(pt)
    return VGroup(Line(a + np.array([-0.18, 0.0, 0]), a + np.array([-0.18, 0.5, 0]), color=INK, stroke_width=5),
                  Line(a + np.array([-0.18, 0.5, 0]), a + np.array([0.14, 0.5, 0]), color=INK, stroke_width=5),
                  Line(a + np.array([0.14, 0.5, 0]), a + np.array([0.14, 0.05, 0]), color=INK, stroke_width=5))


def planned_tag(side="left"):
    """Corner tag marking a drawing of the tool that is not built yet (same style as B05's 'Constructed' tag)."""
    x0 = -5.9 if side == "left" else 3.4
    fold = Polygon([x0, 2.8, 0], [x0 + 0.5, 2.8, 0], [x0 + 0.5, 3.15, 0], fill_color=BOX_L, fill_opacity=1, stroke_color=DK, stroke_width=2)
    return VGroup(fold, lab("Planned", (x0 + 0.8, 2.95), edge=LEFT))


# ═════════════════════════════ B01 · the problem ═════════════════════════════
class B01_Problem(Scene):
    ISO = (-0.181, -3.385, 1.046)
    FIT = (-5.8, 5.8, -1.8, 2.9)

    def make(self, iso):
        o = {}
        o["desk"] = desk(iso, 0.0, 4.0, 3.4, 2.2)
        o["pb"] = posting_box(iso, 0.7, 4.7, 0.62)
        o["desk2"] = desk(iso, 4.2, 0.0, 2.4, 2.2)
        o["pages"] = [iso.page(4.7, 0.5, 0.62 + 0.14 * i, 1.0, 1.3) for i in range(4)]
        o["l_post"] = lab("Posting", iso.p(1.7, 4.0, 0), dy=-0.8)
        o["l_hour"] = lab("1 hour", iso.p(5.4, 0.0, 0), dy=-0.8)
        return o

    def construct(self):
        o = self.make(Iso(*self.ISO))
        self.add(o["desk"], o["desk2"])
        go(self, 0.03, 0.16, FadeIn(o["pb"], shift=DOWN * 0.8))
        go(self, 0.18, 0.26, FadeIn(o["l_post"]))
        go(self, 0.28, 0.40, LaggedStart(*[FadeIn(p, shift=DOWN * 0.7) for p in o["pages"]], lag_ratio=0.35))
        go(self, 0.40, 0.44, FadeIn(o["l_hour"]))
        go(self, 0.58, 0.69, grey_out(o["pb"]))
        finish(self)


# ═════════════════════════════ B02 · what it is ═════════════════════════════
GX = (1.4, 3.2, 5.0)


class B02_Gates(Scene):
    ISO = (-3.249, -1.800, 0.920)
    FIT = (-5.6, 4.2, -1.8, 2.9)

    def make(self, iso):
        o = {}
        o["belt"] = conveyor(iso, 6.4)
        o["gates"] = [gate(iso, x) for x in GX]
        o["pb"] = posting_box(iso, 0.3, 0.35, 0.18)
        o["rep"] = iso.page(7.0, 0.2, 0.0, 1.3, 1.6)
        o["ck"] = check(*iso.p(7.65, 1.0, 0.1)[:2], s=0.22)
        names = ("Live?", "CPT fit?", "Sponsor record?")
        o["labs"] = [lab(n, iso.p(x, -0.45, 0), dx=0.05, dy=-0.6, edge=LEFT) for n, x in zip(names, GX)]
        o["planned"] = planned_tag("left")
        return o

    def construct(self):
        iso = Iso(*self.ISO)
        o = self.make(iso)
        self.add(o["belt"])
        go(self, 0.02, 0.16, LaggedStart(*[FadeIn(g, shift=UP * 0.5) for g in o["gates"]], lag_ratio=0.3))
        go(self, 0.18, 0.28, FadeIn(o["pb"], shift=DOWN * 0.6), FadeIn(o["rep"]))
        go(self, 0.30, 0.42, LaggedStart(*[FadeIn(l) for l in o["labs"]], lag_ratio=0.25), FadeIn(o["planned"]))
        go(self, 0.56, 0.66, o["pb"].animate.shift(iso.v(5.0, 0, 0)), rate_func=linear)
        go(self, 0.66, 0.70, *[g.lamp.animate.set_color(TERRA) for g in o["gates"]], Create(o["ck"]))
        finish(self)


# ═════════════════════════════ B03 · alternatives ═════════════════════════════
class B03_Alternatives(Scene):
    ISO = (-1.306, -3.565, 1.207)
    FIT = (-5.8, 5.8, -1.8, 2.9)

    def make(self, iso):
        o = {}
        o["cab"] = cabinet(iso, 0.6, 3.4)
        o["dk"] = desk(iso, 3.0, 0.0, 3.8, 2.4)
        o["scatter"] = [iso.page(3.5, 0.3, 0.62, 1.0, 1.3), iso.page(4.9, 0.2, 0.62, 1.0, 1.3),
                        iso.page(4.2, 1.2, 0.62, 1.0, 1.3), iso.page(5.5, 1.1, 0.62, 1.0, 1.3)]
        o["drawer"] = ibox(iso, -0.05, 3.55, 1.0, 0.65, 0.7, 0.35, BOX_TOP, BOX_L, BOX_R, stroke=DK, sw=2)
        o["peek"] = iso.page(0.1, 3.68, 1.35, 0.5, 0.45)
        o["l_cab"] = lab("MyVisaJobs", iso.p(0.6, 3.95, 0), dy=-0.8)
        o["l_man"] = lab("Manual check", iso.p(4.9, 0.0, 0.0), dy=-0.95)
        return o

    def construct(self):
        o = self.make(Iso(*self.ISO))
        self.add(o["dk"])
        go(self, 0.03, 0.16, FadeIn(o["cab"], shift=UP * 0.5))
        go(self, 0.17, 0.25, FadeIn(o["l_cab"]))
        go(self, 0.27, 0.40, LaggedStart(*[FadeIn(p, shift=DOWN * 0.6) for p in o["scatter"]], lag_ratio=0.3))
        go(self, 0.40, 0.44, FadeIn(o["l_man"]))
        go(self, 0.58, 0.68, FadeIn(o["drawer"], shift=LEFT * 0.4), FadeIn(o["peek"], shift=LEFT * 0.4))
        finish(self)


# ═════════════════════════════ B04 · what's different ═════════════════════════════
class B04_StopEarly(Scene):
    ISO = (-3.249, -1.800, 0.920)
    FIT = (-5.6, 4.2, -1.8, 2.9)

    def make(self, iso):
        o = {}
        o["belt"] = conveyor(iso, 6.4)
        o["gates"] = [gate(iso, x) for x in GX]
        o["pb"] = posting_box(iso, 0.3, 0.35, 0.18)
        o["rep"] = iso.page(7.0, 0.2, 0.0, 1.3, 1.6)
        o["tag"] = tag_shape(iso, 7.2, 1.9, 0.0)
        o["l_stop"] = lab("Stop early", iso.p(GX[0], -0.45, 0), dx=0.05, dy=-0.6, edge=LEFT)
        o["l_rec"] = lab("No record", iso.p(8.3, 0.4, 0), dx=0.35, dy=-0.5, edge=LEFT)
        o["planned"] = planned_tag("left")
        return o

    def construct(self):
        iso = Iso(*self.ISO)
        o = self.make(iso)
        g = o["gates"]
        self.add(o["belt"])
        go(self, 0.02, 0.14, LaggedStart(*[FadeIn(x, shift=UP * 0.5) for x in g], lag_ratio=0.3))
        go(self, 0.16, 0.26, FadeIn(o["pb"], shift=DOWN * 0.6), FadeIn(o["rep"]))
        go(self, 0.28, 0.42, FadeIn(o["l_stop"]), FadeIn(o["l_rec"]), FadeIn(o["planned"]))
        go(self, 0.57, 0.66, g[0].lamp.animate.set_color(TERRA), g[0].arm.animate.shift(iso.v(0, 0, -0.8)),
           g[1].animate.set_opacity(0.3), g[2].animate.set_opacity(0.3))
        go(self, 0.66, 0.70, FadeIn(o["tag"], shift=DOWN * 0.3))
        finish(self)


# ═════════════════════════════ B05 · who opens it ═════════════════════════════
class B05_Reader(Scene):
    ISO = (-1.026, -3.140, 0.984)
    FIT = (-5.8, 4.6, -1.8, 2.7)

    def make(self, iso):
        o = {}
        o["desk"] = desk(iso, 0.0, 3.2, 4.4, 2.4)
        o["lap"] = laptop(iso, 0.6, 3.8)
        o["readme"] = page_g(iso, 2.6, 3.5, 0.62, 1.0, 1.2)
        o["desk2"] = desk(iso, 4.2, 0.0, 2.4, 2.4)
        o["rep"] = page_g(iso, 4.6, 0.5, 0.62, 1.2, 1.5)
        o["tags"] = [tag_shape(iso, 4.8, 0.55 + 0.4 * i, 0.68) for i in range(3)]
        c = iso.p(2.2, 2.3, 0.0)
        o["cmd"] = pill_cmd(c[0] + 0.2, c[1] - 0.3)
        o["l_hm"] = lab("Hiring manager", iso.p(0.0, 3.2, 0.0), dx=0.2, dy=-1.2, edge=LEFT)
        o["l_con"] = lab("Constructed", (3.45, 2.95), edge=LEFT)
        o["fold"] = Polygon([2.65, 2.8, 0], [3.15, 2.8, 0], [3.15, 3.15, 0], fill_color=BOX_L, fill_opacity=1, stroke_color=DK, stroke_width=2)
        return o

    def construct(self):
        o = self.make(Iso(*self.ISO))
        self.add(o["desk"], o["desk2"])
        go(self, 0.03, 0.14, FadeIn(o["lap"], shift=DOWN * 0.6))
        go(self, 0.16, 0.24, FadeIn(o["l_hm"]))
        go(self, 0.26, 0.36, FadeIn(o["readme"], shift=DOWN * 0.5), FadeIn(o["fold"]))
        go(self, 0.36, 0.43, FadeIn(o["l_con"]))
        go(self, 0.57, 0.62, FadeIn(o["cmd"]))
        go(self, 0.62, 0.69, FadeIn(o["rep"], shift=LEFT * 0.4), LaggedStart(*[GrowFromCenter(t) for t in o["tags"]], lag_ratio=0.3))
        finish(self)


# ═════════════════════════════ B07 · the break test ═════════════════════════════
class B07_BreakTest(Scene):
    ISO = (-2.309, -2.861, 1.034)
    FIT = (-5.8, 3.6, -1.8, 2.9)

    def make(self, iso):
        o = {}
        o["cab"] = cabinet(iso, 0.6, 3.4)
        o["floor"] = ibox(iso, 3.0, -0.2, 0, 3.4, 2.4, 0.12, BELT_TOP, BELT_L, BELT_R, stroke=DK, sw=3)
        o["pb"] = posting_box(iso, 3.4, 0.9, 0.12)
        o["rep"] = iso.page(5.0, 0.3, 0.12, 1.2, 1.5)
        o["tag"] = tag_shape(iso, 5.2, 1.3, 0.2)
        o["l_not"] = lab("Not in data", iso.p(3.0, -0.2, 0), dx=-0.9, dy=-0.6, edge=LEFT)
        o["l_rec"] = lab("No record", iso.p(6.4, -0.2, 0), dx=0.35, dy=0.25, edge=LEFT)
        return o

    def construct(self):
        o = self.make(Iso(*self.ISO))
        self.add(o["cab"], o["floor"])
        go(self, 0.04, 0.20, FadeIn(o["pb"], shift=DOWN * 0.6))
        go(self, 0.22, 0.34, FadeIn(o["l_not"]))
        go(self, 0.34, 0.43, FadeIn(o["l_rec"]))
        go(self, 0.58, 0.64, FadeIn(o["rep"], shift=LEFT * 0.4))
        go(self, 0.64, 0.69, GrowFromCenter(o["tag"]))
        finish(self)


# ═════════════════════════════ B08 · what it proves ═════════════════════════════
class B08_Skills(Scene):
    ISO = (0.000, -3.457, 1.098)
    FIT = (-5.8, 5.8, -1.8, 2.9)

    def make(self, iso):
        o = {}
        xs = (0.0, 1.6, 3.2, 4.8)
        ys = (4.8, 3.2, 1.6, 0.0)
        o["blocks"] = [ibox(iso, x, y, 0, 1.3, 1.3, 1.2) for x, y in zip(xs, ys)]
        o["lamps"] = [Dot(iso.p(x + 0.65, y + 0.65, 1.2), radius=0.1, color=GHOST) for x, y in zip(xs, ys)]
        o["rings"] = [Circle(radius=0.28, color=TERRA, stroke_width=4).move_to(lp.get_center()) for lp in o["lamps"]]
        names = ("Verify", "Source", "Evaluate")
        o["labs"] = [lab(n, iso.p(x, y, 0), dy=-0.55) for n, x, y in zip(names, xs, ys)]
        return o

    def construct(self):
        o = self.make(Iso(*self.ISO))
        self.add(*o["blocks"])
        go(self, 0.03, 0.14, LaggedStart(*[FadeIn(l) for l in o["lamps"]], lag_ratio=0.2))
        go(self, 0.16, 0.30, LaggedStart(*[FadeIn(l) for l in o["labs"]], lag_ratio=0.3))
        go(self, 0.31, 0.40, o["lamps"][0].animate.set_color(TERRA), Create(o["rings"][0]))
        go(self, 0.58, 0.62, o["lamps"][1].animate.set_color(TERRA), Create(o["rings"][1]))
        go(self, 0.62, 0.66, o["lamps"][2].animate.set_color(TERRA), Create(o["rings"][2]))
        go(self, 0.66, 0.70, o["lamps"][3].animate.set_color(TERRA), Create(o["rings"][3]))
        finish(self)


# ═════════════════════════════ B09 · in, out, first ═════════════════════════════
class B09_InOutFirst(Scene):
    ISO = (-0.838, -1.537, 0.715)
    FIT = (-4.8, 5.6, -1.8, 2.9)

    def make(self, iso):
        o = {}
        o["sign"] = ibox(iso, 0.0, 4.6, 0.9, 0.18, 1.8, 1.4)
        o["sup"] = ibox(iso, 0.0, 5.4, 0, 0.18, 0.3, 0.9, BOX_TOP, BOX_L, BOX_R, stroke=DK, sw=2)
        o["x1"] = Line(iso.p(-0.05, 4.75, 1.0), iso.p(-0.05, 6.25, 2.2), color=INK, stroke_width=7)
        o["x2"] = Line(iso.p(-0.05, 6.25, 1.0), iso.p(-0.05, 4.75, 2.2), color=INK, stroke_width=7)
        o["l_not"] = lab("Not advice", iso.p(0.0, 5.5, 0), dy=-0.8)
        o["belt"] = ibox(iso, 2.4, 0.0, 0, 4.4, 1.7, 0.18, BELT_TOP, BELT_L, BELT_R, stroke=DK, sw=3)
        o["pb"] = posting_box(iso, 2.7, 0.35, 0.18)
        c = iso.p(2.6, -0.95, 0.0)
        o["cmd"] = pill_cmd(c[0] - 0.3, c[1] - 0.3)
        o["rep"] = iso.page(7.2, 0.0, 0.0, 1.2, 1.5)
        o["log"] = [iso.page(7.2, -2.0, 0.0 + 0.1 * i, 1.2, 1.5) for i in range(3)]
        o["l_first"] = lab("First run", iso.p(7.2, -2.0, 0), dx=0.1, dy=-0.6)
        o["planned"] = planned_tag("right")
        return o

    def construct(self):
        iso = Iso(*self.ISO)
        o = self.make(iso)
        self.add(o["belt"])
        go(self, 0.03, 0.14, FadeIn(o["sign"], shift=DOWN * 0.5), FadeIn(o["sup"]))
        go(self, 0.15, 0.24, Create(o["x1"]), Create(o["x2"]))
        go(self, 0.25, 0.32, FadeIn(o["l_not"]))
        go(self, 0.32, 0.40, FadeIn(o["pb"], shift=DOWN * 0.5), FadeIn(o["cmd"]))
        go(self, 0.40, 0.44, FadeIn(o["l_first"]), FadeIn(o["planned"]))
        go(self, 0.57, 0.67, o["pb"].animate.shift(iso.v(3.0, 0, 0)), rate_func=linear)
        go(self, 0.67, 0.70, FadeIn(o["rep"]), *[FadeIn(p) for p in o["log"]])
        finish(self)


# ═════════════════════════════ B10 · what could sink it ═════════════════════════════
class B10_Misread(Scene):
    ISO = (-0.094, -3.468, 1.080)
    FIT = (-5.8, 5.8, -1.8, 2.9)

    def make(self, iso):
        o = {}
        o["rep"] = iso.page(0.0, 4.4, 0.0, 1.3, 1.7)
        o["tag"] = tag_shape(iso, 0.2, 4.5, 0.07)
        o["sign"] = ibox(iso, 2.4, 2.2, 0.8, 0.18, 1.7, 1.2, BOX_TOP, BOX_L, BOX_R)
        o["sup"] = ibox(iso, 2.4, 2.9, 0, 0.18, 0.3, 0.8, BOX_TOP, BOX_L, BOX_R, stroke=DK, sw=2)
        o["arrow"] = Arrow(iso.p(1.2, 4.7, 0.4), iso.p(1.95, 3.3, 1.0), color=INK, stroke_width=6, buff=0, max_tip_length_to_length_ratio=0.2)
        o["x1"] = Line(iso.p(2.35, 2.3, 0.9), iso.p(2.35, 3.8, 2.0), color=INK, stroke_width=7)
        o["x2"] = Line(iso.p(2.35, 3.8, 0.9), iso.p(2.35, 2.3, 2.0), color=INK, stroke_width=7)
        o["rng"] = iso.page(4.8, 0.4, 0.0, 1.9, 1.0)
        o["bar"] = Line(iso.p(5.2, 0.9, 0.06), iso.p(6.4, 0.9, 0.06), color=INK, stroke_width=6)
        o["tk"] = VGroup(Line(iso.p(5.2, 0.7, 0.06), iso.p(5.2, 1.1, 0.06), color=INK, stroke_width=5),
                         Line(iso.p(6.4, 0.7, 0.06), iso.p(6.4, 1.1, 0.06), color=INK, stroke_width=5))
        o["cl"] = clip(iso.p(6.5, 1.4, 0.06))
        o["l_mis"] = lab("Misread", iso.p(1.2, 4.0, 0), dy=-1.0)
        o["l_rng"] = lab("Date range", iso.p(5.7, 0.4, 0), dy=-0.8)
        o["planned"] = planned_tag("right")
        return o

    def construct(self):
        o = self.make(Iso(*self.ISO))
        self.add(o["rep"], o["tag"])
        go(self, 0.03, 0.14, FadeIn(o["sign"], shift=DOWN * 0.5), FadeIn(o["sup"]))
        go(self, 0.15, 0.26, GrowFromCenter(o["arrow"]))
        go(self, 0.26, 0.34, FadeIn(o["l_mis"]))
        go(self, 0.34, 0.40, Create(o["x1"]), Create(o["x2"]))
        go(self, 0.40, 0.44, FadeIn(o["l_rng"]), FadeIn(o["planned"]))
        go(self, 0.57, 0.64, FadeIn(o["rng"], shift=LEFT * 0.4), Create(o["bar"]), Create(o["tk"]))
        go(self, 0.64, 0.69, FadeIn(o["cl"], shift=DOWN * 0.3))
        finish(self)


# ═════════════════════════════ B11 · why this project ═════════════════════════════
class B11_Shelves(Scene):
    ISO = (-0.925, -3.643, 0.971)
    FIT = (-5.8, 5.8, -1.8, 2.9)

    def make(self, iso):
        o = {}
        o["s1"] = shelf(iso, 0.0, 4.2)
        o["s2"] = shelf(iso, 4.4, 0.0)
        o["have"] = [ibox(iso, 0.4 + 1.1 * i, 4.5, 1.04, 0.9, 0.9, 0.7 + 0.1 * i) for i in range(3)]
        o["newb"] = [ibox(iso, 4.8 + 1.2 * i, 0.3, 1.04, 0.9, 0.9, 0.8) for i in range(2)]
        o["l_have"] = lab("Already have", iso.p(1.8, 4.2, 0), dy=-0.8)
        o["l_learn"] = lab("Learning", iso.p(6.2, 0.0, 0), dy=-0.8)
        return o

    def construct(self):
        o = self.make(Iso(*self.ISO))
        self.add(o["s1"], o["s2"])
        go(self, 0.03, 0.16, LaggedStart(*[FadeIn(b, shift=DOWN * 0.5) for b in o["have"]], lag_ratio=0.3))
        go(self, 0.17, 0.26, FadeIn(o["l_have"]))
        go(self, 0.27, 0.36, FadeIn(o["l_learn"]))
        go(self, 0.58, 0.64, FadeIn(o["newb"][0], shift=DOWN * 0.8))
        go(self, 0.64, 0.69, FadeIn(o["newb"][1], shift=DOWN * 0.8))
        finish(self)
