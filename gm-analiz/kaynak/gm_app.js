/* KPIs */
const GRUPLAR=Object.keys(L.grup);
const GCOL=g=>SER[GRUPLAR.indexOf(g)];
(function(){
  const kc=count(Q,"konu");const top=Object.entries(kc).sort((a,b)=>b[1]-a[1])[0];
  const kok=count(Q,"kok"), tc=count(Q,"tip"), mv=count(Q,"mevzuat");
  const tar=Q.filter(q=>q.konu==="GM_TARIFE_SINIF").length, hes=Q.filter(q=>q.tip==="HESAPLAMA").length;
  const k=[
    {v:"500",l:"soru, 5 sınav (2021–2025), tamamı mesleki"},
    {v:`${top[1]}<small> soru</small>`,l:`en çok soru gelen konu: ${L.konu[top[0]]}`},
    {v:`%${pct(tar,Q.length)}`,l:`tarife sınıflandırma sorusu (${tar} soru)`},
    {v:`%${pct(hes,Q.length)}`,l:`hesap sorusu: kıymet, KDV, ÖTV, ceza (${hes} soru)`},
    {v:`%${pct(kok.OLUMSUZ||0,Q.length)}`,l:`olumsuz köklü soru ("değildir / yanlıştır")`},
    {v:`%${pct(mv.GK_4458||0,Q.length)}`,l:"doğrudan Gümrük Kanunu'na dayanan soru; ağırlık yönetmelik ve tebliğlerde"},
  ];
  $("#kpis").innerHTML=k.map(x=>`<div class="kpi"><span class="v">${x.v}</span><span class="l">${esc(x.l)}</span></div>`).join("");
})();

/* optik form */
(function(){
  let h=`<div class="oaxis"><span></span>${Array.from({length:100},(_,i)=>`<span${i===99?' style="text-align:right;direction:rtl"':""}>${(i+1)%10===1&&i<91||i===99?i+1:""}</span>`).join("")}</div>`;
  Y.forEach(y=>{
    const qs=byYear(y).sort((a,b)=>a.n-b.n);
    h+=`<div class="orow"><span class="yl">${y}${y===2022?"<sup>B</sup>":""}</span>${qs.map(q=>{const g=L.konu2grup[q.konu];
      return `<span class="ob" tabindex="0" style="background:${GCOL(g)}" data-tip="<b>${y} · Soru ${q.n}</b> (cevap ${q.cevap})<br>${esc(g)} › ${esc(L.konu[q.konu])}<br><span style='opacity:.8'>${esc(q.alt_konu)}</span>"></span>`}).join("")}</div>`;
  });
  $("#optik").innerHTML=h;
  $("#optik-legend").innerHTML=GRUPLAR.map((g,i)=>`<span><i style="background:${SER[i]}"></i>${esc(g)}</span>`).join("");
  const gc={};Q.forEach(q=>{const g=L.konu2grup[q.konu];gc[g]=(gc[g]||0)+1});
  hbars($("#grp-avg"),GRUPLAR.map(g=>({l:g,v:gc[g]/Y.length,vl:fmt(gc[g]/Y.length),c:GCOL(g),tip:`<b>${esc(g)}</b><br>5 yılda ${gc[g]} soru · yılda ort. ${fmt(gc[g]/Y.length)}<br>${L.grup[g].map(k=>esc(L.konu[k])).join(", ")}`})).sort((a,b)=>b.v-a.v),{lw:"58%"});
  const blok=[
    {l:"Tarife sınıflandırma",f:q=>q.konu==="GM_TARIFE_SINIF"},
    {l:"Hesap soruları",f:q=>q.tip==="HESAPLAMA"},
    {l:"İç vergiler, kambiyo & fonlar",f:q=>L.konu2grup[q.konu]==="İç Vergiler, Kambiyo & Fonlar"},
  ].map(b=>({l:b.l,m:Object.fromEntries(Y.map(y=>[y,byYear(y).filter(b.f).length]))}));
  heat($("#bloklar"),blok,{rowHead:"Blok",max:20,extra:{n:1,head:`<th class="c">Ort.</th>`,row:r=>`<td class="tot">${fmt(Y.reduce((s,y)=>s+r.m[y],0)/Y.length)}</td>`}});
  $("#bloklar").insertAdjacentHTML("beforeend",`<p class="cap">Her yıl 100 sorunun yaklaşık üçte biri bu üç bloktan geliyor. GMY sınavında bu alanlar neredeyse hiç sorulmuyor.</p>`);
})();

