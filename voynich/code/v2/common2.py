import re,random,collections,numpy as np,sys; sys.path.insert(0,'/home/claude')
from metrics import lev1
ZL='/home/claude/zl/vu/data/voynich-units/ZL3b.txt'
def zl_meta():
    M={}
    for l in open(ZL,errors='ignore'):
        m=re.match(r'<(f\d+[rv]\d*)>\s*<!(.*)>',l)
        if m: M[m.group(1)]=dict(re.findall(r'\$(\w)=(\w+)',m.group(2)))
    return M
def zl_pages(keep=None):
    P={}
    for l in open(ZL,errors='ignore'):
        m=re.match(r'<(f\d+[rv]\d*)\.\d+,.(P\w*)>\s*(.*)',l)
        if not m or (keep and m.group(1) not in keep): continue
        t=re.sub(r'<[^>]*>','',m.group(3)); t=re.sub(r'\[([^:\]]*):[^\]]*\]',r'\1',t); t=re.sub(r"[{}']",'',t)
        if '?' in t: continue
        ws=[w for w in re.split(r'[.,\s]+',t) if re.fullmatch(r'[a-z]+',w)]
        if len(ws)>=3: P.setdefault(m.group(1),[]).append(ws)
    return P
def tak_pages(keep=None):
    P={}
    for l in open('/home/claude/vdata/voynich/analysis/takahashi_original.txt'):
        m=re.match(r'<(f\d+[rv])\.([A-Z]+)[^>]*>\s*(.*)',l)
        if not m or not m.group(2).startswith('P') or '*' in m.group(3) or (keep and m.group(1) not in keep): continue
        ws=[w.lower() for w in re.split(r'[.\-=,\s]+',m.group(3).replace('!','')) if w and re.fullmatch(r'[A-Za-z]+',w)]
        if len(ws)>=3: P.setdefault(m.group(1),[]).append(ws)
    return P
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
def perm(P,n=300,seed=1):
    pg=list(P.values()) if isinstance(P,dict) else P; (h,v)=counts(pg); rnd=random.Random(seed)
    S=[counts(shuf(pg,rnd)) for _ in range(n)]; out={}
    for lab,real,idx,k in [('H exact',h,0,1),('H near',h,0,2),('V exact',v,1,1),('V near',v,1,2)]:
        null=np.array([s[idx][k] for s in S]); out[lab]=(real[k]/null.mean(), (1+(null>=real[k]).sum())/(1+n))
    out['pairs']=(h[0],v[0]); return out
def fmt(name,R):
    s=f"{name:34s} H-near {R['H near'][0]:.2f}x p={R['H near'][1]:.3f} | H-exact {R['H exact'][0]:.2f}x p={R['H exact'][1]:.3f} | V-near {R['V near'][0]:.2f}x p={R['V near'][1]:.3f} | V-exact {R['V exact'][0]:.2f}x p={R['V exact'][1]:.3f}"
    return s
