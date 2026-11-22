import sys,random,numpy as np; sys.path.insert(0,'/home/claude/virgin'); sys.path.insert(0,'/home/claude')
from syllabary import transcribe,eva_pages
from metrics import lev1
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
for name,P in [('VIRGIN K=80',transcribe(80,0)),('VIRGIN K=150',transcribe(150,0)),('EVA',eva_pages())]:
    pg=list(P.values()); (h,v)=counts(pg); rnd=random.Random(1)
    S=[counts(shuf(pg,rnd)) for _ in range(300)]
    print(f"\n{name}   pairs: horizontal {h[0]}, vertical {v[0]}")
    for lab,real,idx,k in [('next word, exact',h,0,1),('next word, near',h,0,2),('word below, exact',v,1,1),('word below, near',v,1,2)]:
        null=np.array([s[idx][k] for s in S]); p=(1+(null>=real[k]).sum())/(1+len(null))
        print(f"  {lab:18s} observed {real[k]:4d}  chance {null.mean():6.1f}  -> {real[k]/null.mean():.2f}x   p={p:.3f}")
