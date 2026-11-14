# -*- coding: utf-8 -*-
"""4-sinf uchun original matnli masalalar.

Darslikdagi masalalar ko‘chirilmaydi. Har bir javob shu yerda hisoblanadi.
"""
from __future__ import annotations

import re
from fractions import Fraction

NAMES = [
    "Ali", "Madina", "Jasur", "Sevara", "Bekzod", "Nodira", "Aziz", "Malika",
    "Bobur", "Dilnoza", "Kamola", "Sardor", "Zilola", "Akmal", "Lola", "Shahzod",
]
ITEMS = ["daftar", "kitob", "olma", "ruchka", "qalam", "koptok", "nok", "gul"]
CITIES = [
    "Samarqand", "Buxoro", "Andijon", "Namangan", "Farg‘ona", "Nukus",
    "Termiz", "Guliston", "Jizzax", "Qarshi", "Navoiy", "Urganch",
]


def toldir(add, rng, fmt, clock, frac, dec, gcd, round_nearest, round_down, round_up) -> int:
    def until(section: int, target: int, builder) -> int:
        got = 0
        guard = 0
        while got < target and guard < target * 80:
            guard += 1
            item = builder()
            if not item:
                continue
            prompt, correct, wrongs = item
            if add(section, prompt, correct, wrongs):
                got += 1
        if got < target:
            print(f"  masala {section} yetmadi: {got}/{target}")
        return got

    def people():
        return rng.sample(NAMES, 2)

    def item():
        return rng.choice(ITEMS)

    def cities():
        return rng.sample(CITIES, 2)

    def s2_qosh():
        name, thing, a, b = rng.choice(NAMES), item(), rng.randint(12, 480), rng.randint(6, 260)
        correct = a + b
        return (
            f"{name}da {fmt(a)} ta {thing} bor edi. Yana {fmt(b)} ta olib kelishdi. Jami nechta {thing} bo‘ldi?",
            correct,
            [abs(a - b), a, b, correct + b, correct + 10],
        )

    def s2_ayir():
        thing, a = item(), rng.randint(40, 900)
        b = rng.randint(8, a - 5)
        correct = a - b
        return (
            f"Do‘konda {fmt(a)} ta {thing} bor edi. {fmt(b)} tasi sotildi. Nechtasi qoldi?",
            correct,
            [a + b, a, b, correct + b, max(1, correct - 1)],
        )

    def s2_katta():
        name, thing, a = rng.choice(NAMES), item(), rng.randint(1200, 18000)
        b = rng.randint(150, a - 80)
        correct = a - b
        return (
            f"Kutubxonada {fmt(a)} ta {thing} bor edi. {fmt(b)} tasi o‘quvchilarga berildi. Kutubxonada nechta {thing} qoldi?",
            correct,
            [a + b, b, a, correct + 100, max(1, correct - 10)],
        )

    def s2_kop():
        name1, name2 = people()
        thing, a, diff = item(), rng.randint(8, 90), rng.randint(2, 40)
        b = a + diff
        return (
            f"{name1}da {a} ta {thing}, {name2}da {b} ta {thing} bor. {name2}da nechta ko‘p?",
            diff,
            [a + b, b, a, diff + a, diff + 1],
        )

    def s2_kam():
        name1, name2 = people()
        thing, b, diff = item(), rng.randint(8, 70), rng.randint(2, 35)
        a = b + diff
        return (
            f"{name1}da {a} ta {thing}, {name2}da {b} ta {thing} bor. {name2}da nechta kam?",
            diff,
            [a + b, a, b, diff + b, max(1, diff - 1)],
        )

    def s2_yosh():
        name, age, k = rng.choice(NAMES), rng.randint(8, 12), rng.randint(2, 15)
        return (
            f"Hozir {name} {age} yoshda. {k} yildan keyin u necha yoshda bo‘ladi?",
            age + k,
            [age, k, abs(age - k), age + k + 1, age * k],
        )

    def s2_ota():
        son = rng.randint(8, 14)
        diff = rng.randint(22, 32)
        father = son + diff
        return (
            f"Ota {father} yoshda, o‘g‘li {son} yoshda. Ota o‘g‘lidan necha yosh katta?",
            diff,
            [father, son, father + son, diff + son, diff - 1],
        )

    def s2_quti():
        thing, k, n = item(), rng.randint(4, 24), rng.randint(2, 12)
        correct = k * n
        return (
            f"Bir qutida {k} ta {thing} bor. {n} ta bir xil qutida jami nechta {thing} bor?",
            correct,
            [k + n, k, n, correct + k, correct + n],
        )

    def s2_taqsim():
        n, each = rng.randint(3, 12), rng.randint(4, 24)
        total, thing = n * each, item()
        return (
            f"{fmt(total)} ta {thing}ni {n} nafar o‘quvchiga teng taqsimlashdi. Har biriga nechtadan tegdi?",
            each,
            [total, n, each + n, each + 1, max(1, each - 1)],
        )

    def s2_narx():
        thing = rng.choice(["daftar", "kitob", "ruchka", "qalam"])
        price = rng.choice([800, 1200, 1500, 2000, 2500, 3000, 4000, 4500, 5000])
        n = rng.randint(2, 8)
        correct = price * n
        return (
            f"Bitta {thing} {fmt(price)} so‘m turadi. {n} tasini olish uchun necha so‘m kerak?",
            correct,
            [price + n, price, n, correct + price, correct - price],
        )

    def s3_qator():
        rows, each, extra = rng.randint(3, 12), rng.randint(4, 16), rng.randint(2, 25)
        planted = rows * each
        correct = planted + extra
        return (
            f"Bog‘da {rows} qatorga {each} tadan ko‘chat ekildi. Ertasi yana {extra} ta ekildi. Jami nechta ko‘chat?",
            correct,
            [planted, rows + each + extra, extra, correct + each, planted - extra if planted > extra else planted + 1],
        )

    def s3_pul():
        name = rng.choice(NAMES)
        thing = rng.choice(["daftar", "kitob", "ruchka", "qalam", "olma"])
        price = rng.choice([1500, 2000, 2500, 3000, 4000, 5000, 6000, 8000])
        n = rng.randint(2, 6)
        spent = price * n
        left = rng.choice([1000, 2000, 3000, 5000, 8000, 10000, 15000])
        money = spent + left
        return (
            f"{name}ning {fmt(money)} so‘m puli bor. U narxi {fmt(price)} so‘m bo‘lgan {thing}dan {n} ta oldi. Qancha puli qoldi?",
            left,
            [money, spent, money - price, left + price, spent + price],
        )

    def s3_ombor():
        thing, a, b = item(), rng.randint(30, 180), rng.randint(10, 90)
        total = a + b
        c = rng.randint(8, total - 5)
        correct = total - c
        return (
            f"Omborda {fmt(a)} ta {thing} bor edi. {fmt(b)} ta olib kelishdi, keyin {fmt(c)} tasi sinflarga berildi. Omborda nechta {thing} qoldi?",
            correct,
            [total, c, a - b if a > b else b, correct + c, a + c],
        )

    def s3_xarid():
        name = rng.choice(NAMES)
        thing1, thing2 = rng.sample(["daftar", "kitob", "ruchka", "qalam", "olma", "nok"], 2)
        p1, p2 = rng.choice([500, 800, 1200, 1500, 2000]), rng.choice([700, 1000, 1800, 2500, 3000])
        n1, n2 = rng.randint(2, 6), rng.randint(2, 5)
        a, b = p1 * n1, p2 * n2
        correct = a + b
        return (
            f"{name} {n1} ta {thing1}ni, har birini {fmt(p1)} so‘mdan, va {n2} ta {thing2}ni, har birini {fmt(p2)} so‘mdan oldi. Jami necha so‘m to‘ladi?",
            correct,
            [a, b, p1 + p2, correct + p1, abs(a - b) or p1],
        )

    def s4_kun():
        thing = rng.choice(["stul", "ko‘ylak", "non", "parta"])
        rate, hours = rng.randint(4, 18), rng.randint(2, 8)
        correct = rate * hours
        return (
            f"Usta 1 soatda {rate} ta {thing} tayyorlaydi. {hours} soatda nechta {thing} tayyorlaydi?",
            correct,
            [rate + hours, rate, hours, correct + rate, correct + hours],
        )

    def s4_buyurtma():
        thing = rng.choice(["stul", "ko‘ylak", "parta", "oyna"])
        rate, days = rng.randint(4, 15), rng.randint(2, 9)
        total = rate * days
        return (
            f"Buyurtma {total} ta {thing}. Usta kuniga {rate} ta tayyorlaydi. Buyurtma necha kunda bajariladi?",
            days,
            [total, rate, days + rate, days + 1, max(1, days - 1)],
        )

    def s5_qosh():
        x, a = rng.randint(15, 800), rng.randint(8, 500)
        b = x + a
        return (
            f"O‘ylangan songa {fmt(a)} qo‘shilsa, {fmt(b)} chiqadi. O‘ylangan son nechchi?",
            x,
            [b, a, b + a, x + a, abs(b - x) + 1],
        )

    def s5_ayir():
        x, a = rng.randint(40, 900), rng.randint(5, 200)
        if x <= a:
            return None
        b = x - a
        return (
            f"O‘ylangan sondan {fmt(a)} ayirilsa, {fmt(b)} qoladi. O‘ylangan son nechchi?",
            x,
            [b, a, abs(b - a), x + a, b + 10],
        )

    def s6_yuza():
        a, b = rng.randint(4, 24), rng.randint(3, 16)
        area, peri = a * b, 2 * (a + b)
        return (
            f"Xonaning bo‘yi {a} m, eni {b} m. Poliga gilam yotqizish uchun necha kvadrat metr gilam kerak?",
            area,
            [peri, a + b, area + a, abs(a - b) * max(a, b)],
        )

    def s6_sim():
        a, b = rng.randint(8, 40), rng.randint(5, 25)
        peri, area = 2 * (a + b), a * b
        return (
            f"Bog‘ning bo‘yi {a} m, eni {b} m. Atrofiga sim tortish uchun necha metr sim kerak?",
            peri,
            [area, a + b, peri + 2, a * b // 2 or peri + a],
        )

    def s6_vaqt():
        h, m = rng.randint(6, 14), rng.choice([0, 10, 15, 20, 30, 40, 45])
        dh, dm = rng.randint(1, 4), rng.choice([0, 10, 15, 20, 30])
        end = h * 60 + m + dh * 60 + dm
        eh, em = divmod(end, 60)
        if eh > 22:
            return None
        correct = clock(eh, em)
        trip = f"{dh} soat" if dm == 0 else f"{dh} soat {dm} daqiqa"
        wrongs = [clock(h, m), clock(eh, (em + 15) % 60), clock(min(22, eh + 1), em), trip]
        return (
            f"Poyezd soat {clock(h, m)} da jo‘nadi va {trip} yurdi. Soat nechada yetib boradi?",
            correct,
            wrongs,
        )

    def s8_ball():
        name = rng.choice(NAMES)
        scores = [rng.randint(6, 10) for _ in range(3)]
        need = (4 - (sum(scores) % 4)) % 4
        last = [n for n in range(6, 11) if n % 4 == need]
        scores.append(rng.choice(last))
        correct = sum(scores) // 4
        text = ", ".join(str(x) for x in scores)
        return (
            f"{name} to‘rtta nazorat ishidan {text} ball oldi. O‘rta arifmetik balli nechchi?",
            correct,
            [sum(scores), max(scores), min(scores), correct + 1, max(1, correct - 1)],
        )

    def s9_ikki():
        futbol, shaxmat = rng.randint(8, 24), rng.randint(6, 18)
        both = rng.randint(1, min(futbol, shaxmat) - 1)
        correct = futbol + shaxmat - both
        return (
            f"Sinfda {futbol} o‘quvchi futbolni, {shaxmat} o‘quvchi shaxmatni yoqtiradi. {both} o‘quvchi ikkalasini ham yoqtiradi. Kamida bittasini yoqtiradiganlar nechta?",
            correct,
            [futbol + shaxmat, futbol + shaxmat + both, abs(futbol - shaxmat), both, correct + both],
        )

    def s10_masofa():
        name1, name2 = people()
        a, b = rng.sample(range(0, 21), 2)
        correct = abs(a - b)
        if correct == 0:
            return None
        return (
            f"Sayr chizig‘ida {name1} 0 dan {a} birlik, {name2} 0 dan {b} birlik narida. Ular orasidagi masofa necha birlik?",
            correct,
            [a + b, a, b, correct + 1, max(1, correct - 1)],
        )

    def s11_xarita():
        c1, c2 = cities()
        k, cm = rng.choice([4, 5, 6, 8, 10, 12, 15, 20]), rng.randint(2, 12)
        correct = k * cm
        return (
            f"Sayyoh xaritada {c1}dan {c2}gacha {cm} cm masofa o‘lchadi. Xaritada 1 cm haqiqatda {k} km. Shaharlar orasi necha kilometr?",
            correct,
            [k + cm, k, cm, correct + k, correct + cm],
        )

    def s12_yol():
        c1, c2 = cities()
        v, t = rng.choice([36, 40, 45, 48, 50, 54, 60, 72, 80]), rng.choice([2, 3, 4, 5, 6])
        correct = v * t
        return (
            f"Avtobus {c1}dan {c2} tomon {v} km/soat tezlik bilan {t} soat yurdi. U qancha yo‘l bosdi?",
            f"{fmt(correct)} km",
            [f"{v + t} km", f"{fmt(v)} km", f"{t} km", f"{fmt(correct + v)} km", f"{fmt(correct + t)} km"],
        )

    def s12_qolgan():
        v, t_total = rng.choice([40, 45, 50, 60, 72, 80]), rng.randint(3, 6)
        done_t = rng.randint(1, t_total - 1)
        left_t = t_total - done_t
        whole, done = v * t_total, v * done_t
        return (
            f"Shaharlar orasi {fmt(whole)} km. Avtomobil {v} km/soat tezlik bilan {fmt(done)} km yurib bo‘ldi. Qolgan yo‘lni shu tezlikda necha soatda bosadi?",
            left_t,
            [t_total, done_t, v, left_t + 1, whole],
        )

    def s12_yana():
        v, t, extra = rng.choice([40, 48, 50, 60, 70]), rng.randint(2, 5), rng.choice([12, 15, 18, 20, 25, 30])
        first = v * t
        correct = first + extra
        return (
            f"Avtomobil {v} km/soat tezlik bilan {t} soat yurdi. So‘ng yana {extra} km yo‘l bosdi. Jami necha kilometr yo‘l bosdi?",
            correct,
            [first, extra, v + t + extra, correct + v, first - extra if first > extra else first + extra],
        )

    def s13_qarama():
        c1, c2 = cities()
        v1, v2 = rng.choice([(40, 60), (50, 70), (45, 55), (30, 50), (36, 54), (48, 72)])
        t = rng.randint(2, 5)
        s = (v1 + v2) * t
        return (
            f"{c1} va {c2} orasi {fmt(s)} km. Bir avtobus {c1}dan {v1} km/soat, ikkinchisi {c2}dan {v2} km/soat tezlik bilan bir vaqtda qarama-qarshi yo‘lga chiqdi. Necha soatdan keyin uchrashadilar?",
            t,
            [v1 + v2, s, t + 1, abs(v1 - v2), v1],
        )

    def s13_quv():
        v1, v2 = rng.choice([(80, 60), (70, 50), (90, 60), (60, 40), (54, 36), (72, 48)])
        t = rng.randint(2, 5)
        gap = (v1 - v2) * t
        return (
            f"Ikki velosipedchi bir yo‘nalishda ketyapti. Oldingisi {v2} km/soat, keyingisi {v1} km/soat. Oradagi masofa {gap} km. Keyingisi oldingisiga necha soatda yetadi?",
            t,
            [v1 + v2, gap, v1 - v2, t + 1, v2],
        )

    def s14_kg():
        place = 100
        n = rng.randint(place + 15, 9000)
        if n % place == 0:
            n += rng.randint(1, place - 1)
        correct = round_nearest(n, place)
        return (
            f"Bozorga {fmt(n)} kg kartoshka keltirildi. Bu massani yuzlikkacha yaxlitlasa, necha kilogramm bo‘ladi?",
            correct,
            [round_down(n, place), round_up(n, place), n, correct + place, max(0, correct - place)],
        )

    def s15_cham():
        a, b = rng.randint(120, 880), rng.randint(120, 880)
        est = round_nearest(a, 100) + round_nearest(b, 100)
        return (
            f"Do‘kon hisobchisi {fmt(a)} so‘m va {fmt(b)} so‘mlik xarajatni yuzlikkacha chamalaydi. Taxminan necha so‘m chiqadi?",
            est,
            [a + b, round_down(a, 100) + round_down(b, 100), est + 100, abs(est - 100), a],
        )

    def s16_hovuz():
        A, B = rng.randint(8, 20), rng.randint(6, 14)
        a, b = rng.randint(2, A - 2), rng.randint(2, B - 2)
        whole, cut = A * B, a * b
        correct = whole - cut
        return (
            f"Hovlining bo‘yi {A} m, eni {B} m. Burchagida bo‘yi {a} m, eni {b} m hovuz bor. Hovuzdan tashqari maydon necha kvadrat metr?",
            correct,
            [whole, cut, whole + cut, correct + a, abs(A * b - a * B) or whole],
        )

    def s17_qoldiq():
        n, q = rng.randint(3, 9), rng.randint(4, 18)
        r = rng.randint(1, n - 1)
        total, thing = n * q + r, item()
        correct = f"{q} tadan, qoldiq {r}"
        wrongs = [
            f"{q + 1} tadan, qoldiq {r}",
            f"{q} tadan, qoldiq {0 if r + 1 == n else r + 1}",
            f"{max(1, q - 1)} tadan, qoldiq {r}",
            f"{q} tadan, qoldiq 0",
            f"{q + 1} tadan, qoldiq {max(1, r - 1)}",
        ]
        return (
            f"{fmt(total)} ta {thing}ni {n} nafar bolaga teng taqsimlamoqchi. Har biriga nechtadan to‘g‘ri keladi va nechtasi ortib qoladi?",
            correct,
            wrongs,
        )

    def s17_ikki_qop():
        n = rng.randint(3, 9)
        a, b = n * rng.randint(2, 8), n * rng.randint(2, 8)
        correct = (a + b) // n
        thing = rng.choice(["olma", "nok", "kitob", "daftar"])
        return (
            f"Birinchi qopda {a} ta, ikkinchisida {b} ta {thing} bor. Hammasini {n} ta kichik qopga teng solishsa, har birida nechtadan bo‘ladi?",
            correct,
            [a + b, a, b, correct + n, max(1, correct - 1)],
        )

    def s18_qism():
        den = rng.choice([2, 3, 4, 5, 6, 8, 10])
        num = rng.randint(1, den - 1)
        if gcd(num, den) != 1:
            return None
        whole = den * rng.randint(4, 16)
        correct = whole // den * num
        return (
            f"Sinfda {whole} nafar o‘quvchi bor. Ularning {num}/{den} qismi ekskursiyaga bordi. Necha nafar o‘quvchi bordi?",
            correct,
            [whole // den, whole, whole - correct, correct + den, abs(correct - num) or whole // den],
        )

    def s18_qolgan():
        den = rng.choice([2, 3, 4, 5, 6, 8, 10])
        num = rng.randint(1, den - 1)
        if gcd(num, den) != 1:
            return None
        whole = den * rng.randint(4, 16)
        girls = whole // den * num
        boys = whole - girls
        if boys == 0:
            return None
        return (
            f"Sinfdagi {whole} nafar o‘quvchining {num}/{den} qismi qizlar. O‘g‘il bolalar nechta?",
            boys,
            [girls, whole, whole // den, boys + den, abs(boys - num) or girls],
        )

    def s21_tort():
        d = rng.randint(5, 12)
        a = rng.randint(1, d - 2)
        b = rng.randint(1, d - a - 1)
        correct = frac(a + b, d)
        return (
            f"Tortning {a}/{d} qismini opa, {b}/{d} qismini uka yedi. Birga tortning qancha qismini yeyishdi?",
            correct,
            [frac(abs(a - b), d), f"{a + b}/{d * 2}", f"{a}/{d}", frac(a + b, d + 1), f"{b}/{d}"],
        )

    def s22_kun():
        d = rng.choice([2, 3, 4, 5, 6, 8])
        n = rng.randint(1, d - 1)
        if gcd(n, d) != 1:
            return None
        k = rng.randint(2, 6)
        return (
            f"Har kuni sharbatning {n}/{d} qismi ichiladi. {k} kunda jami qancha qismi ichiladi?",
            frac(n * k, d),
            [f"{n}/{d}", frac(n, d * k), frac(n + k, d), frac(n * k, d + 1), f"{k}/{d}"],
        )

    def s23_ip():
        a = rng.randint(180, 480)
        b = rng.randint(25, a - 20)
        correct = dec(a - b, 2)
        return (
            f"Ipning uzunligi {dec(a, 2)} m edi. Undan {dec(b, 2)} m kesib olindi. Necha metr ip qoldi?",
            correct,
            [dec(a + b, 2), dec(a, 2), dec(b, 2), dec(a - b + 15, 2), dec(abs(a - b - 10), 2)],
        )

    def s24_foiz():
        percent = rng.choice([10, 20, 25, 50])
        whole = rng.choice([20, 24, 28, 32, 36, 40, 48, 60, 80, 100, 120, 160, 200])
        if (whole * percent) % 100:
            return None
        correct = whole * percent // 100
        return (
            f"Sinfda {whole} nafar o‘quvchi bor. {percent}% i matematikadan a’lo baho oldi. A’lochilar nechta?",
            correct,
            [whole, percent, whole // 10, correct + percent, abs(whole - correct) or correct + 1],
        )

    def s24_chegirma():
        percent = rng.choice([10, 20, 25, 50])
        price = rng.choice([8000, 12000, 16000, 20000, 24000, 28000, 36000, 40000])
        discount = price * percent // 100
        pay = price - discount
        return (
            f"Kitobning narxi {fmt(price)} so‘m. Chegirma {percent}%. Necha so‘m to‘lanadi?",
            pay,
            [price, discount, pay + price, abs(pay - discount) + 1000, pay + 1000],
        )

    def s24_qop():
        n, kg = rng.randint(3, 12), rng.choice([5, 8, 10, 12, 15, 20, 25, 50])
        correct = n * kg
        return (
            f"Omborxonaga {n} ta qop un keltirildi. Har bir qop {kg} kg. Jami necha kilogramm un?",
            correct,
            [n + kg, kg, n, correct + kg, correct + n],
        )

    def s26_dala():
        a, b = rng.randint(6, 18), rng.randint(4, 12)
        c, d = rng.randint(5, 16), rng.randint(4, 12)
        first, second = a * b, c * d
        correct = first + second
        return (
            f"Birinchi dalaning bo‘yi {a} m, eni {b} m. Ikkinchi dalaning bo‘yi {c} m, eni {d} m. Ikki dalaning umumiy yuzi necha kvadrat metr?",
            correct,
            [first, second, 2 * (a + b + c + d), correct + a, abs(first - second) or first],
        )

    plan = [
        (2, 14, s2_qosh), (2, 12, s2_ayir), (2, 10, s2_katta), (2, 10, s2_kop),
        (2, 8, s2_kam), (2, 8, s2_yosh), (2, 8, s2_ota), (2, 12, s2_quti),
        (2, 12, s2_taqsim), (2, 10, s2_narx),
        (3, 14, s3_qator), (3, 14, s3_pul), (3, 12, s3_ombor), (3, 12, s3_xarid),
        (4, 12, s4_kun), (4, 12, s4_buyurtma),
        (5, 12, s5_qosh), (5, 12, s5_ayir),
        (6, 10, s6_yuza), (6, 10, s6_sim), (6, 10, s6_vaqt),
        (8, 16, s8_ball),
        (9, 12, s9_ikki),
        (10, 12, s10_masofa),
        (11, 12, s11_xarita),
        (12, 10, s12_yol), (12, 8, s12_qolgan), (12, 8, s12_yana),
        (13, 8, s13_qarama), (13, 8, s13_quv),
        (14, 16, s14_kg),
        (15, 12, s15_cham),
        (16, 12, s16_hovuz),
        (17, 16, s17_qoldiq), (17, 12, s17_ikki_qop),
        (18, 12, s18_qism), (18, 12, s18_qolgan),
        (21, 16, s21_tort),
        (22, 12, s22_kun),
        (23, 16, s23_ip),
        (24, 12, s24_foiz), (24, 10, s24_chegirma), (24, 10, s24_qop),
        (26, 12, s26_dala),
    ]
    total = 0
    for section, target, builder in plan:
        total += until(section, target, builder)
    print(f"masalalar: {total}")
    return total


def _int(text: str) -> int:
    raw = str(text).replace(" ", "").replace("−", "-")
    if raw.endswith("km"):
        raw = raw[:-2]
    return int(raw)


def _fraction(text: str):
    raw = str(text).strip()
    mixed = re.fullmatch(r"(\d+) (\d+)/(\d+)", raw)
    if mixed:
        return int(mixed.group(1)) + Fraction(int(mixed.group(2)), int(mixed.group(3)))
    compact = raw.replace(" ", "")
    m = re.fullmatch(r"(\d+),(\d+)", compact)
    if m:
        return Fraction(int(m.group(1) + m.group(2)), 10 ** len(m.group(2)))
    m = re.fullmatch(r"(\d+)/(\d+)", compact)
    if m:
        return Fraction(int(m.group(1)), int(m.group(2)))
    if re.fullmatch(r"\d+", compact):
        return Fraction(int(compact))
    return None


def _nearest(n: int, place: int) -> int:
    down = n // place * place
    if (n % place) * 2 >= place:
        return down + place
    return down


def tekshir(bank: list[dict]) -> int:
    """Matnli masalalarning javobini savol matnidan qayta hisoblaydi."""
    checked = 0
    rules = [
        (r"(\S+)da ([\d ]+) ta (\S+) bor edi\. Yana ([\d ]+) ta olib kelishdi\. Jami nechta \3 bo‘ldi\?",
         lambda m: _int(m.group(2)) + _int(m.group(4))),
        (r"Do‘konda ([\d ]+) ta (\S+) bor edi\. ([\d ]+) tasi sotildi\. Nechtasi qoldi\?",
         lambda m: _int(m.group(1)) - _int(m.group(3))),
        (r"Kutubxonada ([\d ]+) ta (\S+) bor edi\. ([\d ]+) tasi o‘quvchilarga berildi\. Kutubxonada nechta \2 qoldi\?",
         lambda m: _int(m.group(1)) - _int(m.group(3))),
        (r"(\S+)da (\d+) ta (\S+), (\S+)da (\d+) ta \3 bor\. \4da nechta ko‘p\?",
         lambda m: int(m.group(5)) - int(m.group(2))),
        (r"(\S+)da (\d+) ta (\S+), (\S+)da (\d+) ta \3 bor\. \4da nechta kam\?",
         lambda m: int(m.group(2)) - int(m.group(5))),
        (r"Hozir (\S+) (\d+) yoshda\. (\d+) yildan keyin u necha yoshda bo‘ladi\?",
         lambda m: int(m.group(2)) + int(m.group(3))),
        (r"Ota (\d+) yoshda, o‘g‘li (\d+) yoshda\. Ota o‘g‘lidan necha yosh katta\?",
         lambda m: int(m.group(1)) - int(m.group(2))),
        (r"Bir qutida (\d+) ta (\S+) bor\. (\d+) ta bir xil qutida jami nechta \2 bor\?",
         lambda m: int(m.group(1)) * int(m.group(3))),
        (r"([\d ]+) ta (\S+)ni (\d+) nafar o‘quvchiga teng taqsimlashdi\. Har biriga nechtadan tegdi\?",
         lambda m: _int(m.group(1)) // int(m.group(3))),
        (r"Bitta (\S+) ([\d ]+) so‘m turadi\. (\d+) tasini olish uchun necha so‘m kerak\?",
         lambda m: _int(m.group(2)) * int(m.group(3))),
        (r"Bog‘da (\d+) qatorga (\d+) tadan ko‘chat ekildi\. Ertasi yana (\d+) ta ekildi\. Jami nechta ko‘chat\?",
         lambda m: int(m.group(1)) * int(m.group(2)) + int(m.group(3))),
        (r"(\S+)ning ([\d ]+) so‘m puli bor\. U narxi ([\d ]+) so‘m bo‘lgan (\S+)dan (\d+) ta oldi\. Qancha puli qoldi\?",
         lambda m: _int(m.group(2)) - _int(m.group(3)) * int(m.group(5))),
        (r"Omborda ([\d ]+) ta (\S+) bor edi\. ([\d ]+) ta olib kelishdi, keyin ([\d ]+) tasi sinflarga berildi\. Omborda nechta \2 qoldi\?",
         lambda m: _int(m.group(1)) + _int(m.group(3)) - _int(m.group(4))),
        (r"(\S+) (\d+) ta (\S+)ni, har birini ([\d ]+) so‘mdan, va (\d+) ta (\S+)ni, har birini ([\d ]+) so‘mdan oldi\. Jami necha so‘m to‘ladi\?",
         lambda m: int(m.group(2)) * _int(m.group(4)) + int(m.group(5)) * _int(m.group(7))),
        (r"Usta 1 soatda (\d+) ta (\S+) tayyorlaydi\. (\d+) soatda nechta \2 tayyorlaydi\?",
         lambda m: int(m.group(1)) * int(m.group(3))),
        (r"Buyurtma (\d+) ta (\S+)\. Usta kuniga (\d+) ta tayyorlaydi\. Buyurtma necha kunda bajariladi\?",
         lambda m: int(m.group(1)) // int(m.group(3))),
        (r"O‘ylangan songa ([\d ]+) qo‘shilsa, ([\d ]+) chiqadi\. O‘ylangan son nechchi\?",
         lambda m: _int(m.group(2)) - _int(m.group(1))),
        (r"O‘ylangan sondan ([\d ]+) ayirilsa, ([\d ]+) qoladi\. O‘ylangan son nechchi\?",
         lambda m: _int(m.group(1)) + _int(m.group(2))),
        (r"Xonaning bo‘yi (\d+) m, eni (\d+) m\. Poliga gilam yotqizish uchun necha kvadrat metr gilam kerak\?",
         lambda m: int(m.group(1)) * int(m.group(2))),
        (r"Bog‘ning bo‘yi (\d+) m, eni (\d+) m\. Atrofiga sim tortish uchun necha metr sim kerak\?",
         lambda m: 2 * (int(m.group(1)) + int(m.group(2)))),
        (r"Sinfda (\d+) o‘quvchi futbolni, (\d+) o‘quvchi shaxmatni yoqtiradi\. (\d+) o‘quvchi ikkalasini ham yoqtiradi\. Kamida bittasini yoqtiradiganlar nechta\?",
         lambda m: int(m.group(1)) + int(m.group(2)) - int(m.group(3))),
        (r"Sayr chizig‘ida (\S+) 0 dan (\d+) birlik, (\S+) 0 dan (\d+) birlik narida\. Ular orasidagi masofa necha birlik\?",
         lambda m: abs(int(m.group(2)) - int(m.group(4)))),
        (r"Sayyoh xaritada (\S+)dan (\S+)gacha (\d+) cm masofa o‘lchadi\. Xaritada 1 cm haqiqatda (\d+) km\. Shaharlar orasi necha kilometr\?",
         lambda m: int(m.group(3)) * int(m.group(4))),
        (r"Shaharlar orasi ([\d ]+) km\. Avtomobil (\d+) km/soat tezlik bilan ([\d ]+) km yurib bo‘ldi\. Qolgan yo‘lni shu tezlikda necha soatda bosadi\?",
         lambda m: (_int(m.group(1)) - _int(m.group(3))) // int(m.group(2))),
        (r"Avtomobil (\d+) km/soat tezlik bilan (\d+) soat yurdi\. So‘ng yana (\d+) km yo‘l bosdi\. Jami necha kilometr yo‘l bosdi\?",
         lambda m: int(m.group(1)) * int(m.group(2)) + int(m.group(3))),
        (r"Birinchi qopda (\d+) ta, ikkinchisida (\d+) ta (\S+) bor\. Hammasini (\d+) ta kichik qopga teng solishsa, har birida nechtadan bo‘ladi\?",
         lambda m: (int(m.group(1)) + int(m.group(2))) // int(m.group(4))),
        (r"Sinfda (\d+) nafar o‘quvchi bor\. Ularning (\d+)/(\d+) qismi ekskursiyaga bordi\. Necha nafar o‘quvchi bordi\?",
         lambda m: int(m.group(1)) // int(m.group(3)) * int(m.group(2))),
        (r"Sinfdagi (\d+) nafar o‘quvchining (\d+)/(\d+) qismi qizlar\. O‘g‘il bolalar nechta\?",
         lambda m: int(m.group(1)) - int(m.group(1)) // int(m.group(3)) * int(m.group(2))),
        (r"Omborxonaga (\d+) ta qop un keltirildi\. Har bir qop (\d+) kg\. Jami necha kilogramm un\?",
         lambda m: int(m.group(1)) * int(m.group(2))),
        (r"Kitobning narxi ([\d ]+) so‘m\. Chegirma (\d+)%\. Necha so‘m to‘lanadi\?",
         lambda m: _int(m.group(1)) - _int(m.group(1)) * int(m.group(2)) // 100),
        (r"Sinfda (\d+) nafar o‘quvchi bor\. (\d+)% i matematikadan a’lo baho oldi\. A’lochilar nechta\?",
         lambda m: int(m.group(1)) * int(m.group(2)) // 100),
        (r"Poyezd soat (\d+):(\d+) da jo‘nadi va (\d+) soat(?: (\d+) daqiqa)? yurdi\. Soat nechada yetib boradi\?",
         lambda m: f"{(int(m.group(1)) * 60 + int(m.group(2)) + int(m.group(3)) * 60 + int(m.group(4) or 0)) // 60}:{((int(m.group(1)) * 60 + int(m.group(2)) + int(m.group(3)) * 60 + int(m.group(4) or 0)) % 60):02d}"),
        (r"(\S+) to‘rtta nazorat ishidan ([\d, ]+) ball oldi\. O‘rta arifmetik balli nechchi\?",
         lambda m: sum(int(x) for x in m.group(2).split(",")) // 4),
        (r"Avtobus (\S+)dan (\S+) tomon (\d+) km/soat tezlik bilan (\d+) soat yurdi\. U qancha yo‘l bosdi\?",
         lambda m: int(m.group(3)) * int(m.group(4))),
        (r"(\S+) va (\S+) orasi ([\d ]+) km\. Bir avtobus \1dan (\d+) km/soat, ikkinchisi \2dan (\d+) km/soat tezlik bilan bir vaqtda qarama-qarshi yo‘lga chiqdi\. Necha soatdan keyin uchrashadilar\?",
         lambda m: _int(m.group(3)) // (int(m.group(4)) + int(m.group(5)))),
        (r"Ikki velosipedchi bir yo‘nalishda ketyapti\. Oldingisi (\d+) km/soat, keyingisi (\d+) km/soat\. Oradagi masofa (\d+) km\. Keyingisi oldingisiga necha soatda yetadi\?",
         lambda m: int(m.group(3)) // (int(m.group(2)) - int(m.group(1)))),
        (r"Bozorga ([\d ]+) kg kartoshka keltirildi\. Bu massani yuzlikkacha yaxlitlasa, necha kilogramm bo‘ladi\?",
         lambda m: _nearest(_int(m.group(1)), 100)),
        (r"Do‘kon hisobchisi ([\d ]+) so‘m va ([\d ]+) so‘mlik xarajatni yuzlikkacha chamalaydi\. Taxminan necha so‘m chiqadi\?",
         lambda m: _nearest(_int(m.group(1)), 100) + _nearest(_int(m.group(2)), 100)),
        (r"Hovlining bo‘yi (\d+) m, eni (\d+) m\. Burchagida bo‘yi (\d+) m, eni (\d+) m hovuz bor\. Hovuzdan tashqari maydon necha kvadrat metr\?",
         lambda m: int(m.group(1)) * int(m.group(2)) - int(m.group(3)) * int(m.group(4))),
        (r"([\d ]+) ta (\S+)ni (\d+) nafar bolaga teng taqsimlamoqchi\. Har biriga nechtadan to‘g‘ri keladi va nechtasi ortib qoladi\?",
         lambda m: f"{_int(m.group(1)) // int(m.group(3))} tadan, qoldiq {_int(m.group(1)) % int(m.group(3))}"),
        (r"Tortning (\d+)/(\d+) qismini opa, (\d+)/(\d+) qismini uka yedi\. Birga tortning qancha qismini yeyishdi\?",
         lambda m: Fraction(int(m.group(1)) + int(m.group(3)), int(m.group(2)))),
        (r"Har kuni sharbatning (\d+)/(\d+) qismi ichiladi\. (\d+) kunda jami qancha qismi ichiladi\?",
         lambda m: Fraction(int(m.group(1)) * int(m.group(3)), int(m.group(2)))),
        (r"Ipning uzunligi (\d+,\d+) m edi\. Undan (\d+,\d+) m kesib olindi\. Necha metr ip qoldi\?",
         lambda m: _fraction(m.group(1)) - _fraction(m.group(2))),
        (r"Birinchi dalaning bo‘yi (\d+) m, eni (\d+) m\. Ikkinchi dalaning bo‘yi (\d+) m, eni (\d+) m\. Ikki dalaning umumiy yuzi necha kvadrat metr\?",
         lambda m: int(m.group(1)) * int(m.group(2)) + int(m.group(3)) * int(m.group(4))),
    ]
    compiled = [(re.compile(pat), fn) for pat, fn in rules]
    for q in bank:
        ans = q["choices"]["ABCD".index(q["answer"])]
        for pat, fn in compiled:
            m = pat.fullmatch(q["prompt"])
            if not m:
                continue
            expected = fn(m)
            if isinstance(expected, str):
                assert ans == expected, q["id"] + " " + q["prompt"]
            elif isinstance(expected, Fraction):
                assert _fraction(ans) == expected, q["id"] + " " + q["prompt"]
            else:
                assert _int(ans) == expected, q["id"] + " " + q["prompt"]
            checked += 1
            break
    return checked
