import math, random, re

W, H = 800, 600
_id = [0]


def uid():
    _id[0] += 1
    return f"c{_id[0]}"


def rot(x, y, a, inner):
    return f'<g transform="translate({x:.1f} {y:.1f}) rotate({a})">{inner}</g>'


def circle(cx, cy, r, fill, stroke=None, sw=1, op=1):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" opacity="{op}"{s}/>'


def ell(cx, cy, rx, ry, fill, stroke=None, sw=1, a=0, op=1):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return (f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{fill}" opacity="{op}"'
            f' transform="rotate({a} {cx:.1f} {cy:.1f})"{s}/>')


def poly(pts, fill, stroke=None, sw=1):
    s = f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"' if stroke else ""
    p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polygon points="{p}" fill="{fill}"{s}/>'


def pie(cx, cy, r, a0, a1, fill, stroke=None, sw=1):
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    large = 1 if (a1 - a0) % 360 > 180 else 0
    s = f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"' if stroke else ""
    return f'<path d="M{cx:.1f} {cy:.1f} L{x0:.1f} {y0:.1f} A{r} {r} 0 {large} 1 {x1:.1f} {y1:.1f} Z" fill="{fill}"{s}/>'


# ---------- food ----------
def grapes(cx, cy, base="#6b3f7a", hl="#fff", r=11, flip=1):
    out = []
    rows = [3, 4, 4, 3, 2, 1]
    for i, n in enumerate(rows):
        for j in range(n):
            x = cx + (j - (n - 1) / 2) * r * 2 * 0.95
            y = cy + i * r * 1.65
            out.append(circle(x, y, r, base, "#00000022", 1))
            out.append(circle(x - r * .3, y - r * .35, r * .3, hl, op=.35))
    out.append(f'<path d="M{cx} {cy-r} q4 -16 18 -22" stroke="#5f7a4a" stroke-width="3" fill="none" stroke-linecap="round"/>')
    return "".join(out)


def salami_slice(cx, cy, r=24, seed=0):
    rnd = random.Random(seed)
    o = [circle(cx, cy, r, "#b5453d", "#7a2b27", 2.5)]
    for _ in range(9):
        a, d = rnd.random() * 6.28, rnd.random() * (r - 7)
        o.append(circle(cx + d * math.cos(a), cy + d * math.sin(a), rnd.uniform(1.4, 2.6), "#f0c2b4", op=.9))
    return "".join(o)


def salami_fold(cx, cy, r=26, a=0, seed=0):
    rnd = random.Random(seed)
    inner = [f'<path d="M{-r} 0 A{r} {r} 0 0 1 {r} 0 Z" fill="#b5453d" stroke="#7a2b27" stroke-width="2.5" stroke-linejoin="round"/>']
    for _ in range(6):
        x, y = rnd.uniform(-r + 6, r - 6), rnd.uniform(-r + 8, -3)
        inner.append(circle(x, y, rnd.uniform(1.3, 2.3), "#f0c2b4", op=.9))
    return rot(cx, cy, a, "".join(inner))


def prosciutto(x0, y0, x1, y1, bend=26):
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    d = f"M{x0} {y0} Q{mx} {my-bend} {mx} {my} T{x1} {y1}"
    return (f'<path d="{d}" stroke="#d98585" stroke-width="15" fill="none" stroke-linecap="round"/>'
            f'<path d="{d}" stroke="#f3bcbc" stroke-width="5" fill="none" stroke-linecap="round" opacity=".8"/>')


def cracker(cx, cy, s=34, a=0, round_=False):
    inner = []
    if round_:
        inner.append(circle(0, 0, s / 2, "#dcb680", "#b98c52", 2))
        pts = [(-6, -6), (6, -6), (0, 0), (-6, 7), (7, 6)]
    else:
        inner.append(f'<rect x="{-s/2}" y="{-s/2}" width="{s}" height="{s}" rx="5" fill="#dcb680" stroke="#b98c52" stroke-width="2"/>')
        pts = [(-8, -8), (8, -8), (-8, 8), (8, 8), (0, 0)]
    for x, y in pts:
        inner.append(circle(x, y, 1.8, "#b98c52"))
    return rot(cx, cy, a, "".join(inner))


