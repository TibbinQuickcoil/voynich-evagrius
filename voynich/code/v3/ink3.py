import pickle,numpy as np,random,collections,sys; sys.path.insert(0,'/home/claude/v3')
exec(open('ink.py').read().split("rnd=random.Random(0); pages=list(A)")[0])
rnd=random.Random(1); out=collections.defaultdict(list)
for p,P in A.items():
    byline=collections.defaultdict(list)
    for q in P:
        if 0<q['word']<q['nline']-1: byline[q['line']].append(q)
    for q in [q for L in byline.values() for q in L]:
        for k in (1,2,3,5):
            tgt=byline.get(q['line']+k,[])
            if len(tgt)<3: continue
            r=max(tgt,key=lambda r:min(q['x1'],r['x1'])-max(q['x0'],r['x0']))
            if min(q['x1'],r['x1'])-max(q['x0'],r['x0'])<=0: continue
            pool=[t for t in tgt if t is not r]
            out[k].append(sim(q,r)-sim(q,rnd.choice(pool)))
for k in (1,2,3,5):
    d=np.array(out[k]); print(f"{k} line(s) down: aligned word minus random word on that line {d.mean():+.4f}  (SE {d.std()/np.sqrt(len(d)):.4f}, n={len(d)})")
