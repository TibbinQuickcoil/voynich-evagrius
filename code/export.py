import sys,pickle,numpy as np,cv2; sys.path.insert(0,'/home/claude/virgin')
import syllabary as S
from sklearn.cluster import MiniBatchKMeans
K=80
lab=MiniBatchKMeans(K,random_state=0,n_init=3,batch_size=4096).fit_predict(S.Z)
# order clusters by frequency, name them S01..S80
order=np.argsort(-np.bincount(lab,minlength=K)); name={c:f"S{i+1:02d}" for i,c in enumerate(order)}
rows={}
for f,l in zip(S.F,lab): rows.setdefault((f['page'],f['line'],f['word']),[]).append((f['x'],name[l]))
with open('voynich_recipes_virgin_K80.tsv','w') as o:
    o.write("# Independent machine transcription of Voynich recipe section (f103r-f116r, excl. f111r/v)\n# No EVA or training labels used. Each symbol S01-S80 is an unsupervised shape cluster (see syllabary sheet).\n# page\tline\tword\tsymbols\n")
    for (p,li,wi),v in sorted(rows.items(),key=lambda k:(int(k[0][0][1:-1]),k[0][0][-1],k[0][1],k[0][2])):
        o.write(f"{p}\t{li+1}\t{wi+1}\t{'.'.join(s for _,s in sorted(v))}\n")
# syllabary sheet: 80 classes x 8 examples, rendered from the binarized crops
cell=28; sheet=np.full((K*cell//2+10,2*(9*cell)+20),255,np.uint8); rng=np.random.default_rng(0)
for i,c in enumerate(order):
    idx=np.where(lab==c)[0]; pick=rng.choice(idx,min(8,len(idx)),replace=False)
    r,col=divmod(i,2); y=r*cell+5; x0=col*(9*cell+10)+5
    cv2.putText(sheet,name[c],(x0,y+18),cv2.FONT_HERSHEY_SIMPLEX,.4,0,1)
    for j,k in enumerate(pick):
        g=(255-S.F[k]['vec'].reshape(20,20)*255).astype(np.uint8)
        sheet[y+2:y+26,x0+cell*(j+1):x0+cell*(j+1)+24]=cv2.resize(g,(24,24),interpolation=cv2.INTER_NEAREST)
cv2.imwrite('syllabary_K80.png',sheet)
print(open('voynich_recipes_virgin_K80.tsv').read()[:600]); print(sheet.shape)
