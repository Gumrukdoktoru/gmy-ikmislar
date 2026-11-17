---
date: 2026-11-17T11:21:49.723Z
project: gmy-ikmislar
session: eb137516
schema_version: 1
next_steps_count: 4
has_blockers: true
keywords: gm atlas, gm-analiz, gmy-analiz, 2026 b kitapcik, gm soru atlasi, gm gmy karsilastirma, insights_gm_src, tekrar_gm, build_gm, gm_app.js
headline: GM (Gümrük Müşavirliği) + GMY (Gümrük Müşavir Yardımcılığı) sınav soru atlası, repo Gumrukdoktoru/gmy-ikmislar, branch c
---

# Session Handoff Snapshot
> **Generated:** 11/17/2026, 11:21:49 AM

## 🎯 High-Level Objective
* **Goal:** GM (Gümrük Müşavirliği) + GMY (Gümrük Müşavir Yardımcılığı) sınav soru atlası, repo Gumrukdoktoru/gmy-ikmislar, branch claude/elegant-mendel-b4rb61. Hedef: yıl bazlı + yıllar arası analiz; konu ve soru tipi; grafikler; HTML/PDF/README; sınav hazırlığı. Tamam: GMY 2021-2025 (analiz/), GM 2021-2025 (gm-analiz/), bu oturumda GM 2026 eklendi (B kitapçık, 15 Kasım 2026) → GM atlası 2021-2026, 600 soru. Commit 0700380 pushed.

## 📌 Current State & Next Steps
* **Status:** Tamamlandı. Kalan sadece isteğe bağlı takip işleri. GMY 2026 verisi yok → GM-GMY karşılaştırması 2021-2025 ortak yıllarla sınırlı.
* **Blocker:** ["GMY 2026 verisi yok — GM-GMY karşılaştırması 2021-2025 ile sınırlı", "Tartışmalı cevap anahtarları (2026/37-38, 2026/43, 2026/88; 2022/94, 2023/72-73, 2025/12, 2025/16, 2021/4) resmi kaynakla doğrulanmadan değiştirilemez"]
* **Next Action:** Kullanıcı geri bildirimini bekle

### Remaining Queue
- [ ] GMY 2026 PDF gelirse analiz/ altına ekle; GM-GMY karşılaştırması otomatik genişler
- [ ] Kullanıcıya GM 2026 PDF'ini gmcikmislar reposuna koymasını öner
- [ ] Branch'i main'e birleştirmek için PR yalnızca kullanıcı istediğinde aç

## 🛠️ Modified Files Delta
* gm-analiz/kaynak/extract.py: yıl otomatik algılama {yıl}.pdf
* gm-analiz/kaynak/parse.py: yıl otomatik algılama lines_{yıl}.json + sıra sayı regex
* gm-analiz/kaynak/labels_gm.py: YEARS 2021-2026, B_KITAPCIK={2022,2026}
* gm-analiz/kaynak/build_gm.py: DATA.meta, yarı-bölme trend, ortak yıl GMY karşılaştırması, dinamik başlık/README
* gm-analiz/kaynak/gm_app.js: DATA.meta kullanır; dinamik trend ve paydalar
* gm-analiz/kaynak/gm_body.html + template_gm.html: 2021-2026 / 600 soru metinleri
* gm-analiz/kaynak/insights_gm_src.py: altı yıl ifadesi, 2026 maddeleri, poss() yardımcı, dinamik tarife istatistikleri
* gm-analiz/kaynak/insights_gm.json: yeniden üretildi
* gm-analiz/kaynak/tekrar_gm.py: 2026 sayıları + 9 yeni satır
* gm-analiz/kaynak/cls_2026.json: yeni
* gm-analiz/kaynak/BENIOKU.md: güncellendi
* gm-analiz/README.md: güncellendi
* gm-analiz/GM_Soru_Atlasi.html ve .pdf: yeniden üretildi (29 sayfa)
* gm-analiz/gm_soru_siniflandirma.csv/json: 2026 eklendi
* gm-analiz/grafikler/: 2026_*.png eklendi

## 🚫 Failed Approaches (DO NOT RETRY)
* Approach: python3 -I ile pymupdf import → Result: ModuleNotFoundError (kütüphane kullanıcı site dizininde) → Lesson: scriptleri düz python3 ile ayrı bir scripts dizininden çalıştır
* Approach: çalışma dizini scratchpad'de tutmak → Result: oturum yeniden başlatmada silindi → Lesson: kaynakları repodaki gm-analiz/kaynak içinde tut; her şey oradan yeniden üretilebilir
* Approach: orijinal SHARED regex → Result: "39 ve 40 ncı soruları" kaçtı, ortak kök Q38'e eklendi → Lesson: regex'e Türkçe sıra sayı ekleri eklendi; ortak kökleri her zaman incele
* Approach: gm_app.js/build_gm.py içinde "/5" yıl paydası sabit → Result: sayfada "6/5" göründü → Lesson: len(YEARS) kullan
* Approach: eski insight metninde "beş yılın en …" üstünlük ifadeleri → Result: 2026 verisiyle yanlış oldu → Lesson: yıl eklenince her üstünlük ifadesini yeniden doğrula

