# Kaynak dosyalar

Analizi yeniden üretmek için bu klasörde, sırasıyla:

```bash
pip install pymupdf matplotlib
python3 extract.py                      # PDF'lerden satırları ve kırmızı işaretli cevapları çıkarır (lines_<yıl>.json)
python3 parse.py                        # 5 × 100 soruyu ve doğru cevapları ayrıştırır (questions.json)
python3 kokcheck.py 2021 2022 2023 2024 2025   # soru kalıbı sınıflandırmasını metin kalıbıyla çapraz kontrol eder
python3 make_insights.py                # yıl yorumları, tekrar eden kalıplar ve sonuç metinleri (insights.json)
python3 build.py . ..                   # CSV/JSON, grafikler, README.md ve GMY_Soru_Atlasi.html
```

- `TAKSONOMI.md`: konu, soru kalıbı, soru tipi ve mevzuat kodlarının tanımları.
- `cls_<yıl>.json`: her yılın 100 sorusunun sınıflandırması (konu, alt konu, kalıp, tip, mevzuat, zorluk, özet, öğrenilecek bilgi).
- `labels.py`: kodların Türkçe adları ve gümrük konu grupları.
- `template.html`: etkileşimli raporun şablonu.
