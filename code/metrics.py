import re,random,math,collections
import numpy as np
def lev1(a,b):
    if a==b: return False
    la,lb=len(a),len(b)
    if abs(la-lb)>1: return False
    if la==lb: return sum(x!=y for x,y in zip(a,b))==1
    if la>lb: a,b=b,a
    return any(b[:i]+b[i+1:]==a for i in range(len(b)))
def load_voynich():
    pages={}
    for line in open('/home/claude/vdata/voynich/analysis/takahashi_original.txt'):
        m=re.match(r'<(f\d+[rv]\d*)\.([A-Z]+)[^>]*>\s*(.*)',line)
        if not m or not m.group(2).startswith('P') or '*' in m.group(3): continue
        ws=[w.lower() for w in re.split(r'[.\-=,\s]+',m.group(3).replace('!','')) if w and re.fullmatch(r'[A-Za-z]+',w)]
        if len(ws)>=3: pages.setdefault(m.group(1),[]).append(ws)
    return list(pages.values())
def H2(s):
    c1=collections.Counter(s); n=len(s); h1=-sum(v/n*math.log2(v/n) for v in c1.values())
    c2=collections.Counter(zip(s,s[1:])); h=-sum(v/(n-1)*math.log2(v/(n-1)) for v in c2.values()); return h-h1
def measure(pages,seed=0):
    rnd=random.Random(seed)
    L=[l for p in pages for l in p]; W=[w for l in L for w in l]; C=collections.Counter(W)
    f=np.array(sorted(C.values(),reverse=True),float); r=np.arange(1,len(f)+1); k=min(1000,len(f))
    out={}
    out['TTR']=len(C)/len(W)
    out['zipf']=np.polyfit(np.log(r[:k]),np.log(f[:k]),1)[0]
    out['h2']=H2(' '.join(W))
    out['len_mean']=np.mean([len(w) for w in W]); out['len_sd']=np.std([len(w) for w in W])
    out['init_p+t%']=100*sum(l[0][0] in 'pt' for l in L)/len(L)
    out['final_m%']=100*sum(l[-1][-1]=='m' for l in L)/len(L)
    # interior adjacency vs shuffled interior (same page)
    def adj(pg,d):
        ex=nr=t=0
        for p in pg:
            for l in p:
                c=l[1:-1]
                for i in range(len(c)-d): t+=1; ex+=c[i]==c[i+d]; nr+=lev1(c[i],c[i+d])
        return 100*ex/t,100*nr/t
    def shuf(pg):
        o=[]
        for p in pg:
            pool=[w for l in p for w in l[1:-1]]; rnd.shuffle(pool); i=0; q=[]
            for l in p: k=len(l)-2; q.append([l[0]]+pool[i:i+k]+[l[-1]]); i+=k
            o.append(q)
        return o
    S=shuf(pages)
    for d in (1,3,5):
        re_,rn=adj(pages,d); se,sn=adj(S,d)
        out[f'exact_ratio_g{d}']=re_/se if se else float('nan'); out[f'near_ratio_g{d}']=rn/sn if sn else float('nan')
    # across break
    t=ex=nr=0
    for p in pages:
        for a,b in zip(p,p[1:]): t+=1; nr+=lev1(a[-1],b[0])
    fs=[]; 
    for p in pages:
        firsts=[l[0] for l in p]; rnd.shuffle(firsts)
        fs+= [lev1(a[-1],f) for a,f in zip(p,firsts[1:])]
    out['break_near_ratio']=(100*nr/t)/(100*sum(fs)/len(fs)) if sum(fs) else float('nan')
    # page clustering: near rate within page / across whole book
    allw=W[:]; rnd.shuffle(allw); g=[];i=0
    for p in pages:
        q=[]; 
        for l in p: q.append(allw[i:i+len(l)]); i+=len(l)
        g.append(q)
    _g=adj(g,5)[1]; out['page_cluster']=adj(S,5)[1]/_g if _g else 99.0
    return out
