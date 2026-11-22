import sys,pickle; sys.path.insert(0,'/home/claude'); sys.path.insert(0,'/home/claude/v2'); sys.path.insert(0,'/home/claude/v3')
from common2 import perm, zl_pages, tak_pages
from common import baselines
exec(open('/home/claude/sera.py').read().split("K=[")[0])
from controls import wrap, from_lines, read_lines, C
rows=[]
B=baselines(229489)
for k in ('Latin: Pliny NH','Latin: Vulgate','English: Moby Dick'):
    rows.append((k,'real language',perm(wrap(B[k].split()),n=200)))
ct=open(C+'naibbe/greshko_nathist_output_ciphertext.txt').read().split()
rows.append(('Naibbe cipher of Pliny','cipher of real language',perm(wrap(ct),n=200)))
rows.append(('Naibbe cipher of Caesar','cipher of real language',perm(from_lines(read_lines(C+'naibbe/naibbe_caesar_ciphertext_lines.txt')),n=200)))
rows.append(('Timm-Schinner generator (seed 1)','generated nonsense',perm(from_lines(read_lines(C+'selfcitation/selfcite_seed1.txt')),n=200)))
rows.append(('Codex Seraphinianus (OCR)','human nonsense',perm(pages,n=200)))
rows.append(('Voynich, Takahashi','Voynich',perm(tak_pages(),n=200)))
rows.append(('Voynich, Zandbergen-Landini','Voynich',perm(zl_pages(),n=200)))
for n,g,r in rows: print(f"{n:34s} {g:24s} exact {r['H exact'][0]:.2f}x p={r['H exact'][1]:.3f}  near {r['H near'][0]:.2f}x")
pickle.dump([(n,g,r['H exact'][0],r['H near'][0]) for n,g,r in rows],open('headline.pkl','wb'))
