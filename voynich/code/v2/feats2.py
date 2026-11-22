import sys,pickle,glob,numpy as np,cv2; sys.path.insert(0,'/home/claude/virgin')
from seg import page
from skimage.morphology import skeletonize
D='/home/claude/scans/atlas/images/web/'
def blob_feats(lab,b):
    crop=np.isin(lab[b['y']:b['y']+b['h'],b['x']:b['x']+b['w']],b['parts'])
    sk=skeletonize(crop).astype(np.uint8)*255
    s=max(b['w'],b['h'])+4; pad=np.zeros((s,s),np.uint8); oy=(s-b['h'])//2; ox=(s-b['w'])//2
    pad[oy:oy+b['h'],ox:ox+b['w']]=sk
    v=cv2.resize(pad,(24,24),interpolation=cv2.INTER_AREA).astype(np.float32)
    v=cv2.GaussianBlur(v,(0,0),1.0); v/= (v.max()+1e-6)                   # uniform-width redraw
    return np.concatenate([v.ravel(),[np.log(b['w']/b['h'])*1.5, b['h']/8.0]])
def process(folios,out):
    data={}
    for f in folios:
        im,ink,lab,L,thr=page(D+f+'.jpg')
        L=[[w for w in l if not all(b['h']<6 and b['w']<6 for b in w)] for l in L]; L=[l for l in L if len(l)>=2]
        F=[]
        for li,l in enumerate(L):
            for wi,w in enumerate(l):
                for b in w: F.append(dict(page=f,line=li,word=wi,x=b['x'],w=b['w'],h=b['h'],vec=blob_feats(lab,b)))
        data[f]=dict(nwords=sum(map(len,L)),feats=F)
    pickle.dump(data,open(out,'wb')); return data
if __name__=='__main__':
    REC=[f"f{n}{s}" for n in range(103,117) for s in 'rv' if f"f{n}{s}" not in ("f111r","f111v","f116v") and glob.glob(D+f"f{n}{s}.jpg")]
    d=process(REC,'rec2.pkl'); print("blobs",sum(len(x['feats']) for x in d.values()))
