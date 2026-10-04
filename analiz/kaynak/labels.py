"""Taksonomi kodları için Türkçe görüntü adları ve gruplamalar."""

BOLUM = {
    "TURKCE": "Türkçe",
    "MATEMATIK": "Matematik",
    "TARIH": "Tarih (İnkılap)",
    "ANAYASA": "Anayasa / Vatandaşlık",
    "GUMRUK": "Gümrük Mevzuatı",
}
BOLUM_ORDER = list(BOLUM)

KONU = {
    # Türkçe
    "TR_SOZCUK_ANLAM": "Sözcükte Anlam / Deyim",
    "TR_CUMLE_ANLAM": "Cümlede Anlam",
    "TR_PARAGRAF": "Paragraf",
    "TR_DILBILGISI": "Dil Bilgisi",
    "TR_YAZIM_NOKTALAMA": "Yazım & Noktalama",
    "TR_ANLATIM_BOZ": "Anlatım Bozukluğu",
    # Matematik
    "MAT_TEMEL_ISLEM": "Temel İşlem & Sayılar",
    "MAT_PROBLEM": "Problemler",
    "MAT_GEOMETRI": "Geometri",
    # Tarih
    "TAR_OSMANLI_SON": "Osmanlı Son Dönem & I. Dünya Savaşı",
    "TAR_MILLI_MUCADELE": "Millî Mücadele",
    "TAR_INKILAP_ILKE": "İnkılaplar & Atatürk İlkeleri",
    "TAR_DIS_POLITIKA": "Atatürk Dönemi Dış Politika",
    # Anayasa
    "ANA_TEMEL_HUKUK": "Temel Hukuk & Devletin Nitelikleri",
    "ANA_YASAMA": "Yasama (TBMM)",
    "ANA_YURUTME": "Yürütme (Cumhurbaşkanı)",
    "ANA_YARGI": "Yargı",
    "ANA_HAK_ODEV": "Temel Hak ve Ödevler",
    "ANA_SECIM": "Seçimler",
    "ANA_ULUSLARARASI": "Uluslararası Kuruluşlar",
    # Gümrük
    "G_TEMEL_KAVRAM": "Temel Kavramlar & Tanımlar",
    "G_TARIFE": "Tarife & BTB",
    "G_MENSE": "Menşe",
    "G_KIYMET": "Gümrük Kıymeti",
    "G_GIRIS_BEYAN": "Özet Beyan, Geçici Depolama, Beyan & Muayene",
    "G_SERBEST_DOLASIM": "Serbest Dolaşıma Giriş",
    "G_ANTREPO": "Antrepo Rejimi",
    "G_DAHILDE_ISLEME": "Dahilde İşleme Rejimi",
    "G_GKAI": "Gümrük Kontrolü Altında İşleme",
    "G_GECICI_ITHALAT": "Geçici İthalat",
    "G_HARICTE_ISLEME": "Hariçte İşleme",
    "G_TRANSIT": "Transit Rejimi (TIR, NCTS)",
    "G_IHRACAT": "İhracat Rejimi",
    "G_SERBEST_BOLGE": "Serbest Bölge & Gümrüksüz Satış",
    "G_YUKUMLULUK_TEMINAT": "Gümrük Yükümlülüğü & Teminat",
    "G_TAHAKKUK_TAHSIL": "Tahakkuk, Tebliğ & Tahsil",
    "G_GERI_VERME": "Geri Verme / Kaldırma",
    "G_MUAFIYET": "Muafiyetler (Yolcu, Posta, Geri Gelen Eşya)",
    "G_TASFIYE": "Tasfiye",
    "G_CEZA_ITIRAZ": "İdari Para Cezaları & İtiraz",
    "G_KACAKCILIK": "Kaçakçılık (5607)",
    "G_MESLEK": "Gümrük Müşavirliği & Temsil",
    "G_YGM": "Yetkilendirilmiş Gümrük Müşavirliği",
    "G_KOLAYLASTIRMA": "YYS & Onaylanmış Kişi (Kolaylaştırma)",
    "G_DIS_TICARET_POL": "Dış Ticaret Politikası & İthalatta Vergiler",
    "G_OZEL_ISLEMLER": "Özel İşlemler (Akaryakıt, Kumanya, Posta)",
    "G_DIS_TIC_BELGE": "Dış Ticaret Belgeleri & Teşkilat",
}

