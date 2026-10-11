import numpy as np, wave, sys, os
SR=44100
OUT=sys.argv[1]
def save(name, x):
    x=np.asarray(x,dtype=np.float64)
    if x.ndim==1: x=np.stack([x,x],1)
    peak=np.max(np.abs(x))+1e-9
    if peak>0.99: x=x/peak*0.99
    y=(x*32767).astype(np.int16)
    with wave.open(os.path.join(OUT,name),'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(y.tobytes())
def t(d): return np.arange(int(d*SR))/SR
def env_ad(n,a,d):
    tt=np.arange(n)/SR; e=np.minimum(1,tt/max(a,1e-4))*np.exp(-np.maximum(0,tt-a)/d); return e
rng=np.random.default_rng(7)
def lp(x,cut):
    # one-pole lowpass
    a=np.exp(-2*np.pi*cut/SR); y=np.zeros_like(x); s=0.0
    for i in range(len(x)): s=(1-a)*x[i]+a*s; y[i]=s
    return y
# --- SFX ---
# tick / tock
for nm,f in [('tick.wav',2200),('tock.wav',1600)]:
    n=int(0.09*SR); tt=np.arange(n)/SR
    x=(np.sin(2*np.pi*f*tt)*0.6+np.sin(2*np.pi*f*2.7*tt)*0.25)*np.exp(-tt/0.012)
    x+= rng.standard_normal(n)*np.exp(-tt/0.004)*0.3
    save(nm, x*0.7)
# correct ding (two notes)
tt=t(1.6); x=np.zeros_like(tt)
for st,f0 in [(0,1046.5),(0.11,1568.0)]:
    m=tt>=st; u=tt[m]-st
    for k,amp,dec in [(1,1,0.9),(2.0,0.35,0.5),(3.01,0.18,0.3),(4.2,0.08,0.2)]:
        x[m]+=amp*np.sin(2*np.pi*f0*k*u)*np.exp(-u/dec)
x*=np.minimum(1,tt/0.004); save('ding.wav', x*0.35)
# trap buzzer (two low pulses)
tt=t(0.9); x=np.zeros_like(tt)
for st in [0,0.32]:
    m=(tt>=st)&(tt<st+0.26); u=tt[m]-st
    f=150-60*u/0.26
    ph=2*np.pi*np.cumsum(f)/SR
    sq=np.tanh(3*np.sin(ph))+0.3*np.tanh(3*np.sin(2*ph+0.5))
    x[m]+=sq*np.minimum(1,u/0.01)*np.minimum(1,(0.26-u)/0.03)
x=lp(x,1800); save('trap.wav', x*0.32)
# warning two-tone
tt=t(0.7); x=np.zeros_like(tt)
for st,f in [(0,880),(0.22,660)]:
    m=(tt>=st)&(tt<st+0.2); u=tt[m]-st
    x[m]+=(np.sin(2*np.pi*f*u)+0.3*np.sin(2*np.pi*2*f*u))*np.minimum(1,u/0.01)*np.minimum(1,(0.2-u)/0.04)
save('warn.wav', x*0.22)
# important chime (soft rising)
tt=t(1.0); x=np.zeros_like(tt)
for st,f0 in [(0,784),(0.08,988),(0.16,1175)]:
    m=tt>=st; u=tt[m]-st
    x[m]+=np.sin(2*np.pi*f0*u)*np.exp(-u/0.35)+0.2*np.sin(2*np.pi*2*f0*u)*np.exp(-u/0.2)
x*=np.minimum(1,tt/0.003); save('chime.wav', x*0.25)
# whoosh
n=int(0.6*SR); tt=np.arange(n)/SR
nz=rng.standard_normal(n)
cut=300+5000*np.sin(np.pi*tt/0.6)**2
y=np.zeros(n); s=0.0
for i in range(n):
    a=np.exp(-2*np.pi*cut[i]/SR); s=(1-a)*nz[i]+a*s; y[i]=s
y=y-lp(y,250)
e=np.sin(np.pi*tt/0.6)**1.5
save('whoosh.wav', y*e*0.9)
# pop
n=int(0.12*SR); tt=np.arange(n)/SR
f=500+700*tt/0.12; ph=2*np.pi*np.cumsum(f)/SR
save('pop.wav', np.sin(ph)*np.exp(-tt/0.03)*0.45)
# stamp/thud for answer reveal
n=int(0.35*SR); tt=np.arange(n)/SR
f=120*np.exp(-tt/0.08)+50; ph=2*np.pi*np.cumsum(f)/SR
x=np.sin(ph)*np.exp(-tt/0.09)+rng.standard_normal(n)*np.exp(-tt/0.01)*0.2
save('thud.wav', x*0.6)
# --- MUSIC BED (lo-fi pad loop) ---
bpm=84; beat=60/bpm; bar=4*beat
chords=[[57,60,64,67,71],[53,57,60,64,69],[48,55,60,64,67],[55,59,62,67,69]]  # Am9, Fmaj7(add9-ish), Cadd, G6
loop_bars=8; L=int(loop_bars*bar*SR)
mus=np.zeros((L,2))
def mtof(m): return 440*2**((m-69)/12)
tt=np.arange(L)/SR
for ci,ch in enumerate(chords):
    st=ci*2*bar; en=st+2*bar
    m=(tt>=st-0.3)&(tt<en+0.6); u=tt[m]-st
    env=np.clip((u+0.3)/0.9,0,1)*np.clip((2*bar+0.6-u)/0.9,0,1)
    for note in ch:
        f=mtof(note)
        for det,pan in [(-0.12,0.3),(0.12,0.7)]:
            fr=f*2**(det/12/8)
            w=np.sin(2*np.pi*fr*u)+0.25*np.sin(2*np.pi*2*fr*u)+0.08*np.sin(2*np.pi*3*fr*u)
            mus[m,0]+=w*env*(1-pan)*0.035; mus[m,1]+=w*env*pan*0.035
    # bass
    f=mtof(ch[0]-12)
    for b in range(8):
        bs=st+b*beat
        mm=(tt>=bs)&(tt<bs+beat*0.95); uu=tt[mm]-bs
        if b%2==0:
            bw=np.sin(2*np.pi*f*uu)*np.exp(-uu/0.5)*0.16
            mus[mm,0]+=bw; mus[mm,1]+=bw
    # EP arpeggio 8ths
    arp=[ch[1]+12,ch[2]+12,ch[3]+12,ch[4]+12,ch[3]+12,ch[2]+12,ch[1]+12,ch[2]+12]
    for k in range(16):
        ns=st+k*beat/2
        if k%4==3: continue
        nn=arp[k%8]; f=mtof(nn)
        mm=(tt>=ns)&(tt<ns+1.2); uu=tt[mm]-ns
        w=(np.sin(2*np.pi*f*uu)+0.3*np.sin(2*np.pi*2*f*uu)*np.exp(-uu/0.15))*np.exp(-uu/0.45)*np.minimum(1,uu/0.005)*0.045
        p=0.35+0.3*((k*37)%10)/10
        mus[mm,0]+=w*(1-p); mus[mm,1]+=w*p
# drums
for b in range(loop_bars*4):
    bs=b*beat
    if b%4 in (0,2) or (b%8==7):
        n=int(0.3*SR); u=np.arange(n)/SR; f=110*np.exp(-u/0.05)+45
        k=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-u/0.12)*0.22
        i0=int(bs*SR); mus[i0:i0+n,:]+=k[:min(n,L-i0),None]
    if b%4 in (1,3):
        n=int(0.18*SR); u=np.arange(n)/SR
        sn=rng.standard_normal(n); sn=sn-lp(sn,1200)
        s=sn*np.exp(-u/0.05)*0.05
        i0=int(bs*SR); mus[i0:i0+n,:]+=s[:min(n,L-i0),None]
    for h in (0.5,):
        hs=bs+h*beat; n=int(0.05*SR); u=np.arange(n)/SR
        hn=rng.standard_normal(n); hn=hn-lp(hn,6000)
        i0=int(hs*SR); mus[i0:i0+n,:]+=(hn*np.exp(-u/0.012)*0.03)[:min(n,L-i0),None]
# soft vinyl noise
vn=rng.standard_normal(L); vn=lp(vn,2500)*0.004
mus+=vn[:,None]
# gentle lowpass for warmth
mus[:,0]=lp(mus[:,0],5000); mus[:,1]=lp(mus[:,1],5000)
save('bed_loop.wav', mus*1.4)
print('done', L/SR)
