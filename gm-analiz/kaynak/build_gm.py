"""GM soru sınıflandırmasından CSV/JSON, PNG grafikler, README.md ve HTML rapor üretir.

Kullanım: python3 build_gm.py <çalışma_dizini> <çıktı_dizini> [gmy_cls_dizini]
Çalışma dizininde cls_<yıl>.json, insights_gm.json ve template_gm.html bulunmalıdır.
GMY karşılaştırması için gmy_cls_dizini'nde GMY'nin cls_<yıl>.json dosyaları aranır.
"""
import csv
import json
import os
import re
import sys
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from labels_gm import (BOLUMLER, GRUP, HESAP, KOK, KONU, KONU2GRUP, MEVZUAT, TIP, YEARS,  # noqa: E402
                       ZORLUK, fasil_bolum)

WORK, OUT = sys.argv[1], sys.argv[2]
GMY_DIR = sys.argv[3] if len(sys.argv) > 3 else None
IMG = os.path.join(OUT, "grafikler")
os.makedirs(IMG, exist_ok=True)

SER = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
INK, INK2, GRID = "#0f1720", "#4a525c", "#e1e0d9"
SEQ = ["#f0efec", "#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
FIELDS = ["yil", "n", "cevap", "konu", "alt_konu", "kok", "tip", "mevzuat", "madde", "zorluk", "hesap", "fasil",
          "sayisal", "ozet", "anahtar_bilgi"]
GRUPLAR = list(GRUP)
KOK_ORDER, TIP_ORDER, MEVZUAT_ORDER = list(KOK), list(TIP), list(MEVZUAT)

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": "#c3c2b7", "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK, "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb", "savefig.facecolor": "#fcfcfb",
})


# ------------------------------------------------------------------ veri
def load():
    rows, errs = [], []
    for y in YEARS:
        d = json.load(open(os.path.join(WORK, f"cls_{y}.json"), encoding="utf-8"))
        assert len(d) == 100 and sorted(int(r["n"]) for r in d) == list(range(1, 101)), y
        rows += d
    for r in rows:
        r["yil"], r["n"] = int(r["yil"]), int(r["n"])
        for f, dom in (("konu", KONU), ("kok", KOK), ("tip", TIP), ("mevzuat", MEVZUAT), ("zorluk", ZORLUK)):
            if r.get(f) not in dom:
                errs.append((r["yil"], r["n"], f, r.get(f)))
        if r["tip"] == "HESAPLAMA" and r.get("hesap") not in HESAP:
            errs.append((r["yil"], r["n"], "hesap", r.get("hesap")))
        if r["tip"] != "HESAPLAMA":
            r["hesap"] = ""
        r["fasil"] = [f"{int(f):02d}" for f in (r.get("fasil") or []) if str(f).strip().isdigit()]
        for f in ("madde", "sayisal", "alt_konu", "ozet", "anahtar_bilgi"):
            r[f] = (r.get(f) or "").strip()
    if errs:
        print("GEÇERSİZ KODLAR:", errs)
        sys.exit(1)
    rows.sort(key=lambda r: (r["yil"], r["n"]))
    return rows


Q = load()
ins = json.load(open(os.path.join(WORK, "insights_gm.json"), encoding="utf-8"))


def cnt(rows, key):
    return Counter(r[key] for r in rows)


def by_year(y, rows=Q):
    return [r for r in rows if r["yil"] == y]


# Konu ağacı (mermaid)
_kc = Counter(q["konu"] for q in Q)
_mm = ['%%{init: {"flowchart": {"nodeSpacing": 10, "rankSpacing": 60}}}%%', "flowchart LR",
       "  S([GM Sınavı: 100 soru · 150 dk])"]
for _i, _g in enumerate(GRUPLAR):
    _n = sum(_kc[k] for k in GRUP[_g]) / len(YEARS)
    _mm.append(f'  S --> G{_i}["{_g}: ort. {_n:.1f}"]')
    tops = sorted(GRUP[_g], key=lambda k: -_kc[k])[:3]
    for _j, k in enumerate(tops):
        if _kc[k]:
            _mm.append(f'  G{_i} --> G{_i}K{_j}["{KONU[k]} ({_kc[k] / len(YEARS):.1f})"]')
