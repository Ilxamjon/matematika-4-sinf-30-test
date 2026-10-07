# Informatika · 30 savol

M. Usmanovning «Informatikadan mavzulashtirilgan testlar to‘plami» (Navro‘z, 2018) asosida.

1560 ta savol, har urinishda tasodifiy 30 ta takrorlanmaydigan savol, radio orqali javob tanlash, yakunda natija va kitob kaliti bo‘yicha to‘g‘ri javoblar. Sahifa yangilanganda shu brauzerdagi test saqlanadi. Sinf tarmog‘ida natijalar o‘qituvchi kompyuteriga yig‘iladi.

Onlayn: https://ilxamjon.github.io/informatika-30-test/

## Ishga tushirish

Bitta kompyuterda, internetsiz: `1_TESTNI_OCHISH.cmd` yoki `Informatika-30-test.html`.

Sinfdagi boshqa kompyuterlar bilan: o‘qituvchi kompyuterida `3_LOKAL_TARMOQ.cmd` ni ishga tushiring. Windows bir marta ruxsat so‘raydi. Oyna ochiq tursin. O‘quvchilar o‘z kompyuteridagi brauzerga shu oynadagi manzilni yozadi, masalan `http://192.168.1.20:8787/`. Hammasi bir xil Wi-Fi yoki lokal tarmoqda bo‘lsin. Natijalar o‘qituvchi kompyuteridagi brauzerda (`http://127.0.0.1:8787/oqituvchi`) va `natijalar` papkasida saqlanadi. Python, Node.js va internet shart emas.

`sayt/index.html` ni to‘g‘ridan-to‘g‘ri ochish ham mumkin: bu holda natija faqat shu brauzerda qoladi. Fayllar va `questions` papkasi birga saqlansin.

## Manba va qamrov

Yuklangan PDF 311 sahifadan iborat. Savollar PDF 1–282-sahifalardan, kalit PDF 283–302-sahifalardan ajratilgan. PDF sahifa raqami bosma kitob raqamidan farq qiladi. Sahifalar skan bo‘lgani uchun savollar rasm ko‘rinishida beriladi. Original variant harflari o‘zgartirilmagan; savollar tartibi aralashtiriladi.

Bazadagi har bir ID `paragraf-savol` ko‘rinishida. Javob raqam ustuni ostidagi kalit belgisiga koordinatalar bo‘yicha moslangan. Chegarasi, barcha A–D variantlari yoki kaliti ishonchli avtomatik ajratilmagan savollar kiritilmagan. Bu to‘liq kitob raqamlashtirilgani degani emas. Kitobdagi ilmiy yoki bosma xatolar mustaqil ravishda tuzatilmagan; natija «kitob kaliti bo‘yicha» beriladi. Eski dastur versiyalari haqidagi savollar tarixiy kontekstda olinadi.

Asl PDF: Usmonov-Informatika-2018.pdf. `bank.json` va `bank.js` bir xil bankni saqlaydi; interfeys `bank.js` dan foydalanadi.

## Cheklovlar

Bitta fayl yoki onlayn sahifa ochilganda javoblar sahifa manbasida mavjud. Lokal tarmoq rejimida kalit o‘quvchi kompyuteriga yuborilmaydi: ball o‘qituvchi kompyuterida hisoblanadi va faqat test yakunida ko‘rsatiladi. Bu baribir nazorat imtihoni uchun himoyalangan server o‘rnini bosmaydi. LocalStorage ishlamasa joriy sahifa yopilganda jarayon saqlanmaydi. Alohida mavzuda 30 tadan kam savol bo‘lsa, shu mavzudagi barcha savollar beriladi. 53-§ va 91-§ da ajratilgan savol yo‘q.


## Ushbu yuklab olinadigan paket

Kundalik foydalanish uchun `1_TESTNI_OCHISH.cmd` yoki `Informatika-30-test.html` ni oching.
Sinf tarmog‘i uchun `3_LOKAL_TARMOQ.cmd` ni o‘qituvchi kompyuterida oching.
Saytni tahrirlash uchun `sayt/` papkasidagi HTML/CSS/JS fayllaridan foydalaning.
Savollarni `sayt/bank.json` da tahrirlang; tasvirlarni `sayt/questions/` da saqlang.
So‘ng Python 3 bilan `python qayta_yigish.py` ni ishga tushiring.
Bu bank.js va offline HTML nusxasini bir xil holatga keltiradi.
Oddiy foydalanish uchun Python kerak emas.