# Gümrük konularının üst grupları (en fazla 8 → kategorik renk sınırı)
GRUP = {
    "Gümrük Rejimleri": ["G_SERBEST_DOLASIM", "G_ANTREPO", "G_DAHILDE_ISLEME", "G_GKAI",
                          "G_GECICI_ITHALAT", "G_HARICTE_ISLEME", "G_TRANSIT", "G_IHRACAT"],
    "Vergilendirme Unsurları (Tarife-Menşe-Kıymet)": ["G_TARIFE", "G_MENSE", "G_KIYMET"],
    "Genel Hükümler & Gümrük İşlemleri": ["G_TEMEL_KAVRAM", "G_GIRIS_BEYAN", "G_SERBEST_BOLGE",
                                           "G_OZEL_ISLEMLER", "G_TASFIYE"],
    "Vergi Alacağı (Yükümlülük-Tahsil-Geri Verme)": ["G_YUKUMLULUK_TEMINAT", "G_TAHAKKUK_TAHSIL",
                                                     "G_GERI_VERME"],
    "Ceza & Kaçakçılık": ["G_CEZA_ITIRAZ", "G_KACAKCILIK"],
    "Meslek & Kolaylaştırma": ["G_MESLEK", "G_YGM", "G_KOLAYLASTIRMA"],
    "Muafiyetler": ["G_MUAFIYET"],
    "Dış Ticaret": ["G_DIS_TICARET_POL", "G_DIS_TIC_BELGE"],
}
KONU2GRUP = {k: g for g, ks in GRUP.items() for k in ks}

KOK = {
    "OLUMLU": "Olumlu kök",
    "OLUMSUZ": "Olumsuz kök (değildir / yanlıştır)",
    "ONCULLU": "Öncüllü (I-II-III)",
    "BOSLUK": "Boşluk doldurma",
    "TABLO_ESLESTIRME": "Tablo / Eşleştirme",
}
KOK_ORDER = list(KOK)

TIP = {
    "DOGRU_YANLIS_HUKUM": "Doğru/Yanlış Hüküm",
    "KAPSAM_SART": "Kapsam & Şart",
    "SAYISAL": "Sayısal (süre-oran-tutar)",
    "TANIM": "Tanım / Kavram",
    "BELGE_PROSEDUR": "Belge & Prosedür",
    "YETKILI_MERCI": "Yetkili Merci",
    "VAKA_UYGULAMA": "Vaka / Senaryo",
    "HESAPLAMA": "Hesaplama",
    "DIL_KURALI": "Dil Kuralı",
    "YORUM_CIKARIM": "Yorum / Çıkarım",
    "OLGU_BILGI": "Olgu Bilgisi",
}
TIP_ORDER = list(TIP)

MEVZUAT = {
    "GK_4458": "4458 Gümrük Kanunu",
    "GY": "Gümrük Yönetmeliği",
    "KMK_5607": "5607 Kaçakçılık Kanunu",
    "KARAR_2009_15481": "2009/15481 Karar",
    "TEBLIG": "Tebliğler",
    "GIK_YON": "Kolaylaştırma Yönetmeliği",
    "DIS_TIC_MEVZ": "Dış Ticaret Mevzuatı",
    "GENEL_MEVZ": "Genel (\"gümrük mevzuatına göre\")",
    "YOK": "—",
}
MEVZUAT_ORDER = list(MEVZUAT)

ZORLUK = {"KOLAY": "Kolay", "ORTA": "Orta", "ZOR": "Zor"}
YEARS = [2021, 2022, 2023, 2024, 2025]
