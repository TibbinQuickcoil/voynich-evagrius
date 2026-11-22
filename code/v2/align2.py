import pickle,collections,numpy as np,sys; sys.path.insert(0,'/home/claude/v2')
from align import tak_all_lines, machine_lines
from metrics import lev1
def nw(a,b,gap=4):
    n,m=len(a),len(b); D=np.zeros((n+1,m+1)); B={}
    D[:,0]=np.arange(n+1)*gap; D[0,:]=np.arange(m+1)*gap
    for i in range(1,n+1):
        for j in range(1,m+1):
            opts=[(D[i-1,j-1]+abs(len(a[i-1])-len(b[j-1])),'d'),(D[i-1,j]+gap,'u'),(D[i,j-1]+gap,'l')]
            D[i,j],B[i,j]=min(opts)
    i,j=n,m; out=[]
    while i>0 and j>0:
        t=B[i,j]
        if t=='d': out.append((i-1,j-1)); i-=1; j-=1
        elif t=='u': i-=1
        else: j-=1
    return out[::-1]
def aligned(K=80,seed=0,data=None):
    data=data or pickle.load(open('/home/claude/v2/rec2.pkl','rb')); ML=machine_lines(data,K,seed)
    out={}
    for p,m in ML.items():
        E=tak_all_lines(p); A=nw(E,m)
        out[p]=[(E[i],m[j]) for i,j in A if len(E[i])==len(m[j]) and not any('*' in w for w in E[i])]
    return out,ML
if __name__=='__main__':
    A,_=aligned()
    pairs=[(e,mm) for p in A.values() for E,M in p for e,mm in zip(E,M)]
    print("aligned lines",sum(map(len,A.values())),"word pairs",len(pairs))
    by=collections.defaultdict(list)
    for e,mm in pairs: by[e].append(mm)
    same=[(a==b) for v in by.values() for i,a in enumerate(v) for b in v[i+1:]]
    near=[lev1(a,b) for v in by.values() for i,a in enumerate(v) for b in v[i+1:]]
    print(f"same human word -> identical machine spelling: {100*np.mean(same):.1f}%   one-symbol-different: {100*np.mean(near):.1f}%  (from {len(same)} instance pairs)")
    print("examples (human word: machine spellings, symbols numbered by cluster):")
    for w,v in sorted(by.items(),key=lambda kv:-len(kv[1]))[:8]:
        c=collections.Counter(v); print(f"  {w:8s} n={len(v):3d}  distinct machine spellings {len(c)}   blob counts {sorted(collections.Counter(len(x) for x in v).items())}")
    import random; r=random.Random(0); e,m=zip(*pairs); idx=r.sample(range(len(pairs)),3000)
    print(f"sanity: random human/machine pairing gives word-length correlation {np.corrcoef([len(e[i]) for i in idx],[len(m[i]) for i in idx])[0,1]:.2f}; aligned pairs: {np.corrcoef([len(x) for x in e],[len(x) for x in m])[0,1]:.2f}")
