#!/usr/bin/env python3
"""ElevenLabs akış durum çıktısındaki (JSON) üretimleri segment metinleriyle eşleştirip indirir.

Kullanım: python3 fetch_tts.py 01 <creative_get_flow_run_status çıktısı.json>
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
vid, src = sys.argv[1], sys.argv[2]
d = os.path.join(HERE, "audio", f"v{vid}")
segs = json.load(open(os.path.join(d, "segments.json"), encoding="utf-8"))
raw = json.load(open(src, encoding="utf-8"))
if isinstance(raw, list):  # MCP sarmalayıcı: [{"type":"text","text":"{...}"}]
    raw = json.loads(raw[0]["text"])
print("all_completed:", raw.get("all_completed"), "has_failures:", raw.get("has_failures"))
by_prompt = {}
# media[] tam istemi (prompt) taşır; generations[] istemi kısaltılmış olabilir
for m in raw.get("media", []):
    if m.get("url") and m.get("prompt"):
        by_prompt[m["prompt"].strip()] = {"content_url": m["url"], "duration_secs": m.get("duration_secs")}
missing = []
for s in segs:
    g = by_prompt.get(s["text"].strip())
    out = os.path.join(d, s["id"] + ".mp3")
    if g is None:
        if not os.path.exists(out):
            missing.append(s["id"])
        continue
    subprocess.run(["curl", "-sS", "-o", out, g["content_url"]], check=True)
    print(f"  {s['id']:10s} {g.get('duration_secs')}s -> {out}")
print("eksik:", missing)
