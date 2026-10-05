"""GM taksonomisi kodları için Türkçe adlar ve konu grupları."""

KONU = {
    "GM_TEMEL": "Genel Hükümler & Tanımlar",
    "GM_GIRIS_BEYAN": "Özet Beyan, Geçici Depolama, Beyan & Basitleştirmeler",
    "GM_OZEL_TASIT": "Gemi-Uçak, İhrakiye & Kumanya",
    "GM_POSTA": "Posta & Hızlı Kargo",
    "GM_TASFIYE": "Tasfiye",
    "GM_SERBEST_BOLGE": "Serbest Bölge & Gümrüksüz Satış",
    "GM_MUAFIYET": "Muafiyetler (2009/15481, Geri Gelen Eşya)",
    "GM_MESLEK": "Gümrük Müşavirliği & Asgari Ücret",
    "GM_YGM": "Yetkilendirilmiş Gümrük Müşavirliği",
    "GM_KOLAYLASTIRMA": "YYS & Onaylanmış Kişi",
    "GM_SERBEST_DOLASIM": "Serbest Dolaşım & Nihai Kullanım",
    "GM_ANTREPO": "Antrepo Rejimi",
    "GM_DIR": "Dahilde İşleme Rejimi",
    "GM_GKAI": "Gümrük Kontrolü Altında İşleme",
    "GM_GECICI_ITHALAT": "Geçici İthalat",
    "GM_HIR": "Hariçte İşleme",
    "GM_TRANSIT": "Transit Rejimi & TIR",
    "GM_IHRACAT": "İhracat Rejimi (Gümrük İşlemleri)",
    "GM_TARIFE_MEVZ": "Tarife Mevzuatı & BTB",
    "GM_TARIFE_SINIF": "Tarife Sınıflandırma (GTİP)",
    "GM_KIYMET": "Gümrük Kıymeti",
    "GM_MENSE": "Menşe Kuralları",
    "GM_TERCIHLI_STA": "STA & Tercihli Menşe Belgeleri",
    "GM_YUKUMLULUK_TEMINAT": "Gümrük Yükümlülüğü & Teminat",
    "GM_TAHAKKUK_TAHSIL": "Tahakkuk, Tahsil & Zamanaşımı",
    "GM_GERI_VERME": "Geri Verme / Kaldırma",
    "GM_CEZA_UZLASMA": "İdari Para Cezaları & Uzlaşma",
    "GM_KACAKCILIK": "Kaçakçılık (5607)",
    "GM_KDV": "KDV",
    "GM_OTV": "ÖTV",
    "GM_DIGER_VERGI": "Damga V., Transfer Fiyatlandırması & Diğer Vergiler",
    "GM_KAMBIYO": "Kambiyo (32 Sayılı Karar, TCMB)",
    "GM_FONLAR": "KKDF & DFİF",
    "GM_ITHALAT_REJIMI": "İthalat Rejimi & Ek Mali Yükümlülük",
    "GM_DIS_TIC_IHRACAT": "İhracat Mevzuatı (Dış Ticaret)",
    "GM_KORUNMA": "Damping, Sübvansiyon & Korunma",
    "GM_TEKNIK_DUZENLEME": "Teknik Düzenlemeler & TAREKS",
    "GM_YATIRIM_SINIR": "Teşvik, Yabancı Yatırım & Sınır Ticareti",
    "GM_FSMH": "Fikri ve Sınai Haklar",
    "GM_INCOTERMS": "Incoterms (Teslim Şekilleri)",
    "GM_ULUSLARARASI_TIC": "Uluslararası Ticaret, DTÖ & 1/95",
}

# 8 konu grubu (kategorik renk sınırı)
GRUP = {
    "Tarife & Sınıflandırma": ["GM_TARIFE_SINIF", "GM_TARIFE_MEVZ"],
    "Gümrük Rejimleri": ["GM_SERBEST_DOLASIM", "GM_ANTREPO", "GM_DIR", "GM_GKAI", "GM_GECICI_ITHALAT",
                         "GM_HIR", "GM_TRANSIT", "GM_IHRACAT"],
    "Gümrük Kıymeti": ["GM_KIYMET"],
    "Genel Hükümler, İşlemler & Meslek": ["GM_TEMEL", "GM_GIRIS_BEYAN", "GM_OZEL_TASIT", "GM_POSTA", "GM_TASFIYE",
                                          "GM_SERBEST_BOLGE", "GM_MUAFIYET", "GM_MESLEK", "GM_YGM",
                                          "GM_KOLAYLASTIRMA"],
    "Menşe & Tercihli Ticaret": ["GM_MENSE", "GM_TERCIHLI_STA"],
    "Vergi Alacağı, Ceza & Kaçakçılık": ["GM_YUKUMLULUK_TEMINAT", "GM_TAHAKKUK_TAHSIL", "GM_GERI_VERME",
                                         "GM_CEZA_UZLASMA", "GM_KACAKCILIK"],
    "İç Vergiler, Kambiyo & Fonlar": ["GM_KDV", "GM_OTV", "GM_DIGER_VERGI", "GM_KAMBIYO", "GM_FONLAR"],
    "Dış Ticaret Politikası & Uluslararası Ticaret": ["GM_ITHALAT_REJIMI", "GM_DIS_TIC_IHRACAT", "GM_KORUNMA",
                                                      "GM_TEKNIK_DUZENLEME", "GM_YATIRIM_SINIR", "GM_FSMH",
                                                      "GM_INCOTERMS", "GM_ULUSLARARASI_TIC"],
}
KONU2GRUP = {k: g for g, ks in GRUP.items() for k in ks}
assert set(KONU2GRUP) == set(KONU), set(KONU) ^ set(KONU2GRUP)

