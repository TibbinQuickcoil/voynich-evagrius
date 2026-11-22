import sys,pickle,random,collections,numpy as np; sys.path.insert(0,'/home/claude/v2'); sys.path.insert(0,'/home/claude')
from metrics import lev1
from common2 import zl_pages, zl_meta, perm, fmt
pca,km=pickle.load(open('rec_model.pkl','rb'))
def sparse_pages(data):
    """page -> list of lines; each line = dict(word_index -> spelling), using the recipe-trained syllabary"""
    out={}
    for p,d in data.items():
        F=d['feats']
        if not F: continue
        lab=km.predict(pca.transform(np.array([f['vec'] for f in F])))
        W=collections.defaultdict(list)
        for f,l in zip(F,lab): W[(f['line'],f['word'])].append((f['x'],chr(0x4E00+l)))
        L=collections.defaultdict(dict)
        for (li,wi),v in W.items(): L[li][wi]=''.join(s for _,s in sorted(v))
        out[p]=[L[k] for k in sorted(L)]
    return out
def counts(pages):
    h=[0,0,0]; v=[0,0,0]
    for p in pages:
        for l in p:
            ks=sorted(l); 
            for a in ks:
                if a+1 in l and a>min(ks) and a+1<max(ks): x,y=l[a],l[a+1]; h[0]+=1; h[1]+=x==y; h[2]+=lev1(x,y)
        for A,B in zip(p,p[1:]):
            if not A or not B: continue
            na,nb=max(A)+1,max(B)+1
            for i,w in A.items():
                j=round(i*(nb-1)/max(1,na-1))
                if j in B and 0<i<max(A) and 0<j<max(B): v[0]+=1; v[1]+=w==B[j]; v[2]+=lev1(w,B[j])
    return h,v
def shuf(pages,rnd):
    o=[]
    for p in pages:
        keys=[(li,wi) for li,l in enumerate(p) for wi in l if l and min(l)<wi<max(l)]   # interior only
        vals=[p[li][wi] for li,wi in keys]; rnd.shuffle(vals)
        q=[dict(l) for l in p]
        for (li,wi),w in zip(keys,vals): q[li][wi]=w
        o.append(q)
    return o
def ptest(pages,n=300):
    (h,v)=counts(pages); rnd=random.Random(3); S=[counts(shuf(pages,rnd)) for _ in range(n)]; R={}
    for lab,real,idx,k in [('H near',h,0,2),('H exact',h,0,1),('V near',v,1,2),('V exact',v,1,1)]:
        null=np.array([s[idx][k] for s in S]); R[lab]=(real[k]/null.mean(),(1+(null>=real[k]).sum())/(1+n))
    R['pairs']=(h[0],v[0]); return R
def show(name,R):
    print(f"{name:30s} pairs H{R['pairs'][0]:5d} V{R['pairs'][1]:5d} | H-near {R['H near'][0]:.2f}x p={R['H near'][1]:.3f} | H-exact {R['H exact'][0]:.2f}x p={R['H exact'][1]:.3f} | V-near {R['V near'][0]:.2f}x p={R['V near'][1]:.3f} | V-exact {R['V exact'][0]:.2f}x p={R['V exact'][1]:.3f}")
if __name__=='__main__':
    her=pickle.load(open('herbal_qc.pkl','rb')); rec=pickle.load(open('rec2.pkl','rb'))
    SP=sparse_pages(her); SR=sparse_pages(rec)
    A=[SP[p] for p in SP if her[p]['L']=='A']; B=[SP[p] for p in SP if her[p]['L']=='B']
    print(f"MACHINE (virgin, recipe-trained 80-symbol syllabary)")
    show(f"herbal A, scribe 1 ({len(A)} pp)",ptest(A)); show(f"herbal B ({len(B)} pp)",ptest(B)); show("recipes (B, 20 pp)",ptest(list(SR.values())))
    Z=zl_pages(set(her)); 
    print("HUMAN (Zandbergen-Landini) on the same herbal pages")
    for L in 'AB': print("  "+fmt(f"herbal {L}",perm({p:v for p,v in Z.items() if her[p]['L']==L})))
