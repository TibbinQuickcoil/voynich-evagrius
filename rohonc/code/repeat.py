import sys,pickle,random,collections,numpy as np; sys.path.insert(0,'/home/claude')
from metrics import lev1
from sklearn.cluster import MiniBatchKMeans
Dd=pickle.load(open('oh_trans.pkl','rb')); D=pickle.load(open('rohonc_signs.pkl','rb'))
# rebuild lines with sign objects (same reading order as the transliteration)
B=[b for b in D['B'] if b['code'] in Dd['MAP']]; pages=collections.defaultdict(list)
for b in B: pages[b['page']].append(b)
LINES=[]
for p in sorted(pages):
    bl=pages[p]; mid=np.median([b['x']+b['w']/2 for b in bl])
    for sel in ([b for b in bl if b['x']+b['w']/2<mid],[b for b in bl if b['x']+b['w']/2>=mid]):
        sel=sorted(sel,key=lambda b:b['y']+b['h']/2); cur=[]; last=None; page=[]
        for b in sel:
            cy=b['y']+b['h']/2
            if last is not None and cy-last>18: page.append(cur); cur=[]
            cur.append(b); last=cy if last is None else 0.7*last+0.3*cy
        if cur: page.append(cur)
        LINES.append([sorted(L,key=lambda b:-(b['x']+b['w'])) for L in page if len(L)>=4])
# coarser sign classes too, to blunt over-splitting (crescents by size/tilt)
codes=sorted(D['proto']); X=np.array([D['proto'][c].ravel()/255 for c in codes])
coarse={}
for K in (150,60,30):
    if K==150: coarse[K]={c:c for c in codes}
    else:
        lab=MiniBatchKMeans(K,random_state=0,n_init=5).fit_predict(X); coarse[K]={c:f"C{l}" for c,l in zip(codes,lab)}
def words(page_lines,gap,cmap):
    sym={}
    out=[]
    for L in page_lines:
        ws=[];cur=[]
        for i,b in enumerate(L):
            if cur and (L[i-1]['x']-(b['x']+b['w']))>gap: ws.append(cur); cur=[]
            cur.append(b)
        if cur: ws.append(cur)
        out.append([''.join(chr(0x4E00+hash(cmap[b['code']])%5000) for b in w) for w in ws])
    return [l for l in out if len(l)>=3]
def counts(pg):
    h=[0,0,0];v=[0,0,0]
    for p in pg:
        for l in p:
            c=l[1:-1]
            for a,b in zip(c,c[1:]): h[0]+=1; h[1]+=a==b; h[2]+=lev1(a,b)
        for a,b in zip(p,p[1:]):
            for i,w in enumerate(a[1:-1],1):
                j=min(max(round(i*(len(b)-1)/max(1,len(a)-1)),1),len(b)-2)
                if 0<j<len(b)-1: v[0]+=1; v[1]+=w==b[j]; v[2]+=lev1(w,b[j])
    return h,v
def shuf(pg,rnd):
    o=[]
    for p in pg:
        pool=[w for l in p for w in l[1:-1]]; rnd.shuffle(pool); i=0; q=[]
        for l in p: k=len(l)-2; q.append([l[0]]+pool[i:i+k]+[l[-1]]); i+=k
        o.append(q)
    return o
import os; os.environ['PYTHONHASHSEED']='0'
for K in (150,60,30):
    for gap in (10,14,20):
        pg=[words(P,gap,coarse[K]) for P in LINES]; pg=[p for p in pg if p]
        (h,v)=counts(pg); rnd=random.Random(1); S=[counts(shuf(pg,rnd)) for _ in range(150)]
        def rr(real,idx,k):
            null=np.array([s[idx][k] for s in S]); return real[k]/null.mean(), (1+(null>=real[k]).sum())/151, (1+(null<=real[k]).sum())/151
        e=rr(h,0,1); n=rr(h,0,2); ve=rr(v,1,1); vn=rr(v,1,2)
        W=[w for p in pg for l in p for w in l]
        print(f"K={K:3d} gap>{gap:2d}px  words {len(W):6d} ({np.mean([len(w) for w in W]):.1f} signs)  next exact {e[0]:.2f}x [p_hi {e[1]:.3f} p_lo {e[2]:.3f}]  next near {n[0]:.2f}x [p_hi {n[1]:.3f} p_lo {n[2]:.3f}]  below near {vn[0]:.2f}x")
