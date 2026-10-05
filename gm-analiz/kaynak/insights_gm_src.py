"""insights_gm.json üretir: yıl yorumları, tarife/hesap notları, sonuç. Sayılar sınıflandırmadan hesaplanır."""
import json
from collections import Counter
from labels_gm import KONU2GRUP, YEARS
from tekrar_gm import tekrar

Q = [q for y in YEARS for q in json.load(open(f"cls_{y}.json", encoding="utf-8"))]
by = {y: [q for q in Q if q["yil"] == y] for y in YEARS}
K = lambda y, k: sum(q["konu"] == "GM_" + k for q in by[y])
G = lambda y, g: sum(KONU2GRUP[q["konu"]] == g for q in by[y])
KOK = lambda y, k: sum(q["kok"] == k for q in by[y])
TIP = lambda y, t: sum(q["tip"] == t for q in by[y])
MEV = lambda y, m: sum(q["mevzuat"] == m for q in by[y])
Z = lambda y, z: sum(q["zorluk"] == z for q in by[y])
H = lambda y: TIP(y, "HESAPLAMA")
HK = lambda y, h: sum(q["hesap"] == h for q in by[y] if q["tip"] == "HESAPLAMA")
F = lambda y: len({f for q in by[y] for f in q["fasil"]})
FY = lambda y, f: sum(f in q["fasil"] for q in by[y])
tot = lambda fn: sum(fn(y) for y in YEARS)
TAR = lambda y: K(y, "TARIFE_SINIF")
GRP_DT = "Dış Ticaret Politikası & Uluslararası Ticaret"
GRP_REJ = "Gümrük Rejimleri"
GRP_IC = "İç Vergiler, Kambiyo & Fonlar"
GRP_GEN = "Genel Hükümler, İşlemler & Meslek"
GRP_VER = "Vergi Alacağı, Ceza & Kaçakçılık"
GRP_MEN = "Menşe & Tercihli Ticaret"
b = lambda s: f"<b>{s}</b>"