def wedge(cx, cy, s=40, a=0, top="#f3cf5b", side="#d9a92f", holes=True):
    inner = [
        poly([(-s, s * .35), (s, s * .1), (s * .85, -s * .5)], top, "#b88a1f", 2),
        poly([(-s, s * .35), (s, s * .1), (s, s * .1 + s * .32), (-s, s * .35 + s * .32)], side, "#b88a1f", 2),
    ]
    if holes:
        inner += [ell(-s * .35, s * .12, 4, 3, side), ell(s * .25, 0, 3, 2.4, side), ell(s * .55, -s * .2, 2.5, 2, side)]
    return rot(cx, cy, a, "".join(inner))


def cube(cx, cy, s=20, a=0, color="#f3cf5b", edge="#b88a1f"):
    return rot(cx, cy, a, f'<rect x="{-s/2}" y="{-s/2}" width="{s}" height="{s}" rx="3" fill="{color}" stroke="{edge}" stroke-width="2"/>'
               f'<rect x="{-s/2+3}" y="{-s/2+3}" width="{s*.35}" height="{s*.35}" rx="1.5" fill="#fff" opacity=".25"/>')


def brie(cx, cy, r=62):
    mid = 330
    o = [circle(cx + 4, cy + 6, r, "#00000018")]
    o.append(pie(cx, cy, r, 0, 300, "#f6efd8", "#d8cba2", 2.5))
    o.append(pie(cx, cy, r - 7, 0, 300, "#f6e49a"))
    gx, gy = 22 * math.cos(math.radians(mid)), 22 * math.sin(math.radians(mid))
    o.append(f'<g transform="translate({gx:.1f} {gy:.1f})">{pie(cx, cy, r, 300, 360, "#f6efd8", "#d8cba2", 2.5)}{pie(cx, cy, r - 7, 303, 357, "#f9eda8")}</g>')
    return "".join(o)


def strawberry(cx, cy, s=17, a=0, dipped=False):
    cid = uid()
    body = f"M0 {-s*.7} C{s*.95} {-s*.95} {s*1.05} {s*.3} 0 {s*1.0} C{-s*1.05} {s*.3} {-s*.95} {-s*.95} 0 {-s*.7} Z"
    inner = [f'<path d="{body}" fill="#d63a4a" stroke="#a82434" stroke-width="2"/>']
    if dipped:
        inner.append(f'<clipPath id="{cid}"><path d="{body}"/></clipPath>'
                     f'<g clip-path="url(#{cid})"><path d="M{-s*1.3} {s*.15} q{s*.6} {s*.35} {s*1.3} {s*.1} t{s*1.3} {-s*.1} V{s*1.3} H{-s*1.3}Z" fill="#4b2a1d"/></g>')
    for x, y in [(-6, -2), (5, -4), (0, 3), (-4, 8), (6, 4)]:
        inner.append(ell(x * s / 17, y * s / 17, 1.2, 1.8, "#f7d77a", op=.9))
    inner.append(poly([(0, -s * .7), (-s * .5, -s * .95), (-s * .15, -s * .55), (0, -s * 1.1), (s * .15, -s * .55), (s * .5, -s * .95)], "#4f8a43"))
    return rot(cx, cy, a, "".join(inner))


def blueberry(cx, cy, r=8):
    return circle(cx, cy, r, "#3d4a8f", "#2a336b", 1.5) + circle(cx - r * .3, cy - r * .3, r * .28, "#fff", op=.3) + circle(cx, cy - r * .1, r * .22, "#2a336b")


def raspberry(cx, cy, r=9):
    o = [circle(cx, cy, r, "#b8223f")]
    for dx, dy in [(-4, -3), (4, -3), (0, 0), (-4, 4), (4, 4), (0, -6), (0, 6)]:
        o.append(circle(cx + dx * r / 9, cy + dy * r / 9, r * .33, "#d63a55", "#8e1a31", 1))
    return "".join(o)


