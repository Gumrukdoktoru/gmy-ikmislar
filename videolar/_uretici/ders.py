#!/usr/bin/env python3
"""GMY Konu Anlatımı (ders) videoları üreticisi. Ortak parçalar build.py'den gelir.

Kullanım:
  python3 ders.py plan 01             -> audio/d01/segments.json
  python3 ders.py words 01 [seg ...]  -> audio/d01/<seg>.words.json (yerel Whisper)
  python3 ders.py build 01            -> ../gmy-ders-01/index.html + assets

Spec: spec/ders01.json
  intro{chips, parts}, stats{label, years, values, parts}, sections[{title, madde, kind, ...parts}],
  quiz{soru + read/explain/board}, summary{items, parts, badge?}, outro{title, next, parts}
  sections.kind: law (kanun metni kartı) | table (karşılaştırma tablosu) | flow | branch | split | steps | formula | timeline
"""
import json
import math
import os
import shutil
import subprocess
import sys

import build as B
from build import (Aligner, Comp, POSES, FPS_ENV, HERE, animate_show, callout_html, caption_chunks, diagram_html, esc,
                   est_lines, intro_title_px, mix_audio, r3, read_audio, show_callout, speech_bounds, tokens, write_wav)

# ek kutu türü: İPUCU (hafıza kodu / pratik ipucu)
B.CALLOUT_LABEL["ipucu"] = "İPUCU"
B.CALLOUT_POSE["ipucu"] = "onay"
B.CALLOUT_SFX["ipucu"] = "chime"
B.CALLOUT_ICON["ipucu"] = ('<svg viewBox="0 0 64 64"><path d="M32 6 C20 6 12 15 12 26 C12 34 17 39 21 43 L21 50 L43 50 L43 43 '
                           'C47 39 52 34 52 26 C52 15 44 6 32 6 Z" fill="none" stroke="currentColor" stroke-width="5" stroke-linejoin="round"/>'
                           '<path d="M24 57 L40 57" stroke="currentColor" stroke-width="5" stroke-linecap="round"/></svg>')

LETTERS = "ABCDE"
THINK = "Videoyu durdurabilirsin. Beş saniye düşün!"

DCSS = r"""
.callout.ipucu .cl{background:var(--green);color:#fff}
/* istatistik + gündem */
.st-k{position:absolute;left:64px;top:128px;font-family:"GK Mono";font-weight:700;font-size:26px;letter-spacing:.2em;color:var(--gold)}
.st-t{position:absolute;left:64px;top:168px;font-weight:900;font-size:58px;color:#fff;letter-spacing:-.02em}
.chart{position:absolute;left:64px;top:290px;width:620px;height:470px;border-radius:26px;background:rgba(19,35,94,.55);border:3px solid rgba(159,176,224,.25)}
.chart .cap{position:absolute;left:30px;top:20px;font-family:"GK Mono";font-weight:700;font-size:20px;color:var(--muted);letter-spacing:.06em}
.chart .base{position:absolute;left:36px;right:36px;bottom:70px;height:4px;background:rgba(159,176,224,.6);border-radius:2px}
.chart .bar{position:absolute;bottom:74px;width:80px;border-radius:14px 14px 4px 4px;background:linear-gradient(180deg,#FFD27A,#F2B233);transform-origin:50% 100%}
.chart .bar.last{background:linear-gradient(180deg,#FFA060,#FF7A1A)}
.chart .bv{position:absolute;width:80px;text-align:center;font-family:"GK Mono";font-weight:800;font-size:34px;color:#fff}
.chart .bx{position:absolute;bottom:24px;width:80px;text-align:center;font-family:"GK Mono";font-weight:700;font-size:22px;color:var(--muted)}
.st-tot{position:absolute;left:64px;top:786px;width:620px;padding:14px 24px;border-radius:18px;background:rgba(242,178,51,.12);border:3px solid var(--gold);font-weight:800;font-size:26px;color:#fff;opacity:0}
.st-tot b{color:var(--gold2)}
.agenda{position:absolute;left:720px;top:290px;width:606px}
.agenda .ah{font-family:"GK Mono";font-weight:700;font-size:24px;letter-spacing:.2em;color:var(--gold2);margin-bottom:16px}
.agenda .ai{display:flex;align-items:center;gap:18px;min-height:86px;margin-bottom:12px;padding:10px 22px;border-radius:18px;background:rgba(19,35,94,.85);border:3px solid rgba(159,176,224,.35);font-weight:800;font-size:26px;line-height:1.15;color:#fff;opacity:0}
.agenda .ai .n{flex:0 0 auto;width:50px;height:50px;border-radius:50%;background:var(--gold);color:var(--navy);display:flex;align-items:center;justify-content:center;font-family:"GK Mono";font-weight:800;font-size:24px}
.agenda .ai.qz .n{background:var(--green);color:#fff}
/* bölüm geçişi */
.sting{position:absolute;left:0;top:0;width:1340px;height:1080px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;opacity:0}
.sting .sn{font-family:"GK Mono";font-weight:800;font-size:40px;letter-spacing:.3em;color:var(--gold)}
.sting .stt{font-weight:900;font-size:88px;letter-spacing:-.03em;color:#fff;text-align:center;max-width:1220px;line-height:1.04}
/* kanun metni kartı */
.law{position:absolute;left:64px;top:268px;width:1262px;height:420px;border-radius:26px;background:var(--paper);color:var(--ink);box-shadow:0 22px 44px rgba(0,0,0,.4);overflow:hidden;opacity:0}
.law .lh{position:absolute;left:0;top:0;right:0;height:60px;display:flex;align-items:center;gap:14px;padding:0 30px;background:#E9E1CC;border-bottom:3px solid rgba(22,34,76,.15)}
.law .lh .lb{padding:6px 14px;border-radius:10px;background:var(--ink);color:#fff;font-weight:900;font-size:20px;letter-spacing:.1em}
.law .lh .lm{font-family:"GK Mono";font-weight:700;font-size:22px;color:#3A4775}
.law .lt{position:absolute;left:44px;right:44px;top:78px;font-family:"GK Serif";font-weight:600;line-height:1.36;color:var(--ink)}
.law .mk{position:relative;display:inline-block}
.law .mk .mkbg{position:absolute;left:-5px;right:-5px;bottom:3px;height:45%;background:rgba(242,178,51,.72);border-radius:6px;transform-origin:0 50%;z-index:0}
.law .mk .mkt{position:relative;z-index:1}
.law .plain{position:absolute;left:24px;right:24px;bottom:18px;padding:12px 22px;border-radius:16px;background:#E2F3EA;border:3px solid var(--green);opacity:0}
.law .plain b{display:block;font-weight:900;font-size:19px;letter-spacing:.16em;color:#0E7A4E}
.law .plain p{font-family:"GK Serif";font-weight:600;font-size:25px;line-height:1.26;color:var(--ink);margin-top:4px}
/* karşılaştırma tablosu */
.tbl{position:absolute;left:64px;top:268px;width:1262px;height:420px}
.tbl .tr{position:absolute;left:0;width:1262px;display:grid;gap:10px;opacity:0}
.tbl .td{display:flex;align-items:center;padding:6px 18px;border-radius:14px;background:var(--navy2);border:3px solid rgba(159,176,224,.35);color:#fff;font-weight:700;line-height:1.16}
.tbl .td.k{background:rgba(242,178,51,.12);border-color:rgba(242,178,51,.6);color:var(--gold2);font-weight:800}
.tbl .th .td{justify-content:center;text-align:center;font-weight:900;letter-spacing:.05em}
.tbl .th .td.gold{background:rgba(242,178,51,.24);border-color:var(--gold);color:var(--gold2)}
.tbl .th .td.navy{background:rgba(159,176,224,.2);color:#fff}
.tbl .th .td.green{background:rgba(24,165,107,.28);border-color:var(--green);color:#BFF2DA}
.tbl .th .td.red{background:rgba(217,68,63,.26);border-color:var(--red);color:#FFC9C6}
.tbl .th .td.blank{background:transparent;border-color:transparent}
.tbl .td .glowr{position:absolute}
.tbl .tr .hlbox{position:absolute;inset:-8px;border-radius:18px;border:5px solid var(--gold);opacity:0}
/* özet rozeti */
.sbadge{position:absolute;left:64px;top:846px;padding:12px 24px;border-radius:14px;background:rgba(24,165,107,.2);border:3px solid #18A56B;color:#BFF2DA;font-weight:800;font-size:25px;opacity:0}
"""