years = {
 "2021": [
  f"Sınav konu bloklarıyla kurulmuş: 1–40 genel hükümler, beyan ve muafiyetler; {b('41–50 tamamen kaçakçılık')} (5607 ve akaryakıt/elkonulan eşya yönetmelikleri); 51–80 dış ticaret, kambiyo ve rejimler; {b('81–90 hesap bloğu')}; {b('91–100 tarife sınıflandırma')}.",
  f"En çok soru {b(f'Kaçakçılık ({K(2021,chr(75)+chr(65)+chr(67)+chr(65)+chr(75)+chr(67)+chr(73)+chr(76)+chr(73)+chr(75))})')} ve {b(f'Tarife Sınıflandırma ({TAR(2021)})')} konularından geldi; ardından Gümrük Kıymeti ({K(2021,'KIYMET')}) ve Özet Beyan–Geçici Depolama ({K(2021,'GIRIS_BEYAN')}) var. Kaçakçılığa 10 soru ayrılan tek yıl bu; sonraki yıllarda 2–4 soruya iniyor.",
  f"Genel hükümler ve tanımlar ({K(2021,'TEMEL')} soru: risk, gizlilik, çalışma saatleri, gümrük vergileri tanımı) bu yıl belirgin; 2023'ten itibaren bu başlıkta hiç soru yok. {b('STA ve tercihli menşe belgelerinden hiç soru gelmedi')}; sonraki dört yılda yılda 5–8 soru çıkıyor.",
  f"Soru kalıbında {b(f'olumsuz kök %{KOK(2021,chr(79)+chr(76)+chr(85)+chr(77)+chr(83)+chr(85)+chr(90))}')} ile beş yılın en yüksek oranında; öncüllü (I-II-III) soru yalnızca {KOK(2021,'ONCULLU')}. Doğrudan 4458 sayılı Kanun'a dayanan {MEV(2021,'GK_4458')} soru da beş yılın zirvesi: 2021 sınavı kanun metnini ölçen, en klasik sınav.",
  f"Hesap bloğu {H(2021)} soru: kıymet {HK(2021,'KIYMET')}, KDV matrahı {HK(2021,'KDV_MATRAH')}, uzlaşma ve ceza 1'er. Kültür fonunun uzlaşmaya konu olmaması (82) ve lisans ücretinde 3 yıllık zamanaşımı (83) gibi ayrıntılar hesapla birlikte soruluyor.",
  f"Beş yılın en kolay sınavı: {Z(2021,'KOLAY')} kolay, {Z(2021,'ORTA')} orta, {Z(2021,'ZOR')} zor. Tarife soruları {F(2021)} farklı fasıla yayılıyor; 96. fasıl 3 soruyla öne çıkıyor.",
 ],
 "2022": [
  f"Elimizdeki dosya {b('B kitapçığı')}; sorular A kitapçığına göre karışık sıralandığından optik formda blok yapısı daha az belirgin. Yine de tarife soruları 75–88, hesap soruları 89–100 aralığında toplanıyor.",
  f"En çok soru {b(f'Tarife Sınıflandırma ({TAR(2022)})')} ve {b(f'Gümrük Kıymeti ({K(2022,chr(75)+chr(73)+chr(89)+chr(77)+chr(69)+chr(84))})')} konularından geldi. Arkasından STA–menşe belgeleri, transit ve ÖTV ({K(2022,'OTV')}) geliyor.",
  f"{b(f'Dış ticaret politikası grubu {G(2022,GRP_DT)} soruyla')} beş yılın zirvesinde: ihracat mevzuatı (konsinye, bedelsiz ihracat, 96/31 yasak mallar), ithalat rejimi ve ek mali yükümlülük, teknik düzenlemeler ({K(2022,'TEKNIK_DUZENLEME')}), damping ve sınır ticareti. Dayanak olarak dış ticaret mevzuatı ({MEV(2022,'DIS_TIC_MEVZ')} soru) ilk kez Gümrük Kanunu'nu ({MEV(2022,'GK_4458')}) geçiyor.",
  f"Hesap soruları {H(2022)}'e çıktı: kıymet {HK(2022,'KIYMET')}, ÖTV {HK(2022,'OTV')} (sigarada nispi/maktu vergi), asgari–azami gümrük vergisi, antrepo götürü teminatı ve kendiliğinden bildirimde ceza. 94. sorunun cevap anahtarı (466.200 TL) standart hesapla elde edilemiyor; standart kurgu 452.000 TL (B) veriyor.",
  f"Kalıp değişimi bu yıl başlıyor: {b(f'öncüllü soru {KOK(2022,chr(79)+chr(78)+chr(67)+chr(85)+chr(76)+chr(76)+chr(85))}')} (2021'de {KOK(2021,'ONCULLU')}), olumsuz kök %{KOK(2022,'OLUMSUZ')}. Zor soru sayısı {Z(2022,'ZOR')}.",
  f"Tarifede HS 2022 değişiklikleri doğrudan soruldu: yenilebilir böcekler (04.10) ve elektronik sigara–24.04 ayrımı. Balina (01.06) ve ortopedik ayakkabı (90.21) gibi \"fasıl dışı\" tuzaklar bu yıl başlıyor ve sonraki yıllarda tekrarlanıyor.",
 ],
 "2023": [
  f"{b(f'Tarife bloğu sınavın başına alındı (4–21) ve {TAR(2023)} soruya çıktı')}: beş yılın en yüksek tarife payı (2024'le birlikte). 84. fasıl tek başına {FY(2023,'84')} soru getirdi (kültivatör, conta takımı, cep hesap makinesi, lehim makinesi, ısı değiştirici).",
  f"{b(f'Hesap ağırlığı zirvede: {H(2023)} hesap sorusu')}, çoğu 66–84 aralığında. Bunların {HK(2023,'KIYMET')}'u kıymet hesabı. 72–73. sorular ortak senaryolu; 72'de şıklar metindeki tutarların 10 katıyla kurulmuş, 73'te anahtar (D) test ücretini de KDV matrahına katıyor, standart hesap C (5.085.000) veriyor.",
  f"STA–menşe belgeleri ({K(2023,'TERCIHLI_STA')}), transit (86–93 bloğu, {K(2023,'TRANSIT')} soru) ve kambiyo ({K(2023,'KAMBIYO')}: ihracat bedellerinin yurda getirilmesi, kıymetli maden ithali) güçlendi. Gemi–uçak, ihrakiye ve kumanya ({K(2023,'OZEL_TASIT')}) bu yıl en çok soru aldığı seviyede.",
  f"{b(f'Kolay soru yalnızca {Z(2023,chr(75)+chr(79)+chr(76)+chr(65)+chr(89))}')}, zor soru {Z(2023,'ZOR')}: beş yılın en az kolay soru içeren sınavı. Olumlu kök {KOK(2023,'OLUMLU')}'e çıktı, öncüllü soru {KOK(2023,'ONCULLU')}, vaka/senaryo sorusu {TIP(2023,'VAKA_UYGULAMA')}.",
  f"Uluslararası anlaşmalara dayanan soru {MEV(2023,'ULUSLARARASI')}'e yükseldi (TIR, CISG, Gümrük Kıymeti Komitesi, 1/95 OKK, TPS-OIC). Bu eğilim 2024 ve 2025'te de sürüyor.",
 ],
 "2024": [
  f"{b(f'Tarife {TAR(2024)} soru (çoğu 44–60 aralığında)')} ve {b(f'{F(2024)} farklı fasıl')}: beş yılın en geniş fasıl yayılımı. 85. fasıl {FY(2024,'85')} soru (düz panel ekran modülü, LED, akıllı kart); kauçuk–silikon, ayakkabı aksamı, römorkör ve buz pisti makinesi gibi tek tek eşya soruları ağırlıkta.",
  f"{b(f'Gümrük rejimleri grubu {G(2024,GRP_REJ)} soruyla')} öne çıktı: transit {K(2024,'TRANSIT')} (TIR karnesi, kefil, LRN), antrepo {K(2024,'ANTREPO')} (götürü teminat, kapatma, geri gönderme), DİR {K(2024,'DIR')} ve geçici ithalat {K(2024,'GECICI_ITHALAT')}.",
  f"Kıymet ({K(2024,'KIYMET')}) ve hesap ({H(2024)}) soruları bu kez sınavın başında, 9–29 aralığında. Royalti–lisans (13, 15, 23), satın alma komisyonu, kullanılmış taşıt amortismanı ve gözetim farkı KDV'si soruldu.",
  f"{b(f'Beş yılın en zor sınavı: {Z(2024,chr(90)+chr(79)+chr(82))} zor soru')}. Antrepo götürü teminatı ve DİR süreleri gibi tebliğ ayrıntısı isteyen sorular zorluğu artırıyor. Olumsuz kök %{KOK(2024,'OLUMSUZ')}, öncüllü {KOK(2024,'ONCULLU')}.",
  f"Muafiyetler {K(2024,'MUAFIYET')} soruyla en yüksek seviyede; bunların 3'ü geri gelen eşya (istisnalar, elde olmayan sebepler, sürenin başlangıcı). STA–menşe belgeleri {K(2024,'TERCIHLI_STA')} soru: anlaşma–belge eşleştirmeleri ve taraf ülkeler.",
 ],
 "2025": [
  f"Tarife {TAR(2025)} soru (39–55), transit {b(f'{K(2025,chr(84)+chr(82)+chr(65)+chr(78)+chr(83)+chr(73)+chr(84))} soruluk tek blok (65–72)')}, STA–menşe belgeleri {K(2025,'TERCIHLI_STA')}. Bu üç konu birlikte sınavın üçte birini oluşturuyor.",
  f"{b('Yeni başlıklar geldi')}: damga vergisi ve transfer fiyatlandırması (1, 4, 5), GATT VII isteğe bağlı kıymet unsurları (3), TKA ön karar kapsamı (6), nihai kullanım ve gümrük statü belgesi (21–24). İç vergiler, kambiyo ve fonlar grubu {G(2025,GRP_IC)} soruyla beş yılın en yükseği.",
  f"{b(f'Gümrük Kıymeti {K(2025,chr(75)+chr(73)+chr(89)+chr(77)+chr(69)+chr(84))} soruya düştü')}: beş yılın en düşük seviyesi. Hesap soruları da {H(2025)} ile en az; çoğu 12–20 aralığında. 12. soruda anahtar (464) ardiyeyi KDV matrahına katmıyor; ardiye eklenirse 484 (E) çıkıyor.",
  f"{b('En çeşitli soru kalıbı bu yılda')}: öncüllü {KOK(2025,'ONCULLU')} (beş yılın zirvesi), boşluk doldurma {KOK(2025,'BOSLUK')}, eşleştirme/sıralama {KOK(2025,'ESLESTIRME_SIRALAMA')}. Olumlu kök {KOK(2025,'OLUMLU')}'a geriledi.",
  f"Sınav sonu yine meslek ve kolaylaştırma soruları: YYS ve OKS ({K(2025,'KOLAYLASTIRMA')}), YGM tespit kodları (98, 100) ve asgari ücret tarifesi (99). Zorluk: {Z(2025,'KOLAY')} kolay, {Z(2025,'ORTA')} orta, {Z(2025,'ZOR')} zor.",
 ],
}

