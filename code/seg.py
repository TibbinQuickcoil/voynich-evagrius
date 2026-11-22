import cv2,numpy as np,sys
from scipy.signal import find_peaks
def load(path):
    im=cv2.imread(path); g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY).astype(np.float32)
    bg=cv2.medianBlur(g.astype(np.uint8),51).astype(np.float32)+1
    n=np.clip(g/bg,0,1.2)                       # flatten parchment illumination
    ink=(n<0.80).astype(np.uint8)
    # parchment region: bright area bounding box, shrink a bit
    page=(cv2.GaussianBlur(g,(0,0),15)>110).astype(np.uint8)
    cnts,_=cv2.findContours(page,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    x,y,w,h=cv2.boundingRect(max(cnts,key=cv2.contourArea))
    m=np.zeros_like(ink); m[y+int(.03*h):y+int(.97*h), x+int(.04*w):x+int(.97*w)]=1
    return im,ink*m
def components(ink):
    n,lab,st,cen=cv2.connectedComponentsWithStats(ink,8)
    comps=[]
    for i in range(1,n):
        x,y,w,h,a=st[i]
        if a<6: continue                            # specks
        if h>32 or w>60 or (w>30 and h>28): continue   # stars, drawings, cross-line merges
        comps.append(dict(x=x,y=y,w=w,h=h,a=a,cy=cen[i][1],id=i))
    return lab,comps
def lines(comps,H):
    prof=np.zeros(H)
    for c in comps: prof[int(c['cy'])]+=c['a']
    prof=np.convolve(prof,np.ones(9)/9,'same')
    pk,_=find_peaks(prof,distance=22,height=prof.max()*0.06)
    rows=[[] for _ in pk]
    for c in comps:
        j=int(np.argmin(abs(pk-c['cy'])))
        if abs(pk[j]-c['cy'])<14: rows[j].append(c)
    return pk,[sorted(r,key=lambda c:c['x']) for r in rows]
def blobs(row):
    out=[]
    for c in row:                                   # merge fragments that overlap horizontally
        if out:
            b=out[-1]; ov=min(b['x']+b['w'],c['x']+c['w'])-max(b['x'],c['x'])
            if ov>0.5*min(b['w'],c['w']):
                x0=min(b['x'],c['x']); x1=max(b['x']+b['w'],c['x']+c['w']); y0=min(b['y'],c['y']); y1=max(b['y']+b['h'],c['y']+c['h'])
                b.update(x=x0,y=y0,w=x1-x0,h=y1-y0,parts=b['parts']+[c['id']]); continue
        out.append(dict(x=c['x'],y=c['y'],w=c['w'],h=c['h'],parts=[c['id']]))
    return out
def words(bl,thr):
    ws=[];cur=[]
    for b in bl:
        if cur and b['x']-(cur[-1]['x']+cur[-1]['w'])>thr: ws.append(cur); cur=[]
        cur.append(b)
    if cur: ws.append(cur)
    return ws
def mainblock(cm,W):
    col=np.zeros(W)
    for c in cm: col[c['x']:c['x']+c['w']]+=c['h']
    col=np.convolve(col,np.ones(25)/25,'same'); on=col>0.15*np.median(col[col>0])
    best=(0,0,0);s0=None
    for i,v in enumerate(list(on)+[False]):
        if v and s0 is None: s0=i
        if not v and s0 is not None:
            if i-s0>best[0]: best=(i-s0,s0,i)
            s0=None
    return [c for c in cm if c['x']>=best[1] and c['x']+c['w']<=best[2]]
def page(path):
    im,ink=load(path); lab,cm=components(ink); cm=mainblock(cm,ink.shape[1]); pk,rows=lines(cm,ink.shape[0])
    rows=[blobs(r) for r in rows if len(r)>=4]
    gaps=[b['x']-(a['x']+a['w']) for r in rows for a,b in zip(r,r[1:])]
    gaps=np.array([g for g in gaps if g>-5])
    # word-gap threshold: valley between intra-word and inter-word gaps
    hist=np.bincount(np.clip(gaps,0,40).astype(int),minlength=41).astype(float)
    sm=np.convolve(hist,np.ones(3)/3,'same')
    thr=3+int(np.argmin(sm[3:13]))+0.5              # valley between letter gaps and word gaps
    lines_=[words(r,thr) for r in rows]
    return im,ink,lab,lines_,thr
if __name__=='__main__':
    im,ink,lab,L,thr=page(sys.argv[1]); print("gap thr",thr,"lines",len(L),"words",sum(map(len,L)),"per line",[len(l) for l in L])
    vis=im.copy()
    for l in L:
        for w in l:
            x0=min(b['x'] for b in w); x1=max(b['x']+b['w'] for b in w); y0=min(b['y'] for b in w); y1=max(b['y']+b['h'] for b in w)
            cv2.rectangle(vis,(x0,y0),(x1,y1),(0,0,255),1)
    cv2.imwrite(sys.argv[2],vis[150:700,100:1080])
