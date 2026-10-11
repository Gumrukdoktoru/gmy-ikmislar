# GMY Soru Kampı: Gümrük Koçu video serisi

GMY çıkmış soruları incelenerek yazılmış 15 yeni sorunun 5 videoda (her videoda 3 soru) anlatımı.

| Video | Konu | Süre | Cevaplar |
|---|---|---|---|
| 1 | Gümrük Kıymeti | 5:38 | B · D · A |
| 2 | Menşe ve Serbest Dolaşım | 5:38 | C · E · B |
| 3 | Dahilde İşleme ve Geçici İthalat | 5:14 | D · A · C |
| 4 | Transit, Antrepo ve Geri Gelen Eşya | 5:54 | E · B · C |
| 5 | Yaptırımlar: Cezalar ve Kaçakçılık | 5:30 | A · E · D |

- Videolar: `gmy-kamp-0N/renders/gmy-kamp-0N-teslim.mp4` (1920×1080, 30 fps, H.264 + AAC)
- Sorular, doğru cevaplar ve gerekçeler: [`SORULAR.md`](SORULAR.md)

## Her videoda

- Cem'in sesiyle anlatım (ElevenLabs Eleven v4), Gümrük Koçu avatarı (6 poz, konuşmaya göre hareket)
- Soru kartı: kökte vurgulanan anahtar ifade, öncüller ve şıklar, 5 saniyelik "DÜŞÜN" sayacı, doğru cevap damgası
- Çözüm tahtası: oklu akış, dal, iki/üç sütun, formül ve zaman çizelgesi şemaları, mevzuat dayanağı etiketi
- TUZAK / DİKKAT / UYARI / ÖNEMLİ kutuları, ses efektleri, alt yazı, "Akılda Kalsın" hafıza kartı ve skor tablosu

## Yeniden üretim (`_uretici/`)

```bash
cd videolar/_uretici
python3 build.py plan 01            # spec/video01.json -> audio/v01/segments.json
# segments.json içindeki her metin ElevenLabs'te (eleven_v4, Cem) seslendirilir,
# fetch_tts.py ile audio/v01/<segment>.mp3 olarak indirilir
python3 build.py words 01           # yerel Whisper ile kelime zamanları
python3 build.py build 01           # ../gmy-kamp-01/index.html + assets
cd ../gmy-kamp-01 && npx hyperframes lint && npx hyperframes render . --crf 26
```

Soru metinleri `spec/video0N.json` dosyalarındadır. Metin değişirse yalnız değişen segmentin sesi yeniden üretilir.