tar_tot = tot(TAR)
fas_all = Counter(f for q in Q for f in q["fasil"])
tarife_not = (
 "<h3 style='margin-bottom:6px'>Tarife soruları nereden geliyor?</h3><ul class='notes'>"
 f"<li>5 yılda {b(f'{tar_tot} tarife sınıflandırma sorusu')} var (yılda {TAR(2021)}→{TAR(2025)}) ve bu sorular {len(fas_all)} farklı fasla dağılıyor. "
 f"En çok soru gelen fasıllar 84 ve 85 ({fas_all['84']}'ar soru), ardından 24 ({fas_all['24']}), 44, 64, 87 ve 96 ({fas_all['96']}'er).</li>"
 "<li>Bölüm bazında makine ve elektrikli cihazlar (XVI) ile gıda, içecek ve tütün (IV) açık ara önde. Canlı hayvanlar (I) ve kimya (VI) izliyor.</li>"
 f"<li>Soruların {sum(q['kok']=='OLUMSUZ' for q in Q if q['konu']=='GM_TARIFE_SINIF')}'ü olumsuz köklü: "
 "\"hangisi farklı fasılda yer alır\", \"hangisi bu pozisyonda değildir\". Tek eşyanın pozisyonunu soran sorudan çok, fasıl ve pozisyon kapsamını bilmeyi ölçen karşılaştırmalı sorular ağırlıkta.</li>"
 "<li>HS 2022 değişiklikleri her yıl soruluyor: yenilebilir böcekler 04.10 (2022/79, 2024/2), elektronik sigara ve 24.04 (2022/86, 2025/52), düz panel ekran modülleri 85.24 (2024/56), sıcak izostatik presler 85.14 (2025/45).</li>"
 "<li>Fasıl ve bölüm notları en verimli çalışma alanı: 64. fasıl not 2 (ayakkabı aksamı; 2024 ve 2025), 3. fasıl notu (memeliler 01.06'da; 2022 ve 2025), 42.02 pozisyon metni (2023'te iki soru) ve ısıtma tertibatlı ön camın taşıt aksamı sayılması (2023 ve 2025) tekrar soruldu.</li></ul>"
)

