"""template_gm.html = baş (stil) + gm_body.html + ortak yardımcı JS + gm_app.js"""
import sys
t = open("template_gm.html", encoding="utf-8").read().split("\n")
i_wrap = t.index('<div class="wrap">')
i_js = t.index("<script>", i_wrap)
i_app = t.index("/* KPIs */", i_js)
i_end = max(i for i, l in enumerate(t) if l == "</script>")
head, helpers, tail = t[:i_wrap], t[i_js:i_app], t[i_end:]
body = open("gm_body.html", encoding="utf-8").read().rstrip("\n").split("\n")
app = open("gm_app.js", encoding="utf-8").read().rstrip("\n").split("\n")
if app[-1] == "</script>":
    app = app[:-1]
open("template_gm.html", "w", encoding="utf-8").write("\n".join(head + body + helpers + app + tail))
print("ok", len(head), len(body), len(helpers), len(app), len(tail))
