import json, os
import pymupdf as fitz
from collections import Counter

# PDF'lerden satırları renk bilgisiyle çıkarır; doğru cevaplar kırmızı (#ff0000) işaretlidir.
REPO=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
FILES={2021:"2021-gmy-sinavi-cevapli.pdf",2022:"2022-gmy-sinavi-cevapli.pdf",2023:"2023-gmy-sinavi-cevapli.pdf",2024:"2024-gmy-sinavi-cevapli.pdf",2025:"Gümrük_Müşavir_Yardımcılığı_A_Kitapçığı_Yanıt_Anahtarlı.pdf"}
OUT=os.path.dirname(os.path.abspath(__file__))

def is_red(c):
    r=(c>>16)&255; g=(c>>8)&255; b=c&255
    return r>150 and g<100 and b<100

for year,fn in FILES.items():
    doc=fitz.open(os.path.join(REPO,fn))
    lines=[]
    colors=Counter()
    for pno,page in enumerate(doc):
        W=page.rect.width
        d=page.get_text("dict")
        items=[]
        for b in d["blocks"]:
            if b.get("type")!=0: continue
            for l in b["lines"]:
                spans=[s for s in l["spans"] if s["text"].strip()]
                if not spans: continue
                x0=l["bbox"][0]; y0=l["bbox"][1]
                txt="".join(s["text"] for s in l["spans"])
                red=any(is_red(s["color"]) for s in spans)
                redtxt="".join(s["text"] for s in l["spans"] if is_red(s["color"]))
                for s in spans: colors[s["color"]]+=1
                col=0 if x0 < W/2-10 else 1
                items.append((col,round(y0,1),x0,txt,red,redtxt))
        items.sort(key=lambda t:(t[0],t[1],t[2]))
        for it in items:
            lines.append({"p":pno+1,"col":it[0],"y":it[1],"x":round(it[2],1),"t":it[3],"red":it[4],"rt":it[5]})
    json.dump(lines,open(f"{OUT}/lines_{year}.json","w"),ensure_ascii=False)
    print(year,len(lines),"top colors:",[(hex(c),n) for c,n in colors.most_common(6)])
