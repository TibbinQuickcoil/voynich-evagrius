import sys,pickle,numpy as np,collections,cv2; sys.path.insert(0,'.')
from refs import norm, SCRIPTS
D=pickle.load(open('rohonc_signs.pkl','rb')); R=pickle.load(open('refs.pkl','rb'))
rng=np.random.default_rng(0)
B=D['B']; idx=rng.choice(len(B),5000,replace=False)
S=np.array([v for v in (norm(B[i]['img']>127) for i in idx) if v is not None]); codes=[B[i]['code'] for i in idx]
def tf(a,k):
    return [np.rot90(a,1),np.rot90(a,3),np.flipud(np.rot90(a,1)),np.fliplr(np.rot90(a,1))][k]
res={}
for name,L in R.items():
    V=np.array([v for _,_,v in L]); simR=S@V.T                                   # signs x letters, as written
    T=np.stack([np.array([norm(tf(a,k)) for _,a,_ in L]) for k in range(4)])     # 4 scrambles x letters
    simN=np.einsum('sd,kld->ksl',S,T)
    Mv=np.array([norm(np.fliplr(a)) for _,a,_ in L]); simM=np.maximum(simR,S@Mv.T)  # allowing mirror writing
    real=[];null=[];mir=[]
    for _ in range(300):
        sub=rng.choice(len(L),22,replace=False); ks=rng.integers(0,4,len(sub))
        real.append(simR[:,sub].max(1).mean())
        null.append(simN[ks,:,sub].max(0).mean())
        mir.append(simM[:,sub].max(1).mean())
    res[name]=dict(real=np.mean(real),null=np.mean(null),lift=np.mean(np.array(real)-np.array(null)),
                   lift_sd=np.std(np.array(real)-np.array(null)),mirror=np.mean(mir),simR=simR,L=L)
for name,r in sorted(res.items(),key=lambda kv:-kv[1]['lift']):
    print(f"{name:20s} match {r['real']:.3f}  scrambled {r['null']:.3f}  lift {r['lift']:+.3f} (sd {r['lift_sd']:.3f})  with mirror {r['mirror']:.3f}")
pickle.dump({k:{kk:vv for kk,vv in v.items() if kk not in('simR','L')} for k,v in res.items()},open('match_res.pkl','wb'))
# Coptic map for the 25 commonest Rohonc codes, with best overall rival
P=D['proto']; cnt=D['counts']; top=sorted(cnt,key=lambda c:-cnt[c])[:25]
allL=[(n,cp,v) for n,L in R.items() for cp,_,v in L]
print("\ncode  count  nearest Coptic      sim   | nearest letter in any script")
rows=[]
for c in top:
    v=norm(P[c]>127); cs=[(float(v@x),cp) for cp,_,x in R['Coptic']]; s,cp=max(cs)
    o=max(((float(v@x),n,cp2) for n,cp2,x in allL),key=lambda t:t[0])
    rows.append((c,cnt[c],chr(cp),f"U+{cp:04X}",s,o)); print(f"{c} {cnt[c]:6d}  {chr(cp)} U+{cp:04X}  {s:.3f}   | {chr(o[2])} ({o[1]}) {o[0]:.3f}")
pickle.dump(rows,open('coptic_map.pkl','wb'))
