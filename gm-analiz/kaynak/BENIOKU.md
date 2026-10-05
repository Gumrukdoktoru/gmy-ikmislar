# Kaynak dosyalar

Analizi yeniden üretmek için bu klasörde, sırasıyla:

```bash
pip install pymupdf matplotlib
# GM sınav PDF'lerini (gumrukdoktoru/gmcikmislar) 2021.pdf … 2025.pdf adlarıyla bir klasöre koyun
python3 extract.py <pdf_klasörü>        # satırları ve kırmızı işaretli cevapları çıkarır (lines_<yıl>.json)
python3 parse.py                        # 5 × 100 soruyu ve doğru cevapları ayrıştırır (questions.json)
python3 kokcheck_gm.py 2021 2022 2023 2024 2025   # soru kalıbı sınıflandırmasını metin kalıbıyla çapraz kontrol eder
python3 insights_gm_src.py              # yıl yorumları, tarife/hesap notları, tekrar eden kalıplar ve sonuç (insights_gm.json)
python3 assemble_gm.py                  # gm_body.html ve gm_app.js'i template_gm.html'e yerleştirir
python3 build_gm.py . .. ../../analiz/kaynak   # CSV/JSON, grafikler, README.md ve GM_Soru_Atlasi.html (+ GMY karşılaştırması)
node pdf.js ../GM_Soru_Atlasi.html ../GM_Soru_Atlasi.pdf   # A4 PDF (Playwright gerekir)
```

- `TAKSONOMI_GM.md`: konu, soru kalıbı, soru tipi, mevzuat, hesap ve zorluk kodlarının tanımları.
- `cls_<yıl>.json`: her yılın 100 sorusunun sınıflandırması (konu, alt konu, kalıp, tip, mevzuat, madde, zorluk, hesap türü, fasıllar, sayısal değer, özet, öğrenilecek bilgi).
- `labels_gm.py`: kodların Türkçe adları, 8 konu grubu ve TGTC bölümleri.
- `tekrar_gm.py`: yıllar arasında tekrar eden soru kalıpları.
- `apply_rev.py`: bağımsız ikinci kontrolde önerilen düzeltmeleri, eski değer eşleşmesini doğrulayarak uygular.
- `template_gm.html`, `gm_body.html`, `gm_app.js`: etkileşimli raporun şablonu.
- 2022 dosyası B kitapçığıdır; soru numaraları o kitapçığa göredir.
