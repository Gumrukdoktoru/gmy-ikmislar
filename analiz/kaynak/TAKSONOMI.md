# GMY Sınavı Soru Sınıflandırma Taksonomisi (SABİT — sadece bu kodları kullan)

Her soru için aşağıdaki alanları doldur. `konu`, `kok`, `tip`, `mevzuat` alanlarında YALNIZCA aşağıdaki listelerdeki KODLARI kullan (birebir yaz).

## 1. `bolum` (soru numarasına göre sabittir)
- 1-5   → `TURKCE`
- 6-10  → `MATEMATIK`
- 11-15 → `TARIH`
- 16-20 → `ANAYASA`
- 21-100 → `GUMRUK`

## 2. `konu` (sorunun asıl ölçtüğü konu — TEK kod seç)

### TURKCE bölümü
- `TR_SOZCUK_ANLAM`  : gerçek/mecaz/yan anlam, eş/zıt/sesteş anlam, deyim, sözcük anlamı
- `TR_CUMLE_ANLAM`   : cümlede anlam, anlam ilişkileri (koşul, amaç-sonuç), pişmanlık/duygu anlamı
- `TR_PARAGRAF`      : ana düşünce, akışı bozan cümle, düşünceyi geliştirme yolları, paragraf yorumlama
- `TR_DILBILGISI`    : ses bilgisi (yumuşama vb.), yapı bilgisi (ekler), sözcük türleri (topluluk adı vb.), cümle öğeleri, fiiller
- `TR_YAZIM_NOKTALAMA`: yazım kuralları, "ki/de" yazımı, kesme işareti, noktalama
- `TR_ANLATIM_BOZ`   : anlatım bozukluğu

### MATEMATIK bölümü
- `MAT_TEMEL_ISLEM`  : dört işlem, sayılar, bölünebilme, çarpan/bölen, kesirler, denklem, işlem tanımlama, örüntü
- `MAT_PROBLEM`      : yaş, ortalama, işçi-havuz, yüzde-kâr, saat/zaman, ölçü birimi (kg, litre, metre), günlük hayat problemleri
- `MAT_GEOMETRI`     : alan, çevre, üçgen/dikdörtgen/kare

### TARIH bölümü
- `TAR_OSMANLI_SON`  : Osmanlı'nın son dönemi, I. Dünya Savaşı, cepheler, Mondros, Misak-ı Milli
- `TAR_MILLI_MUCADELE`: Kurtuluş Savaşı, kongreler, cemiyetler/gazeteler, muharebeler, Mudanya, Samsun'a çıkış, TBMM'nin açılışı, Nutuk
- `TAR_INKILAP_ILKE` : Cumhuriyet'in ilanı, inkılaplar, Atatürk ilkeleri, Millet Mektepleri, Atatürk'ün hayatı
- `TAR_DIS_POLITIKA` : Lozan ve sonrası, Hatay, Balkan Antantı, Atatürk dönemi dış politika

### ANAYASA bölümü
- `ANA_TEMEL_HUKUK`  : hukuk kavramları, pozitif hukuk, normlar hiyerarşisi, anayasa tanımı, devletin nitelikleri, değiştirilemez maddeler, yönetim şekli
- `ANA_YASAMA`       : TBMM, milletvekili sayısı/yaşı, yasama dokunulmazlığı, kanun teklifi, yasama işlemi
- `ANA_YURUTME`      : Cumhurbaşkanı görev/yetki/seçim, Cumhurbaşkanlığı kararnameleri
- `ANA_YARGI`        : yargı organları, Anayasa Mahkemesi (siyasi parti mali denetimi dahil), yargı mercii
- `ANA_HAK_ODEV`     : temel hak ve özgürlükler, ekonomik-sosyal haklar, vatandaşlara özgü haklar
- `ANA_SECIM`        : seçim ilkeleri, seçme-seçilme yaşı (milletvekili seçilme yaşı → ANA_YASAMA değil, ANA_SECIM)
- `ANA_ULUSLARARASI` : AB, uluslararası kuruluşlar, Türkiye'nin üyelikleri

