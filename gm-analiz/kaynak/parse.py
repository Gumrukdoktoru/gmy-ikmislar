"""Satırlardan 100 soruyu ve kırmızı işaretli doğru cevabı ayrıştırır.

- Yeni soru, beklenen numarayla başlayan satırdır ve önceki sorunun E şıkkı okunmuş olmalıdır
  (soru metni içinde "93. Fasıl" gibi satır başları yeni soru sayılmaz).
- Tek başına duran sayı satırları yalnızca sayfa üstünde/altında ise (sayfa no) atılır.
- "89 ve 90. soruları aşağıdaki ... göre çözünüz" gibi ortak metinler ilgili soruların başına eklenir.
"""
import json, os, re
OUT = os.path.dirname(os.path.abspath(__file__))
SKIP = re.compile(r"(Diğer [Ss]ayfaya [Gg]eçiniz|GÜMRÜK MÜŞAVİRLİĞİ|[AB] Kitapçığı|TİCARET BAKANLIĞI|YAŞAM BOYU|OGRENME MERKEZ|ÖĞRENME MERKEZ|^\s*[AB]\s*$|^\s*\d+\s*$|TEST BİTTİ|Test bitti|rıh trsltt|^-{2,}\(.*\)-*$)")
SHARED = re.compile(r"^(\d{1,3})\.?\s*(?:ve|-|–)\s*(\d{1,3})\.?\s*(?:numaralı\s*)?soru", re.I)
res, shared_all = {}, {}
for year in range(2021, 2026):
    L = json.load(open(f"{OUT}/lines_{year}.json"))
    qs = {}; cur = None; expected = 1; stop = False; shared = []; sbuf = None
    for ln in L:
        if ln["p"] == 1:
            continue
        t = ln["t"].strip()
        if re.search(r"SINAVDA UYUL", t):
            stop = True
        if stop:
            continue
        ready = cur is None or "E" in cur["opts_seen"]
        sm = SHARED.match(t)
        if sm and ready and int(sm.group(1)) == expected:
            sbuf = {"from": int(sm.group(1)), "to": int(sm.group(2)), "text": [t]}
            shared.append(sbuf); cur = None
            continue
        m = re.match(r"^(\d{1,3})\s?[\.\)]\s*(.*)$", t)
        if m and int(m.group(1)) == expected and ready and not re.match(r"^\d{1,3}\.\d", t):
            cur = {"n": expected, "text": [], "opts_seen": [], "ans": None, "ans_src": None, "page": ln["p"], "reds": []}
            qs[expected] = cur; expected += 1; sbuf = None
            if m.group(2):
                cur["text"].append(m.group(2))
            continue
        if SKIP.search(t) and not (re.match(r"^\s*\d+\s*$", t) and 40 < ln["y"] < 760):
            continue
        if sbuf is not None and cur is None:
            sbuf["text"].append(t); continue
        if cur is None:
            continue
        letters = re.findall(r"(?:^|\s)([A-E])\)", t)
        if ln["red"]:
            cur["reds"].append(ln["rt"].strip())
            if cur["ans"] is None:
                rl = re.findall(r"(?:^|\s)([A-E])\)", " " + ln["rt"])
                if rl:
                    cur["ans"], cur["ans_src"] = rl[0], "harf"
                elif letters and re.match(r"^[A-E]\)", t):
                    cur["ans"], cur["ans_src"] = letters[0], "satır-başı"
                else:
                    cur["ans"] = cur["opts_seen"][-1] if cur["opts_seen"] else None
                    cur["ans_src"] = "devam"
        cur["opts_seen"] += letters
        cur["text"].append(t)
    for s in shared:
        for n in range(s["from"], s["to"] + 1):
            if n in qs:
                qs[n]["shared"] = "\n".join(s["text"])
    for q in qs.values():
        q["text"] = "\n".join(q["text"])
    res[year] = qs
    missing = [i for i in range(1, 101) if i not in qs]
    noans = [i for i, q in qs.items() if not q["ans"]]
    alt = [(i, q["ans_src"]) for i, q in qs.items() if q["ans_src"] != "harf"]
    print(year, "soru", len(qs), "eksik", missing, "cevapsız", noans, "harf-dışı", alt,
          "ortak metin", [(s["from"], s["to"], len("\n".join(s["text"]))) for s in shared])
json.dump(res, open(f"{OUT}/questions.json", "w"), ensure_ascii=False, indent=1)