def olive(cx, cy, a=0, color="#7d8a3a", stuffed=True):
    inner = ell(0, 0, 11, 8, color, "#4f5a22", 1.5)
    if stuffed:
        inner += circle(-5, 0, 3, "#d6483f")
    inner += ell(3, -3, 3, 1.5, "#fff", op=.3)
    return rot(cx, cy, a, inner)


def fig(cx, cy, r=20, a=0):
    inner = (circle(0, 0, r, "#5b2a4e", "#3d1a35", 2) + circle(0, 0, r * .74, "#d4608a") + circle(0, 0, r * .3, "#f2a9bf"))
    for k in range(10):
        t = k * 36
        inner += circle(r * .5 * math.cos(math.radians(t)), r * .5 * math.sin(math.radians(t)), 1.4, "#f7d3df")
    return rot(cx, cy, a, inner)


def almond(cx, cy, a=0):
    return ell(cx, cy, 9, 5.5, "#b98558", "#8d5f38", 1.5, a) + ell(cx - 2, cy - 1.5, 4, 1.4, "#fff", a=a, op=.25)


def apricot(cx, cy, a=0):
    return ell(cx, cy, 13, 10, "#e08a2c", "#b5651a", 1.5, a) + ell(cx - 3, cy - 3, 5, 2, "#fff", a=a, op=.25)


def rosemary(x, y, a=0, L=70):
    inner = [f'<path d="M0 0 Q{L/2} -8 {L} 0" stroke="#5f7a4a" stroke-width="2.5" fill="none" stroke-linecap="round"/>']
    for i in range(1, 11):
        px = L * i / 11
        py = -8 * (1 - (2 * i / 11 - 1) ** 2) * .9
        inner.append(ell(px, py - 4, 7, 1.7, "#4f8a43", a=-55))
        inner.append(ell(px, py + 4, 7, 1.7, "#6aa05a", a=55))
    return rot(x, y, a, "".join(inner))


def mint(x, y, a=0):
    inner = '<path d="M0 0 L26 0" stroke="#4f8a43" stroke-width="2.5" stroke-linecap="round"/>'
    for px, py, ang in [(10, -6, -40), (10, 6, 40), (20, -6, -40), (20, 6, 40), (28, 0, 0)]:
        inner += ell(px, py, 8, 5, "#5ea352", "#3f7a36", 1, ang)
    return rot(x, y, a, inner)


def flower(cx, cy, r=9, petal="#b88ad8", center="#f2b84b"):
    o = []
    for k in range(5):
        a = k * 72
        o.append(ell(cx + r * .8 * math.cos(math.radians(a)), cy + r * .8 * math.sin(math.radians(a)), r * .75, r * .5, petal, "#00000014", 1, a))
    o.append(circle(cx, cy, r * .38, center))
    return "".join(o)


def bowl(cx, cy, r, fill, rim="#f4f1ea", edge="#cfc9b8", spoon=False, shine=True):
    o = [circle(cx + 3, cy + 5, r + 2, "#00000020"), circle(cx, cy, r, rim, edge, 2), circle(cx, cy, r * .78, fill)]
    if shine:
        o.append(ell(cx - r * .25, cy - r * .3, r * .28, r * .12, "#fff", a=-30, op=.35))
    if spoon:
        o.append(f'<path d="M{cx} {cy} L{cx+r*1.1} {cy-r*.9}" stroke="#a97c50" stroke-width="4" stroke-linecap="round"/>')
    return "".join(o)


def citrus(cx, cy, r=22, rind="#7fae3d", flesh="#d8ec9a", line="#a9cf5f", segs=8):
    o = [circle(cx, cy, r, rind, "#00000018", 1.5), circle(cx, cy, r * .86, "#f7f3d8"), circle(cx, cy, r * .78, flesh)]
    for k in range(segs):
        a = math.radians(k * 360 / segs)
        o.append(f'<line x1="{cx}" y1="{cy}" x2="{cx+r*.78*math.cos(a):.1f}" y2="{cy+r*.78*math.sin(a):.1f}" stroke="{line}" stroke-width="2"/>')
    o.append(circle(cx, cy, 2.5, "#f7f3d8"))
    return "".join(o)


