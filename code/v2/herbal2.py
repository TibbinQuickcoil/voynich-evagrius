import sys,pickle,numpy as np,collections; sys.path.insert(0,'/home/claude/v2')
from sklearn.decomposition import PCA
from sklearn.cluster import MiniBatchKMeans
from herbal import zl_count
rec=pickle.load(open('rec2.pkl','rb')); her=pickle.load(open('herbal_all.pkl','rb'))
FR=[f for d in rec.values() for f in d['feats']]
pca=PCA(40,random_state=0).fit(np.array([f['vec'] for f in FR])); ZR=pca.transform(np.array([f['vec'] for f in FR]))
km=MiniBatchKMeans(80,random_state=0,n_init=3,batch_size=4096).fit(ZR)
dR=np.min(km.transform(ZR),1); thr=np.percentile(dR,95)
out={};rep=[]
for p,d in her.items():
    F=d['feats']
    if not F: continue
    dist=np.min(km.transform(pca.transform(np.array([f['vec'] for f in F]))),1)
    words=collections.defaultdict(list)
    for f,ds in zip(F,dist): words[(f['line'],f['word'])].append(ds<=thr)
    good={k for k,v in words.items() if np.mean(v)>=0.8}
    lines=collections.Counter(k[0] for k in good); goodlines={l for l,c in lines.items() if c>=3}
    keepF=[f for f in F if (f['line'],f['word']) in good and f['line'] in goodlines]
    nw=len({(f['line'],f['word']) for f in keepF}); z=zl_count(p); rep.append((p,nw,z))
    out[p]=dict(nwords=nw,feats=keepF,zl=z)
ok={p:v for p,v in out.items() if v['zl']>=40 and 0.8<=v['nwords']/v['zl']<=1.25}
print("pages passing QC:",len(ok),"/",len(out))
import statistics; print("median machine/ZL ratio after filter: %.2f"%statistics.median(n/max(z,1) for _,n,z in rep))
pickle.dump(ok,open('herbal_qc.pkl','wb')); pickle.dump((pca,km),open('rec_model.pkl','wb'))
