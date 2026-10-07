# Bakanlık Soru Yazarının Zihni

## GMY 2021–2025: 400 gümrük sorusunun tersine mühendisliği

**Gümrük Koçu - Ufuk Çetintaş** · Ekim 2026

> Bu rapor çıkmış soruları "ne sordu" diye okumaz. Her soruyu şu iki soruyla okur: "Yazar bunu neden sordu, adayı nerede yakalamak istedi?" Dayanak beş sınavın 500 sorusu ve resmî cevaplarıdır. 400 gümrük sorusunun her biri tek tek mevzuat metniyle eşlendi. Soru soru çözümlemeler `soru-soru/` klasöründe.

---

## 0. Kısa cevap

Bakanlığın soru yazarı, adayın gümrük mevzuatını yorumlayıp yorumlayamadığını ölçmüyor. Ölçtüğü şu: **Aday mevzuatın lafzını, komşu hükümle karıştırmadan, kelimesi kelimesine biliyor mu?**

- **Lafız:** 400 sorunun 275'inde (%69) kilit cümle madde metninin birebir kopyası. Çıkarım gerektiren soru yalnızca 49 (%12).
- **Komşu hüküm:** Yanlış şıklar çoğunlukla uydurma değil. Aynı maddenin yan fıkrasından ya da komşu rejimden taşınmış **gerçek hükümler**. Her yıl en sık kullanılan tuzak bu: 165 soru (%41).
- **Karıştırma:** Yazar adayı bilgisizlikten değil, karıştırmaktan eliyor. Karıştırılan çiftler şunlar:
  - 15 gün ↔ 30 gün,
  - iki kat ↔ dört kat,
  - şartlı muafiyet ↔ geri ödeme,
  - gümrük statüsü ↔ menşe,
  - gümrük müdürlüğü ↔ bölge müdürlüğü.

Bu temel ölçünün üstüne üç amaç ekleniyor:

1. Aday kendi mesleğinin kurallarını bilmeli: gümrük müşaviri, yardımcısı, YGM ve disiplin.
2. Aday güncel tutarları ve değişiklikleri izlemeli.
3. Aday bir vakada saklanan istisnayı görebilmeli. Bu amaç 2022'den beri belirginleşiyor.

### Neden böyle soruyorlar?

Bu tercihlerin arkasında yazarın dört zorunluluğu var:

1. **Savunulabilirlik.** Her soru itiraza dayanmalı. Metinden birebir alınan cümle tartışılmaz. Veri bunu doğruluyor: birebir sorularda kusur ya da tartışma oranı %3, parafrazda %7, çıkarımda %10.
2. **Ayırt edicilik.** 80 soruyla binlerce adayı sıralamak gerekiyor. "Bilen ile yaklaşık bilen" ayrımını en keskin biçimde sayı, terim ve liste sınırı yapıyor.
3. **Üretim ekonomisi.** Her modülü bir uzman yazıyor. Dört doğru madde cümlesi ve tek kelimesi değiştirilmiş beşinci cümle, en hızlı üretilen ve en az riskli soru tipi.
4. **Mesleki uygunluk.** Sınav, yardımcının sahada ceza yemeden iş görmesi için gereken bilgiyi ölçüyor: süre, makam, kıymet unsuru, ceza katı, kendi yetkisinin sınırı.

---

## 1. Veri ve yöntem

- **Sınavlar.** 2021'i ASYM (Ankara Üniversitesi), 2022–2025'i Hacettepe Üniversitesi Yaşam Boyu Öğrenme Merkezi hazırladı. Her sınav 100 soru ve 150 dakika. 1–20 genel kültür, 21–100 gümrük mevzuatı.
- **Resmî cevaplar.**
  - PDF'lerde doğru şıklar kırmızı basılmış. Renk bilgisi karakter düzeyinde okundu ve 500 sorunun 500'ünde tek kırmızı şık bulundu.
  - 2025'te A kitapçığının (yanıt anahtarlı) cevapları, soru ve şık metinleri eşleştirilerek B kitapçığına aktarıldı. Bkz. `CEVAP-ANAHTARI.md`.
  - Eski envanterde türetilen cevaplar 2021–2024'te 7 soruda resmî anahtardan farklı çıktı. 2025'in 80 cevabı envanterde hiç yoktu. Bkz. Bölüm 12.
- **Çözümleme.** Her gümrük sorusu için şu bilgiler tespit edildi:
  - dayanak madde,
  - yazarın hedefi (tek cümle),
  - hükmün müşavirlik pratiğindeki karşılığı,
  - doğru cevabın metinle ilişkisi,
  - her yanlış şıkkın metindeki "gerçek yuvası",
  - yazarın aynı hükümden sonraki olası hamlesi.
- **Sabit kodlar.** Düzey, format, tuzak ve metne yakınlık için sabit kodlar kullanıldı. Bir soruya birden fazla kod verilebildi:
  - **Düzey:** HATIRLAMA, TANIMA, AYIRT, UYGULAMA, BÜTÜNLEŞİK.
  - **Tuzak:** SAYI, YAKIN-SAYI, BAŞLANGIÇ (sürenin başlangıç anı), MAKAM, TERİM, KOMŞU (komşu fıkra/rejim), TERSİNE (olumsuzlama), MUTLAK, UNSUR (tanımdan unsur düşürme/ekleme), LİSTE-DIŞI, İSTİSNA, ŞART, AD-HESAP, SAĞDUYU (mantıklı görünen ama mevzuatta olmayan).
  - **Yakınlık:** BİREBİR, PARAFRAZ, ÇIKARIM.
- **Numaralama.** 2025 soru numaraları **B kitapçığına** göredir. A karşılıkları soru soru dosyasında ve cevap anahtarında.

### Beş yılın kod toplamları (400 soru)

| Düzey | Sayı | | Tuzak | Sayı | | Format | Sayı |
|---|---|---|---|---|---|---|---|
| HATIRLAMA | 178 | | KOMŞU | 165 | | KLASİK | 157 |
| AYIRT | 140 | | SAYI | 103 | | OLUMSUZ KÖK | 153 |
| TANIMA | 87 | | TERİM | 85 | | ÖNCÜLLÜ | 39 |
| UYGULAMA | 26 | | LİSTE-DIŞI | 74 | | TANIM-ADI | 34 |
| BÜTÜNLEŞİK | 23 | | TERSİNE | 52 | | VAKA | 16 |
| | | | SAĞDUYU | 40 | | BOŞLUK | 12 |
| | | | YAKIN-SAYI | 38 | | HESAP | 7 |
| | | | MAKAM | 29 | | EŞLEŞTİRME | 3 |
| | | | UNSUR | 25 | | | |
| | | | BAŞLANGIÇ | 16 | | | |

