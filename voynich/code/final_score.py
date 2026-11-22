import sys,json,pickle,numpy as np; sys.path.insert(0,'/home/claude'); sys.path.insert(0,'/home/claude/v2'); sys.path.insert(0,'/home/claude/v3')
from metrics import measure, load_voynich
from common2 import perm
import evagrius2 as E
from controls import from_lines, read_lines, C
Pav=json.load(open('bestP_av.json')); E.set_legal(Pav['th']); P0=dict(Pav,avoid=0)
def books():
    yield 'Voynich (Takahashi)', [load_voynich()]
    yield 'Evagrius, no aversion', [E.scribe(P0,seed=s) for s in range(5)]
    yield 'Evagrius, aversion 0.5', [E.scribe(Pav,seed=s) for s in range(5)]
    yield 'Timm-Schinner generator', [list(from_lines(read_lines(C+f'selfcitation/selfcite_seed{s}.txt')).values()) for s in (1,2,3)]
K=['TTR','h2','zipf','len_mean','exact_ratio_g1','near_ratio_g1','page_cluster']
rows={}
for name,bs in books():
    M=[measure(b,seed=i) for i,b in enumerate(bs)]; R=[perm(b,n=100,seed=i) for i,b in enumerate(bs)]
    rows[name]={k:(np.mean([float(m[k]) for m in M]),np.std([float(m[k]) for m in M])) for k in K}
    rows[name]['V-near']=(np.mean([r['V near'][0] for r in R]),np.std([r['V near'][0] for r in R]))
    print(name,{k:f"{v[0]:.3f}±{v[1]:.3f}" for k,v in rows[name].items()})
pickle.dump(rows,open('final_score.pkl','wb'))
b=E.scribe(Pav,seed=2); print("\nSample, Evagrius with aversion, page 40:"); [print('  '+' '.join(l)) for l in b[40][:5]]
