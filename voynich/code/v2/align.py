import re,pickle,collections,sys; sys.path.insert(0,'/home/claude/v2')
from trans2 import *
def tak_all_lines(p):
    L=[]
    for l in open('/home/claude/vdata/voynich/analysis/takahashi_original.txt'):
        m=re.match(r'<(f\d+[rv])\.([A-Z]+)[^>]*>\s*(.*)',l)
        if m and m.group(1)==p:
            ws=[w.lower() for w in re.split(r'[.\-=,\s]+',m.group(3).replace('!','')) if w and re.search('[A-Za-z*]',w)]
            if ws: L.append(ws)
    return L
def machine_lines(data,K,seed=0):
    F=[f for d in data.values() for f in d['feats']]
    _,F,lab,_=transcribe(data,K,seed,return_model=True)
    M={}
    for f,l in zip(F,lab): M.setdefault(f['page'],{}).setdefault(f['line'],{}).setdefault(f['word'],[]).append((f['x'],chr(0x4E00+l)))
    return {p:[[''.join(s for _,s in sorted(ws[w])) for w in sorted(ws)] for _,ws in sorted(ls.items())] for p,ls in M.items()}
if __name__=='__main__':
    data=pickle.load(open('rec2.pkl','rb')); ML=machine_lines(data,80)
    tot=same_lines=0; pairs=0
    for p in ML:
        E=tak_all_lines(p); m=ML[p]
        ok=len(E)==len(m); tot+=1; same_lines+=ok
        wm=sum(len(a)==len(b) for a,b in zip(E,m)) if ok else 0
        pairs+=sum(len(a) for a,b in zip(E,m) if len(a)==len(b)) if ok else 0
        print(f"{p:6s} EVA lines {len(E):3d} machine lines {len(m):3d}  {'MATCH' if ok else '':5s}  lines with equal word counts {wm}")
    print("pages with matching line count",same_lines,"/",tot,"aligned word pairs",pairs)