### GUMRUK bölümü (21-100)
- `G_TEMEL_KAVRAM`   : GK md.1-3 tanımları ve genel hükümler: kanunun amacı, Türkiye Gümrük Bölgesi, gümrük idaresi, kişi/yükümlü, gümrük statüsü, "gümrükçe onaylanmış işlem veya kullanım" (GOİK) deyimi ve kapsamı, gümrük rejimlerinin sayısı/listesi ("hangisi gümrük rejimi değildir"), ekonomik etkili rejimlerin listesi, şartlı muafiyet düzenlemesi tanımı, "gümrük vergileri" deyimi, brüt ağırlık vb. genel tanımlar, mücbir sebep tanımı
- `G_TARIFE`         : gümrük tarifesi, tarife sınıflandırması, GTİP/tarife pozisyonu örnekleri, Bağlayıcı Tarife Bilgisi (BTB)
- `G_MENSE`          : tercihli/tercihsiz menşe, tümüyle elde edilen eşya, yetersiz işçilik, menşe şahadetnamesi, EUR.1/A.TR/Form A gibi menşe/dolaşım belgeleri, Bağlayıcı Menşe Bilgisi (BMB), GTS menşe belgesi, AB-Türkiye Gümrük Birliği'nde dolaşım belgesi
- `G_KIYMET`         : gümrük kıymeti, kıymet yöntemleri (satış bedeli, aynı/benzer eşya, indirgeme, hesaplanmış, son yöntem), fiilen ödenen fiyat, ilaveler/indirimler, ilişkili kişiler, royalti, veri taşıyıcıları, kur çevrimi, eski model düşümü, GATT md.VII, EXW/CIF kıymet hesabı
- `G_GIRIS_BEYAN`    : eşyanın gümrüğe sunulması, özet beyan, geçici depolama (yerler ve süreler), GOİK verilme süreleri, gümrük beyanı/beyanname türleri, beyanname yerine geçen belgeler, beyannamede düzeltme/iptal, muayene, tahlil, kontrol hatları (kırmızı/sarı/yeşil/mavi), beyanın kontrol türleri, risk analizi, belge saklama, rejim kodları (genel)
- `G_SERBEST_DOLASIM`: serbest dolaşıma giriş rejimi, serbest dolaşım statüsünün kazanılması/kaybı, gümrük statü belgesi, nihai kullanım, tarife kontenjanı/tavan uygulamasının serbest dolaşımdaki etkisi
- `G_ANTREPO`        : antrepo rejimi, antrepo tipleri (A,B,C,D,E,F), antrepo işleticisi, elleçleme, antrepo süreleri, özel/genel antrepo
- `G_DAHILDE_ISLEME` : dahilde işleme rejimi (DİR), şartlı muafiyet/geri ödeme sistemi, eşdeğer eşya, önceden ihracat, DİİB, DİR'de menşe/tercihli tarife
- `G_GKAI`           : gümrük kontrolü altında işleme rejimi
- `G_GECICI_ITHALAT` : geçici ithalat rejimi, kısmi muafiyet hesaplaması, ATA karnesi, geçici ithal edilen kara taşıtları tebliği, fuar/sergi eşyası, rejim ihlali
- `G_HARICTE_ISLEME` : hariçte işleme rejimi, standart değişim sistemi, üçgen trafik, tamir amaçlı geçici ihracat
- `G_TRANSIT`        : transit rejimi, ortak/ulusal transit, NCTS, TIR karnesi/TIR tebliği, transitte teminat, transitin sona ermesi, NATO SOFA transit
- `G_IHRACAT`        : ihracat rejimi, ihracat beyannamesi, eksik beyan, beyanname kapatma süresi, ihracat rejim kodları, ihracatta yükümlülüğün başlaması, geçici ihracat
- `G_SERBEST_BOLGE`  : serbest bölgeler, gümrüksüz satış mağazaları
- `G_YUKUMLULUK_TEMINAT`: gümrük yükümlülüğünün doğuşu/başlangıç tarihi/sona ermesi, teminat (türleri, götürü teminat, kabul edilmeyen teminatlar)
- `G_TAHAKKUK_TAHSIL`: gümrük vergilerinin tahakkuku, tebliği, ödeme süreleri, tebligat zamanaşımı, gecikme faizi/zammı, 6183 takibat, tecil-taksit, vergi oranının belirlenme tarihi
- `G_GERI_VERME`     : geri verme ve kaldırma (başvuru süreleri, yetkili birim, kusurlu eşya)
- `G_MUAFIYET`       : gümrük vergisi muafiyet ve istisnaları: 2009/15481 Karar (yolcu beraberi eşya, hediyelik eşya, kesin dönüş, taşıt muafiyeti, engelli, miras eşyası, cenaze), posta ve hızlı kargo, diplomatik muafiyet, bilgi materyali/eğitim-bilim eşyası, GERİ GELEN EŞYA (GK 168-170), yolcu eşyası ambarları/süreleri
- `G_TASFIYE`        : tasfiye (tasfiyelik eşya, tasfiye yöntemleri, ihale, taşıt şerhleri), el konulan eşyanın tasfiyesi (5607'ye göre değilse)
- `G_CEZA_ITIRAZ`    : 4458 GK idari para cezaları ve usulsüzlükler (md. 234, 235, 236, 238, 241), ceza tutarları, cezaların tebliği ve müteselsil sorumluluk, itiraz (md. 242), uzlaşma, ceza zamanaşımı
- `G_KACAKCILIK`     : 5607 sayılı Kaçakçılıkla Mücadele Kanunu ve uygulama yönetmelikleri (suçlar, cezalar, artırımlar, görevliler, el koyma, müsadere, akaryakıt, ulusal marker)
- `G_MESLEK`         : gümrük müşavirliği ve gümrük müşavir yardımcılığı meslek mevzuatı: şartlar, sınav, izin belgesi, bildirimler, disiplin cezaları, asgari ücret tarifesi, şirket kurma, belge saklama (meslek mensubu), TEMSİL (doğrudan/dolaylı temsil, temsil hakkı, md. 5)
- `G_YGM`            : Yetkilendirilmiş Gümrük Müşavirliği (YGM) tebliği: tespit işlemleri, raporlar (DR1, DR2...), hisse oranları, YGM görevleri
- `G_KOLAYLASTIRMA`  : Yetkilendirilmiş Yükümlü Sertifikası (YYS), Onaylanmış Kişi Statüsü (OKS), Gümrük İşlemlerinin Kolaylaştırılması Yönetmeliği, mavi hat, kamu kurumlarına kolaylıklar
- `G_DIS_TICARET_POL`: İthalat Rejimi Kararı ve listeleri, İlave Gümrük Vergisi (3351), ek mali yükümlülük, ticaret politikası önlemleri, kota/tarife kontenjanı/tavan kavramları, TEV/damping, GTS tanımı, sınır ticareti, ithalatta alınan vergi ve fonlar (KDV, ÖTV, damga), gümrüklenmiş değer hesabı, fikri ve sınai hakların korunması (GK 57)
- `G_OZEL_ISLEMLER`  : akaryakıt ve kumanya, kabotaj, liman bayileri, gemi/uçak işlemleri, taşıtların geçici çıkışı, posta gümrük işlemleri (listeler), sevk işlemleri
- `G_DIS_TIC_BELGE`  : dış ticaret ve taşıma belgeleri (proforma fatura, çeki listesi, konşimento, CMR, taşıma belgesi), Incoterms, ödeme şekilleri, gümrük teşkilatı/bölge müdürlükleri

Kararsız kalırsan sorunun KÖKÜNDE hangi kurum/rejim/kavram geçiyorsa onu seç.

## 3. `kok` (soru kalıbı / kök yapısı — TEK kod)
- `OLUMLU`   : "hangisidir / doğrudur / hangisinde doğru verilmiştir / kaçtır / ne ad verilir" vb. olumlu kök
- `OLUMSUZ`  : "değildir / yanlıştır / yer almaz / söylenemez / sayılmamıştır / olamaz / -maz/-mez / yararlanamaz / uygulanmaz" vb. olumsuz kök (kök vurgulu olumsuz)
- `ONCULLU`  : I., II., III. ... şeklinde numaralı öncüller verilip "hangileri / hangisi" diye sorulan (öncüllü sorular olumlu ya da olumsuz olsa da ONCULLU yaz)
- `BOSLUK`   : "……" boşluk doldurma
- `TABLO_ESLESTIRME` : tablo/liste eşleştirme, sıralama

## 4. `tip` (soru tipi — ölçülen bilgi türü, TEK kod)
- `TANIM`        : bir kavramın tanımı / "ne ad verilir" / "… deyimi neyi ifade eder" / tanımdan kavramı bulma
- `SAYISAL`      : süre, oran, tutar, yaş, sayı, limit, yıl gibi sayısal mevzuat bilgisi ("kaç gün", "yüzde kaç", "kaç yıl", "ne kadar süre")
- `KAPSAM_SART`  : bir düzenlemenin kapsamı, şartları, unsurları, türleri, listesi (hangisi kapsamda/kapsam dışı, hangisi şartlardan biri, hangisi türlerinden)
- `DOGRU_YANLIS_HUKUM`: birden fazla mevzuat hükmü içeren seçeneklerden doğru/yanlış olanı bulma ("aşağıdakilerden hangisi yanlıştır/doğrudur" tipinde, seçenekler farklı kurallar içeriyorsa)
- `YETKILI_MERCI`: yetkili makam, kurum, merci, kimin yaptığı/kime başvurulduğu
- `BELGE_PROSEDUR`: hangi belge/form/rejim kodu ile işlem yapılır, hangi rejim hükümleri uygulanır, usul/prosedür adımı
- `VAKA_UYGULAMA`: örnek olay/senaryo üzerinden mevzuatın uygulanması (X firması..., yolcu A...), ceza veya rejim belirleme
- `HESAPLAMA`    : sayısal işlem/hesap gerektiren soru (matematik soruları ve kıymet/vergi hesabı)
- `DIL_KURALI`   : Türkçe dil bilgisi, yazım, noktalama, anlam kuralı uygulama
- `YORUM_CIKARIM`: paragraf yorumlama, ana fikir, akış, anlam çıkarımı
- `OLGU_BILGI`   : tarih/olay/kişi/yer/kurum gibi genel kültür olgu bilgisi

Not: Matematik soruları genelde `HESAPLAMA`; Türkçe dil bilgisi/yazım/anlam soruları `DIL_KURALI`, paragraf soruları `YORUM_CIKARIM`; tarih soruları genelde `OLGU_BILGI` (tanım içeriyorsa TANIM olabilir); anayasa soruları içeriğe göre SAYISAL/TANIM/YETKILI_MERCI/KAPSAM_SART/OLGU_BILGI.

## 5. `mevzuat` (sorunun dayandığı ana mevzuat — TEK kod; GUMRUK dışı bölümlerde `YOK`)
- `GK_4458`      : 4458 sayılı Gümrük Kanunu (soru "Gümrük Kanunu'na göre" diyorsa veya konu doğrudan Kanun hükmüyse)
- `GY`           : Gümrük Yönetmeliği
- `KMK_5607`     : 5607 sayılı Kaçakçılıkla Mücadele Kanunu ve yönetmelikleri
- `KARAR_2009_15481`: 2009/15481 sayılı Gümrük Kanunu'nun Bazı Maddelerinin Uygulanması Hakkında Karar
- `TEBLIG`       : Gümrük Genel Tebliğleri, YGM Tebliği, OKS Tebliği, TIR Tebliği, Nihai Kullanım, Tarife, DİR Tebliği, kara taşıtları tebliği, asgari ücret tebliği vb.
- `GIK_YON`      : Gümrük İşlemlerinin Kolaylaştırılması Yönetmeliği
- `DIS_TIC_MEVZ` : İthalat Rejimi Kararı, İGV Kararı, DİR Kararı, sınır ticareti, serbest bölgeler kanunu, gümrüksüz satış mağazaları yönetmeliği, GATT, KDV/ÖTV kanunları vb.
- `GENEL_MEVZ`   : soru belirli bir mevzuat adı vermiyor ve genel gümrük mevzuatı/dış ticaret bilgisi soruyor ("gümrük mevzuatına göre" vb.)
- `YOK`          : Türkçe/Matematik/Tarih/Anayasa

## 6. Serbest metin alanları (Türkçe, kısa)
- `alt_konu`: 2-6 kelimelik spesifik alt konu (ör. "Özet beyan verilme süresi", "Antrepo tipleri", "Kaçakçılıkta örgüt artırımı", "Sözcükte mecaz anlam")
- `ozet`: sorunun ne sorduğunun tek cümlelik özeti (max ~20 kelime)
- `anahtar_bilgi`: doğru cevabın verdiği öğrenilmesi gereken bilgi, tek cümle (ör. "Özet beyan kapsamı eşyaya denizyolunda 45 gün, diğer yollarda 20 gün içinde GOİK verilir.") — doğru cevap harfi verildi, o seçeneğin içeriğini kullan
- `zorluk`: `KOLAY` / `ORTA` / `ZOR` (mevzuat detay düzeyine ve çeldiricilere göre kendi değerlendirmen)
