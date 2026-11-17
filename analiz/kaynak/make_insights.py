import json
ins = {}
ins["years"] = {
"2021": [
 "Sınavı <b>Ankara Üniversitesi (ASYM)</b> hazırladı; 2022'den itibaren Hacettepe Üniversitesi hazırlıyor. 2021'in konu dağılımı bu yüzden diğer yıllardan belirgin biçimde farklı.",
 "En çok soru <b>Kaçakçılık (5607)</b> konusundan geldi: <b>10 soru</b>, üstelik 91–100 arası bloğun tamamı. Altı yıl içinde tek bir konudan yılda gelen en yüksek ikinci sayı bu.",
 "<b>Gümrük Müşavirliği & Temsil</b> ve <b>Muafiyetler</b> 8'er soruyla ikinci sırada. Liman bayileri, kabotaj, posta kolisi listesi gibi <b>özel işlemler</b> (6 soru) ile <b>tasfiye</b> (5 soru) yalnızca bu yıl bu kadar ağırlık taşıdı.",
 "Gümrük Kanunu'nun <b>idari para cezaları (md. 234–241) hiç sorulmadı</b>. Ceza ağırlığı tamamen 5607'de.",
 "Soru tipinde <b>tanım soruları zirvede</b> (15). \"Ne ad verilir\" kalıbı çok sık (çeki listesi, proforma fatura, üçgen trafik, ulusal transit).",
 "Kalıp: %58 olumlu, %34 olumsuz kök, 7 öncüllü ve 1 eşleştirme (kontrol hatlarının renkleri). Matematikte işlem ve örüntü, tarihte Millî Mücadele ağırlıktaydı."
],
"2022": [
 "Yılın konusu <b>Gümrük Kıymeti</b>: <b>11 soru</b> (47–56 ve 98–99) ile altı yılın tek konudan gelen en yüksek sayısı. Aynı eşya, benzer eşya, ilişkili kişiler, royalti, hesaplanmış kıymet, komisyonlar ve kur çevrimi soruldu.",
 "Sınav <b>Kaçakçılık bloğuyla</b> açıldı (21–27, 7 soru). Ardından <b>özet beyan, geçici depolama, beyan ve muayene</b> (7) ile <b>GK idari para cezaları ve itiraz</b> (6) geliyor.",
 "<b>Olumsuz kök oranı %42</b> ile altı yılın en yüksek değeri (2026'da %41). \"Hangisi yanlıştır / değildir\" kalıbı her 5 sorudan 2'sinde var.",
 "2009/15481 Karar'dan 5 soru geldi (hediyelik eşya limiti 150/430 Avro, taşıt muafiyeti, kişisel/şahsi eşya). Ayrıca o yıla ait <b>241/1 usulsüzlük cezası tutarı</b> (235 TL) soruldu; güncel tutarlar takip edilmeli.",
 "Matematik okul düzeyinde temel işlemdi (denklem, bileşik kesir, üslü sayılar, bölünebilme)."
],
"2023": [
 "<b>Kanun'un genel hükümleri yılı</b>: <b>Temel Kavramlar</b> (11) ve <b>Özet Beyan / Beyan & Muayene</b> (11) birlikte gümrük sorularının %27,5'ini oluşturuyor. Gümrük idaresi, gümrük statüsü, yükümlü, Türkiye Gümrük Bölgesi, Kanun'un amacı ve brüt ağırlık tanımları soruldu.",
 "Sorular \"Gümrük Kanunu'na göre…\" diye başlıyor: <b>46/80 soru doğrudan 4458'e dayanıyor</b> (altı yılın en yükseği).",
 "<b>Meslek mevzuatı 8 soru</b>: disiplin cezaları (uyarma, kınama, 6 ay–1 yıl alıkoyma, meslekten çıkarma), sınava en fazla 3 kez giriş hakkı, 5 yıl belge saklama.",
 "<b>Sayısal sorular zirvede</b> (19): BTB 6 yıl, BMB 3 yıl, 45/20 gün, tebligat zamanaşımı 3 yıl, kısmi muafiyet %3.",
 "<b>En kolay sınav</b>: 49 soru kolay, yalnızca 8 soru zor. Transit, serbest dolaşım, kolaylaştırma (YYS/OKS) ve tasfiyeden hiç soru gelmedi. Matematiğin 5 sorusu da günlük hayat problemiydi."
],
"2024": [
 "Ağırlık <b>rejimlere ve vergilendirme unsurlarına</b> kaydı. <b>İdari para cezaları</b> (8), <b>Kıymet</b> (7), <b>Menşe</b> (7), <b>Dış Ticaret Politikası</b> (6) ve <b>Transit</b> (6) öne çıkıyor.",
 "<b>En zor sınav</b> (17 zor soru) ve <b>vaka sorularının zirvesi</b> (9). Rejim içinde hangi cezanın uygulanacağı soruldu: geçici ithalatta bilgisiz çıkış, ihraçta %10 fark, 235/2-a, transitte aykırılık, kaçakçılıkta teşebbüs, Erenköy→Sarp transitinin sona ermesi.",
 "Menşe bloğu (29–41): tümüyle elde edilen eşya, yetersiz işçilik, menşe şahadetnamesinin içeriği, GTS'de Form A, Çin→Almanya→Türkiye trafiğinde menşe ve serbest dolaşım ayrımı.",
 "Dış ticaret politikasında İthalat Rejimi Kararı listeleri, ek mali yükümlülük, İGV, kota, GTS ve sınır ticareti soruldu. <b>Gümrük Yönetmeliği'ne dayanan 20 soru</b> ile altı yılın en yükseği.",
 "Olumsuz kök %37, 7 öncüllü soru var. Doğru şıklarda <b>B</b> 28 kez çıktı; D ise yalnızca 12 kez."
],
"2025": [
 "<b>Gümrük rejimleri grubu 27/80</b> ile altı yılın en yükseği. <b>Dahilde İşleme</b> (7, 54–60 bloğu), <b>Serbest Dolaşım & Nihai Kullanım</b> (5) ve <b>Geçici İthalat</b> (5) öne çıkıyor.",
 "En çok soru <b>Menşe</b> konusundan geldi: <b>9 soru</b> (33–44). A.TR ile EUR.1 ayrımı, yetersiz işçilik, tümüyle elde edilen eşya, menşe şahadetnamesinin 6 ay içinde sonradan ibrazı ve basım yetkilisi TOBB/TESK/TİM soruldu.",
 "<b>Soru kalıbı değişti</b>: <b>17 öncüllü</b> (önceki yıllarda 4–7) ve <b>5 boşluk doldurma</b> sorusu var. Olumsuz kök %24'e indi (altı yılın en düşüğü).",
 "Mevzuat kaynağı genişledi. 4458'e dayanan soru 21'e düştü; <b>tebliğler</b> (9: Nihai Kullanım, Tarife/BTB, Seri 149, Kara Taşıtları) ve <b>dış ticaret mevzuatı</b> (6) zirve yaptı.",
 "<b>Hesap soruları</b> geldi: kendiliğinden başvuruda ceza tutarı, kullanılmış taşıtta yıl düşümü, EXW'den kıymet. Kaçakçılık 3 soruya geriledi. Genel yetenekte matematik çok temel günlük hayat problemleriydi."
]
}
ins["tekrar"] = [
 {"kalip":"Antrepo tipleri (A–F; genel/özel)","konu":"G_ANTREPO","sorular":{"2021":[54],"2022":[68,72],"2023":[85],"2024":[63],"2026":[57, 62]},"bilgi":"Genel antrepo: A, B ve F tipi; özel antrepo: C, D ve E tipi. A tipinde işletici stok kaydını tutar ve noksanlıktan sorumludur; E tipinde stok kaydı eşya izin hak sahibinin depolama yerine ulaşınca yapılır."},
 {"kalip":"Özet beyan sonrası GOİK verilme süresi","konu":"G_GIRIS_BEYAN","sorular":{"2021":[36],"2022":[32],"2023":[39,74]},"bilgi":"Denizyolu ile gelen eşyada 45 gün, diğer yollarda 20 gün."},
 {"kalip":"Geri gelen eşyada süre ve süre aşımı","konu":"G_MUAFIYET","sorular":{"2021":[30,64],"2023":[53],"2024":[71],"2025":[49],"2026":[49]},"bilgi":"İhraçtan itibaren 3 yıl içinde geri gelirse muafiyet; süre fiilî ihraç (ör. uçağın hareketi) tarihinden başlar."},
 {"kalip":"Yolcu eşyası ambarı / depolama süresi","konu":"G_MUAFIYET","sorular":{"2021":[40],"2023":[50],"2025":[71,84]},"bilgi":"Yolcu eşyası ambarlarında ve geçici depolama yerlerinde 3 ay."},
 {"kalip":"Geçici ithalat rejiminin tanımı","konu":"G_GECICI_ITHALAT","sorular":{"2021":[45,75],"2023":[54],"2025":[79],"2026":[71, 72]},"bilgi":"Serbest dolaşımda olmayan eşyanın tam/kısmi muafiyetle kullanılıp olağan yıpranma dışında değişmeden yeniden ihracı."},
 {"kalip":"Kısmi muafiyette aylık vergi oranı","konu":"G_GECICI_ITHALAT","sorular":{"2021":[53],"2023":[37],"2024":[72]},"bilgi":"Rejimde kalınan her ay için, serbest dolaşıma girseydi alınacak vergilerin %3'ü."},
 {"kalip":"Sonradan tespit edilen vergide tebligat zamanaşımı","konu":"G_TAHAKKUK_TAHSIL","sorular":{"2023":[70],"2024":[79],"2025":[90]},"bilgi":"Gümrük yükümlülüğünün doğduğu tarihten itibaren 3 yıl."},
 {"kalip":"Ek tahakkukta ödeme süresi","konu":"G_TAHAKKUK_TAHSIL","sorular":{"2022":[88],"2024":[81],"2025":[91]},"bilgi":"Tebliğden itibaren 15 gün; yazılı istem ve teminatla 30 güne kadar uzatılabilir."},
 {"kalip":"İtiraz süresi ve karar süresi (GK 242)","konu":"G_CEZA_ITIRAZ","sorular":{"2022":[66],"2023":[77],"2024":[95],"2026":[80]},"bilgi":"Tebliğden itibaren 15 gün içinde bir üst makama; itiraz 30 gün içinde karara bağlanır."},
 {"kalip":"Kaçakçılıkla mücadelede görevli olmayan","konu":"G_KACAKCILIK","sorular":{"2021":[93],"2022":[25],"2023":[22]},"bilgi":"Mülki amirler, Emniyet, Jandarma, Sahil Güvenlik ve gümrük muhafaza görevlidir; askerî birlikler ve özel güvenlik görevli değildir."},
 {"kalip":"Alıcı ile satıcı arasında ilişki sayılan haller","konu":"G_KIYMET","sorular":{"2022":[99],"2023":[98],"2024":[28],"2026":[21, 28]},"bilgi":"Tek acentelik veya aynı sanayi kolunda faaliyet göstermek tek başına ilişki sayılmaz."},
 {"kalip":"Kıymette yabancı paranın çevrilmesi","konu":"G_KIYMET","sorular":{"2021":[35],"2022":[55],"2024":[25],"2026":[30]},"bilgi":"Yükümlülüğün başladığı tarihte geçerli TCMB döviz satış kuru."},
 {"kalip":"Alıcının kendi hesabına pazarlama faaliyeti","konu":"G_KIYMET","sorular":{"2021":[31],"2022":[52],"2024":[23]},"bilgi":"Satıcıya dolaylı ödeme sayılmaz, kıymete eklenmez (GK 27/1-b yardımı da değildir)."},
 {"kalip":"Aynı / benzer eşya unsurları","konu":"G_KIYMET","sorular":{"2022":[48,98],"2024":[27]},"bilgi":"Benzer eşyada kalite, itibar ve ticari marka dikkate alınır; fiyat bir unsur değildir."},
 {"kalip":"Gümrük rejimi olan/olmayan, ekonomik etkili rejimler","konu":"G_TEMEL_KAVRAM","sorular":{"2021":[26,43],"2022":[28,33],"2023":[63],"2026":[89]},"bilgi":"Kanun'da 8 rejim var. Geçici ihracat ve nihai kullanım rejim değildir; transit ekonomik etkili rejim değildir."},
 {"kalip":"Şartlı muafiyet düzenlemesinin kapsamı","konu":"G_TEMEL_KAVRAM","sorular":{"2022":[62],"2023":[83],"2024":[30]},"bilgi":"Transit, antrepo, şartlı muafiyet sistemli DİR, GKAİ ve geçici ithalat; geri ödeme sistemi ve ihracat değildir."},
 {"kalip":"GOİK (gümrükçe onaylanmış işlem veya kullanım) kapsamı","konu":"G_TEMEL_KAVRAM","sorular":{"2022":[31],"2023":[31],"2024":[93],"2026":[32]},"bilgi":"Rejime tabi tutma, serbest bölgeye girme, yeniden ihraç, imha ve gümrüğe terk. Teslim ve geçici depolama GOİK değildir."},
 {"kalip":"Telafi edici vergi (DİR'de tercihli tarife)","konu":"G_DAHILDE_ISLEME","sorular":{"2021":[89],"2022":[46],"2024":[54]},"bilgi":"Tercihli tarife, bünyedeki serbest dolaşımda olmayan eşyanın vergilerinin ödenmesine bağlıysa TEV doğar ve ihracat beyannamesinin tescil tarihine göre hesaplanır."},
 {"kalip":"Serbest dolaşım statüsünün kaybı","konu":"G_SERBEST_DOLASIM","sorular":{"2021":[42],"2022":[39],"2025":[31],"2026":[39]},"bilgi":"Beyannamenin iptali ve geri ödeme sistemli DİR'de vergilerin geri verilmesi statüyü kaybettirir; nihai kullanım kaybettirmez."},
 {"kalip":"Tümüyle elde edilen eşya / yetersiz işçilik","konu":"G_MENSE","sorular":{"2023":[64],"2024":[33,34],"2025":[33,38,41],"2026":[37]},"bilgi":"İthal girdiyle üretilen ürün tümüyle elde edilmiş sayılmaz. Tarife pozisyonu değişikliği ve iplikten kumaş üretimi yetersiz işçilik değildir."},
 {"kalip":"Rejim kodunun açıklaması","konu":"G_IHRACAT","sorular":{"2023":[52],"2024":[49],"2025":[53]},"bilgi":"1000: daha önce rejime tabi tutulmamış eşyanın kesin ihracatı. 1040: muafiyete tabi olmadan serbest dolaşım ile eş zamanlı yurt içi kullanıma giren eşyanın kesin ihracatı. 1023: geri gelmek üzere geçici ihraç edilen eşyanın kesin ihracatı."},
 {"kalip":"İthalat Rejimi Kararı eki listeler","konu":"G_DIS_TICARET_POL","sorular":{"2022":[35],"2024":[31],"2025":[37]},"bilgi":"I tarım ürünleri, II sanayi ürünleri, III işlenmiş tarım ürünleri, IV balıkçılık ve su ürünleri, V gümrük vergisi askıya alınan sanayi ürünleri, VI sivil hava taşıtlarında kullanılacak ürünler."},
 {"kalip":"Gümrük müşavir yardımcısı olma şartları","konu":"G_MESLEK","sorular":{"2021":[83],"2022":[63],"2025":[98],"2026":[94]},"bilgi":"T.C. vatandaşlığı, medeni hakları kullanma ehliyeti, kamu haklarından mahrum olmamak, memuriyetten çıkarılmamış olmak, sayılan suçlardan hüküm giymemiş olmak."},
 {"kalip":"Yetkilendirilmiş yükümlü ve onaylanmış kişi şartları ve süreleri","konu":"G_KOLAYLASTIRMA","sorular":{"2021":[25],"2022":[93],"2024":[75,76],"2025":[87,88],"2026":[73, 74]},"bilgi":"YYS için en az 3 yıl faaliyet, OKS için 2 yıl; YYS süresizdir ve 5 yılda bir izlenir."},
 {"kalip":"Teminat olarak kabul edilmeyen değer","konu":"G_YUKUMLULUK_TEMINAT","sorular":{"2022":[92],"2025":[92],"2026":[76]},"bilgi":"Kabul edilenler: nakit TL, süresiz banka teminat mektubu, DİBS ve TCMB'nin kabul ettiği dövizler. Soru iki yılda da 92. sırada."},
 {"kalip":"Bilgi değişikliğini bildirme süresi","konu":"G_MESLEK","sorular":{"2021":[84],"2023":[26]},"bilgi":"İzin belgesi numarası, şirket adı, temsilci gibi bilgilerdeki değişiklik bir hafta içinde bildirilir."},
 {"kalip":"İlişkinin beyan edilmemesi cezası","konu":"G_CEZA_ITIRAZ","sorular":{"2023":[43],"2024":[26]},"bilgi":"Vergi kaybı olmasa da 241/1'deki tutarın iki katı usulsüzlük cezası."},
 {"kalip":"Çeki listesinin tanımı","konu":"G_DIS_TIC_BELGE","sorular":{"2021":[49],"2022":[81]},"bilgi":"Kaplardaki eşya miktarını gösteren belge çeki listesidir. Soru metni iki yılda birebir aynı."},
 {"kalip":"Kıymet yöntemlerinin uygulama sırası","konu":"G_KIYMET","sorular":{"2021":[29],"2026":[22]},"bilgi":"Yöntemler sırayla uygulanır; beyan sahibinin yazılı talebi uygun bulunursa indirgeme yönteminden önce hesaplanmış kıymet yöntemi uygulanabilir."},
 {"kalip":"Menşe şahadetnamesinin içeriği","konu":"G_MENSE","sorular":{"2025":[35],"2026":[42]},"bilgi":"Menşe şahadetnamesinde gönderen ve alıcı, kapların marka, numara ve sayısı ile eşyanın cinsi ve menşe ülkesi yer alır."},
 {"kalip":"Fikri haklarda re'sen durdurma ve ihtiyati tedbir","konu":"G_DIS_TICARET_POL","sorular":{"2022":[30],"2026":[38, 40, 41]},"bilgi":"Açık delil varsa gümrük idaresi eşyayı hak sahibinin başvurusu için re'sen durdurur; hak sahibi süresinde ihtiyati tedbir getirmezse işlemlere devam edilir."},
 {"kalip":"İhracatta beyanname yerine geçen belgeler","konu":"G_IHRACAT","sorular":{"2024":[45],"2026":[44]},"bilgi":"ATA ve CPD karnesi, Form 302 ve kumanya listesi beyanname yerine kullanılabilir."},
 {"kalip":"Beyanname kapatma süresinin uzatılması","konu":"G_IHRACAT","sorular":{"2025":[95],"2026":[50]},"bilgi":"Geçici depolama yerine konulmadan ihraç edilecek eşyada kapatma süresi makul sebeplerle gümrük idaresince uzatılabilir."},
 {"kalip":"CPD karnesi","konu":"G_GECICI_ITHALAT","sorular":{"2022":[61],"2026":[70]},"bilgi":"Ticari ve kişisel kara taşıtları için kefil kuruluşlarca verilen uluslararası gümrük belgesidir."},
 {"kalip":"Kusurlu eşyada geri verme başvuru süresi","konu":"G_GERI_VERME","sorular":{"2025":[93],"2026":[77]},"bilgi":"Başvuru 3 yıl değil, vergilerin yükümlüye tebliğinden itibaren 1 yıl içinde yapılır."},
 {"kalip":"Hediyelik eşya muafiyet limiti","konu":"G_MUAFIYET","sorular":{"2022":[86],"2026":[83]},"bilgi":"15 yaş altı yolcular için 150 Avro, 15 yaş üstü yolcular için 430 Avro."},
 {"kalip":"Yasak ve kısıtlama gerekçeleri","konu":"G_DIS_TICARET_POL","sorular":{"2023":[72],"2026":[90]},"bilgi":"Kamu ahlakı, düzeni ve güvenliği; insan, hayvan ve bitki sağlığı; ulusal hazineler ve fikri-sınai haklar gerekçesiyle yasak ve kısıtlama konulabilir."},
 {"kalip":"Müşavirlerin belge saklama süresi","konu":"G_MESLEK","sorular":{"2023":[23],"2026":[92]},"bilgi":"Gümrük müşavirleri defter, vekaletname ve düzenledikleri belgeleri 5 yıl saklar."},
 {"kalip":"Disiplin cezalarında zamanaşımı","konu":"G_MESLEK","sorular":{"2023":[24],"2026":[93]},"bilgi":"Adli kovuşturma hali dışında disiplin cezaları aykırılığın tespitinden itibaren 3 yıl içinde uygulanmazsa zamanaşımına uğrar. Soru iki yılda neredeyse aynı metinle soruldu."},
 {"kalip":"Meslekten çıkarmada yetkili merci","konu":"G_MESLEK","sorular":{"2024":[90],"2026":[95]},"bilgi":"Meslekten çıkarma cezasını Ticaret Bakanlığı Yüksek Disiplin Kurulu verir."},
 {"kalip":"Kaçakçılıkta eşya türüne göre ceza artırımı","konu":"G_KACAKCILIK","sorular":{"2021":[96],"2026":[99]},"bilgi":"Akaryakıt, tütün, makaron, etil alkol ve yaprak sigara kâğıdı gibi eşyada ceza artırılır."},
]
ins["sonuc"] = {"paragraflar": [
 {"baslik":"En çok soru gelen konular", "maddeler":[
  "Puanın <b>%80'i gümrük mevzuatından</b> geliyor (her yıl 80/100). Genel yetenek ve genel kültür sabit 20 soru.",
  "Konu grubu olarak zirvede <b>Gümrük Rejimleri</b>: 400 sorunun 94'ü (%23,5). Ardından Genel Hükümler & Gümrük İşlemleri (70), Vergilendirme Unsurları (58), Ceza & Kaçakçılık (50) ve Meslek & Kolaylaştırma (47) geliyor.",
  "Tek konu olarak ilk sekiz: <b>Gümrük Kıymeti (29)</b>, Özet Beyan/Beyan & Muayene (28), Gümrük Müşavirliği & Temsil (27), Muafiyetler (26), Kaçakçılık (26), Temel Kavramlar (24), İdari Para Cezaları & İtiraz (24), Menşe (21). Bu sekiz konu gümrük sorularının <b>%51'ini</b> oluşturuyor.",
  "<b>12 konu beş sınavın hepsinde çıktı</b>: Kıymet, Özet Beyan/Beyan & Muayene, Meslek, Muafiyetler, Kaçakçılık, Temel Kavramlar, Dahilde İşleme, Geçici İthalat, Tahakkuk-Tahsil, Antrepo, YGM ve Geri Verme.",
  "Genel yetenek ve genel kültürde en çok matematik problemleri (15), Millî Mücadele (10), İnkılaplar & Atatürk İlkeleri (9), temel işlem (8) ve sözcükte anlam (7) soruldu."
 ]},
 {"baslik":"Eğilim: sınav nereye kayıyor?", "maddeler":[
  "<b>Yükselenler</b> (2021–22 ortalaması → 2024–25 ortalaması): <b>Menşe 0,5 → 8</b>, Dahilde İşleme 2 → 5,5, Dış Ticaret Politikası 2 → 5, Transit 3 → 5.",
  "<b>Düşenler</b>: <b>Kaçakçılık 8,5 → 3</b>, Özet Beyan/Beyan & Muayene 6 → 2,5, Meslek 6 → 3,5, Kıymet 7,5 → 5. Özel işlemler ve tasfiye neredeyse hiç sorulmuyor.",
  "Mevzuat kaynağı da değişiyor. 2023'te gümrük sorularının 46'sı doğrudan 4458'e dayanıyordu; 2025'te bu sayı 21'e indi. Yerini Gümrük Yönetmeliği, tebliğler (Nihai Kullanım, BTB, Kara Taşıtları) ve dış ticaret mevzuatı aldı.",
  "<b>2025'te soru kalıbı değişti</b>: 17 öncüllü (I-II-III) ve 5 boşluk doldurma sorusu geldi. Önceki yıllarda öncüllü soru sayısı 4–7 arasındaydı."
 ]},
 {"baslik":"Hangi soru tipi, hangi kalıpla soruluyor?", "maddeler":[
  "500 sorunun %56'sı olumlu, <b>%33'ü olumsuz köklü</b> (\"değildir / yanlıştır / yer almaz\"), %8'i öncüllü. Gümrük bölümünde olumsuz kök oranı %35,5.",
  "Gümrük sorularında en sık tip <b>Kapsam & Şart (%31)</b>, ardından <b>Sayısal (%18,5)</b>, <b>Doğru/Yanlış Hüküm (%17,5)</b>, Tanım (%12), Belge & Prosedür (%10,5), Yetkili Merci (%5,5) ve Vaka (%4) geliyor.",
  "Kapsam & şart sorularının <b>üçte ikisi olumsuz köklü</b> (124 sorunun 82'si). Tipik GMY sorusu şu kalıpta: \"… göre aşağıdakilerden hangisi X'in şartları / kapsamı arasında <u>yer almaz</u>?\"",
  "Sayısal sorular neredeyse her zaman olumlu köklü (74 sorunun 65'i) ve süre soruyor: kaç gün, kaç yıl, yüzde kaç. Doğru/yanlış hüküm sorularının 50/70'i \"hangisi yanlıştır\" biçiminde.",
  "Doğru şıklar dengeli dağılmış (A 73, B 106, C 111, D 99, E 111). Şık tahminine dayanan bir strateji işe yaramaz."
 ]},
 {"baslik":"Çalışma stratejisi", "maddeler":[
  "Önce <b>4458 sayılı Kanun + Gümrük Yönetmeliği</b> çalışılmalı: gümrük sorularının yaklaşık %62'si doğrudan bu ikisine dayanıyor.",
  "Bir <b>süreler ve oranlar tablosu</b> hazırlanmalı: 45/20 gün, 3 yıl tebligat, 15 gün ödeme ve itiraz, %3 kısmi muafiyet, 3 ay yolcu eşyası, 1 ay ihraç amaçlı depolama, BTB 6 yıl, BMB 3 yıl, 5 yıl belge saklama, menşe şahadetnamesi için 6 ay.",
  "<b>Sayılan listeler</b> ezberlenmeli, çünkü olumsuz köklü kapsam soruları bunlardan geliyor: rejimler, GOİK, şartlı muafiyet düzenlemesi, ilişkili kişiler, kabul edilmeyen teminatlar, kaçakçılıkla görevliler, disiplin cezaları, antrepo tipleri, tasfiye yöntemleri.",
  "Son iki yılın yönüne göre <b>menşe, dahilde işleme, transit, nihai kullanım, BTB, geçici ithalat ve İthalat Rejimi Kararı</b> konularına ağırlık verilmeli. Öncüllü ve boşluk doldurma sorularıyla pratik yapılmalı.",
  "<b>Tekrar eden soru kalıpları</b> tablosundaki bilgiler mutlaka bilinmeli. Bazı sorular yıllar içinde neredeyse aynı metinle tekrar soruldu (çeki listesi, ilişki beyanı cezası, teminat, bildirim süresi)."
 ]}
]}
ins["yontem"] = ("Kaynak, depodaki altı A kitapçığı PDF'i: 2021 (Ankara Üniversitesi ASYM), 2022–2026 (Hacettepe Üniversitesi). "
 "Doğru cevaplar PDF'lerde kırmızıyla işaretlenmiş seçeneklerden otomatik okundu ve 600 sorunun hepsi için bulundu. 2026'nın tablo biçimli 51. sorusu sayfa görüntüsünden doğrulandı. "
 "2022'nin görsel olan 7. ve 8. soruları sayfa görüntüsünden doğrulandı. "
 "Her soru sabit bir taksonomiye göre sınıflandırıldı: bölüm, 47 konu (27'si gümrük), 8 gümrük konu grubu, 5 soru kalıbı, 11 soru tipi, 8 mevzuat kaynağı ve zorluk. "
 "Soru kalıbı ayrıca metin kalıbı taramasıyla çapraz kontrol edildi. "
 "Konu, tip ve zorluk atamaları yoruma dayanır; sınırda kalan sorular, kökünde geçen kavrama göre atandı. "
 "\"Öğrenilecek bilgi\" alanı resmî cevap anahtarına dayanır. Bu bilgiler, özellikle her yıl güncellenen ceza tutarları ve süreler, mevzuatın güncel metninden ayrıca kontrol edilmelidir.")

