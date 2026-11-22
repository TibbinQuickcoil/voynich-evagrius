import sys,random,itertools,collections,numpy as np; sys.path.insert(0,'/home/claude/v2'); sys.path.insert(0,'/home/claude')
from common2 import *
from evagrius import tok
REC=[f"f{n}{s}" for n in range(103,117) for s in 'rv' if f"f{n}{s}" not in ('f111r','f111v','f116v')]
def degrade(P,pm,v,pe,wb,seed):
    R=random.Random(seed); out={}
    for p,ls in P.items():
        nl=[]
        for l in ls:
            ws=[]
            for w in l:
                u=tok(w); blobs=[]
                for x in u:                                   # strokes join into blobs at random
                    if blobs and R.random()<pm: blobs[-1]+=x
                    else: blobs.append(x)
                sy=[]
                for b in blobs:
                    if R.random()<pe: sy.append(chr(0x4E00+R.randrange(80)))          # misread
                    else: sy.append(chr(0x5000+hash((b,R.randrange(v)))%20000))         # split into variants
                ws.append(''.join(sy))
            m=[]                                              # word-boundary errors
            for w in ws:
                r=R.random()
                if m and r<wb/2: m[-1]+=w
                elif r<wb and len(w)>=2: k=R.randrange(1,len(w)); m+= [w[:k],w[k:]]
                else: m.append(w)
            if len(m)>=3: nl.append(m)
        out[p]=nl
    return out
def stats(P):
    W=[w for p in P.values() for l in p for w in l]; c=collections.Counter(W); n=len(W)
    return len(c)/n, 100*sum(x*x for x in c.values())/n/n, np.mean([len(w) for w in W])
if __name__=='__main__':
    E=tak_pages(REC); target=(0.732,0.103,34552/9465)
    best=None
    for pm,v,pe,wb in itertools.product([0,.05,.1,.15],[1,2,3],[0,.03,.06,.1],[.1,.2,.3,.4]):
        s=stats(degrade(E,pm,v,pe,wb,0)); loss=((s[0]-target[0])/.02)**2+((s[1]-target[1])/.01)**2+((s[2]-target[2])/.2)**2
        if best is None or loss<best[0]: best=(loss,(pm,v,pe,wb),s)
    print("calibrated noise",best[1],"-> TTR %.3f identical-by-chance %.3f%% blobs/word %.2f   (machine: 0.732, 0.103%%, 3.65)"%best[2])
    import json; json.dump(best[1],open('noise.json','w'))
