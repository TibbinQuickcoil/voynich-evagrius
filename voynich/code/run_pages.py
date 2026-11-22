import sys,re,glob,pickle,numpy as np,cv2; sys.path.insert(0,'/home/claude/virgin')
from seg import *
D='/home/claude/scans/atlas/images/web/'
folios=[f"f{n}{s}" for n in range(103,117) for s in 'rv']
folios=[f for f in folios if glob.glob(D+f+'.jpg') and f!='f116v']
eva={}
for l in open('/home/claude/vdata/voynich/analysis/takahashi_original.txt'):
    m=re.match(r'<(f\d+[rv])\.',l)
    if m: eva[m.group(1)]=eva.get(m.group(1),0)+len([w for w in re.split(r'[.\-=,\s]+',l.split('>',1)[1]) if re.search('[a-zA-Z]',w)])
data={}
for f in folios:
    im,ink,lab,L,thr=page(D+f+'.jpg')
    # drop "words" that are only tiny specks
    L=[[w for w in l if not all(b['h']<6 and b['w']<6 for b in w)] for l in L]
    L=[l for l in L if len(l)>=2]
    feats=[]
    for li,l in enumerate(L):
        for wi,w in enumerate(l):
            for b in w:
                crop=np.isin(lab[b['y']:b['y']+b['h'],b['x']:b['x']+b['w']],b['parts']).astype(np.uint8)*255
                s=max(b['w'],b['h']); pad=np.zeros((s,s),np.uint8); oy=(s-b['h'])//2; ox=(s-b['w'])//2
                pad[oy:oy+b['h'],ox:ox+b['w']]=crop
                v=cv2.resize(pad,(20,20),interpolation=cv2.INTER_AREA).astype(np.float32).ravel()/255
                feats.append(dict(page=f,line=li,word=wi,x=b['x'],vec=v,w=b['w'],h=b['h']))
    nw=sum(map(len,L)); data[f]=dict(L=L,feats=feats)
    print(f"{f:6s} lines {len(L):3d}  words {nw:4d}  EVA {eva.get(f,0):4d}  ratio {nw/max(1,eva.get(f,1)):.2f}  gap-thr {thr}")
pickle.dump(data,open('pages.pkl','wb'))
tot=sum(len(d['feats']) for d in data.values()); print("glyph blobs total",tot)