def cucumber(cx, cy, r=15):
    o = [circle(cx, cy, r, "#4f7f3a"), circle(cx, cy, r - 2.5, "#cfe3a8"), circle(cx, cy, r - 6, "#e4f0c4")]
    for k in range(6):
        a = math.radians(k * 60 + 15)
        o.append(ell(cx + (r - 8) * .6 * math.cos(a), cy + (r - 8) * .6 * math.sin(a), 1.6, 1, "#a8c47a"))
    return "".join(o)


def tomato(cx, cy, r=12):
    return (circle(cx, cy, r, "#d6392f", "#a52a22", 1.5) + circle(cx - r * .35, cy - r * .35, r * .25, "#fff", op=.35)
            + poly([(cx, cy - r * .7), (cx - 5, cy - r * .95), (cx - 1, cy - r * .5), (cx + 1, cy - r * 1.1), (cx + 3, cy - r * .5), (cx + 6, cy - r * .9)], "#4f8a43"))


def pepper(cx, cy, a=0, color="#f08a24", edge="#b8620f"):
    return rot(cx, cy, a, f'<rect x="-20" y="-8" width="40" height="16" rx="8" fill="{color}" stroke="{edge}" stroke-width="2"/>'
               f'<path d="M-20 0 q-6 -2 -9 -8" stroke="#4f8a43" stroke-width="3" fill="none" stroke-linecap="round"/>'
               f'<ellipse cx="-8" cy="-3" rx="8" ry="1.8" fill="#fff" opacity=".3"/>')


def pretzel(cx, cy, a=0):
    return rot(cx, cy, a, '<rect x="-16" y="-10" width="32" height="20" rx="4" fill="#c98b45" stroke="#9a6525" stroke-width="2"/>'
               + "".join(circle(x, y, 1.6, "#f5e6c4") for x, y in [(-9, -4), (-2, 3), (6, -3), (10, 5), (-8, 6)]))


def macaron(cx, cy, color="#f4a6b9", edge="#d6788f", a=0):
    inner = (f'<rect x="-17" y="-2" width="34" height="14" rx="7" fill="{color}" stroke="{edge}" stroke-width="1.5"/>'
             f'<rect x="-15" y="2" width="30" height="6" rx="3" fill="#fff6e8"/>'
             f'<rect x="-17" y="-12" width="34" height="14" rx="7" fill="{color}" stroke="{edge}" stroke-width="1.5"/>'
             f'<ellipse cx="-6" cy="-8" rx="6" ry="2" fill="#fff" opacity=".35"/>')
    return rot(cx, cy, a, inner)


def choc(cx, cy, a=0, s=22):
    inner = f'<rect x="{-s/2}" y="{-s/2}" width="{s}" height="{s}" rx="3" fill="#5a3322" stroke="#3b2015" stroke-width="1.5"/>'
    inner += f'<line x1="0" y1="{-s/2}" x2="0" y2="{s/2}" stroke="#3b2015" stroke-width="1.2"/><line x1="{-s/2}" y1="0" x2="{s/2}" y2="0" stroke="#3b2015" stroke-width="1.2"/>'
    inner += f'<rect x="{-s/2+2}" y="{-s/2+2}" width="6" height="4" rx="1" fill="#fff" opacity=".18"/>'
    return rot(cx, cy, a, inner)


def cookie(cx, cy, r=24, seed=0):
    rnd = random.Random(seed)
    o = [circle(cx, cy, r, "#d9a566", "#a97434", 2)]
    for _ in range(7):
        a, d = rnd.random() * 6.28, rnd.random() * (r - 8)
        o.append(ell(cx + d * math.cos(a), cy + d * math.sin(a), 3.6, 2.6, "#4b2a1d", a=rnd.randint(0, 180)))
    return "".join(o)


# ---------- scenes ----------
def fix_alpha(t):
    def rep(m):
        a = int(m.group(3), 16) / 255
        return f'{m.group(1)}="#{m.group(2)}" {m.group(1)}-opacity="{a:.2f}"'
    return re.sub(r'(fill|stroke)="#([0-9a-fA-F]{6})([0-9a-fA-F]{2})"', rep, t)


