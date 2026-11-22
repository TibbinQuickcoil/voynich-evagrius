import sys; sys.path.insert(0,'/home/claude')
from common import *
vw=voy_words(); vs=' '.join(vw); N=len(vs)
print("Voynich chars",N)
# A) hand-chosen glyph groupings (standard proposals in the literature)
def tok(s,units):
    out=[];i=0
    while i<len(s):
        for u in units:
            if s.startswith(u,i): out.append(u); i+=len(u); break
        else: out.append(s[i]); i+=1
    return out
schemes={'raw EVA':[],
 'benches+gallows (ch,sh,cth,ckh,cph,cfh)':['cth','ckh','cph','cfh','ch','sh'],
 '+ ii/ee/aiin family':['cth','ckh','cph','cfh','aiin','ain','iin','ii','ee','ch','sh'],
 '+ qo, dy, ol, or, ar, al (aggressive)':['cth','ckh','cph','cfh','aiin','ain','iin','ii','ee','ch','sh','qo','dy','ol','or','ar','al']}
print("\n-- hand groupings (alphabet, h1, h2|1) --")
for k,u in schemes.items():
    a,h1,h2=h_cond(tok(vs,u)); print(f"{k:45s} {a:3d} {h1:.2f} {h2:.2f}")
# B) fair control: same BPE merges applied to everyone
base=baselines(N)
print("\n-- BPE merges: h2|1 (alphabet) --")
ks=[0,5,10,20,40]
print(f"{'text':24s}"+''.join(f"  k={k:<9d}" for k in ks))
for name,s in [('VOYNICH',vs)]+list(base.items()):
    row=[]
    for k in ks:
        a,h1,h2=h_cond(bpe(s,k)); row.append(f"  {h2:.2f} ({a:3d})")
    print(f"{name:24s}"+''.join(row))
