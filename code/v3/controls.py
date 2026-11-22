import sys,random,numpy as np; sys.path.insert(0,'/home/claude/v2'); sys.path.insert(0,'/home/claude')
from common2 import perm, zl_pages
from metrics import measure
C='/home/claude/zl/vu/data/controls/'
def from_lines(lines,per_page=20):
    lines=[l for l in lines if len(l)>=3]; return {i:lines[i:i+per_page] for i in range(0,len(lines),per_page)}
def wrap(tokens,per_line=9,per_page=20):
    L=[tokens[i:i+per_line] for i in range(0,len(tokens),per_line)]; return from_lines(L,per_page)
def read_lines(f): return [l.split() for l in open(f) if l.strip()]
corp={}
corp['Voynich (ZL, whole book)']=zl_pages()
for s in (1,2,3): corp[f'Timm-Schinner self-citation, seed {s}']=from_lines(read_lines(C+f'selfcitation/selfcite_seed{s}.txt'))
ct=open(C+'naibbe/greshko_nathist_output_ciphertext.txt').read().split(); pt=open(C+'naibbe/greshko_nathist_pre_encryption_respaced_plaintext.txt').read().split()
corp['Naibbe cipher of Pliny (Greshko)']=wrap(ct)
corp['   same Pliny, plaintext chunks']=wrap(pt)
corp['Naibbe cipher of Caesar']=from_lines(read_lines(C+'naibbe/naibbe_caesar_ciphertext_lines.txt'))
import json; R={}
for k,P in corp.items():
    r=perm(P,n=200); m=measure(list(P.values())); R[k]=(r,m)
    print(f"{k:40s} H-near {r['H near'][0]:.2f}x p={r['H near'][1]:.3f} | H-exact {r['H exact'][0]:.2f}x p={r['H exact'][1]:.3f} | V-near {r['V near'][0]:.2f}x p={r['V near'][1]:.3f} | V-exact {r['V exact'][0]:.2f}x | TTR {m['TTR']:.3f} h2 {m['h2']:.2f} zipf {m['zipf']:.2f} len {m['len_mean']:.2f}")
import pickle; pickle.dump(R,open('controls.pkl','wb'))
