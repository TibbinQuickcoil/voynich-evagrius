import sys,re,pickle,json,collections,numpy as np; sys.path.insert(0,'/home/claude/arch/work'); sys.path.insert(0,'/home/claude/v2')
from scripts_test import test
from common2 import tak_pages
# Voynich, EVA glyphs within each line (word spaces removed: sign-to-sign adjacency only)
V=[list(''.join(l)) for p in tak_pages().values() for l in p]
# Rohonc, machine sign codes within each line, coarse 60-class version to blunt over-splitting
exec(open('/home/claude/rohonc/work/repeat.py').read().split("import os;")[0].replace("Dd=pickle.load(open('oh_trans.pkl'","Dd=pickle.load(open('/home/claude/rohonc/work/oh_trans.pkl'").replace("D=pickle.load(open('rohonc_signs.pkl'","D=pickle.load(open('/home/claude/rohonc/work/rohonc_signs.pkl'"))
RO=[[coarse[60][b['code']] for b in L] for P in LINES for L in P]
R=json.load(open('scripts_results.json'))
R['Voynich (EVA glyphs)']=test(V,n=200); R['Rohonc (machine signs, 60 classes)']=test(RO,n=200)
for k in ('Voynich (EVA glyphs)','Rohonc (machine signs, 60 classes)'):
    v=R[k]; print(f"{k:36s} units {v['units']:6d} same-twice {v['exact']:.2f}x (p_hi {v['p_hi']:.3f}, p_lo {v['p_lo']:.3f})")
json.dump(R,open('scripts_results.json','w'),indent=1)