def scaled(items, k, cx=400, cy=300):
    return f'<g transform="translate({cx} {cy}) scale({k}) translate({-cx} {-cy})">' + "".join(items) + "</g>"


def svg(body, bg, defs=""):
    body = fix_alpha(body)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img">'
            f'<defs><filter id="sh" x="-10%" y="-10%" width="120%" height="125%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#14304a" flood-opacity=".28"/></filter>{defs}</defs>'
            f'<rect width="{W}" height="{H}" fill="{bg}"/>{body}</svg>')


def grain(path_fn, n, color, seed):
    rnd = random.Random(seed)
    return "".join(path_fn(rnd) for _ in range(n))


def round_board():
    cx, cy, R = 400, 300, 262
    b = [f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#b27a47" filter="url(#sh)"/>',
         circle(cx, cy, R - 10, "#c38a52"),
         circle(cx, cy, R - 10, "none", "#a06a3a", 2)]
    rnd = random.Random(3)
    for _ in range(14):
        y = cy + rnd.uniform(-R + 40, R - 40)
        hw = math.sqrt(max(R * R - (y - cy) ** 2, 0)) - 24
        b.append(f'<path d="M{cx-hw:.0f} {y:.0f} q{hw*.5:.0f} {rnd.uniform(-8,8):.0f} {hw*2:.0f} 0" stroke="#a9733f" stroke-width="1.6" fill="none" opacity=".5"/>')
    f = []
    f.append(brie(300, 290, 66))
    f.append(rosemary(262, 262, -25, 60))
    f.append(flower(300, 286, 8, "#f6d6e2", "#f2b84b"))
    for i, (x, y, a) in enumerate([(380, 150, 10), (430, 160, 25), (478, 180, 40), (520, 212, 55), (552, 252, 70), (570, 300, 85)]):
        f.append(salami_fold(x, y, 27, a, i))
    f.append(grapes(500, 330, "#6b3f7a", r=11))
    f.append(grapes(250, 420, "#9bbf5e", "#fff", r=10))
    for k, (x, y, a) in enumerate([(380, 440, -20), (420, 462, -5), (462, 458, 12), (500, 440, 30)]):
        f.append(cracker(x, y, 38, a, round_=k % 2 == 0))
    f.append(bowl(560, 410, 30, "#e0a82e", spoon=True))
    f.append(bowl(210, 300, 24, "#8e2b4a"))
    for x, y, a in [(335, 395, 20), (352, 410, -10), (318, 412, 40)]:
        f.append(fig(x, y, 18, a))
    for x, y, a in [(250, 190, 10), (270, 205, 50), (232, 210, 90), (292, 190, -20)]:
        f.append(olive(x, y, a))
    for x, y, a in [(430, 260, 10), (445, 275, 80), (420, 280, 140), (460, 255, 30), (438, 295, 5), (410, 258, 60)]:
        f.append(almond(x, y, a))
    for x, y in [(330, 190), (350, 225), (455, 385)]:
        f.append(blueberry(x, y))
    f.append(raspberry(472, 380, 9))
    f.append(raspberry(488, 395, 9))
    f.append(flower(220, 380, 8))
    f.append(flower(600, 350, 7, "#f6d6e2"))
    f.append(flower(340, 480, 8, "#b88ad8"))
    for x, y in [(385, 215), (410, 232), (380, 242), (405, 205), (430, 215)]:
        f.append(cube(x, y, 19, x % 30 - 15))
    f.append(apricot(520, 470, 20))
    f.append(apricot(540, 485, -10))
    f.append(apricot(498, 488, 40))
    f.append(strawberry(440, 345, 16, 30))
    f.append(strawberry(412, 360, 16, -20))
    f.append(rosemary(470, 170, 30, 50))
    return svg("".join(b) + scaled(f, 1.14), "#cfe5df")


