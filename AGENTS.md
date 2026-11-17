# AGENTS.md

<!-- handoff:learnings:begin -->
## Session Learnings (auto-updated by handoff)

### Implicit Rules
- Stack: Python + PyMuPDF + matplotlib; Node Playwright (global npm root) ile PDF üretimi kaynak/pdf.js ile (A4, scale 0.72)
- Build sırası (gm-analiz/kaynak içinden): python3 insights_gm_src.py; python3 assemble_gm.py; python3 build_gm.py . .. ../../analiz/kaynak; node pdf.js ../GM_Soru_Atlasi.html ../GM_Soru_Atlasi.pdf
- Kullanıcıya dönük tüm metin Türkçe
- Commit'lere attribution satırları: Co-Authored-By Claude ve Claude-Session URL
- Artifact artifact_gm.html'den yayınlanır (doctype yok; mermaid host tarafından native render edilir)
- Resmi cevap anahtarları değiştirilmez

### Key Decisions
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

<!-- handoff:learnings:end -->