ins["mermaid"] = "\n".join(_mm)

# GM ve GMY karşılaştırması
CMP = [
    ("Tarife & sınıflandırma", ["GM_TARIFE_SINIF", "GM_TARIFE_MEVZ"], ["G_TARIFE"]),
    ("Gümrük kıymeti", ["GM_KIYMET"], ["G_KIYMET"]),
    ("Menşe & tercihli ticaret", ["GM_MENSE", "GM_TERCIHLI_STA"], ["G_MENSE"]),
    ("Gümrük rejimleri", GRUP["Gümrük Rejimleri"],
     ["G_SERBEST_DOLASIM", "G_ANTREPO", "G_DAHILDE_ISLEME", "G_GKAI", "G_GECICI_ITHALAT", "G_HARICTE_ISLEME",
      "G_TRANSIT", "G_IHRACAT"]),
    ("Genel hükümler, beyan & özel işlemler",
     ["GM_TEMEL", "GM_GIRIS_BEYAN", "GM_OZEL_TASIT", "GM_POSTA", "GM_TASFIYE", "GM_SERBEST_BOLGE"],
     ["G_TEMEL_KAVRAM", "G_GIRIS_BEYAN", "G_OZEL_ISLEMLER", "G_TASFIYE", "G_SERBEST_BOLGE"]),
    ("Muafiyetler", ["GM_MUAFIYET"], ["G_MUAFIYET"]),
    ("Vergi alacağı, ceza & uzlaşma", ["GM_YUKUMLULUK_TEMINAT", "GM_TAHAKKUK_TAHSIL", "GM_GERI_VERME",
                                       "GM_CEZA_UZLASMA"],
     ["G_YUKUMLULUK_TEMINAT", "G_TAHAKKUK_TAHSIL", "G_GERI_VERME", "G_CEZA_ITIRAZ"]),
    ("Kaçakçılık (5607)", ["GM_KACAKCILIK"], ["G_KACAKCILIK"]),
    ("Meslek, YGM & kolaylaştırma", ["GM_MESLEK", "GM_YGM", "GM_KOLAYLASTIRMA"],
     ["G_MESLEK", "G_YGM", "G_KOLAYLASTIRMA"]),
    ("İç vergiler, kambiyo & fonlar", GRUP["İç Vergiler, Kambiyo & Fonlar"], []),
    ("Dış ticaret politikası & uluslararası ticaret", GRUP["Dış Ticaret Politikası & Uluslararası Ticaret"],
     ["G_DIS_TICARET_POL", "G_DIS_TIC_BELGE"]),
]
gmy_cmp = []
if GMY_DIR and all(os.path.exists(os.path.join(GMY_DIR, f"cls_{y}.json")) for y in YEARS):
    G = [r for y in YEARS for r in json.load(open(os.path.join(GMY_DIR, f"cls_{y}.json"), encoding="utf-8"))
         if r["bolum"] == "GUMRUK"]
    gk = Counter(r["konu"] for r in G)
    covered = set(k for _, _, ks in CMP for k in ks)
    missing = set(gk) - covered
    assert not missing, f"GMY eşlenmemiş konular: {missing}"
    covered_gm = set(k for _, ks, _ in CMP for k in ks)
    assert covered_gm == set(KONU), set(KONU) ^ covered_gm
    for alan, gm_k, gmy_k in CMP:
        a, b = sum(_kc[k] for k in gm_k), sum(gk[k] for k in gmy_k)
        gmy_cmp.append(dict(alan=alan, gm=a * 100 / len(Q), gmy=b * 100 / len(G), gm_n=a, gmy_n=b))

# ------------------------------------------------------------------ CSV / JSON
with open(os.path.join(OUT, "gm_soru_siniflandirma.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["Yıl", "Soru No", "Doğru Cevap", "Konu Grubu", "Konu", "Alt Konu", "Soru Kalıbı", "Soru Tipi",
                "Mevzuat", "Madde", "Zorluk", "Hesap Türü", "Fasıl", "Sayısal Değer", "Soru Özeti",
                "Öğrenilecek Bilgi"])
    for q in Q:
        w.writerow([q["yil"], q["n"], q["cevap"], KONU2GRUP[q["konu"]], KONU[q["konu"]], q["alt_konu"], KOK[q["kok"]],
                    TIP[q["tip"]], MEVZUAT[q["mevzuat"]], q["madde"], ZORLUK[q["zorluk"]],
                    HESAP.get(q["hesap"], ""), ", ".join(q["fasil"]), q["sayisal"], q["ozet"], q["anahtar_bilgi"]])