/* yıl panelleri */
function renderYear(y,p=$("#ypanel"),pr=false){
  const qs=byYear(y);
  const kc=count(qs,"konu"), kok=count(qs,"kok"), tc=count(qs,"tip"), mc=count(qs,"mevzuat"), zc=count(qs,"zorluk"), ac=count(qs,"cevap");
  const topK=Object.entries(kc).sort((a,b)=>b[1]-a[1]);
  const tar=qs.filter(q=>q.konu==="GM_TARIFE_SINIF"), hes=qs.filter(q=>q.tip==="HESAPLAMA");
  const fas={};qs.forEach(q=>(q.fasil||[]).forEach(f=>fas[f]=(fas[f]||0)+1));
  const hc=count(hes,"hesap");
  const ins=(INS.years&&INS.years[y])||[];
  p.innerHTML=`${pr?`<h2 class="pyh">${y} sınavı${y===2022?" (B kitapçığı)":""}</h2>`:""}
  <div class="kpis k4">
    <div class="kpi"><span class="v">${topK[0][1]}<small> soru</small></span><span class="l">en çok: ${esc(L.konu[topK[0][0]])}</span></div>
    <div class="kpi"><span class="v">${tar.length}<small> soru</small></span><span class="l">tarife sınıflandırma · ${Object.keys(fas).length} farklı fasıl</span></div>
    <div class="kpi"><span class="v">${hes.length}<small> soru</small></span><span class="l">hesap sorusu</span></div>
    <div class="kpi"><span class="v">%${pct(kok.OLUMSUZ||0,100)}</span><span class="l">olumsuz kök · öncüllü ${kok.ONCULLU||0} soru</span></div>
  </div>
  <div class="callout"><h3 style="margin-bottom:6px">${y} sınavı yorumu</h3><ul class="notes">${ins.map(t=>`<li>${t}</li>`).join("")}</ul></div>
  <div class="grid2">
    <div class="card"><h3>Konular (${y}, 100 soru)</h3><div class="y-konu"></div></div>
    <div class="card" style="gap:16px"><div style="display:flex;flex-direction:column;gap:10px"><h3>Soru kalıbı</h3><div class="y-kok"></div></div>
      <div style="display:flex;flex-direction:column;gap:10px"><h3>Soru tipi</h3><div class="y-tip"></div></div></div>
  </div>
  <div class="grid3">
    <div class="card"><h3>Mevzuat kaynağı</h3><div class="y-mev"></div></div>
    <div class="card"><h3>Fasıllar ve hesaplar</h3><div class="y-fas"></div></div>
    <div class="card"><h3>Zorluk ve doğru şık</h3><div class="y-zor"></div><div class="y-sik"></div></div>
  </div>`;
  hbars(p.querySelector(".y-konu"),topK.map(([k,v])=>({l:L.konu[k],v,c:GCOL(L.konu2grup[k]),tip:`<b>${esc(L.konu[k])}</b><br>${v} soru · soru no: ${qs.filter(q=>q.konu===k).map(q=>q.n).join(", ")}`})),{lw:"58%"});
  hbars(p.querySelector(".y-kok"),L.kok_order.filter(k=>kok[k]).map(k=>({l:L.kok[k],v:kok[k],c:SER[L.kok_order.indexOf(k)]})),{lw:"52%"});
  hbars(p.querySelector(".y-tip"),Object.entries(tc).sort((a,b)=>b[1]-a[1]).map(([k,v])=>({l:L.tip[k],v})),{lw:"52%"});
  hbars(p.querySelector(".y-mev"),Object.entries(mc).sort((a,b)=>b[1]-a[1]).map(([k,v])=>({l:L.mevzuat[k],v})),{lw:"55%"});
  const fl=Object.keys(fas).sort((a,b)=>a-b);
  p.querySelector(".y-fas").innerHTML=`<p class="cap" style="margin:0">Sorulan fasıllar</p><div class="chips">${fl.map(f=>`<span class="chip" data-tip="Fasıl ${f}: ${fas[f]} soru">${f}${fas[f]>1?`<b>×${fas[f]}</b>`:""}</span>`).join("")||"—"}</div>
    <p class="cap" style="margin:10px 0 0">Hesap türleri</p><div class="chips">${Object.entries(hc).sort((a,b)=>b[1]-a[1]).map(([k,v])=>`<span class="chip">${esc(L.hesap[k]||k)} <b>×${v}</b></span>`).join("")||"—"}</div>`;
  hbars(p.querySelector(".y-zor"),["KOLAY","ORTA","ZOR"].map((k,i)=>({l:L.zorluk[k],v:zc[k]||0,c:["var(--h3)","var(--h5)","var(--h7)"][i]})),{lw:"30%",max:100});
  p.querySelector(".y-sik").innerHTML=`<p class="cap" style="margin-top:8px">Doğru şık dağılımı: ${["A","B","C","D","E"].map(s=>`<b class="mono">${s}</b> ${ac[s]||0}`).join(" · ")}</p>`;
}
(function(){
  const tabs=$("#ytabs");
  tabs.innerHTML=Y.map((y,i)=>`<button class="tab" role="tab" id="t${y}" aria-selected="${i===Y.length-1}" data-y="${y}">${y}</button>`).join("");
  tabs.addEventListener("click",e=>{const b=e.target.closest(".tab");if(!b)return;tabs.querySelectorAll(".tab").forEach(t=>t.setAttribute("aria-selected",t===b));renderYear(+b.dataset.y);try{localStorage.setItem("gm-yil",b.dataset.y)}catch(_){}} );
  let start=Y[Y.length-1];try{const s=+localStorage.getItem("gm-yil");if(Y.includes(s))start=s}catch(_){}
  tabs.querySelectorAll(".tab").forEach(t=>t.setAttribute("aria-selected",+t.dataset.y===start));
  renderYear(start);
  Y.forEach(y=>{const d=document.createElement("div");d.className="yprint";$("#ypanel-all").appendChild(d);renderYear(y,d,true)});
})();

