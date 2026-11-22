import re,sys,collections,random; sys.path.insert(0,'/home/claude')
from metrics import lev1
exec(open('/home/claude/sera.py').read().split("K=[")[0])          # reuse page loader
gt=[l.split() for l in open('/home/claude/ext/codex_seraphinianus_ocr/CS_DB/gt/words.txt') if '.AAA_' in l]
ids=[g[0].split('.AAA_')[0] for g in gt]; vocab=collections.Counter(' '.join(g[8:]) for g in gt)
# contiguous hand-labeled pairs?
pos=set()
for i in ids:
    m=re.match(r'(.*)-L(\d+)\.(\d+)',i); pos.add((m.group(1),int(m.group(2)),int(m.group(3))))
adj=sum((b,l,w+1) in pos for b,l,w in pos)
print("hand-labeled words",len(gt),"distinct labels",len(vocab),"| adjacent hand-labeled pairs:",adj)
W=[w for p in pages for l in p for w in l]
inv=sum(w in vocab for w in W)
print(f"OCR tokens that exactly equal a training label: {100*inv/len(W):.1f}%  ({len(set(W)&set(vocab))} of {len(set(W))} OCR word types)")
# repeats: are they dominated by training-vocab words?
rp=[(a) for p in pages for l in p for a,b in zip(l[1:-1],l[2:-1]) if a==b]
print(f"adjacent exact repeats: {len(rp)}, of which training-label words: {100*sum(w in vocab for w in rp)/max(1,len(rp)):.0f}%")
# excess ratio with training-vocab words excluded entirely
def ratio(pg,rnd):
    def rates(P):
        ex=nr=t=0
        for p in P:
            for l in p:
                c=l[1:-1]
                for a,b in zip(c,c[1:]): t+=1; ex+=a==b; nr+=lev1(a,b)
        return ex/t,nr/t
    S=[]
    for p in pg:
        pool=[w for l in p for w in l[1:-1]]; rnd.shuffle(pool); i=0; q=[]
        for l in p: k=len(l)-2; q.append([l[0]]+pool[i:i+k]+[l[-1]]); i+=k
        S.append(q)
    (re_,rn),(se,sn)=rates(pg),rates(S); return re_/se,rn/sn
for name,filt in [('all words',lambda w:True),('training-label words removed',lambda w:w not in vocab)]:
    pg=[[[w for w in l if filt(w)] for l in p] for p in pages]
    pg=[[l for l in p if len(l)>=4] for p in pg]
    rs=[ratio(pg,random.Random(s)) for s in range(10)]
    ex=sum(r[0] for r in rs)/10; nr=sum(r[1] for r in rs)/10
    print(f"{name:30s} exact {ex:.2f}x   near {nr:.2f}x")
