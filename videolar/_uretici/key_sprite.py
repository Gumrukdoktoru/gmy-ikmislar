import numpy as np, cv2, sys
from PIL import Image
src = np.array(Image.open(sys.argv[1]).convert('RGB')).astype(np.float32)
bg = np.array([20,40,99], np.float32)
d = np.sqrt(((src-bg)**2).sum(-1))
print('bg d pct', np.percentile(d[:40,:200], [50,90,99,100]))
T = float(sys.argv[4]) if len(sys.argv)>4 else 18
cand = (d < T).astype(np.uint8)
n, lab = cv2.connectedComponents(cand, connectivity=4)
border = set(np.unique(np.concatenate([lab[0,:],lab[-1,:],lab[:,0],lab[:,-1]])).tolist()) - {0}
bgmask = np.isin(lab, list(border)).astype(np.uint8)
# close small specks
bgmask = cv2.morphologyEx(bgmask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
fg = 1 - bgmask
# remove tiny fg islands
n2, lab2, stats, _ = cv2.connectedComponentsWithStats(fg.astype(np.uint8), connectivity=8)
keep = np.zeros(n2, bool); keep[1:] = stats[1:, cv2.CC_STAT_AREA] > 4000
fg = keep[lab2].astype(np.float32)
# erode 1px then feather
fg = cv2.erode(fg, np.ones((3,3),np.uint8), iterations=1)
a = cv2.GaussianBlur(fg, (0,0), 1.2)
aa = np.clip(a,1e-3,1)[...,None]
col = np.clip((src - (1-aa)*bg)/aa, 0, 255)
rgba = np.dstack([col, a*255]).astype(np.uint8)
colmask = (a>0.5).any(0)
xs = np.where(colmask)[0]
groups=[]; start=xs[0]; prev=xs[0]
for x in xs[1:]:
    if x-prev>40: groups.append((start,prev)); start=x
    prev=x
groups.append((start,prev))
names = sys.argv[3].split(',')
print(len(groups), groups)
for (x0,x1),nm in zip(groups,names):
    sub = rgba[:, max(0,x0-12):x1+12]
    rows = np.where((sub[...,3]>128).any(1))[0]
    sub = sub[max(0,rows[0]-12):min(sub.shape[0],rows[-1]+8)]
    Image.fromarray(sub).save(f"{sys.argv[2]}/{nm}.png")
    print(nm, sub.shape)