# ---- veriden hesaplanan bölümler (sonuç ve 2026 yorumu) ----
import os as _os
from collections import Counter as _C
from labels import YEARS as _Y, KONU as _K, KONU2GRUP as _K2G, GRUP as _GR
_D = _os.path.dirname(_os.path.abspath(__file__))
_Q = [q for y in _Y for q in json.load(open(_os.path.join(_D, f"cls_{y}.json"), encoding="utf-8"))]
_G = [q for q in _Q if q["bolum"] == "GUMRUK"]
_by = lambda y, L=_G: [q for q in L if q["yil"] == y]
_kc = _C(q["konu"] for q in _G)
_h = len(_Y) // 2
_avg = lambda k, ys: sum(sum(q["konu"] == k for q in _by(y)) for y in ys) / len(ys)
_fmt = lambda x: f"{x:.1f}".replace(".", ",").replace(",0", "")
_pct = lambda a, b: f"%{a * 100 / b:.0f}"
_e, _l = f"{_Y[0]}–{str(_Y[_h-1])[2:]}", f"{_Y[-_h]}–{str(_Y[-1])[2:]}"
def _poss(n):
    if n % 10: return f"{n}'" + {1:"i",2:"si",3:"ü",4:"ü",5:"i",6:"sı",7:"si",8:"i",9:"u"}[n % 10]
    return f"{n}'" + {1:"u",2:"si",3:"u",4:"ı",5:"si",6:"ı",7:"i",8:"i",9:"ı"}[(n // 10) % 10]
_pp = lambda a, b: "%" + _poss(round(a * 100 / b))
_gc = _C(_K2G[q["konu"]] for q in _G)
_top = _kc.most_common(8)
_all = [k for k in _kc if all(sum(q["konu"] == k for q in _by(y)) for y in _Y)]
_tr = sorted(((_avg(k, _Y[-_h:]) - _avg(k, _Y[:_h]), k) for k in _kc), reverse=True)
_up = [f"{_K[k]} {_fmt(_avg(k, _Y[:_h]))} → {_fmt(_avg(k, _Y[-_h:]))}" for d, k in _tr[:4] if d > 0]
_dn = [f"{_K[k]} {_fmt(_avg(k, _Y[:_h]))} → {_fmt(_avg(k, _Y[-_h:]))}" for d, k in _tr[::-1][:4] if d < 0]
_kok = _C(q["kok"] for q in _Q); _kokg = _C(q["kok"] for q in _G)
_tip = _C(q["tip"] for q in _G)
_ks = [q for q in _G if q["tip"] == "KAPSAM_SART"]; _sy = [q for q in _G if q["tip"] == "SAYISAL"]
_dy = [q for q in _G if q["tip"] == "DOGRU_YANLIS_HUKUM"]
_cev = _C(q["cevap"] for q in _Q)
_mev = _C(q["mevzuat"] for q in _G)
_nong = [q for q in _Q if q["bolum"] != "GUMRUK"]; _nk = _C(q["konu"] for q in _nong).most_common(5)
TN = {"KAPSAM_SART": "Kapsam & Şart", "SAYISAL": "Sayısal", "DOGRU_YANLIS_HUKUM": "Doğru/Yanlış Hüküm", "TANIM": "Tanım",
      "BELGE_PROSEDUR": "Belge & Prosedür", "YETKILI_MERCI": "Yetkili Merci", "VAKA_UYGULAMA": "Vaka"}
ins["sonuc"] = {"paragraflar": [
 {"baslik": "En çok soru gelen konular", "maddeler": [
  f"Puanın <b>%80'i gümrük mevzuatından</b> geliyor (her yıl 80/100). Genel yetenek ve genel kültür sabit 20 soru.",
  f"Konu grubu olarak zirvede <b>{_gc.most_common(1)[0][0]}</b>: {len(_G)} sorunun {_poss(_gc.most_common(1)[0][1])} ({_pct(_gc.most_common(1)[0][1], len(_G))}). Ardından " + ", ".join(f"{g} ({n})" for g, n in _gc.most_common(5)[1:]) + " geliyor.",
  "Tek konu olarak ilk sekiz: " + ", ".join(f"{'<b>' if i == 0 else ''}{_K[k]} ({n}){'</b>' if i == 0 else ''}" for i, (k, n) in enumerate(_top))
  + f". Bu sekiz konu gümrük sorularının <b>{_pp(sum(n for _, n in _top), len(_G))}</b> oluşturuyor.",
  f"<b>{len(_all)} konu altı sınavın hepsinde çıktı</b>: " + ", ".join(_K[k] for k in sorted(_all, key=lambda k: -_kc[k])) + ".",
  "Genel yetenek ve genel kültürde en çok " + ", ".join(f"{_K[k]} ({n})" for k, n in _nk) + " soruldu.",
 ]},
 {"baslik": "Eğilim: sınav nereye kayıyor?", "maddeler": [
  f"<b>Yükselenler</b> ({_e} ortalaması → {_l} ortalaması): " + ", ".join(_up) + ".",
  f"<b>Düşenler</b>: " + ", ".join(_dn) + ". Özel işlemler ve tasfiye artık seyrek soruluyor.",
  f"Mevzuat kaynağı değişken: 4458'e dayanan gümrük sorusu 2023'te 46 iken 2025'te 21'e indi, 2026'da yeniden {sum(q['mevzuat'] == 'GK_4458' for q in _by(2026))} oldu. Gümrük Yönetmeliği, tebliğler ve 2009/15481 Karar her yıl düzenli soru alıyor.",
  f"Soru kalıbı yıldan yıla oynuyor: 2025'te 17 öncüllü ve 5 boşluk doldurma sorusu geldi; 2026'da öncüllü {sum(q['kok'] == 'ONCULLU' for q in _by(2026, _Q))}'ya indi, olumsuz kök {_pct(sum(q['kok'] == 'OLUMSUZ' for q in _by(2026, _Q)), 100)}'e çıktı.",
 ]},
 {"baslik": "Hangi soru tipi, hangi kalıpla soruluyor?", "maddeler": [
  f"{len(_Q)} sorunun {_pp(_kok['OLUMLU'], len(_Q))} olumlu, <b>{_pp(_kok['OLUMSUZ'], len(_Q))} olumsuz köklü</b> (\"değildir / yanlıştır / yer almaz\"), {_pp(_kok['ONCULLU'], len(_Q))} öncüllü. Gümrük bölümünde olumsuz kök oranı {_pct(_kokg['OLUMSUZ'], len(_G))}.",
  "Gümrük sorularında en sık tipler: " + ", ".join(f"{TN.get(t, t)} ({_pct(n, len(_G))})" for t, n in _tip.most_common(7)) + ".",
  f"Kapsam & şart sorularının çoğu olumsuz köklü ({len(_ks)} sorunun {_poss(sum(q['kok'] == 'OLUMSUZ' for q in _ks))}). Tipik GMY sorusu şu kalıpta: \"… göre aşağıdakilerden hangisi X'in şartları / kapsamı arasında <u>yer almaz</u>?\"",
  f"Sayısal sorular çoğunlukla olumlu köklü ({len(_sy)} sorunun {_poss(sum(q['kok'] == 'OLUMLU' for q in _sy))}) ve süre soruyor: kaç gün, kaç yıl, yüzde kaç. {len(_dy)} doğru/yanlış hüküm sorusunun {_poss(sum(q['kok'] == 'OLUMSUZ' for q in _dy))} \"hangisi yanlıştır\" biçiminde.",
  "Doğru şıklar dengeli dağılmış (" + ", ".join(f"{k} {_cev[k]}" for k in "ABCDE") + "). Şık tahminine dayanan bir strateji işe yaramaz.",
 ]},
 {"baslik": "Çalışma stratejisi", "maddeler": [
  f"Önce <b>4458 sayılı Kanun + Gümrük Yönetmeliği</b> çalışılmalı: gümrük sorularının {_pp(_mev['GK_4458'] + _mev['GY'], len(_G))} doğrudan bu ikisine dayanıyor.",
  "Bir <b>süreler ve oranlar tablosu</b> hazırlanmalı: 45/20 gün, 3 yıl tebligat, 15 gün ödeme ve itiraz, 30 gün itiraz kararı, %3 kısmi muafiyet, 3 ay yolcu eşyası, BTB 6 yıl, BMB 3 yıl, 5 yıl belge saklama, 3 yıl disiplin zamanaşımı, kusurlu eşyada 1 yıl, menşe şahadetnamesi için 6 ay.",
  "<b>Sayılan listeler</b> ezberlenmeli, çünkü olumsuz köklü kapsam soruları bunlardan geliyor: rejimler, GOİK, şartlı muafiyet düzenlemesi, ilişkili kişiler, kabul edilmeyen teminatlar, kaçakçılıkla görevliler, disiplin cezaları, antrepo tipleri, geçici ithalata konu olmayan eşya.",
  "Son yılların yönüne göre <b>gümrük kıymeti, muafiyetler, geçici ithalat, antrepo, ihracat, fikri haklar ve İthalat Rejimi Kararı</b> konularına ağırlık verilmeli. Öncüllü ve boşluk doldurma sorularıyla pratik yapılmalı.",
  "<b>Tekrar eden soru kalıpları</b> tablosundaki bilgiler mutlaka bilinmeli. 2026'da disiplin zamanaşımı, belge saklama süresi, hediyelik eşya limiti ve kusurlu eşyada geri verme süresi önceki yıllardaki metinlerle neredeyse aynı soruldu.",
 ]},
]}

_g6 = _by(2026); _a6 = _by(2026, _Q)
_k6 = lambda k: sum(q["konu"] == k for q in _g6)
ins["years"]["2026"] = [
 f"Sınavı yine Hacettepe Üniversitesi hazırladı (A kitapçığı). Gümrük bölümü bloklarla ilerliyor: 21–30 ağırlıkla kıymet, 31–42 serbest dolaşım, temel kavramlar, menşe ve fikri haklar, 43–50 ihracat ve özel işlemler, 56–62 antrepo, 63–66 transit, 67–72 geçici ithalat, 83–88 muafiyetler, 92–96 meslek, 97–100 kaçakçılık.",
 f"En çok soru <b>Gümrük Kıymeti</b> konusundan geldi: <b>{_k6('G_KIYMET')} soru</b> (2022'den sonraki en yüksek sayı). İlişkili kişiler, kıymet yöntemlerinin sırası, istisnai kıymet ve kur çevrimi soruldu; hesap sorusu gelmedi.",
 f"<b>Antrepo ({_k6('G_ANTREPO')}) ve ihracat ({_k6('G_IHRACAT')})</b> altı yılın en yüksek seviyesinde; geçici ithalat {_k6('G_GECICI_ITHALAT')}, muafiyetler {_k6('G_MUAFIYET')}, meslek {_k6('G_MESLEK')} soru. 2009/15481 Karar'a dayanan soru {sum(q['mevzuat'] == 'KARAR_2009_15481' for q in _g6)} ile altı yılın zirvesi. Menşe 2025'teki 9 sorudan {_k6('G_MENSE')}'ye indi.",
 f"Kalıpta olumsuz kök yeniden yükseldi: {sum(q['kok'] == 'OLUMSUZ' for q in _a6)}/100. Öncüllü soru {sum(q['kok'] == 'ONCULLU' for q in _a6)}'ya indi. <b>Doğru/yanlış hüküm</b> sorusu {sum(q['tip'] == 'DOGRU_YANLIS_HUKUM' for q in _g6)} ile altı yılın en yükseği; 4458'e dayanan soru yeniden {sum(q['mevzuat'] == 'GK_4458' for q in _g6)}'e çıktı.",
 "<b>Önceki yıllardan neredeyse aynı tekrar eden sorular</b>: disiplin cezalarında 3 yıl zamanaşımı (93 = 2023/24), müşavirlerin belge saklama süresi (92 = 2023/23), hediyelik eşya limiti 150/430 Avro (83 = 2022/86), kusurlu eşyada 1 yıl (77 = 2025/93), meslekten çıkarmada Yüksek Disiplin Kurulu (95 = 2024/90), CPD karnesi (70 = 2022/61).",
 f"Genel yetenekte matematik yine temel işlem ve problemdi. 10. soruda D ve E şıkları aynı (\"3 saat 40 dakika\"); bu bir soru hatası, B cevabını etkilemiyor. Zorluk: {sum(q['zorluk'] == 'KOLAY' for q in _a6)} kolay, {sum(q['zorluk'] == 'ZOR' for q in _a6)} zor soru.",
]

json.dump(ins, open("insights.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
