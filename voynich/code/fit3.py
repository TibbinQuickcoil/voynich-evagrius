import sys,itertools,json,numpy as np; sys.path.insert(0,'/home/claude')
from metrics import measure, load_voynich
import evagrius2 as E
V=measure(load_voynich())
sc={'TTR':.02,'zipf':.1,'h2':.08,'len_mean':.3,'exact_ratio_g1':.15,'near_ratio_g1':.1,'page_cluster':.3,'init_p+t%':3,'final_m%':3}
def loss(M): return sum(((float(M[k])-float(V[k]))/s)**2 for k,s in sc.items())
P0=json.load(open('bestP.json')); E.set_legal(P0['th'])
res=[]
for avoid,one,pl,far,sub in itertools.product([0,.5,.8,.95],[.2,.5,.8],[.1,.2,.35],[.02,.05],[.45,.6]):
    P=dict(P0,avoid=avoid,one=one,p_line=pl,p_far=far,sub=sub,av_win=4)
    L=[loss(measure(E.scribe(P,seed=s),seed=s)) for s in (0,1)]; res.append((np.mean(L),avoid,P))
res.sort(key=lambda x:x[0])
for av in (0,.5,.8,.95):
    b=min((r for r in res if r[1]==av),key=lambda r:r[0]); print(f"aversion {av:.2f}: best loss {b[0]:6.1f}")
json.dump(res[0][2],open('bestP_av.json','w')); print("overall best",res[0][1],res[0][2])
