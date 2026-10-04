import json, re, os
OUT=os.path.dirname(os.path.abspath(__file__))
SKIP=re.compile(r"(Diğer [Ss]ayfaya [Gg]eçiniz|GÜMRÜK MÜŞAVİR YARDIMCILIĞI|A Kitapçığı|TİCARET BAKANLIĞI|^\s*A\s*$|^\s*\d+\s*$|TEST BİTTİ|Test bitti)")
res={}
for year in range(2021,2026):
    L=json.load(open(f"{OUT}/lines_{year}.json"))
    qs={}; cur=None; expected=1
    stop=False
    for ln in L:
        if ln["p"]==1: continue
        t=ln["t"].strip()
        if re.search(r"SINAVDA UYUL",t): stop=True
        if stop: continue
        if SKIP.search(t) and not re.match(r"^\d+\.\s*\S",t): continue
        m=re.match(r"^(\d{1,3})\.\s*(.*)$",t)
        if m and int(m.group(1))==expected:
            cur={"n":expected,"text":[],"opts_seen":[],"ans":None,"page":ln["p"]}
            qs[expected]=cur; expected+=1
            rest=m.group(2)
            if rest: cur["text"].append(rest)
            continue
        if cur is None: continue
        if expected>101: break
        letters=re.findall(r"(?:^|\s)([A-E])\)",t)
        if ln["red"] and cur["ans"] is None:
            rl=re.findall(r"(?:^|\s)([A-E])\)",ln["rt"]) or re.findall(r"^([A-E])\)",ln["rt"].strip())
            if rl: cur["ans"]=rl[0]
            elif re.match(r"^\s*([A-E])\s*$",ln["rt"]): cur["ans"]=ln["rt"].strip()
            else:
                # continuation of an option: last seen letter
                prev=cur["opts_seen"][-1] if cur["opts_seen"] else None
                cur["ans_guess"]=prev; cur["ans"]=prev
        cur["opts_seen"]+=letters
        cur["text"].append(t)
    for q in qs.values():
        q["text"]="\n".join(q["text"])
    res[year]=qs
    missing=[i for i in range(1,101) if i not in qs]
    noans=[i for i,q in qs.items() if not q["ans"]]
    guess=[i for i,q in qs.items() if q.get("ans_guess")]
    print(year,"parsed",len(qs),"missing",missing,"noans",noans,"guess",guess)
json.dump(res,open(f"{OUT}/questions.json","w"),ensure_ascii=False,indent=1)
