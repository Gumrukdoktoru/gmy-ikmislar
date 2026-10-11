---
workflow: general-video
flow: automation
storyboard: no
message: "GMY Soru Kampı 1/5 — Gümrük Kıymeti: 3 özgün soru, tuzaklar ve hafıza kartı"
destination: youtube
aspect: 1920x1080
language: tr
audience: "Gümrük Müşavir Yardımcılığı (GMY) sınavına hazırlanan adaylar"
voice: "ElevenLabs eleven_v4 · Cem (D1xRw7f8ZHedI7xJgfvz)"
---

## Intent

Gümrük Koçu ders kanalı için anlatımlı, görselli, şemalı ve yazılı (altyazılı) soru çözüm videosu.
Konu: Gümrük Kıymeti. GMY çıkmış sorularının dili ve kurgusuyla hazırlanmış 3 özgün soru;
oklar, şemalar ve ÖNEMLİ / DİKKAT / UYARI / TUZAK kartlarıyla çözüm.

## Assets

- assets/avatar/*.png — Gümrük Koçu avatarının 6 pozu (kullanıcının görselinden kesildi) + yarım boy yeşil fon görseli.
- assets/mix.mp3 — Cem sesiyle anlatım + yerelde sentezlenen efektler ve fon müziği.

## Customizations

- Geri sayım ("Durdur ve düşün"), soru ilerleme göstergesi, mevzuat dayanağı rozeti, hafıza kartı, skor tablosu.
- Avatar: lip-sync yerine sese tepki veren poz animasyonu (lip-sync maliyeti yüksek).

## Notes

- Soru 1: Somut olay · Hesaplama — doğru cevap B
- Soru 2: Öncüllü · Kapsam dışı — doğru cevap D
- Soru 3: Doğru-yanlış hüküm · Yöntemler — doğru cevap A
- Kaynak üretici: ../_uretici (spec/video01.json → build.py).
