#!/usr/bin/env python3
"""GMY Soru Kampı — HyperFrames video üreticisi.

Kullanım:
  python3 build.py plan  01   -> audio/v01/segments.json  (ElevenLabs'e gidecek anlatım metinleri)
  python3 build.py words 01   -> audio/v01/<seg>.words.json (yerel Whisper kelime zamanları)
  python3 build.py build 01   -> ../gmy-kamp-01/ (index.html + assets/ + ses miksajı)

Her video spec/videoNN.json dosyasından üretilir. Anlatım, Cem sesiyle
(ElevenLabs eleven_v4) segment segment üretilip audio/vNN/<seg>.mp3 olarak indirilir.
"""
import difflib
import html
import json
import math
import os
import re
import shutil
import subprocess
import sys
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SR = 44100
FPS_ENV = 12.5  # avatar konuşma zarfı örnekleme hızı

POSES = ["anlatim", "dusunme", "onemli", "onay", "dur", "saskin"]
CALLOUT_POSE = {"tuzak": "saskin", "dikkat": "dur", "uyari": "dur", "onemli": "onemli"}
CALLOUT_LABEL = {"tuzak": "TUZAK", "dikkat": "DİKKAT", "uyari": "UYARI", "onemli": "ÖNEMLİ"}
CALLOUT_SFX = {"tuzak": "trap", "dikkat": "warn", "uyari": "warn", "onemli": "chime"}
CALLOUT_ICON = {
    # basit, satır içi SVG ikonlar
    "tuzak": '<svg viewBox="0 0 64 64"><path d="M6 44 L58 44" stroke="currentColor" stroke-width="5" stroke-linecap="round"/><path d="M10 44 L16 26 L22 40 L28 22 L34 40 L40 22 L46 40 L52 26 L56 44" fill="none" stroke="currentColor" stroke-width="4.5" stroke-linejoin="round"/><circle cx="32" cy="52" r="4" fill="currentColor"/></svg>',
    "dikkat": '<svg viewBox="0 0 64 64"><path d="M4 32 Q32 8 60 32 Q32 56 4 32 Z" fill="none" stroke="currentColor" stroke-width="5" stroke-linejoin="round"/><circle cx="32" cy="32" r="9" fill="currentColor"/></svg>',
    "uyari": '<svg viewBox="0 0 64 64"><path d="M32 6 L60 56 L4 56 Z" fill="none" stroke="currentColor" stroke-width="5" stroke-linejoin="round"/><path d="M32 24 L32 40" stroke="currentColor" stroke-width="6" stroke-linecap="round"/><circle cx="32" cy="48" r="3.6" fill="currentColor"/></svg>',
    "onemli": '<svg viewBox="0 0 64 64"><path d="M32 4 L39.5 23 L60 24.5 L44 37.5 L49 58 L32 47 L15 58 L20 37.5 L4 24.5 L24.5 23 Z" fill="currentColor"/></svg>',
}


# ----------------------------------------------------------------------------
# yardımcılar
# ----------------------------------------------------------------------------
def esc(s):
    return html.escape(str(s), quote=True)


def strip_tags(s):
    return re.sub(r"\[[^\]]*\]", "", s).replace("  ", " ").strip()


def tr_lower(s):
    return s.replace("İ", "i").replace("I", "ı").lower()


def norm_tok(w):
    w = tr_lower(w)
    w = re.sub(r"(?<=\d)[.,](?=\d)", "", w)
    w = re.sub(r"[^0-9a-zçğıöşüâîû%]", "", w)
    return w


def tokens(text):
    out = []
    for w in strip_tags(text).split():
        n = norm_tok(w)
        if n:
            out.append(n)
    return out


def ffprobe_dur(p):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", p],
        capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def read_audio(p):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype=np.float32).reshape(-1, 2).astype(np.float64)


def r3(x):
    return round(float(x), 3)


# ----------------------------------------------------------------------------
# segment planı
# ----------------------------------------------------------------------------
THINK_LINES = [
    "Videoyu durdurabilirsin. Süren başladı… beş saniye!",
    "Şimdi sıra sende. Beş saniye düşün!",
    "Kalemi al, işaretle. Beş saniye!",
]


def segments(spec):
    """Videonun anlatım segmentleri: [{id, parts:[{say,...}]}]"""
    segs = [{"id": "intro", "parts": spec["intro"]["parts"]}]
    for i, q in enumerate(spec["questions"], 1):
        segs.append({"id": f"q{i}_read", "parts": q["read"]})
        segs.append({"id": f"q{i}_think", "parts": [{"say": q.get("think", THINK_LINES[(i - 1) % 3])}]})
        segs.append({"id": f"q{i}_exp", "parts": q["explain"]})
    segs.append({"id": "summary", "parts": spec["summary"]["parts"]})
    segs.append({"id": "outro", "parts": spec["outro"]["parts"]})
    for s in segs:
        s["text"] = " ".join(p["say"].strip() for p in s["parts"])
    return segs


def load_spec(vid):
    with open(os.path.join(HERE, "spec", f"video{vid}.json"), encoding="utf-8") as f:
        return json.load(f)