Metne yakınlık: birebir 275, parafraz 68, çıkarım 49. Kaynak metinde karşılığı bulunamayan soru 8.

---

## 2. Yazarın masası: bir soru nasıl doğuyor?

Beş yılın örüntüsünden yazarın iş akışı şöyle okunuyor:

### Adım 1: Modülü alır

Kitapçıklar konu bloklarıyla dizilmiş:

- **2022:** 21–27 kaçakçılık, 44–55 kıymet, 83–86 muafiyet, 89–91 geri verme.
- **2024:** 21–28 kıymet, 29–42 menşe/TPÖ, 56–61 transit/TIR, 87–91 disiplin/YGM.
- **2025 (A kitapçığı):** 21–47 kıymet–menşe–BTB–İthalat Rejimi Kararı, 54–60 DİR, 61–64 transit, 76–78 kaçakçılık, 79–85 geçici ithalat, 86–89 YYS/OKSB, 90–100 tahsilat ve müşavirlik.

Bloklar arasındaki üslup farkı belirgin. 2025 kıymet bloğunda vaka ve hesap var, menşe bloğunda liste, DİR bloğunda tanım üçlemesi. Bu, soruları farklı uzmanların modül modül yazdığını düşündürüyor. B kitapçığı aynı soruları karıştırarak diziyor.

**Sonuç:** Bir modülün yazarı değiştiğinde o konunun ağırlığı da değişiyor. Menşe ve TPÖ grubunun yıllara göre soru sayısı 0 → 1 → 4 → 12 → 11.

### Adım 2: Maddeyi açar, "karışabilecek" noktayı arar

Yazar maddenin en önemli hükmünü değil, **benzeriyle karışabilecek** hükmünü seçiyor:

- iki süre içeren fıkra (GK 46: denizyolu 45, diğer yollar 20 gün),
- iki sistemli rejim (DİR: şartlı muafiyet / geri ödeme),
- birbirine benzeyen iki liste (şartlı muafiyet düzenlemesi / ekonomik etkili rejimler),
- basamaklı yaptırım (GK 241: 2-4-6-8 kat).

### Adım 3: Doğru cevabı metinden keser

Kök ya da doğru şık çoğunlukla madde cümlesinin kendisi. Bu, 400 sorunun 275'inde böyle.

### Adım 4: Çeldiriciyi aynı rafta arar

Yazar çeldirici için şu sırayla bakıyor:

1. Aynı maddenin diğer fıkrası.
2. Komşu rejimin benzer hükmü.
3. Aynı mevzuatın sayı havuzu.
4. En son çare olarak uydurma.

Uydurma çeldiriciler ("siyah hat", "heykel", "yeminli gümrük müşaviri", "tasdik raporu") en zayıf soruların izi.

### Adım 5: Yönü seçer

Yazar dört kalıptan birini kullanıyor:

- **Tek kelime değişikliği:** Dört doğru madde cümlesi ve tek kelimesi bozulmuş beşinci cümle. Kök "yanlıştır".
- **Liste dışı unsur:** Kapalı listeye akla yatkın bir yabancı eklenir. Kök "değildir / yer almaz".
- **Tanımdan ad:** Tanım verilir, adı sorulur. Kök "ne ad verilir / hangisidir".
- **Vaka:** Bir vaka verilir, vakanın içinde bir istisna saklanır.

### Yazarın iç sesi

Aşağıdaki iç ses, beş yılın verisine dayanan bir canlandırmadır.

> "Önümde GK 46 var. Adayların çoğu 45 günü bilir. Ben 45'i sormam; 45 ile 20'nin **hangi taşıma türüne** ait olduğunu sorarım. Havayolu, demiryolu, karayolu için ayrı süreler varmış gibi şık kurarım (2022-32).
>
> Doğru cevabı metinden aynen alırım, çünkü itiraz gelirse savunacağım cümle Kanunun cümlesi olsun. Çeldiriciyi uydurmam; aynı maddenin öbür fıkrasından alırım. Böylece yanlış şık 'yanlış bilgi' değil, 'yanlış yerde duran doğru bilgi' olur.
>
> Bir hüküm seçtiysem, aynı sınavda tersinden bir daha sorarım (2022-33 ↔ 2022-62). Mantıklı görünen ama listede olmayan bir kurum, bir belge, bir şart eklerim: özel güvenlik görevlisi, kefalet, 'kıymet' bilgisi. Mevzuatı sağduyuyla çözmeye çalışan aday orada düşer.
>
> Bu adaylar müşavir yardımcısı olacak. Kendi yetkisini, yasaklarını ve hangi hatanın kaç kat ceza getirdiğini bilmesini isterim. Sınav yılının usulsüzlük cezası tutarını da sorarım; güncel mevzuatı izleyeni ayırırım."

---

## 3. Yazarın sekiz hedefi

### H1. Lafız: Metni kelimesi kelimesine bilmek

- **Kanıt.**
  - 275 birebir soru.
  - Yaklaşık **68 soruda** (%17) doğru cevap, madde cümlesinin tek kelimesi değiştirilerek üretilmiş. Yıllara göre: 2021'de 19, 2022'de 12, 2023'te 10, 2024'te yaklaşık 15, 2025'te 12.
- **Tek kelime değişikliği örnekleri:**

| Soru | Metindeki ifade | Sorudaki ifade |
|---|---|---|
| 2021-24 | süre "yılın **sonundan**" başlar | "yılın **başından**" |
| 2021-33 | gümrük **gözetimi** | gümrük **kontrolü** |
| 2021-58 | işyeri nakli **suretiyle** | işyeri nakli **hariç** |
| 2022-37 | devredilebilir | devredilemez |
| 2022-71 | **fotokopi** | **orijinal** |
| 2023-69 | para cezaları | "**adli** para cezaları" |
| 2023-79 | "**Türkiye dışında**" | "Türkiye'de" |
| 2024-33 | "kara suları **dışındaki**" | "dışındaki" silinmiş |
| 2024-35 | **gümrük idaresi** | **vergi dairesi** |
| 2024-60 | yönetmelikle belirlenen haller dışında | "**her halde**" |
| 2025-54 | **uygulanmaz** | **uygulanır** |
| 2025-81 | **bölge müdürlüğü** | **gümrük müdürlüğü** |