hes_tot = tot(H)
hesap_not = (
 "<h3 style='margin-bottom:6px'>Hesap sorularında neler öne çıkıyor?</h3><ul class='notes'>"
 f"<li>5 yılda {b(f'{hes_tot} hesap sorusu')} var (yılda {min(H(y) for y in YEARS)}–{max(H(y) for y in YEARS)}). "
 f"Bunların {b(str(tot(lambda y: HK(y,'KIYMET'))))}'u gümrük kıymeti, {tot(lambda y: HK(y,'KDV_MATRAH'))}'u KDV matrahı veya KDV tutarı. "
 f"Hesap sorularının {sum(q['zorluk']=='ZOR' for q in Q if q['tip']=='HESAPLAMA')}'u zor düzeyde.</li>"
 "<li>Kıymet hesabında hep aynı ayrımlar sınanıyor: satış komisyonu eklenir, satın alma komisyonu eklenmez; satış şartı olan royalti eklenir, Türkiye'de çoğaltma hakkı eklenmez; alıcının bedelsiz sağladığı girdiler eklenir; ithalat sonrası montaj ve Türkiye'deki nakliye eklenmez.</li>"
 "<li>KDV matrahına gümrük kıymetine ek olarak tescile kadar yapılan giderler (ardiye, fazla mesai, varış yerine kadar taşıma) eklenir, tescil sonrası giderler eklenmez. Kullanılmış taşıt amortismanı dört yılda soruldu ve 3 yıllık zamanaşımı hesap sorusunun içine yerleştiriliyor.</li>"
 "<li>Hesap bloğunun yeri yıldan yıla değişiyor: 2021'de 81–90, 2022'de 89–100, 2023'te 66–84, 2024'te 9–29, 2025'te 12–20.</li>"
 "<li><b>Cevap anahtarı tartışmalı hesaplar:</b> 2022/94 (anahtar 466.200; standart hesap 452.000), 2023/72–73 (şıklar metindeki tutarların 10 katı; 73'te standart hesap 5.085.000, anahtar 5.095.000), "
 "2025/12 (anahtar 464; ardiye KDV matrahına eklenirse 484) ve 2025/16 (anahtar model yılından sayıyor; fatura yılından sayılırsa 7.000). "
 "Hesap dışında 2021/4'ün anahtarı da itiraza açık: Türkiye'de çoğaltma hakkı için yapılan ödemeler de kıymete dahil edilmeyen unsurlardandır.</li></ul>"
)