/* karşılaştırma */
(function(){
  const stat=Object.keys(L.konu).map(k=>{const m={};Y.forEach(y=>m[y]=Q.filter(q=>q.yil===y&&q.konu===k).length);const tot=Y.reduce((s,y)=>s+m[y],0);const early=(m[Y[0]]+m[Y[1]])/2,late=(m[Y[3]]+m[Y[4]])/2;return {k,l:L.konu[k],m,tot,avg:tot/Y.length,yrs:Y.filter(y=>m[y]>0).length,early,late,g:L.konu2grup[k]}}).filter(r=>r.tot>0).sort((a,b)=>b.tot-a.tot||a.l.localeCompare(b.l,"tr"));
  DATA._stat=stat;
  heat($("#hm-konu"),stat,{extra:{n:4,head:`<th class="c">Toplam</th><th class="c">Ort./yıl</th><th class="c">Yıl</th><th class="c">Eğilim</th>`,row:r=>{const d=r.late-r.early;const cls=d>=1?"up":d<=-1?"dn":"eq";const sym=d>=1?"▲":d<=-1?"▼":"■";return `<td class="tot">${r.tot}</td><td class="tot">${fmt(r.avg)}</td><td class="tot">${r.yrs}/5</td><td class="c"><span class="trend ${cls}" data-tip="2021–22 ort. ${fmt(r.early)} → 2024–25 ort. ${fmt(r.late)}">${sym} ${d>0?"+":""}${fmt(d)}</span></td>`}}});
  hbars($("#top-konu"),stat.slice(0,15).map(r=>({l:r.l,v:r.tot,c:GCOL(r.g),tip:`<b>${esc(r.l)}</b><br>5 yılda ${r.tot} soru · yılda ort. ${fmt(r.avg)}<br>${Y.map(y=>y+": "+r.m[y]).join(" · ")}`})),{lw:"56%"});
  const grows=Y.map(y=>{const m={};byYear(y).forEach(q=>{const g=L.konu2grup[q.konu];m[g]=(m[g]||0)+1});return {l:y,m}});
  stack100($("#stk-grup"),grows,GRUPLAR,Object.fromEntries(GRUPLAR.map(g=>[g,g])),$("#lg-grup"));
  stack100($("#stk-kok"),Y.map(y=>({l:y,m:count(byYear(y),"kok")})),L.kok_order,L.kok,$("#lg-kok"));
  const sorted=(keys,field,names)=>keys.filter(k=>Q.some(q=>q[field]===k)).map(k=>({l:names[k],m:Object.fromEntries(Y.map(y=>[y,byYear(y).filter(q=>q[field]===k).length]))})).sort((a,b)=>Y.reduce((s,y)=>s+b.m[y],0)-Y.reduce((s,y)=>s+a.m[y],0));
  const tot={n:1,head:`<th class="c">Toplam</th>`,row:r=>`<td class="tot">${Y.reduce((s,y)=>s+r.m[y],0)}</td>`};
  heat($("#hm-tip"),sorted(L.tip_order,"tip",L.tip),{rowHead:"Tip",extra:tot});
  heat($("#hm-mev"),sorted(L.mevzuat_order,"mevzuat",L.mevzuat),{rowHead:"Mevzuat",extra:tot});
  stack100($("#stk-zor"),Y.map(y=>({l:y,m:count(byYear(y),"zorluk")})),["KOLAY","ORTA","ZOR"],L.zorluk,$("#lg-zor"),{colors:["var(--h3)","var(--h5)","var(--h7)"],inks:["var(--h-ink-lo)","var(--h-ink-hi)","var(--h-ink-hi)"]});
  heat($("#hm-sik"),["A","B","C","D","E"].map(s=>({l:"Şık "+s,m:Object.fromEntries(Y.map(y=>[y,byYear(y).filter(q=>q.cevap===s).length]))})),{rowHead:"Doğru şık",max:30});
  const dd=stat.filter(r=>Math.abs(r.late-r.early)>=1).sort((a,b)=>(b.late-b.early)-(a.late-a.early));
  const W=580,rowH=26,top=26,left=262,right=24,H=top+dd.length*rowH+10;const mx=Math.max(...dd.flatMap(r=>[r.early,r.late]),1);
  const x=v=>left+(W-left-right)*v/Math.ceil(mx);
  let svg=`<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Yükselen ve düşen konular">`;
  for(let t=0;t<=Math.ceil(mx);t+=Math.ceil(mx)>12?2:1){svg+=`<line x1="${x(t)}" x2="${x(t)}" y1="${top-6}" y2="${H-6}" stroke="var(--line)" stroke-width="1"/><text x="${x(t)}" y="${top-12}" fill="var(--muted)" font-size="11" font-family="IBM Plex Mono,monospace" text-anchor="middle">${t}</text>`}
  dd.forEach((r,i)=>{const yy=top+i*rowH+rowH/2;const col=r.late>r.early?"var(--rise)":"var(--fall)";
    svg+=`<g data-tip="<b>${esc(r.l)}</b><br>2021–22 ort. ${fmt(r.early)} → 2024–25 ort. ${fmt(r.late)}"><rect x="0" y="${yy-rowH/2}" width="${W}" height="${rowH}" fill="transparent"/><text x="${left-10}" y="${yy+4}" fill="var(--ink)" font-size="12" text-anchor="end" font-family="IBM Plex Sans,system-ui,sans-serif">${esc(r.l.length>36?r.l.slice(0,35)+"…":r.l)}</text><line x1="${x(r.early)}" x2="${x(r.late)}" y1="${yy}" y2="${yy}" stroke="${col}" stroke-width="2"/><circle cx="${x(r.early)}" cy="${yy}" r="5" fill="var(--surface)" stroke="${col}" stroke-width="2"/><circle cx="${x(r.late)}" cy="${yy}" r="5.5" fill="${col}" stroke="var(--surface)" stroke-width="2"/></g>`});
  $("#dumb").innerHTML=svg+"</svg>";
})();

