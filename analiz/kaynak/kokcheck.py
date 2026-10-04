"""Ajan sınıflandırmasındaki 'kok' alanını soru metninden regex ile tahmin edilen kalıpla karşılaştırır."""
import json, re, sys
Q = json.load(open("questions.json"))
NEG = re.compile(r"(değildir|değil\b|yanlıştır|yanlış\b|yer almaz|söylenemez|sayılmamıştır|sayılmaz|olamaz|"
                 r"bulunmamaktadır|kullanılmaz|uygulanmaz|yararlanamaz|faydalanamaz|imzalamamıştır|kapsamaz|"
                 r"verilmemiştir|gerçekleşmez|içermez|aranmamaktadır|kabul edilmez|getiremez|düzenlenemez|"
                 r"teşkil etmez|bahsedilemez|tabi değildir|dahil değildir|değerlendirilemez|kaybetmez|sona ermez|"
                 r"yürütülmez|yapılmaz|dikkate alınamaz|oluşturmamaktadır|çıkartılmamıştır|mümkün değildir|"
                 r"zorunlu değildir|edilmez|izin verilmemektedir|görevli değildir)", re.I)
def guess(text):
    stem = re.split(r"\n\s*A\)", text)[0]
    if re.search(r"(^|\n|\s)(I|i)[\.\)]\s", stem) and re.search(r"(^|\n|\s)(II|ii)[\.\)]\s", stem):
        return "ONCULLU"
    if re.search(r"(\.{4,}|…{2,}|-{4,}|…\s*…)", stem):
        return "BOSLUK"
    if NEG.search(stem):
        return "OLUMSUZ"
    return "OLUMLU"
diff = []
for y in sys.argv[1:]:
    d = json.load(open(f"cls_{y}.json"))
    for r in d:
        g = guess(Q[str(y)][str(r["n"])]["text"])
        if g != r["kok"]:
            stem = " ".join(re.split(r"\n\s*A\)", Q[str(y)][str(r["n"])]["text"])[0].split())
            diff.append((y, r["n"], r["kok"], g, stem[-150:]))
for x in diff:
    print(x)
print("fark:", len(diff))
