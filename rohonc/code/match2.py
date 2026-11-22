import sys,pickle,numpy as np; sys.path.insert(0,'.')
from refs import norm
D=pickle.load(open('rohonc_signs.pkl','rb')); R=pickle.load(open('refs.pkl','rb'))
P=D['proto']; S=np.array([v for v in (norm(P[c]>127) for c in P) if v is not None]); print('sign types used',len(S)); rng=np.random.default_rng(1)
def tf(a,k): return [np.rot90(a,1),np.rot90(a,3),np.flipud(np.rot90(a,1)),np.fliplr(np.rot90(a,1))][k]
for name,L in sorted(R.items()):
    V=np.array([v for _,_,v in L]); simR=S@V.T
    T=np.stack([np.array([norm(tf(a,k)) for _,a,_ in L]) for k in range(4)]); simN=np.einsum('sd,kld->ksl',S,T)
    d=[]
    for _ in range(300):
        sub=rng.choice(len(L),22,replace=False); ks=rng.integers(0,4,len(sub))
        d.append(simR[:,sub].max(1).mean()-simN[ks,:,sub].max(0).mean())
    print(f"{name:20s} lift per sign type {np.mean(d):+.3f} (sd {np.std(d):.3f})")