/* derinlemesine */
(function(){
  const fasRows=[];const fasAll={};
  Q.forEach(q=>(q.fasil||[]).forEach(f=>{fasAll[f]=fasAll[f]||{};fasAll[f][q.yil]=(fasAll[f][q.yil]||0)+1}));
  const bolumOf=f=>{const n=+f;const b=L.bolumler.find(b=>n>=b[2]&&n<=b[3]);return b?`${b[0]} · ${b[1]}`:"?"};
  Object.keys(fasAll).sort((a,b)=>a-b).forEach(f=>fasRows.push({g:bolumOf(f),l:"Fasıl "+f,m:fasAll[f]}));
  const fgs=[];fasRows.forEach(r=>{let g=fgs.find(x=>x.g===r.g);if(!g)fgs.push(g={g:r.g,rows:[]});g.rows.push(r)});
  $("#hm-fasil").innerHTML=fgs.map(g=>`<div class="fg"><div class="fgl">${esc(g.g)}</div><table class="hm fgt"><thead><tr><th>Fasıl</th>${Y.map(y=>`<th class="c">${String(y).slice(2)}</th>`).join("")}<th class="c">Σ</th></tr></thead><tbody>${g.rows.map(r=>`<tr><td class="rl">${esc(r.l.replace("Fasıl ",""))}</td>${Y.map(y=>{const v=r.m[y]||0;return `<td class="cell ${hcls(v,4)}" data-tip="<b>${esc(r.l)}</b><br>${y}: ${v} soru">${v||"·"}</td>`}).join("")}<td class="tot">${Y.reduce((s,y)=>s+(r.m[y]||0),0)}</td></tr>`).join("")}</tbody></table></div>`).join("");
  const bc={};fasRows.forEach(r=>{bc[r.g]=(bc[r.g]||0)+Y.reduce((s,y)=>s+(r.m[y]||0),0)});
  hbars($("#bolum-bar"),Object.entries(bc).sort((a,b)=>b[1]-a[1]).map(([k,v])=>({l:k,v,c:GCOL("Tarife & Sınıflandırma")})),{lw:"62%"});
  $("#tarife-not").innerHTML=INS.tarife_not||"";
  const hes=Q.filter(q=>q.tip==="HESAPLAMA");
  heat($("#hm-hesap"),Object.keys(L.hesap).filter(k=>hes.some(q=>q.hesap===k)).map(k=>({l:L.hesap[k],m:Object.fromEntries(Y.map(y=>[y,hes.filter(q=>q.yil===y&&q.hesap===k).length]))})).sort((a,b)=>Y.reduce((s,y)=>s+b.m[y],0)-Y.reduce((s,y)=>s+a.m[y],0)),{rowHead:"Hesaplanan",extra:{n:1,head:`<th class="c">Toplam</th>`,row:r=>`<td class="tot">${Y.reduce((s,y)=>s+r.m[y],0)}</td>`}});
  $("#hesap-not").innerHTML=INS.hesap_not||"";
  const C=DATA.gmy_cmp||[];const cm=Math.max(...C.flatMap(r=>[r.gm,r.gmy]),1);
  $("#gmy-cmp").innerHTML=`<div class="legend sq" style="margin-bottom:8px"><span><i style="background:var(--s1)"></i>GM (500 soru)</span><span><i style="background:var(--s2)"></i>GMY gümrük bölümü (400 soru)</span></div><div class="cmp">${C.map(r=>`<div class="cr" data-tip="<b>${esc(r.alan)}</b><br>GM: %${fmt(r.gm)} (${r.gm_n} soru)<br>GMY: %${fmt(r.gmy)} (${r.gmy_n} soru)"><span class="lab">${esc(r.alan)}</span><span class="bars"><span class="b1" style="width:${r.gm/cm*100}%"></span><span class="b2" style="width:${r.gmy/cm*100}%"></span></span><span class="val">%${fmt(r.gm)} · %${fmt(r.gmy)}</span></div>`).join("")}</div>`;
  const S=Q.filter(q=>q.tip==="SAYISAL"&&q.sayisal).sort((a,b)=>GRUPLAR.indexOf(L.konu2grup[a.konu])-GRUPLAR.indexOf(L.konu2grup[b.konu])||L.konu[a.konu].localeCompare(L.konu[b.konu],"tr")||a.yil-b.yil);
  let last=null;
  $("#sayisal").innerHTML=`<div class="tblwrap"><table class="st"><thead><tr><th>Değer</th><th>Bilgi</th><th class="c">Yıl/Soru</th></tr></thead><tbody>${S.map(q=>{let h="";if(q.konu!==last){last=q.konu;h=`<tr class="grp"><td colspan="3">${esc(L.konu[q.konu])}</td></tr>`}return h+`<tr><td class="sv">${esc(q.sayisal)}</td><td><b>${esc(q.alt_konu)}</b> · <span class="kb">${esc(q.anahtar_bilgi)}</span></td><td class="c mono">${q.yil}/${q.n}</td></tr>`}).join("")}</tbody></table></div>`;
  const T=INS.tekrar||[];
  $("#tekrar").innerHTML=`<div class="tblwrap"><table><thead><tr><th>Soru kalıbı</th><th>Konu</th>${Y.map(y=>`<th class="c">${y}</th>`).join("")}<th>Doğru bilgi</th></tr></thead><tbody>${T.map(t=>`<tr><td><b>${esc(t.kalip)}</b></td><td>${esc(L.konu[t.konu]||t.konu)}</td>${Y.map(y=>{const v=(t.sorular[y]||[]);return `<td class="c mono">${v.length?v.join(", "):"·"}</td>`}).join("")}<td class="kb">${esc(t.bilgi)}</td></tr>`).join("")}</tbody></table></div>`;
})();