KOK = {
    "OLUMLU": "Olumlu kök",
    "OLUMSUZ": "Olumsuz kök (değildir / yanlıştır)",
    "ONCULLU": "Öncüllü (I-II-III)",
    "BOSLUK": "Boşluk doldurma",
    "ESLESTIRME_SIRALAMA": "Eşleştirme / Sıralama",
}
TIP = {
    "KAPSAM_SART": "Kapsam & Şart",
    "DOGRU_YANLIS_HUKUM": "Doğru/Yanlış Hüküm",
    "SINIFLANDIRMA": "Tarife Sınıflandırma",
    "HESAPLAMA": "Hesaplama",
    "SAYISAL": "Sayısal (süre-oran-tutar)",
    "TANIM": "Tanım / Kavram",
    "BELGE_PROSEDUR": "Belge & Prosedür",
    "YETKILI_MERCI": "Yetkili Merci",
    "VAKA_UYGULAMA": "Vaka / Senaryo",
    "OLGU_BILGI": "Olgu Bilgisi",
}
MEVZUAT = {
    "GK_4458": "4458 Gümrük Kanunu",
    "GY": "Gümrük Yönetmeliği",
    "TEBLIG": "Gümrük Genel Tebliğleri",
    "GIK_YON": "Kolaylaştırma Yönetmeliği",
    "KARAR_2009_15481": "2009/15481 Karar",
    "KMK_5607": "5607 Kaçakçılık Kanunu",
    "TGTC": "Tarife Cetveli, İzahname & GYK",
    "KDV_KANUNU": "KDV Kanunu",
    "OTV_KANUNU": "ÖTV Kanunu",
    "DIGER_VERGI": "Diğer Vergi Kanunları",
    "KAMBIYO_MEVZ": "Kambiyo & Fon Mevzuatı",
    "DIS_TIC_MEVZ": "Dış Ticaret Mevzuatı",
    "ULUSLARARASI": "Uluslararası Anlaşmalar",
    "GENEL": "Genel bilgi",
}
HESAP = {
    "KIYMET": "Gümrük kıymeti",
    "KDV_MATRAH": "KDV matrahı / KDV",
    "OTV": "ÖTV",
    "GV_IGV": "Gümrük vergisi / İGV",
    "CEZA": "Ceza / ek tahakkuk",
    "UZLASMA": "Uzlaşma",
    "GECICI_ITH_VERGI": "Geçici ithalat vergisi",
    "ANTREPO_TEMINAT": "Antrepo teminatı",
    "DIGER": "Diğer",
}
ZORLUK = {"KOLAY": "Kolay", "ORTA": "Orta", "ZOR": "Zor"}
YEARS = [2021, 2022, 2023, 2024, 2025]

# TGTC bölümleri (fasıl → bölüm), fasıl ısı haritası için
BOLUMLER = [
    ("I", "Canlı hayvanlar, hayvansal ürünler", 1, 5), ("II", "Bitkisel ürünler", 6, 14),
    ("III", "Hayvansal/bitkisel yağlar", 15, 15), ("IV", "Gıda sanayii, içecek, tütün", 16, 24),
    ("V", "Mineral ürünler", 25, 27), ("VI", "Kimya sanayii", 28, 38), ("VII", "Plastik, kauçuk", 39, 40),
    ("VIII", "Deri, kürk, saraciye", 41, 43), ("IX", "Ağaç, mantar, hasır", 44, 46),
    ("X", "Kâğıt, karton", 47, 49), ("XI", "Dokumaya elverişli maddeler", 50, 63),
    ("XII", "Ayakkabı, şapka, şemsiye", 64, 67), ("XIII", "Taş, seramik, cam", 68, 70),
    ("XIV", "Kıymetli taş ve metaller", 71, 71), ("XV", "Adi metaller", 72, 83),
    ("XVI", "Makine, elektrikli cihazlar", 84, 85), ("XVII", "Taşıtlar", 86, 89),
    ("XVIII", "Optik, tıbbi, saat, müzik aletleri", 90, 92), ("XIX", "Silah, mühimmat", 93, 93),
    ("XX", "Çeşitli mamul eşya", 94, 96), ("XXI", "Sanat eserleri, antika", 97, 97),
    ("—", "Fasıl 98-99 (ulusal)", 98, 99),
]


def fasil_bolum(f):
    n = int(f)
    for b, ad, a, z in BOLUMLER:
        if a <= n <= z:
            return b, ad
    return "?", "?"