- **Neden?** Dört cümle Kanundan aynen alınırsa itiraz edilemez. Beşinci cümledeki tek kelime ise aday metni gerçekten okumadıysa fark edilemez.
- **Öğrenciye mesaj:** "Anlamını biliyorum" yetmez. Edatlara ve kayıtlara dikkat: *dışında, hariç, suretiyle, sadece, talebi üzerine, olsun olmasın, sonundan/başından*. Soruyu genellikle bu kelimeler belirliyor.

### H2. Karıştırmamak: Doğru bilgiyi yanlış yerde tanımak

- **Kanıt.** KOMŞU tuzağı her yıl birinci sırada: 27, 38, 32, 38, 30 soru.
- **Örnekler:**
  - **2021-36:** Bilinen 45/20 günü doğru şıklara koyar, az bilinen "bir ayı aşan uzatmada gerekçe" sayısını kaydırır.
  - **2022-74:** TIR'da 120/168 saat soruluyor. Çeldiriciler 144 ve 192 saat (doğru değerlere +24 saat). Bir başka şıkta süre aşımına 241/1 uygulanacağı söyleniyor; oysa metin aşım süresine göre 241'in "ilgili fıkraları" diyor.
  - **2022-36 ↔ 2022-42:** İzne tabi eşyada iki kat, yasak eşyada dört kat. Aynı maddenin iki bendi iki ayrı soruda.
  - **2022-53:** İndirgeme yöntemindeki "pazarlama giderleri", hesaplanmış kıymet sorusuna taşınmış.
  - **2025-49:** Menşe şahadetnamesinin 6 ayı, nihai kullanım sorusunda çeldirici olmuş. Doğru cevap 3 ay.
  - **2025-63:** "Fire" tanımı "ikincil ürün" tanımının yerine konmuş.
- **Neden?** Uydurma bir şık kolay elenir. Başka yerde doğru olan bir hüküm ise "bunu bir yerde okumuştum" hissi verir. Yazar bu hissi kullanıyor.
- **Öğrenciye mesaj:** Bir sayıyı tek başına ezberlemek yetmez. Her sayıyı **komşusuyla birlikte** ezberleyin: "15 gün ödeme / 30 gün uzatma / 3 yıl tebliğ zamanaşımı".

### H3. Sayıyı yerinde ve başlangıcıyla bilmek

- **Kanıt.** 103 SAYI, 38 YAKIN-SAYI ve 16 BAŞLANGIÇ tuzağı var.
- **Sayısal şıklar nasıl dizilmiş?**
  - Şıkları sayı olan 52 sorunun 45'inde şıklar küçükten büyüğe dizilmiş.
  - Doğru değer 41 soruda (%79) ortadaki üç şıktan birinde. En küçük değer 8 soruda, en büyük değer yalnızca 3 soruda doğru.
  - Yani yazar doğru değeri ortaya koyup iki yanına gerçekçi değerler diziyor.
- **Başlangıç anı ayrıca soruluyor:**
  - 2021-24: yılın sonu / başı.
  - 2021-60 ve 2021-62: ihale ilanı / tasfiye kararı.
  - 2024-79: yükümlülüğün doğduğu tarih.
  - 2025-38: BTB'nin geçersizlik anı.
  - 2025-43: yasağın bildirimi.
  - 2025-69: havayolunda uçağın hareketi.
- **Neden?** Müşavirlik sahasında süre kaçırmak ceza ya da hak kaybı demek. Sayı soruları ayrıca tartışmasız doğru/yanlış üretir.
- **Öğrenciye mesaj:** Bir süreyi iki bilgiyle birlikte ezberleyin: başlangıç anı ve uzatma makamı.

### H4. Kapalı listenin sınırını bilmek

- **Kanıt.** 74 LİSTE-DIŞI ve 40 SAĞDUYU tuzağı var. Olumsuz köklü 153 sorunun önemli bir kısmı "listede olmayanı bul" tipinde. Örneğin 2023'te 25 olumsuz kökün 18'i bu tipte.
- **Sağduyu tuzağı örnekleri:** Aşağıdaki unsurların hepsi sahada mantıklı görünür, ama mevzuat listesinde yoktur.

| Soru | Kapalı liste | Listeye eklenen "mantıklı" unsur |
|---|---|---|
| 2021-93, 2022-25, 2023-22 | 5607'deki görevliler | özel güvenlik görevlisi, sınırdaki asker |
| 2022-92 | teminat türleri | kefalet |
| 2024-29, 2025-46 | menşe şahadetnamesinin zorunlu bilgileri | eşyanın kıymeti |
| 2023-98, 2024-28 | ilişkili kişiler | "aynı sektörde faaliyet" |
| 2024-76 | YYS sertifikası | belirli bir süre (oysa sertifika süresiz) |
| 2025-84 | özel antrepo şartları | gümrük müşaviri istihdamı (meslek yanlılığı tuzağı) |
| 2025-99 | YYS koşulları | "kapsamlı teminat" (AB terimi) |

- **Neden?** Kapalı liste ("yalnızca", "şunlardır") savunması en kolay bilgidir. Sağduyuyla çözülemez; okuyanı okumayandan ayırır.
- **Öğrenciye mesaj:** Kapalı listeler eleman sayısıyla birlikte ezberlenmeli. Örnek: "GOİK beş tanedir, rejim sekiz tanedir."

### H5. Kavram çiftlerini ayırmak

- **Kanıt.** AYIRT düzeyi 140 soru (%35). Bu oran 2024'te 40'a çıktı.
- **Ayrıntı:** Çiftler Bölüm 4'te tablo halinde.
- **Neden?** Gümrük işlemi doğru rejimi, doğru belgeyi ve doğru makamı seçmekle başlar. Yanlış seçim, beyanın baştan yanlış olması demek.

### H6. Kendi mesleğini bilmek