/* sonuç */
(function(){
  const S=INS.sonuc||{};
  $("#sonuc-body").innerHTML=(S.paragraflar||[]).map(p=>`<div class="callout"><h3 style="margin-bottom:6px">${p.baslik}</h3><ul class="notes">${p.maddeler.map(m=>`<li>${m}</li>`).join("")}</ul></div>`).join("");
  const stat=DATA._stat;
  const t1=stat.filter(r=>r.avg>=5),t2=stat.filter(r=>r.avg>=2&&r.avg<5),t3=stat.filter(r=>r.avg<2);
  const tier=(c,t,s,arr)=>`<div class="tier" style="--c:${c}"><span class="pill ${t}">${s.badge}</span><h3>${s.title}</h3><span class="sub">${s.sub}</span><ol>${arr.map(r=>`<li>${esc(r.l)} <span class="mono" style="color:var(--muted)">${fmt(r.avg)}/yıl</span></li>`).join("")}</ol></div>`;
  $("#tiers").innerHTML=tier("var(--stamp)","p1",{badge:"ÖNCELİK 1",title:"Her yıl çok soru",sub:"Yılda ortalama 5 ve üzeri soru"},t1)+tier("var(--accent)","p2",{badge:"ÖNCELİK 2",title:"Düzenli gelen",sub:"Yılda ortalama 2–5 soru"},t2)+tier("var(--neutral-mark)","p3",{badge:"ÖNCELİK 3",title:"Ara sıra",sub:"Yılda ortalama 2'den az"},t3);
})();
</script>
