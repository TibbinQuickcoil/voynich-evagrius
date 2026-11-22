import sys,json,numpy as np; sys.path.insert(0,'/home/claude/v2')
from degrade import *
E=tak_pages(REC); pm,v,pe,wb=json.load(open('noise.json'))
rows=[]
for s in range(20):
    R=perm(degrade(E,pm,v,pe,wb,100+s),n=150,seed=s); rows.append(R)
def summ(k):
    r=np.array([x[k][0] for x in rows]); p=np.array([x[k][1] for x in rows])
    return f"{k:8s} mean {r.mean():.2f}x (range {r.min():.2f}-{r.max():.2f})   significant p<0.05 in {int((p<0.05).sum())}/20 draws"
print("HUMAN EVA, clean:"); print("  "+fmt('',perm(E)))
print("HUMAN EVA degraded to machine-level noise, 20 draws:")
for k in ('H near','H exact','V near','V exact'): print("  "+summ(k))
print("MACHINE (observed): H near 1.12-1.14x p=.003 | V near 0.99-1.03x p=.28-.64")