def cmd_plan(vid):
    spec = load_spec(vid)
    segs = segments(spec)
    d = os.path.join(HERE, "audio", f"v{vid}")
    os.makedirs(d, exist_ok=True)
    out = [{"id": s["id"], "text": s["text"], "chars": len(s["text"])} for s in segs]
    with open(os.path.join(d, "segments.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    tot = sum(o["chars"] for o in out)
    print(f"video {vid}: {len(out)} segment, {tot} karakter")
    for o in out:
        print(f"  {o['id']:10s} {o['chars']:5d}")


def cmd_words(vid, only=None):
    d = os.path.join(HERE, "audio", f"v{vid}")
    with open(os.path.join(d, "segments.json"), encoding="utf-8") as f:
        segs = json.load(f)
    for s in segs:
        if only and s["id"] not in only:
            continue
        mp3 = os.path.join(d, s["id"] + ".mp3")
        wj = os.path.join(d, s["id"] + ".words.json")
        if os.path.exists(wj):
            continue
        if not os.path.exists(mp3):
            print("ses yok, atlandı:", s["id"])
            continue
        tmp = os.path.join(d, "_tr_" + s["id"])
        os.makedirs(tmp, exist_ok=True)
        subprocess.run(["npx", "hyperframes", "transcribe", mp3, "--model", "small", "--language", "tr",
                        "--json", "-d", tmp, "--timeout", "3600000"], capture_output=True, text=True)
        tj = os.path.join(tmp, "transcript.json")
        with open(tj, encoding="utf-8") as f:
            tr = json.load(f)
        words = tr.get("words", tr) if isinstance(tr, dict) else tr
        with open(wj, "w", encoding="utf-8") as f:
            json.dump(words, f, ensure_ascii=False)
        shutil.rmtree(tmp, ignore_errors=True)
        print("words", s["id"], len(words))


# ----------------------------------------------------------------------------
# hizalama: script kelimesi -> zaman
# ----------------------------------------------------------------------------
class Aligner:
    def __init__(self, text, words, dur, speech):
        self.tok = tokens(text)
        self.dur = dur
        self.s0, self.s1 = speech
        wt = [norm_tok(w["text"]) for w in words]
        wt_f = [(t, w) for t, w in zip(wt, words) if t]
        self.wtok = [t for t, _ in wt_f]
        self.wobj = [w for _, w in wt_f]
        sm = difflib.SequenceMatcher(a=self.tok, b=self.wtok, autojunk=False)
        self.anchors = []
        for a, b, n in sm.get_matching_blocks():
            for k in range(n):
                self.anchors.append((a + k, float(self.wobj[b + k]["start"])))
        self.anchors.sort()
        self.match_ratio = len(self.anchors) / max(1, len(self.tok))

    def t(self, idx):
        if not self.tok:
            return self.s0
        n = len(self.tok)
        if not self.anchors:
            return self.s0 + (self.s1 - self.s0) * idx / n
        ai = [a for a, _ in self.anchors]
        import bisect
        j = bisect.bisect_left(ai, idx)
        if j < len(ai) and ai[j] == idx:
            return self.anchors[j][1]
        if j == 0:
            a1, t1 = self.anchors[0]
            per = (self.s1 - self.s0) / n
            return max(self.s0, t1 - (a1 - idx) * per)
        if j >= len(ai):
            a0, t0 = self.anchors[-1]
            per = (self.s1 - t0) / max(1, n - a0)
            return min(self.s1, t0 + (idx - a0) * per)
        a0, t0 = self.anchors[j - 1]
        a1, t1 = self.anchors[j]
        return t0 + (t1 - t0) * (idx - a0) / (a1 - a0)


def speech_bounds(x):
    mono = np.abs(x).mean(1)
    win = int(0.02 * SR)
    n = len(mono) // win
    if n == 0:
        return 0.0, len(mono) / SR
    rms = np.sqrt((mono[: n * win].reshape(n, win) ** 2).mean(1))
    thr = max(1e-4, rms.max() * 0.04)
    idx = np.where(rms > thr)[0]
    if len(idx) == 0:
        return 0.0, len(mono) / SR
    return idx[0] * win / SR, (idx[-1] + 1) * win / SR


# ----------------------------------------------------------------------------
# metin sığdırma tahminleri
# ----------------------------------------------------------------------------
def est_lines(text, px, width, k=0.5):
    cpl = max(8, int(width / (px * k)))
    words = text.split()
    lines, cur = 1, 0
    for w in words:
        L = len(w) + (1 if cur else 0)
        if cur + L > cpl:
            lines += 1
            cur = len(w)
        else:
            cur += L
    return lines


# ----------------------------------------------------------------------------
# HTML parçaları
# ----------------------------------------------------------------------------
CSS = r"""
@font-face{font-family:"GK Sans";src:url("assets/fonts/Montserrat.ttf") format("truetype");font-weight:100 900;font-style:normal}
@font-face{font-family:"GK Serif";src:url("assets/fonts/SourceSerif4.ttf") format("truetype");font-weight:200 900;font-style:normal}
@font-face{font-family:"GK Mono";src:url("assets/fonts/JetBrainsMono.ttf") format("truetype");font-weight:100 800;font-style:normal}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1920px;height:1080px;overflow:hidden;background:#0A1438}
:root{--navy:#0A1438;--navy2:#13235E;--navy3:#1C3180;--gold:#F2B233;--gold2:#FFD27A;--paper:#F6F1E4;--ink:#16224C;
--green:#18A56B;--red:#D9443F;--orange:#FF7A1A;--cream:#F3EEE0;--muted:#9FB0E0}
#root{position:relative;width:100%;height:100%;overflow:hidden;font-family:"GK Sans",sans-serif;color:var(--cream)}
.scene{position:absolute;inset:0;overflow:hidden}
.inner{position:absolute;inset:0}
.layer{position:absolute;inset:0;pointer-events:none}
/* arka plan */
#bg .bgfill{position:absolute;inset:0;background:radial-gradient(1200px 800px at 18% 12%,#1B2E78 0%,rgba(27,46,120,0) 70%),radial-gradient(1000px 700px at 92% 96%,#22307A 0%,rgba(34,48,122,0) 70%),#0A1438}
#bg .grid{position:absolute;left:-80px;top:-80px;width:2080px;height:1240px;opacity:.16;
background-image:linear-gradient(rgba(159,176,224,.55) 2px,transparent 2px),linear-gradient(90deg,rgba(159,176,224,.55) 2px,transparent 2px);background-size:80px 80px}
#bg .glow{position:absolute;width:900px;height:900px;border-radius:50%;background:radial-gradient(circle,rgba(242,178,51,.22) 0%,rgba(242,178,51,0) 65%)}
#bg .ghost{position:absolute;left:40px;bottom:-60px;font-weight:900;font-size:300px;letter-spacing:-.04em;color:rgba(159,176,224,.07);white-space:nowrap}
#bg .ghost::before{content:attr(data-t)}
#bg .stamp{position:absolute;right:560px;top:150px;width:260px;height:260px;border-radius:50%;border:6px solid rgba(242,178,51,.14);display:flex;align-items:center;justify-content:center}
#bg .stamp span{font-family:"GK Mono";font-weight:700;font-size:26px;color:rgba(242,178,51,.22);letter-spacing:.2em;text-align:center;line-height:1.3}
/* üst bar */
#topbar .bar{position:absolute;left:0;top:0;width:1920px;height:96px;display:flex;align-items:center;justify-content:space-between;padding:0 56px;background:linear-gradient(180deg,rgba(6,12,36,.85),rgba(6,12,36,0));}
.brand{display:flex;align-items:center;gap:18px}
.badge{width:58px;height:58px;border-radius:50%;background:var(--gold);color:var(--navy);display:flex;align-items:center;justify-content:center;font-family:"GK Mono";font-weight:800;font-size:24px;box-shadow:0 0 0 4px rgba(242,178,51,.25)}
.brand b{font-weight:900;font-size:30px;letter-spacing:.02em;color:#fff}
.brand i{font-style:normal;font-family:"GK Mono";font-weight:700;font-size:22px;color:var(--gold2);letter-spacing:.12em;padding-left:18px;border-left:3px solid rgba(242,178,51,.5)}
.vinfo{display:flex;align-items:center;gap:22px}
.vinfo .vt{font-family:"GK Mono";font-weight:700;font-size:22px;color:var(--muted);letter-spacing:.08em}
.pill{width:64px;height:44px;border-radius:22px;border:3px solid rgba(159,176,224,.45);display:flex;align-items:center;justify-content:center;font-family:"GK Mono";font-weight:800;font-size:20px;color:var(--muted);position:relative}
.pill .pf{position:absolute;inset:-3px;border-radius:22px;background:var(--gold);opacity:0}
.pill .pd{position:absolute;inset:-3px;border-radius:22px;background:var(--green);opacity:0}
.pill span{position:relative}
/* avatar */
#avatar .av-move{position:absolute;left:1290px;top:300px;width:760px;height:1000px}
#avatar .av-shadow{position:absolute;left:190px;top:960px;width:380px;height:60px;border-radius:50%;background:radial-gradient(closest-side,rgba(0,0,0,.55),rgba(0,0,0,0))}
#avatar .av-pop,#avatar .av-talk,#avatar .av-idle{position:absolute;inset:0}
#avatar img{position:absolute;left:0;top:0;width:760px;height:1000px;opacity:0}
.half{position:absolute;width:820px;height:990px}
.half .av-talk{position:absolute;inset:0}
.half img{position:absolute;left:0;top:0;width:820px;height:990px}
/* altyazı */
#caps .cap{position:absolute;left:64px;top:936px;width:1240px;height:112px;display:flex;align-items:center;justify-content:center;opacity:0}
#caps .cap span{display:block;max-width:1240px;padding:12px 30px;border-radius:18px;background:rgba(5,10,30,.86);border:2px solid rgba(242,178,51,.35);
font-weight:600;font-size:33px;line-height:1.28;color:#fff;text-align:center}
/* giriş */
.intro-kicker{position:absolute;left:110px;top:150px;font-family:"GK Mono";font-weight:700;font-size:30px;letter-spacing:.24em;color:var(--gold)}
.intro-num{position:absolute;left:104px;top:205px;font-family:"GK Mono";font-weight:800;font-size:140px;letter-spacing:-.02em;color:var(--gold);line-height:1}
.intro-title{position:absolute;left:104px;top:390px;width:1150px;font-weight:900;font-size:118px;line-height:1.0;letter-spacing:-.035em;color:#fff}
.intro-title .w{display:inline-block;margin-right:28px}
.intro-sub{position:absolute;left:110px;top:0;width:1100px;font-family:"GK Serif";font-weight:500;font-size:40px;line-height:1.3;color:var(--muted)}
.chips{position:absolute;left:104px;display:flex;gap:18px}
.chip{display:flex;align-items:center;gap:12px;padding:14px 26px;border-radius:40px;font-weight:800;font-size:28px;letter-spacing:.04em}
.chip .dot{width:16px;height:16px;border-radius:50%}
/* soru kartı */
.qbig{position:absolute;left:0;top:0;width:1340px;height:1080px;display:flex;align-items:center;justify-content:center}
.qbig b{display:block;font-weight:900;font-size:200px;letter-spacing:-.04em;color:var(--gold)}
.card{position:absolute;left:64px;top:118px;width:1262px;height:798px;border-radius:30px;background:var(--paper);color:var(--ink);
box-shadow:0 30px 60px rgba(0,0,0,.45),0 0 0 6px rgba(242,178,51,.18);overflow:hidden}
.card .rules{position:absolute;inset:0;background-image:linear-gradient(rgba(22,34,76,.06) 2px,transparent 2px);background-size:100% 46px;background-position:0 22px}
.card .margin{position:absolute;left:96px;top:0;width:3px;height:100%;background:rgba(217,68,63,.35)}
.card .chead{position:absolute;left:130px;top:34px;right:44px;height:56px;display:flex;align-items:center;gap:16px}
.qchip{padding:10px 22px;border-radius:14px;background:var(--ink);color:#fff;font-weight:900;font-size:26px;letter-spacing:.06em}
.tchip{padding:10px 20px;border-radius:14px;border:3px solid var(--ink);font-weight:700;font-size:22px;color:var(--ink)}
.chead .src{margin-left:auto;font-family:"GK Mono";font-weight:700;font-size:20px;color:rgba(22,34,76,.6)}
.cbody{position:absolute;left:130px;top:112px;right:52px;bottom:30px;display:flex;flex-direction:column;gap:14px}
.stem{font-family:"GK Serif";font-weight:600;color:var(--ink);line-height:1.3}
.stem .mk{position:relative;display:inline-block}
.stem .mk .mkbg{position:absolute;left:-6px;right:-6px;bottom:2px;height:46%;background:rgba(242,178,51,.65);border-radius:6px;transform-origin:0 50%;z-index:0}
.stem .mk .mkt{position:relative;z-index:1}
.stmts{display:flex;flex-direction:column;gap:6px;padding-left:6px}
.stmt{font-family:"GK Serif";font-weight:500;color:var(--ink);line-height:1.28;display:flex;gap:16px}
.stmt .rn{font-weight:800;min-width:56px}
.opts{display:flex;flex-direction:column;gap:10px}
.opt{position:relative;display:flex;align-items:flex-start;gap:18px;padding:6px 10px;border-radius:14px}
.opt .hl{position:absolute;inset:0;border-radius:14px;background:rgba(24,165,107,.20);border:3px solid var(--green);transform-origin:0 50%;opacity:0}
.opt .lt{position:relative;flex:0 0 auto;width:50px;height:50px;border-radius:50%;border:3px solid var(--ink);display:flex;align-items:center;justify-content:center;font-weight:900;font-size:24px;color:var(--ink)}
.opt .lt .ltf{position:absolute;inset:-3px;border-radius:50%;background:var(--green);opacity:0}
.opt .lt span{position:relative}
.opt .tx{position:relative;font-family:"GK Serif";font-weight:500;color:var(--ink);line-height:1.28;padding-top:5px}
.opt .strike{position:absolute;left:78px;right:20px;top:50%;height:4px;background:var(--red);border-radius:2px;transform-origin:0 50%;opacity:.85}
.opt .ck{position:absolute;right:16px;top:50%;width:54px;height:54px;margin-top:-27px;border-radius:50%;background:var(--green);display:flex;align-items:center;justify-content:center;opacity:0}
.optgrid{display:grid;grid-template-columns:repeat(5,1fr);gap:14px}
.optgrid .opt{border:3px solid rgba(22,34,76,.25);background:rgba(255,255,255,.4);align-items:center;padding:10px 12px;gap:12px}
.optgrid .opt .lt{width:44px;height:44px;font-size:22px}
.optgrid .opt .tx{padding-top:0;font-weight:700}
.optgrid .opt .strike{left:12px;right:12px}
.optgrid .opt .ck{width:40px;height:40px;margin-top:-20px;right:-14px;top:0}
.timer{position:absolute;left:1560px;top:92px;width:210px;height:210px;opacity:0}
.timer .tbg{position:absolute;inset:0;border-radius:50%;background:var(--navy);box-shadow:0 14px 30px rgba(0,0,0,.35)}
.timer svg{position:absolute;inset:0;width:210px;height:210px}
.timer .tn{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-family:"GK Mono";font-weight:800;font-size:92px;color:#fff;opacity:0}
.timer .tl{position:absolute;left:0;top:150px;width:210px;text-align:center;font-weight:800;font-size:20px;letter-spacing:.14em;color:var(--gold2)}
.stampa{position:absolute;right:36px;top:22px;padding:10px 24px;border:6px solid var(--green);border-radius:16px;color:var(--green);font-weight:900;font-size:34px;letter-spacing:.06em;white-space:nowrap;background:rgba(246,241,228,.96);opacity:0}
/* çözüm tahtası */
.bhead{position:absolute;left:64px;top:118px;width:1262px;height:84px;display:flex;align-items:center;gap:18px}
.bhead .sol{padding:12px 26px;border-radius:16px;background:var(--gold);color:var(--navy);font-weight:900;font-size:30px;letter-spacing:.08em}
.bhead .ttl{font-weight:800;font-size:40px;color:#fff;letter-spacing:-.01em}
.bhead .ans{margin-left:auto;display:flex;align-items:center;gap:10px;padding:10px 22px;border-radius:16px;background:rgba(24,165,107,.18);border:3px solid var(--green);font-weight:800;font-size:26px;color:#BFF2DA}
.mchip{position:absolute;left:64px;top:214px;display:flex;align-items:center;gap:12px;padding:8px 18px;border-radius:12px;background:rgba(242,178,51,.12);border:2px solid rgba(242,178,51,.55);font-family:"GK Mono";font-weight:700;font-size:21px;color:var(--gold2)}
.diag{position:absolute;left:64px;top:268px;width:1262px;height:420px}
.diag svg.arr{position:absolute;left:0;top:0;width:1262px;height:420px;overflow:visible}
.node{position:absolute;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;border-radius:20px;padding:14px 16px;
background:var(--navy2);border:3px solid rgba(159,176,224,.45);color:#fff;font-weight:700;font-size:27px;line-height:1.2;opacity:0}
.node .sub{display:block;margin-top:6px;font-family:"GK Serif";font-weight:500;font-size:22px;color:var(--muted);line-height:1.22}
.node .num{position:absolute;left:-18px;top:-18px;width:44px;height:44px;border-radius:50%;background:var(--gold);color:var(--navy);font-family:"GK Mono";font-weight:800;font-size:22px;display:flex;align-items:center;justify-content:center}
.node.gold{border-color:var(--gold);background:#2A2F5E}
.node.green{border-color:var(--green);background:#0F3A3A}
.node.red{border-color:var(--red);background:#3A1A2E}
.node.paper{background:var(--paper);color:var(--ink);border-color:var(--paper)}
.node.paper .sub{color:#3A4775}
.node .glowr{position:absolute;inset:-10px;border-radius:26px;border:5px solid var(--gold);opacity:0}
.col{position:absolute;top:0;height:420px;border-radius:24px;border:3px dashed rgba(159,176,224,.35);opacity:0}
.col .ch{position:absolute;left:0;top:0;width:100%;height:70px;border-radius:20px 20px 0 0;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:28px;letter-spacing:.06em}
.col.green .ch{background:rgba(24,165,107,.25);color:#BFF2DA}
.col.red .ch{background:rgba(217,68,63,.25);color:#FFC9C6}
.col.gold .ch{background:rgba(242,178,51,.22);color:var(--gold2)}
.col.navy .ch{background:rgba(159,176,224,.18);color:#fff}
.tlaxis{position:absolute;left:40px;top:200px;width:1180px;height:6px;border-radius:3px;background:rgba(159,176,224,.55);transform-origin:0 50%}
.opsym{position:absolute;width:60px;height:60px;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:54px;color:var(--gold);opacity:0}
.callout{position:absolute;left:64px;top:704px;width:1262px;height:212px;border-radius:26px;display:flex;align-items:stretch;overflow:hidden;opacity:0;box-shadow:0 20px 40px rgba(0,0,0,.4)}
.callout .cl{flex:0 0 230px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;font-weight:900;font-size:34px;letter-spacing:.08em}
.callout .cl svg{width:64px;height:64px}
.callout .cr{flex:1;display:flex;flex-direction:column;justify-content:center;gap:8px;padding:18px 34px;background:#F6F1E4;color:var(--ink)}
.callout .cr b{font-weight:900;font-size:33px;line-height:1.15}
.callout .cr p{font-family:"GK Serif";font-weight:500;font-size:27px;line-height:1.28}
.callout.tuzak .cl{background:repeating-linear-gradient(-45deg,#FFD60A 0 26px,#151515 26px 52px);color:#fff}
.callout.tuzak .cl span{background:#D9443F;padding:6px 16px;border-radius:10px}
.callout.tuzak .cl svg{color:#fff;background:#151515;border-radius:14px;padding:6px;width:76px;height:76px}
.callout.dikkat .cl{background:var(--orange);color:#fff}
.callout.uyari .cl{background:var(--red);color:#fff}
.callout.onemli .cl{background:var(--gold);color:var(--navy)}
.callout.q{left:64px;top:700px;width:1262px}
/* özet */
.sumtitle{position:absolute;left:64px;top:128px;font-weight:900;font-size:76px;letter-spacing:-.02em;color:#fff}
.sumtitle em{font-style:normal;color:var(--gold)}
.mcard{position:absolute;left:64px;width:1262px;height:168px;border-radius:24px;background:var(--paper);color:var(--ink);display:flex;align-items:center;gap:26px;padding:0 34px;opacity:0;box-shadow:0 16px 32px rgba(0,0,0,.35)}
.mcard .mn{flex:0 0 auto;width:88px;height:88px;border-radius:22px;background:var(--navy);color:var(--gold);font-family:"GK Mono";font-weight:800;font-size:30px;display:flex;align-items:center;justify-content:center}
.mcard b{display:block;font-weight:900;font-size:31px;line-height:1.15}
.mcard p{font-family:"GK Serif";font-weight:500;font-size:27px;line-height:1.25;margin-top:6px;color:#2A3666}
.score{position:absolute;left:64px;top:840px;display:flex;gap:14px;opacity:0}
.score div{padding:12px 22px;border-radius:14px;font-weight:800;font-size:24px}
/* kapanış */
.out-k{position:absolute;left:110px;top:170px;font-family:"GK Mono";font-weight:700;font-size:30px;letter-spacing:.2em;color:var(--gold)}
.out-t{position:absolute;left:104px;top:226px;width:1050px;font-weight:900;font-size:96px;line-height:1.02;letter-spacing:-.03em;color:#fff}
.out-n{position:absolute;left:110px;top:560px;width:1000px;padding:26px 34px;border-radius:24px;background:rgba(242,178,51,.12);border:3px solid var(--gold)}
.out-n small{display:block;font-family:"GK Mono";font-weight:700;font-size:22px;letter-spacing:.16em;color:var(--gold2)}
.out-n b{display:block;margin-top:8px;font-weight:900;font-size:44px;color:#fff}
"""


class Comp:
    """Zaman çizelgesi + HTML üreticisi"""

    def __init__(self):
        self.js = []          # timeline satırları
        self.sfx = []         # (t, name, gain)
        self.ids = 0

    def uid(self, p):
        self.ids += 1
        return f"{p}{self.ids}"

    def add(self, line):
        self.js.append(line)

    def set(self, sel, props, t):
        self.add(f'tl.set("{sel}",{json.dumps(props)},{r3(t)});')

    def to(self, sel, props, t):
        self.add(f'tl.to("{sel}",{json.dumps(props)},{r3(t)});')

    def fromto(self, sel, a, b, t):
        # emit() sırasında: aynı hedefte en erken fromTo dışındakilere immediateRender:false eklenir
        self.js.append({"sel": sel, "a": a, "b": b, "t": float(t)})

    def emit(self):
        first = {}
        for it in self.js:
            if isinstance(it, dict):
                if it["sel"] not in first or it["t"] < first[it["sel"]]["t"]:
                    first[it["sel"]] = it
        out = []
        for it in self.js:
            if isinstance(it, dict):
                b = dict(it["b"])
                if first[it["sel"]] is not it:
                    b["immediateRender"] = False
                out.append(f'tl.fromTo("{it["sel"]}",{json.dumps(it["a"])},{json.dumps(b)},{r3(it["t"])});')
            else:
                out.append(it)
        return out

    def sound(self, t, name, gain=1.0):
        self.sfx.append((float(t), name, gain))


def build_video(vid):
    spec = load_spec(vid)
    segs = segments(spec)
    adir = os.path.join(HERE, "audio", f"v{vid}")
    proj = os.path.normpath(os.path.join(HERE, "..", f"gmy-kamp-{vid}"))
    os.makedirs(os.path.join(proj, "assets"), exist_ok=True)
    write_brief(proj, spec)

    # --- ses segmentleri ve hizalayıcılar
    A = {}
    for s in segs:
        mp3 = os.path.join(adir, s["id"] + ".mp3")
        x = read_audio(mp3)
        dur = len(x) / SR
        sb = speech_bounds(x)
        wj = os.path.join(adir, s["id"] + ".words.json")
        words = json.load(open(wj, encoding="utf-8")) if os.path.exists(wj) else []
        al = Aligner(s["text"], words, dur, sb)
        # parça başlangıç zamanları
        pstarts = []
        idx = 0
        for p in s["parts"]:
            pstarts.append(al.t(idx))
            idx += len(tokens(p["say"]))
        A[s["id"]] = {"x": x, "dur": dur, "al": al, "pt": pstarts, "speech": sb, "seg": s}
        print(f"  {s['id']:10s} {dur:6.2f}s  eşleşme %{al.match_ratio*100:4.0f}")

    C = Comp()
    nq = len(spec["questions"])
    placements = []  # (t, seg_id)
    poses = []       # (t, pose)

    # ---------------- zamanlama planı
    T = {}
    t = 0.0
    T["intro_scene"] = 0.0
    T["intro_say"] = 1.1
    placements.append((T["intro_say"], "intro"))
    t = T["intro_say"] + A["intro"]["dur"] + 0.5
    Q = []
    for i in range(1, nq + 1):
        q = {}
        q["start"] = t
        q["read"] = t + 1.5
        placements.append((q["read"], f"q{i}_read"))
        q["think"] = q["read"] + A[f"q{i}_read"]["dur"] + 0.3
        placements.append((q["think"], f"q{i}_think"))
        q["cd"] = q["think"] + A[f"q{i}_think"]["speech"][1] + 0.25
        q["cd_end"] = q["cd"] + 5.0
        q["exp"] = q["cd_end"] + 0.35
        placements.append((q["exp"], f"q{i}_exp"))
        ex = A[f"q{i}_exp"]
        q["board"] = q["exp"] + ex["pt"][1] - 0.35 if len(ex["pt"]) > 1 else q["exp"] + ex["dur"] * 0.3
        q["end"] = q["exp"] + ex["dur"] + 0.7
        t = q["end"]
        Q.append(q)
    T["sum"] = t
    T["sum_say"] = t + 1.0
    placements.append((T["sum_say"], "summary"))
    t = T["sum_say"] + A["summary"]["dur"] + 0.6
    T["out"] = t
    T["out_say"] = t + 0.8
    placements.append((T["out_say"], "outro"))
    TOTAL = T["out_say"] + A["outro"]["dur"] + 2.2
    TOTAL = math.ceil(TOTAL * 10) / 10

    def ptime(seg, k):
        """segment parçasının global başlangıcı"""
        st = dict((sid, tt) for tt, sid in placements)[seg]
        return st + A[seg]["pt"][k]

    seg_start = dict((sid, tt) for tt, sid in placements)
    XF = 0.45  # sahne geçiş süresi

    scenes_html = []

    def scene(sid, start, end, inner, track=1):
        dur = end - start
        scenes_html.append(
            f'<section id="{sid}" class="scene clip" data-start="{r3(start)}" data-duration="{r3(dur)}" data-track-index="{track}">'
            f'<div class="inner" id="{sid}-in">{inner}</div></section>')
        C.fromto(f"#{sid}-in", {"opacity": 0}, {"opacity": 1, "duration": XF, "ease": "power1.out"}, start)
        C.to(f"#{sid}-in", {"opacity": 0, "duration": XF, "ease": "power1.in"}, end - XF)

    # ---------------- GİRİŞ
    vnum = spec["no"]
    title_words = spec["title"].split()
    tw_html = "".join(f'<span class="w" id="it-w{k}">{esc(w)}</span>' for k, w in enumerate(title_words))
    t_lines = est_lines(spec["title"], 118, 1150, 0.62)
    sub_top = 390 + t_lines * 118 + 30
    chips = spec["intro"].get("chips", ["3 SORU", "TUZAK AVI", "HAFIZA KARTI"])
    chip_colors = ["#F2B233", "#FF7A1A", "#18A56B"]
    chips_html = "".join(
        f'<div class="chip" id="ic{k}" style="background:rgba(255,255,255,.08);border:3px solid {chip_colors[k%3]};color:#fff"><span class="dot" style="background:{chip_colors[k%3]}"></span>{esc(c)}</div>'
        for k, c in enumerate(chips))
    intro_inner = (
        f'<div class="intro-kicker" id="ik">GMY SORU KAMPI · VİDEO {vnum}/5</div>'
        f'<div class="intro-num" id="inum">{int(vnum):02d}</div>'
        f'<div class="intro-title" id="ititle">{tw_html}</div>'
        f'<div class="intro-sub" id="isub" style="top:{sub_top}px">{esc(spec["subtitle"])}</div>'
        f'<div class="chips" style="top:{sub_top + 140}px">{chips_html}</div>'
        f'<div class="half" id="ihalf" style="left:1150px;top:150px"><div class="av-talk" id="ihalf-talk"><img src="assets/avatar/yarim_boy.png" alt=""></div></div>'
    )
    intro_end = Q[0]["start"] + XF
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
    # intro parçaları (chip vurgu vb.)
    for k, p in enumerate(segs[0]["parts"]):
        if p.get("chip") is not None:
            tt = ptime("intro", k)
            C.fromto(f"#ic{p['chip']}", {"scale": 1}, {"scale": 1.12, "duration": 0.25, "ease": "power2.out", "yoyo": True, "repeat": 1}, tt)
    C.fromto("#ititle", {"x": 0}, {"x": -14, "duration": max(1.0, intro_end - 2.0), "ease": "none"}, 1.5)

    # ---------------- SORULAR
    letters = "ABCDE"
    x_scenes = []
    for i, (qs, q) in enumerate(zip(spec["questions"], Q), 1):
        rd = f"q{i}_read"
        ex = f"q{i}_exp"
        pre = f"q{i}"
        onermeli = bool(qs.get("statements"))
        stem_txt = qs["stem"]
        # yazı boyutu seçimi
        width = 1262 - 130 - 52
        best = None
        for stem_px, opt_px in [(40, 34), (38, 32), (36, 31), (34, 30), (32, 28), (30, 27), (29, 26), (28, 25), (27, 24), (26, 23)]:
            h = est_lines(stem_txt, stem_px, width, 0.47) * stem_px * 1.3 + 14
            if onermeli:
                for st in qs["statements"]:
                    h += est_lines(st, opt_px, width - 72, 0.46) * opt_px * 1.28 + 6
                h += 14 + 74
            else:
                for o in qs["options"]:
                    h += max(56, est_lines(o, opt_px, width - 150, 0.46) * opt_px * 1.28 + 12) + 10
            if h <= 640:
                best = (stem_px, opt_px)
                break
        if best is None:
            best = (26, 23)
        stem_px, opt_px = best
        # vurgulanacak ifade
        stem_html = esc(stem_txt)
        marks = []
        for k, p in enumerate(qs["read"]):
            if p.get("mark"):
                mid = f"{pre}-mk{len(marks)}"
                m_esc = esc(p["mark"])
                if m_esc in stem_html:
                    stem_html = stem_html.replace(
                        m_esc, f'<span class="mk"><span class="mkbg" id="{mid}"></span><span class="mkt">{m_esc}</span></span>', 1)
                    marks.append((mid, k))
        body = f'<div class="stem" id="{pre}-stem" style="font-size:{stem_px}px">{stem_html}</div>'
        if onermeli:
            romans = ["I.", "II.", "III.", "IV.", "V."]
            body += '<div class="stmts">' + "".join(
                f'<div class="stmt" id="{pre}-s{k}" style="font-size:{opt_px}px"><span class="rn">{romans[k]}</span><span>{esc(st)}</span></div>'
                for k, st in enumerate(qs["statements"])) + "</div>"
            body += '<div class="optgrid" id="{0}-og">'.format(pre)
            for k, o in enumerate(qs["options"]):
                body += (f'<div class="opt" id="{pre}-o{k}"><div class="hl" id="{pre}-o{k}-hl"></div>'
                         f'<div class="lt"><div class="ltf" id="{pre}-o{k}-ltf"></div><span>{letters[k]}</span></div>'
                         f'<div class="tx" style="font-size:{min(opt_px, 26)}px">{esc(o)}</div>'
                         + ("" if letters[k] == qs["answer"] else f'<div class="strike" id="{pre}-o{k}-st"></div>')
                         + f'<div class="ck" id="{pre}-o{k}-ck"><svg viewBox="0 0 40 40" width="28" height="28"><path d="M8 21 L17 29 L32 11" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg></div></div>')
            body += "</div>"
        else:
            body += '<div class="opts">'
            for k, o in enumerate(qs["options"]):
                body += (f'<div class="opt" id="{pre}-o{k}"><div class="hl" id="{pre}-o{k}-hl"></div>'
                         f'<div class="lt"><div class="ltf" id="{pre}-o{k}-ltf"></div><span>{letters[k]}</span></div>'
                         f'<div class="tx" style="font-size:{opt_px}px">{esc(o)}</div>'
                         + ("" if letters[k] == qs["answer"] else f'<div class="strike" id="{pre}-o{k}-st"></div>')
                         + f'<div class="ck" id="{pre}-o{k}-ck"><svg viewBox="0 0 40 40" width="34" height="34"><path d="M8 21 L17 29 L32 11" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg></div></div>')
            body += "</div>"
        ans = letters.index(qs["answer"])
        card = (
            f'<div class="card" id="{pre}-card"><div class="rules"></div><div class="margin"></div>'
            f'<div class="chead"><div class="qchip">SORU {i}/{nq}</div><div class="tchip">{esc(qs["chip"])}</div><div class="src">{esc(qs.get("src", "GMY tarzı · özgün soru"))}</div></div>'
            f'<div class="cbody" id="{pre}-body">{body}</div>'
            f'<div class="stampa" id="{pre}-stamp">DOĞRU CEVAP: {qs["answer"]}</div></div>'
        )
        timer = (
            f'<div class="timer" id="{pre}-timer"><div class="tbg"></div>'
            f'<svg viewBox="0 0 210 210"><circle cx="105" cy="105" r="88" fill="none" stroke="rgba(159,176,224,.25)" stroke-width="14"/>'
            f'<circle id="{pre}-ring" cx="105" cy="105" r="88" fill="none" stroke="#F2B233" stroke-width="14" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="0" transform="rotate(-90 105 105)"/></svg>'
            + "".join(f'<div class="tn" id="{pre}-tn{n}">{n}</div>' for n in range(5, 0, -1))
            + '<div class="tl">DÜŞÜN</div></div>'
        )
        qbig = f'<div class="qbig" id="{pre}-big"><b>SORU {i}</b></div>'
        # soru sahnesindeki callout (opsiyonel)
        qcall_html = ""
        qcalls = []
        for k, p in enumerate(qs["read"]):
            if p.get("callout"):
                cid = f"{pre}-qc{len(qcalls)}"
                qcall_html += callout_html(cid, p["callout"], extra="q")
                qcalls.append((cid, k, p["callout"]))
        q_end_scene = q["board"] + XF
        scene(f"sc-{pre}", q["start"], q_end_scene, qbig + card + timer + qcall_html)
        # --- animasyonlar
        t0 = q["start"]
        C.sound(t0 + 0.02, "whoosh", 0.7)
        C.fromto(f"#{pre}-big", {"scale": 1.8, "opacity": 0}, {"scale": 1, "opacity": 1, "duration": 0.45, "ease": "back.out(1.7)"}, t0 + 0.05)
        C.sound(t0 + 0.2, "thud", 0.8)
        C.to(f"#{pre}-big", {"scale": 0.6, "opacity": 0, "y": -300, "duration": 0.45, "ease": "power3.in"}, t0 + 0.95)
        C.fromto(f"#{pre}-card", {"y": 120, "opacity": 0, "rotation": -1.5}, {"y": 0, "opacity": 1, "rotation": 0, "duration": 0.7, "ease": "power3.out"}, t0 + 1.05)
        # okunan parçalar
        opt_shown = set()
        for k, p in enumerate(qs["read"]):
            tt = ptime(rd, k)
            if k == 0:
                C.fromto(f"#{pre}-stem", {"opacity": 0, "y": 16}, {"opacity": 1, "y": 0, "duration": 0.5, "ease": "power2.out"}, min(tt, q["read"]) - 0.1)
            if p.get("show") is not None:
                show = p["show"] if isinstance(p["show"], list) else [p["show"]]
                for s_i, sv in enumerate(show):
                    if isinstance(sv, str) and sv.startswith("S"):
                        n = int(sv[1:])
                        C.fromto(f"#{pre}-s{n}", {"opacity": 0, "x": -30}, {"opacity": 1, "x": 0, "duration": 0.45, "ease": "power3.out"}, tt - 0.05 + s_i * 0.08)
                    else:
                        oi = letters.index(sv)
                        opt_shown.add(oi)
                        C.fromto(f"#{pre}-o{oi}", {"opacity": 0, "x": -40}, {"opacity": 1, "x": 0, "duration": 0.45, "ease": "power3.out"}, tt - 0.05 + s_i * 0.08)
                        C.sound(tt - 0.05 + s_i * 0.08, "pop", 0.35)
            if p.get("pose"):
                poses.append((tt, p["pose"]))
        for (mid, k) in marks:
            tt = ptime(rd, k)
            C.fromto(f"#{mid}", {"scaleX": 0}, {"scaleX": 1, "duration": 0.5, "ease": "power2.inOut"}, tt + 0.15)
        for (cid, k, co) in qcalls:
            tt = ptime(rd, k)
            show_callout(C, cid, co, tt, poses)
            # bir sonraki parçada (yoksa düşünme başlangıcında) kapanır
            t_close = ptime(rd, k + 1) if k + 1 < len(qs["read"]) else q["think"]
            C.to(f"#{cid}", {"opacity": 0, "y": 40, "duration": 0.3, "ease": "power2.in"}, max(tt + 1.2, t_close - 0.3))
            poses.append((max(tt + 1.2, t_close - 0.3), "anlatim"))
        # gösterilmemiş seçenekler okuma başında görünsün
        for oi in range(5):
            if oi not in opt_shown:
                C.fromto(f"#{pre}-o{oi}", {"opacity": 0, "x": -40}, {"opacity": 1, "x": 0, "duration": 0.45, "ease": "power3.out"}, q["read"] + 0.3 + 0.08 * oi)
        if not qs["read"][0].get("pose"):
            poses.append((q["start"] + 0.2, "anlatim"))
        # düşünme + geri sayım
        poses.append((q["think"], "dusunme"))
        C.fromto(f"#{pre}-timer", {"scale": 0.4, "opacity": 0}, {"scale": 1, "opacity": 1, "duration": 0.5, "ease": "back.out(1.8)"}, q["think"] + 0.1)
        C.sound(q["think"] + 0.1, "pop", 0.6)
        C.fromto(f"#{pre}-ring", {"strokeDashoffset": 0}, {"strokeDashoffset": 1, "duration": 5.0, "ease": "none"}, q["cd"])
        for n in range(5):
            tn = q["cd"] + n
            C.set(f"#{pre}-tn{5-n}", {"opacity": 1}, tn)
            C.fromto(f"#{pre}-tn{5-n}", {"scale": 1.35}, {"scale": 1, "duration": 0.35, "ease": "power3.out"}, tn)
            C.set(f"#{pre}-tn{5-n}", {"opacity": 0}, tn + 0.999)
            C.sound(tn, "tick" if n % 2 == 0 else "tock", 0.8)
        C.to(f"#{pre}-timer", {"scale": 0.5, "opacity": 0, "duration": 0.3, "ease": "power2.in"}, q["cd_end"])
        # cevap açılışı
        tr = q["exp"] + A[ex]["pt"][0]
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

        # --- ÇÖZÜM TAHTASI
        b = qs["board"]
        x_start = q["board"]
        x_end = (Q[i]["start"] if i < nq else T["sum"]) + XF
        diag_html, diag_items = diagram_html(f"{pre}x", b)
        callouts = []
        call_html = ""
        for k, p in enumerate(qs["explain"]):
            if p.get("callout"):
                cid = f"{pre}x-co{len(callouts)}"
                call_html += callout_html(cid, p["callout"])
                callouts.append((cid, k, p["callout"]))
        board_inner = (
            f'<div class="bhead" id="{pre}x-head"><div class="sol">ÇÖZÜM</div><div class="ttl">{esc(b["title"])}</div>'
            f'<div class="ans"><svg viewBox="0 0 40 40" width="30" height="30"><path d="M8 21 L17 29 L32 11" fill="none" stroke="#BFF2DA" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>Cevap {qs["answer"]}</div></div>'
            f'<div class="mchip" id="{pre}x-m">⚖ Dayanak: {esc(b["madde"])}</div>'
            f'<div class="diag" id="{pre}x-diag">{diag_html}</div>{call_html}'
        )
        scene(f"sc-{pre}x", x_start, x_end, board_inner, track=2)
        C.sound(x_start, "whoosh", 0.55)
        C.fromto(f"#{pre}x-head", {"y": -30, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.5, "ease": "power3.out"}, x_start + 0.15)
        C.fromto(f"#{pre}x-m", {"x": -30, "opacity": 0}, {"x": 0, "opacity": 1, "duration": 0.45, "ease": "power2.out"}, x_start + 0.4)
        shown = set()
        last_call = None
        for k, p in enumerate(qs["explain"]):
            if k == 0:
                continue
            tt = ptime(ex, k)
            if p.get("pose"):
                poses.append((tt, p["pose"]))
            elif k == 1:
                poses.append((tt, "anlatim"))
            for sid in p.get("show", []):
                animate_show(C, f"{pre}x", sid, diag_items, shown, tt)
                tt += 0.12
            hl_t = ptime(ex, k) + (0.75 + 0.12 * len(p.get("show", [])) if p.get("show") else 0.1)
            for hid in p.get("hl", []):
                C.fromto(f"#{pre}x-{hid}-g", {"opacity": 0, "scale": 0.92}, {"opacity": 1, "scale": 1.0, "duration": 0.35, "ease": "power2.out"}, hl_t)
                C.fromto(f"#{pre}x-{hid}", {"scale": 1}, {"scale": 1.06, "duration": 0.3, "ease": "power2.out", "yoyo": True, "repeat": 1}, hl_t)
        for (cid, k, co) in callouts:
            tt = ptime(ex, k)
            if last_call:
                C.to(f"#{last_call}", {"opacity": 0, "y": 60, "duration": 0.3, "ease": "power2.in"}, tt - 0.25)
            show_callout(C, cid, co, tt, poses)
            last_call = cid
        x_scenes.append((x_start, x_end))

    # ---------------- ÖZET
    sm = spec["summary"]
    cards = ""
    n_items = len(sm["items"])
    gap = 16
    ch = 168
    top0 = 250
    for k, it in enumerate(sm["items"]):
        cards += (f'<div class="mcard" id="mc{k}" style="top:{top0 + k * (ch + gap)}px"><div class="mn">S{k+1}</div>'
                  f'<div><b>{esc(it["title"])}</b><p>{esc(it["text"])}</p></div></div>')
    score = ('<div class="score" id="score">'
             '<div style="background:rgba(24,165,107,.2);border:3px solid #18A56B;color:#BFF2DA">3/3 · Müşavirlik yolundasın!</div>'
             '<div style="background:rgba(242,178,51,.14);border:3px solid #F2B233;color:#FFE3A6">2/3 · Tuzakları tekrar et</div>'
             '<div style="background:rgba(217,68,63,.16);border:3px solid #D9443F;color:#FFC9C6">0-1 · Videoyu baştan izle</div></div>')
    sum_inner = f'<div class="sumtitle" id="stitle">AKILDA <em>KALSIN</em> · Hafıza Kartı</div>{cards}{score}'
    scene("sc-sum", T["sum"], T["out"] + XF, sum_inner)
    C.sound(T["sum"], "whoosh", 0.6)
    C.fromto("#stitle", {"y": -40, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.6, "ease": "power3.out"}, T["sum"] + 0.15)
    poses.append((T["sum"] + 0.3, "onemli"))
    item_k = 0
    for k, p in enumerate(sm["parts"]):
        tt = ptime("summary", k)
        if p.get("item") is not None:
            it = p["item"]
            C.fromto(f"#mc{it}", {"x": -80, "opacity": 0, "rotationX": -50}, {"x": 0, "opacity": 1, "rotationX": 0, "duration": 0.6, "ease": "power3.out"}, tt - 0.1)
            C.sound(tt - 0.1, "pop", 0.5)
        if p.get("score"):
            C.fromto("#score", {"y": 30, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.5, "ease": "back.out(1.6)"}, tt)
            poses.append((tt, "onay"))
        if p.get("pose"):
            poses.append((tt, p["pose"]))
    # (özet kartı item'ı parçalarda yoksa sırayla göster)
    if not any(p.get("item") is not None for p in sm["parts"]):
        for it in range(n_items):
            C.fromto(f"#mc{it}", {"x": -80, "opacity": 0}, {"x": 0, "opacity": 1, "duration": 0.6, "ease": "power3.out"}, T["sum_say"] + 0.5 + it * 2)

    # ---------------- KAPANIŞ
    ou = spec["outro"]
    out_inner = (
        f'<div class="out-k" id="ok">GÜMRÜK KOÇU · GMY SORU KAMPI</div>'
        f'<div class="out-t" id="ot">{esc(ou["title"])}</div>'
        f'<div class="out-n" id="on"><small>SIRADAKİ VİDEO</small><b>{esc(ou["next"])}</b></div>'
        f'<div class="half" id="ohalf" style="left:1150px;top:150px"><div class="av-talk" id="ohalf-talk"><img src="assets/avatar/yarim_boy_kapanis.png" alt=""></div></div>'
    )
    scene("sc-out", T["out"], TOTAL, out_inner)
    C.sound(T["out"], "whoosh", 0.6)
    C.fromto("#ok", {"x": -60, "opacity": 0}, {"x": 0, "opacity": 1, "duration": 0.5, "ease": "power3.out"}, T["out"] + 0.2)
    C.fromto("#ot", {"y": 60, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.7, "ease": "power4.out"}, T["out"] + 0.35)
    C.fromto("#on", {"scale": 0.8, "opacity": 0}, {"scale": 1, "opacity": 1, "duration": 0.5, "ease": "back.out(1.8)"}, T["out"] + 0.9)
    C.fromto("#ohalf", {"x": 520, "opacity": 0}, {"x": 0, "opacity": 1, "duration": 0.8, "ease": "back.out(1.2)"}, T["out"] + 0.3)
    C.sound(T["out"] + 0.9, "chime", 0.6)

    # ---------------- ÜST BAR
    pills = "".join(f'<div class="pill" id="pl{k}"><div class="pf" id="pl{k}-f"></div><div class="pd" id="pl{k}-d"></div><span>S{k+1}</span></div>' for k in range(nq))
    topbar = (f'<div id="topbar" class="clip" data-start="{r3(Q[0]["start"])}" data-duration="{r3(T["out"] + XF - Q[0]["start"])}" data-track-index="5">'
              f'<div class="bar" id="tb-in"><div class="brand"><div class="badge">GK</div><b>GÜMRÜK KOÇU</b><i>GMY SORU KAMPI</i></div>'
              f'<div class="vinfo"><div class="vt">VİDEO {vnum}/5 · {esc(spec["short"])}</div>{pills}</div></div></div>')
    C.fromto("#tb-in", {"y": -100, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.5, "ease": "power3.out"}, Q[0]["start"] + 0.1)
    C.to("#tb-in", {"opacity": 0, "duration": XF}, T["out"])
    for k, q in enumerate(Q):
        C.fromto(f"#pl{k}-f", {"opacity": 0}, {"opacity": 1, "duration": 0.3}, q["start"] + 0.2)
        C.add(f'tl.set("#pl{k} span",{{"color":"#0A1438"}},{r3(q["start"] + 0.2)});')
        C.to(f"#pl{k}-d", {"opacity": 1, "duration": 0.3}, q["exp"] + 0.4)
        C.add(f'tl.set("#pl{k} span",{{"color":"#ffffff"}},{r3(q["exp"] + 0.4)});')

    # ---------------- AVATAR (tam boy pozlar)
    av_imgs = "".join(f'<img id="av-{p}" src="assets/avatar/{p}.png" alt="">' for p in POSES)
    avatar = (f'<div id="avatar" class="clip" data-start="0" data-duration="{r3(TOTAL)}" data-track-index="6">'
              f'<div class="av-move" id="av-move"><div class="av-shadow"></div><div class="av-pop" id="av-pop"><div class="av-idle" id="av-idle"><div class="av-talk" id="av-talk">{av_imgs}</div></div></div></div></div>')
    C.set("#av-move", {"opacity": 0, "x": 500}, 0)
    C.to("#av-move", {"opacity": 1, "x": 0, "duration": 0.8, "ease": "back.out(1.3)"}, Q[0]["start"] + 0.5)
    C.to("#av-move", {"opacity": 0, "x": 500, "duration": 0.6, "ease": "power2.in"}, T["out"] - 0.1)
    # poz değişimleri
    poses.sort()
    cur = None
    C.set("#av-anlatim", {"opacity": 1}, 0)
    cur = "anlatim"
    last_t = -9
    for tt, p in poses:
        if p == cur:
            continue
        if tt - last_t < 0.5:
            tt = last_t + 0.5
        C.to(f"#av-{cur}", {"opacity": 0, "duration": 0.14, "ease": "none"}, tt)
        C.to(f"#av-{p}", {"opacity": 1, "duration": 0.14, "ease": "none"}, tt)
        C.fromto("#av-pop", {"scale": 0.96, "y": 10}, {"scale": 1, "y": 0, "duration": 0.35, "ease": "back.out(2.2)"}, tt)
        cur = p
        last_t = tt
    # nefes alma (sonlu tekrar)
    rep = max(0, int(math.floor(TOTAL / 3.2)) - 1)
    C.add(f'tl.fromTo("#av-idle",{{"scaleY":1}},{{"scaleY":1.012,"duration":1.6,"ease":"sine.inOut","yoyo":true,"repeat":{rep}}},0);')

    # ---------------- SES MİKSİ + konuşma zarfı
    mix, env = mix_audio(A, placements, C.sfx, TOTAL, adir)
    write_wav(os.path.join(proj, "assets", "mix.wav"), mix)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(proj, "assets", "mix.wav"), "-c:a", "libmp3lame", "-b:a", "192k",
                    os.path.join(proj, "assets", "mix.mp3")], check=True)
    os.remove(os.path.join(proj, "assets", "mix.wav"))
    # konuşma animasyonu: zarf -> tween anahtarları
    def talk_keys(sel, t_from, t_to):
        n0 = int(t_from * FPS_ENV)
        n1 = min(len(env) - 1, int(t_to * FPS_ENV))
        prev = None
        for n in range(n0, n1):
            e = float(env[n])
            sy = round(1 + 0.022 * e, 4)
            yy = round(-7 * e, 2)
            rot = round(0.9 * e * math.sin(n * 0.9), 3)
            key = (sy, yy, rot)
            if prev == key:
                continue
            prev = key
            C.add(f'tl.to("{sel}",{{scaleY:{sy},y:{yy},rotation:{rot},duration:{r3(0.97 / FPS_ENV)},ease:"sine.inOut"}},{r3(n / FPS_ENV)});')
    talk_keys("#av-talk", Q[0]["start"], T["out"] + 0.5)
    talk_keys("#ihalf-talk", 0, intro_end)
    talk_keys("#ohalf-talk", T["out"], TOTAL)

    # ---------------- ALTYAZI
    caps_html = []
    ci = 0
    for (st, sid) in placements:
        a = A[sid]
        for (c0, c1, txt) in caption_chunks(a):
            caps_html.append(f'<div class="cap" id="cap{ci}"><span>{esc(txt)}</span></div>')
            C.set(f"#cap{ci}", {"opacity": 1}, st + c0)
            C.set(f"#cap{ci}", {"opacity": 0}, st + c1)
            ci += 1
    caps = (f'<div id="caps" class="clip" data-start="0" data-duration="{r3(TOTAL)}" data-track-index="7">' + "".join(caps_html) + "</div>")

    # ---------------- ARKA PLAN
    bg = (f'<div id="bg" class="clip" data-start="0" data-duration="{r3(TOTAL)}" data-track-index="0">'
          f'<div class="bgfill"></div><div class="grid" id="bg-grid"></div>'
          f'<div class="glow" id="bg-g1" style="left:-200px;top:-260px"></div><div class="glow" id="bg-g2" style="left:1250px;top:520px"></div>'
          f'<div class="ghost" id="bg-ghost" aria-hidden="true" data-t="GÜMRÜK · KOÇU · GMY"></div></div>')
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
<title>GMY Soru Kampı · Video {vnum} · {esc(spec['short'])}</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>{CSS}</style>
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
    # paylaşılan varlıklar
    for sub in ["fonts", "avatar"]:
        dst = os.path.join(proj, "assets", sub)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(os.path.join(HERE, "shared", sub), dst)
    # zaman çizelgesi özeti
    info = {"total": TOTAL, "questions": [{k: r3(v) for k, v in q.items()} for q in Q], "summary": r3(T["sum"]), "outro": r3(T["out"])}
    with open(os.path.join(proj, "timing.json"), "w") as f:
        json.dump(info, f, indent=1)
    print(f"video {vid}: {TOTAL:.1f}s, {len(C.js)} tween satırı, {len(caps_html)} altyazı -> {proj}")


