"""rev_<yıl>.json önerilerini cls_<yıl>.json'a uygular (eski değer eşleşmesi zorunlu)."""
import json, sys
y = int(sys.argv[1]); skip = {tuple(s.split(":")) for s in sys.argv[2:]}  # "n:alan"
R = json.load(open(f"cls_{y}.json")); byn = {r["n"]: r for r in R}
ok = 0
for e in json.load(open(f"rev_{y}.json")):
    key = (str(e["n"]), e["alan"])
    if key in skip:
        print("ATLANDI", y, *key); continue
    r = byn[e["n"]]
    if r[e["alan"]] != e["eski"]:
        print("UYUŞMAZLIK", y, *key, "\n  mevcut:", r[e["alan"]], "\n  eski  :", e["eski"]); continue
    r[e["alan"]] = e["yeni"]; ok += 1
json.dump(R, open(f"cls_{y}.json", "w"), ensure_ascii=False, indent=1)
print(y, "uygulandı:", ok)
