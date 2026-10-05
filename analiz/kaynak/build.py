"""GMY soru sınıflandırmasından CSV/JSON, PNG grafikler, Markdown ve HTML rapor üretir.

Kullanım: python3 build.py <çalışma_dizini> <çıktı_dizini>
Çalışma dizininde cls_<yıl>.json, insights.json ve template.html bulunmalıdır.
"""
import csv
import json
import os
import re
import sys
from collections import Counter, defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from labels import (BOLUM, BOLUM_ORDER, GRUP, KOK, KOK_ORDER, KONU, KONU2GRUP,  # noqa: E402
                    MEVZUAT, MEVZUAT_ORDER, TIP, TIP_ORDER, YEARS, ZORLUK)

WORK = sys.argv[1]
OUT = sys.argv[2]
IMG = os.path.join(OUT, "grafikler")
os.makedirs(IMG, exist_ok=True)

SER = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
NEUTRAL = "#b9bec4"
INK, INK2, MUTED, GRID = "#0f1720", "#4a525c", "#7d848c", "#e1e0d9"
SEQ = ["#f0efec", "#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
FIELDS = ["yil", "n", "cevap", "bolum", "konu", "alt_konu", "kok", "tip", "mevzuat", "zorluk", "ozet", "anahtar_bilgi"]
GRUPLAR = list(GRUP)

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": "#c3c2b7", "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK, "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb", "savefig.facecolor": "#fcfcfb",
})


# ---------------------------------------------------------------- veri
def load():
    rows = []
    for y in YEARS:
        d = json.load(open(os.path.join(WORK, f"cls_{y}.json"), encoding="utf-8"))
        assert len(d) == 100, (y, len(d))
        rows += d
    errs = []
    expect_b = lambda n: "TURKCE" if n <= 5 else "MATEMATIK" if n <= 10 else "TARIH" if n <= 15 else "ANAYASA" if n <= 20 else "GUMRUK"
    for r in rows:
        r["yil"], r["n"] = int(r["yil"]), int(r["n"])
        if r["bolum"] != expect_b(r["n"]):
            errs.append((r["yil"], r["n"], "bolum", r["bolum"]))
        for f, dom in (("konu", KONU), ("kok", KOK), ("tip", TIP), ("mevzuat", MEVZUAT), ("zorluk", ZORLUK)):
            if r.get(f) not in dom:
                errs.append((r["yil"], r["n"], f, r.get(f)))
    if errs:
        print("GEÇERSİZ KODLAR:", errs)
        sys.exit(1)
    rows.sort(key=lambda r: (r["yil"], r["n"]))
    return rows


Q = load()
GK = [q for q in Q if q["bolum"] == "GUMRUK"]
ins = json.load(open(os.path.join(WORK, "insights.json"), encoding="utf-8"))
_kc = Counter(q["konu"] for q in GK)
_mm = ["flowchart LR", "  S([GMY Sınavı: 100 soru · 150 dk])", "  S --> GY[Genel Yetenek: 10 soru]",
       "  S --> GKL[Genel Kültür: 10 soru]", "  S --> AL[Gümrük Mevzuatı: 80 soru]",
       "  GY --> T1[Türkçe 5]", "  GY --> T2[Matematik 5]", "  GKL --> T3[Tarih 5]", "  GKL --> T4[Anayasa 5]"]
for _i, _g in enumerate(GRUP):
    _n = sum(_kc[k] for k in GRUP[_g]) / len(YEARS)
    _mm.append(f'  AL --> G{_i}["{re.sub(r" [(].*[)]", "", _g)}: ort. {_n:.1f} soru/yıl"]')
ins["mermaid"] = "\n".join(_mm)


def cnt(rows, key):
    return Counter(r[key] for r in rows)


def by_year(y, rows=Q):
    return [r for r in rows if r["yil"] == y]


# ---------------------------------------------------------------- CSV / JSON
with open(os.path.join(OUT, "gmy_soru_siniflandirma.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["Yıl", "Soru No", "Doğru Cevap", "Bölüm", "Konu Grubu", "Konu", "Alt Konu", "Soru Kalıbı",
                "Soru Tipi", "Mevzuat", "Zorluk", "Soru Özeti", "Öğrenilecek Bilgi"])
    for q in Q:
        w.writerow([q["yil"], q["n"], q["cevap"], BOLUM[q["bolum"]], KONU2GRUP.get(q["konu"], BOLUM[q["bolum"]]),
                    KONU[q["konu"]], q["alt_konu"], KOK[q["kok"]], TIP[q["tip"]], MEVZUAT[q["mevzuat"]],
                    ZORLUK[q["zorluk"]], q["ozet"], q["anahtar_bilgi"]])
