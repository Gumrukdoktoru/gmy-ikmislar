"""GM sınavı PDF'lerinden satırları renk bilgisiyle çıkarır; doğru cevaplar kırmızı (#ff0000) işaretlidir."""
import json, os, sys
import pymupdf
PDF = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pdf")
OUT = os.path.dirname(os.path.abspath(__file__))

def is_red(c):
    r, g, b = (c >> 16) & 255, (c >> 8) & 255, c & 255
    return r > 150 and g < 100 and b < 100

for year in range(2021, 2026):
    doc = pymupdf.open(os.path.join(PDF, f"{year}.pdf"))
    lines = []
    for pno, page in enumerate(doc):
        W = page.rect.width
        items = []
        for b in page.get_text("dict")["blocks"]:
            if b.get("type") != 0:
                continue
            for l in b["lines"]:
                spans = [s for s in l["spans"] if s["text"].strip()]
                if not spans:
                    continue
                x0, y0 = l["bbox"][0], l["bbox"][1]
                txt = "".join(s["text"] for s in l["spans"])
                red = any(is_red(s["color"]) for s in spans)
                redtxt = "".join(s["text"] for s in l["spans"] if is_red(s["color"]))
                col = 0 if x0 < W / 2 - 10 else 1
                items.append((col, round(y0, 1), x0, txt, red, redtxt))
        items.sort(key=lambda t: (t[0], t[1], t[2]))
        for it in items:
            lines.append({"p": pno + 1, "col": it[0], "y": it[1], "x": round(it[2], 1), "t": it[3], "red": it[4], "rt": it[5]})
    json.dump(lines, open(f"{OUT}/lines_{year}.json", "w"), ensure_ascii=False)
    print(year, len(lines), "satır")
