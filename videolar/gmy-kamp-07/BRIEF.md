---
workflow: general-video
flow: automation
storyboard: no
message: "GMY Soru Kampı 7/7 — Gümrük Yükümlülüğü ve Geri Verme: 3 özgün soru, tuzaklar ve hafıza kartı"
destination: youtube
aspect: 1920x1080
language: tr
audience: "Gümrük Müşavir Yardımcılığı (GMY) sınavına hazırlanan adaylar"
voice: "ElevenLabs eleven_v4 · Cem (D1xRw7f8ZHedI7xJgfvz)"
---

## Intent

Gümrük Koçu ders kanalı için anlatımlı, görselli, şemalı ve yazılı (altyazılı) soru çözüm videosu.
Konu: Gümrük Yükümlülüğü ve Geri Verme. GMY çıkmış sorularının dili ve kurgusuyla hazırlanmış 3 özgün soru;
oklar, şemalar ve ÖNEMLİ / DİKKAT / UYARI / TUZAK kartlarıyla çözüm.

## Assets

- assets/avatar/*.png — Gümrük Koçu avatarının 6 pozu (kullanıcının görselinden kesildi) + yarım boy yeşil fon görseli.
- assets/mix.mp3 — Cem sesiyle anlatım + yerelde sentezlenen efektler ve fon müziği.

## Customizations

- Geri sayım ("Durdur ve düşün"), soru ilerleme göstergesi, mevzuat dayanağı rozeti, hafıza kartı, skor tablosu.
- Avatar: lip-sync yerine sese tepki veren poz animasyonu (lip-sync maliyeti yüksek).

## Notes

- Soru 1: Eşleştirme · Tarih — doğru cevap B
- Soru 2: Somut olay · Kusurlu eşya — doğru cevap D
- Soru 3: Öncüllü · Geri verme — doğru cevap A
- Kaynak üretici: ../_uretici (spec/video07.json → build.py).