- **Kanıt.** Meslek bloğunda (GM, GMY, YGM, disiplin, temsil) 38 soru var. Yıllara göre 11, 6, 10, 7, 4. Düzey neredeyse hep HATIRLAMA: 38 sorunun 25'i. Tuzaklar SAYI ve YAKIN-SAYI.
- **Örnekler:**
  - **2025-23:** Yardımcı tebliğ kabul edemez, tek başına iş takibi yapamaz.
  - **2023-89:** Dolaylı temsil yalnızca gümrük müşavirine aittir.
  - **2021-84 ve 2023-26:** Değişikliklerin derneğe bildirim süresi bir hafta.
  - **2023-24, 25, 27, 28:** Disiplin cezaları ve zamanaşımı.
  - **2025-84:** Adayın "müşavir her yerde şarttır" önyargısını yakalayan soru.
- **Neden?** Sınav bir meslek giriş sınavı. Yardımcının yetkisini aşması 241 cezası ya da disiplin sonucu doğurur.

### H7. Güncel olmak

- **Kanıt:**
  - 2021-96: 2020 değişikliğiyle 5607'ye eklenen yaprak sigara kâğıdı.
  - 2022-65, 2024-26, 2025-32: Sınav yılının 241/1 tutarı (235 TL, 828 TL, 1.191 TL).
  - 2022-72: 2022 tarihli "antrepo izinleri süresiz" değişikliği.
  - 2024-91: 2024'te eklenen YGM TP1 kodu.
  - 2024-62: Elektrikli araçta 160 kW sınırı.
  - 2025-76: 2024 sonundaki posta kıymet kuralı.
- **Neden?** Sahadaki müşavir güncel tutarla ve güncel kuralla çalışır. Güncel bilgi, eski kaynaktan çalışan adayı da ayırır.
- **Öğrenciye mesaj:** Sınavdan önceki 12 ayın Resmî Gazete değişiklikleri ayrıca çalışılmalı.

### H8. Vakada gizli istisnayı görmek

- **Kanıt.** UYGULAMA veya BÜTÜNLEŞİK kodlu soru sayısı yıllara göre 1 → 10 → 11 → 10 → 12. Öncüllü format 2025'te 17'ye çıktı.
- **Örnekler:**
  - **2025-32:** Vaka adayı "3 kat ceza, %10 indirim" hesabına sokuyor. Oysa ithalatçı bir kamu idaresi (Maden ve Petrol İşleri GM) olduğu için 234 değil, 241 uygulanıyor. Cevap hesapla değil, istisnayı görmekle bulunuyor.
  - **2025-36:** EXW fiyata navlunun ve sigortanın yalnızca sınıra kadarki payı ekleniyor.
  - **2024-85:** Aynı fiil için firmaya ve müşavire ayrı ayrı tebliğ edilen idari para cezasını her biri ayrı öder. 2022-87'de ise vergi borcu müteselsildir ve bir kez ödenir. Yazar bu iki kuralı iki yıl arayla karşı karşıya koymuş.
  - **2023-60:** Beyansız ihracat teşebbüsü 239/1'e bağlanıyor.
  - **2025-70:** Yabancı uyruklu cenazenin gönderilmesi sözlü beyanla yapılıyor.
  - **2025-69:** Geri gelen eşyada süre, havayolunda uçağın hareketiyle başlıyor.
- **Neden?** Hacettepe döneminde yazar ezberi sahaya taşımak istiyor. Ama vakanın cevabı yine tek bir madde cümlesinde duruyor; vaka yalnızca bu cümleyi gizliyor.

---

## 4. Beş yılın değişmeyen eksenleri: ikiz kavramlar

Yazar bu çiftleri hem yıllar boyunca tekrar ediyor hem de çoğu zaman **aynı sınavda iki yönden** soruyor. Aynı sınavdaki çiftlere örnekler:

- **2022:** 33↔62, 34↔39, 36↔42, 48↔98, 89↔91.
- **2024:** 56↔77, 79↔82.
- **2025:** 27↔30; 39, 45 ve 86 (statü ≠ menşe üç kez).

| # | Eksen | Yazarın karıştırttığı | Sorular |
|---|---|---|---|
| 1 | Şartlı muafiyet düzenlemesi listesi ↔ ekonomik etkili rejim listesi | Transit birinde var, ötekinde yok. HİR'de durum tersine. | 21-43, 22-33, 22-62, 23-83, 24-30, 24-74 |
| 2 | DİR şartlı muafiyet ↔ geri ödeme | Vergi teminata mı bağlanıyor, yoksa tahsil edilip iade mi ediliyor? Standart değişim HİR'e ait. | 21-21, 23-65, 23-99, 24-51, 25-62, 25-63, 25-64, 25-71 |
| 3 | Gümrük statüsü ↔ menşe | A.TR statü belgesidir. Serbest dolaşıma girmek menşe kazandırmaz. Statü belgesi menşe göstermez. | 23-42, 24-40, 24-41, 24-45, 25-39, 25-45, 25-86 |
| 4 | Tümüyle elde edilme ↔ esaslı işçilik ↔ yetersiz işlem | Basit montaj ve ambalaj menşe kazandırmaz. Pozisyon değişikliği kazandırır. | 23-64, 24-33, 24-34, 25-47, 25-52, 25-53 |
| 5 | GK 241 kat merdiveni (2-4-6-8) | Fiilin hangi basamakta olduğu | 22-69, 23-29, 24-26, 24-32, 24-48, 25-31 |
| 6 | GK 235 matrahı ve katı | Gümrüklenmiş değer mi, vergi mi? Yasak eşyada 4 kat, izne tabi eşyada 2 kat. | 22-36, 22-42, 24-52, 25-95; tanım: 22-21, 23-45, 25-37, 25-87 |
| 7 | Ödeme 15 gün ↔ uzatma 30 gün ↔ tebliğ zamanaşımı 3 yıl | Aynı fıkradaki ikinci sayı çeldirici | 21-81, 22-88, 24-81, 25-27; 23-70, 24-79, 24-82, 25-30 |
| 8 | Geri verme: genel 3 yıl ↔ kusurlu eşya ve uluslararası anlaşma 1 yıl | Süre ve başlangıç | 22-89, 22-91, 24-83, 25-26 |
| 9 | İptal ↔ düzeltme | Yükümlülüğü ve serbest dolaşım statüsünü iptal sona erdirir, düzeltme sona erdirmez. | 21-42, 22-34, 22-39, 23-68, 25-40 |
| 10 | GOİK listesi ↔ ara statüler | Geçici depolama GOİK değildir. "Terk" yerine "teslim" yazılmış. | 21-33, 22-31, 23-31, 24-93, 24-100, 25-85 |
| 11 | Kıymet ikizleri | Satış ↔ satın alma komisyonu; aynı ↔ benzer eşya; ilişki listesi; pazarlama dolaylı ödeme değildir; TCMB döviz satış kuru | 21-31, 21-35, 22-48, 22-51, 22-52, 22-55, 22-98, 22-99, 23-98, 24-23, 24-25, 24-27, 24-28 |
| 12 | Doğrudan ↔ dolaylı temsil | Kimin adına, kimin hesabına | 21-22, 22-79, 23-89, 25-22 |
| 13 | Depolama süreleri | GDY 45/20 gün, yolcu ambarı 3 ay, ihracatta GDY 1 ay + 3 ay | 21-36, 21-40, 22-32, 22-82, 23-39, 23-50, 24-46, 25-80, 25-94 |
| 14 | BTB 6 yıl ↔ BMB 3 yıl | Geçerlilik süresi ve geçersizlik anı | 21-38, 23-86, 23-87, 25-38, 25-57, 25-58 |
| 15 | Vergide müteselsil sorumluluk ↔ idari para cezasının kişiselliği | Vergi bir kez ödenir, ceza her muhataba ayrı | 22-87 ↔ 24-85 |
| 16 | Geçici ithalat | Aylık %3; satış ve kiralama yasağı; "olağan yıpranma dışında değişmeden" ifadesi | 21-45, 21-53, 21-75, 22-60, 23-37, 23-54, 24-69, 24-72, 25-91, 25-92 |
| 17 | Antrepo tipleri | Genel A-B-F, özel C-D-E; işletici kimin sorumluluğunda | 21-54, 22-68, 23-85, 24-63 |
| 18 | DİR izni ↔ DİR izin belgesi | İzni gümrük idaresi, belgeyi Bakanlık (İhracat GM) verir. Makarna üretimi izinle değil belgeyle yapılır. | 23-56, 25-59, 25-66 |

