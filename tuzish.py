# -*- coding: utf-8 -*-
"""4-sinf matematika test bazasini tuzish.

Savollar I. V. Repyova, «Matematika. 4-sinf», I–IV qism
(«Novda Edutainment», 2023) mavzulariga moslab tuziladi.
Darslikdagi mashqlar ko‘chirilmaydi: har bir javob shu yerda hisoblanadi.
"""
from __future__ import annotations

import json
import random
import re
from fractions import Fraction
from pathlib import Path

rng = random.Random(20261114)
root = Path(__file__).resolve().parent
out_path = root / "sayt" / "bank.json"

META = {
    1: ("I", "1-dars", 5),
    2: ("I", "2–3-dars", 8),
    3: ("I", "4-dars", 14),
    4: ("I", "5–7-dars", 17),
    5: ("I", "8-dars", 26),
    6: ("I", "9–11-dars", 29),
    7: ("I", "12–18-dars", 38),
    8: ("I", "21–24-dars", 68),
    9: ("I", "30–36-dars", 94),
    10: ("I", "27–29-dars", 85),
    11: ("II", "41–44-dars", 8),
    12: ("II", "46-dars", 23),
    13: ("II", "48–55-dars", 29),
    14: ("II", "56–63-dars", 55),
    15: ("II", "64–66-dars", 79),
    16: ("II", "67–68-dars", 88),
    17: ("III", "72–73-dars", 5),
    18: ("III", "74–78-dars", 11),
    19: ("III", "79–83-dars", 26),
    20: ("III", "84–85-dars", 41),
    21: ("III", "88–98-dars", 55),
    22: ("III", "99-dars", 88),
    23: ("III", "101–104-dars", 96),
    24: ("III", "105–108-dars", 108),
    25: ("IV", "109–111-dars", 5),
    26: ("IV", "113–114-dars", 17),
    27: ("IV", "115–120-dars", 23),
    28: ("IV", "121–125-dars", 41),
    29: ("IV", "127–133-dars", 61),
}

bank: list[dict] = []
seen: set[str] = set()


def gcd(a: int, b: int) -> int:
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    return a // gcd(a, b) * b


def fmt(n: int) -> str:
    n = int(n)
    sign = "-" if n < 0 else ""
    s = str(abs(n))
    parts = []
    while s:
        parts.append(s[-3:])
        s = s[:-3]
    return sign + " ".join(reversed(parts))


def dec(scaled: int, places: int) -> str:
    sign = "-" if scaled < 0 else ""
    scaled = abs(int(scaled))
    whole, frac = divmod(scaled, 10**places)
    return sign + fmt(whole) + "," + str(frac).zfill(places)


def frac(n: int, d: int) -> str:
    if d < 0:
        n, d = -n, -d
    g = gcd(n, d)
    n, d = n // g, d // g
    if d == 1:
        return str(n)
    if n >= d:
        w, n = divmod(n, d)
        if n == 0:
            return str(w)
        return f"{w} {n}/{d}"
    return f"{n}/{d}"


def show(v) -> str:
    if isinstance(v, int) and not isinstance(v, bool):
        return fmt(v)
    return str(v)