def long_board():
    x0, y0, bw, bh = 40, 80, 720, 450
    b = [f'<rect x="{x0}" y="{y0}" width="{bw}" height="{bh}" rx="26" fill="#9d6a3b" filter="url(#sh)"/>',
         f'<rect x="{x0+10}" y="{y0+10}" width="{bw-20}" height="{bh-20}" rx="20" fill="#b9814b"/>',
         f'<rect x="{x0+bw-4}" y="{y0+bh/2-28}" width="40" height="56" rx="14" fill="#9d6a3b"/>',
         f'<circle cx="{x0+bw+18}" cy="{y0+bh/2}" r="7" fill="#cfe5df"/>']
    rnd = random.Random(8)
    for _ in range(12):
        y = y0 + 30 + rnd.uniform(0, bh - 60)
        b.append(f'<path d="M{x0+26} {y:.0f} q{bw/4:.0f} {rnd.uniform(-8,8):.0f} {bw/2-26:.0f} 0 t{bw/2-52:.0f} 0" stroke="#a06a3a" stroke-width="1.6" fill="none" opacity=".5"/>')
    f = []
    f.append(brie(170, 220, 70))
    f.append(rosemary(120, 160, -20, 70))
    f.append(flower(170, 214, 8, "#f6d6e2"))
    f.append(wedge(160, 360, 46, -8))
    f.append(wedge(250, 400, 40, 10, "#f4a455", "#cf7d2a"))
    for x, y in [(270, 330), (292, 345), (255, 352), (278, 365)]:
        f.append(cube(x, y, 20, (x * 3) % 40 - 20))
    # salami river
    for i in range(9):
        t = i / 8
        f.append(salami_fold(290 + t * 250, 130 + math.sin(t * 4) * 20 + t * 70, 30, 20 + t * 40 + math.sin(t * 4) * 20, i))
    f.append(prosciutto(360, 300, 520, 270))
    f.append(prosciutto(380, 335, 540, 310, 20))
    f.append(grapes(600, 175, "#6b3f7a", r=12))
    f.append(grapes(660, 255, "#9bbf5e", r=11))
    for k in range(6):
        f.append(cracker(340 + k * 52, 460, 40, -6 + k * 3, round_=k % 2 == 1))
    for k in range(4):
        f.append(cracker(580 + k * 28, 400 + k * 10, 38, 25 + k * 6, round_=False))
    f.append(bowl(500, 400, 32, "#8e2b4a", spoon=True))
    f.append(bowl(440, 350, 22, "#c9a227"))
    for x, y, a in [(600, 330, 30), (620, 345, -20), (585, 350, 60)]:
        f.append(fig(x, y, 19, a))
    for x, y in [(650, 360), (668, 345), (640, 380)]:
        f.append(apricot(x, y, 20))
    for x, y, a in [(690, 430, 10), (708, 440, 70), (676, 445, -30), (700, 410, 130), (672, 418, 40)]:
        f.append(almond(x, y, a))
    for x, y, a in [(105, 300, 10), (125, 312, 60), (92, 318, 100)]:
        f.append(olive(x, y, a, "#3b2f3a", False))
    for x, y in [(100, 440), (116, 456), (86, 456), (132, 440)]:
        f.append(blueberry(x, y))
    for x, y in [(520, 215), (538, 232)]:
        f.append(raspberry(x, y))
    f.append(strawberry(225, 150, 16, 20))
    f.append(strawberry(245, 130, 16, -20))
    f.append(rosemary(560, 480, -10, 60))
    f.append(flower(560, 235, 8))
    f.append(flower(310, 250, 8, "#b88ad8"))
    f.append(flower(690, 330, 7, "#f6d6e2"))
    return svg("".join(b) + "".join(f), "#e5eef1")


