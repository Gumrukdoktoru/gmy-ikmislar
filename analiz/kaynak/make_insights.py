import json
ins = {}
ins["years"] = {
"2021": [
 "Sınavı <b>Ankara Üniversitesi (ASYM)</b> hazırladı; 2022'den itibaren Hacettepe Üniversitesi hazırlıyor. 2021'in konu dağılımı bu yüzden diğer yıllardan belirgin biçimde farklı.",
 "En çok soru <b>Kaçakçılık (5607)</b> konusundan geldi: <b>10 soru</b>, üstelik 91–100 arası bloğun tamamı. Beş yıl içinde tek bir konudan yılda gelen en yüksek ikinci sayı bu.",
 "<b>Gümrük Müşavirliği & Temsil</b> ve <b>Muafiyetler</b> 8'er soruyla ikinci sırada. Liman bayileri, kabotaj, posta kolisi listesi gibi <b>özel işlemler</b> (6 soru) ile <b>tasfiye</b> (5 soru) yalnızca bu yıl bu kadar ağırlık taşıdı.",
 "Gümrük Kanunu'nun <b>idari para cezaları (md. 234–241) hiç sorulmadı</b>. Ceza ağırlığı tamamen 5607'de.",
 "Soru tipinde <b>tanım soruları zirvede</b> (15). \"Ne ad verilir\" kalıbı çok sık (çeki listesi, proforma fatura, üçgen trafik, ulusal transit).",
 "Kalıp: %58 olumlu, %34 olumsuz kök, 7 öncüllü ve 1 eşleştirme (kontrol hatlarının renkleri). Matematikte işlem ve örüntü, tarihte Millî Mücadele ağırlıktaydı."
],
"2022": [
 "Yılın konusu <b>Gümrük Kıymeti</b>: <b>11 soru</b> (47–56 ve 98–99) ile beş yılın tek konudan gelen en yüksek sayısı. Aynı eşya, benzer eşya, ilişkili kişiler, royalti, hesaplanmış kıymet, komisyonlar ve kur çevrimi soruldu.",
 "Sınav <b>Kaçakçılık bloğuyla</b> açıldı (21–27, 7 soru). Ardından <b>özet beyan, geçici depolama, beyan ve muayene</b> (7) ile <b>GK idari para cezaları ve itiraz</b> (6) geliyor.",
 "<b>Olumsuz kök oranı %42</b> ile beş yılın en yüksek değeri. \"Hangisi yanlıştır / değildir\" kalıbı her 5 sorudan 2'sinde var.",
 "2009/15481 Karar'dan 5 soru geldi (hediyelik eşya limiti 150/430 Avro, taşıt muafiyeti, kişisel/şahsi eşya). Ayrıca o yıla ait <b>241/1 usulsüzlük cezası tutarı</b> (235 TL) soruldu; güncel tutarlar takip edilmeli.",
 "Matematik okul düzeyinde temel işlemdi (denklem, bileşik kesir, üslü sayılar, bölünebilme). 7 ve 8. sorular PDF'te görsel olduğu için sayfa görüntüsünden doğrulandı."
],
"2023": [
 "<b>Kanun'un genel hükümleri yılı</b>: <b>Temel Kavramlar</b> (11) ve <b>Özet Beyan / Beyan & Muayene</b> (11) birlikte gümrük sorularının %27,5'ini oluşturuyor. Gümrük idaresi, gümrük statüsü, yükümlü, Türkiye Gümrük Bölgesi, Kanun'un amacı ve brüt ağırlık tanımları soruldu.",
 "Sorular \"Gümrük Kanunu'na göre…\" diye başlıyor: <b>46/80 soru doğrudan 4458'e dayanıyor</b> (beş yılın en yükseği).",
 "<b>Meslek mevzuatı 8 soru</b>: disiplin cezaları (uyarma, kınama, 6 ay–1 yıl alıkoyma, meslekten çıkarma), sınava en fazla 3 kez giriş hakkı, 5 yıl belge saklama.",
 "<b>Sayısal sorular zirvede</b> (19): BTB 6 yıl, BMB 3 yıl, 45/20 gün, tebligat zamanaşımı 3 yıl, kısmi muafiyet %3.",
 "<b>En kolay sınav</b>: 49 soru kolay, yalnızca 8 soru zor. Transit, serbest dolaşım, kolaylaştırma (YYS/OKS) ve tasfiyeden hiç soru gelmedi. Matematiğin 5 sorusu da günlük hayat problemiydi."
],
"2024": [
 "Ağırlık <b>rejimlere ve vergilendirme unsurlarına</b> kaydı. <b>İdari para cezaları</b> (8), <b>Kıymet</b> (7), <b>Menşe</b> (7), <b>Dış Ticaret Politikası</b> (6) ve <b>Transit</b> (6) öne çıkıyor.",
 "<b>En zor sınav</b> (17 zor soru) ve <b>vaka sorularının zirvesi</b> (9). Rejim içinde hangi cezanın uygulanacağı soruldu: geçici ithalatta bilgisiz çıkış, ihraçta %10 fark, 235/2-a, transitte aykırılık, kaçakçılıkta teşebbüs, Erenköy→Sarp transitinin sona ermesi.",
 "Menşe bloğu (29–41): tümüyle elde edilen eşya, yetersiz işçilik, menşe şahadetnamesinin içeriği, GTS'de Form A, Çin→Almanya→Türkiye trafiğinde menşe ve serbest dolaşım ayrımı.",
 "Dış ticaret politikasında İthalat Rejimi Kararı listeleri, ek mali yükümlülük, İGV, kota, GTS ve sınır ticareti soruldu. <b>Gümrük Yönetmeliği'ne dayanan 20 soru</b> ile beş yılın en yükseği.",
 "Olumsuz kök %37, 7 öncüllü soru var. Doğru şıklarda <b>B</b> 28 kez çıktı; D ise yalnızca 12 kez."
],
"2025": [
 "<b>Gümrük rejimleri grubu 27/80</b> ile beş yılın en yükseği. <b>Dahilde İşleme</b> (7, 54–60 bloğu), <b>Serbest Dolaşım & Nihai Kullanım</b> (5) ve <b>Geçici İthalat</b> (5) öne çıkıyor.",
 "En çok soru <b>Menşe</b> konusundan geldi: <b>9 soru</b> (33–44). A.TR ile EUR.1 ayrımı, yetersiz işçilik, tümüyle elde edilen eşya, menşe şahadetnamesinin 6 ay içinde sonradan ibrazı ve basım yetkilisi TOBB/TESK/TİM soruldu.",
 "<b>Soru kalıbı değişti</b>: <b>17 öncüllü</b> (önceki yıllarda 4–7) ve <b>5 boşluk doldurma</b> sorusu var. Olumsuz kök %24'e indi (beş yılın en düşüğü).",
 "Mevzuat kaynağı genişledi. 4458'e dayanan soru 21'e düştü; <b>tebliğler</b> (9: Nihai Kullanım, Tarife/BTB, Seri 149, Kara Taşıtları) ve <b>dış ticaret mevzuatı</b> (6) zirve yaptı.",
 "<b>Hesap soruları</b> geldi: kendiliğinden başvuruda ceza tutarı, kullanılmış taşıtta yıl düşümü, EXW'den kıymet. Kaçakçılık 3 soruya geriledi. Genel yetenekte matematik çok temel günlük hayat problemleriydi."
]
}
ins["tekrar"] = [
 {"kalip":"Antrepo tipleri (A–F; genel/özel)","konu":"G_ANTREPO","sorular":{"2021":[54],"2022":[68,72],"2023":[85],"2024":[63]},"bilgi":"Genel antrepo: A, B ve F tipi; özel antrepo: C, D ve E tipi. A tipinde işletici stok kaydını tutar ve noksanlıktan sorumludur; E tipinde stok kaydı eşya izin hak sahibinin depolama yerine ulaşınca yapılır."},
 {"kalip":"Özet beyan sonrası GOİK verilme süresi","konu":"G_GIRIS_BEYAN","sorular":{"2021":[36],"2022":[32],"2023":[39,74]},"bilgi":"Denizyolu ile gelen eşyada 45 gün, diğer yollarda 20 gün."},
 {"kalip":"Geri gelen eşyada süre ve süre aşımı","konu":"G_MUAFIYET","sorular":{"2021":[30,64],"2023":[53],"2024":[71],"2025":[49]},"bilgi":"İhraçtan itibaren 3 yıl içinde geri gelirse muafiyet; süre fiilî ihraç (ör. uçağın hareketi) tarihinden başlar."},
 {"kalip":"Yolcu eşyası ambarı / depolama süresi","konu":"G_MUAFIYET","sorular":{"2021":[40],"2023":[50],"2025":[71,84]},"bilgi":"Yolcu eşyası ambarlarında ve geçici depolama yerlerinde 3 ay."},
 {"kalip":"Geçici ithalat rejiminin tanımı","konu":"G_GECICI_ITHALAT","sorular":{"2021":[45,75],"2023":[54],"2025":[79]},"bilgi":"Serbest dolaşımda olmayan eşyanın tam/kısmi muafiyetle kullanılıp olağan yıpranma dışında değişmeden yeniden ihracı."},
 {"kalip":"Kısmi muafiyette aylık vergi oranı","konu":"G_GECICI_ITHALAT","sorular":{"2021":[53],"2023":[37],"2024":[72]},"bilgi":"Rejimde kalınan her ay için, serbest dolaşıma girseydi alınacak vergilerin %3'ü."},
 {"kalip":"Sonradan tespit edilen vergide tebligat zamanaşımı","konu":"G_TAHAKKUK_TAHSIL","sorular":{"2023":[70],"2024":[79],"2025":[90]},"bilgi":"Gümrük yükümlülüğünün doğduğu tarihten itibaren 3 yıl."},
 {"kalip":"Ek tahakkukta ödeme süresi","konu":"G_TAHAKKUK_TAHSIL","sorular":{"2022":[88],"2024":[81],"2025":[91]},"bilgi":"Tebliğden itibaren 15 gün; yazılı istem ve teminatla 30 güne kadar uzatılabilir."},
 {"kalip":"İtiraz süresi ve karar süresi (GK 242)","konu":"G_CEZA_ITIRAZ","sorular":{"2022":[66],"2023":[77],"2024":[95]},"bilgi":"Tebliğden itibaren 15 gün içinde bir üst makama; itiraz 30 gün içinde karara bağlanır."},
 {"kalip":"Kaçakçılıkla mücadelede görevli olmayan","konu":"G_KACAKCILIK","sorular":{"2021":[93],"2022":[25],"2023":[22]},"bilgi":"Mülki amirler, Emniyet, Jandarma, Sahil Güvenlik ve gümrük muhafaza görevlidir; askerî birlikler ve özel güvenlik görevli değildir."},
 {"kalip":"Alıcı ile satıcı arasında ilişki sayılan haller","konu":"G_KIYMET","sorular":{"2022":[99],"2023":[98],"2024":[28]},"bilgi":"Tek acentelik veya aynı sanayi kolunda faaliyet göstermek tek başına ilişki sayılmaz."},
 {"kalip":"Kıymette yabancı paranın çevrilmesi","konu":"G_KIYMET","sorular":{"2021":[35],"2022":[55],"2024":[25]},"bilgi":"Yükümlülüğün başladığı tarihte geçerli TCMB döviz satış kuru."},
 {"kalip":"Alıcının kendi hesabına pazarlama faaliyeti","konu":"G_KIYMET","sorular":{"2021":[31],"2022":[52],"2024":[23]},"bilgi":"Satıcıya dolaylı ödeme sayılmaz, kıymete eklenmez (GK 27/1-b yardımı da değildir)."},
 {"kalip":"Aynı / benzer eşya unsurları","konu":"G_KIYMET","sorular":{"2022":[48,98],"2024":[27]},"bilgi":"Benzer eşyada kalite, itibar ve ticari marka dikkate alınır; fiyat bir unsur değildir."},
 {"kalip":"Gümrük rejimi olan/olmayan, ekonomik etkili rejimler","konu":"G_TEMEL_KAVRAM","sorular":{"2021":[26,43],"2022":[28,33],"2023":[63]},"bilgi":"Kanun'da 8 rejim var. Geçici ihracat ve nihai kullanım rejim değildir; transit ekonomik etkili rejim değildir."},
 {"kalip":"Şartlı muafiyet düzenlemesinin kapsamı","konu":"G_TEMEL_KAVRAM","sorular":{"2022":[62],"2023":[83],"2024":[30]},"bilgi":"Transit, antrepo, şartlı muafiyet sistemli DİR, GKAİ ve geçici ithalat; geri ödeme sistemi ve ihracat değildir."},
 {"kalip":"GOİK (gümrükçe onaylanmış işlem veya kullanım) kapsamı","konu":"G_TEMEL_KAVRAM","sorular":{"2022":[31],"2023":[31],"2024":[93]},"bilgi":"Rejime tabi tutma, serbest bölgeye girme, yeniden ihraç, imha ve gümrüğe terk. Teslim ve geçici depolama GOİK değildir."},
 {"kalip":"Telafi edici vergi (DİR'de tercihli tarife)","konu":"G_DAHILDE_ISLEME","sorular":{"2021":[89],"2022":[46],"2024":[54]},"bilgi":"Tercihli tarife, bünyedeki serbest dolaşımda olmayan eşyanın vergilerinin ödenmesine bağlıysa TEV doğar ve ihracat beyannamesinin tescil tarihine göre hesaplanır."},
 {"kalip":"Serbest dolaşım statüsünün kaybı","konu":"G_SERBEST_DOLASIM","sorular":{"2021":[42],"2022":[39],"2025":[31]},"bilgi":"Beyannamenin iptali ve geri ödeme sistemli DİR'de vergilerin geri verilmesi statüyü kaybettirir; nihai kullanım kaybettirmez."},
 {"kalip":"Tümüyle elde edilen eşya / yetersiz işçilik","konu":"G_MENSE","sorular":{"2023":[64],"2024":[33,34],"2025":[33,38,41]},"bilgi":"İthal girdiyle üretilen ürün tümüyle elde edilmiş sayılmaz. Tarife pozisyonu değişikliği ve iplikten kumaş üretimi yetersiz işçilik değildir."},
 {"kalip":"Rejim kodunun açıklaması","konu":"G_IHRACAT","sorular":{"2023":[52],"2024":[49],"2025":[53]},"bilgi":"1000: daha önce rejime tabi tutulmamış eşyanın kesin ihracatı. 1040: muafiyete tabi olmadan serbest dolaşım ile eş zamanlı yurt içi kullanıma giren eşyanın kesin ihracatı. 1023: geri gelmek üzere geçici ihraç edilen eşyanın kesin ihracatı."},
 {"kalip":"İthalat Rejimi Kararı eki listeler","konu":"G_DIS_TICARET_POL","sorular":{"2022":[35],"2024":[31],"2025":[37]},"bilgi":"I tarım ürünleri, II sanayi ürünleri, III işlenmiş tarım ürünleri, IV balıkçılık ve su ürünleri, V gümrük vergisi askıya alınan sanayi ürünleri, VI sivil hava taşıtlarında kullanılacak ürünler."},
 {"kalip":"Gümrük müşavir yardımcısı olma şartları","konu":"G_MESLEK","sorular":{"2021":[83],"2022":[63],"2025":[98]},"bilgi":"T.C. vatandaşlığı, medeni hakları kullanma ehliyeti, kamu haklarından mahrum olmamak, memuriyetten çıkarılmamış olmak, sayılan suçlardan hüküm giymemiş olmak."},
 {"kalip":"Yetkilendirilmiş yükümlü ve onaylanmış kişi şartları ve süreleri","konu":"G_KOLAYLASTIRMA","sorular":{"2021":[25],"2022":[93],"2024":[75,76],"2025":[87,88]},"bilgi":"YYS için en az 3 yıl faaliyet, OKS için 2 yıl; YYS süresizdir ve 5 yılda bir izlenir."},
 {"kalip":"Teminat olarak kabul edilmeyen değer","konu":"G_YUKUMLULUK_TEMINAT","sorular":{"2022":[92],"2025":[92]},"bilgi":"Kabul edilenler: nakit TL, süresiz banka teminat mektubu, DİBS ve TCMB'nin kabul ettiği dövizler. Soru iki yılda da 92. sırada."},
 {"kalip":"Bilgi değişikliğini bildirme süresi","konu":"G_MESLEK","sorular":{"2021":[84],"2023":[26]},"bilgi":"İzin belgesi numarası, şirket adı, temsilci gibi bilgilerdeki değişiklik bir hafta içinde bildirilir."},
 {"kalip":"İlişkinin beyan edilmemesi cezası","konu":"G_CEZA_ITIRAZ","sorular":{"2023":[43],"2024":[26]},"bilgi":"Vergi kaybı olmasa da 241/1'deki tutarın iki katı usulsüzlük cezası."},
 {"kalip":"Çeki listesinin tanımı","konu":"G_DIS_TIC_BELGE","sorular":{"2021":[49],"2022":[81]},"bilgi":"Kaplardaki eşya miktarını gösteren belge çeki listesidir. Soru metni iki yılda birebir aynı."},
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
ins["yontem"] = ("Kaynak, depodaki beş A kitapçığı PDF'i: 2021 (Ankara Üniversitesi ASYM), 2022–2025 (Hacettepe Üniversitesi). "
 "Doğru cevaplar PDF'lerde kırmızıyla işaretlenmiş seçeneklerden otomatik okundu ve 500 sorunun hepsi için bulundu. "
 "2022'nin görsel olan 7. ve 8. soruları sayfa görüntüsünden doğrulandı. "
 "Her soru sabit bir taksonomiye göre sınıflandırıldı: bölüm, 47 konu (27'si gümrük), 8 gümrük konu grubu, 5 soru kalıbı, 11 soru tipi, 8 mevzuat kaynağı ve zorluk. "
 "Soru kalıbı ayrıca metin kalıbı taramasıyla çapraz kontrol edildi. "
 "Konu, tip ve zorluk atamaları yoruma dayanır; sınırda kalan sorular, kökünde geçen kavrama göre atandı. "
 "\"Öğrenilecek bilgi\" alanı resmî cevap anahtarına dayanır. Bu bilgiler, özellikle her yıl güncellenen ceza tutarları ve süreler, mevzuatın güncel metninden ayrıca kontrol edilmelidir.")
json.dump(ins, open("insights.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
