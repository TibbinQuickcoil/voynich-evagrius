import pickle,re,math,collections,random,numpy as np
from wordfreq import top_n_list, word_frequency
Dd=pickle.load(open('oh_trans.pkl','rb')); MAP,snd,T=Dd['MAP'],Dd['snd'],Dd['T']
UNITS=['dzs','cs','dz','gy','ly','ny','sz','ty','zs','mb','nc','nd','nk','mp','nt','ch','us']
SPLIT={'mb':['m','b'],'nc':['n','c'],'nd':['n','d'],'nk':['n','k'],'mp':['m','p'],'nt':['n','t'],'us':['u','s'],'dz':['d','z'],'dzs':['d','zs']}
def tok(s):
    out=[];i=0
    while i<len(s):
        for u in ['dzs','cs','gy','ly','ny','sz','ty','zs','ch']:
            if s.startswith(u,i): out.append(u); i+=len(u); break
        else: out.append(s[i]); i+=1
    return out
def units_of(sound): return SPLIT.get(sound,tok(sound))
# Hungarian reference: 30,000 commonest words weighted by frequency, in the same sound units
uni=collections.Counter(); bi=collections.Counter()
for w in top_n_list('hu',30000):
    if not re.fullmatch(r'[a-záéíóöőúüű]+',w): continue
    f=word_frequency(w,'hu'); u=['#']+[x for t in tok(w) for x in SPLIT.get(t,[t])]+['#']
    for a in u[1:-1]: uni[a]+=f
    for a,b in zip(u,u[1:]): bi[(a,b)]+=f
V=sorted(set(uni)|{'#'}); tot=sum(uni.values()); pu={a:uni[a]/tot for a in uni}
bt=collections.Counter(); [bt.update({a:v}) for (a,b),v in bi.items()]
def lp(a,b): return math.log2((bi[(a,b)]+1e-6*bt[a]+1e-9)/(bt[a]*(1+1e-6*len(V))+1e-9))
VOW=set('aáeéiíoóöőuúüű')
def score(mapping):
    """mapping: code->sound. returns bits per unit under Hungarian bigram model, vowel share, unigram JS divergence"""
    ll=0;n=0;c=collections.Counter()
    for p,s,oh,lat,codes in T:
        u=['#']+[x for cd in codes for x in units_of(mapping[cd])]+['#']
        for a,b in zip(u,u[1:]): ll+=lp(a,b); n+=1
        c.update(u[1:-1])
    N=sum(c.values()); q={a:c[a]/N for a in c}; keys=set(q)|set(pu)
    m={a:(q.get(a,0)+pu.get(a,0))/2 for a in keys}
    js=0.5*sum(q[a]*math.log2(q[a]/m[a]) for a in q if q[a]>0)+0.5*sum(pu[a]*math.log2(pu[a]/m[a]) for a in pu if pu[a]>0)
    return -ll/n, sum(c[a] for a in c if a in VOW)/N, js
real={cd:snd[MAP[cd][0]] for cd in MAP}
r=score(real)
hu_v=sum(pu[a] for a in pu if a in VOW)
print(f"shape mapping:      {r[0]:.2f} bits/unit   vowel share {r[1]:.2f}   letter-mix distance {r[2]:.3f}")
rng=random.Random(0); codes=list(MAP); letters=list(snd.values())
perm=[];rand=[]
for _ in range(300):
    v=[real[c] for c in codes]; rng.shuffle(v); perm.append(score(dict(zip(codes,v))))
    rand.append(score({c:rng.choice(letters) for c in codes}))
for name,S in (('same letters, shuffled among signs',perm),('random letters',rand)):
    a=np.array(S); print(f"{name:35s} {a[:,0].mean():.2f} bits/unit (best {a[:,0].min():.2f})  vowel {a[:,1].mean():.2f}  distance {a[:,2].mean():.3f}")
    print(f"   share of shuffles at least as Hungarian as the shape mapping: {(a[:,0]<=r[0]).mean():.2f}")
# real Hungarian, scored the same way, as the target
ll=0;n=0
for w in top_n_list('hu',3000)[:3000]:
    if not re.fullmatch(r'[a-záéíóöőúüű]+',w): continue
    u=['#']+[x for t in tok(w) for x in SPLIT.get(t,[t])]+['#']
    for a,b in zip(u,u[1:]): ll+=lp(a,b); n+=1
print(f"real Hungarian words: {-ll/n:.2f} bits/unit   vowel share {hu_v:.2f}")