---

## 5. Konu konu: Yazar burada neyi avlıyor?

| Konu grubu | Soru (2021–25) | Baskın tuzak | Yazarın derdi | Sahadaki karşılığı |
|---|---|---|---|---|
| Tanımlar / beyan / muayene | 41 (7-9-**20**-3-2) | KOMŞU, TERİM, LİSTE-DIŞI | Kavramı adıyla tanımak: GOİK, gümrük idaresi türleri, hatlar, beyanname yerine geçen belgeler | Beyanı doğru kavramla ve doğru belgeyle vermek |
| Tahsilat / teminat / geri verme / itiraz | 40 | KOMŞU, SAYI, **BAŞLANGIÇ** | Süreyi başlangıç anıyla bilmek: 15 gün, 30 gün, 3 yıl, 1 yıl, 15 gün itiraz | Süre kaçırınca hak kaybı ve takip |
| Meslek (GM, GMY, YGM, disiplin, temsil) | 38 (11-6-10-7-4) | SAYI, YAKIN-SAYI | Kendi yetkisinin sınırını ve kendi sürelerini çıplak ezberle bilmek | Yetki aşımı, disiplin, müteselsil sorumluluk |
| Antrepo / GDY / serbest bölge / gümrüksüz satış | 34 | SAYI, KOMŞU | Süreler, antrepo tipleri, makam (gümrük ↔ bölge müdürlüğü) | Eşyanın statüsünü ve süresini takip etmek |
| Kıymet | 34 (5-**12**-5-7-5) | **LİSTE-DIŞI, SAĞDUYU, İSTİSNA** | İlaveler ve indirimler, ilişki listesi, yasak yöntemler, kur. "Mantıkla" kıymet çalışanı eler. | Yanlış kıymet → vergi farkı + 234/241 cezası |
| DİR / HİR / GKAİR / şartlı muafiyet | 31 | **KOMŞU** (18/31), TERİM | Rejim ve sistem tanımlarını birbirinden ayırmak | Yanlış sistem → teminatın yakılması, ceza |
| Menşe / TPÖ / İthalat Rejimi Kararı | 28 (0-1-4-**12-11**) | KOMŞU, TERİM | Belge türleri (A.TR, EUR.1, menşe şahadetnamesi, GTS), statü ↔ menşe, yetersiz işlem | Tercihli vergi ve TPÖ hatası |
| Kaçakçılık (5607) | 27 (**10**-7-4-3-3) | KOMŞU, LİSTE-DIŞI, SAĞDUYU | Kapalı görevli listesi, artırım oranları, gümrüklenmiş değer | Müşavirin ağır ceza riski |
| Muafiyet / yolcu / posta | 21 | SAYI, TERSİNE | Avro limitleri, "1 ay önce / 3 ay sonra", araç muafiyeti tekrarı (5 yıl) | Yolcu ve kargo uygulaması |
| GK cezaları | 20 (0-5-6-5-4) | **SAYI** (17/20) | Kat merdiveni ve matrah; vaka ve hesap en çok burada | Yardımcının hatasının bedeli |
| Geçici ithalat | 18 | KOMŞU | Tanım, %3, yasak işlemler, taşıt belgeleri | Rejim ihlali → gümrüklenmiş değerin 2 katı |
| Transit / TIR | 17 | KOMŞU, LİSTE-DIŞI | Teminat istisnaları, sona erme ↔ ibra, TIR saatleri | Rejimin kapanmaması → vergi ve ceza |
| İhracat / geri gelen eşya | 14 | KOMŞU, YAKIN-SAYI | Terk tarihi, 3 yıl, beyanname kapatma süreleri, rejim kodu | İhracatın tevsiki |
| Serbest dolaşım / nihai kullanım / fikri haklar | 12 | KOMŞU, TERSİNE | Statü kaybı halleri, devir, lehe oran şartları | Vergi avantajının kaybı |
| YYS / OKSB | 11 | SAYI | Faaliyet süresi (YYS 3 yıl, OKSB 2 yıl), mavi hat ↔ yeşil hat, süresiz sertifika | Kolaylaştırma haklarını doğru kullanmak |
| Tarife / BTB | 11 | TERİM | Basamak sayıları (2-4-6-12), BTB yetkili bölge müdürlükleri, geçersizlik halleri | Doğru GTİP |

