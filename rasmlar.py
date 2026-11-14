# -*- coding: utf-8 -*-
"""4-sinf matematikasidan rasmli savollar. Rasmlar shu yerda chiziladi."""
from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

INK = (23, 62, 54)
ACCENT = (36, 109, 87)
SOFT = (213, 235, 139)
PAPER = (255, 255, 255)
MUTED = (90, 110, 102)
LINE = (200, 214, 206)

rng = random.Random(20261115)


def font(size: int):
    for path in (r"C:\Windows\Fonts\segoeui.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


F = font(22)
FS = font(18)
FL = font(28)


def canvas(w, h):
    im = Image.new("RGB", (w, h), PAPER)
    return im, ImageDraw.Draw(im)


def label(draw, xy, text, fill=INK, fnt=FS, anchor="mm"):
    draw.text(xy, text, font=fnt, fill=fill, anchor=anchor)


def gcd(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def frac(n, d):
    g = gcd(n, d)
    n, d = n // g, d // g
    if d == 1:
        return str(n)
    if n > d:
        w, n = divmod(n, d)
        if n == 0:
            return str(w)
        return f"{w} {n}/{d}"
    return f"{n}/{d}"


def clear_questions():
    qdir = Path(__file__).resolve().parent / "sayt" / "questions"
    qdir.mkdir(parents=True, exist_ok=True)
    for path in qdir.glob("*.png"):
        path.unlink()


def draw_rect(a, b):
    max_side = 280
    scale = max_side / max(a, b)
    w, h = max(78, int(a * scale)), max(64, int(b * scale))
    im, d = canvas(w + 120, h + 110)
    x0, y0 = 46, 36
    d.rectangle([x0, y0, x0 + w, y0 + h], outline=INK, width=4)
    d.line([(x0, y0 + h + 16), (x0 + w, y0 + h + 16)], fill=ACCENT, width=2)
    label(d, (x0 + w / 2, y0 + h + 34), f"{a} cm")
    d.line([(x0 + w + 16, y0), (x0 + w + 16, y0 + h)], fill=ACCENT, width=2)
    label(d, (x0 + w + 48, y0 + h / 2), f"{b} cm")
    return im


def draw_square(side):
    s = 220
    im, d = canvas(s + 130, s + 100)
    x0, y0 = 40, 30
    d.rectangle([x0, y0, x0 + s, y0 + s], outline=INK, width=4)
    label(d, (x0 + s / 2, y0 + s + 28), f"{side} cm")
    return im


def draw_clock(hour, minute):
    im, d = canvas(320, 320)
    cx, cy, r = 160, 160, 118
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=4)
    for i in range(12):
        ang = math.radians(i * 30 - 90)
        inner, outer = r - 16, r - 6
        d.line(
            [(cx + inner * math.cos(ang), cy + inner * math.sin(ang)), (cx + outer * math.cos(ang), cy + outer * math.sin(ang))],
            fill=INK,
            width=3,
        )
        tr = r - 34
        label(d, (cx + tr * math.cos(ang), cy + tr * math.sin(ang)), str(12 if i == 0 else i), fnt=FS)
    def hand(length, deg, width, color):
        ang = math.radians(deg - 90)
        d.line([(cx, cy), (cx + length * math.cos(ang), cy + length * math.sin(ang))], fill=color, width=width)
    hand(62, (hour % 12) * 30 + minute * 0.5, 8, INK)
    hand(100, minute * 6, 4, ACCENT)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=ACCENT)
    return im


def draw_bars(names, vals):
    im, d = canvas(560, 340)
    left, bottom, top = 64, 280, 40
    width = 460
    maxv = max(vals)
    step = 5 if maxv <= 30 else 10
    topv = ((maxv + step - 1) // step) * step
    d.line([(left, top), (left, bottom), (left + width, bottom)], fill=INK, width=3)
    for tick in range(0, topv + 1, step):
        y = bottom - (tick / topv) * (bottom - top)
        d.line([(left - 6, y), (left, y)], fill=INK, width=2)
        d.line([(left, y), (left + width, y)], fill=LINE, width=1)
        label(d, (left - 12, y), str(tick), anchor="rm", fnt=FS)
    slot = width / len(vals)
    for i, (name, val) in enumerate(zip(names, vals)):
        bh = (val / topv) * (bottom - top)
        x = left + i * slot + 18
        d.rectangle([x, bottom - bh, x + slot - 36, bottom], fill=SOFT, outline=ACCENT, width=2)
        label(d, ((x + x + slot - 36) / 2, bottom + 22), name, fnt=FS)
    return im


def draw_venn(only_a, only_b, both):
    im, d = canvas(520, 300)
    d.ellipse([40, 50, 300, 250], outline=INK, width=4)
    d.ellipse([210, 50, 470, 250], outline=ACCENT, width=4)
    label(d, (110, 78), "A", fnt=FL)
    label(d, (400, 78), "B", fnt=FL)
    label(d, (130, 155), str(only_a), fnt=FL)
    label(d, (255, 155), str(both), fnt=FL)
    label(d, (370, 155), str(only_b), fnt=FL)
    return im


def draw_ray(point, end=12):
    im, d = canvas(560, 160)
    y, x0, x1 = 78, 40, 520
    d.line([(x0, y), (x1, y)], fill=INK, width=3)
    d.polygon([(x1, y), (x1 - 14, y - 7), (x1 - 14, y + 7)], fill=INK)
    for i in range(end + 1):
        x = x0 + i * ((x1 - 40 - x0) / end)
        d.line([(x, y - 8), (x, y + 8)], fill=INK, width=2)
        label(d, (x, y + 28), str(i), fnt=FS)
    x = x0 + point * ((x1 - 40 - x0) / end)
    d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=ACCENT)
    return im