def load_spec(vid):
    with open(os.path.join(HERE, "spec", f"ders{vid}.json"), encoding="utf-8") as f:
        return json.load(f)


def adir_of(vid):
    return os.path.join(HERE, "audio", f"d{vid}")


def segments(spec):
    segs = [{"id": "intro", "parts": spec["intro"]["parts"]}]
    if spec.get("stats"):
        segs.append({"id": "stats", "parts": spec["stats"]["parts"]})
    for k, s in enumerate(spec["sections"], 1):
        segs.append({"id": f"s{k}", "parts": s["parts"]})
    q = spec["quiz"]
    segs.append({"id": "quiz_read", "parts": q["read"]})
    segs.append({"id": "quiz_think", "parts": [{"say": q.get("think", THINK)}]})
    segs.append({"id": "quiz_exp", "parts": q["explain"]})
    segs.append({"id": "summary", "parts": spec["summary"]["parts"]})
    segs.append({"id": "outro", "parts": spec["outro"]["parts"]})
    for s in segs:
        s["text"] = " ".join(p["say"].strip() for p in s["parts"])
    return segs


def cmd_plan(vid):
    spec = load_spec(vid)
    segs = segments(spec)
    d = adir_of(vid)
    os.makedirs(d, exist_ok=True)
    out = [{"id": s["id"], "text": s["text"], "chars": len(s["text"])} for s in segs]
    with open(os.path.join(d, "segments.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"ders {vid}: {len(out)} segment, {sum(o['chars'] for o in out)} karakter")
    for o in out:
        print(f"  {o['id']:10s} {o['chars']:5d}")


def cmd_words(vid, only=None):
    d = adir_of(vid)
    segs = json.load(open(os.path.join(d, "segments.json"), encoding="utf-8"))
    for s in segs:
        if only and s["id"] not in only:
            continue
        mp3 = os.path.join(d, s["id"] + ".mp3")
        wj = os.path.join(d, s["id"] + ".words.json")
        if os.path.exists(wj) or not os.path.exists(mp3):
            continue
        tmp = os.path.join(d, "_tr_" + s["id"])
        os.makedirs(tmp, exist_ok=True)
        subprocess.run(["npx", "hyperframes", "transcribe", mp3, "--model", "small", "--language", "tr",
                        "--json", "-d", tmp, "--timeout", "3600000"], capture_output=True, text=True)
        tr = json.load(open(os.path.join(tmp, "transcript.json"), encoding="utf-8"))
        words = tr.get("words", tr) if isinstance(tr, dict) else tr
        with open(wj, "w", encoding="utf-8") as f:
            json.dump(words, f, ensure_ascii=False)
        shutil.rmtree(tmp, ignore_errors=True)
        print("words", s["id"], len(words), flush=True)


# ----------------------------------------------------------------------------
# sahne parçaları
# ----------------------------------------------------------------------------
def mark_html(text, marks, mid_prefix):
    """text içindeki her işaretli ifadeyi sözcük sözcük vurgulanabilir yapar. Döner: (html, [(mid, nw)])"""
    h = esc(text)
    out = []
    for i, m in enumerate(marks):
        m_esc = esc(m)
        if m_esc not in h:
            raise ValueError(f"işaret metinde yok: {m}")
        ws = m_esc.split(" ")
        mid = f"{mid_prefix}{i}"
        span = " ".join(f'<span class="mk"><span class="mkbg" id="{mid}w{j}"></span><span class="mkt">{w}</span></span>'
                        for j, w in enumerate(ws))
        h = h.replace(m_esc, span, 1)
        out.append((mid, len(ws)))
    return h, out


def law_html(px, sec):
    law = sec["law"]
    plain = law.get("plain")
    plain_h = 0
    if plain:
        plain_h = 14 + 24 + est_lines(plain, 25, 1262 - 48 - 50, 0.47) * 25 * 1.26 + 24
    avail = 420 - 78 - (plain_h + 26 if plain else 20)
    fs = 24
    for cand in (34, 32, 30, 29, 28, 27, 26, 25, 24):
        if est_lines(law["text"], cand, 1262 - 88, 0.47) * cand * 1.36 <= avail:
            fs = cand
            break
    body, marks = mark_html(law["text"], law.get("marks", []), f"{px}-mk")
    html = (f'<div class="law" id="{px}-law"><div class="lh"><span class="lb">KANUN METNİ</span><span class="lm">{esc(law.get("ref", sec["madde"]))}</span></div>'
            f'<div class="lt" style="font-size:{fs}px">“{body}”</div>'
            + (f'<div class="plain" id="{px}-plain"><b>SADE DİLLE</b><p>{esc(plain)}</p></div>' if plain else "")
            + "</div>")
    return html, marks


def table_html(px, tb):
    cols = tb["cols"]
    nc = len(cols)
    rows = tb["rows"]
    nr = len(rows)
    tmpl = "grid-template-columns:" + (tb.get("tmpl") or f"{tb.get('kw', 290)}px repeat({nc - 1},1fr)")
    hh = 62
    gap = 10
    rh = min(88, int((420 - hh - gap * nr) / max(1, nr)))
    fs = 25 if rh >= 78 else (23 if rh >= 64 else 21)
    parts = []
    head = "".join(f'<div class="td {c.get("tone", "navy") if k else "blank"}" style="font-size:{22 if k else 20}px">{esc(c["title"])}</div>'
                   for k, c in enumerate(cols))
    parts.append(f'<div class="tr th" id="{px}-head" style="top:0;height:{hh}px;{tmpl}">{head}</div>')
    items = {"head": {"type": "row"}}
    for r, row in enumerate(rows):
        top = hh + gap + r * (rh + gap)
        cells = "".join(f'<div class="td{" k" if k == 0 else ""}" style="font-size:{fs - (1 if k == 0 else 0)}px">{esc(c)}</div>'
                        for k, c in enumerate(row["cells"]))
        parts.append(f'<div class="tr" id="{px}-{row["id"]}" style="top:{top}px;height:{rh}px;{tmpl}"><div class="hlbox" id="{px}-{row["id"]}-g"></div>{cells}</div>')
        items[row["id"]] = {"type": "row"}
    return f'<div class="tbl" id="{px}-tbl">{"".join(parts)}</div>', items


def show_item(C, px, sid, items, shown, tt):
    it = items.get(sid)
    if it is None:
        raise ValueError(f"bölümde yok: {sid}")
    if it["type"] == "row":
        C.fromto(f"#{px}-{sid}", {"opacity": 0, "x": -50}, {"opacity": 1, "x": 0, "duration": 0.45, "ease": "power3.out"}, tt)
        C.sound(tt, "pop", 0.4)
        shown.add(sid)
        return
    animate_show(C, px, sid, items, shown, tt)


# ----------------------------------------------------------------------------
def build_lesson(vid):
    spec = load_spec(vid)
    segs = segments(spec)
    adir = adir_of(vid)
    proj = os.path.normpath(os.path.join(HERE, "..", f"gmy-ders-{vid}"))
    os.makedirs(os.path.join(proj, "assets"), exist_ok=True)
    write_brief(proj, spec)

    A = {}
    for s in segs:
        x = read_audio(os.path.join(adir, s["id"] + ".mp3"))
        dur = len(x) / B.SR
        sb = speech_bounds(x)
        wj = os.path.join(adir, s["id"] + ".words.json")
        words = json.load(open(wj, encoding="utf-8")) if os.path.exists(wj) else []
        al = Aligner(s["text"], words, dur, sb)
        pst, idx = [], 0
        for p in s["parts"]:
            pst.append(al.t(idx))
            idx += len(tokens(p["say"]))
        A[s["id"]] = {"x": x, "dur": dur, "al": al, "pt": pst, "speech": sb, "seg": s}
        print(f"  {s['id']:10s} {dur:6.2f}s  eşleşme %{al.match_ratio*100:4.0f}")

    C = Comp()
    placements, poses = [], []
    XF = 0.45
    secs = spec["sections"]
    ns = len(secs)

    # ---------------- zamanlama
    T = {"intro_say": 1.1}
    placements.append((T["intro_say"], "intro"))
    t = T["intro_say"] + A["intro"]["dur"] + 0.5
    if spec.get("stats"):
        T["stats"] = t
        T["stats_say"] = t + 0.7
        placements.append((T["stats_say"], "stats"))
        t = T["stats_say"] + A["stats"]["dur"] + 0.6
    S = []
    for k in range(1, ns + 1):
        s = {"start": t, "say": t + 1.45}
        placements.append((s["say"], f"s{k}"))
        s["end"] = s["say"] + A[f"s{k}"]["dur"] + 0.7
        t = s["end"]
        S.append(s)
    q = {"start": t, "read": t + 1.5}
    placements.append((q["read"], "quiz_read"))
    q["think"] = q["read"] + A["quiz_read"]["dur"] + 0.3
    placements.append((q["think"], "quiz_think"))
    q["cd"] = q["think"] + A["quiz_think"]["speech"][1] + 0.25
    q["cd_end"] = q["cd"] + 5.0
    q["exp"] = q["cd_end"] + 0.35
    placements.append((q["exp"], "quiz_exp"))
    ex = A["quiz_exp"]
    q["board"] = q["exp"] + (ex["pt"][1] - 0.35 if len(ex["pt"]) > 1 else ex["dur"] * 0.3)
    q["end"] = q["exp"] + ex["dur"] + 0.7
    t = q["end"]
    T["sum"] = t
    T["sum_say"] = t + 1.0
    placements.append((T["sum_say"], "summary"))
    t = T["sum_say"] + A["summary"]["dur"] + 0.6
    T["out"] = t
    T["out_say"] = t + 0.8
    placements.append((T["out_say"], "outro"))
    TOTAL = math.ceil((T["out_say"] + A["outro"]["dur"] + 2.2) * 10) / 10
    seg_start = dict((sid, tt) for tt, sid in placements)

    def ptime(seg, k):
        return seg_start[seg] + A[seg]["pt"][k]

    def pend(seg, k):
        """parçanın bitişi (bir sonraki parçanın başı ya da konuşma sonu)"""
        pts = A[seg]["pt"]
        return seg_start[seg] + (pts[k + 1] if k + 1 < len(pts) else A[seg]["speech"][1])

    scenes_html = []

    def scene(sid, start, end, inner, track=1):
        scenes_html.append(f'<section id="{sid}" class="scene clip" data-start="{r3(start)}" data-duration="{r3(end - start)}" data-track-index="{track}">'
                           f'<div class="inner" id="{sid}-in">{inner}</div></section>')
        C.fromto(f"#{sid}-in", {"opacity": 0}, {"opacity": 1, "duration": XF, "ease": "power1.out"}, start)
        C.to(f"#{sid}-in", {"opacity": 0, "duration": XF, "ease": "power1.in"}, end - XF)

    first_main = T.get("stats", S[0]["start"])

    # ---------------- GİRİŞ
    vnum = spec["no"]
    title_words = spec["title"].split()
    tw_html = "".join(f'<span class="w" id="it-w{k}">{esc(w)}</span>' for k, w in enumerate(title_words))
    chips = spec["intro"].get("chips", [f"{ns} BÖLÜM", "ŞEMA + TUZAK", "MİNİ TEST"])
    chip_colors = ["#F2B233", "#FF7A1A", "#18A56B"]
    chips_html = "".join(
        f'<div class="chip" id="ic{k}" style="background:rgba(255,255,255,.08);border:3px solid {chip_colors[k % 3]};color:#fff"><span class="dot" style="background:{chip_colors[k % 3]}"></span>{esc(c)}</div>'
        for k, c in enumerate(chips))
    intro_inner = (
        f'<div class="intro-kicker" id="ik">GMY KONU ANLATIMI · DERS {vnum}/5</div>'
        f'<div class="intro-num" id="inum">{int(vnum):02d}</div>'
        f'<div class="intro-block"><div class="intro-title" id="ititle" style="font-size:{intro_title_px(spec["title"])}px">{tw_html}</div>'
        f'<div class="intro-sub" id="isub">{esc(spec["subtitle"])}</div>'
        f'<div class="chips">{chips_html}</div></div>'
        f'<div class="half" id="ihalf" style="left:1150px;top:150px"><div class="av-talk" id="ihalf-talk"><img src="assets/avatar/yarim_boy.png" alt=""></div></div>')
    intro_end = first_main + XF
    scene("sc-intro", 0, intro_end, intro_inner)
    C.sound(0.05, "whoosh", 0.8)
    C.fromto("#ik", {"x": -60, "opacity": 0}, {"x": 0, "opacity": 1, "duration": 0.6, "ease": "power3.out"}, 0.15)
    C.fromto("#inum", {"scale": 1.6, "opacity": 0}, {"scale": 1, "opacity": 1, "duration": 0.55, "ease": "back.out(1.6)"}, 0.3)
    C.sound(0.35, "thud", 0.7)
    for k in range(len(title_words)):
        C.fromto(f"#it-w{k}", {"y": 70, "opacity": 0, "rotation": 4}, {"y": 0, "opacity": 1, "rotation": 0, "duration": 0.55, "ease": "power4.out"}, 0.55 + 0.09 * k)
    C.fromto("#isub", {"y": 24, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.6, "ease": "power2.out"}, 1.05)
    for k in range(len(chips)):
        C.fromto(f"#ic{k}", {"scale": 0.6, "opacity": 0}, {"scale": 1, "opacity": 1, "duration": 0.45, "ease": "back.out(2)"}, 1.4 + 0.15 * k)
        C.sound(1.4 + 0.15 * k, "pop", 0.6)
    C.fromto("#ihalf", {"x": 520, "opacity": 0}, {"x": 0, "opacity": 1, "duration": 0.8, "ease": "back.out(1.2)"}, 0.4)
    for k, p in enumerate(spec["intro"]["parts"]):
        if p.get("chip") is not None:
            C.fromto(f"#ic{p['chip']}", {"scale": 1}, {"scale": 1.12, "duration": 0.25, "ease": "power2.out", "yoyo": True, "repeat": 1}, ptime("intro", k))
    C.fromto("#ititle", {"x": 0}, {"x": -14, "duration": max(1.0, intro_end - 2.0), "ease": "none"}, 1.5)

    # ---------------- NEDEN BU KONU? (istatistik + gündem)
    if spec.get("stats"):
        st = spec["stats"]
        vals = st["values"]
        yrs = st["years"]
        n = len(vals)
        vmax = max(vals) or 1
        cw_ = 620
        slot = (cw_ - 72) / n
        bars = ""
        for k, (y, v) in enumerate(zip(yrs, vals)):
            bx = 36 + slot * k + (slot - 80) / 2
            bh = max(8, int(300 * v / vmax))
            bars += (f'<div class="bar{" last" if k == n - 1 else ""}" id="st-b{k}" style="left:{bx:.0f}px;height:{bh}px"></div>'
                     f'<div class="bv" id="st-v{k}" style="left:{bx:.0f}px;bottom:{74 + bh + 8}px">{v}</div>'
                     f'<div class="bx" style="left:{bx:.0f}px">{esc(y)}</div>')
        ag_items = "".join(f'<div class="ai" id="ag{k}"><span class="n">{k + 1}</span>{esc(s_["title"])}</div>' for k, s_ in enumerate(secs))
        ag_items += f'<div class="ai qz" id="ag{ns}"><span class="n">✓</span>Mini test: 1 soru</div>'
        stats_inner = (
            f'<div class="st-k" id="st-k">NEDEN BU KONU?</div><div class="st-t" id="st-t">{esc(st.get("title", "Sınavda bu konu"))}</div>'
            f'<div class="chart" id="st-chart"><div class="cap">{esc(st["label"])}</div><div class="base"></div>{bars}</div>'
            f'<div class="st-tot" id="st-tot">{st["total_html"]}</div>'
            f'<div class="agenda"><div class="ah" id="ag-h">BU DERSTE</div>{ag_items}</div>')
        scene("sc-stats", T["stats"], S[0]["start"] + XF, stats_inner)
        t0 = T["stats"]
        C.sound(t0, "whoosh", 0.6)
        C.fromto("#st-k", {"x": -40, "opacity": 0}, {"x": 0, "opacity": 1, "duration": 0.45, "ease": "power3.out"}, t0 + 0.15)
        C.fromto("#st-t", {"y": 30, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.55, "ease": "power3.out"}, t0 + 0.3)
        C.fromto("#st-chart", {"y": 40, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.5, "ease": "power3.out"}, t0 + 0.45)
        t_bars = t0 + 0.9
        for k, p in enumerate(st["parts"]):
            if p.get("bars"):
                t_bars = ptime("stats", k)
        for k in range(n):
            tb = t_bars + 0.18 * k
            C.fromto(f"#st-b{k}", {"scaleY": 0}, {"scaleY": 1, "duration": 0.6, "ease": "power3.out"}, tb)
            C.fromto(f"#st-v{k}", {"opacity": 0, "y": 20}, {"opacity": 1, "y": 0, "duration": 0.35, "ease": "back.out(2)"}, tb + 0.45)
            C.sound(tb + 0.45, "pop", 0.4)
        t_tot = t_bars + 0.18 * n + 0.6
        for k, p in enumerate(st["parts"]):
            if p.get("total"):
                t_tot = ptime("stats", k)
        C.fromto("#st-tot", {"scale": 0.8, "opacity": 0}, {"scale": 1, "opacity": 1, "duration": 0.45, "ease": "back.out(2)"}, t_tot)
        C.sound(t_tot, "chime", 0.5)
        ag_t = {}
        for k, p in enumerate(st["parts"]):
            for a in (p["agenda"] if isinstance(p.get("agenda"), list) else ([p["agenda"]] if p.get("agenda") is not None else [])):
                ag_t[a] = ptime("stats", k)
        t_ag0 = min(ag_t.values()) if ag_t else t_tot + 0.6
        C.fromto("#ag-h", {"opacity": 0}, {"opacity": 1, "duration": 0.4}, t_ag0 - 0.3)
        last = t_ag0
        for a in range(ns + 1):
            ta = ag_t.get(a, last + 0.35)
            C.fromto(f"#ag{a}", {"opacity": 0, "x": 60}, {"opacity": 1, "x": 0, "duration": 0.45, "ease": "power3.out"}, ta)
            C.sound(ta, "pop", 0.35)
            last = ta
        poses.append((T["stats"] + 0.3, "anlatim"))
        for k, p in enumerate(st["parts"]):
            if p.get("pose"):
                poses.append((ptime("stats", k), p["pose"]))

    # ---------------- BÖLÜMLER
    for k, (sec, s) in enumerate(zip(secs, S), 1):
        sid = f"s{k}"
        px = f"b{k}"
        end = (S[k]["start"] if k < ns else q["start"]) + XF
        kind = sec["kind"]
        marks = []
        if kind == "law":
            content, marks = law_html(px, sec)
            items = {}
        elif kind == "table":
            content, items = table_html(px, sec["table"])
        else:
            dh, items = diagram_html(px, sec["board"] | {"kind": kind} if "board" in sec else sec)
            content = f'<div class="diag" id="{px}-diag">{dh}</div>'
        callouts, call_html = [], ""
        for j, p in enumerate(sec["parts"]):
            if p.get("callout"):
                cid = f"{px}-co{len(callouts)}"
                call_html += callout_html(cid, p["callout"])
                callouts.append((cid, j, p["callout"]))
        inner = (f'<div class="sting" id="{px}-st"><div class="sn">BÖLÜM {k}</div><div class="stt">{esc(sec["title"])}</div></div>'
                 f'<div class="bhead" id="{px}-head"><div class="sol">BÖLÜM {k}</div><div class="ttl">{esc(sec["title"])}</div></div>'
                 f'<div class="mchip" id="{px}-m">⚖ Dayanak: {esc(sec["madde"])}</div>'
                 f'{content}{call_html}')
        scene(f"sc-{px}", s["start"], end, inner, track=2 if k % 2 else 1)
        t0 = s["start"]
        C.sound(t0 + 0.02, "whoosh", 0.7)
        C.fromto(f"#{px}-st", {"opacity": 0, "scale": 0.7}, {"opacity": 1, "scale": 1, "duration": 0.45, "ease": "back.out(1.7)"}, t0 + 0.05)
        C.sound(t0 + 0.2, "thud", 0.7)
        C.to(f"#{px}-st", {"opacity": 0, "y": -260, "scale": 0.6, "duration": 0.45, "ease": "power3.in"}, t0 + 1.0)
        C.fromto(f"#{px}-head", {"y": -30, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.5, "ease": "power3.out"}, t0 + 1.15)
        C.fromto(f"#{px}-m", {"x": -30, "opacity": 0}, {"x": 0, "opacity": 1, "duration": 0.45, "ease": "power2.out"}, t0 + 1.35)
        poses.append((t0 + 0.3, "anlatim"))
        if kind == "law":
            C.fromto(f"#{px}-law", {"y": 60, "opacity": 0, "rotation": -1}, {"y": 0, "opacity": 1, "rotation": 0, "duration": 0.6, "ease": "power3.out"}, t0 + 1.3)
        elif kind == "table":
            C.fromto(f"#{px}-head", {"opacity": 0}, {"opacity": 1, "duration": 0.01}, t0 + 1.15)  # (bhead; tablo başlığı aşağıda)
            C.fromto(f"#{px}-head", {"opacity": 0}, {"opacity": 1, "duration": 0.01}, t0 + 1.15)
        shown = set()
        if kind == "table":
            show_item(C, px, "head", items, shown, t0 + 1.35)
        last_call = None
        callmap = {j: (cid, co) for (cid, j, co) in callouts}
        for j, p in enumerate(sec["parts"]):
            tt = ptime(sid, j)
            if p.get("pose"):
                poses.append((tt, p["pose"]))
            ts = tt
            for itm in p.get("show", []):
                show_item(C, px, itm, items, shown, ts)
                ts += 0.14
            if p.get("mark") is not None:
                mk = p["mark"] if isinstance(p["mark"], list) else [p["mark"]]
                for mi in mk:
                    mid, nw = marks[mi]
                    step = min(0.12, 0.55 / max(1, nw))
                    for w in range(nw):
                        C.fromto(f"#{mid}w{w}", {"scaleX": 0}, {"scaleX": 1, "duration": max(0.18, 0.5 - step * (nw - 1)), "ease": "power2.inOut"}, tt + 0.2 + step * w)
                    C.sound(tt + 0.2, "pop", 0.3)
            if p.get("plain"):
                C.fromto(f"#{px}-plain", {"opacity": 0, "y": 30}, {"opacity": 1, "y": 0, "duration": 0.5, "ease": "back.out(1.6)"}, tt)
                C.sound(tt, "chime", 0.45)
            hl_t = tt + (0.75 + 0.14 * len(p.get("show", [])) if p.get("show") else 0.15)
            for hid in p.get("hl", []):
                C.fromto(f"#{px}-{hid}-g", {"opacity": 0, "scale": 0.94}, {"opacity": 1, "scale": 1.0, "duration": 0.35, "ease": "power2.out"}, hl_t)
                if items.get(hid, {}).get("type") != "row":
                    C.fromto(f"#{px}-{hid}", {"scale": 1}, {"scale": 1.06, "duration": 0.3, "ease": "power2.out", "yoyo": True, "repeat": 1}, hl_t)
            if j in callmap:
                cid, co = callmap[j]
                if last_call:
                    C.to(f"#{last_call}", {"opacity": 0, "y": 60, "duration": 0.3, "ease": "power2.in"}, tt - 0.25)
                show_callout(C, cid, co, tt, poses)
                last_call = cid
                # kutu sonraki parçada kapanır ve poz anlatıma döner (kapat:false ile açık kalır)
                if co.get("keep") is not True and j + 1 < len(sec["parts"]) and (j + 1) not in callmap:
                    tc = max(tt + 2.0, pend(sid, j) - 0.1)
                    C.to(f"#{cid}", {"opacity": 0, "y": 60, "duration": 0.3, "ease": "power2.in"}, tc)
                    poses.append((tc, "anlatim"))
                    last_call = None

    # ---------------- MİNİ TEST
    qs = spec["quiz"]
    pre = "qz"
    onermeli = bool(qs.get("statements"))
    width = 1262 - 130 - 52
    best = (26, 23)
    for stem_px, opt_px in [(40, 34), (38, 32), (36, 31), (34, 30), (32, 28), (30, 27), (29, 26), (28, 25), (27, 24), (26, 23)]:
        h = est_lines(qs["stem"], stem_px, width, 0.47) * stem_px * 1.3 + 14
        if onermeli:
            for stt in qs["statements"]:
                h += est_lines(stt, opt_px, width - 72, 0.46) * opt_px * 1.28 + 6
            h += 14 + 74
        else:
            for o in qs["options"]:
                h += max(56, est_lines(o, opt_px, width - 150, 0.46) * opt_px * 1.28 + 12) + 10
        if h <= 640:
            best = (stem_px, opt_px)
            break
    stem_px, opt_px = best
    mk_list = [p["mark"] for p in qs["read"] if p.get("mark")]
    stem_html, qmarks = mark_html(qs["stem"], mk_list, f"{pre}-mk")
    qmark_parts = [j for j, p in enumerate(qs["read"]) if p.get("mark")]
    body = f'<div class="stem" id="{pre}-stem" style="font-size:{stem_px}px">{stem_html}</div>'
    ck_svg = '<svg viewBox="0 0 40 40" width="{0}" height="{0}"><path d="M8 21 L17 29 L32 11" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    if onermeli:
        romans = ["I.", "II.", "III.", "IV.", "V."]
        body += '<div class="stmts">' + "".join(
            f'<div class="stmt" id="{pre}-s{k}" style="font-size:{opt_px}px"><span class="rn">{romans[k]}</span><span>{esc(stt)}</span></div>'
            for k, stt in enumerate(qs["statements"])) + "</div>"
        body += f'<div class="optgrid" id="{pre}-og">'
        for k, o in enumerate(qs["options"]):
            body += (f'<div class="opt" id="{pre}-o{k}"><div class="hl" id="{pre}-o{k}-hl"></div>'
                     f'<div class="lt"><div class="ltf" id="{pre}-o{k}-ltf"></div><span>{LETTERS[k]}</span></div>'
                     f'<div class="tx" style="font-size:{min(opt_px, 26)}px">{esc(o)}</div>'
                     + ("" if LETTERS[k] == qs["answer"] else f'<div class="strike" id="{pre}-o{k}-st"></div>')
                     + f'<div class="ck" id="{pre}-o{k}-ck">{ck_svg.format(28)}</div></div>')
        body += "</div>"
    else:
        body += '<div class="opts">'
        for k, o in enumerate(qs["options"]):
            body += (f'<div class="opt" id="{pre}-o{k}"><div class="hl" id="{pre}-o{k}-hl"></div>'
                     f'<div class="lt"><div class="ltf" id="{pre}-o{k}-ltf"></div><span>{LETTERS[k]}</span></div>'
                     f'<div class="tx" style="font-size:{opt_px}px">{esc(o)}</div>'
                     + ("" if LETTERS[k] == qs["answer"] else f'<div class="strike" id="{pre}-o{k}-st"></div>')
                     + f'<div class="ck" id="{pre}-o{k}-ck">{ck_svg.format(34)}</div></div>')
        body += "</div>"
    ans = LETTERS.index(qs["answer"])
    card = (f'<div class="card" id="{pre}-card"><div class="rules"></div><div class="margin"></div>'
            f'<div class="chead"><div class="qchip">MİNİ TEST</div><div class="tchip">{esc(qs["chip"])}</div><div class="src">{esc(qs.get("src", "GMY tarzı · özgün soru"))}</div></div>'
            f'<div class="cbody" id="{pre}-body">{body}</div>'
            f'<div class="stampa" id="{pre}-stamp">DOĞRU CEVAP: {qs["answer"]}</div></div>')
    timer = (f'<div class="timer" id="{pre}-timer"><div class="tbg"></div>'
             f'<svg viewBox="0 0 210 210"><circle cx="105" cy="105" r="88" fill="none" stroke="rgba(159,176,224,.25)" stroke-width="14"/>'
             f'<circle id="{pre}-ring" cx="105" cy="105" r="88" fill="none" stroke="#F2B233" stroke-width="14" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="0" transform="rotate(-90 105 105)"/></svg>'
             + "".join(f'<div class="tn" id="{pre}-tn{n_}">{n_}</div>' for n_ in range(5, 0, -1))
             + '<div class="tl">DÜŞÜN</div></div>')
    qbig = f'<div class="qbig" id="{pre}-big"><b>MİNİ TEST</b></div>'
    scene("sc-qz", q["start"], q["board"] + XF, qbig + card + timer)
    t0 = q["start"]
    C.sound(t0 + 0.02, "whoosh", 0.7)
    C.fromto(f"#{pre}-big", {"scale": 1.8, "opacity": 0}, {"scale": 1, "opacity": 1, "duration": 0.45, "ease": "back.out(1.7)"}, t0 + 0.05)
    C.sound(t0 + 0.2, "thud", 0.8)
    C.to(f"#{pre}-big", {"scale": 0.6, "opacity": 0, "y": -300, "duration": 0.45, "ease": "power3.in"}, t0 + 0.95)
    C.fromto(f"#{pre}-card", {"y": 120, "opacity": 0, "rotation": -1.5}, {"y": 0, "opacity": 1, "rotation": 0, "duration": 0.7, "ease": "power3.out"}, t0 + 1.05)
    opt_shown = set()
    for k, p in enumerate(qs["read"]):
        tt = ptime("quiz_read", k)
        if k == 0:
            C.fromto(f"#{pre}-stem", {"opacity": 0, "y": 16}, {"opacity": 1, "y": 0, "duration": 0.5, "ease": "power2.out"}, min(tt, q["read"]) - 0.1)
        if p.get("show") is not None:
            show = p["show"] if isinstance(p["show"], list) else [p["show"]]
            for si, sv in enumerate(show):
                if sv.startswith("S"):
                    C.fromto(f"#{pre}-s{int(sv[1:])}", {"opacity": 0, "x": -30}, {"opacity": 1, "x": 0, "duration": 0.45, "ease": "power3.out"}, tt - 0.05 + si * 0.08)
                else:
                    oi = LETTERS.index(sv)
                    opt_shown.add(oi)
                    C.fromto(f"#{pre}-o{oi}", {"opacity": 0, "x": -40}, {"opacity": 1, "x": 0, "duration": 0.45, "ease": "power3.out"}, tt - 0.05 + si * 0.08)
                    C.sound(tt - 0.05 + si * 0.08, "pop", 0.35)
    for (mid, nw), j in zip(qmarks, qmark_parts):
        tt = ptime("quiz_read", j)
        step = min(0.12, 0.5 / max(1, nw))
        for w in range(nw):
            C.fromto(f"#{mid}w{w}", {"scaleX": 0}, {"scaleX": 1, "duration": max(0.18, 0.5 - step * (nw - 1)), "ease": "power2.inOut"}, tt + 0.15 + step * w)
    for oi in range(5):
        if oi not in opt_shown:
            C.fromto(f"#{pre}-o{oi}", {"opacity": 0, "x": -40}, {"opacity": 1, "x": 0, "duration": 0.45, "ease": "power3.out"}, q["read"] + 0.3 + 0.08 * oi)
    poses.append((q["start"] + 0.2, "anlatim"))
    poses.append((q["think"], "dusunme"))
    C.fromto(f"#{pre}-timer", {"scale": 0.4, "opacity": 0}, {"scale": 1, "opacity": 1, "duration": 0.5, "ease": "back.out(1.8)"}, q["think"] + 0.1)
    C.sound(q["think"] + 0.1, "pop", 0.6)
    C.fromto(f"#{pre}-ring", {"strokeDashoffset": 0}, {"strokeDashoffset": 1, "duration": 5.0, "ease": "none"}, q["cd"])
    for n_ in range(5):
        tn = q["cd"] + n_
        C.set(f"#{pre}-tn{5 - n_}", {"opacity": 1}, tn)
        C.fromto(f"#{pre}-tn{5 - n_}", {"scale": 1.35}, {"scale": 1, "duration": 0.35, "ease": "power3.out"}, tn)
        C.set(f"#{pre}-tn{5 - n_}", {"opacity": 0}, tn + 0.999)
        C.sound(tn, "tick" if n_ % 2 == 0 else "tock", 0.8)
    C.to(f"#{pre}-timer", {"scale": 0.5, "opacity": 0, "duration": 0.3, "ease": "power2.in"}, q["cd_end"])
    tr = q["exp"] + ex["pt"][0]
    poses.append((tr, "onay"))
    for oi in range(5):
        if oi == ans:
            continue
        C.fromto(f"#{pre}-o{oi}", {"opacity": 1}, {"opacity": 0.38, "duration": 0.35, "ease": "power1.out"}, tr + 0.05)
        C.fromto(f"#{pre}-o{oi}-st", {"scaleX": 0}, {"scaleX": 1, "duration": 0.3, "ease": "power2.out"}, tr + 0.05 + 0.06 * oi)
    C.fromto(f"#{pre}-o{ans}-hl", {"scaleX": 0, "opacity": 1}, {"scaleX": 1, "opacity": 1, "duration": 0.45, "ease": "power3.out"}, tr + 0.1)
    C.fromto(f"#{pre}-o{ans}-ltf", {"opacity": 0}, {"opacity": 1, "duration": 0.25}, tr + 0.15)
    C.fromto(f"#{pre}-o{ans}-ck", {"scale": 0, "opacity": 0}, {"scale": 1, "opacity": 1, "duration": 0.45, "ease": "back.out(2.4)"}, tr + 0.3)
    C.fromto(f"#{pre}-o{ans}", {"scale": 1}, {"scale": 1.03, "duration": 0.3, "ease": "power2.out", "yoyo": True, "repeat": 1}, tr + 0.3)
    C.fromto(f"#{pre}-stamp", {"scale": 2.2, "opacity": 0, "rotation": -18}, {"scale": 1, "opacity": 1, "rotation": -6, "duration": 0.4, "ease": "power4.in"}, tr + 0.45)
    C.sound(tr + 0.05, "ding", 0.9)
    C.sound(tr + 0.85, "thud", 0.6)
    # çözüm tahtası
    b = qs["board"]
    x_start, x_end = q["board"], T["sum"] + XF
    dh, ditems = diagram_html(f"{pre}x", b)
    xcalls, xcall_html = [], ""
    for j, p in enumerate(qs["explain"]):
        if p.get("callout"):
            cid = f"{pre}x-co{len(xcalls)}"
            xcall_html += callout_html(cid, p["callout"])
            xcalls.append((cid, j, p["callout"]))
    board_inner = (
        f'<div class="bhead" id="{pre}x-head"><div class="sol">ÇÖZÜM</div><div class="ttl">{esc(b["title"])}</div>'
        f'<div class="ans"><svg viewBox="0 0 40 40" width="30" height="30"><path d="M8 21 L17 29 L32 11" fill="none" stroke="#BFF2DA" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>Cevap {qs["answer"]}</div></div>'
        f'<div class="mchip" id="{pre}x-m">⚖ Dayanak: {esc(b["madde"])}</div>'
        f'<div class="diag" id="{pre}x-diag">{dh}</div>{xcall_html}')
    scene("sc-qzx", x_start, x_end, board_inner, track=2)
    C.sound(x_start, "whoosh", 0.55)
    C.fromto(f"#{pre}x-head", {"y": -30, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.5, "ease": "power3.out"}, x_start + 0.15)
    C.fromto(f"#{pre}x-m", {"x": -30, "opacity": 0}, {"x": 0, "opacity": 1, "duration": 0.45, "ease": "power2.out"}, x_start + 0.4)
    shown = set()
    last_call = None
    for j, p in enumerate(qs["explain"]):
        if j == 0:
            continue
        tt = ptime("quiz_exp", j)
        poses.append((tt, p["pose"] if p.get("pose") else "anlatim") if (p.get("pose") or j == 1) else (tt, None))
        for itm in p.get("show", []):
            animate_show(C, f"{pre}x", itm, ditems, shown, tt)
            tt += 0.12
        hl_t = ptime("quiz_exp", j) + (0.75 + 0.12 * len(p.get("show", [])) if p.get("show") else 0.1)
        for hid in p.get("hl", []):
            C.fromto(f"#{pre}x-{hid}-g", {"opacity": 0, "scale": 0.92}, {"opacity": 1, "scale": 1.0, "duration": 0.35, "ease": "power2.out"}, hl_t)
            C.fromto(f"#{pre}x-{hid}", {"scale": 1}, {"scale": 1.06, "duration": 0.3, "ease": "power2.out", "yoyo": True, "repeat": 1}, hl_t)
    for (cid, j, co) in xcalls:
        tt = ptime("quiz_exp", j)
        if last_call:
            C.to(f"#{last_call}", {"opacity": 0, "y": 60, "duration": 0.3, "ease": "power2.in"}, tt - 0.25)
        show_callout(C, cid, co, tt, poses)
        last_call = cid
    poses = [pp for pp in poses if pp[1]]

    # ---------------- ÖZET
    sm = spec["summary"]
    cards = ""
    n_items = len(sm["items"])
    ch_ = 168 if n_items <= 3 else 132
    gap_ = 16 if n_items <= 3 else 12
    for k, it in enumerate(sm["items"]):
        cards += (f'<div class="mcard" id="mc{k}" style="top:{250 + k * (ch_ + gap_)}px;height:{ch_}px"><div class="mn">{k + 1}</div>'
                  f'<div><b>{esc(it["title"])}</b><p>{esc(it["text"])}</p></div></div>')
    badge = f'<div class="sbadge" id="sbadge">{esc(sm["badge"])}</div>' if sm.get("badge") else ""
    scene("sc-sum", T["sum"], T["out"] + XF, f'<div class="sumtitle" id="stitle">AKILDA <em>KALSIN</em> · Hafıza Kartı</div>{cards}{badge}')
    C.sound(T["sum"], "whoosh", 0.6)
    C.fromto("#stitle", {"y": -40, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.6, "ease": "power3.out"}, T["sum"] + 0.15)
    poses.append((T["sum"] + 0.3, "onemli"))
    for k, p in enumerate(sm["parts"]):
        tt = ptime("summary", k)
        if p.get("item") is not None:
            C.fromto(f"#mc{p['item']}", {"x": -80, "opacity": 0, "rotationX": -50}, {"x": 0, "opacity": 1, "rotationX": 0, "duration": 0.6, "ease": "power3.out"}, tt - 0.1)
            C.sound(tt - 0.1, "pop", 0.5)
        if p.get("badge") and badge:
            C.fromto("#sbadge", {"y": 30, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.5, "ease": "back.out(1.6)"}, tt)
            poses.append((tt, "onay"))
        if p.get("pose"):
            poses.append((tt, p["pose"]))

    # ---------------- KAPANIŞ
    ou = spec["outro"]
    scene("sc-out", T["out"], TOTAL,
          f'<div class="out-k" id="ok">GÜMRÜK KOÇU · GMY KONU ANLATIMI</div>'
          f'<div class="out-t" id="ot">{esc(ou["title"])}</div>'
          f'<div class="out-n" id="on"><small>{esc(ou.get("next_label", "SIRADAKİ DERS"))}</small><b>{esc(ou["next"])}</b></div>'
          f'<div class="half" id="ohalf" style="left:1150px;top:150px"><div class="av-talk" id="ohalf-talk"><img src="assets/avatar/yarim_boy_kapanis.png" alt=""></div></div>')
    C.sound(T["out"], "whoosh", 0.6)
    C.fromto("#ok", {"x": -60, "opacity": 0}, {"x": 0, "opacity": 1, "duration": 0.5, "ease": "power3.out"}, T["out"] + 0.2)
    C.fromto("#ot", {"y": 60, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.7, "ease": "power4.out"}, T["out"] + 0.35)
    C.fromto("#on", {"scale": 0.8, "opacity": 0}, {"scale": 1, "opacity": 1, "duration": 0.5, "ease": "back.out(1.8)"}, T["out"] + 0.9)
    C.fromto("#ohalf", {"x": 520, "opacity": 0}, {"x": 0, "opacity": 1, "duration": 0.8, "ease": "back.out(1.2)"}, T["out"] + 0.3)
    C.sound(T["out"] + 0.9, "chime", 0.6)

    # ---------------- ÜST BAR (bölüm ilerlemesi)
    labels = [f"B{k}" for k in range(1, ns + 1)] + ["T"]
    starts = [s["start"] for s in S] + [q["start"]]
    dones = [s["end"] - 0.6 for s in S] + [q["exp"] + 0.4]
    pills = "".join(f'<div class="pill" id="pl{k}"><div class="pf" id="pl{k}-f"></div><div class="pd" id="pl{k}-d"></div><span>{lb}</span></div>' for k, lb in enumerate(labels))
    tb0 = first_main
    topbar = (f'<div id="topbar" class="clip" data-start="{r3(tb0)}" data-duration="{r3(T["out"] + XF - tb0)}" data-track-index="5">'
              f'<div class="bar" id="tb-in"><div class="brand"><div class="badge">GK</div><b>GÜMRÜK KOÇU</b><i>KONU ANLATIMI</i></div>'
              f'<div class="vinfo"><div class="vt">DERS {vnum}/5 · {esc(spec["short"])}</div>{pills}</div></div></div>')
    C.fromto("#tb-in", {"y": -100, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.5, "ease": "power3.out"}, tb0 + 0.1)
    C.to("#tb-in", {"opacity": 0, "duration": XF}, T["out"])
    for k, (st_, dn) in enumerate(zip(starts, dones)):
        C.fromto(f"#pl{k}-f", {"opacity": 0}, {"opacity": 1, "duration": 0.3}, st_ + 0.2)
        C.add(f'tl.set("#pl{k} span",{{"color":"#0A1438"}},{r3(st_ + 0.2)});')
        C.to(f"#pl{k}-d", {"opacity": 1, "duration": 0.3}, dn)
        C.add(f'tl.set("#pl{k} span",{{"color":"#ffffff"}},{r3(dn)});')

    # ---------------- AVATAR
    av_imgs = "".join(f'<img id="av-{p}" src="assets/avatar/{p}.png" alt="">' for p in POSES)
    avatar = (f'<div id="avatar" class="clip" data-start="0" data-duration="{r3(TOTAL)}" data-track-index="6">'
              f'<div class="av-move" id="av-move"><div class="av-shadow"></div><div class="av-pop" id="av-pop"><div class="av-idle" id="av-idle"><div class="av-talk" id="av-talk">{av_imgs}</div></div></div></div></div>')
    C.set("#av-move", {"opacity": 0, "x": 500}, 0)
    C.to("#av-move", {"opacity": 1, "x": 0, "duration": 0.8, "ease": "back.out(1.3)"}, first_main + 0.5)
    C.to("#av-move", {"opacity": 0, "x": 500, "duration": 0.6, "ease": "power2.in"}, T["out"] - 0.1)
    poses.sort()
    C.set("#av-anlatim", {"opacity": 1}, 0)
    cur, last_t = "anlatim", -9
    for tt, p in poses:
        if p == cur:
            continue
        if tt - last_t < 0.5:
            tt = last_t + 0.5
        C.to(f"#av-{cur}", {"opacity": 0, "duration": 0.14, "ease": "none"}, tt)
        C.to(f"#av-{p}", {"opacity": 1, "duration": 0.14, "ease": "none"}, tt)
        C.fromto("#av-pop", {"scale": 0.96, "y": 10}, {"scale": 1, "y": 0, "duration": 0.35, "ease": "back.out(2.2)"}, tt)
        cur, last_t = p, tt
    rep = max(0, int(math.floor(TOTAL / 3.2)) - 1)
    C.add(f'tl.fromTo("#av-idle",{{"scaleY":1}},{{"scaleY":1.012,"duration":1.6,"ease":"sine.inOut","yoyo":true,"repeat":{rep}}},0);')

    # ---------------- SES + konuşma zarfı
    mix, env = mix_audio(A, placements, C.sfx, TOTAL, adir)
    write_wav(os.path.join(proj, "assets", "mix.wav"), mix)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(proj, "assets", "mix.wav"), "-c:a", "libmp3lame", "-b:a", "192k",
                    os.path.join(proj, "assets", "mix.mp3")], check=True)
    os.remove(os.path.join(proj, "assets", "mix.wav"))

    def talk_keys(sel, t_from, t_to):
        prev = None
        for n_ in range(int(t_from * FPS_ENV), min(len(env) - 1, int(t_to * FPS_ENV))):
            e = float(env[n_])
            key = (round(1 + 0.022 * e, 4), round(-7 * e, 2), round(0.9 * e * math.sin(n_ * 0.9), 3))
            if prev == key:
                continue
            prev = key
            C.add(f'tl.to("{sel}",{{scaleY:{key[0]},y:{key[1]},rotation:{key[2]},duration:{r3(0.97 / FPS_ENV)},ease:"sine.inOut"}},{r3(n_ / FPS_ENV)});')
    talk_keys("#av-talk", first_main, T["out"] + 0.5)
    talk_keys("#ihalf-talk", 0, intro_end)
    talk_keys("#ohalf-talk", T["out"], TOTAL)

    # ---------------- ALTYAZI
    caps_html, ci = [], 0
    for (st_, sid) in placements:
        for (c0, c1, txt) in caption_chunks(A[sid]):
            caps_html.append(f'<div class="cap" id="cap{ci}"><span>{esc(txt)}</span></div>')
            C.set(f"#cap{ci}", {"opacity": 1}, st_ + c0)
            C.set(f"#cap{ci}", {"opacity": 0}, st_ + c1)
            ci += 1
    caps = f'<div id="caps" class="clip" data-start="0" data-duration="{r3(TOTAL)}" data-track-index="7">' + "".join(caps_html) + "</div>"

    # ---------------- ARKA PLAN
    bg = (f'<div id="bg" class="clip" data-start="0" data-duration="{r3(TOTAL)}" data-track-index="0">'
          f'<div class="bgfill"></div><div class="grid" id="bg-grid"></div>'
          f'<div class="glow" id="bg-g1" style="left:-200px;top:-260px"></div><div class="glow" id="bg-g2" style="left:1250px;top:520px"></div>'
          f'<div class="ghost" id="bg-ghost" aria-hidden="true" data-t="GÜMRÜK · KOÇU · DERS"></div></div>')
    rep_g = max(0, int(math.floor(TOTAL / 12)) - 1)
    C.add(f'tl.fromTo("#bg-grid",{{x:0,y:0}},{{x:80,y:80,duration:{r3(TOTAL)},ease:"none"}},0);')
    C.add(f'tl.fromTo("#bg-g1",{{scale:1,opacity:.8}},{{scale:1.18,opacity:1,duration:6,ease:"sine.inOut",yoyo:true,repeat:{rep_g}}},0);')
    C.add(f'tl.fromTo("#bg-g2",{{scale:1.1,opacity:1}},{{scale:.9,opacity:.7,duration:6,ease:"sine.inOut",yoyo:true,repeat:{rep_g}}},0);')
    C.add(f'tl.fromTo("#bg-ghost",{{x:0}},{{x:-900,duration:{r3(TOTAL)},ease:"none"}},0);')
    audio = f'<audio id="mix" src="assets/mix.mp3" data-start="0" data-duration="{r3(TOTAL)}" data-track-index="10" data-volume="1"></audio>'

    doc = f"""<!doctype html>
<html lang="tr">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080" />
<title>GMY Konu Anlatımı · Ders {vnum} · {esc(spec['short'])}</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>{B.CSS}{DCSS}</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-width="1920" data-height="1080" data-duration="{r3(TOTAL)}">
{bg}
{''.join(scenes_html)}
{topbar}
{avatar}
{caps}
{audio}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(C.emit())}
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""
    with open(os.path.join(proj, "index.html"), "w", encoding="utf-8") as f:
        f.write(doc)
    for sub in ["fonts", "avatar"]:
        dst = os.path.join(proj, "assets", sub)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(os.path.join(HERE, "shared", sub), dst)
    info = {"total": TOTAL, "stats": r3(T.get("stats", 0)), "sections": [{kk: r3(v) for kk, v in s.items()} for s in S],
            "quiz": {kk: r3(v) for kk, v in q.items()}, "summary": r3(T["sum"]), "outro": r3(T["out"])}
    with open(os.path.join(proj, "timing.json"), "w") as f:
        json.dump(info, f, indent=1)
    print(f"ders {vid}: {TOTAL:.1f}s, {len(C.js)} tween satırı, {len(caps_html)} altyazı -> {proj}")


def write_brief(proj, spec):
    p = os.path.join(proj, "BRIEF.md")
    if os.path.exists(p):
        return
    secs = "\n".join(f"- Bölüm {k}: {s['title']} ({s['madde']})" for k, s in enumerate(spec["sections"], 1))
    with open(p, "w", encoding="utf-8") as f:
        f.write(f"""---
workflow: general-video
flow: automation
storyboard: no
message: "GMY Konu Anlatımı {spec['no']}/5 — {spec['title']}"
destination: youtube
aspect: 1920x1080
language: tr
audience: "Gümrük Müşavir Yardımcılığı (GMY) sınavına hazırlanan adaylar"
voice: "ElevenLabs eleven_v4 · Cem (D1xRw7f8ZHedI7xJgfvz)"
---

## Intent

Gümrük Koçu ders kanalı için bir konunun tek bir parçasını anlatan, şemalı ve altyazılı konu anlatımı videosu.
Konu parçası: {spec['title']}. GMY çıkmış soruları incelenerek seçildi; sonunda bir mini test var.

## Bölümler

{secs}

## Notes

- Kaynak üretici: ../_uretici (spec/ders{int(spec['no']):02d}.json → ders.py).
""")


if __name__ == "__main__":
    cmd, vid = sys.argv[1], sys.argv[2]
    if cmd == "plan":
        cmd_plan(vid)
    elif cmd == "words":
        cmd_words(vid, sys.argv[3:] or None)
    elif cmd == "build":
        build_lesson(vid)
    else:
        raise SystemExit("komut: plan|words|build")