json.dump([{k: q[k] for k in FIELDS} for q in Q], open(os.path.join(OUT, "gmy_soru_siniflandirma.json"), "w",
          encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------------------------------------------------------------- istatistik
konu_stat = []
for k in [k for k in KONU if k.startswith("G_")]:
    m = {y: sum(1 for q in GK if q["yil"] == y and q["konu"] == k) for y in YEARS}
    tot = sum(m.values())
    if not tot:
        continue
    konu_stat.append(dict(k=k, l=KONU[k], m=m, tot=tot, avg=tot / len(YEARS), yrs=sum(1 for v in m.values() if v),
                          early=(m[2021] + m[2022]) / 2, late=(m[2024] + m[2025]) / 2, g=KONU2GRUP[k]))
konu_stat.sort(key=lambda r: (-r["tot"], r["l"]))


def save(fig, name):
    p = os.path.join(IMG, name)
    fig.savefig(p, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return f"grafikler/{name}"


def hbar(ax, labels, vals, color=SER[0], title=None, maxv=None):
    ys = range(len(labels))[::-1]
    ax.barh(list(ys), vals, color=color, height=0.62)
    ax.set_yticks(list(ys))
    ax.set_yticklabels(labels, fontsize=9)
    ax.xaxis.grid(True, color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    m = maxv or max(vals + [1])
    ax.set_xlim(0, m * 1.15)
    for yv, v in zip(ys, vals):
        ax.text(v + m * 0.012, yv, str(v), va="center", fontsize=8.5, color=INK2)
    if title:
        ax.set_title(title, loc="left", fontsize=11.5, color=INK, fontweight="bold")


def heat_png(rows, cols, name, title, row_key="l", figw=8.6, vmax=None, extra=None):
    import numpy as np
    mat = np.array([[r["m"][c] for c in cols] for r in rows], dtype=float)
    vmax = vmax or max(1, mat.max())
    cmap = LinearSegmentedColormap.from_list("seq", SEQ)
    h = 0.34 * len(rows) + 1.3
    fig, ax = plt.subplots(figsize=(figw, h))
    ax.imshow(mat, cmap=cmap, vmin=0, vmax=vmax, aspect="auto")
    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels([str(c) for c in cols])
    ax.xaxis.tick_top()
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[row_key] for r in rows], fontsize=9)
    for i, r in enumerate(rows):
        for j, c in enumerate(cols):
            v = r["m"][c]
            ax.text(j, i, str(v) if v else "·", ha="center", va="center", fontsize=8.5,
                    color="#ffffff" if v / vmax > 0.55 else INK)
        if extra:
            ax.text(len(cols) - 0.35, i, extra(r), ha="left", va="center", fontsize=8.5, color=INK2)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks([x - 0.5 for x in range(1, len(cols))], minor=True)
    ax.set_yticks([y - 0.5 for y in range(1, len(rows))], minor=True)
    ax.grid(which="minor", color="#fcfcfb", lw=2)
    ax.tick_params(which="both", length=0)
    ax.set_title(title, loc="left", fontsize=12, color=INK, fontweight="bold", pad=24)
    return save(fig, name)


def stack_png(rows, keys, names, colors, name, title):
    fig, ax = plt.subplots(figsize=(8.6, 0.55 * len(rows) + 1.6))
    ys = list(range(len(rows)))[::-1]
    for yv, r in zip(ys, rows):
        tot = sum(r["m"].get(k, 0) for k in keys)
        left = 0
        for i, k in enumerate(keys):
            v = r["m"].get(k, 0)
            if not v:
                continue
            p = v / tot * 100
            ax.barh(yv, p, left=left, color=colors[i], height=0.62, edgecolor="#fcfcfb", linewidth=1.5)
            if p >= 8:
                ax.text(left + p / 2, yv, f"%{round(p)}", ha="center", va="center", fontsize=8,
                        color=INK if i in (2, 3, 4) else "#ffffff")
            left += p
    ax.set_yticks(ys)
    ax.set_yticklabels([str(r["l"]) for r in rows])
    ax.set_xlim(0, 100)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xticklabels(["%0", "%25", "%50", "%75", "%100"])
    ax.set_title(title, loc="left", fontsize=12, color=INK, fontweight="bold")
    handles = [plt.Rectangle((0, 0), 1, 1, color=colors[i]) for i in range(len(keys))]
    ax.legend(handles, [names[k] for k in keys], loc="upper center", bbox_to_anchor=(0.5, -0.12),
              ncol=2 if len(keys) > 4 else len(keys), frameon=False, fontsize=8.5)
    return save(fig, name)


imgs = {}

# Optik form şeması
fig, ax = plt.subplots(figsize=(13, 3.2))
for yi, y in enumerate(YEARS):
    for q in by_year(y):
        c = SER[GRUPLAR.index(KONU2GRUP[q["konu"]])] if q["bolum"] == "GUMRUK" else NEUTRAL
        ax.add_patch(plt.Circle((q["n"], -yi * 1.35), 0.42, color=c))
ax.set_xlim(0, 101)
ax.set_ylim(-(len(YEARS) - 1) * 1.35 - 0.8, 0.8)
ax.set_aspect("equal")
ax.set_yticks([-i * 1.35 for i in range(len(YEARS))])
ax.set_yticklabels([str(y) for y in YEARS])
ax.set_xticks([1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
ax.tick_params(length=0)
for s in ax.spines.values():
    s.set_visible(False)
ax.set_title("Optik form şeması: her daire bir soru (gri = genel yetenek & kültür, renkler = gümrük konu grubu)",
             loc="left", fontsize=11, color=INK, fontweight="bold")
handles = [plt.Line2D([], [], marker="o", ls="", color=NEUTRAL, ms=8)] + \
          [plt.Line2D([], [], marker="o", ls="", color=SER[i], ms=8) for i in range(len(GRUPLAR))]
ax.legend(handles, ["Genel yetenek & kültür"] + GRUPLAR, loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=3,
          frameon=False, fontsize=8.5)
imgs["optik"] = save(fig, "00_optik_form_semasi.png")

# Yıl yıl grafikler
for y in YEARS:
    g = by_year(y, GK)
    kc = cnt(g, "konu").most_common()
    fig, ax = plt.subplots(figsize=(8.6, 0.3 * len(kc) + 1.0))
    hbar(ax, [KONU[k] for k, _ in kc], [v for _, v in kc], title=f"{y} · Gümrük konuları (80 soru)")
    imgs[f"{y}_konu"] = save(fig, f"{y}_1_gumruk_konulari.png")

    fig, axs = plt.subplots(1, 2, figsize=(11, 3.4), gridspec_kw={"wspace": 0.85})
    kk = cnt(by_year(y), "kok")
    ks = [k for k in KOK_ORDER if kk.get(k)]
    hbar(axs[0], [KOK[k] for k in ks], [kk[k] for k in ks], color=[SER[KOK_ORDER.index(k)] for k in ks],
         title="Soru kalıbı (100 soru)")
    tc = cnt(g, "tip").most_common()
    hbar(axs[1], [TIP[k] for k, _ in tc], [v for _, v in tc], color=SER[6], title="Soru tipi (gümrük, 80 soru)")
    imgs[f"{y}_kok_tip"] = save(fig, f"{y}_2_soru_kalibi_ve_tipi.png")

# Karşılaştırma grafikleri
imgs["hm_konu"] = heat_png(konu_stat, YEARS, "10_karsilastirma_konu_isi_haritasi.png",
                           "Gümrük konuları × yıl (soru sayısı)",
                           extra=lambda r: f"Σ{r['tot']}  ort.{r['avg']:.1f}  {r['yrs']}/5 yıl", figw=9.4)
top = konu_stat[:12]
fig, ax = plt.subplots(figsize=(8.6, 4.6))
hbar(ax, [r["l"] for r in top], [r["tot"] for r in top], title="En çok soru gelen 12 gümrük konusu (2021–2025 toplam)")
imgs["top12"] = save(fig, "11_en_cok_soru_gelen_konular.png")

grows = []
for y in YEARS:
    m = Counter(KONU2GRUP[q["konu"]] for q in by_year(y, GK))
    grows.append({"l": y, "m": m})
imgs["grup"] = stack_png(grows, GRUPLAR, {g: g for g in GRUPLAR}, SER, "12_konu_grubu_paylari.png",
                         "Gümrük konu grubu payları, yıla göre")
imgs["kok"] = stack_png([{"l": y, "m": cnt(by_year(y), "kok")} for y in YEARS], KOK_ORDER, KOK, SER,
                        "13_soru_kalibi_yillara_gore.png", "Soru kalıbı (kök yapısı), yıla göre — 100 soru")

tip_rows = [{"l": TIP[k], "m": {y: sum(1 for q in by_year(y, GK) if q["tip"] == k) for y in YEARS}} for k in TIP_ORDER]
tip_rows = sorted([r for r in tip_rows if sum(r["m"].values())], key=lambda r: -sum(r["m"].values()))
imgs["hm_tip"] = heat_png(tip_rows, YEARS, "14_soru_tipi_isi_haritasi.png", "Soru tipi × yıl (gümrük soruları)",
                          extra=lambda r: f"Σ{sum(r['m'].values())}")
mev_rows = [{"l": MEVZUAT[k], "m": {y: sum(1 for q in by_year(y, GK) if q["mevzuat"] == k) for y in YEARS}}
            for k in MEVZUAT_ORDER]
mev_rows = sorted([r for r in mev_rows if sum(r["m"].values())], key=lambda r: -sum(r["m"].values()))
imgs["hm_mev"] = heat_png(mev_rows, YEARS, "15_mevzuat_kaynagi_isi_haritasi.png",
                          "Dayanılan mevzuat × yıl (gümrük soruları)", extra=lambda r: f"Σ{sum(r['m'].values())}")

dd = sorted([r for r in konu_stat if abs(r["late"] - r["early"]) >= 1], key=lambda r: r["late"] - r["early"])
if dd:
    fig, ax = plt.subplots(figsize=(8.6, 0.36 * len(dd) + 1.2))
    for i, r in enumerate(dd):
        c = "#006300" if r["late"] > r["early"] else "#b3261e"
        ax.plot([r["early"], r["late"]], [i, i], color=c, lw=2, zorder=1)
        ax.scatter([r["early"]], [i], s=46, facecolor="#fcfcfb", edgecolor=c, lw=2, zorder=2)
        ax.scatter([r["late"]], [i], s=52, color=c, zorder=3)
    ax.set_yticks(range(len(dd)))
    ax.set_yticklabels([r["l"] for r in dd], fontsize=9)
    ax.xaxis.grid(True, color=GRID)
    ax.set_axisbelow(True)
    ax.set_xlabel("yıllık ortalama soru sayısı")
    ax.set_title("Yükselen (yeşil) ve düşen (kırmızı) konular: 2021–22 ort. ○ → 2024–25 ort. ●", loc="left",
                 fontsize=11, color=INK, fontweight="bold")
    imgs["dumb"] = save(fig, "16_yukselen_dusen_konular.png")

nong = [q for q in Q if q["bolum"] != "GUMRUK"]
gk_rows = []
for b in ["TURKCE", "MATEMATIK", "TARIH", "ANAYASA"]:
    for k in KONU:
        m = {y: sum(1 for q in nong if q["yil"] == y and q["konu"] == k and q["bolum"] == b) for y in YEARS}
        if sum(m.values()):
            gk_rows.append({"l": f"{BOLUM[b].split(' ')[0]} · {KONU[k]}", "m": m})
imgs["hm_gk"] = heat_png(gk_rows, YEARS, "17_genel_yetenek_kultur_alt_konular.png",
                         "Genel yetenek & genel kültür alt konuları × yıl", vmax=5,
                         extra=lambda r: f"Σ{sum(r['m'].values())}")

# ---------------------------------------------------------------- Markdown
def md_table(head, rows):
    out = "| " + " | ".join(head) + " |\n|" + "|".join(["---"] * len(head)) + "|\n"
    for r in rows:
        out += "| " + " | ".join(str(c) for c in r) + " |\n"
    return out


md = []
md.append("# GMY Soru Atlası 2021–2025\n")
md.append("Gümrük Müşavir Yardımcılığı sınavının 2021, 2022, 2023, 2024 ve 2025 yıllarına ait A kitapçıklarındaki "
          "**500 sorunun** konu, soru kalıbı, soru tipi ve dayandığı mevzuata göre analizi. Etkileşimli sürüm: "
          "`GMY_Soru_Atlasi.html` (tarayıcıda açın).\n")
md.append("## İçindekiler\n\n1. [Sınavın yapısı](#1-sınavın-yapısı)\n2. [Yıl yıl analiz](#2-yıl-yıl-analiz)\n"
          "3. [Yılların karşılaştırması](#3-yılların-karşılaştırması)\n4. [Sonuç: en çok neyden, nasıl soruluyor?](#4-sonuç-en-çok-neyden-nasıl-soruluyor)\n"
          "5. [Yöntem ve dosyalar](#5-yöntem-ve-dosyalar)\n")
md.append("## 1. Sınavın yapısı\n")
md.append(md_table(["Bölüm", "Soru no", *map(str, YEARS)],
                   [[BOLUM[b], rng, *[sum(1 for q in by_year(y) if q["bolum"] == b) for y in YEARS]]
                    for b, rng in zip(BOLUM_ORDER, ["1–5", "6–10", "11–15", "16–20", "21–100"])]))
md.append("\nSınav her yıl 100 soru / 150 dakika; puanın **%80'i gümrük mevzuatından** geliyor.\n")
md.append("```mermaid\n" + ins["mermaid"] + "\n```\n")
md.append(f"![Optik form şeması]({imgs['optik']})\n")

md.append("## 2. Yıl yıl analiz\n")
for y in YEARS:
    g = by_year(y, GK)
    md.append(f"### {y}\n")
    for t in ins["years"][str(y)]:
        md.append(f"- {re.sub(r'<[^>]+>', '', t).replace('&nbsp;', ' ')}")
    md.append("")
    md.append(f"![{y} gümrük konuları]({imgs[f'{y}_konu']})\n")
    md.append(f"![{y} soru kalıbı ve tipi]({imgs[f'{y}_kok_tip']})\n")
    kc = cnt(g, "konu").most_common()
    md.append("<details><summary>Konu tablosu ve soru numaraları</summary>\n")
    md.append(md_table(["Konu", "Soru", "Soru numaraları"],
                       [[KONU[k], v, ", ".join(str(q["n"]) for q in g if q["konu"] == k)] for k, v in kc]))
    md.append("\n</details>\n")

md.append("## 3. Yılların karşılaştırması\n")
md.append(f"![Konu ısı haritası]({imgs['hm_konu']})\n")
md.append(md_table(["#", "Konu", *map(str, YEARS), "Toplam", "Ort./yıl", "Çıktığı yıl", "Eğilim (24–25 vs 21–22)"],
                   [[i + 1, r["l"], *[r["m"][y] for y in YEARS], r["tot"], f"{r['avg']:.1f}", f"{r['yrs']}/5",
                     f"{'▲' if r['late'] - r['early'] >= 1 else '▼' if r['late'] - r['early'] <= -1 else '■'} "
                     f"{r['late'] - r['early']:+.1f}"] for i, r in enumerate(konu_stat)]))
md.append(f"\n![En çok soru gelen konular]({imgs['top12']})\n")
md.append(f"![Konu grubu payları]({imgs['grup']})\n")
md.append(f"![Soru kalıbı]({imgs['kok']})\n")
md.append(f"![Soru tipi]({imgs['hm_tip']})\n")
md.append(f"![Mevzuat kaynağı]({imgs['hm_mev']})\n")
if "dumb" in imgs:
    md.append(f"![Yükselen ve düşen konular]({imgs['dumb']})\n")
md.append(f"![Genel yetenek ve kültür]({imgs['hm_gk']})\n")
md.append("### Zorluk ve doğru şık dağılımı\n")
md.append(md_table(["", *map(str, YEARS)],
                   [[ZORLUK[z], *[sum(1 for q in by_year(y) if q["zorluk"] == z) for y in YEARS]] for z in ZORLUK] +
                   [[f"Doğru şık {s}", *[sum(1 for q in by_year(y) if q["cevap"] == s) for y in YEARS]] for s in "ABCDE"]))
md.append("\n### Tekrar eden soru kalıpları\n")
md.append(md_table(["Soru kalıbı", "Konu", *map(str, YEARS), "Doğru bilgi"],
                   [[t["kalip"], KONU.get(t["konu"], t["konu"]),
                     *[", ".join(map(str, t["sorular"].get(str(y), []))) or "·" for y in YEARS], t["bilgi"]]
                    for t in ins["tekrar"]]))

md.append("\n## 4. Sonuç: en çok neyden, nasıl soruluyor?\n")
for p in ins["sonuc"]["paragraflar"]:
    md.append(f"### {p['baslik']}\n")
    for m in p["maddeler"]:
        md.append(f"- {re.sub(r'<[^>]+>', '', m)}")
    md.append("")
md.append("### Çalışma öncelik listesi (gümrük konuları)\n")
for title, lo, hi in (("Öncelik 1 — yılda ort. 4+ soru", 4, 99), ("Öncelik 2 — yılda ort. 2–4 soru", 2, 4),
                      ("Öncelik 3 — yılda ort. 2'den az", 0, 2)):
    arr = [r for r in konu_stat if lo <= r["avg"] < hi]
    md.append(f"**{title}:** " + ", ".join(f"{r['l']} ({r['avg']:.1f})" for r in arr) + "\n")

md.append("## 5. Yöntem ve dosyalar\n")
md.append(re.sub(r"<[^>]+>", "", ins["yontem"]) + "\n")
md.append(md_table(["Dosya", "İçerik"], [
    ["`GMY_Soru_Atlasi.html`", "Etkileşimli rapor: optik form şeması, yıl sekmeleri, ısı haritaları, tekrar eden soru kalıpları"],
    ["`GMY_Soru_Atlasi.pdf`", "Raporun yazdırılabilir A4 sürümü: beş yılın analizi art arda, ardından karşılaştırma ve sonuç"],
    ["`gmy_soru_siniflandirma.csv`", "500 sorunun tamamı: konu, alt konu, kalıp, tip, mevzuat, zorluk, özet, öğrenilecek bilgi (Excel'de açılır)"],
    ["`gmy_soru_siniflandirma.json`", "Aynı veri, JSON"],
    ["`grafikler/`", "Bu rapordaki PNG grafikler"],
    ["`kaynak/`", "PDF'ten soru/cevap çıkarma ve rapor üretme betikleri, taksonomi"],
]))
open(os.path.join(OUT, "README.md"), "w", encoding="utf-8").write("\n".join(md))

# ---------------------------------------------------------------- HTML
labels = dict(bolum=BOLUM, bolum_order=BOLUM_ORDER, konu=KONU, grup=GRUP, konu2grup=KONU2GRUP, kok=KOK,
              kok_order=KOK_ORDER, tip=TIP, tip_order=TIP_ORDER, mevzuat=MEVZUAT, mevzuat_order=MEVZUAT_ORDER,
              zorluk=ZORLUK)
data = dict(labels=labels, years=YEARS, questions=[{k: q[k] for k in FIELDS} for q in Q],
            insights={k: v for k, v in ins.items() if k != "yontem"})
tpl = open(os.path.join(WORK, "template.html"), encoding="utf-8").read()
payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
page = tpl.replace("/*__DATA__*/null", payload).replace('<pre class="mermaid" id="mm"></pre>',
                                                        '<pre class="mermaid" id="mm">' + ins["mermaid"] + "</pre>")
open(os.path.join(WORK, "artifact.html"), "w", encoding="utf-8").write(page)
standalone = ("<!doctype html>\n<html lang=\"tr\">\n<head>\n<meta charset=\"utf-8\">\n"
              "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1,viewport-fit=cover\">\n"
              + page.replace("</style>", "</style>\n</head>\n<body>", 1)
              + "\n<script src=\"https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js\"></script>\n"
              "<script>try{mermaid.initialize({startOnLoad:true,theme:matchMedia('(prefers-color-scheme: dark)').matches?'dark':'neutral'})}catch(e){}</script>\n"
              "</body>\n</html>\n")
open(os.path.join(OUT, "GMY_Soru_Atlasi.html"), "w", encoding="utf-8").write(standalone)
print("tamam:", len(Q), "soru;", len(imgs), "grafik;", OUT)
