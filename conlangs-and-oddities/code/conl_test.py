import sys,re,glob,json,random; sys.path.insert(0,'/home/claude/arch/work'); sys.path.insert(0,'/home/claude')
from scripts_test import test
import lorem
C='/home/claude/conl/'
def sents(text,alpha):
    out=[]
    for s in re.split(r'[.!?;:\n]+',text.lower()):
        ws=re.findall(alpha,s)
        if len(ws)>=3: out.append([tuple(w) for w in ws])
    return out
R={}
kl=' '.join(open(f,errors='ignore').read() for f in glob.glob(C+'klingon/sources/**/*.txt',recursive=True))
R['Klingon (xifan hol spelling)']=test(sents(kl,r"[a-z]+"),near=True)
eo=open(C+'eo/RAW/wsdump-Zamenhof_Dietterle_Originala_Verkaro_1929.txt',errors='ignore').read()
R['Esperanto (Zamenhof)']=test(sents(eo,r"[a-zĉĝĥĵŝŭ]+")[:20000],near=True)
tp=[]
for f in glob.glob(C+'poki/plaintext/**/*.md',recursive=True):
    t='\n'.join(l for l in open(f,errors='ignore') if not l.lstrip().startswith(('#','|','---','!','[','<','>')))
    tp+=sents(t,r"[a-z]+")
R['Toki Pona']=test(tp[:20000],near=True)
jb=[l.split('\t')[1] for l in open(C+'phrases/dist/en2jb.tsv',errors='ignore') if '\t' in l]
R['Lojban']=test([[tuple(w.strip(".")) for w in s.split() if w.strip(".")] for s in jb][:20000],near=True)
bird=[list(l.strip()) for f in glob.glob(C+'POMM-Python/*observed_sequences*.txt')+glob.glob(C+'POMM-Python/baseline_subset_1.txt') for l in open(f) if len(l.strip())>=3]
R['Bengalese finch song (syllables)']=test(bird)
random.seed(1); lo=[s for s in (lorem.sentence() for _ in range(4000))]
R['Lorem ipsum (random filler)']=test(sents(' . '.join(lo),r"[a-z]+"),near=True)
for k,v in R.items():
    nr=f"  near {v['near']:.2f}x" if 'near' in v else ''
    print(f"{k:34s} pairs {v['pairs']:7d}  same-twice {v['exact']:.2f}x (p_hi {v['p_hi']:.3f}, p_lo {v['p_lo']:.3f}){nr}")
json.dump(R,open('conl_results.json','w'),indent=1)
