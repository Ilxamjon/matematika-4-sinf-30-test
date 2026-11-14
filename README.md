# Matematika · 4-sinf · 30 savol

I. V. Repyovaning «Matematika. 4-sinf» darsligi (I–IV qism, «Novda Edutainment», 2023) mavzulariga mos test.

2229 ta savol: 508 tasi matnli masala, 255 tasi rasmli. Har urinishda tasodifiy 30 ta takrorlanmaydigan savol. Mavzu bo‘yicha ham mashq qilish mumkin. Javob tugma orqali tanlanadi, yakunda natija va to‘g‘ri javoblar ko‘rsatiladi. Sahifa yangilanganda shu brauzerdagi test saqlanadi. Sinf tarmog‘ida natijalar o‘qituvchi kompyuteriga yig‘iladi.

## Ishga tushirish

Bitta kompyuterda, internetsiz: `1_TESTNI_OCHISH.cmd` yoki `Matematika-4-sinf-30-test.html`.

Sinfdagi boshqa kompyuterlar bilan: o‘qituvchi kompyuterida `3_LOKAL_TARMOQ.cmd` ni ishga tushiring. Windows bir marta ruxsat so‘raydi. Oyna ochiq tursin. O‘quvchilar o‘z kompyuteridagi brauzerga shu oynadagi manzilni yozadi, masalan `http://192.168.1.20:8787/`. Hammasi bir xil Wi-Fi yoki lokal tarmoqda bo‘lsin. Natijalar o‘qituvchi kompyuteridagi brauzerda (`http://127.0.0.1:8787/oqituvchi`) va `natijalar` papkasida saqlanadi. Python, Node.js va internet shart emas.

`sayt/index.html` ni to‘g‘ridan-to‘g‘ri ochish ham mumkin: bu holda natija faqat shu brauzerda qoladi.

## Manba

Savollar to‘rt qismli darslikning 29 ta mavzu guruhiga moslab tuzilgan. Darslikdagi mashqlar ko‘chirilmagan: har bir savol shu test uchun yozilgan, javobi `tuzish.py` ichida hisoblab tekshirilgan.

`sayt/bank.json` va `sayt/bank.js` bir xil bankni saqlaydi. Interfeys `bank.js` dan foydalanadi. Matnli masalalar `masalalar.py` da, rasmli savollar `rasmlar.py` da tuziladi. Rasmlar `sayt/questions/` papkasiga yoziladi.

## Cheklovlar

Bitta fayl yoki onlayn sahifa ochilganda javoblar sahifa manbasida mavjud. Lokal tarmoq rejimida kalit o‘quvchi kompyuteriga yuborilmaydi: ball o‘qituvchi kompyuterida hisoblanadi va faqat test yakunida ko‘rsatiladi. Bu baribir nazorat imtihoni uchun himoyalangan server o‘rnini bosmaydi. LocalStorage ishlamasa joriy sahifa yopilganda jarayon saqlanmaydi. Alohida mavzuda 30 tadan kam savol bo‘lsa, shu mavzudagi barcha savollar beriladi.

## Tahrirlash

Savollarni qayta tuzish: `python tuzish.py`

Saytni yig‘ish: `python qayta_yigish.py`

Bu `sayt/bank.js` va `Matematika-4-sinf-30-test.html` offline nusxasini yangilaydi. Oddiy foydalanish uchun Python kerak emas.