**Okuma notu:** Kıymette olumsuz kök 34 sorunun 19'unda kullanılmış. Bu konuda yazar "listede olmayanı" arıyor. Cezalarda ise neredeyse hep doğrudan "kaç kat" ya da "hangi ceza" soruluyor.

---

## 6. Yıl yıl yazar imzası ve eğilim

| | 2021 (ASYM) | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|
| Olumsuz kök | 31 (%39) | **38 (%47,5)** | 25 (%31) | 34 (%42,5) | 25 (%31) |
| Birebir metin | **64** | 63 | 45 | 62 | 41 |
| Uygulama veya bütünleşik | **1** | 10 | 11 | 10 | **12** |
| Öncüllü | 7 | 3 | 5 | 7 | **17** |
| Vaka / hesap | 0 / 0 | 4 / 2 | 3 / 1 | 3 / 1 | **6 / 3** |
| Ortalama kök uzunluğu (karakter) | 237 | 187 | 173 | 197 | **282** |
| Ağırlıklı blok | Kaçakçılık (10) ve meslek (11) | Kıymet (12) | Tanımlar (20) ve meslek (10) | Kıymet ve menşe (19) | Menşe, serbest dolaşım ve BTB; DİR (7) |
| En çok kim elenir? | 5607'yi ve yönetmelikleri atlayan | Kıymeti mantıkla çalışan | Tanım ve meslek ezberi zayıf olan | Tebliğ ayrıntısına inmeyen | Statü ↔ menşe ve izin ↔ belge ayrımını yapamayan |

- **2021 (ASYM).** Saf ezber sınavı: hesap ve vaka sıfır, düzeyde HATIRLAMA 48. Son 10 soru tamamen 5607. Kalite kontrolü zayıf: aynı GK 128 tanımı iki kez sorulmuş (45 ve 75) ve yazım hataları var.
- **2022.** Kıymet yılı. Olumsuz kök en yüksek düzeyde. Ayna sorular bilinçli kurulmuş. 49–53 arasındaki beş sorunun cevabı arka arkaya E.
- **2023.** "Temel tanımlar + meslek hukuku" yılı. Transit, HİR, GKAİR, teminat ve tasfiye doğrudan hiç sorulmamış. Çok sayıda zayıf, uydurma çeldirici var. 59 ve 72'de aynı beşli makam şık seti kullanılmış.
- **2024.** "Ayırt et" yılı: AYIRT düzeyi 40 soru. Kat merdiveni ve güncel tutar soruları var. Menşe bloğu büyümüş.
- **2025.** Blok yazarlığı en net bu yılda. Öncüllü ve vaka soruları artmış, kök uzamış. Statü ↔ menşe ekseni üç kez sorulmuş.

**Eğilim (2026–2027 için):**

1. Ezberden uygulamaya kayma **yavaş ama sürekli**. Yine de uygulama soruları da tek bir madde cümlesine dayanıyor.
2. Öncüllü format artıyor.
3. Menşe, TPÖ ve İthalat Rejimi Kararı yükselişte. Kaçakçılık yılda 3 soruda sabitlenmiş görünüyor.
4. Meslek hukuku her yıl soruluyor.
5. Güncel tutar sorusu 2022, 2024 ve 2025'te geldi. 2026'da da beklenmeli.

---

## 7. Kitapçığın biçim kalıpları

| Kalıp | Bulgu |
|---|---|
| Cevap harfi dağılımı (400 soru) | A 57 (%14), B 89, C 81, D 82, E 91. **A en az kullanılan harf.** |
| Art arda aynı harf | Her yıl 10–18 kez görülüyor. En uzun seri 5 (2022, 49–53, hepsi E). Bakanlık bu konuda bir kural uygulamıyor. |
| Sayısal şıklar | 52 sorunun 45'inde şıklar küçükten büyüğe dizilmiş. Doğru değer 41 soruda (%79) ortadaki üç şıkta. |
| Öncüllü sorularda en kapsamlı şık | 40 sorunun 23'ünde (%58) doğru. Yazar tüm öncülleri doğru yapıp adayı eksik seçime itiyor (21-73, 21-74, 25-24, 25-40, 25-51, 25-96). |
| Öncüllü kök yönü | 32 olumlu, 8 olumsuz |
| Doğru şıkkın uzunluğu | En uzun şık %26, en kısa şık %25 oranında doğru. Rastlantı düzeyi %20 olduğu için **uzunluk bir ipucu değil**. |
| Kökte mevzuat adı | Köklerin yaklaşık %55–70'inde var. Kalan köklerde ya "gümrük mevzuatına göre" yazıyor ya da hiçbir mevzuat adı yok. |
| Kökte madde numarası | 2021'de 1 soru, sonraki yıllarda 7–9 soru. Numara verildiğinde cevap çoğu zaman kolaylaşıyor. |

### Gümrük Koçu kurallarıyla karşılaştırma (Prompt 3)

Bakanlık "art arda aynı harf" yasağı uygulamıyor ve köklerin bir kısmında dayanağı yazmıyor. Prompt 3'teki iki kuralımız Bakanlık pratiğinden **daha sıkı** ve korunmalı:

- art arda aynı cevap harfi yok,
- kök = mevzuat adı + hükmün konusu + kurum kalıbı.

Bunlar öğrencinin kaynağı tanımasını ve dengeli çalışmasını sağlıyor. Taklit edilmesi gereken üç şey ise Bakanlığın şu tercihleri:

- doğru şıkkı birebir metinden kurmak,
- çeldiriciyi komşu hükümden üretmek,
- sayısal şıkları sıralı ve doğru değeri ortaya yakın dizmek.

---

## 8. En çok kim elenir? Beş aday profili

1. **Yalnızca Kanun okuyan.**
   - Soruların yaklaşık yarısı Gümrük Yönetmeliği, tebliğ ve karar ayrıntısına iniyor. 2025'te Kanun 31 soru, Yönetmelik 22 soru, alt düzenlemeler 24 soru.
   - Bu adayı eleyen ayrıntılar: YGM rapor kodları, INF formları, TIR'da 120/168 saat, BTB'yi düzenleyen bölge müdürlükleri, OKSB'nin mavi hattı.
