import sys,pickle,numpy as np,collections,cv2; sys.path.insert(0,'/home/claude/virgin'); sys.path.insert(0,'/home/claude/v3')
from seg import page
from boxes import load_boxes
D='/home/claude/scans/atlas/images/web/'
pca,km=pickle.load(open('/home/claude/v2/rec_model.pkl','rb'))
sys.path.insert(0,'/home/claude/v2'); from feats2 import blob_feats
def machine_words(p):
    im,ink,lab,L,thr=page(D+p+'.jpg')
    L=[[w for w in l if not all(b['h']<6 and b['w']<6 for b in w)] for l in L]; L=[l for l in L if len(l)>=2]
    out=[]
    for li,l in enumerate(L):
        for wi,w in enumerate(l):
            V=np.array([blob_feats(lab,b) for b in w]); c=km.predict(pca.transform(V))
            order=np.argsort([b['x'] for b in w])
            x0=min(b['x'] for b in w); x1=max(b['x']+b['w'] for b in w); y0=min(b['y'] for b in w); y1=max(b['y']+b['h'] for b in w)
            parts=[q for b in w for q in b['parts']]
            crop=np.isin(lab[y0:y1,x0:x1],parts).astype(np.float32)
            hh=24; ww=max(4,int(round(crop.shape[1]*hh/max(1,crop.shape[0]))))
            img=cv2.resize(crop,(ww,hh),interpolation=cv2.INTER_AREA)
            out.append(dict(img=img,line=li,word=wi,nline=len(l),x0=min(b['x'] for b in w),x1=max(b['x']+b['w'] for b in w),
                            y0=min(b['y'] for b in w),y1=max(b['y']+b['h'] for b in w),sp=''.join(chr(0x4E00+c[k]) for k in order)))
    return out
def iou_score(M,E,s,dx,dy):
    mb=np.array([[m['x0'],m['y0'],m['x1'],m['y1']] for m in M],float)
    eb=np.array([[e['x'],e['y'],e['x']+e['w_'],e['y']+e['h']] for e in E],float)*s+[dx,dy,dx,dy]
    ix=np.clip(np.minimum(eb[:,None,2],mb[None,:,2])-np.maximum(eb[:,None,0],mb[None,:,0]),0,None)
    iy=np.clip(np.minimum(eb[:,None,3],mb[None,:,3])-np.maximum(eb[:,None,1],mb[None,:,1]),0,None)
    inter=ix*iy; ua=((eb[:,2]-eb[:,0])*(eb[:,3]-eb[:,1]))[:,None]+((mb[:,2]-mb[:,0])*(mb[:,3]-mb[:,1]))[None,:]-inter
    return (inter/ua).max(1).mean()
def fit(M,E):
    b=fit0(M,E); _,s0,dx0,dy0=b; best=None
    for s in np.arange(s0-0.06,s0+0.061,0.02):
        for ddy in range(-60,61,4):
            for ddx in range(-30,31,6):
                sc=iou_score(M,E,s,dx0+ddx,dy0+ddy)
                if best is None or sc>best[0]: best=(sc,s,dx0+ddx,dy0+ddy)
    sc,s,dx,dy=best                                   # fine pass
    for s2 in np.arange(s-0.01,s+0.011,0.005):
        for d2y in range(-3,4):
            for d2x in range(-4,5,2):
                v=iou_score(M,E,s2,dx+d2x,dy+d2y)
                if v>best[0]: best=(v,s2,dx+d2x,dy+d2y)
    return best
def fit0(M,E):
    mc=np.array([[(m['x0']+m['x1'])/2,(m['y0']+m['y1'])/2] for m in M]); ec=np.array([[e['x']+e['w_']/2,e['y']+e['h']/2] for e in E])
    best=None
    for s in np.arange(1.25,1.70,0.01):
        dx=np.median(mc[:,0])-s*np.median(ec[:,0]); dy=np.median(mc[:,1])-s*np.median(ec[:,1])
        for _ in range(6):                              # nearest-neighbour refinement
            P=ec*s+[dx,dy]; d=((P[:,None,:]-mc[None,:,:])**2).sum(-1); j=d.argmin(1)
            r=mc[j]-P; dx+=np.median(r[:,0]); dy+=np.median(r[:,1])
        P=ec*s+[dx,dy]; inside=sum(any(m['x0']-3<=x<=m['x1']+3 and m['y0']-3<=y<=m['y1']+3 for m in M) for x,y in P)
        if best is None or inside>best[0]: best=(inside,s,dx,dy)
    return best
def pairs(p):
    M=machine_words(p); E=load_boxes(p); inside,s,dx,dy=fit(M,E)
    hits=collections.defaultdict(list); owner={}
    for k,e in enumerate(E):
        x=(e['x']+e['w_']/2)*s+dx; y=(e['y']+e['h']/2)*s+dy
        for i,m in enumerate(M):
            if m['x0']-3<=x<=m['x1']+3 and m['y0']-3<=y<=m['y1']+3: hits[i].append(k); owner[k]=i; break
    P=[]
    for i,ks in hits.items():
        if len(ks)==1: e=E[ks[0]]; P.append(dict(eva=e['w'],ex=(e['x']+e['w_']/2)*s+dx,ey=(e['y']+e['h']/2)*s+dy,**M[i]))
    return P,inside,len(E),len(M)
if __name__=='__main__':
    REC=[f"f{n}{s}" for n in range(103,117) for s in 'rv' if f"f{n}{s}" not in ('f111r','f111v','f116v')]
    import glob,os
    REC=[p for p in REC if os.path.exists(D+p+'.jpg') and os.path.exists('/home/claude/zl/vu/data/voynich-units/morphometry_voynichese/voynichese_boxes/'+p+'.js')]
    allp={}
    for p in REC:
        P,cov,ne,nm=pairs(p); allp[p]=P
        print(f"{p:6s} mean IoU {cov*len(E) if False else 0:.0f}  clean 1:1 pairs {len(P):4d}")
    pickle.dump(allp,open('pairs.pkl','wb'))
    print("total clean pairs",sum(map(len,allp.values())))