# ----------------------------------------------------------------------------
def write_brief(proj, spec):
    p = os.path.join(proj, "BRIEF.md")
    if os.path.exists(p):
        return
    qs = "\n".join(f"- Soru {i}: {q['chip']} — doğru cevap {q['answer']}" for i, q in enumerate(spec["questions"], 1))
    with open(p, "w", encoding="utf-8") as f:
        f.write(f"""---
workflow: general-video
flow: automation
storyboard: no
message: "GMY Soru Kampı {spec['no']}/5 — {spec['title']}: 3 özgün soru, tuzaklar ve hafıza kartı"
destination: youtube
aspect: 1920x1080
language: tr
audience: "Gümrük Müşavir Yardımcılığı (GMY) sınavına hazırlanan adaylar"
voice: "ElevenLabs eleven_v4 · Cem (D1xRw7f8ZHedI7xJgfvz)"
---

## Intent

Gümrük Koçu ders kanalı için anlatımlı, görselli, şemalı ve yazılı (altyazılı) soru çözüm videosu.
Konu: {spec['title']}. GMY çıkmış sorularının dili ve kurgusuyla hazırlanmış 3 özgün soru;
oklar, şemalar ve ÖNEMLİ / DİKKAT / UYARI / TUZAK kartlarıyla çözüm.

## Assets

- assets/avatar/*.png — Gümrük Koçu avatarının 6 pozu (kullanıcının görselinden kesildi) + yarım boy yeşil fon görseli.
- assets/mix.mp3 — Cem sesiyle anlatım + yerelde sentezlenen efektler ve fon müziği.

## Customizations

- Geri sayım ("Durdur ve düşün"), soru ilerleme göstergesi, mevzuat dayanağı rozeti, hafıza kartı, skor tablosu.
- Avatar: lip-sync yerine sese tepki veren poz animasyonu (lip-sync maliyeti yüksek).

## Notes

{qs}
- Kaynak üretici: ../_uretici (spec/video{int(spec['no']):02d}.json → build.py).
""")


