# GM (Gümrük Müşavirliği) Sınavı Sınıflandırma Taksonomisi — SABİT

Her soru için aşağıdaki alanları doldur. Kod alanlarında YALNIZCA bu listelerdeki kodları birebir kullan.
Sınavda genel yetenek/kültür bölümü YOKTUR; 100 sorunun tamamı mesleki konudur.

## 1. `konu` (sorunun asıl ölçtüğü konu — TEK kod)

### Genel hükümler, gümrük işlemleri, meslek
- `GM_TEMEL` : GK genel hükümleri ve tanımlar (md. 1-24 arası genel hükümler), "gümrük mevzuatının uygulanmasına ilişkin kararlar", bilgilerin gizliliği, risk tanımı, gümrük vergileri tanımı, gümrük idareleri/teşkilat (B sınıfı müdürlük, bölge müdürlükleri), belge saklama, eşyanın ağırlığı ve kapları, mücbir sebep, 1/95'e uyum DIŞINDAKİ genel kavramlar
- `GM_GIRIS_BEYAN` : eşyanın TGB'ye girişi, özet beyan (verilme, değiştirme, süreler, kimin vereceği), gümrüğe sunma, boşaltma, geçici depolama yerleri ve süreleri, GOİK verilme, gümrük beyanı/beyanname, basitleştirilmiş usuller (eksik beyan, tamamlayıcı beyan, yerinde gümrükleme, basitleştirilmiş usul kodları), muayene, tahlil, eşyanın teslimi, beyannameye eklenecek belgeler, çıkış özet beyanı
- `GM_OZEL_TASIT` : gemiler, uçaklar, taşıtların geçici çıkışı, ihrakiye, kumanya, akaryakıt, seferin devamı, kabotaj, fiili ihraç tarihi (taşıtlara ilişkin), Türk bandıralı gemi listeleri
- `GM_POSTA` : posta gümrük işlemleri, posta ve hızlı kargo tebliği, posta kolisi belgeleri
- `GM_TASFIYE` : tasfiyelik eşya, tasfiye süreleri ve işlemleri, terk, tahlilden arta kalan numunelerin terki
- `GM_SERBEST_BOLGE` : serbest bölgeler, gümrüksüz satış mağazaları, serbest bölgelerde yükümlülük
- `GM_MUAFIYET` : gümrük vergisi muafiyet ve istisnaları: 2009/15481 Karar (yolcu beraberi eşya, kesin dönüş, taşıt muafiyeti, diplomatik, standart depo, basılı yayın, hediyelik eşya, engelli vb.), GK 167 istisnaları, geri gelen eşya (GK 168-170), diplomatik eşyanın satış ve devri
- `GM_MESLEK` : gümrük müşavirliği, müşavir yardımcılığı, disiplin, temsil, Asgari Ücret Tarifesi tebliği
- `GM_YGM` : yetkilendirilmiş gümrük müşavirliği tebliği, tespit işlemleri ve rapor kodları
- `GM_KOLAYLASTIRMA` : yetkilendirilmiş yükümlü (YYS), onaylanmış kişi statüsü (OKS), Gümrük İşlemlerinin Kolaylaştırılması Yönetmeliği

### Gümrük rejimleri
- `GM_SERBEST_DOLASIM` : serbest dolaşıma giriş rejimi, statü kaybı, lehe oran (GK 74), nihai kullanım (izin, devir, sonradan verilme), gümrük statü belgesi
- `GM_ANTREPO` : antrepo rejimi, antrepo tipleri, antrepo izni ve geri alınması, antrepo götürü teminatı (alan/tank hesabı dahil), antrepoda devir, antrepoya konulabilecek eşya, orta/ağır kusur
- `GM_DIR` : dahilde işleme rejimi (izin, geri ödeme, şartlı muafiyet, eş değer eşya, TEV, DİR tebliği süreleri ve müeyyideleri)
- `GM_GKAI` : gümrük kontrolü altında işleme
- `GM_GECICI_ITHALAT` : geçici ithalat (tam/kısmi muafiyet, ATA karnesi, kara taşıtları tebliği, sözlü beyan, teminat aranan eşya, faiz)
- `GM_HIR` : hariçte işleme (standart değişim, tamir, geçici ihracat dilekçesi, vergilendirme)
- `GM_TRANSIT` : transit rejimi, transit tebliğleri (Seri 4,5,6), NCTS, GRN/LRN, kefil, izinli gönderici/alıcı, TIR sözleşmesi ve TIR karnesi, boru hattı
- `GM_IHRACAT` : gümrük mevzuatındaki ihracat rejimi işlemleri (ihracat beyannamesi, nüshalar, çıkış bildirimi, sözlü beyan edilecek eşya, beyanname kapatma, ticari kiralama yoluyla geçici ihracat işlemleri)

