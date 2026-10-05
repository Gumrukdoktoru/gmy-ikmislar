"""Sınıflandırmadaki 'kok' alanını soru kökünden regex ile tahmin edilen kalıpla karşılaştırır."""
import json, re, sys
Q = json.load(open("questions.json"))
NEG = re.compile(r"(değildir|değil\b|yanlıştır|yanlış\b|yer almaz|yer almamaktadır|söylenemez|sayılmamıştır|sayılmaz|"
                 r"olamaz|bulunmaz|bulunmamaktadır|kullanılmaz|kullanılamaz|uygulanmaz|yararlanamaz|faydalanamaz|"
                 r"sınıflandırılamaz|sınıflandırılmaz|sınıflandırılmamaktadır|kapsamaz|girmez|girmemektedir|"
                 r"verilmemiştir|gerçekleşmez|içermez|aranmaz|aranmamaktadır|edilmez|edilemez|getiremez|düzenlenemez|"
                 r"tutulamaz|gösterilemez|bahsedilemez|değerlendirilemez|kaybetmez|sona ermez|yapılmaz|yapılamaz|"
                 r"alınamaz|çıkartılmamıştır|mümkün değildir|zorunlu değildir|iletilmez|tanımlanmamıştır|"
                 r"düzenlenmemiştir|ifade etmez|yer almayan|almaz\?|tabi değildir)", re.I)
def guess(text):
    stem = re.split(r"\n\s*A\)", text)[0]
    if re.search(r"(^|\n|\s)(I|i)[\.\)]\s", stem) and re.search(r"(^|\n|\s)(II|ii)[\.\)]\s", stem) and re.search(r"hangi(si|leri)", stem.split("\n")[-1] + stem[-200:]):
        return "ONCULLU"
    if re.search(r"(\.{4,}|…{2,}|-{4,}|…)", stem):
        return "BOSLUK"
    if NEG.search(stem[-260:]):
        return "OLUMSUZ"
    return "OLUMLU"
diff = []
for y in sys.argv[1:]:
    for r in json.load(open(f"cls_{y}.json")):
        g = guess(Q[str(y)][str(r["n"])]["text"])
        if g != r["kok"]:
            stem = " ".join(re.split(r"\n\s*A\)", Q[str(y)][str(r["n"])]["text"])[0].split())
            diff.append((y, r["n"], r["kok"], g, stem[-140:]))
for x in diff: print(x)
print("fark:", len(diff))
