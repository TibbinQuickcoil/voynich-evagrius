import re,sys,numpy as np; sys.path.insert(0,'/home/claude')
from metrics import measure, load_voynich
pages=[];cur=None
for line in open('/home/claude/ext/codex_seraphinianus_ocr/CS_OCR_TRANSLITERATION.txt',errors='ignore'):
    if line.startswith('###PAGE'): cur=[]; pages.append(cur); continue
    if line.startswith('#') or cur is None: continue
    if '?' in line or '...' in line: continue          # drop lines with OCR uncertainty marks
    ws=[w for w in re.split(r'[\s.]+',line.strip()) if re.fullmatch(r'[A-Za-z]{2,}',w)]
    if len(ws)>=3: cur.append(ws)
pages=[p for p in pages if sum(map(len,p))>=60]
print("Seraphinianus pages",len(pages),"lines",sum(map(len,pages)),"words",sum(len(l) for p in pages for l in p))
K=['TTR','zipf','h2','len_mean','exact_ratio_g1','near_ratio_g1','near_ratio_g3','near_ratio_g5','break_near_ratio','page_cluster']
S=[measure(pages,seed=s) for s in range(5)]; V=[measure(load_voynich(),seed=s) for s in range(5)]
print(f"{'metric':17s} {'VOYNICH':>14s} {'SERAPHINIANUS':>15s}")
for k in K:
    v=[float(r[k]) for r in V]; s=[float(r[k]) for r in S]
    print(f"{k:17s} {np.mean(v):7.3f}±{np.std(v):.3f}  {np.mean(s):8.3f}±{np.std(s):.3f}")
