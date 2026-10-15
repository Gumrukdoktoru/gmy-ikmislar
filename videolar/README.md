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

---

# GMY Konu Anlatımı: Gümrük Koçu ders serisi

GMY çıkmış sorularında en sık sorulan konulardan birer **parça** seçilerek hazırlanan 5 ders. Her ders konunun tamamını değil, sınavda tekrar tekrar sorulan tek bir dilimini anlatır.

| Ders | Konu parçası | Neden bu parça? | Süre | Mini test |
|---|---|---|---|---|
| 1 | Dahilde işlemede şartlı muafiyet sistemi | DİR soruları 2→2→4→4→7 artıyor | 6:44 | E |
| 2 | Satış bedeli yöntemi ve ilişkili kişiler | Kıymet 31 soruyla 2. sırada | 6:14 | D |
| 3 | Tebliğ, ödeme ve itiraz süreleri | Her sınavda var, 2024'te 5 soru | 5:44 | B |
| 4 | Gümrük müşavirlerinin disiplin cezaları | Müşavirlik 35 soruyla 1. sırada | 6:24 | A |
| 5 | Kaçakçılık suçları ve ceza aralıkları (5607 md. 3) | 27 kaçakçılık sorusunun 8'i md. 3 | 8:04 | C |

- Videolar: `gmy-ders-0N/renders/gmy-ders-0N-teslim.mp4` (1920×1080, 30 fps, H.264 + AAC)
- Ders metinleri, şemalar ve mini test: `_uretici/spec/ders0N.json`

## Her derste

- Cem'in sesiyle anlatım (ElevenLabs Eleven v4), Gümrük Koçu öğretmen avatarı
- "Neden bu konu?" açılışı: yıllara göre soru sayısı grafiği ve ders gündemi
- 5 bölüm; her bölümde bir şema: oklu akış, dal, karşılaştırma tablosu, sütunlar, zaman çizelgesi veya kelime kelime vurgulanan kanun metni kartı ("Sade dille" özetiyle)
- ÖNEMLİ / DİKKAT / UYARI / TUZAK / İPUCU kutuları; tuzaklar gerçek sınav çeldiricilerine dayanır
- Üst çubukta bölüm ilerlemesi, alt yazı, ses efektleri ve fon müziği
- Mini test: 5 saniyelik "DÜŞÜN" sayacı, cevap ve çözüm tahtası
- "Akılda Kalsın" hafıza kartı

## Yeniden üretim

```bash
cd videolar/_uretici
python3 ders.py plan 01     # spec/ders01.json -> audio/d01/segments.json (karakter sayısı = Eleven v4 kredisi)
# segments.json içindeki her metin ElevenLabs'te (eleven_v4, Cem) seslendirilip audio/d01/<id>.mp3 olarak kaydedilir
python3 ders.py words 01    # yerel Whisper ile kelime zamanları
python3 ders.py build 01    # ../gmy-ders-01/index.html + assets
cd ../gmy-ders-01 && npx hyperframes lint && npx hyperframes render . -o renders/gmy-ders-01-teslim.mp4 --crf 26
```