### Tarife ve sınıflandırma
- `GM_TARIFE_MEVZ` : gümrük tarifesi kavramı, BTB (geçerlilik, başvuru, düzenleyen bölge müdürlükleri), 474 sayılı Kanun ve Cumhurbaşkanı yetkisi, GTİP'in yapısı/hane anlamları (kavramsal)
- `GM_TARIFE_SINIF` : belirli bir eşyanın TGTC'de hangi fasıl/pozisyonda sınıflandırılacağı, fasıl/bölüm notları, GYK (Genel Yorum Kuralları) uygulaması, izahname

### Gümrük kıymeti
- `GM_KIYMET` : gümrük kıymeti (yöntemler, satış bedeli, ilişkili kişiler, aynı/benzer eşya, indirgeme, hesaplanmış kıymet, son yöntem, royalti ve lisans, ilaveler/indirimler, istisnai kıymet, Kıymet Tebliğleri, kullanılmış taşıt kıymeti) — hem kavramsal hem hesaplama soruları (hesap ise `tip`=HESAPLAMA)

### Menşe ve tercihli ticaret
- `GM_MENSE` : tercihli olmayan menşe kuralları, menşe kazanma (yetersiz işçilik, son esaslı işçilik, GY 5 no.lu ek), menşe şahadetnamesi (içerik, GY 205 vb.), BMB
- `GM_TERCIHLI_STA` : STA'lar ve taraf ülkeler, tercihli menşe ve dolaşım belgeleri (EUR.1, EUR-MED, A.TR, Form A, menşe beyanı, tedarikçi beyanı, D-8, TPS-OIC, Malezya vb.), belge vize/basım/ibraz süreleri, sonradan kontrol, kümülasyon (Pan-Avrupa-Akdeniz), GTS, AKÇT ürünleri, EFTA

### Vergi alacağı, ceza, kaçakçılık
- `GM_YUKUMLULUK_TEMINAT` : gümrük yükümlülüğünün doğuşu/sona ermesi, teminat (türleri, kabul edilen teminatlar, götürü teminat — antrepo götürü teminatı HARİÇ)
- `GM_TAHAKKUK_TAHSIL` : tahakkuk, tebliğ, ödeme süreleri, zamanaşımı, gecikme faizi/zammı, 6183, tecil-taksit, Tahsilat Tebliği (Seri 2), müteselsil sorumluluk
- `GM_GERI_VERME` : geri verme ve kaldırma
- `GM_CEZA_UZLASMA` : GK idari para cezaları (234-241), usulsüzlük cezaları (GY 82 no.lu ek), uzlaşma (GK 244), itiraz, kıymet/vergi farkı cezası hesapları, KDV cezası
- `GM_KACAKCILIK` : 5607 sayılı Kanun ve yönetmelikleri (suçlar, nitelikli haller, etkin pişmanlık, el koyma, akaryakıt, ikramiye, kamuoyuna ilan, davaya katılma)