def callout_html(cid, co, extra=""):
    typ = co["type"]
    return (f'<div class="callout {typ} {extra}" id="{cid}"><div class="cl">{CALLOUT_ICON[typ]}<span>{CALLOUT_LABEL[typ]}</span></div>'
            f'<div class="cr"><b>{esc(co["title"])}</b><p>{esc(co["text"])}</p></div></div>')


def show_callout(C, cid, co, tt, poses):
    typ = co["type"]
    if typ == "tuzak":
        C.fromto(f"#{cid}", {"opacity": 0, "scale": 1.25, "rotation": -3}, {"opacity": 1, "scale": 1, "rotation": 0, "duration": 0.35, "ease": "power4.in"}, tt - 0.05)
        C.fromto(f"#{cid}", {"x": 0}, {"x": 10, "duration": 0.05, "ease": "none", "yoyo": True, "repeat": 5}, tt + 0.3)
    elif typ in ("dikkat", "uyari"):
        C.fromto(f"#{cid}", {"opacity": 0, "y": 60}, {"opacity": 1, "y": 0, "duration": 0.45, "ease": "back.out(1.8)"}, tt - 0.05)
    else:
        C.fromto(f"#{cid}", {"opacity": 0, "scale": 0.85}, {"opacity": 1, "scale": 1, "duration": 0.5, "ease": "back.out(2)"}, tt - 0.05)
    C.sound(tt - 0.05, CALLOUT_SFX[typ], 0.9)
    poses.append((tt, co.get("pose", CALLOUT_POSE[typ])))