2. **Sayıyı yaklaşık bilen.**
   - Çeldiriciler doğru değerin hemen yanındaki gerçek değerlerden geliyor: 20/45 gün, 120/168 saat, 15/30/45 gün, 1/3 yıl, 2/4 kat.
3. **Mevzuatı sağduyuyla çözen.**
   - Kapalı listeye eklenen mantıklı unsurlarla eleniyor: özel güvenlik görevlisi, kefalet, "kıymet", "aynı sektör", müşavir istihdamı.
4. **Olumsuz kökü hızlı okuyan.**
   - Olumsuz kök oranı %31–47,5. Bu soruların önemli bir kısmında aranan şık, doğru cümleden tek kelimeyle ayrılıyor.
5. **Güncellemeyi izlemeyen.**
   - Sınav yılının ceza tutarı, yeni rapor kodu, posta kıymet kuralı gibi sorularda eleniyor. Eski kaynaktan çalışan aday, değişen hükümde eski cevabı işaretliyor (2021-86, 2021-95).

---

## 9. 2026–2027 için yazarın olası hamleleri

Ayrıntılı liste 400 soru için `SONRAKI-HAMLELER.md` dosyasında. Burada en olası hamleler:

### a) Sorulmuş maddelerin sorulmamış komşu fıkraları

Yazarın en tutarlı davranışı bu.

- **GK 241:** Henüz eşleştirilmemiş fiil-kat çiftleri. Örnek: 241/3-a, kararlara dayanak oluşturan belge ve bilgilerin yanlış verilmesi; 241/3-g, antrepo kayıtları.
- **GK 235:** 235/4-a'daki 30 gün (yalnızca doğrudan transit).
- **GK 179/1:** %1, %3 ve %10 oranları.
- **GK 177/4:** Otuzar günlük intikal ve teslim süreleri.
- **Kıymet:**
  - GY 55/1-ç'deki %5 oy hakkı ve 55/2'deki tek acente istisnası.
  - GY 48 indirgeme yöntemindeki indirimler.
  - 28/c'deki faizin düşülme şartları.
  - GY 57/2'deki bilgi amaçlı kurlar.
- **Menşe:**
  - GY 40/2: Hangi eksikliğin idare amirinin onayıyla tamamlanabileceği.
  - GY 38/3 ve 38/5: 6 aylık geri verme ve denetim süreleri.
  - GY 36/3: Üçüncü ülkedeki antrepo menşei değiştirmez.
  - GK 18/2-f, g, h: Deniz ürünleri, fabrika gemileri, deniz dibi.
- **DİR:**
  - Kapatma süresi (3 ay), eksikliklerin tamamlanması (1 ay).
  - Kısmi teminat iadesinde %90 sınırı.
  - Değişmemiş eşyada %1, işletme malzemesinde %2 sınırları.
  - GK 117: Geri ödeme sisteminin uygulanmadığı haller.
- **Meslek:**
  - Geçici 6/4–6/9: Savunma için 10 gün, tedbir için 6 ay, dönem süreleri.
  - GY 563/2: "Her yılın ikinci ayı" bildirimi.
  - YGM'de henüz sorulmamış kodlar (BD1, TK1, NK1, AN6, AN7).
- **5607:** md.4/1 ve 4/4 artırım oranları.

### b) Hiç ya da çok az sorulmuş alanlar

Kullanıcının konu kapsamı tercihine göre bu alanlar açık.

- 5 yılda 1 soru sorulanlar: kabotaj, sınır ticareti, taşıtlar, mücbir sebep, belge saklama, gümrüksüz satış.
- Sonradan kontrol hiç sorulmadı. Uzlaşma yalnızca süre olarak geçti (23-77, 24-80).
- Transit ve TIR 2023'te hiç sorulmadı.

### c) Kaynak metinlerde dipnotla görünen 2025–2026 değişiklikleri

Yazar güncelliği ödüllendiriyor; aşağıdaki değişiklikler yüksek olasılıkla soru kaynağı.

- Posta ve hızlı kargo düzeni (2009/15481 Karar md.62, 2026 değişikliği).
- İthalat Rejimi Kararı ek listeleri. Depodaki güncel metinde VI sayılı listenin başlığı değişmiş.
- Asgari ücret tarifesindeki genel indirimin %20 olması (30.12.2025).
- Akaryakıt yönetmeliğinde yetkili bakanlıklar (18.01.2024 değişikliği).
- 241/1 usulsüzlük cezasının 2026 tutarı.

---

## 10. Yazar gibi soru yazmak: Gümrük Koçu kontrol listesi

Aşağıdaki liste Prompt 3'ün yerine geçmez. Prompt 3'ün **üstüne** eklenir; çelişki olursa Prompt 3 geçerlidir.

1. **Karışabilecek hükmü seç.** İki sayılı, iki sistemli, iki listeli ya da basamaklı hükümler öncelikli.
2. **Doğru cevabı madde cümlesinden birebir al.** Çıkarım gerekiyorsa çıkarım tek adımlı olsun.
3. **Çeldiricinin metindeki gerçek yuvasını yaz.** Her çeldirici şu üç kaynaktan birinden gelsin: aynı maddenin komşu fıkrası, komşu rejimin benzer hükmü, aynı mevzuatın sayı havuzu. Uydurma çeldirici yalnızca son çare olsun.
4. **Olumsuz köklü soruyu iki kalıptan biriyle kur.**
   - Dört birebir doğru cümle + tek kelimesi değiştirilmiş beşinci cümle.
   - Kapalı liste + akla yatkın bir yabancı unsur.
