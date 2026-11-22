import pickle,numpy as np,random,collections,cv2,sys; sys.path.insert(0,'/home/claude')
from metrics import lev1
A=pickle.load(open('pairs.pkl','rb'))
def norm(img):
    v=cv2.resize(img,(72,24),interpolation=cv2.INTER_AREA).ravel(); v=v-v.mean(); return v/(np.linalg.norm(v)+1e-6)
for p in A:
    for q in A[p]: q['v']=norm(q['img']); q['wd']=q['img'].shape[1]
def sim(a,b):
    r=max(a['wd'],b['wd'])/min(a['wd'],b['wd'])
    return float(a['v']@b['v'])-0.5*np.log(r)          # shape correlation, penalised for width mismatch
def rel(a,b): return 'same' if a['eva']==b['eva'] else ('near' if lev1(a['eva'],b['eva']) else 'other')
def page_pairs(P,rnd):
    idx={(q['line'],q['word']):q for q in P}; inter=lambda q:0<q['word']<q['nline']-1
    H=[(q,idx[(q['line'],q['word']+1)]) for q in P if inter(q) and (q['line'],q['word']+1) in idx and inter(idx[(q['line'],q['word']+1)])]
    V=[]
    byline=collections.defaultdict(list)
    for q in P: byline[q['line']].append(q)
    for q in P:
        if not inter(q): continue
        nxt=[r for r in byline.get(q['line']+1,[]) if inter(r)]
        if nxt:
            r=max(nxt,key=lambda r:min(q['x1'],r['x1'])-max(q['x0'],r['x0']))
            if min(q['x1'],r['x1'])-max(q['x0'],r['x0'])>0: V.append((q,r))
    Ps=[q for q in P if inter(q)]
    F=[(a,b) for a,b in (rnd.sample(Ps,2) for _ in range(400)) if abs(a['line']-b['line'])>=4]
    return H,V,F
rnd=random.Random(0); pages=list(A)
def stats(sel_pages):
    out={k:collections.defaultdict(list) for k in 'HVF'}
    for p in sel_pages:
        H,V,F=page_pairs(A[p],random.Random(hash(p)%1000))
        for k,L in zip('HVF',(H,V,F)):
            for a,b in L: out[k][rel(a,b)].append(sim(a,b))
    return out
S=stats(pages)
print(f"{'':16s}{'pairs':>7s} {'ink similarity: same':>22s} {'near':>8s} {'other':>8s}   {'lift same-other':>16s}")
for k,name in zip('HVF',('same line (H)','line below (V)','far apart (F)')):
    d=S[k]; n=sum(len(v) for v in d.values())
    print(f"{name:16s}{n:7d} {np.mean(d['same']):22.3f} {np.mean(d['near']):8.3f} {np.mean(d['other']):8.3f}   {np.mean(d['same'])-np.mean(d['other']):16.3f}   (n same={len(d['same'])}, near={len(d['near'])})")
# bootstrap over pages for lifts
B=[]
for _ in range(300):
    sp=[rnd.choice(pages) for _ in pages]; s=stats(sp)
    B.append({k:(np.mean(s[k]['same'])-np.mean(s[k]['other']) if s[k]['same'] else np.nan, np.mean(s[k]['near'])-np.mean(s[k]['other'])) for k in 'HVF'})
for k,name in zip('HVF',('H','V','F')):
    a=np.array([b[k][0] for b in B]); c=np.array([b[k][1] for b in B])
    print(f"{name}: lift(same) 95% CI [{np.nanpercentile(a,2.5):.3f}, {np.nanpercentile(a,97.5):.3f}]   lift(near) 95% CI [{np.percentile(c,2.5):.3f}, {np.percentile(c,97.5):.3f}]")
dv=np.array([b['V'][0]-b['F'][0] for b in B]); dh=np.array([b['H'][0]-b['F'][0] for b in B])
print(f"V minus far, lift(same): 95% CI [{np.nanpercentile(dv,2.5):.3f}, {np.nanpercentile(dv,97.5):.3f}]   H minus far: [{np.nanpercentile(dh,2.5):.3f}, {np.nanpercentile(dh,97.5):.3f}]")
pickle.dump(S,open('ink_stats.pkl','wb'))