json.dump([{k: q[k] for k in FIELDS} for q in Q], open(os.path.join(OUT, "gm_soru_siniflandirma.json"), "w",
          encoding="utf-8"), ensure_ascii=False, indent=1)

# ------------------------------------------------------------------ istatistik
konu_stat = []
for k in KONU:
    m = {y: sum(1 for q in Q if q["yil"] == y and q["konu"] == k) for y in YEARS}
    tot = sum(m.values())
    if tot:
        konu_stat.append(dict(k=k, l=KONU[k], m=m, tot=tot, avg=tot / len(YEARS),
                              yrs=sum(1 for v in m.values() if v), early=(m[2021] + m[2022]) / 2,
                              late=(m[2024] + m[2025]) / 2, g=KONU2GRUP[k]))
konu_stat.sort(key=lambda r: (-r["tot"], r["l"]))


def save(fig, name):
    fig.savefig(os.path.join(IMG, name), dpi=150, bbox_inches="tight")
    plt.close(fig)
    return f"grafikler/{name}"


def hbar(ax, labels, vals, color=SER[0], title=None, maxv=None, fmtv=str):
    ys = list(range(len(labels)))[::-1]
    ax.barh(ys, vals, color=color, height=0.62)
    ax.set_yticks(ys)
    ax.set_yticklabels(labels, fontsize=9)
    ax.xaxis.grid(True, color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    m = maxv or max(list(vals) + [1])
    ax.set_xlim(0, m * 1.15)
    for yv, v in zip(ys, vals):
        ax.text(v + m * 0.012, yv, fmtv(v), va="center", fontsize=8.5, color=INK2)
    if title:
        ax.set_title(title, loc="left", fontsize=11.5, color=INK, fontweight="bold")


def heat_png(rows, cols, name, title, figw=8.6, vmax=None, extra=None, group=False):
    import numpy as np
    labels, data, seps = [], [], []
    last = None
    for r in rows:
        if group and r["g"] != last:
            last = r["g"]
            labels.append(f"— {r['g']} —")
            data.append([np.nan] * len(cols))
            seps.append(len(labels) - 1)
        labels.append(r["l"])
        data.append([r["m"].get(c, 0) for c in cols])
    mat = np.array(data, dtype=float)
    vmax = vmax or max(1, np.nanmax(mat))
    cmap = LinearSegmentedColormap.from_list("seq", SEQ)
    cmap.set_bad("#eef0f2")
    fig, ax = plt.subplots(figsize=(figw, 0.32 * len(labels) + 1.3))
    ax.imshow(np.ma.masked_invalid(mat), cmap=cmap, vmin=0, vmax=vmax, aspect="auto")
    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels([str(c) for c in cols])
    ax.xaxis.tick_top()
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=8.5)
    for i in seps:
        ax.get_yticklabels()[i].set_fontweight("bold")
    ri = 0
    for i, lab in enumerate(labels):
        if i in seps:
            continue
        r = rows[ri]
        ri += 1
        for j, c in enumerate(cols):
            v = r["m"].get(c, 0)
            ax.text(j, i, str(v) if v else "·", ha="center", va="center", fontsize=8.5,
                    color="#ffffff" if v / vmax > 0.55 else INK)
        if extra:
            ax.text(len(cols) - 0.35, i, extra(r), ha="left", va="center", fontsize=8.5, color=INK2)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks([x - 0.5 for x in range(1, len(cols))], minor=True)
    ax.set_yticks([y - 0.5 for y in range(1, len(labels))], minor=True)
    ax.grid(which="minor", color="#fcfcfb", lw=2)
    ax.tick_params(which="both", length=0)
    ax.set_title(title, loc="left", fontsize=12, color=INK, fontweight="bold", pad=24)
    return save(fig, name)


