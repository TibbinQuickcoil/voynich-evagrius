import sys,re; sys.path.insert(0,'/home/claude/v2'); sys.path.insert(0,'/home/claude/v3')
from common2 import perm
from controls import wrap
L='/home/claude/zl/vu/voynich_decipherment_repro_bundle/decipherment_attack_v6/lm_corpora/'
for f in ('lm_italian','lm_german','lm_french','lm_hebrew'):
    t=re.sub(r'[^\w\s]',' ',open(L+f+'.txt',errors='ignore').read().lower()); w=[x for x in t.split() if x.isalpha()][:38000]
    r=perm(wrap(w),n=200); print(f"{f:12s} words {len(w)}  next-word exact {r['H exact'][0]:.2f}x  near {r['H near'][0]:.2f}x  line-below near {r['V near'][0]:.2f}x")
