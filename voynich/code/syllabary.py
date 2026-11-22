import sys,pickle,random,re,collections,numpy as np; sys.path.insert(0,'/home/claude')
from sklearn.decomposition import PCA
from sklearn.cluster import MiniBatchKMeans
from metrics import lev1
data=pickle.load(open('pages.pkl','rb'))
for bad in ('f111r','f111v'): data.pop(bad)
F=[f for d in data.values() for f in d['feats']]
X=np.array([np.concatenate([f['vec'],[np.log(f['w']/f['h'])*2,f['h']/10]]) for f in F])
Z=PCA(40,random_state=0).fit_transform(X)
def transcribe(K,seed=0):
    lab=MiniBatchKMeans(K,random_state=seed,n_init=3,batch_size=4096).fit_predict(Z)
    sym=[chr(0x4E00+l) for l in lab]           # one invented symbol per cluster
    pages={}
    for f,s in zip(F,sym): pages.setdefault(f['page'],{}).setdefault(f['line'],{}).setdefault(f['word'],[]).append((f['x'],s))
    out={}
    for p,ls in pages.items():
        out[p]=[[''.join(s for _,s in sorted(ws[w])) for w in sorted(ws)] for l,ws in sorted(ls.items())]
        out[p]=[l for l in out[p] if len(l)>=3]
    return out
def eva_pages():
    P={}
    for l in open('/home/claude/vdata/voynich/analysis/takahashi_original.txt'):
        m=re.match(r'<(f\d+[rv])\.([A-Z]+)[^>]*>\s*(.*)',l)
        if not m or m.group(1) not in data or '*' in m.group(3): continue
        ws=[w.lower() for w in re.split(r'[.\-=,\s]+',m.group(3).replace('!','')) if w and re.fullmatch(r'[A-Za-z]+',w)]
        if len(ws)>=3: P.setdefault(m.group(1),[]).append(ws)
    return P
def tests(P,reps=20):
    pg=list(P.values()); rnd=random.Random(0)
    def horiz(pgs,d):
        ex=nr=t=0
        for p in pgs:
            for l in p:
                c=l[1:-1]
                for i in range(len(c)-d): t+=1; ex+=c[i]==c[i+d]; nr+=lev1(c[i],c[i+d])
        return ex/t,nr/t
    def vert(pgs):          # word directly below, by relative position in line
        ex=nr=t=0
        for p in pgs:
            for a,b in zip(p,p[1:]):
                for i,w in enumerate(a[1:-1],1):
                    j=round(i*(len(b)-1)/max(1,len(a)-1)); j=min(max(j,1),len(b)-2)
                    if 0<j<len(b)-1: t+=1; ex+=w==b[j]; nr+=lev1(w,b[j])
        return ex/t,nr/t
    def shuf(pgs):
        o=[]
        for p in pgs:
            pool=[w for l in p for w in l[1:-1]]; rnd.shuffle(pool); i=0; q=[]
            for l in p: k=len(l)-2; q.append([l[0]]+pool[i:i+k]+[l[-1]]); i+=k
            o.append(q)
        return o
    S=[shuf(pg) for _ in range(reps)]
    res={}
    for name,fn in [('next word',lambda x:horiz(x,1)),('2 words on',lambda x:horiz(x,2)),('word below',vert)]:
        r=fn(pg); s=np.array([fn(x) for x in S])
        res[name]=(r[0]/s[:,0].mean(), r[1]/s[:,1].mean(), r[0]*100, s[:,0].mean()*100)
    W=[w for p in pg for l in p for w in l]
    res['_info']=(len(W),len(set(W))/len(W))
    return res
def show(name,R):
    n,ttr=R['_info']; print(f"\n{name}   words {n}  TTR {ttr:.3f}")
    for k in ('next word','2 words on','word below'):
        e,nr,er,es=R[k]; print(f"   {k:11s} exact {e:5.2f}x  ({er:.2f}% vs {es:.2f}%)   near {nr:5.2f}x")
if __name__=='__main__':
    show("EVA (human transcription), same 20 pages",tests(eva_pages()))
    for K in (40,80,150):
        for seed in (0,1):
            show(f"VIRGIN syllabary K={K} seed={seed}",tests(transcribe(K,seed)))