### İç vergiler, kambiyo, fonlar
- `GM_KDV` : KDV Kanunu (ithalde KDV, matrah, oranlar, 2007/13033 BKK listeleri, sorumlu sıfatı, indirim, istisnalar) — KDV matrahı hesabı da buraya (`tip`=HESAPLAMA)
- `GM_OTV` : ÖTV Kanunu (listeler, ilk iktisap, ithalat tanımı, diplomatik istisna, ÖTV hesabı)
- `GM_DIGER_VERGI` : damga vergisi, Kurumlar Vergisi / transfer fiyatlandırması, VUK, diğer vergiler
- `GM_KAMBIYO` : 32 sayılı Karar (kıymetli maden/taş, Türk parası, ödeme belgeleri, efektif), TCMB genelgeleri (1-M, Sermaye Hareketleri, İhracat Genelgesi), ihracat bedellerinin yurda getirilmesi, kıymetli maden/altın ithali, yolcu beraberi Türk parası
- `GM_FONLAR` : KKDF (kesinti, oran, kur), Destekleme ve Fiyat İstikrar Fonu

### Dış ticaret politikası ve uluslararası ticaret
- `GM_ITHALAT_REJIMI` : İthalat Rejimi Kararı (3350), ek mali yükümlülük, ilave gümrük vergisi, özel nitelikli eşya, TPÖ mevzuatı, ithalatta vergi numarası, kontrol/izin belgeleri (Tarım Bakanlığı tebliği vb. ithalat denetimi HARİÇ → TEKNIK)
- `GM_DIS_TIC_IHRACAT` : İhracat Rejimi Kararı/Yönetmeliği, ihracı yasak ve ön izne bağlı mallar (96/31), kayda bağlı ihracat, konsinye ihracat, takas, ticari kiralama yoluyla ihracat (dış ticaret mevzuatı yönü), izne bağlı ihracat
- `GM_KORUNMA` : ithalatta haksız rekabet (damping, sübvansiyon), İHRDK, korunma önlemleri, gözetim
- `GM_TEKNIK_DUZENLEME` : ürün güvenliği ve teknik düzenlemeler (7223, TAREKS, CE işareti, uygunluk değerlendirme), GY 181 kontrolleri, Tarım ve Orman Bakanlığı kontrolüne tabi ürünler tebliği
- `GM_YATIRIM_SINIR` : yatırım teşvik (2012/3305), Doğrudan Yabancı Yatırımlar (4875), sınır ticareti (4874 sayılı Karar)
- `GM_FSMH` : fikri ve sınai hakların gümrükte korunması
- `GM_INCOTERMS` : teslim şekilleri (Incoterms 2020, ICC)
- `GM_ULUSLARARASI_TIC` : ödeme şekilleri, konşimento ve dış ticaret belgeleri, CISG (Viyana Satım Sözleşmesi), DTÖ/GATT, DGÖ, Gümrük Kıymeti Komitesi, Ticaretin Kolaylaştırılması Anlaşması, AB-Türkiye 1/95 OKK ve Gümrük Birliği'nin genel kapsamı, döviz kuru kavramı

Kararsız kalırsan sorunun KÖKÜNDE hangi düzenleme/kavram geçiyorsa onu seç. Hesaplama sorularında konu, hesaplanan büyüklüğe göre seçilir (gümrük kıymeti → GM_KIYMET; KDV matrahı/KDV → GM_KDV; ÖTV → GM_OTV; ceza/uzlaşma → GM_CEZA_UZLASMA; geçici ithalat vergisi → GM_GECICI_ITHALAT; GV/İGV tutarı → GM_KIYMET değil, eşyanın vergilendirildiği rejim/konu; emin değilsen GM_ITHALAT_REJIMI).

## 2. `kok` (TEK kod)
- `OLUMLU`, `OLUMSUZ` (değildir/yanlıştır/söylenemez/yer almaz/sınıflandırılamaz…), `ONCULLU` (I-II-III / i-ii-iii öncüllü; olumsuz olsa da ONCULLU), `BOSLUK` (boşluk doldurma), `ESLESTIRME_SIRALAMA` (eşleştirme tablosu veya sıralama)
Not: Ortak senaryo (i, ii, iii… verilerle hesap) içeren hesap soruları, öncüller seçenek olarak sorulmuyorsa ONCULLU DEĞİLDİR; kök yapısına göre OLUMLU/OLUMSUZ yaz.

