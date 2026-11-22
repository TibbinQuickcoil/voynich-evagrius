import pickle,numpy as np,sys
from sklearn.decomposition import PCA
from sklearn.cluster import MiniBatchKMeans
sys.path.insert(0,'/home/claude/v2'); from common2 import *
def transcribe(data,K,seed=0,pcs=40,return_model=False):
    F=[f for d in data.values() for f in d['feats']]
    X=np.array([f['vec'] for f in F]); Z=PCA(pcs,random_state=0).fit_transform(X)
    lab=MiniBatchKMeans(K,random_state=seed,n_init=3,batch_size=4096).fit_predict(Z)
    pages={}
    for f,l in zip(F,lab): pages.setdefault(f['page'],{}).setdefault(f['line'],{}).setdefault(f['word'],[]).append((f['x'],chr(0x4E00+l)))
    out={p:[l for l in [[''.join(s for _,s in sorted(ws[w])) for w in sorted(ws)] for _,ws in sorted(ls.items())] if len(l)>=3] for p,ls in pages.items()}
    return (out,F,lab,Z) if return_model else out
def consistency(P):
    W=[w for p in P.values() for l in p for w in l]; c=collections.Counter(W); n=len(W)
    return len(c)/n, 100*sum(v*v for v in c.values())/n/n     # TTR, chance two random words are identical (%)
if __name__=='__main__':
    new=pickle.load(open('rec2.pkl','rb'))
    old=pickle.load(open('/home/claude/virgin/pages.pkl','rb')); [old.pop(k) for k in ('f111r','f111v')]
    for K in (40,60,80):
        for name,d in [('old (thickness-sensitive)',old),('new (skeleton)',new)]:
            P=transcribe(d,K); t,c=consistency(P); print(f"K={K:3d} {name:26s} TTR {t:.3f}  identical-by-chance {c:.3f}%")