def dock_board():
    planks = []
    for i in range(8):
        y = i * 78
        planks.append(f'<rect x="0" y="{y}" width="{W}" height="78" fill="{["#b88a57","#c0935f"][i%2]}"/>'
                      f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="#7d5b33" stroke-width="3"/>')
    rnd = random.Random(21)
    for _ in range(26):
        y = rnd.uniform(5, H - 5)
        x = rnd.uniform(-50, W - 150)
        planks.append(f'<path d="M{x:.0f} {y:.0f} q80 {rnd.uniform(-5,5):.0f} {rnd.uniform(120,260):.0f} 0" stroke="#a37845" stroke-width="1.5" fill="none" opacity=".5"/>')
    x0, y0, bw, bh = 70, 130, 660, 340
    b = [f'<rect x="{x0}" y="{y0}" width="{bw}" height="{bh}" rx="24" fill="#f2f5f4" filter="url(#sh)"/>',
         f'<rect x="{x0+12}" y="{y0+12}" width="{bw-24}" height="{bh-24}" rx="16" fill="#e4ecea" stroke="#c6d3d0" stroke-width="2"/>']
    f = []
    f.append(citrus(160, 200, 26))
    f.append(citrus(205, 235, 22, "#e3a223", "#f8d77b", "#e8b84a", 10))
    for k in range(5):
        f.append(cucumber(150 + k * 30, 330 + (k % 2) * 14, 16))
    for x, y in [(135, 400), (160, 410), (185, 398)]:
        f.append(tomato(x, y, 13))
    f.append(pepper(260, 190, 15))
    f.append(pepper(280, 215, 10, "#f2c230", "#c2951a"))
    f.append(pepper(255, 240, 20, "#d6392f", "#a52a22"))
    f.append(bowl(330, 320, 38, "#d9c28a", spoon=False))
    f.append(f'<g fill="#7d8a3a"><circle cx="318" cy="310" r="2"/></g>' + circle(330, 320, 10, "#4f8a43", op=.8))
    for k, (x, y, a) in enumerate([(300, 400, -15), (335, 408, 0), (370, 400, 15)]):
        f.append(pretzel(x, y, a))
    for k in range(5):
        f.append(cube(400 + (k % 3) * 24, 190 + (k // 3) * 24, 20, k * 12))
    for i in range(6):
        t = i / 5
        f.append(salami_fold(430 + t * 140, 275 + math.sin(t * 4) * 10, 26, 30 + t * 30, i))
    f.append(grapes(560, 190, "#9bbf5e", r=11))
    f.append(grapes(645, 250, "#6b3f7a", r=11))
    for k in range(5):
        f.append(cracker(470 + k * 44, 390, 36, -8 + k * 5, round_=k % 2 == 0))
    for x, y in [(610, 330), (630, 346), (594, 348)]:
        f.append(apricot(x, y, 15))
    for x, y, a in [(670, 400, 20), (688, 412, 80), (655, 412, -20)]:
        f.append(olive(x, y, a))
    f.append(citrus(375, 255, 18))
    f.append(mint(180, 270, -20))
    f.append(flower(520, 330, 7, "#f6d6e2"))
    for x, y in [(455, 330), (480, 346), (440, 352)]:
        f.append(cucumber(x, y, 14))
    f.append(wedge(230, 330, 0.01, 0, holes=False) if False else "")
    f.append(cube(560, 300, 20, 10)); f.append(cube(585, 292, 20, -8))
    f.append(tomato(235, 395, 12)); f.append(tomato(262, 405, 12))
    f.append(pepper(200, 300, -10, "#f2c230", "#c2951a"))
    f.append(citrus(120, 270, 18, "#e3a223", "#f8d77b", "#e8b84a", 10))
    f.append(olive(280, 280, 30)); f.append(olive(300, 262, -20))
    f.append(blueberry(390, 330, 8)); f.append(blueberry(405, 345, 8)); f.append(blueberry(378, 348, 8))
    return svg("".join(planks) + "".join(b) + scaled(f, 1.08, 400, 300), "#b88a57")


def sweet_board():
    x0, y0, bw, bh = 60, 70, 680, 460
    b = [f'<rect x="{x0}" y="{y0}" width="{bw}" height="{bh}" rx="34" fill="#e9eef0" stroke="#cdd6d9" stroke-width="3" filter="url(#sh)"/>']
    rnd = random.Random(5)
    for _ in range(8):
        sx, sy = rnd.uniform(x0 + 40, x0 + bw - 200), rnd.uniform(y0 + 40, y0 + bh - 40)
        b.append(f'<path d="M{sx:.0f} {sy:.0f} q{rnd.uniform(20,60):.0f} {rnd.uniform(-30,30):.0f} {rnd.uniform(90,200):.0f} {rnd.uniform(-40,40):.0f}" stroke="#aebcc2" stroke-width="1.5" fill="none" opacity=".6"/>')
    f = []
    cols = [("#f4a6b9", "#d6788f"), ("#9fd8c9", "#6bb3a2"), ("#f7d77a", "#d4ae3a"), ("#c3a6e6", "#9a7ac4"), ("#f4a6b9", "#d6788f")]
    for k, (c, e) in enumerate(cols):
        f.append(macaron(150 + k * 44, 150 + math.sin(k) * 10, c, e, -8 + k * 5))
    for k, (c, e) in enumerate(cols[::-1]):
        f.append(macaron(190 + k * 44, 200 + math.sin(k + 2) * 10, c, e, 10 - k * 6))
    f.append(bowl(200, 360, 48, "#4b2a1d"))
    for x, y, a in [(160, 340, 0), (190, 345, 6)]:
        pass
    for k in range(4):
        f.append(strawberry(150 + k * 26, 450 - (k % 2) * 10, 17, 160 + k * 8, dipped=True))
    f.append(cookie(360, 170, 30, 1))
    f.append(cookie(420, 220, 27, 2))
    for i in range(6):
        f.append(choc(350 + (i % 3) * 28, 320 + (i // 3) * 28, (i * 7) % 20 - 10))
    f.append(choc(440, 440, 15, 24))
    f.append(choc(470, 420, -10, 24))
    f.append(pretzel(380, 440, 20))
    f.append(pretzel(410, 460, -10))
    for k in range(5):
        f.append(strawberry(530 + k * 28, 160 + (k % 2) * 18, 19, 20 + k * 10))
    for x, y in [(520, 260), (540, 276), (508, 280), (560, 262), (530, 295), (562, 290)]:
        f.append(blueberry(x, y, 9))
    for x, y in [(620, 250), (640, 268), (606, 272)]:
        f.append(raspberry(x, y, 10))
    f.append(bowl(640, 380, 40, "#d63a55"))
    f.append(circle(640, 380, 12, "#f6efd8"))
    f.append(mint(560, 340, 20))
    f.append(mint(300, 90, -10))
    f.append(mint(620, 450, 200))
    f.append(flower(300, 260, 8, "#f6d6e2"))
    f.append(flower(480, 360, 8, "#b88ad8"))
    f.append(flower(250, 470, 8, "#f6d6e2"))
    f.append(flower(680, 150, 8, "#b88ad8"))
    for k, (c, e) in enumerate(cols):
        f.append(macaron(230 + k * 44, 255 + math.sin(k + 4) * 8, c, e, -4 + k * 4))
    f.append(cookie(300, 400, 28, 3))
    f.append(cookie(520, 470, 26, 4))
    for x, y in [(600, 470), (625, 485), (580, 490)]:
        f.append(raspberry(x, y, 10))
    for x, y in [(330, 470), (350, 485), (312, 488)]:
        f.append(blueberry(x, y, 9))
    f.append(strawberry(450, 300, 19, 40)); f.append(strawberry(480, 330, 19, -25))
    f.append(choc(560, 215, 20, 22)); f.append(choc(585, 225, -5, 22))
    return svg("".join(b) + scaled(f, 1.06), "#bfe0e0")


if __name__ == "__main__":
    out = {
        "board-round-table": (round_board(), "A round graze board with a cut wheel of brie, a salami fold, grapes, figs, crackers, olives, almonds and honey."),
        "board-gathering": (long_board(), "A large rectangular charcuterie board with brie, cheddar, folded salami, prosciutto, grapes, figs, crackers, jam and almonds."),
        "board-dockside": (dock_board(), "A compact boat board on a teak deck with cucumber, tomatoes, peppers, pretzels, cheese cubes, salami, grapes and lime."),
        "board-sweet-tide": (sweet_board(), "A dessert graze board with macarons, dipped strawberries, cookies, chocolate, berries and mint."),
    }
    for name, (s, desc) in out.items():
        s = s.replace('role="img">', f'role="img" aria-label="{desc}">', 1)
        open(f"images/{name}.svg", "w").write(s)
    print("done")