def draw_pair(a, b):
    im, d = canvas(560, 150)
    y = 70
    x0 = 36
    span = 480
    d.line([(x0, y), (x0 + span, y)], fill=INK, width=3)
    for value, color in ((min(a, b), INK), (max(a, b), ACCENT)):
        x = x0 + value / 16 * span
        d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=color)
        label(d, (x, y - 28), str(value), fill=color, fnt=F)
    label(d, (28, y + 36), "0", fnt=FS)
    return im


def draw_lines(kind):
    im, d = canvas(420, 240)
    if kind == "parallel":
        d.line([(40, 70), (380, 70)], fill=INK, width=4)
        d.line([(40, 160), (380, 160)], fill=ACCENT, width=4)
    else:
        d.line([(40, 120), (380, 120)], fill=INK, width=4)
        d.line([(200, 30), (200, 210)], fill=ACCENT, width=4)
    return im


def draw_cut(A, B, a, b):
    scale = 260 / max(A, B)
    def P(x, y):
        return (50 + x * scale, 40 + y * scale)
    im, d = canvas(int(A * scale) + 140, int(B * scale) + 120)
    outer = [P(0, 0), P(A, 0), P(A, B), P(0, B)]
    d.polygon(outer, outline=INK, width=4)
    cut = [P(A - a, 0), P(A, 0), P(A, b), P(A - a, b)]
    d.polygon(cut, fill=SOFT, outline=ACCENT)
    label(d, ((P(0, B)[0] + P(A, B)[0]) / 2, P(0, B)[1] + 26), f"{A} cm")
    label(d, (P(0, 0)[0] - 28, (P(0, 0)[1] + P(0, B)[1]) / 2), f"{B} cm")
    label(d, ((P(A - a, 0)[0] + P(A, 0)[0]) / 2, P(A, 0)[1] + b * scale / 2), f"{a}×{b}", fill=ACCENT)
    return im


def draw_two(a, b, c, d2):
    im, dr = canvas(520, 260)
    def box(x, y, w, h, text):
        dr.rectangle([x, y, x + w, y + h], outline=INK, width=4)
        label(dr, (x + w / 2, y + h / 2), text, fnt=F)
    box(40, 50, 180, 120, f"{a} × {b} cm")
    box(280, 70, 180, 100, f"{c} × {d2} cm")
    return im


def draw_fraction_bar(k, n):
    im, d = canvas(80 + n * 56, 150)
    x, y, w, h = 30, 40, 52, 64
    for i in range(n):
        d.rectangle([x + i * w, y, x + (i + 1) * w, y + h], fill=SOFT if i < k else PAPER, outline=INK, width=3)
    return im


def draw_pie(k, n):
    im, d = canvas(280, 280)
    cx, cy, r = 140, 140, 108
    for i in range(n):
        a0 = -math.pi / 2 + i * 2 * math.pi / n
        a1 = -math.pi / 2 + (i + 1) * 2 * math.pi / n
        pts = [(cx, cy)]
        steps = 12
        for s in range(steps + 1):
            ang = a0 + (a1 - a0) * s / steps
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
        d.polygon(pts, fill=SOFT if i < k else PAPER, outline=INK)
    for i in range(n):
        ang = -math.pi / 2 + i * 2 * math.pi / n
        d.line([(cx, cy), (cx + r * math.cos(ang), cy + r * math.sin(ang))], fill=INK, width=3)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=3)
    return im