def neigh(n: int) -> list[int]:
    out = []
    for d in (1, -1, 2, -2, 10, -10, 5, -5, 100, -100, 20, -20, 3, -3):
        v = n + d
        if v >= 0 and v != n:
            out.append(v)
    if n > 1:
        out.append(n * 2)
    if n > 20:
        out.append(n + n // 10)
        out.append(max(0, n - n // 10))
    return out


def numeric(text: str):
    raw = str(text).strip()
    compact = raw.replace(" ", "")
    if re.fullmatch(r"-?\d+", compact):
        return Fraction(int(compact))
    m = re.fullmatch(r"(-?\d+),(\d+)", compact)
    if m:
        whole = int(m.group(1))
        part = m.group(2)
        sign = -1 if compact.startswith("-") else 1
        return sign * (abs(whole) + Fraction(int(part), 10 ** len(part)))
    m = re.fullmatch(r"(\d+) (\d+)/(\d+)", raw)
    if m:
        return int(m.group(1)) + Fraction(int(m.group(2)), int(m.group(3)))
    m = re.fullmatch(r"(\d+)/(\d+)", compact)
    if m and int(m.group(2)):
        return Fraction(int(m.group(1)), int(m.group(2)))
    return None


def add(section: int, prompt: str, correct, wrongs, picture=None, uniq=None) -> bool:
    prompt = " ".join(prompt.split())
    key = uniq or prompt
    if not prompt or key in seen:
        return False
    correct_s = show(correct)
    options = []
    used = {correct_s}
    used_n = []
    correct_n = numeric(correct_s)
    if correct_n is not None:
        used_n.append(correct_n)
    for w in wrongs:
        s = show(w)
        if not s or s in used or s.startswith("["):
            continue
        n = numeric(s)
        if n is not None and any(n == old for old in used_n):
            continue
        used.add(s)
        if n is not None:
            used_n.append(n)
        options.append(s)
        if len(options) == 3:
            break
    if len(options) < 3:
        return False
    options.append(correct_s)
    rng.shuffle(options)
    letters = ["A", "B", "C", "D"]
    part, lesson, page = META[section]
    n = 1 + sum(1 for q in bank if q["section"] == section)
    row = {
        "id": f"{section}-{n}",
        "section": section,
        "number": n,
        "page": page,
        "part": part,
        "lesson": lesson,
        "answer": letters[options.index(correct_s)],
        "options": letters,
        "prompt": prompt,
        "choices": options,
    }
    if picture is not None:
        qdir = root / "sayt" / "questions"
        qdir.mkdir(parents=True, exist_ok=True)
        rel = f"questions/{section}-{n}.png"
        picture.save(qdir / f"{section}-{n}.png", "PNG", optimize=True)
        row["image"] = rel
        row["width"] = picture.width
        row["height"] = picture.height
    bank.append(row)
    seen.add(key)
    return True


def put_fixed(section: int, rows: list[tuple]) -> None:
    for prompt, correct, wrongs in rows:
        if not add(section, prompt, correct, wrongs):
            print("  o‘tkazildi:", prompt[:70])


def fill(section: int, target: int, builder) -> None:
    before = sum(1 for q in bank if q["section"] == section)
    guard = 0
    while sum(1 for q in bank if q["section"] == section) < before + target and guard < target * 120:
        guard += 1
        item = builder()
        if not item:
            continue
        add(section, *item)
    got = sum(1 for q in bank if q["section"] == section) - before
    print(f"bo‘lim {section}: {got}")


def round_down(n: int, place: int) -> int:
    return n // place * place


def round_up(n: int, place: int) -> int:
    down = round_down(n, place)
    return n if n == down else down + place


def round_nearest(n: int, place: int) -> int:
    down = round_down(n, place)
    if (n % place) * 2 >= place:
        return down + place
    return down


def clock(h: int, m: int) -> str:
    return f"{h}:{m:02d}"


def span_text(mins: int) -> str:
    h, m = divmod(mins, 60)
    if h and m:
        return f"{h} soat {m} daqiqa"
    if h:
        return f"{h} soat"
    return f"{m} daqiqa"


# --- 1. Ko‘p xonali sonlar ---
def b1():
    kind = rng.randrange(5)
    if kind == 0:
        n = rng.randint(10_000, 9_999_999)
        place, name = rng.choice([(10, "o‘nlik"), (100, "yuzlik"), (1000, "minglik"), (10_000, "o‘n minglik")])
        correct = n // place
        return (
            f"{fmt(n)} sonida nechta to‘liq {name} bor?",
            correct,
            [correct + 1, max(0, correct - 1), n // (place * 10) if place < n else correct + 10, n % place],
        )
    if kind == 1:
        n = rng.randint(100_000, 9_999_999)
        shifts = [
            (10, "o‘nlar"),
            (100, "yuzlar"),
            (1000, "minglar"),
            (10_000, "o‘n minglar"),
            (100_000, "yuz minglar"),
        ]
        place, name = rng.choice(shifts)
        digit = (n // place) % 10
        wrongs = [(digit + d) % 10 for d in (1, 2, 3, 4, 5)]
        return (f"{fmt(n)} sonida {name} xonasidagi raqam qaysi?", digit, wrongs)
    if kind == 2:
        mln = rng.randint(1, 25)
        ming = rng.randint(0, 999)
        bir = rng.randint(0, 999)
        correct = mln * 1_000_000 + ming * 1000 + bir
        return (
            f"{mln} million {fmt(ming)} ming {fmt(bir)} ni raqam bilan yozing.",
            correct,
            [correct + 1000, max(0, correct - 1000), mln * 1000 + ming, correct + 1_000_000],
        )
    if kind == 3:
        a = rng.randint(1000, 900_000)
        b = a + rng.choice([1, 2, 10, 100, 1000, 25])
        if rng.random() < 0.5:
            a, b = b, a
        sign = ">" if a > b else "<"
        return (
            f"{fmt(a)} va {fmt(b)} sonlarini taqqoslang. To‘g‘ri belgi qaysi?",
            sign,
            [s for s in (">", "<", "=", "≥") if s != sign],
        )
    n = rng.randint(1000, 99_999)
    return (
        f"{fmt(n)} dan keyin keladigan son qaysi?",
        n + 1,
        [n - 1, n + 10, n + 2, n],
    )


# --- 2. Amallar ---
def b2():
    kind = rng.randrange(4)
    if kind == 0:
        a, b = rng.randint(150, 80_000), rng.randint(80, 50_000)
        correct = a + b
        return (f"Hisoblang: {fmt(a)} + {fmt(b)}", correct, neigh(correct) + [abs(a - b)])
    if kind == 1:
        a, b = rng.randint(500, 90_000), rng.randint(100, 40_000)
        if a < b:
            a, b = b, a
        correct = a - b
        return (f"Hisoblang: {fmt(a)} − {fmt(b)}", correct, neigh(correct) + [a + b])
    if kind == 2:
        a, b = rng.randint(12, 240), rng.randint(3, 25)
        correct = a * b
        return (f"Hisoblang: {fmt(a)} · {fmt(b)}", correct, neigh(correct) + [a + b, a * (b + 1)])
    d = rng.choice([2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 20, 25])
    q = rng.randint(8, 400)
    a = d * q
    return (f"Hisoblang: {fmt(a)} : {d}", q, neigh(q) + [a, q + d])


# --- 3. Amallar tartibi ---
def b3():
    kind = rng.randrange(4)
    if kind == 0:
        a, b, c = rng.randint(10, 80), rng.randint(3, 20), rng.randint(3, 15)
        correct = a + b * c
        return (
            f"Ifodaning qiymatini toping: {a} + {b} · {c}",
            correct,
            [(a + b) * c, a + b + c, a * b + c, correct + b],
        )
    if kind == 1:
        a, b, c = rng.randint(4, 30), rng.randint(4, 25), rng.randint(2, 12)
        correct = (a + b) * c
        return (
            f"Ifodaning qiymatini toping: ({a} + {b}) · {c}",
            correct,
            [a + b * c, a + b + c, a * c + b, correct + c],
        )
    if kind == 2:
        c = rng.choice([2, 3, 4, 5, 6, 8, 10])
        b = c * rng.randint(3, 20)
        a = b // c + rng.randint(5, 40)
        correct = a - b // c
        return (
            f"Ifodaning qiymatini toping: {a} − {b} : {c}",
            correct,
            [correct + 1, b // c, a, correct + c, a + c],
        )
    a, b = rng.randint(2, 12), rng.randint(2, 12)
    c, d = rng.randint(2, 12), rng.randint(2, 12)
    correct = a * b + c * d
    return (
        f"Ifodaning qiymatini toping: {a} · {b} + {c} · {d}",
        correct,
        [(a + c) * (b + d), a * b * c * d, a + b + c + d, a * (b + c) * d],
    )


# --- 4. Harakat, formula, ish unumdorligi ---
WORK = [(6, 3, 2), (4, 12, 3), (6, 6, 3), (4, 4, 2), (12, 6, 4), (12, 4, 3), (20, 5, 4), (15, 10, 6), (8, 24, 6), (9, 18, 6), (10, 10, 5), (8, 8, 4), (12, 12, 6), (2, 2, 1), (3, 6, 2)]


def b4():
    kind = rng.randrange(4)
    if kind == 0:
        v, t = rng.choice([40, 45, 50, 60, 72, 80, 90]), rng.randint(2, 8)
        correct = v * t
        return (
            f"Avtomobil {v} km/soat tezlik bilan {t} soat yurdi. U qancha yo‘l bosdi?",
            f"{fmt(correct)} km",
            [f"{fmt(v + t)} km", f"{fmt(correct + v)} km", f"{fmt(v * (t + 1))} km", f"{fmt(abs(correct - v))} km"],
        )
    if kind == 1:
        v = rng.choice([4, 5, 6, 8, 10, 12, 15])
        t = rng.randint(2, 9)
        s = v * t
        return (
            f"Velosipedchi {fmt(s)} km yo‘lni {t} soatda bosib o‘tdi. Tezligi qancha?",
            f"{v} km/soat",
            [f"{s} km/soat", f"{t} km/soat", f"{v + t} km/soat", f"{v * t} km/soat"],
        )
    if kind == 2:
        rate, hours = rng.randint(6, 24), rng.randint(2, 8)
        correct = rate * hours
        return (
            f"Usta 1 soatda {rate} ta detal yasaydi. {hours} soatda nechta detal yasaydi?",
            correct,
            neigh(correct) + [rate + hours],
        )
    a, b, t = rng.choice(WORK)
    return (
        f"Birinchi ishchi ishni {a} soatda, ikkinchisi {b} soatda bajaradi. Birga ishlasalar, ish necha soatda bitadi?",
        t,
        [a + b, abs(a - b) or 1, a, b],
    )


# --- 5. Tenglamalar va tengsizliklar ---
def b5():
    kind = rng.randrange(5)
    if kind == 0:
        x, a = rng.randint(20, 2000), rng.randint(15, 1500)
        b = x + a
        return (f"Tenglamani yeching: x + {fmt(a)} = {fmt(b)}", x, [b + a, b, a, x + 10, abs(a - x)])
    if kind == 1:
        x, a = rng.randint(40, 2500), rng.randint(10, 800)
        b = x - a if x > a else None
        if b is None or b == 0:
            return None
        return (f"Tenglamani yeching: x − {fmt(a)} = {fmt(b)}", x, [b, a, abs(b - a), x + a, b + 10])
    if kind == 2:
        a, x = rng.randint(30, 900), rng.randint(8, 400)
        if a <= x:
            return None
        b = a - x
        return (f"Tenglamani yeching: {fmt(a)} − x = {fmt(b)}", x, [a + b, a, b, x + a, abs(a - b)])
    if kind == 3:
        a, x = rng.choice([2, 3, 4, 5, 6, 8, 10, 12]), rng.randint(6, 80)
        p = a * x
        return (f"Tenglamani yeching: {a} · x = {fmt(p)}", x, [p, a, p + a, x + a, abs(p - a)])
    bound = rng.randint(30, 200)
    good = bound - rng.randint(1, 8)
    bad = [bound, bound + 1, bound + rng.randint(2, 15), bound + 10]
    return (f"x < {bound} tengsizlikni qanoatlantiruvchi sonni tanlang.", good, bad)


# --- 6. Vaqt, yuza, perimetr ---
def b6():
    kind = rng.randrange(5)
    if kind == 0:
        h, m = rng.randint(1, 8), rng.choice([0, 5, 10, 15, 20, 25, 30, 40, 45])
        total = h * 60 + m
        return (
            f"{h} soat {m} daqiqa necha daqiqa?",
            total,
            [h + m, h * 100 + m, total + 10, h * 60, abs(total - 15)],
        )
    if kind == 1:
        h = rng.randint(7, 15)
        m = rng.choice([0, 10, 15, 20, 25, 30, 40, 45])
        dur = rng.choice([15, 20, 25, 30, 35, 40, 45, 50, 90])
        end = h * 60 + m + dur
        eh, em = divmod(end, 60)
        if eh > 20:
            return None
        correct = clock(eh, em)
        wrongs = [clock(h, m), clock(eh, (em + 10) % 60), span_text(dur), clock(min(20, eh + 1), em)]
        return (f"Dars soat {clock(h, m)} da boshlandi va {dur} daqiqa davom etdi. Soat nechada tugaydi?", correct, wrongs)
    if kind == 2:
        a, b = rng.randint(3, 30), rng.randint(2, 20)
        area, peri = a * b, 2 * (a + b)
        if rng.random() < 0.5:
            return (
                f"To‘g‘ri to‘rtburchakning bo‘yi {a} cm, eni {b} cm. Yuzi necha kvadrat santimetr?",
                area,
                [peri, a + b, area + a, abs(a - b) * max(a, b)],
            )
        return (
            f"To‘g‘ri to‘rtburchakning bo‘yi {a} cm, eni {b} cm. Perimetri necha santimetr?",
            peri,
            [area, a + b, 2 * a * b, peri + 2],
        )
    if kind == 3:
        side = rng.randint(3, 25)
        if rng.random() < 0.5:
            return (f"Tomoni {side} cm bo‘lgan kvadratning yuzi necha kvadrat santimetr?", side * side, [side * 4, side * 2, side + 4, side * side + side])
        return (f"Tomoni {side} cm bo‘lgan kvadratning perimetri necha santimetr?", side * 4, [side * side, side * 2, side, side * 4 + 4])
    peri = rng.choice([12, 16, 20, 24, 28, 32, 36, 40])
    side = peri // 4
    return (
        f"Kvadratning perimetri {peri} cm. Yuzi necha kvadrat santimetr?",
        side * side,
        [peri, side, peri * 4, side * 4],
    )


# --- 7. Bo‘linish alomatlari ---
def b7():
    kind = rng.randrange(3)
    div = rng.choice([2, 3, 4, 5, 9, 10])
    if kind == 0:
        good = div * rng.randint(12, 4000)
        bads = []
        while len(bads) < 6:
            n = rng.randint(100, 40_000)
            if n % div != 0:
                bads.append(n)
        return (f"Qaysi son {div} ga qoldiqsiz bo‘linadi?", good, bads)
    if kind == 1:
        bads = [div * rng.randint(12, 2000) for _ in range(5)]
        good = rng.randint(100, 40_000)
        while good % div == 0:
            good += 1
        return (f"Qaysi son {div} ga qoldiqsiz bo‘linmaydi?", good, bads)
    a, b = rng.randint(2, 12), rng.randint(2, 12)
    correct = lcm(a, b)
    return (
        f"{a} ga ham, {b} ga ham qoldiqsiz bo‘linadigan eng kichik musbat son qaysi?",
        correct,
        [a * b, a + b, max(a, b), gcd(a, b), correct * 2],
    )


# --- 8. To‘plam, o‘rta arifmetik, chastota ---
def b8():
    kind = rng.randrange(4)
    if kind == 0:
        a = rng.randint(8, 30)
        b = rng.randint(6, 24)
        inter = rng.randint(1, min(a, b) - 1)
        correct = a + b - inter
        return (
            f"A to‘plamda {a} ta, B to‘plamda {b} ta element bor. Umumiy elementlar {inter} ta. Birlashmada nechta element bor?",
            correct,
            [a + b, a + b + inter, abs(a - b), inter],
        )
    if kind == 1:
        nums = [rng.randint(4, 30) for _ in range(4)]
        if sum(nums) % 4:
            nums[0] += 4 - sum(nums) % 4
        correct = sum(nums) // 4
        text = ", ".join(str(x) for x in nums)
        return (f"{text} sonlarining o‘rta arifmetigini toping.", correct, neigh(correct) + [sum(nums), max(nums)])
    if kind == 2:
        value = rng.randint(2, 9)
        others = [rng.choice([n for n in range(1, 10) if n != value]) for _ in range(5)]
        count = rng.randint(2, 4)
        seq = others[:]
        for _ in range(count):
            seq.insert(rng.randrange(len(seq) + 1), value)
        text = ", ".join(str(x) for x in seq)
        return (f"{text} qatorida {value} necha marta uchraydi?", count, [count + 1, max(1, count - 1), len(seq), 1])
    only_a, only_b, both = rng.randint(3, 15), rng.randint(2, 12), rng.randint(1, 8)
    return (
        f"Venn diagrammasida faqat A da {only_a} ta, faqat B da {only_b} ta, umumiy qismda {both} ta element bor. A to‘plamda jami nechta element?",
        only_a + both,
        [only_a, only_a + only_b, only_a + only_b + both, both],
    )


# --- 9. Diagramma va grafik ---
def b9():
    names = rng.sample(["olma", "nok", "uzum", "shaftoli", "anor", "o‘rik"], 4)
    vals = [rng.randint(4, 30) for _ in names]
    kind = rng.randrange(3)
    data = ", ".join(f"{n} — {v}" for n, v in zip(names, vals))
    if vals.count(max(vals)) != 1:
        return None
    if kind == 0:
        i = vals.index(max(vals))
        return (f"Ustunli diagramma: {data}. Qaysi meva eng ko‘p?", names[i], [names[j] for j in range(4) if j != i])
    if kind == 1:
        return (f"Diagramma: {data}. Jami nechta meva?", sum(vals), neigh(sum(vals)) + [max(vals)])
    i, j = 0, 1
    if vals[j] > vals[i]:
        i, j = j, i
    diff = vals[i] - vals[j]
    if diff == 0:
        return None
    return (
        f"Diagramma: {data}. {names[i]} {names[j]} dan nechta ko‘p?",
        diff,
        neigh(diff) + [vals[i] + vals[j]],
    )


# --- 10. Koordinata va parallel chiziqlar ---
def b10():
    kind = rng.randrange(3)
    if kind == 0:
        a, b = rng.sample(range(0, 21), 2)
        correct = abs(a - b)
        return (
            f"Koordinata nurida A nuqtaning koordinatasi {a}, B niki {b}. AB kesmaning uzunligi qancha?",
            correct,
            neigh(correct) + [a + b],
        )
    if kind == 1:
        start = rng.randint(2, 16)
        step = rng.randint(1, 8)
        if rng.random() < 0.5:
            return (
                f"Nuqta koordinatasi {start}. U o‘ngga {step} birlik siljidi. Yangi koordinata qaysi?",
                start + step,
                [start - step if start >= step else start + 1, start, step, start + step + 1],
            )
        if start <= step:
            return None
        return (
            f"Nuqta koordinatasi {start}. U chapga {step} birlik siljidi. Yangi koordinata qaysi?",
            start - step,
            [start + step, start, step, abs(start - step - 1)],
        )
    a, b = rng.sample(range(1, 12), 2)
    return (
        f"Koordinata burchagida nuqta ({a}; {b}). Uning abssissasi qaysi son?",
        a,
        [b, a + b, abs(a - b), 0],
    )


# --- 11. Masshtab va masofa ---
def b11():
    kind = rng.randrange(2)
    if kind == 0:
        k = rng.choice([4, 5, 6, 8, 10, 12, 15, 20])
        cm = rng.randint(2, 12)
        correct = k * cm
        return (
            f"Xaritada 1 cm ga {k} km to‘g‘ri keladi. {cm} cm haqiqatda necha kilometr?",
            correct,
            [k + cm, k, cm, correct + k],
        )
    point = rng.randint(2, 18)
    return (
        f"Sonli nurda K nuqta 0 dan {point} birlik narida. K nuqtaning koordinatasi qaysi?",
        point,
        [point + 1, max(0, point - 1), 0, point * 2],
    )


# --- 12. Yo‘l, vaqt, tezlik ---
def b12():
    v = rng.choice([36, 40, 45, 48, 50, 54, 60, 72, 80, 90])
    t = rng.choice([2, 3, 4, 5, 6])
    s = v * t
    kind = rng.randrange(3)
    if kind == 0:
        return (f"Tezlik {v} km/soat, vaqt {t} soat. Bosib o‘tilgan yo‘l qancha?", f"{fmt(s)} km", [f"{v + t} km", f"{fmt(v)} km", f"{t} km", f"{fmt(s + v)} km"])
    if kind == 1:
        return (f"Yo‘l {fmt(s)} km, vaqt {t} soat. Tezlik qancha?", f"{v} km/soat", [f"{s} km/soat", f"{t} km/soat", f"{v + t} km/soat", f"{fmt(s * t)} km/soat"])
    return (f"Yo‘l {fmt(s)} km, tezlik {v} km/soat. Vaqt necha soat?", t, [s, v, t + 1, v // t if v > t else t + 2])


# --- 13. Qarama-qarshi va quvlama harakat ---
def b13():
    if rng.random() < 0.5:
        v1, v2 = rng.choice([(40, 60), (50, 70), (45, 55), (30, 50), (36, 54), (48, 72)])
        t = rng.randint(2, 5)
        s = (v1 + v2) * t
        return (
            f"Ikki shahar orasi {s} km. Avtobuslar bir vaqtda qarama-qarshi yo‘lga chiqdi. Tezliklari {v1} va {v2} km/soat. Necha soatdan keyin uchrashadilar?",
            t,
            [v1 + v2, s, t + 1, abs(v1 - v2) or 1],
        )
    v1, v2 = rng.choice([(80, 60), (70, 50), (90, 60), (60, 40), (54, 36)])
    t = rng.randint(2, 5)
    gap = (v1 - v2) * t
    return (
        f"Ikki avtomobil bir yo‘nalishda ketyapti. Oldingisi {v2} km/soat, keyingisi {v1} km/soat. Oradagi masofa {gap} km. Keyingisi oldingisiga necha soatda yetadi?",
        t,
        [v1 + v2, gap, t + 1, v1 - v2],
    )


# --- 14. Yaxlitlash ---
PLACES = [(10, "o‘nlikkacha"), (100, "yuzlikkacha"), (1000, "minglikkacha")]


def b14():
    place, name = rng.choice(PLACES)
    n = rng.randint(place + place // 5, place * 80)
    if n % place == 0:
        n += rng.randint(1, place - 1)
    kind = rng.randrange(3)
    if kind == 0:
        correct = round_nearest(n, place)
        return (f"{fmt(n)} sonini {name} yaxlitlang.", correct, [round_down(n, place), round_up(n, place), correct + place, n])
    if kind == 1:
        return (f"{fmt(n)} sonini {name} ortig‘i bilan yaxlitlang.", round_up(n, place), [round_down(n, place), round_nearest(n, place), n, round_up(n, place) + place])
    return (f"{fmt(n)} sonini {name} kami bilan yaxlitlang.", round_down(n, place), [round_up(n, place), round_nearest(n, place), n, max(0, round_down(n, place) - place)])


# --- 15. Chamalash va qulay hisoblash ---
def b15():
    kind = rng.randrange(3)
    if kind == 0:
        a = rng.randint(120, 880)
        b = rng.randint(120, 880)
        est = round_nearest(a, 100) + round_nearest(b, 100)
        return (
            f"{fmt(a)} + {fmt(b)} yig‘indisini yuzlikkacha yaxlitlab chamalang.",
            est,
            [a + b, round_down(a, 100) + round_down(b, 100), est + 100, abs(est - 100)],
        )
    if kind == 1:
        a = rng.choice([25, 50, 125])
        b = rng.choice([4, 8, 12, 16])
        if a == 125 and b not in (4, 8):
            b = 8
        correct = a * b
        return (f"Qulay usul bilan hisoblang: {a} · {b}", correct, [a + b, a * (b // 2), correct + a, correct // 2 or 1])
    a = rng.randint(11, 89)
    b = 100 - a
    c = rng.randint(5, 40)
    correct = a + b + c
    return (f"Qulay usul bilan hisoblang: {a} + {c} + {b}", correct, [a + b, c, correct + 10, a * b])


# --- 16. Yuzni hisoblash ---
def b16():
    A, B = rng.randint(6, 18), rng.randint(5, 12)
    a, b = rng.randint(2, A - 1), rng.randint(2, B - 1)
    whole, cut = A * B, a * b
    correct = whole - cut
    return (
        f"Bo‘yi {A} cm va eni {B} cm bo‘lgan to‘g‘ri to‘rtburchakdan burchagidagi {a} cm × {b} cm to‘g‘ri to‘rtburchak olib tashlandi. Qolgan qismning yuzi necha kvadrat santimetr?",
        correct,
        [whole, cut, whole + cut, abs(A * b - a * B), correct + a],
    )


# --- 17. Bo‘lish ---
def b17():
    d = rng.choice([2, 3, 4, 5, 6, 7, 8, 9, 12, 15])
    q = rng.randint(12, 250)
    a = d * q
    if rng.random() < 0.5:
        return (f"Bo‘ling: {fmt(a)} : {d}", q, neigh(q) + [a, d])
    return (
        f"Kutubxonada {fmt(a)} ta kitob {d} ta javonga teng taqsimlandi. Har bir javonda nechtadan kitob?",
        q,
        neigh(q) + [a, a + d],
    )


# --- 18. Ulush va qism ---
def b18():
    den = rng.choice([2, 3, 4, 5, 6, 8, 10])
    num = rng.randint(1, den - 1)
    while gcd(num, den) != 1:
        num = rng.randint(1, den - 1)
    whole = den * rng.randint(3, 24)
    correct = whole // den * num
    kind = rng.randrange(2)
    if kind == 0:
        return (
            f"{fmt(whole)} ning {num}/{den} qismini toping.",
            correct,
            [whole // den, whole, correct + den, abs(whole - correct)],
        )
    left = whole - correct
    return (
        f"Lentaning uzunligi {whole} cm. Uning {num}/{den} qismi ishlatildi. Necha santimetr qoldi?",
        left,
        [correct, whole, whole // den, left + num],
    )


# --- 19. Kasr turlari ---
def b19():
    kind = rng.randrange(3)
    if kind == 0:
        w, d = rng.randint(1, 8), rng.randint(2, 9)
        n = rng.randint(1, d - 1)
        if gcd(n, d) != 1:
            return None
        imp_n = w * d + n
        return (
            f"{w} {n}/{d} aralash kasrini noto‘g‘ri kasrga aylantiring.",
            f"{imp_n}/{d}",
            [f"{w + n}/{d}", f"{w * n}/{d}", f"{imp_n}/{w}", frac(imp_n, d + 1)],
        )
    if kind == 1:
        d = rng.randint(2, 9)
        n = d * rng.randint(1, 6) + rng.randint(1, d - 1)
        return (
            f"{n}/{d} noto‘g‘ri kasridan butun qismni ajrating.",
            frac(n, d),
            [f"{n}/{d}", frac(n, d + 1), str(n // d), frac(n + 1, d)],
        )
    n, d = rng.randint(1, 8), rng.randint(2, 9)
    if n < d:
        correct, wrongs = "to‘g‘ri kasr", ["noto‘g‘ri kasr", "aralash kasr", "butun son"]
        label = f"{n}/{d}"
    else:
        correct, wrongs = "noto‘g‘ri kasr", ["to‘g‘ri kasr", "aralash kasr", "o‘nli kasr"]
        label = f"{n + d}/{d}"
    return (f"{label} qanday kasr?", correct, wrongs)


# --- 20. Kasrlarni taqqoslash ---
def b20():
    if rng.random() < 0.5:
        d = rng.randint(3, 12)
        a, b = rng.sample(range(1, d), 2)
        bigger = f"{max(a, b)}/{d}"
        smaller = f"{min(a, b)}/{d}"
        return (
            f"Qaysi kasr katta: {a}/{d} yoki {b}/{d}?",
            bigger,
            [smaller, "teng", f"{a + b}/{d}", f"1/{d}"],
        )
    n = rng.randint(1, 5)
    d1, d2 = rng.sample(range(n + 1, 12), 2)
    bigger = f"{n}/{min(d1, d2)}"
    smaller = f"{n}/{max(d1, d2)}"
    return (
        f"Qaysi kasr katta: {n}/{d1} yoki {n}/{d2}?",
        bigger,
        [smaller, "teng", f"{n}/{d1 + d2}", f"{d1}/{n}" if n else "0"],
    )


# --- 21. Kasrlarni qo‘shish va ayirish ---
def b21():
    kind = rng.randrange(3)
    d = rng.randint(4, 12)
    if kind == 0:
        a, b = rng.randint(1, d - 2), rng.randint(1, d - 2)
        if a + b > d:
            b = max(1, d - a)
        correct = frac(a + b, d)
        return (f"Hisoblang: {a}/{d} + {b}/{d}", correct, [frac(abs(a - b), d), f"{a + b}/{d * 2}", frac(a + b, d + 1), f"{a}/{d}"])
    if kind == 1:
        a = rng.randint(2, d - 1)
        b = rng.randint(1, a - 1)
        return (f"Hisoblang: {a}/{d} − {b}/{d}", frac(a - b, d), [frac(a + b, d), f"{a - b}/{d * 2}", f"{b}/{d}", frac(a - b, d - 1 if d > 2 else d)])
    a = rng.randint(1, d - 1)
    return (f"Hisoblang: 1 − {a}/{d}", frac(d - a, d), [f"{a}/{d}", frac(a, d), "1", frac(d - a, d + 1)])


# --- 22. Kasrni natural songa ko‘paytirish ---
def b22():
    d = rng.randint(2, 9)
    n = rng.randint(1, d - 1)
    if gcd(n, d) != 1:
        return None
    k = rng.randint(2, 8)
    return (
        f"Hisoblang: {n}/{d} · {k}",
        frac(n * k, d),
        [f"{n * k}/{d * k}", f"{n}/{d * k}", frac(n + k, d), f"{k}/{d}"],
    )


# --- 23. O‘nli kasrlar ---
def b23():
    kind = rng.randrange(4)
    if kind == 0:
        n = rng.randint(1, 9)
        return (f"{n}/10 kasrini o‘nli kasr ko‘rinishida yozing.", dec(n, 1), [dec(n, 2), f"{n}", f"{n},0", dec((10 - n) or 2, 1)])
    if kind == 1:
        n = rng.randint(1, 99)
        return (f"{n}/100 kasrini o‘nli kasr ko‘rinishida yozing.", dec(n, 2), [dec(n + 1, 2), f"{n}", dec(n, 3), dec(n, 1)])
    if kind == 2:
        a = rng.randint(10, 250)
        b = rng.randint(10, 200)
        return (f"Hisoblang: {dec(a, 2)} + {dec(b, 2)}", dec(a + b, 2), [dec(abs(a - b), 2), dec(a + b, 1), dec(a + b + 10, 2), dec(a, 2)])
    a = rng.randint(50, 400)
    b = rng.randint(10, a - 5)
    return (f"Hisoblang: {dec(a, 2)} − {dec(b, 2)}", dec(a - b, 2), [dec(a + b, 2), dec(abs(a - b) + 10, 2), dec(b, 2), dec(a - b, 1)])


# --- 24. Uzunlik, massa, foiz ---
def b24():
    kind = rng.randrange(4)
    if kind == 0:
        km, m = rng.randint(1, 8), rng.choice([0, 25, 40, 50, 125, 200, 250, 400, 750])
        correct = km * 1000 + m
        return (f"{km} km {m} m necha metr?", correct, [km + m, km * 100 + m, correct + 100, km * 1000])
    if kind == 1:
        kg, g = rng.randint(1, 9), rng.choice([0, 50, 100, 200, 250, 500, 750])
        correct = kg * 1000 + g
        return (f"{kg} kg {g} g necha gramm?", correct, [kg + g, kg * 100 + g, correct // 10, kg * 1000])
    if kind == 2:
        m, cm = rng.randint(1, 12), rng.choice([0, 5, 8, 15, 20, 25, 40, 50])
        correct = m * 100 + cm
        return (f"{m} m {cm} cm necha santimetr?", correct, [m + cm, m * 10 + cm, correct + 10, m * 100])
    percent = rng.choice([1, 5, 10, 20, 25, 50])
    step = 100 // gcd(percent, 100)
    whole = step * rng.randint(2, 40)
    correct = whole * percent // 100
    return (f"{fmt(whole)} ning {percent}% ini toping.", correct, [whole // 10, percent, correct + step, abs(whole - correct)])


# --- 26. Nostandart yuz, qo‘shimcha matnli ---
def b26():
    # Ikki to‘g‘ri to‘rtburchak yonma-yon.
    a, b = rng.randint(3, 10), rng.randint(3, 8)
    c, d = rng.randint(3, 10), rng.randint(3, 8)
    correct = a * b + c * d
    return (
        f"Shakl ikkita to‘g‘ri to‘rtburchakdan yig‘ilgan: {a} cm × {b} cm va {c} cm × {d} cm. Umumiy yuzi necha kvadrat santimetr?",
        correct,
        [a * b, c * d, 2 * (a + b + c + d), correct + a],
    )


def self_test() -> None:
    assert fmt(448924) == "448 924"
    assert fmt(1000) == "1 000"
    assert fmt(12) == "12"
    assert frac(2, 4) == "1/2"
    assert frac(7, 3) == "2 1/3"
    assert frac(6, 3) == "2"
    assert frac(5, 5) == "1"
    assert round_nearest(347, 10) == 350
    assert round_nearest(342, 10) == 340
    assert round_nearest(345, 10) == 350
    assert round_up(347, 10) == 350
    assert round_down(347, 10) == 340
    assert lcm(4, 6) == 12
    assert dec(345, 2) == "3,45"
    assert dec(5, 2) == "0,05"
    for a, b, t in WORK:
        assert a * b == t * (a + b)


def build() -> None:
    self_test()
    fill(1, 90, b1)
    fill(2, 90, b2)
    fill(3, 70, b3)
    fill(4, 55, b4)
    put_fixed(
        4,
        [
            ("Yo‘l, tezlik va vaqt o‘rtasidagi to‘g‘ri formula qaysi?", "s = v · t", ["s = v + t", "s = v : t", "v = s · t"]),
            ("Agar tezlik va vaqt ma’lum bo‘lsa, yo‘l qanday topiladi?", "tezlikni vaqtga ko‘paytirish bilan", ["tezlikni vaqtga bo‘lish bilan", "tezlik va vaqtni qo‘shish bilan", "vaqtdan tezlikni ayirish bilan"]),
        ],
    )
    fill(5, 70, b5)
    fill(6, 55, b6)
    put_fixed(
        6,
        [
            ("1 soat necha daqiqa?", 60, [100, 24, 30, 12]),
            ("1 minut necha soniya?", 60, [100, 30, 24, 10]),
            ("1 sutka necha soat?", 24, [12, 60, 30, 48]),
            ("Yuzi va perimetri haqida qaysi gap to‘g‘ri?", "Yuza kvadrat birlikda, perimetr uzunlik birligida o‘lchanadi", ["Ikkalasi ham faqat santimetrda o‘lchanadi", "Perimetr kvadrat birlikda o‘lchanadi", "Yuza faqat soatda o‘lchanadi"]),
        ],
    )
    fill(7, 70, b7)
    put_fixed(
        7,
        [
            ("Son 2 ga bo‘linishi uchun oxirgi raqami qanday bo‘lishi kerak?", "juft: 0, 2, 4, 6 yoki 8", ["faqat 0", "faqat 5", "toq raqam"]),
            ("Son 5 ga bo‘linishi uchun oxirgi raqami qanday bo‘lishi kerak?", "0 yoki 5", ["faqat juft", "faqat 1", "istalgan raqam"]),
            ("Son 10 ga bo‘linishi uchun oxirgi raqami qanday bo‘lishi kerak?", "0", ["5", "2", "1"]),
            ("Son 3 ga bo‘linishini tekshirish uchun nima qilinadi?", "raqamlari yig‘indisi 3 ga bo‘linishi kerak", ["oxirgi raqami 3 bo‘lishi kerak", "oxirgi ikki raqami qaraladi", "birinchi raqami 3 ga bo‘linadi"]),
            ("Son 9 ga bo‘linishini tekshirish uchun nima qilinadi?", "raqamlari yig‘indisi 9 ga bo‘linishi kerak", ["oxirgi raqami 9 bo‘lishi kerak", "oxirgi ikki raqami 9 ga bo‘linadi", "son juft bo‘lishi kerak"]),
            ("Son 4 ga bo‘linishini tekshirish uchun nima qilinadi?", "oxirgi ikki raqam tashkil etgan son 4 ga bo‘linadi", ["raqamlar yig‘indisi 4 ga bo‘linadi", "oxirgi raqam 4 bo‘ladi", "birinchi raqam juft bo‘ladi"]),
        ],
    )
    fill(8, 50, b8)
    fill(9, 45, b9)
    put_fixed(
        9,
        [
            ("Ustunli diagrammada kattaliklar odatda qanday ko‘rsatiladi?", "ustunlarning balandligi bilan", ["faqat aylana rangi bilan", "faqat nuqta koordinatasi bilan", "faqat kasr chizig‘i bilan"]),
            ("Chiziqli diagramma nimani ko‘rsatishga qulay?", "kattalikning o‘zgarishini", ["faqat bitta sonning raqamlarini", "faqat shaklning perimetrini", "faqat kasrning maxrajini"]),
            ("Venn diagrammasidagi umumiy qism nimani bildiradi?", "ikkala to‘plamga ham kiradigan elementlarni", ["faqat birinchi to‘plamning elementlarini", "hech qaysi to‘plamga kirmaydigan sonlarni", "diagrammaning nomini"]),
        ],
    )
    fill(10, 40, b10)
    put_fixed(
        10,
        [
            ("Bir tekislikda yotib, kesishmaydigan to‘g‘ri chiziqlar qanday ataladi?", "parallel to‘g‘ri chiziqlar", ["perpendikulyar to‘g‘ri chiziqlar", "kesma", "nur"]),
            ("To‘g‘ri burchak hosil qilib kesishgan to‘g‘ri chiziqlar qanday ataladi?", "perpendikulyar to‘g‘ri chiziqlar", ["parallel to‘g‘ri chiziqlar", "aylana", "nur"]),
            ("Koordinata nurining boshlang‘ich nuqtasi qaysi son?", 0, [1, 10, 2]),
        ],
    )
    fill(11, 40, b11)
    fill(12, 50, b12)
    put_fixed(
        12,
        [
            ("Tezlik qanday topiladi?", "yo‘lni vaqtga bo‘lib", ["yo‘lni vaqtga ko‘paytirib", "yo‘l bilan vaqtni qo‘shib", "vaqtdan yo‘lni ayirib"]),
            ("Vaqt qanday topiladi?", "yo‘lni tezlikka bo‘lib", ["tezlikni yo‘lga ko‘paytirib", "tezlik bilan yo‘lni qo‘shib", "tezlikdan yo‘lni ayirib"]),
        ],
    )
    fill(13, 40, b13)
    put_fixed(
        13,
        [
            ("Qarama-qarshi yo‘nalishda yaqinlashayotgan ikki jismning yaqinlashish tezligi qanday topiladi?", "tezliklar qo‘shiladi", ["tezliklar ayiriladi", "tezliklar ko‘paytiriladi", "tezliklarning o‘rta arifmetigi olinadi"]),
            ("Bir yo‘nalishda quvib yetish tezligi qanday topiladi?", "katta tezlikdan kichigini ayirish bilan", ["tezliklarni qo‘shish bilan", "tezliklarni ko‘paytirish bilan", "yo‘lni vaqtga qo‘shish bilan"]),
        ],
    )
    fill(14, 70, b14)
    put_fixed(
        14,
        [
            ("Yaxlitlashda 5, 6, 7, 8, 9 raqamlari qanday qaraladi?", "oldingi xona 1 ga oshiriladi", ["oldingi xona o‘zgarmaydi", "son 0 ga aylanadi", "keyingi xona o‘chirilmaydi"]),
            ("Yaxlitlashda 0, 1, 2, 3, 4 raqamlari qanday qaraladi?", "oldingi xona o‘zgarmaydi", ["oldingi xona 1 ga oshadi", "son ikki baravar bo‘ladi", "kasr butunga aylanadi"]),
            ("Ortig‘i bilan yaxlitlash degani nima?", "berilgan xonagacha bo‘lgan qoldiq tashlab, sonni shu xonada kattalashtirish", ["songa eng yaqin qiymatni olish", "faqat oxirgi raqamni 0 qilish", "sonni 10 ga bo‘lish"]),
        ],
    )
    fill(15, 40, b15)
    fill(16, 36, b16)
    put_fixed(
        16,
        [
            ("Murakkab shaklning yuzini topishning qulay yo‘li qaysi?", "uni tanish to‘g‘ri to‘rtburchaklarga ajratib, yuzlarni qo‘shish", ["barcha tomonlarni ko‘paytirish", "faqat eng uzun tomonni olish", "perimetrni ikkiga bo‘lish"]),
            ("To‘g‘ri to‘rtburchak ichidan kichik to‘g‘ri to‘rtburchak qirqib olinsa, qolgan yuz qanday topiladi?", "katta yuzdan kichik yuz ayiriladi", ["ikkala yuz qo‘shiladi", "tomonlar qo‘shiladi", "perimetrlar ko‘paytiriladi"]),
        ],
    )
    fill(17, 55, b17)
    put_fixed(
        17,
        [
            ("Bo‘linuvchi, bo‘luvchi va bo‘linma o‘rtasidagi bog‘lanish qaysi?", "bo‘linuvchi = bo‘luvchi · bo‘linma", ["bo‘linuvchi = bo‘luvchi + bo‘linma", "bo‘linma = bo‘linuvchi · bo‘luvchi", "bo‘luvchi = bo‘linuvchi · bo‘linma"]),
            ("Qoldiqli bo‘lishda qoldiq bo‘luvchidan qanday bo‘ladi?", "qoldiq bo‘luvchidan kichik bo‘ladi", ["qoldiq bo‘luvchidan katta bo‘ladi", "qoldiq doim 0 bo‘ladi", "qoldiq bo‘linmaga teng bo‘ladi"]),
        ],
    )
    fill(18, 50, b18)
    put_fixed(
        18,
        [
            ("Sonning 1/2 qismi nimani anglatadi?", "sonning yarmini", ["sonning ikki baravarini", "sonning choragini", "sonning o‘zidan 2 taga ortig‘ini"]),
            ("Sonning qismini topishda avval nima qilinadi?", "son shu qismning maxrajiga bo‘linadi", ["son suratga ko‘paytiriladi va shu yerda to‘xtaladi", "maxraj bilan surat qo‘shiladi", "son 100 ga bo‘linadi"]),
        ],
    )
    fill(19, 45, b19)
    put_fixed(
        19,
        [
            ("To‘g‘ri kasr qanday kasr?", "surati maxrajidan kichik bo‘lgan kasr", ["surati maxrajidan katta bo‘lgan kasr", "butun qismi ham, kasr qismi ham bor son", "maxraji 10 bo‘lgan kasr"]),
            ("Noto‘g‘ri kasr qanday kasr?", "surati maxrajidan katta yoki unga teng kasr", ["surati maxrajidan kichik kasr", "faqat o‘nli kasr", "maxraji 1 bo‘lgan kasr"]),
            ("Aralash kasr nimadan iborat?", "butun son va to‘g‘ri kasrdan", ["ikkita butun sondan", "faqat surat va maxrajdan, butunsiz", "faqat o‘nli verguldan"]),
        ],
    )
    # fix accidental nested list in put_fixed above - I'll check after run
    fill(20, 40, b20)
    put_fixed(
        20,
        [
            ("Maxraji bir xil kasrlardan qaysinisi katta?", "surati katta bo‘lgani", ["surati kichigi", "maxraji katta bo‘lgani", "ikkala kasr ham teng"]),
            ("Surati bir xil to‘g‘ri kasrlardan qaysinisi katta?", "maxraji kichigi", ["maxraji kattasi", "surati 1 ga teng bo‘lgani", "ikkala kasr ham teng"]),
        ],
    )
    fill(21, 50, b21)
    put_fixed(
        21,
        [
            ("Maxraji bir xil kasrlarni qo‘shganda maxraj nima bo‘ladi?", "o‘zgarmaydi", ["suratlar qo‘shilganidek qo‘shiladi", "0 bo‘lib qoladi", "10 ga aylanadi"]),
            ("1 dan 3/8 ni ayirsak, natija qanday kasr?", "5/8", ["3/8", "4/8", "8/3"]),
        ],
    )
    fill(22, 40, b22)
    fill(23, 50, b23)
    put_fixed(
        23,
        [
            ("O‘nli kasrda verguldan keyingi birinchi xona qanday ataladi?", "o‘ndan birlar", ["yuzdan birlar", "mingdan birlar", "o‘nliklar"]),
            ("O‘nli kasrda verguldan keyingi ikkinchi xona qanday ataladi?", "yuzdan birlar", ["o‘ndan birlar", "mingdan birlar", "yuzliklar"]),
            ("O‘nli kasrda verguldan keyingi uchinchi xona qanday ataladi?", "mingdan birlar", ["o‘ndan birlar", "yuzdan birlar", "mingliklar"]),
            ("0,1 soni qanday kasrga teng?", "1/10", ["1/100", "1/1000", "10/1"]),
        ],
    )
    fill(24, 50, b24)
    put_fixed(
        24,
        [
            ("1 km necha metr?", 1000, [100, 10, 60]),
            ("1 m necha santimetr?", 100, [10, 1000, 60]),
            ("1 kg necha gramm?", 1000, [100, 10, 60]),
            ("1 t necha kilogramm?", 1000, [100, 10, 500]),
            ("1% nimani bildiradi?", "sonning yuzdan bir qismini", ["sonning o‘ndan bir qismini", "sonning yarmini", "sonning o‘zini"]),
            ("50% qanday qismga teng?", "1/2", ["1/4", "1/10", "1/5"]),
            ("25% qanday qismga teng?", "1/4", ["1/2", "1/25", "1/5"]),
        ],
    )
    put_fixed(
        25,
        [
            ("Kvadratning nechta simmetriya o‘qi bor?", "4", ["2", "1", "3"]),
            ("Teng tomonli uchburchakning nechta simmetriya o‘qi bor?", "3", ["1", "4", "2"]),
            ("Kvadrat bo‘lmagan to‘g‘ri to‘rtburchakning nechta simmetriya o‘qi bor?", "2", ["4", "1", "0"]),
            ("Teng tomonli bo‘lmagan teng yonli uchburchakning nechta simmetriya o‘qi bor?", "1", ["3", "2", "0"]),
            ("Aylananing simmetriya o‘qlari soni qanday?", "cheksiz ko‘p", ["4", "1", "2"]),
            ("Turli tomonli uchburchakning nechta simmetriya o‘qi bor?", "0", ["1", "3", "2"]),
            ("Kvadrat bo‘lmagan rombning nechta simmetriya o‘qi bor?", "2", ["4", "1", "0"]),
            ("Muntazam oltiburchakning nechta simmetriya o‘qi bor?", "6", ["3", "4", "8"]),
            ("Teng yonli trapetsiyaning nechta simmetriya o‘qi bor?", "1", ["2", "4", "0"]),
            ("O‘q simmetriya qanday almashtirish?", "to‘g‘ri chiziqqa nisbatan aks ettirish", ["nuqta atrofida 180° burish", "parallel ko‘chirish", "cho‘zish"]),
            ("Markaziy simmetriya qanday almashtirish?", "nuqta atrofida 180° burish", ["to‘g‘ri chiziqqa nisbatan aks ettirish", "90° ga burish", "parallel ko‘chirish"]),
            ("Qaysi shakl markaziy simmetriyaga ega?", "kvadrat", ["teng tomonli uchburchak", "teng yonli uchburchak", "turli tomonli uchburchak"]),
            ("Qaysi shaklda simmetriya o‘qi yo‘q?", "turli tomonli uchburchak", ["kvadrat", "aylana", "teng yonli uchburchak"]),
            ("Qaysi almashtirish o‘q simmetriya hisoblanmaydi?", "parallel ko‘chirish", ["kvadrat diagonaliga nisbatan aks ettirish", "aylana diametriga nisbatan aks ettirish", "teng yonli uchburchak balandligiga nisbatan aks ettirish"]),
            ("Simmetriya o‘qi bo‘ylab buklanganda ikki qism qanday joylashadi?", "ustma-ust tushadi", ["doim parallel qoladi", "burchagi 90° ga o‘zgaradi", "yo‘qolib ketadi"]),
            ("Aylana markazidan o‘tgan to‘g‘ri chiziq aylana uchun nima hisoblanadi?", "simmetriya o‘qi", ["faqat urinma", "faqat vatar", "radiusning yarmi"]),
            ("Nuqta va uning o‘qqa nisbatan simmetrik nuqtasi haqida qaysi gap to‘g‘ri?", "ular o‘qdan bir xil uzoqlikda yotadi", ["ular doim koordinata boshida yotadi", "ularning masofasi 0 ga teng", "ular parallel bo‘ladi"]),
            ("To‘g‘ri chiziqqa nisbatan simmetriyada saqlanadigan kattalik qaysi?", "nuqtadan o‘qqacha bo‘lgan masofa", ["nuqtaning faqat rangi", "shaklning faqat nomi", "varaqdagi katak soni"]),
        ],
    )
    fill(26, 36, b26)
    put_fixed(
        27,
        [
            ("Kubning nechta yoqi bor?", "6", ["4", "8", "12"]),
            ("Kubning nechta uchi bor?", "8", ["6", "12", "4"]),
            ("Kubning nechta qirrasi bor?", "12", ["6", "8", "4"]),
            ("To‘g‘ri burchakli parallelepipedning nechta yoqi bor?", "6", ["4", "8", "12"]),
            ("To‘g‘ri burchakli parallelepipedning nechta uchi bor?", "8", ["6", "12", "4"]),
            ("Uchburchakli prizmaning nechta yoqi bor?", "5", ["4", "6", "3"]),
            ("Uchburchakli prizmaning nechta uchi bor?", "6", ["5", "8", "4"]),
            ("Uchburchakli prizmaning nechta qirrasi bor?", "9", ["6", "12", "8"]),
            ("To‘rtburchakli piramidaning nechta yoqi bor?", "5", ["4", "6", "8"]),
            ("To‘rtburchakli piramidaning nechta uchi bor?", "5", ["4", "6", "8"]),
            ("Uchburchakli piramidaning nechta yoqi bor?", "4", ["3", "5", "6"]),
            ("Uchburchakli piramidaning nechta qirrasi bor?", "6", ["4", "8", "12"]),
            ("Prizmaning yon qirralari o‘zaro qanday?", "parallel va teng", ["doim perpendikulyar", "bitta nuqtada kesishadi", "aylana bo‘ylab yotadi"]),
            ("Piramidaning yon qirralari qayerda uchrashadi?", "bitta uchida", ["asos markazida doim", "hech qayerda", "faqat asosning tomonida"]),
            ("Kuboidning barcha yoqlari qanday shakl?", "to‘g‘ri to‘rtburchak", ["uchburchak", "aylana", "trapetsiya"]),
            ("Kubning barcha yoqlari qanday shakl?", "kvadrat", ["to‘g‘ri to‘rtburchak, lekin kvadrat emas", "uchburchak", "doira"]),
            ("Prizmaning yoyilmasida nimalar bo‘ladi?", "ikki asos va yon yoqlar", ["faqat bitta uchburchak", "faqat aylana", "faqat bitta nuqta"]),
            ("Qaysi jismning asosi ko‘pburchak bo‘ladi?", "prizma", ["shar", "silindr", "konus"]),
        ],
    )
    put_fixed(
        28,
        [
            ("Doira markazidan chetigacha bo‘lgan kesma nima?", "radius", ["diametr", "vatar", "urinma"]),
            ("Doira markazidan o‘tib, ikki chetini tutashtiruvchi kesma nima?", "diametr", ["radius", "urinma", "balandlik"]),
            ("Diametr radiusdan necha marta katta?", "2 marta", ["3 marta", "4 marta", "teng"]),
            ("Radiusi 6 cm bo‘lgan doiraning diametri necha santimetr?", 12, [6, 3, 18, 36]),
            ("Diametri 18 cm bo‘lgan doiraning radiusi necha santimetr?", 9, [18, 36, 6]),
            ("Shar qanday jism?", "barcha nuqtalari markazdan bir xil uzoqlikda bo‘lgan yumaloq jism", ["ikki asosli silindr", "uchburchakli prizma", "tekis doira"]),
            ("Doira va sharning farqi qaysi?", "doira tekis shakl, shar hajmli jism", ["ikkalasi ham tekis shakl", "ikkalasi ham piramida", "doira hajmli, shar tekis"]),
            ("Silindrning nechta asosi bor?", "2", ["1", "3", "0"]),
            ("Silindr asoslari qanday shakl?", "doira", ["kvadrat", "uchburchak", "trapetsiya"]),
            ("Silindr yoyilmasi nimadan iborat?", "ikkita doira va bitta to‘g‘ri to‘rtburchak", ["uchta uchburchak", "bitta kvadrat", "faqat aylana"]),
            ("Konusning nechta asosi bor?", "1", ["2", "3", "0"]),
            ("Konus yoyilmasida qanday shakllar bo‘ladi?", "doira va sektor", ["ikkita doira", "uchta kvadrat", "faqat to‘g‘ri to‘rtburchak"]),
            ("Qaysi jismning hamma tekis kesimi doira bo‘lishi mumkin?", "shar", ["kub", "uchburchakli prizma", "piramida"]),
            ("Qaysi jism g‘ildirab yumalashi tabiiy?", "silindr", ["kub", "uchburchakli prizma", "piramida"]),
            ("Radiusi 4 cm bo‘lgan sharning diametri necha santimetr?", 8, [4, 16, 2]),
            ("Agar diametr 20 cm bo‘lsa, radius necha santimetr?", 10, [20, 40, 5]),
        ],
    )
    # Burchaklar: parametrli va qoida.
    def b29():
        kind = rng.randrange(3)
        if kind == 0:
            deg = rng.choice([1, 15, 20, 30, 44, 45, 60, 89, 91, 100, 120, 135, 150, 179])
            if deg < 90:
                correct = "o‘tkir burchak"
            elif deg > 90:
                correct = "o‘tmas burchak"
            else:
                correct = "to‘g‘ri burchak"
            wrongs = [w for w in ("o‘tkir burchak", "to‘g‘ri burchak", "o‘tmas burchak", "yoyiq burchak") if w != correct]
            return (f"{deg}° li burchak qanday burchak?", correct, wrongs)
        if kind == 1:
            deg = rng.choice([20, 25, 30, 35, 40, 45, 50, 55, 60, 70])
            return (
                f"To‘g‘ri chiziqqa qo‘shni burchaklardan biri {deg}°. Ikkinchisi necha gradus?",
                180 - deg,
                [90 - deg, deg, 90, 180],
            )
        deg = rng.choice([15, 20, 25, 30, 35, 40])
        return (
            f"{deg}° li burchakni to‘g‘ri burchakgacha to‘ldirish uchun yana necha gradus kerak?",
            90 - deg,
            [180 - deg, deg, 90, 45],
        )

    fill(29, 50, b29)
    put_fixed(
        29,
        [
            ("To‘g‘ri burchak necha gradus?", "90°", ["45°", "180°", "60°"]),
            ("Yoyiq burchak necha gradus?", "180°", ["90°", "360°", "100°"]),
            ("To‘liq burchak necha gradus?", "360°", ["180°", "90°", "270°"]),
            ("O‘tkir burchak qanday burchak?", "90° dan kichik", ["90° ga teng", "90° dan katta va 180° dan kichik", "180° ga teng"]),
            ("O‘tmas burchak qanday burchak?", "90° dan katta va 180° dan kichik", ["90° dan kichik", "180° ga teng", "90° ga teng"]),
            ("Burchakni graduslarda o‘lchash uchun qaysi asbob ishlatiladi?", "transportir", ["sirkul", "tarozi", "sekundomer"]),
            ("Transportir yordamida burchak yasashda avval nima belgilanadi?", "burchak uchi va bir tomoni", ["faqat shaklning yuzi", "faqat radius", "faqat massa"]),
            ("90° li burchak qanday ataladi?", "to‘g‘ri burchak", ["o‘tkir burchak", "o‘tmas burchak", "yoyiq burchak"]),
        ],
    )
    from rasmlar import iter_pictures
    pics = 0
    for section, prompt, correct, wrongs, picture, uniq in iter_pictures():
        if add(section, prompt, correct, wrongs, picture=picture, uniq=uniq):
            pics += 1
    print(f"rasmli savollar: {pics}")
    from masalalar import toldir
    toldir(add, rng, fmt, clock, frac, dec, gcd, round_nearest, round_down, round_up)


def check() -> None:
    ids = [q["id"] for q in bank]
    assert len(ids) == len(set(ids))
    assert len(seen) == len(bank)
    letters = set("ABCD")
    for q in bank:
        assert q["answer"] in letters
        assert q["options"] == ["A", "B", "C", "D"]
        assert len(q["choices"]) == 4
        assert len(set(q["choices"])) == 4
        assert q["choices"]["ABCD".index(q["answer"])]
        assert q["section"] in META
        assert q["prompt"]
        if q.get("image"):
            assert (root / "sayt" / q["image"]).is_file(), q["image"]
        # javob matni variant ichida
        assert q["choices"]["ABCD".index(q["answer"])] != ""
        correct = q["choices"]["ABCD".index(q["answer"])]
        correct_n = numeric(correct)
        if correct_n is not None:
            for choice in q["choices"]:
                if choice == correct:
                    continue
                other = numeric(choice)
                assert other != correct_n, q["id"] + " " + q["prompt"]
    # namunaviy hisob-kitobni qayta tekshirish
    import re

    def num(s: str) -> int:
        return int(s.replace(" ", "").replace("−", "-"))

    checked = 0
    for q in bank:
        ans = q["choices"]["ABCD".index(q["answer"])]
        m = re.fullmatch(r"Hisoblang: (.+) \+ (.+)", q["prompt"])
        if m and "," not in q["prompt"] and "/" not in q["prompt"]:
            assert num(ans) == num(m.group(1)) + num(m.group(2))
            checked += 1
        m = re.fullmatch(r"Hisoblang: (.+) − (.+)", q["prompt"])
        if m and "," not in q["prompt"] and "/" not in q["prompt"] and ":" not in q["prompt"]:
            assert num(ans) == num(m.group(1)) - num(m.group(2))
            checked += 1
        m = re.fullmatch(r"Hisoblang: (.+) · (.+)", q["prompt"])
        if m and "/" not in q["prompt"]:
            assert num(ans) == num(m.group(1)) * num(m.group(2))
            checked += 1
        m = re.fullmatch(r"Hisoblang: (.+) : (\d+)", q["prompt"])
        if m:
            assert num(ans) == num(m.group(1)) // int(m.group(2))
            checked += 1
        m = re.fullmatch(r"Bo‘ling: (.+) : (\d+)", q["prompt"])
        if m:
            assert num(ans) == num(m.group(1)) // int(m.group(2))
            checked += 1
    print("qayta tekshirilgan ifoda:", checked)
    assert checked > 40
    from masalalar import tekshir
    masala_checked = tekshir(bank)
    print("qayta tekshirilgan masala:", masala_checked)
    assert masala_checked == 508


if __name__ == "__main__":
    build()
    check()
    # Ba'zi qat'iy savollarda xato qavslar tushib qolgan bo'lishi mumkin.
    bad = [q for q in bank if any(isinstance(c, list) for c in q["choices"]) or not isinstance(q["prompt"], str)]
    if bad:
        raise SystemExit(f"Yaroqsiz savol: {bad[0]['id']}")
    out_path.write_text(json.dumps(bank, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Jami: {len(bank)} ta savol -> {out_path}")
    for s in range(1, 30):
        n = sum(1 for q in bank if q["section"] == s)
        print(f"  {s:2d}. {n:3d}  {META[s][0]} qism")
