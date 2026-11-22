import sys,pickle,numpy as np,collections,cv2; sys.path.insert(0,'/home/claude/v2')
from common2 import zl_meta
import herbal
her=pickle.load(open('herbal_all.pkl','rb')); pca,km=pickle.load(open('rec_model.pkl','rb')); M=zl_meta()
rec=pickle.load(open('rec2.pkl','rb')); dR=np.min(km.transform(pca.transform(np.array([f['vec'] for d in rec.values() for f in d['feats']]))),1)
thr=np.percentile(dR,85); ok={}
for p,d in her.items():
    F=d['feats']
    if not F: continue
    dist=np.min(km.transform(pca.transform(np.array([f['vec'] for f in F]))),1)
    words=collections.defaultdict(list)
    for f,ds in zip(F,dist): words[(f['line'],f['word'])].append(ds<=thr)
    good={k for k,v in words.items() if np.mean(v)>=0.8}
    lines=collections.Counter(k[0] for k in good); gl={l for l,c in lines.items() if c>=4}
    keep=[f for f in F if (f['line'],f['word']) in good and f['line'] in gl]
    nw=len({(f['line'],f['word']) for f in keep}); z=herbal.zl_count(p)
    if z>=40 and 0.8<=nw/z<=1.25: ok[p]=dict(nwords=nw,feats=keep,L=M[p].get('L'),H=M[p].get('H'))
pickle.dump(ok,open('herbal_qc.pkl','wb'))
print(sorted(ok, key=lambda p:(int(p[1:-1]),p[-1])))
for p in [next(p for p in ok if ok[p]['L']=='A'), next(p for p in ok if ok[p]['L']=='B')]:
    im=cv2.imread(f'/home/claude/scans/atlas/images/web/{p}.jpg')
    for f in her[p]['feats']: cv2.rectangle(im,(f['x'],0),(f['x'],0),(0,0,0),1)
    kept={(f['line'],f['word']) for f in ok[p]['feats']}
    import seg
    _,_,lab,L,_=seg.page(f'/home/claude/scans/atlas/images/web/{p}.jpg')
    L=[[w for w in l if not all(b['h']<6 and b['w']<6 for b in w)] for l in L]; L=[l for l in L if len(l)>=2]
    for li,l in enumerate(L):
        for wi,w in enumerate(l):
            x0=min(b['x'] for b in w); x1=max(b['x']+b['w'] for b in w); y0=min(b['y'] for b in w); y1=max(b['y']+b['h'] for b in w)
            cv2.rectangle(im,(x0,y0),(x1,y1),(0,170,0) if (li,wi) in kept else (0,0,255),2)
    cv2.imwrite(f'check_{p}.jpg',cv2.resize(im,None,fx=0.6,fy=0.6)); print("wrote",p,ok[p]['L'])