def draw_angle(deg):
    im, d = canvas(440, 280)
    vx, vy, length = 70, 210, 250
    d.line([(vx, vy), (vx + length, vy)], fill=INK, width=4)
    rad = math.radians(-deg)
    d.line([(vx, vy), (vx + length * math.cos(rad), vy + length * math.sin(rad))], fill=INK, width=4)
    r = 48
    d.arc([vx - r, vy - r, vx + r, vy + r], start=-deg, end=0, fill=ACCENT, width=4)
    if deg == 90:
        s = 24
        d.line([(vx + s, vy), (vx + s, vy - s), (vx, vy - s)], fill=ACCENT, width=3)
    return im


def draw_adjacent(deg):
    im, d = canvas(520, 250)
    y, ox = 160, 210
    d.line([(24, y), (496, y)], fill=INK, width=4)
    rad = math.radians(-deg)
    d.line([(ox, y), (ox + 150 * math.cos(rad), y + 150 * math.sin(rad))], fill=ACCENT, width=4)
    mid = math.radians(-deg / 2)
    label(d, (ox + 78 * math.cos(mid), y + 78 * math.sin(mid)), f"{deg}°", fill=ACCENT, fnt=F)
    other = 180 - deg
    mid2 = math.radians(-(deg + other / 2))
    label(d, (ox + 78 * math.cos(mid2), y + 78 * math.sin(mid2)), "?", fnt=FL)
    return im


def draw_circle(radius):
    im, d = canvas(360, 280)
    cx, cy, r = 150, 140, 100
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=4)
    d.line([(cx, cy), (cx + r, cy)], fill=ACCENT, width=4)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=ACCENT)
    label(d, (cx + r / 2, cy - 18), f"{radius} cm", fill=ACCENT)
    return im


def draw_shape(kind):
    im, d = canvas(320, 240)
    if kind == "kvadrat":
        d.rectangle([80, 40, 240, 200], outline=INK, width=4)
    elif kind == "to‘g‘ri to‘rtburchak":
        d.rectangle([40, 70, 280, 180], outline=INK, width=4)
    elif kind == "aylana":
        d.ellipse([60, 30, 260, 210], outline=INK, width=4)
    elif kind == "uchburchak":
        d.polygon([(160, 30), (40, 200), (280, 200)], outline=INK, width=4)
    return im


def draw_solid(kind):
    im, d = canvas(320, 240)
    if kind == "kub":
        d.polygon([(70, 90), (150, 50), (250, 90), (170, 130)], outline=INK)
        d.polygon([(70, 90), (170, 130), (170, 210), (70, 170)], outline=INK)
        d.polygon([(170, 130), (250, 90), (250, 170), (170, 210)], outline=ACCENT)
    elif kind == "silindr":
        d.ellipse([90, 36, 230, 86], outline=INK, width=3)
        d.line([(90, 61), (90, 170)], fill=INK, width=3)
        d.line([(230, 61), (230, 170)], fill=INK, width=3)
        d.arc([90, 145, 230, 195], start=0, end=180, fill=INK, width=3)
        d.arc([90, 145, 230, 195], start=180, end=360, fill=MUTED, width=2)
    elif kind == "konus":
        d.polygon([(160, 36), (70, 180), (250, 180)], outline=INK)
        d.arc([70, 160, 250, 210], start=0, end=180, fill=INK, width=3)
    elif kind == "shar":
        d.ellipse([60, 30, 260, 210], outline=INK, width=4)
        d.arc([60, 90, 260, 160], start=0, end=180, fill=ACCENT, width=2)
    elif kind == "piramida":
        d.polygon([(160, 30), (40, 180), (280, 180)], outline=INK)
        d.line([(160, 30), (160, 200)], fill=ACCENT, width=3)
        d.line([(40, 180), (280, 180)], fill=INK, width=3)
    else:
        d.polygon([(40, 80), (140, 40), (260, 80), (160, 120)], outline=INK)
        d.polygon([(40, 80), (40, 180), (160, 220), (160, 120)], outline=INK)
        d.polygon([(160, 120), (160, 220), (260, 180), (260, 80)], outline=ACCENT)
    return im


def take(section, prompt, correct, wrongs, picture, uniq):
    return section, prompt, correct, wrongs, picture, uniq


