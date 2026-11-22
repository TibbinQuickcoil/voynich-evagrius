import sys,glob,pickle,numpy as np,cv2; sys.path.insert(0,'.')
from segr import page_blobs
from sklearn.decomposition import PCA
from sklearn.cluster import MiniBatchKMeans
B=[]
for p in sorted(glob.glob('/home/claude/rohonc/pages/p-*.jpg')):
    _,bl=page_blobs(p)
    if len(bl)<60: continue                                   # covers, blank leaves
    for b in bl: B.append(dict(page=p[-7:-4],x=b['x'],y=b['y'],w=b['w'],h=b['h'],img=b['img']))
print("spreads used",len({b['page'] for b in B}),"sign blobs",len(B))
X=np.array([cv2.GaussianBlur(b['img'].astype(np.float32)/255,(0,0),1.0).ravel() for b in B])
pca=PCA(40,random_state=0).fit(X); Z=pca.transform(X)
K=150; km=MiniBatchKMeans(K,random_state=0,n_init=3,batch_size=4096).fit(Z); lab=km.labels_
order=np.argsort(-np.bincount(lab,minlength=K)); name={c:f"R{i+1:03d}" for i,c in enumerate(order)}
for b,l in zip(B,lab): b['code']=name[l]
# mean image per invented sign (what gets compared to other scripts)
proto={name[c]:np.mean([B[i]['img'] for i in np.where(lab==c)[0]],axis=0) for c in range(K)}
counts={name[c]:int((lab==c).sum()) for c in range(K)}
pickle.dump(dict(B=[{k:v for k,v in b.items()} for b in B],proto=proto,counts=counts),open('rohonc_signs.pkl','wb'))
# sheet: 150 codes x 6 examples
cell=36; cols=3; per=7; W=cols*(per*cell+60); H=(K//cols+1)*cell; sheet=np.full((H,W),255,np.uint8); rng=np.random.default_rng(0)
for i,c in enumerate(order):
    idx=np.where(lab==c)[0]; pick=rng.choice(idx,min(6,len(idx)),replace=False)
    r,col=divmod(i,cols); y=r*cell+2; x0=col*(per*cell+60)
    cv2.putText(sheet,name[c],(x0+2,y+22),cv2.FONT_HERSHEY_SIMPLEX,0.38,0,1)
    for j,k in enumerate(pick): sheet[y:y+32,x0+60+j*cell:x0+60+j*cell+32]=255-B[k]['img']
cv2.imwrite('rohonc_signs_sheet.png',sheet); print(sheet.shape)
