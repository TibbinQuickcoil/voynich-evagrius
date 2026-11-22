import sys,random,collections,json,numpy as np; sys.path.insert(0,'/home/claude'); sys.path.insert(0,'/home/claude/arch/work'); sys.path.insert(0,'/home/claude/v3')
from scripts_test import test
from common import baselines
words=baselines(229489)['Latin: Pliny NH'].split()[:30000]
lines=[words[i:i+9] for i in range(0,len(words),9)]
freq=collections.Counter(''.join(words)); rng=random.Random(5)
R=json.load(open('scripts_results.json'))
R['Latin, Pliny (plain), words']=test([[tuple(w) for w in l] for l in lines],near=True,n=200)
for total in (60,120):                      # number of cipher symbols overall
    # homophones per letter proportional to its frequency (the classic design)
    n=sum(freq.values()); alloc={c:max(1,round(total*f/n)) for c,f in freq.items()}; sym={};k=0
    for c,a in alloc.items(): sym[c]=list(range(k,k+a)); k+=a
    enc=[[tuple(rng.choice(sym[c]) for c in w) for w in l] for l in lines]
    R[f'Homophonic cipher of Pliny ({k} symbols), words']=test(enc,near=True,n=200)
for key in [k for k in R if 'Pliny' in k]:
    v=R[key]; print(f"{key:48s} same-twice {v['exact']:.2f}x  near {v['near']:.2f}x")
json.dump(R,open('scripts_results.json','w'),indent=1)
