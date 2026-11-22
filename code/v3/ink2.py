import pickle,numpy as np,random,collections,sys; sys.path.insert(0,'/home/claude/v3')
exec(open('ink.py').read().split("rnd=random.Random(0); pages=list(A)")[0])
# machine-only: neighbour ink similarity vs a random interior word from the same target line
def test(seed):
    rnd=random.Random(seed); res={'H':[], 'V':[]}
    for p,P in A.items():
        byline=collections.defaultdict(list)
        for q in P:
            if 0<q['word']<q['nline']-1: byline[q['line']].append(q)
        H,V,_=page_pairs(P,rnd)
        for k,L in (('H',H),('V',V)):
            for a,b in L:
                pool=[r for r in byline[b['line']] if r is not b and r is not a]
                if pool: res[k].append(sim(a,b)-sim(a,rnd.choice(pool)))
    return res
R=test(0)
for k,name in (('H','same line'),('V','line below')):
    d=np.array(R[k]); m=d.mean(); se=d.std()/np.sqrt(len(d))
    # permutation-free: sign-flip null on paired differences
    rnd=np.random.default_rng(0); null=np.array([(d*rnd.choice([-1,1],len(d))).mean() for _ in range(2000)])
    print(f"{name:11s} neighbour minus random-word-on-that-line: {m:+.4f} (SE {se:.4f}, n={len(d)})  p={(1+(null>=m).sum())/2001:.4f}")