def stack_png(rows, keys, names, colors, name, title):
    fig, ax = plt.subplots(figsize=(8.6, 0.55 * len(rows) + 1.9))
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
              ncol=2, frameon=False, fontsize=8.5)
    return save(fig, name)


imgs = {}
# Optik form şeması
fig, ax = plt.subplots(figsize=(13, 3.2))
for yi, y in enumerate(YEARS):
    for q in by_year(y):
        ax.add_patch(plt.Circle((q["n"], -yi * 1.35), 0.42, color=SER[GRUPLAR.index(KONU2GRUP[q["konu"]])]))
ax.set_xlim(0, 101)
ax.set_ylim(-(len(YEARS) - 1) * 1.35 - 0.8, 0.8)
ax.set_aspect("equal")
ax.set_yticks([-i * 1.35 for i in range(len(YEARS))])
ax.set_yticklabels([f"{y}{' (B)' if y == 2022 else ''}" for y in YEARS])
ax.set_xticks([1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
ax.tick_params(length=0)
for s in ax.spines.values():
    s.set_visible(False)
ax.set_title("Optik form şeması: her daire bir soru, renk konu grubu", loc="left", fontsize=11, color=INK,
             fontweight="bold")
ax.legend([plt.Line2D([], [], marker="o", ls="", color=SER[i], ms=8) for i in range(len(GRUPLAR))], GRUPLAR,
          loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=3, frameon=False, fontsize=8.5)
imgs["optik"] = save(fig, "00_optik_form_semasi.png")

for y in YEARS:
    kc = cnt(by_year(y), "konu").most_common()
    fig, ax = plt.subplots(figsize=(8.6, 0.3 * len(kc) + 1.0))
    hbar(ax, [KONU[k] for k, _ in kc], [v for _, v in kc],
         color=[SER[GRUPLAR.index(KONU2GRUP[k])] for k, _ in kc], title=f"{y} · Konular (100 soru)")
    imgs[f"{y}_konu"] = save(fig, f"{y}_1_konular.png")
    fig, axs = plt.subplots(1, 2, figsize=(11, 3.6), gridspec_kw={"wspace": 0.85})
    kk = cnt(by_year(y), "kok")
    ks = [k for k in KOK_ORDER if kk.get(k)]
    hbar(axs[0], [KOK[k] for k in ks], [kk[k] for k in ks], color=[SER[KOK_ORDER.index(k)] for k in ks],
         title="Soru kalıbı")
    tc = cnt(by_year(y), "tip").most_common()
    hbar(axs[1], [TIP[k] for k, _ in tc], [v for _, v in tc], color=SER[6], title="Soru tipi")
    imgs[f"{y}_kok_tip"] = save(fig, f"{y}_2_soru_kalibi_ve_tipi.png")

imgs["hm_konu"] = heat_png(konu_stat, YEARS, "10_konu_isi_haritasi.png", "Konular × yıl (soru sayısı)",
                           extra=lambda r: f"Σ{r['tot']}  ort.{r['avg']:.1f}  {r['yrs']}/5", figw=9.6)
top = konu_stat[:15]
fig, ax = plt.subplots(figsize=(8.6, 5.4))
hbar(ax, [r["l"] for r in top], [r["tot"] for r in top], color=[SER[GRUPLAR.index(r["g"])] for r in top],
     title="En çok soru gelen 15 konu (2021–2025 toplam)")
imgs["top"] = save(fig, "11_en_cok_soru_gelen_konular.png")
imgs["grup"] = stack_png([{"l": y, "m": Counter(KONU2GRUP[q["konu"]] for q in by_year(y))} for y in YEARS],
                         GRUPLAR, {g: g for g in GRUPLAR}, SER, "12_konu_grubu_paylari.png",
                         "Konu grubu payları, yıla göre")
imgs["kok"] = stack_png([{"l": y, "m": cnt(by_year(y), "kok")} for y in YEARS], KOK_ORDER, KOK, SER,
                        "13_soru_kalibi.png", "Soru kalıbı (kök yapısı), yıla göre")


def rows_for(field, order, names):
    rr = [{"l": names[k], "m": {y: sum(1 for q in by_year(y) if q[field] == k) for y in YEARS}} for k in order]
    return sorted([r for r in rr if sum(r["m"].values())], key=lambda r: -sum(r["m"].values()))


imgs["hm_tip"] = heat_png(rows_for("tip", TIP_ORDER, TIP), YEARS, "14_soru_tipi.png", "Soru tipi × yıl",
                          extra=lambda r: f"Σ{sum(r['m'].values())}")
imgs["hm_mev"] = heat_png(rows_for("mevzuat", MEVZUAT_ORDER, MEVZUAT), YEARS, "15_mevzuat_kaynagi.png",
                          "Dayanılan mevzuat × yıl", extra=lambda r: f"Σ{sum(r['m'].values())}")
hes = [q for q in Q if q["tip"] == "HESAPLAMA"]
imgs["hm_hesap"] = heat_png([{"l": HESAP[k], "m": {y: sum(1 for q in hes if q["yil"] == y and q["hesap"] == k)
                                                    for y in YEARS}} for k in HESAP
                             if any(q["hesap"] == k for q in hes)], YEARS, "16_hesap_turleri.png",
                            "Hesap soruları: hesaplanan büyüklük × yıl", extra=lambda r: f"Σ{sum(r['m'].values())}")
fas = {}
for q in Q:
    for f in q["fasil"]:
        fas.setdefault(f, Counter())[q["yil"]] += 1
fas_rows = [{"g": "{} · {}".format(*fasil_bolum(f)), "l": f"Fasıl {f}", "m": dict(fas[f])} for f in sorted(fas)]
if fas_rows:
    imgs["hm_fasil"] = heat_png(fas_rows, YEARS, "17_fasil_isi_haritasi.png", "Sorulan fasıllar × yıl",
                                vmax=4, group=True, extra=lambda r: f"Σ{sum(r['m'].values())}")
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
    imgs["dumb"] = save(fig, "18_yukselen_dusen_konular.png")
if gmy_cmp:
    import numpy as np
    fig, ax = plt.subplots(figsize=(8.6, 0.55 * len(gmy_cmp) + 1.2))
    ys = np.arange(len(gmy_cmp))[::-1]
    ax.barh(ys + 0.18, [r["gm"] for r in gmy_cmp], height=0.34, color=SER[0], label="GM (500 soru)")
    ax.barh(ys - 0.18, [r["gmy"] for r in gmy_cmp], height=0.34, color=SER[1], label="GMY gümrük bölümü (400 soru)")
    ax.set_yticks(ys)
    ax.set_yticklabels([r["alan"] for r in gmy_cmp], fontsize=9)
    for yv, r in zip(ys, gmy_cmp):
        ax.text(r["gm"] + 0.4, yv + 0.18, f"%{r['gm']:.1f}", va="center", fontsize=8, color=INK2)
        ax.text(r["gmy"] + 0.4, yv - 0.18, f"%{r['gmy']:.1f}", va="center", fontsize=8, color=INK2)
    ax.xaxis.grid(True, color=GRID)
    ax.set_axisbelow(True)
    ax.legend(loc="lower right", frameon=False, fontsize=8.5)
    ax.set_title("GM ve GMY'de konu ağırlıkları (soruların yüzdesi)", loc="left", fontsize=11.5, color=INK,
                 fontweight="bold")
    imgs["gmy"] = save(fig, "19_gm_gmy_karsilastirma.png")


# ------------------------------------------------------------------ README
def md_table(head, rows):
    out = "| " + " | ".join(head) + " |\n|" + "|".join(["---"] * len(head)) + "|\n"
    for r in rows:
        out += "| " + " | ".join(str(c).replace("|", "/") for c in r) + " |\n"
    return out


def strip(s):
    return re.sub(r"<[^>]+>", "", s)


md = ["# GM Soru Atlası 2021–2025\n",
      "Gümrük Müşavirliği sınavının 2021–2025 yıllarına ait **500 sorusunun** konu, soru kalıbı, soru tipi, mevzuat, "
      "tarife faslı ve hesap türüne göre analizi. Etkileşimli sürüm: `GM_Soru_Atlasi.html`, yazdırılabilir sürüm: "
      "`GM_Soru_Atlasi.pdf`.\n",
      "## İçindekiler\n\n1. [Sınavın yapısı](#1-sınavın-yapısı)\n2. [Yıl yıl analiz](#2-yıl-yıl-analiz)\n"
      "3. [Yılların karşılaştırması](#3-yılların-karşılaştırması)\n"
      "4. [Derinlemesine: tarife, hesap ve sayısal bilgiler](#4-derinlemesine-tarife-hesap-ve-sayısal-bilgiler)\n"
      "5. [Sonuç](#5-sonuç-en-çok-neyden-nasıl-soruluyor)\n",
      "## 1. Sınavın yapısı\n",
      "Her yıl 100 soru / 150 dakika; genel yetenek ve genel kültür bölümü yok, soruların tamamı mesleki. 2022 dosyası "
      "B kitapçığıdır (soru sırası A'dan farklı).\n",
      md_table(["Konu grubu", *map(str, YEARS), "Ort./yıl"],
               [[g, *[sum(1 for q in by_year(y) if KONU2GRUP[q["konu"]] == g) for y in YEARS],
                 f"{sum(1 for q in Q if KONU2GRUP[q['konu']] == g) / len(YEARS):.1f}"] for g in GRUPLAR]),
      "\n```mermaid\n" + ins["mermaid"] + "\n```\n", f"![Optik form şeması]({imgs['optik']})\n",
      "## 2. Yıl yıl analiz\n"]
for y in YEARS:
    md.append(f"### {y}{' (B kitapçığı)' if y == 2022 else ''}\n")
    md += [f"- {strip(t)}" for t in ins["years"][str(y)]]
    md += ["", f"![{y} konular]({imgs[f'{y}_konu']})\n", f"![{y} kalıp ve tip]({imgs[f'{y}_kok_tip']})\n"]
    g = by_year(y)
    md.append("<details><summary>Konu tablosu ve soru numaraları</summary>\n")
    md.append(md_table(["Konu", "Soru", "Soru numaraları"],
                       [[KONU[k], v, ", ".join(str(q["n"]) for q in g if q["konu"] == k)]
                        for k, v in cnt(g, "konu").most_common()]))
    md.append("\n</details>\n")
md.append("## 3. Yılların karşılaştırması\n")
md.append(f"![Konu ısı haritası]({imgs['hm_konu']})\n")
md.append(md_table(["#", "Konu", *map(str, YEARS), "Toplam", "Ort./yıl", "Çıktığı yıl", "Eğilim"],
                   [[i + 1, r["l"], *[r["m"][y] for y in YEARS], r["tot"], f"{r['avg']:.1f}", f"{r['yrs']}/5",
                     f"{'▲' if r['late'] - r['early'] >= 1 else '▼' if r['late'] - r['early'] <= -1 else '■'} "
                     f"{r['late'] - r['early']:+.1f}"] for i, r in enumerate(konu_stat)]))
for k in ("top", "grup", "kok", "hm_tip", "hm_mev", "dumb"):
    if k in imgs:
        md.append(f"\n![]({imgs[k]})\n")
md.append("## 4. Derinlemesine: tarife, hesap ve sayısal bilgiler\n")
md.append("### Tarife sınıflandırma\n")
if "hm_fasil" in imgs:
    md.append(f"![Fasıllar]({imgs['hm_fasil']})\n")
md.append(strip(ins.get("tarife_not", "")).strip() + "\n")
md.append("### Hesap soruları\n")
md.append(f"![Hesap türleri]({imgs['hm_hesap']})\n")
md.append(strip(ins.get("hesap_not", "")).strip() + "\n")
if gmy_cmp:
    md.append("### GM ve GMY karşılaştırması\n")
    md.append(f"![GM-GMY]({imgs['gmy']})\n")
    md.append(md_table(["Alan", "GM %", "GM soru", "GMY %", "GMY soru"],
                       [[r["alan"], f"{r['gm']:.1f}", r["gm_n"], f"{r['gmy']:.1f}", r["gmy_n"]] for r in gmy_cmp]))
md.append("\n### Sınavda sorulan süre, oran ve tutarlar\n")
S = sorted([q for q in Q if q["tip"] == "SAYISAL" and q["sayisal"]],
           key=lambda q: (GRUPLAR.index(KONU2GRUP[q["konu"]]), KONU[q["konu"]], q["yil"]))
md.append(md_table(["Konu", "Değer", "Bilgi", "Yıl/Soru"],
                   [[KONU[q["konu"]], q["sayisal"], f"{q['alt_konu']}: {q['anahtar_bilgi']}", f"{q['yil']}/{q['n']}"]
                    for q in S]))
md.append("\n### Tekrar eden soru kalıpları\n")
md.append(md_table(["Soru kalıbı", "Konu", *map(str, YEARS), "Doğru bilgi"],
                   [[t["kalip"], KONU.get(t["konu"], t["konu"]),
                     *[", ".join(map(str, t["sorular"].get(str(y), []))) or "·" for y in YEARS], t["bilgi"]]
                    for t in ins["tekrar"]]))
md.append("\n## 5. Sonuç: en çok neyden, nasıl soruluyor?\n")
for p in ins["sonuc"]["paragraflar"]:
    md.append(f"### {p['baslik']}\n")
    md += [f"- {strip(m)}" for m in p["maddeler"]]
    md.append("")
md.append("### Çalışma öncelik listesi\n")
for title, lo, hi in (("Öncelik 1 — yılda ort. 5+ soru", 5, 99), ("Öncelik 2 — yılda ort. 2–5 soru", 2, 5),
                      ("Öncelik 3 — yılda ort. 2'den az", 0, 2)):
    md.append(f"**{title}:** " + ", ".join(f"{r['l']} ({r['avg']:.1f})" for r in konu_stat if lo <= r["avg"] < hi)
              + "\n")
md.append("## Dosyalar\n")
md.append(md_table(["Dosya", "İçerik"], [
    ["`GM_Soru_Atlasi.html`", "Etkileşimli rapor: optik form şeması, yıl sekmeleri, ısı haritaları, fasıl ve hesap analizi"],
    ["`GM_Soru_Atlasi.pdf`", "Raporun yazdırılabilir A4 sürümü"],
    ["`gm_soru_siniflandirma.csv`", "500 sorunun tam sınıflandırması (Excel'de açılır)"],
    ["`gm_soru_siniflandirma.json`", "Aynı veri, JSON"],
    ["`grafikler/`", "Bu rapordaki PNG grafikler"],
    ["`kaynak/`", "Soru/cevap çıkarma ve rapor üretme betikleri, taksonomi"],
]))
open(os.path.join(OUT, "README.md"), "w", encoding="utf-8").write("\n".join(md))

# ------------------------------------------------------------------ HTML
labels = dict(konu=KONU, grup=GRUP, konu2grup=KONU2GRUP, kok=KOK, kok_order=KOK_ORDER, tip=TIP, tip_order=TIP_ORDER,
              mevzuat=MEVZUAT, mevzuat_order=MEVZUAT_ORDER, hesap=HESAP, zorluk=ZORLUK,
              bolumler=[list(b) for b in BOLUMLER])
data = dict(labels=labels, years=YEARS, questions=[{k: q[k] for k in FIELDS} for q in Q], gmy_cmp=gmy_cmp,
            insights={k: v for k, v in ins.items() if k not in ("yontem", "mermaid")})
tpl = open(os.path.join(WORK, "template_gm.html"), encoding="utf-8").read()
payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
page = tpl.replace("/*__DATA__*/null", payload).replace('<pre class="mermaid" id="mm"></pre>',
                                                        '<pre class="mermaid" id="mm">' + ins["mermaid"] + "</pre>")
assert payload in page and ins["mermaid"] in page
open(os.path.join(WORK, "artifact_gm.html"), "w", encoding="utf-8").write(page)
standalone = ("<!doctype html>\n<html lang=\"tr\">\n<head>\n<meta charset=\"utf-8\">\n"
              "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1,viewport-fit=cover\">\n"
              + page.replace('<div class="wrap">', '</head>\n<body>\n<div class="wrap">', 1)
              + "\n<script src=\"https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js\"></script>\n"
              "<script>try{mermaid.initialize({startOnLoad:true,theme:matchMedia('(prefers-color-scheme: dark)').matches?'dark':'neutral'})}catch(e){}</script>\n"
              "</body>\n</html>\n")
open(os.path.join(OUT, "GM_Soru_Atlasi.html"), "w", encoding="utf-8").write(standalone)
print("tamam:", len(Q), "soru;", len(imgs), "grafik;", OUT)
