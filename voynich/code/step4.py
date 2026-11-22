import sys,re,random,collections; sys.path.insert(0,'/home/claude')
from common import *
random.seed(1)
pages=collections.OrderedDict()
for line in open('/home/claude/vdata/voynich/analysis/takahashi_original.txt'):
    m=re.match(r'<(f\d+[rv]\d*)\.[^>]*>\s*(.*)',line)
    if not m: continue
    body=m.group(2).replace('!','')
    ws=[w.lower() for w in re.split(r'[.\-=,\s]+',body) if w and '*' not in w and re.fullmatch(r'[A-Za-z]+',w)]
    pages.setdefault(m.group(1),[]).extend(ws)
pages={k:v for k,v in pages.items() if len(v)>=60}
avg=sum(map(len,pages.values()))//len(pages)
print("pages",len(pages),"avg words/page",avg)
def lev1(a,b):
    if a==b: return False
    la,lb=len(a),len(b)
    if abs(la-lb)>1: return False
    if la==lb: return sum(x!=y for x,y in zip(a,b))==1
    if la>lb: a,b=b,a
    for i in range(len(b)):
        if b[:i]+b[i+1:]==a: return True
    return False
G=[1,2,3,5,10,20,40]
def prof(pg):
    ex=collections.Counter(); nr=collections.Counter(); tot=collections.Counter()
    for ws in pg:
        for d in G:
            for i in range(len(ws)-d):
                a,b=ws[i],ws[i+d]; tot[d]+=1; ex[d]+=a==b; nr[d]+=lev1(a,b)
    return {d:(100*ex[d]/tot[d],100*nr[d]/tot[d]) for d in G}
def show(name,pg):
    real=prof(pg)
    inpage=prof([random.sample(w,len(w)) for w in pg])
    allw=[w for p in pg for w in p]; random.shuffle(allw); glob_=[]; i=0
    for p in pg: glob_.append(allw[i:i+len(p)]); i+=len(p)
    gl=prof(glob_)
    print(f"\n{name}   (near-match % = differs by one letter;  real | shuffled-within-page | shuffled-globally)")
    for d in G:
        print(f"  gap {d:2d}: exact {real[d][0]:5.2f} | {inpage[d][0]:5.2f} | {gl[d][0]:5.2f}    near {real[d][1]:5.2f} | {inpage[d][1]:5.2f} | {gl[d][1]:5.2f}")
show("VOYNICH",list(pages.values()))
for name,s in baselines(229489).items():
    if name in ('Latin: Pliny NH','Latin: Vulgate','English: Moby Dick'):
        w=s.split(); show(name,[w[i:i+avg] for i in range(0,len(w)-avg,avg)])