5. **Sayısal şıkları küçükten büyüğe diz.** Doğru değeri ortadaki üç şıktan birine koy. Diğer değerleri aynı mevzuatın gerçek sayılarından seç (15/30/45/60 gün; 1/3/5/6 yıl; 2/4/6/8 kat).
6. **Süre soruluyorsa başlangıç anını da yokla.** Ya kökte ver ya da şıklara koy.
7. **Her ikiz kavram için aynı sette iki yönlü soru düşün.** Örnek: "ŞMD listesinde olmayan" ile "EER listesinde olmayan".
8. **Öncüllü sorularda öncül sayısı en az 3 olsun.** Bakanlık "hepsi" cevabını sık kullanıyor. Biz de kullanalım, ama setin cevap dengesini bozmadan.
9. **Vaka sorusunda vakanın içine tek bir istisna sakla.** Örnek: kamu idaresi, taşıma türü, sınıra kadarki navlun payı. Hesap zinciri istisnayı görmeyeni yanıltsın.
10. **Her sette bir "meslek yanlılığı" sorusu kur.** Adayın "müşavir şarttır / yardımcı yapabilir" önyargısını yoklayan bir soru olsun.
11. **Her sette bir güncellik sorusu kur.** Son 12 ayda değişen hükümden, depodaki güncel metne dayanarak sor.
12. **Kalite kontrolünde Bakanlığın kusurlarına düşme:**
    - aynı sette aynı hükmü iki kez sorma (Bakanlık 2021'de 45 ve 75'te bunu yaptı),
    - kökte doğru şıkkın adını verme (2023-99),
    - kök "Kanuna göre" derken hükmü Yönetmelikten alma (2025-96).

---

## 11. Kaynak eksikleri

Sorulmuş ama depoda metni olmayan bilgi alanları şunlar. Depoya eklenmeleri önerilir.

| Eksik kaynak | Sorular |
|---|---|
| Rejim kodları listesi (BİLGE / beyanname doldurma kılavuzu) | 23-52, 24-49, 25-68 |
| 2009/15481 Karar Ek-9 kişisel eşya listesi ve tanımlar maddesi (aile ünitesi, şahsi/kişisel eşya) | 22-85, 23-48, 24-98 |
| Kullanılmış taşıtta amortisman indirimi uygulaması | 24-22, 25-34 |
| 3351 sayılı İlave Gümrük Vergisi Kararı | 24-36 (25-44 dolaylı) |
| Gümrük Genel Tebliği (Uluslararası Anlaşmalar) Seri No 10: statü-menşe, EUR.1 ve A.TR | 25-39, 25-41 |
| Gümrük Genel Tebliği (Gümrük İşlemleri) Seri No 149: menşe belgelerinin basımı | 25-42 |
| GTS ve Form A | 24-41, 24-42 |
| 241/1 tutarlarının yıllara göre listesi (dipnotlar) | 22-65, 24-26, 25-32 |
| GY Ek-82 (241/1 fiilleri), GY Ek-8 (kıymet yorum notları), GY 444 (geçici çıkarılan taşıtlar) | 23-30; 22-44, 22-50, 22-52; 21-32 |
| Dış ticaret genel bilgisi: proforma fatura, beyannamenin genel tanımı, ithalatta tahsil edilen vergiler | 21-61, 21-66, 21-71, 22-38, 23-49 |
| DİR Kararı amaç maddesi, GATT madde içerikleri, INF formları | 22-97, 25-33, 22-45/58 |

---

## 12. Resmî cevap düzeltmeleri ve tartışmalı sorular

### a) Eski envanterdeki cevap farkları (2021–2024)

Envanterde türetilen cevaplar 7 soruda resmî anahtarla uyuşmuyor. Envanter bu raporla birlikte düzeltildi.

| Soru | Eski | Resmî | Açıklama |
|---|---|---|---|
| 2021-86 | B | **A (%25)** | Sınav tarihindeki oran %25. Güncel metinde %20. |
| 2021-95 | C | **E** | Sınav tarihinde Hazine ve Maliye Bakanlığı da yetkiliydi. 18.01.2024'te listeden çıkarıldı. |
| 2022-83 | E | **D** | İzinle vatandaşlıktan çıkanlar kapsam dışı. E şıkkı da tartışmalı. |
| 2022-87 | D | **B** | Müteselsil borç bir kez ödenir; yanlış öncül yalnızca II. |
| 2024-47 | B | **C** | GK 3/2-d'ye göre ihracat gümrük idaresi (çıkış gümrük idaresi değil). |
| 2024-85 | D | **B** | İdari para cezasını her muhatap ayrı ayrı öder. Tartışmalı (bkz. 3/H8). |
| 2024-100 | D | **A** | Eşya GDY'ye rejim beyanıyla konmaz; geçici depolama bir statüdür. D şıkkı da tartışmalı. |

2025'in 80 gümrük sorusunun resmî cevabı ilk kez bu çalışmada envantere girdi.

### b) Mevzuatı sonradan değişen sorular

Resmî cevap sınav tarihine göre doğru, ama güncel metinle uyuşmuyor:

- 2021-86 ve 2021-95 (yukarıda).
- 2025-50: VI sayılı listenin başlığı değişti.
- 2025-76: Karar 62'deki 30 Avro düzeni 2026'da kalktı.

### c) Tartışmalı ya da kusurlu sorular

Bu soruların resmî cevabı değişmiyor, ama ifade sorunlu:

- **2025-100:** Kaynak metinde koşulların izlenmesi 5 yılda bir; resmî cevap 1 yıl.
- **2025-86:** A şıkkı GK 157/1-d ile çelişkili okunabilir.
- **2022-83, 2024-85, 2024-100:** Yukarıdaki tabloda açıklandı.
- **2021-40 ve 2021-46:** Kök belirsiz.
- **2023-74/III:** Kanun "özet beyanın verildiği tarih" diyor, öncülde "tescil tarihi" yazıyor.
- **2025-59:** Yalnızca "izin" kelimesi soruyu kurtarıyor.

**Öğrenciye mesaj:** Çıkarım sorusunda iki şık savunulabilir görünüyorsa, madde lafzına en yakın şıkkı işaretleyin. Bakanlığın resmî cevabı neredeyse her zaman lafızdan yana.

---

## Ek: Dosyalar

| Dosya | İçerik |
|---|---|
| `CEVAP-ANAHTARI.md` | 2021–2025 resmî cevap anahtarı (2025 A ve B) ve A↔B soru eşlemesi |
| `soru-soru/2021.md` … `2025.md` | 400 sorunun her biri için madde, hedef, neden bu hüküm, çeldiricilerin kaynağı, sonraki hamle ve yıl imzası |
| `SONRAKI-HAMLELER.md` | Sonraki hamleler konu gruplarına göre |
| `../araclar/` | Kırmızı işaretli cevapları PDF'ten çıkaran betikler |
