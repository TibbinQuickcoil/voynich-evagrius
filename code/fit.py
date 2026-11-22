import sys,itertools,random; sys.path.insert(0,'/home/claude')
from metrics import *; from evagrius import *
V=measure(load_voynich())
keys=['exact_ratio_g3','near_ratio_g3','TTR','zipf','h2','len_mean','len_sd','exact_ratio_g1','near_ratio_g1','near_ratio_g5','break_near_ratio','page_cluster','init_p+t%','final_m%']
def loss(M):
    sc={'TTR':.05,'zipf':.1,'h2':.15,'len_mean':.3,'len_sd':.3,'exact_ratio_g1':.15,'near_ratio_g1':.1,'near_ratio_g5':.1,'break_near_ratio':.15,'page_cluster':.2,'init_p+t%':3,'final_m%':3}
    return sum(((M[k]-V[k])/sc[k])**2 for k in sc)
base=dict(one=.7,sub=.6,pre=.2,p_line=.35,win=3,p_exact=.03,open=.2,close=.17,p_far=.1)
best=None
import evagrius
grid=list(itertools.product([.1,.2],[.0,.02],[.2,.5],[.45,.6,.75],[2],[.02,.05,.1,.2]))
for th in (2,4):
  evagrius.set_legal(th)
  for pl,pe,one,sub,win,far in grid:
    P=dict(base,p_line=pl,p_exact=pe,one=one,sub=sub,win=win,p_far=far,th=th)
    M=measure(evagrius.scribe(P)); l=loss(M)
    if best is None or l<best[0]: best=(l,P,M)
if __name__=="__main__":
  l,P,M=best; print("best loss %.1f"%l, P)
  import json; json.dump(P,open('bestP.json','w'))
  print(f"{'metric':18s} {'VOYNICH':>9s} {'EVAGRIUS':>9s}")
  for k in keys: print(f"{k:18s} {V[k]:9.3f} {M[k]:9.3f}")