ort = lambda fn: tot(fn) / len(YEARS)
sonuc = {"paragraflar": [
 {"baslik": "En çok soru gelen konular", "maddeler": [
   f"{b('Tarife sınıflandırma')} sınavın bel kemiği: 5 yılda {tar_tot} soru, son üç yılda {min(TAR(y) for y in (2023,2024,2025))}–{max(TAR(y) for y in (2023,2024,2025))} soru. Tarife mevzuatıyla birlikte her yıl ortalama {ort(lambda y: G(y,'Tarife & Sınıflandırma')):.0f} soru bu alandan geliyor.",
   f"{b('Gümrük kıymeti')} ikinci sırada ({tot(lambda y: K(y,'KIYMET'))} soru), ancak 2025'te {K(2025,'KIYMET')} soruya düştü. Kıymet sorularının yarıdan fazlası hesap sorusu.",
   f"{b('Transit ve TIR')} ({tot(lambda y: K(y,'TRANSIT'))}) ile {b('STA–tercihli menşe belgeleri')} ({tot(lambda y: K(y,'TERCIHLI_STA'))}) en hızlı yükselen konular: 2021'de 1 ve 0 soru, 2025'te {K(2025,'TRANSIT')} ve {K(2025,'TERCIHLI_STA')} soru.",
   f"Muafiyetler (2009/15481, geri gelen eşya; {tot(lambda y: K(y,'MUAFIYET'))}), kaçakçılık ({tot(lambda y: K(y,'KACAKCILIK'))}), antrepo ({tot(lambda y: K(y,'ANTREPO'))}) ve kambiyo ({tot(lambda y: K(y,'KAMBIYO'))}) her yıl düzenli soru alan ikinci halka.",
   "Düşüşte olanlar: genel hükümler ve tanımlar (2023'ten beri yok), özet beyan–geçici depolama ve kaçakçılık (2021'deki 8 ve 10 sorudan 2025'te 2'ye).",
 ]},
 {"baslik": "En çok sorulan soru tipleri ve kalıpları", "maddeler": [
   f"{b('Kapsam ve şart')} soruları ({tot(lambda y: TIP(y,'KAPSAM_SART'))}) ve {b('doğru/yanlış hüküm')} soruları ({tot(lambda y: TIP(y,'DOGRU_YANLIS_HUKUM'))}) beş yılın toplamında ilk iki sırada; bunları tarife sınıflandırma ({tot(lambda y: TIP(y,'SINIFLANDIRMA'))}) ve hesap ({hes_tot}) izliyor.",
   f"Olumsuz kök (\"değildir, yanlıştır, söylenemez\") 5 yılda {tot(lambda y: KOK(y,'OLUMSUZ'))} soru (%{tot(lambda y: KOK(y,'OLUMSUZ'))/5:.0f}). Öncüllü soru 2021'de {KOK(2021,'ONCULLU')} iken 2025'te {KOK(2025,'ONCULLU')}: tek tek öncülleri değerlendirmek giderek daha önemli.",
   f"Soruların yalnızca %{tot(lambda y: MEV(y,'GK_4458'))/5:.0f}'si doğrudan Gümrük Kanunu'na dayanıyor. Yönetmelik ({tot(lambda y: MEV(y,'GY'))}), tarife cetveli ({tot(lambda y: MEV(y,'TGTC'))}), tebliğler ({tot(lambda y: MEV(y,'TEBLIG'))}) ve uluslararası anlaşmalar ({tot(lambda y: MEV(y,'ULUSLARARASI'))}) daha belirleyici.",
   "Süre, oran ve tutar soruları (geri gelen eşyada 3 yıl, özet beyanda 150 gün, FSMH'de 3/10 iş günü, KKDF ve tek ve maktu vergi oranları) her yıl 5–9 soru. Bu değerler mevzuat değiştikçe güncellendiği için güncel metinden çalışılmalı.",
 ]},
 {"baslik": "Sınavın değişen yönü", "maddeler": [
   "2021 kanun metni ve kaçakçılık ağırlıklı, klasik bir sınavdı. 2023'ten itibaren sınav tarife, kıymet hesabı, transit ve tercihli menşe üzerine kuruluyor ve uluslararası anlaşmalar (TIR, GATT VII, TKA, 1/95 OKK, TPS-OIC) daha çok soruluyor.",
   "2025 sınavı yeni konular açtı: damga vergisi, transfer fiyatlandırması, nihai kullanım ve gümrük statü belgesi. 2026 için bu başlıkların devam etmesi beklenebilir.",
   f"Aynı bilgi yıllar içinde tekrar soruluyor: tekrar tablosundaki {len(tekrar())} kalıp, çıkmış soruların konu konu çalışılmasının en verimli yöntem olduğunu gösteriyor.",
 ]},
]}

out = dict(years=years, tekrar=tekrar(), sonuc=sonuc, tarife_not=tarife_not, hesap_not=hesap_not)
json.dump(out, open("insights_gm.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("insights_gm.json yazıldı")