## 🔑 Crucial Context & Implicit Rules
* Stack: Python + PyMuPDF + matplotlib; Node Playwright (global npm root) ile PDF üretimi kaynak/pdf.js ile (A4, scale 0.72)
* Build sırası (gm-analiz/kaynak içinden): python3 insights_gm_src.py; python3 assemble_gm.py; python3 build_gm.py . .. ../../analiz/kaynak; node pdf.js ../GM_Soru_Atlasi.html ../GM_Soru_Atlasi.pdf
* Kullanıcıya dönük tüm metin Türkçe
* Commit'lere attribution satırları: Co-Authored-By Claude ve Claude-Session URL
* Artifact artifact_gm.html'den yayınlanır (doctype yok; mermaid host tarafından native render edilir)
* Resmi cevap anahtarları değiştirilmez

## Key Decisions
- Decision: cevaplar kırmızı metin span'larından okunur (PyMuPDF) — Reason: güvenilir, her soruda tek kırmızı şık doğrulandı
- Decision: extract.py/parse.py yılları {yıl}.pdf / lines_{yıl}.json dosyalarından otomatik algılar — Reason: gelecek yıllarda kod değişikliği gerekmez
- Decision: ortak-kök regex Türkçe sıra sayı ekine izin verir ("40 ncı soruları") — Reason: 39 ve 40 soruları ayrışsın
- Decision: labels_gm.py YEARS=2021..2026, B_KITAPCIK={2022,2026} — Reason: B kitapçık sıra farkı
- Decision: trend = ilk yarı yıllar ortalaması vs son yarı (2021-23 → 2024-26) — Reason: 6 yıl için dengeli karşılaştırma
- Decision: GM-GMY karşılaştırması ortak yıllar 2021-2025 ile sınırlı — Reason: GMY 2026 verisi yok
- Decision: build_gm.py DATA.meta (n,y0,y1,b,early,late,cmp) geçirir; gm_app.js yıl sabiti içermez — Reason: hardcode yıl hataları önlenir
- Decision: insights_gm_src.py tüm sayıları veriden hesaplar; poss() yardımcı fonksiyonu Türkçe iyelik ekleri (39'u, 13'ü) için — Reason: sayılar elle girilmesin
- Decision: tekrar_gm.py 38 tekrarlayan kalıp — Reason: yıllar arası tekrar analizi
- Decision: resmi cevap anahtarları asla değiştirilmez; tartışmalı olanlar sadece belgelenir (2026/37-38, 2026/43, 2026/88; 2022/94, 2023/72-73, 2025/12, 2025/16, 2021/4) — Reason: resmi kaynak esas
- Decision: HTML/PDF'te metodoloji bölümü ve soru listesi yok — Reason: kullanıcı talebi

## 🙋 User Contribution (human-authored)
GM 2026 B kitapçık PDF'ini yükledi; metodoloji ve soru listesi istemedi; 2026'yı atlasa eklemeyi istedi.

## 🙋 User Decisions (made by the human)
- **GM atlası için ayrı GM sınavını kullan (GMY gümrük bölümü değil)**
  - Reason: Kullanıcı tercihi
- **HTML/PDF'ten metodoloji bölümü ve soru listelerini çıkar**
  - Reason: Kullanıcı talebi
- **2026'yı atlasa ekle — kullanıcı PDF yükleyerek**
  - Reason: Kullanıcı talebi

## Summary
GM 2026 PDF kullanıcı tarafından yüklendi; 100 soru + kırmızı işaretli cevaplar çıkarıldı (PyMuPDF, kırmızı span #ff0000/#ee0000; her soruda tek kırmızı şık doğrulandı). Mevcut taksonomi ile sınıflandırıldı (2 paralel ajan + bağımsız reviewer, 9 düzeltme). Pipeline 6 yıla genelleştirildi; insights yeniden yazıldı; HTML/PDF 29 sayfa. Artifact https://claude.ai/artifact/VRFQZgHLUv6SLKgFqksMkb v2'ye güncellendi. PDF kullanıcıya gönderildi. Türkçe özet verildi.

---
*A short hint surfaces on session start; full context loads only if your next prompt matches a keyword above, or via manual `/handoff-resume`. The same record is available as a sibling `.json` file for external tools.*