## 3. `tip` (TEK kod)
- `TANIM`, `SAYISAL` (süre/oran/tutar/sayı bilgisi), `KAPSAM_SART`, `DOGRU_YANLIS_HUKUM`, `YETKILI_MERCI`, `BELGE_PROSEDUR`, `VAKA_UYGULAMA` (senaryoya kural uygulama, hesap gerekmiyorsa), `HESAPLAMA` (sayısal hesap gerektiren), `SINIFLANDIRMA` (eşyanın tarife pozisyonu/faslını belirleme, GYK uygulama), `OLGU_BILGI` (ülke listeleri, kuruluşlar, anlaşma adları gibi olgular)

## 4. `mevzuat` (TEK kod — dayanılan ana düzenleme)
- `GK_4458`, `GY` (Gümrük Yönetmeliği), `TEBLIG` (gümrük genel tebliğleri: transit, nihai kullanım, kıymet, tahsilat, posta, YGM, asgari ücret, OKS, kara taşıtları, DİR tebliği vb.), `GIK_YON`, `KARAR_2009_15481`, `KMK_5607`, `TGTC` (Tarife Cetveli, izahname, fasıl notları, GYK, 474 sayılı Kanun), `KDV_KANUNU`, `OTV_KANUNU`, `DIGER_VERGI` (damga, KV, VUK, 6183), `KAMBIYO_MEVZ` (32 sayılı Karar, TCMB genelgeleri, KKDF/DFİF kararları), `DIS_TIC_MEVZ` (ithalat/ihracat rejimi kararları ve yönetmelikleri, teknik düzenlemeler, korunma/damping, sınır ticareti, teşvik, DYY, serbest bölgeler, gümrüksüz satış), `ULUSLARARASI` (GATT/DTÖ anlaşmaları, STA ve menşe protokolleri, 1/95 OKK, TIR sözleşmesi, ATA, CISG, Incoterms), `GENEL` (belirli bir düzenleme adı yok / genel dış ticaret bilgisi)

## 5. Ek kodlu alanlar
- `zorluk`: `KOLAY` / `ORTA` / `ZOR`
- `hesap`: SADECE `tip`=HESAPLAMA ise doldur, değilse "" (boş). Kodlar: `KIYMET` (gümrük kıymeti), `KDV_MATRAH` (KDV matrahı/KDV tutarı), `OTV`, `GV_IGV` (gümrük vergisi/ilave GV tutarı), `CEZA` (idari para cezası/ek tahakkuk+ceza), `UZLASMA`, `GECICI_ITH_VERGI`, `ANTREPO_TEMINAT`, `DIGER`
- `fasil`: SADECE konu GM_TARIFE_SINIF veya tarife pozisyonu geçen sorular için; doğru cevapla ilgili TGTC fasıl numaraları, 2 haneli string listesi (ör. ["27"], ["84","85"]). GYK genel sorularında []. Diğer sorularda [].

## 6. Serbest metin alanları (Türkçe, kısa)
- `alt_konu`: 2-6 kelimelik spesifik alt konu (ör. "Özet beyan verilme süreleri", "Royaltinin kıymete eklenmesi", "64. fasıl ayakkabı aksamı")
- `madde`: biliniyorsa dayanılan madde/ek/not (ör. "GK md. 27", "GY md. 181", "84. fasıl not 9", "GYK 3(b)", "KDV K. md. 21"); bilinmiyorsa ""
- `sayisal`: SADECE `tip`=SAYISAL veya HESAPLAMA ise doğru cevaptaki değer ve birimi (ör. "30 gün", "%3", "5.300 USD"); diğerlerinde ""
- `ozet`: sorunun ne sorduğu, tek cümle (≤20 kelime)
- `anahtar_bilgi`: doğru cevaba dayanan öğrenilecek bilgi, tek-iki cümle. Hesap sorularında hesabın nasıl kurulduğunu kısa yaz (hangi kalemler eklendi/çıkarıldı). Sınıflandırma sorularında doğru pozisyon/fasıl ve gerekçeyi yaz. Cevap anahtarındaki harfi esas al; şüphen varsa "Cevap anahtarına göre…" diye başla.
