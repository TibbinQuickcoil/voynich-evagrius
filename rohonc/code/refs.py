import numpy as np,cv2,pickle
from PIL import Image,ImageDraw,ImageFont
from skimage.morphology import skeletonize
F='/home/claude/rohonc/fonts/'
SCRIPTS={
 'Coptic':('NotoSansCoptic',list(range(0x2C80,0x2CB2,2))+list(range(0x03E2,0x03F0,2))),
 'Greek':('NotoSans',[c for c in range(0x0391,0x03AA) if c!=0x03A2]),
 'Latin':('NotoSans',list(range(0x41,0x5B))),
 'Phoenician':('NotoSansPhoenician',list(range(0x10900,0x10916))),
 'Aramaic (Imperial)':('NotoSansImperialAramaic',list(range(0x10840,0x10856))),
 'Hebrew':('NotoSansHebrew',list(range(0x05D0,0x05EB))),
 'Old Italic':('NotoSansOldItalic',list(range(0x10300,0x1031F))),
 'Gothic':('NotoSansGothic',list(range(0x10330,0x1034B))),
 'Old Hungarian':('NotoSansOldHungarian',list(range(0x10C80,0x10CB3))),
 'Glagolitic':('NotoSansGlagolitic',list(range(0x2C00,0x2C2F))),
}
def norm(binimg):
    """skeleton redrawn at uniform width, padded square, 32x32, blurred"""
    ys,xs=np.nonzero(binimg)
    if len(ys)==0: return None
    crop=binimg[ys.min():ys.max()+1,xs.min():xs.max()+1]
    h,w=crop.shape; s=max(h,w)+4; pad=np.zeros((s,s),np.uint8); pad[(s-h)//2:(s-h)//2+h,(s-w)//2:(s-w)//2+w]=crop
    im=cv2.resize(pad.astype(np.uint8)*255,(64,64),interpolation=cv2.INTER_AREA)>100
    sk=skeletonize(im).astype(np.uint8)*255
    sk=cv2.dilate(sk,np.ones((5,5),np.uint8))
    v=cv2.GaussianBlur(cv2.resize(sk,(32,32),interpolation=cv2.INTER_AREA).astype(np.float32),(0,0),1.2)
    v=v.ravel()-v.mean(); return v/(np.linalg.norm(v)+1e-6)
def render(fontfile,cp):
    f=ImageFont.truetype(F+fontfile+'.ttf',96); img=Image.new('L',(200,200),0); d=ImageDraw.Draw(img)
    d.text((40,30),chr(cp),font=f,fill=255); a=np.array(img)>128
    return a if a.sum()>30 else None
R={}
for name,(ff,cps) in SCRIPTS.items():
    letters=[]
    for cp in cps:
        a=render(ff,cp)
        if a is not None: letters.append((cp,a,norm(a)))
    R[name]=letters; print(f"{name:20s} {len(letters)} letters")
pickle.dump({k:[(cp,a,v) for cp,a,v in L] for k,L in R.items()},open('refs.pkl','wb'))
# contact sheet of references
rows=[]
for name,L in R.items():
    tiles=[cv2.resize((a[20:180,20:180]*255).astype(np.uint8),(28,28)) for _,a,_ in L][:51]
    row=np.full((30,30*52),0,np.uint8)
    for i,t in enumerate(tiles): row[1:29,30*(i+1)+1:30*(i+1)+29]=t
    cv2.putText(row,name[:3],(1,20),cv2.FONT_HERSHEY_SIMPLEX,0.35,255,1); rows.append(row)
cv2.imwrite('refs_sheet.png',255-np.vstack(rows))