# ----------------------------------------------------------------------------
# diyagramlar
# ----------------------------------------------------------------------------
def diagram_html(px, b):
    """px: id öneki. Döner: (html, items{id:{kind, sel, edges_in:[...]}})"""
    kind = b["kind"]
    W, H = 1262, 420
    items = {}
    parts = []
    arrows = []  # (id, d, label, lx, ly)

    def node(nid, x, y, w, h, text, sub=None, tone=None, num=None, fs=None):
        cls = "node" + (f" {tone}" if tone else "")
        style = f"left:{x}px;top:{y}px;width:{w}px;height:{h}px" + (f";font-size:{fs}px" if fs else "")
        inner = esc(text) + (f'<span class="sub">{esc(sub)}</span>' if sub else "")
        if num is not None:
            inner = f'<span class="num">{num}</span>' + inner
        parts.append(f'<div class="{cls}" id="{px}-{nid}" style="{style}"><div class="glowr" id="{px}-{nid}-g"></div>{inner}</div>')
        items[nid] = {"type": "node", "edges": [], "x": x, "y": y, "w": w, "h": h}

    def arrow(aid, x1, y1, x2, y2, to, frm, label=None, curve=0):
        if curve:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - curve
            d = f"M{x1} {y1} Q{mx} {my} {x2} {y2}"
        else:
            d = f"M{x1} {y1} L{x2} {y2}"
        arrows.append((aid, d, label, (x1 + x2) / 2, (y1 + y2) / 2 - 18 - (curve / 2 if curve else 0)))
        items.setdefault(to, {"type": "node", "edges": []})
        items[to]["edges"].append((aid, frm))

    if kind == "flow":
        ns = b["nodes"]
        n = len(ns)
        rows = 1 if n <= 4 else 2
        per = math.ceil(n / rows)
        gapx = 74
        w = int((W - gapx * (per - 1)) / per)
        h = 150 if rows == 1 else 150
        for k, nd in enumerate(ns):
            r, c = divmod(k, per)
            if r == 1:
                c = per - 1 - c  # yılan düzeni
            x = c * (w + gapx)
            y = (H - h) // 2 if rows == 1 else (20 + r * 230)
            node(nd["id"], x, y, w, h, nd["text"], nd.get("sub"), nd.get("tone"), nd.get("num"), nd.get("fs"))
        for k in range(1, n):
            a, bnode = ns[k - 1], ns[k]
            A_, B_ = items[a["id"]], items[bnode["id"]]
            if A_["y"] == B_["y"]:
                if B_["x"] > A_["x"]:
                    arrow(f"ar{k}", A_["x"] + A_["w"] + 6, A_["y"] + A_["h"] / 2, B_["x"] - 10, B_["y"] + B_["h"] / 2, bnode["id"], a["id"], bnode.get("elabel"))
                else:
                    arrow(f"ar{k}", A_["x"] - 6, A_["y"] + A_["h"] / 2, B_["x"] + B_["w"] + 10, B_["y"] + B_["h"] / 2, bnode["id"], a["id"], bnode.get("elabel"))
            else:
                arrow(f"ar{k}", A_["x"] + A_["w"] / 2, A_["y"] + A_["h"] + 6, B_["x"] + B_["w"] / 2, B_["y"] - 10, bnode["id"], a["id"], bnode.get("elabel"))
    elif kind == "branch":
        # kök solda, dallar sağda
        root = b["root"]
        brs = b["branches"]
        rw, rh = 360, 170
        node(root["id"], 0, (H - rh) // 2, rw, rh, root["text"], root.get("sub"), root.get("tone", "gold"))
        nb = len(brs)
        bh = min(120, int((H - 16 * (nb - 1)) / nb))
        bw = 700
        bx = W - bw
        tot = nb * bh + (nb - 1) * 16
        y0 = (H - tot) // 2
        for k, br in enumerate(brs):
            y = y0 + k * (bh + 16)
            node(br["id"], bx, y, bw, bh, br["text"], br.get("sub"), br.get("tone"), br.get("num"), br.get("fs", 25))
            arrow(f"ar{k}", rw + 8, H / 2, bx - 12, y + bh / 2, br["id"], root["id"], br.get("elabel"), curve=0)
    elif kind == "split":
        cols = b["columns"]
        nc = len(cols)
        gap = 30
        cw = int((W - gap * (nc - 1)) / nc)
        for k, c in enumerate(cols):
            x = k * (cw + gap)
            parts.append(f'<div class="col {c.get("tone","navy")}" id="{px}-{c["id"]}" style="left:{x}px;width:{cw}px"><div class="ch">{esc(c["title"])}</div></div>')
            items[c["id"]] = {"type": "col", "edges": []}
            its = [it for it in b["items"] if it["col"] == c["id"]]
            ni = len(its)
            ih = min(96, int((420 - 86 - 12 * max(0, ni - 1) - 14) / max(1, ni)))
            for j, it in enumerate(its):
                node(it["id"], x + 18, 84 + j * (ih + 12), cw - 36, ih, it["text"], it.get("sub"), it.get("tone"), None, it.get("fs", 24))
    elif kind == "steps":
        ns = b["nodes"]
        n = len(ns)
        gap = 18
        h = min(96, int((H - gap * (n - 1)) / n))
        for k, nd in enumerate(ns):
            x = 60 + k * int((W - 760 - 60) / max(1, n - 1)) if n > 1 else 60
            y = k * (h + gap)
            node(nd["id"], x, y, 700, h, nd["text"], nd.get("sub"), nd.get("tone"), k + 1, nd.get("fs", 25))
        for k in range(1, n):
            A_, B_ = items[ns[k - 1]["id"]], items[ns[k]["id"]]
            arrow(f"ar{k}", A_["x"] + 40, A_["y"] + A_["h"] + 2, B_["x"] + 40 - 0, B_["y"] - 4, ns[k]["id"], ns[k - 1]["id"])
    elif kind == "formula":
        ts = b["terms"]
        n = len(ts)
        opw = 64
        w = int((W - opw * (n - 1)) / n)
        h = 190
        y = (H - h) // 2
        for k, tm in enumerate(ts):
            x = k * (w + opw)
            node(tm["id"], x, y, w, h, tm["text"], tm.get("sub"), tm.get("tone"), None, tm.get("fs", 28))
            if k > 0:
                oid = f"op{k}"
                parts.append(f'<div class="opsym" id="{px}-{oid}" style="left:{x - opw + 2}px;top:{y + h / 2 - 30}px">{esc(tm.get("op", "+"))}</div>')
                items[tm["id"]]["edges"].append(("OP:" + oid, None))
    elif kind == "timeline":
        pts = b["points"]
        n = len(pts)
        parts.append(f'<div class="tlaxis" id="{px}-axis"></div>')
        items["axis"] = {"type": "axis", "edges": []}
        span = 1180
        for k, pt in enumerate(pts):
            cx = 40 + (span * (k + 0.5) / n)
            w = min(300, int(span / n) - 20)
            up = k % 2 == 0
            y = 20 if up else 240
            node(pt["id"], int(cx - w / 2), y, w, 150, pt["text"], pt.get("sub"), pt.get("tone"), None, pt.get("fs", 26))
            arrow(f"art{k}", cx, 203, cx, (y + 150 + 4) if up else (y - 6), pt["id"], "axis")
    else:
        raise ValueError("bilinmeyen diyagram: " + kind)

    svg = ['<svg class="arr" viewBox="0 0 1262 420"><defs>'
           f'<marker id="{px}-ah" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#F2B233"/></marker></defs>']
    labels = []
    for aid, d, label, lx, ly in arrows:
        svg.append(f'<path id="{px}-{aid}" d="{d}" fill="none" stroke="#F2B233" stroke-width="6" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" marker-end="url(#{px}-ah)" opacity="0"/>')
        if label:
            labels.append(f'<div class="node" id="{px}-{aid}-lb" style="left:{lx - 110}px;top:{ly - 26}px;width:220px;height:46px;padding:4px 8px;font-size:20px;border-radius:12px;background:#0A1438;border-color:#F2B233;color:#FFD27A">{esc(label)}</div>')
    svg.append("</svg>")
    return "".join(svg) + "".join(parts) + "".join(labels), items


def animate_show(C, px, sid, items, shown, tt):
    it = items.get(sid)
    if it is None:
        raise ValueError(f"diyagramda yok: {sid}")
    if it["type"] == "col":
        C.fromto(f"#{px}-{sid}", {"opacity": 0, "y": 30}, {"opacity": 1, "y": 0, "duration": 0.45, "ease": "power3.out"}, tt)
        shown.add(sid)
        return
    if it["type"] == "axis":
        C.fromto(f"#{px}-axis", {"scaleX": 0}, {"scaleX": 1, "duration": 0.6, "ease": "power2.inOut"}, tt)
        shown.add(sid)
        return
    delay = 0
    for (aid, frm) in it["edges"]:
        if aid.startswith("OP:"):
            oid = aid[3:]
            C.fromto(f"#{px}-{oid}", {"opacity": 0, "scale": 0.3}, {"opacity": 1, "scale": 1, "duration": 0.3, "ease": "back.out(2)"}, tt)
            delay = 0.15
        elif frm is None or frm in shown:
            C.set(f"#{px}-{aid}", {"opacity": 1}, tt)
            C.fromto(f"#{px}-{aid}", {"strokeDashoffset": 1}, {"strokeDashoffset": 0, "duration": 0.45, "ease": "power2.out"}, tt)
            C.add(f'if (document.getElementById("{px}-{aid}-lb")) tl.fromTo("#{px}-{aid}-lb",{{opacity:0,scale:.7}},{{opacity:1,scale:1,duration:.3,ease:"back.out(2)"}},{r3(tt + 0.3)});')
            delay = 0.3
    C.fromto(f"#{px}-{sid}", {"opacity": 0, "scale": 0.82, "y": 16}, {"opacity": 1, "scale": 1, "y": 0, "duration": 0.45, "ease": "back.out(1.7)"}, tt + delay)
    C.sound(tt + delay, "pop", 0.4)
    shown.add(sid)


# ----------------------------------------------------------------------------
# altyazı
# ----------------------------------------------------------------------------
def caption_chunks(a):
    s = a["seg"]
    al = a["al"]
    text = strip_tags(s["text"])
    words = text.split()
    # cümle/virgül sınırlarında böl, ~62 karakter
    chunks = []
    cur = []
    for w in words:
        cur.append(w)
        L = len(" ".join(cur))
        if (L >= 30 and re.search(r"[.!?…:;]$", w)) or (L >= 44 and w.endswith(",")) or L >= 62:
            chunks.append(cur)
            cur = []
    if cur:
        if chunks and len(" ".join(cur)) < 14:
            chunks[-1] += cur
        else:
            chunks.append(cur)
    out = []
    idx = 0
    starts = []
    for ch in chunks:
        starts.append(al.t(idx))
        idx += len([w for w in ch if norm_tok(w)])
    for k, ch in enumerate(chunks):
        c0 = max(0.0, starts[k] - 0.08)
        c1 = starts[k + 1] - 0.04 if k + 1 < len(chunks) else a["speech"][1] + 0.25
        if c1 - c0 < 0.4:
            c1 = c0 + 0.4
        out.append((c0, c1, " ".join(ch)))
    return out


# ----------------------------------------------------------------------------
# ses miksajı
# ----------------------------------------------------------------------------
def write_wav(p, x):
    y = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    with wave.open(p, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(y.tobytes())


def mix_audio(A, placements, sfx, total, adir):
    n = int(total * SR) + SR
    voice = np.zeros((n, 2))
    for (st, sid) in placements:
        x = A[sid]["x"]
        i0 = int(st * SR)
        m = min(len(x), n - i0)
        voice[i0:i0 + m] += x[:m]
    # ses seviyesi: konuşmayı ~-1 dBFS tepeye yakın normalize et
    pk = np.max(np.abs(voice)) + 1e-9
    voice *= 0.80 / pk
    # efektler
    fx = np.zeros((n, 2))
    cache = {}
    for (t, name, g) in sfx:
        if name not in cache:
            cache[name] = read_audio(os.path.join(HERE, "shared", "sfx", name + ".wav"))
        x = cache[name]
        i0 = int(max(0, t) * SR)
        m = min(len(x), n - i0)
        if m > 0:
            fx[i0:i0 + m] += x[:m] * g * 0.55
    # müzik yatağı (döngü) + konuşmaya göre kısma
    bed = read_audio(os.path.join(HERE, "shared", "sfx", "bed_loop.wav"))
    reps = int(math.ceil(n / len(bed)))
    music = np.tile(bed, (reps, 1))[:n]
    mono = np.abs(voice).mean(1)
    hop = int(SR / FPS_ENV)
    nf = int(math.ceil(n / hop))
    pad = np.zeros(nf * hop)
    pad[:n] = mono
    rms = np.sqrt((pad.reshape(nf, hop) ** 2).mean(1))
    # konuşma zarfı (avatar için)
    env = rms / (np.percentile(rms[rms > 1e-4], 95) + 1e-9) if np.any(rms > 1e-4) else rms
    env = np.clip(env, 0, 1)
    sm = np.convolve(env, np.ones(3) / 3, mode="same")
    # kısma eğrisi
    speaking = (rms > 0.01).astype(float)
    duck = np.convolve(speaking, np.ones(10) / 10, mode="same")
    duck = np.clip(duck * 1.5, 0, 1)
    duck_s = np.repeat(duck, hop)[:n]
    music_gain = 0.16 * (1 - 0.55 * duck_s)
    # giriş/çıkış fade
    fade = np.ones(n)
    fi = int(1.5 * SR)
    fade[:fi] = np.linspace(0, 1, fi)
    fo = int(3.0 * SR)
    end = int(total * SR)
    fade[end - fo:end] = np.linspace(1, 0, fo)
    fade[end:] = 0
    music *= (music_gain * fade)[:, None]
    mix = voice + fx + music
    pk = np.max(np.abs(mix))
    if pk > 0.97:
        mix *= 0.97 / pk
    return mix[: int(total * SR)], sm


if __name__ == "__main__":
    cmd, vid = sys.argv[1], sys.argv[2]
    if cmd == "plan":
        cmd_plan(vid)
    elif cmd == "words":
        cmd_words(vid, sys.argv[3:] or None)
    elif cmd == "build":
        build_video(vid)
    else:
        raise SystemExit("komut: plan|words|build")
