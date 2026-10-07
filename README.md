# GMY Çıkmışlar

Ticaret Bakanlığı Gümrük Müşavir Yardımcılığı sınavının 2021–2025 soruları ve bunların tersine mühendisliği.

Gümrük Koçu - Ufuk Çetintaş

## İçerik

| Yol | İçerik |
|---|---|
| `2021…2024-gmy-sinavi-cevapli.pdf` | Sınav kitapçıkları (A). Doğru şıklar kırmızı basılmış. |
| `Gümrük_Müşavir_Yardımcılığı_A_Kitapçığı_Yanıt_Anahtarlı.pdf` | 2025 A kitapçığı, cevapları kırmızı basılmış |
| `analiz/BAKANLIK-SORU-YAZARI-ANALIZI.pdf` | Ana raporun baskıya hazır A4 PDF'i (16 sayfa) |
| `analiz/BAKANLIK-SORU-YAZARI-ANALIZI.md` | **Ana rapor:** soru yazarı neyi hedefliyor, neden böyle soruyor, çeldiricileri nasıl üretiyor, 2026–2027 için olası hamleler |
| `analiz/soru-soru/2021.md … 2025.md` | 400 gümrük sorusunun her biri için dayanak madde, yazarın hedefi, hükmün mesleki karşılığı, her çeldiricinin kaynağı, sonraki hamle; her dosyanın sonunda "yıl imzası" |
| `analiz/SONRAKI-HAMLELER.md` | Sonraki hamleler, konu gruplarına göre |
| `analiz/CEVAP-ANAHTARI.md` | 2021–2025 resmî cevap anahtarı (2025 A ve B) ve 2025 A↔B soru eşlemesi |
| `araclar/kirmizi_cevap_cikar.py` | PDF'ten soruları ve kırmızı işaretli cevapları çıkaran betik (`pdfplumber`) |
| `araclar/rapor_pdf.mjs` | Raporu Gümrük Koçu tasarımıyla PDF'e çevirir (pandoc + Playwright): `NODE_PATH=<playwright klasörü> node araclar/rapor_pdf.mjs analiz/BAKANLIK-SORU-YAZARI-ANALIZI.md analiz/BAKANLIK-SORU-YAZARI-ANALIZI.pdf` |

Mevzuat kaynakları ve soru üretimi `2027-ye-Haz-rl-k` deposundadır. O depodaki `promptlar/prompt-4-bakanlik-yazar-profili.md`, bu analizin soru üretimine aktarılmış özetidir.