def iter_pictures():
    clear_questions()
    out = []

    def push(section, prompt, correct, wrongs, picture, uniq):
        out.append(take(section, prompt, correct, wrongs, picture, uniq))

    for _ in range(32):
        a, b = rng.randint(4, 18), rng.randint(3, 14)
        if a == b:
            b += 1
        area, peri = a * b, 2 * (a + b)
        if rng.random() < 0.55:
            push(6, "Rasmda to‘g‘ri to‘rtburchakning yuzi necha kvadrat santimetr?", area, [peri, a + b, area + a, abs(a - b) * max(a, b)], draw_rect(a, b), f"rect-s-{a}-{b}")
        else:
            push(6, "Rasmda to‘g‘ri to‘rtburchakning perimetri necha santimetr?", peri, [area, a + b, peri + 2, a * b + 2], draw_rect(a, b), f"rect-p-{a}-{b}")
    for side in rng.sample(list(range(3, 21)), 12):
        push(6, "Rasmda kvadratning yuzi necha kvadrat santimetr?", side * side, [side * 4, side * 2, side, side * side + side], draw_square(side), f"sq-{side}")
    times = []
    while len(times) < 24:
        item = (rng.randint(1, 12), rng.choice([0, 15, 20, 30, 40, 45]))
        if item not in times:
            times.append(item)
    for hour, minute in times:
        shown = f"{hour}:{minute:02d}"
        wrongs = [f"{hour}:{(minute + 15) % 60:02d}", f"{12 if hour == 1 else hour - 1}:{minute:02d}", f"{1 if hour == 12 else hour + 1}:{minute:02d}", f"{hour}:{(minute + 30) % 60:02d}"]
        push(6, "Soat nechani ko‘rsatmoqda?", shown, wrongs, draw_clock(hour, minute), f"clock-{hour}-{minute}")

    fruits = ["olma", "nok", "uzum", "anor", "shaftoli", "o‘rik"]
    for i in range(28):
        names = rng.sample(fruits, 4)
        vals = [rng.randint(4, 24) for _ in names]
        if vals.count(max(vals)) != 1:
            vals[0] = max(vals) + 3
        picture = draw_bars(names, vals)
        kind = i % 3
        if kind == 0:
            correct = names[vals.index(max(vals))]
            push(9, "Ustunli diagrammada qaysi meva eng ko‘p?", correct, [n for n in names if n != correct], picture, f"bar-max-{i}-{vals}")
        elif kind == 1:
            push(9, "Diagrammadagi mevalar jami nechta?", sum(vals), [sum(vals) + 2, sum(vals) - 1, max(vals), sum(vals) + max(vals)], picture, f"bar-sum-{i}-{vals}")
        else:
            order = sorted(range(4), key=lambda k: vals[k], reverse=True)
            diff = vals[order[0]] - vals[order[1]]
            push(9, f"Diagrammada {names[order[0]]} {names[order[1]]} dan nechta ko‘p?", diff, [diff + 1, diff + 2, vals[order[0]], max(1, diff - 1)], picture, f"bar-diff-{i}-{vals}")

    for i in range(18):
        only_a, only_b, both = rng.randint(3, 14), rng.randint(2, 12), rng.randint(1, 8)
        picture = draw_venn(only_a, only_b, both)
        if i % 2 == 0:
            push(9, "Venn diagrammasida A to‘plamda jami nechta element?", only_a + both, [only_a, only_b + both, only_a + only_b + both, both], picture, f"venn-a-{only_a}-{only_b}-{both}")
        else:
            push(9, "Venn diagrammasida ikkala to‘plamda jami nechta element?", only_a + only_b + both, [only_a + both, only_b + both, only_a + only_b, both], picture, f"venn-u-{only_a}-{only_b}-{both}")

    for point in range(1, 13):
        push(10, "Nuqtaning koordinatasi qaysi son?", point, [point + 1, max(0, point - 1), 0, point + 2], draw_ray(point), f"ray-{point}")
    for _ in range(16):
        a, b = rng.sample(range(1, 16), 2)
        dist = abs(a - b)
        push(10, "Ikki nuqta orasidagi masofa nechta birlik?", dist, [a + b, dist + 1, max(a, b), min(a, b)], draw_pair(a, b), f"pair-{a}-{b}")
    push(10, "Rasmda to‘g‘ri chiziqlar qanday joylashgan?", "parallel", ["perpendikulyar", "kesishuvchi va perpendikulyar emas", "ustma-ust"], draw_lines("parallel"), "lines-par")
    push(10, "Rasmda to‘g‘ri chiziqlar qanday joylashgan?", "perpendikulyar", ["parallel", "ustma-ust", "aylana bo‘ylab"], draw_lines("perp"), "lines-perp")

    for _ in range(22):
        A, B = rng.randint(8, 16), rng.randint(6, 12)
        a, b = rng.randint(2, A - 2), rng.randint(2, B - 2)
        correct = A * B - a * b
        push(16, "Bo‘yalgan to‘g‘ri to‘rtburchak olib tashlangan. Qolgan yuz necha kvadrat santimetr?", correct, [A * B, a * b, A * B + a * b, correct + a], draw_cut(A, B, a, b), f"cut-{A}-{B}-{a}-{b}")
    for _ in range(18):
        a, b = rng.randint(3, 12), rng.randint(3, 9)
        c, d2 = rng.randint(3, 12), rng.randint(3, 9)
        correct = a * b + c * d2
        push(26, "Ikki to‘g‘ri to‘rtburchakning umumiy yuzi necha kvadrat santimetr?", correct, [a * b, c * d2, 2 * (a + b + c + d2), correct + a], draw_two(a, b, c, d2), f"two-{a}-{b}-{c}-{d2}")

    for _ in range(24):
        n = rng.choice([2, 3, 4, 5, 6, 8])
        k = rng.randint(1, n - 1)
        correct = f"{k}/{n}"
        wrongs = [f"{n - k}/{n}", f"{k}/{n + 1}", f"{min(n - 1, k + 1)}/{n}", f"1/{n}"]
        push(18, "Bo‘yalgan qism qanday kasr?", correct, wrongs, draw_fraction_bar(k, n), f"barf-{k}-{n}")
    for _ in range(16):
        n = rng.choice([2, 3, 4, 5, 6, 8])
        k = rng.randint(1, n - 1)
        correct = f"{k}/{n}"
        push(18, "Doira bo‘yalgan qismi qanday kasr?", correct, [f"{n - k}/{n}", f"{k}/{n + 1}", f"1/{n}", str(k)], draw_pie(k, n), f"pie-{k}-{n}")

    for deg in [15, 20, 30, 40, 45, 50, 60, 70, 80, 90, 100, 110, 120, 135, 150, 160]:
        if deg < 90:
            kind = "o‘tkir burchak"
        elif deg == 90:
            kind = "to‘g‘ri burchak"
        else:
            kind = "o‘tmas burchak"
        wrongs = [w for w in ("o‘tkir burchak", "to‘g‘ri burchak", "o‘tmas burchak", "yoyiq burchak") if w != kind]
        push(29, "Rasmda ko‘rsatilgan burchak qanday?", kind, wrongs, draw_angle(deg), f"ang-{deg}")
    for deg in [20, 30, 40, 45, 50, 60, 70, 110, 120, 130, 140, 150]:
        if deg >= 180:
            continue
        other = 180 - deg
        push(29, "To‘g‘ri chiziqdagi noma’lum burchak necha gradus?", other, [deg, 90, 90 - deg if deg < 90 else deg - 90, other + 10], draw_adjacent(deg), f"adj-{deg}")

    for radius in [3, 4, 5, 6, 7, 8, 9, 10, 12]:
        push(28, "Aylananing diametri necha santimetr?", radius * 2, [radius, radius * 3, radius + 2, radius * 4], draw_circle(radius), f"circ-{radius}")

    shapes = [
        ("kvadrat", "kvadrat", ["uchburchak", "aylana", "to‘g‘ri to‘rtburchak"]),
        ("to‘g‘ri to‘rtburchak", "to‘g‘ri to‘rtburchak", ["kvadrat", "uchburchak", "aylana"]),
        ("aylana", "aylana", ["kvadrat", "uchburchak", "to‘g‘ri to‘rtburchak"]),
        ("uchburchak", "uchburchak", ["kvadrat", "aylana", "to‘g‘ri to‘rtburchak"]),
    ]
    for key, name, wrongs in shapes:
        push(25, "Rasmda qanday shakl chizilgan?", name, wrongs, draw_shape(key), f"shape-{key}")
    solids = [
        ("kub", "kub", ["shar", "silindr", "konus"]),
        ("silindr", "silindr", ["kub", "konus", "shar"]),
        ("konus", "konus", ["silindr", "piramida", "shar"]),
        ("shar", "shar", ["aylana", "silindr", "kub"]),
        ("piramida", "piramida", ["prizma", "konus", "kub"]),
        ("prizma", "uchburchakli prizma", ["piramida", "kub", "silindr"]),
    ]
    for key, name, wrongs in solids:
        push(27, "Rasmda qanday jism tasvirlangan?", name, wrongs, draw_solid(key), f"solid-{key}")
        faces = {"kub": "6", "silindr": "2", "konus": "1", "shar": "0", "piramida": "4", "prizma": "5"}[key]
        face_wrongs = [x for x in ("6", "5", "4", "3", "2", "1", "0", "8") if x != faces][:3]
        push(27, "Rasmda tasvirlangan jismning nechta tekis yoqi bor?", faces, face_wrongs, draw_solid(key), f"faces-{key}")
    return out
