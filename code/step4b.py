import sys,re,random,collections; sys.path.insert(0,'/home/claude')
from common import *
from step4 import lev1
random.seed(7)
pages=collections.OrderedDict()
for line in open('/home/claude/vdata/voynich/analysis/takahashi_original.txt'):
    m=re.match(r'<(f\d+[rv]\d*)\.(P|T|L|C|R|S|X|Y|N|O|Z|U|Q|K|M|F|G|H|I|J|V|W|D|E|A|B)?[^>]*>\s*(.*)',line)
    m2=re.match(r'<(f\d+[rv]\d*)\.([A-Z]+)[^>]*>\s*(.*)',line)
    if not m2: continue
    pg,unit,body=m2.groups()
    if not unit.startswith('P'): continue      # running paragraph text only (no labels, circles, radii)
    ws=[w.lower() for w in re.split(r'[.\-=,\s]+',body.replace('!','')) if w and re.fullmatch(r'[A-Za-z]+',w)]
    if '*' in body:   # drop lines with unreadable glyphs to avoid broken adjacency
        continue
    if len(ws)>=3: pages.setdefault(pg,[]).append(ws)
L=[l for p in pages.values() for l in p]
print("paragraph lines kept",len(L),"words",sum(map(len,L)))
# 1) do line effects exist?
first=collections.Counter(l[0][0] for l in L); last=collections.Counter(l[-1][-1] for l in L)
inF=collections.Counter(w[0] for l in L for w in l[1:-1]); inL=collections.Counter(w[-1] for l in L for w in l[1:-1])
nI=sum(inF.values()); nL=len(L)
print("\nFIRST glyph: line-initial % vs interior %")
for g in 'pfkt' + 'qoc': print(f"  {g}: {100*first[g]/nL:5.1f} vs {100*inF[g]/nI:5.1f}")
print("LAST glyph: line-final % vs interior %")
for g in 'mgyl' + 'n': print(f"  {g}: {100*last[g]/nL:5.1f} vs {100*inL[g]/nI:5.1f}")
avg=lambda xs: sum(map(len,xs))/len(xs)
print(f"word length: first {avg([l[0] for l in L]):.2f}  interior {avg([w for l in L for w in l[1:-1]]):.2f}  last {avg([l[-1] for l in L]):.2f}")
# 2) interior-only, within-line adjacency; baseline = shuffle interior words among interior slots of same page
def within(lines_, d):
    ex=nr=t=0
    for l in lines_:
        core=l[1:-1]
        for i in range(len(core)-d):
            a,b=core[i],core[i+d]; t+=1; ex+=a==b; nr+=lev1(a,b)
    return 100*ex/t,100*nr/t,t
def shuffled_interior(pg):
    out=[]
    for lines_ in pg.values():
        pool=[w for l in lines_ for w in l[1:-1]]; random.shuffle(pool); i=0; new=[]
        for l in lines_:
            k=len(l)-2; new.append([l[0]]+pool[i:i+k]+[l[-1]]); i+=k
        out+=new
    return out
print("\nINTERIOR words, same line   exact% real | shuffled     near% real | shuffled   (pairs)")
reps=[shuffled_interior(pages) for _ in range(5)]
for d in (1,2,3,4,5):
    r=within(L,d); s=[within(x,d) for x in reps]
    se=sum(x[0] for x in s)/5; sn=sum(x[1] for x in s)/5
    print(f"  gap {d}:   {r[0]:5.2f} | {se:5.2f}        {r[1]:5.2f} | {sn:5.2f}    ({r[2]})")
# 3) across the line break: last word of line i vs first word of line i+1 (same page)
def across(pg):
    ex=nr=t=0
    for lines_ in pg.values():
        for a,b in zip(lines_,lines_[1:]):
            t+=1; ex+=a[-1]==b[0]; nr+=lev1(a[-1],b[0])
    return 100*ex/t,100*nr/t,t
def shuffle_edges(pg):
    out={}
    for k,lines_ in pg.items():
        fs=[l[0] for l in lines_]; random.shuffle(fs); out[k]=[[f]+l[1:] for f,l in zip(fs,lines_)]
    return out
r=across(pages); s=[across(shuffle_edges(pages)) for _ in range(20)]
print(f"\nACROSS line break: exact {r[0]:.2f} | {sum(x[0] for x in s)/20:.2f}   near {r[1]:.2f} | {sum(x[1] for x in s)/20:.2f}   ({r[2]} pairs)")
# 4) entropy on interior-only text
core=' '.join(w for l in L for w in l[1:-1]); full=' '.join(w for l in L for w in l)
print("\nh2|1 full paragraph text %.2f   interior-only %.2f" % (h_cond(full)[2], h_cond(core)[2]))
