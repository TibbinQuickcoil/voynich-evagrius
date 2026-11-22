import cv2,numpy as np,glob,pickle,sys
def page_blobs(path):
    im=cv2.imread(path); g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY).astype(np.float32)
    parch=(cv2.GaussianBlur(g,(0,0),12)>95).astype(np.uint8)            # parchment vs black surround
    parch=cv2.erode(parch,np.ones((25,25),np.uint8))                     # stay clear of the ragged edges
    bg=cv2.medianBlur(g.astype(np.uint8),41).astype(np.float32)+1
    ink=((g/bg)<0.62).astype(np.uint8)*parch
    n,lab,st,cen=cv2.connectedComponentsWithStats(ink,8)
    comps=[dict(x=st[i,0],y=st[i,1],w=st[i,2],h=st[i,3],a=st[i,4],id=i) for i in range(1,n)
           if st[i,4]>=12 and st[i,3]<=45 and st[i,2]<=60 and not (st[i,2]>40 and st[i,3]>38)]
    # merge pieces of one sign: strong horizontal overlap and close vertically (dots over strokes, broken strokes)
    comps.sort(key=lambda c:c['x']); out=[]
    for c in comps:
        for b in out:
            ov=min(b['x']+b['w'],c['x']+c['w'])-max(b['x'],c['x'])
            gap=max(b['y'],c['y'])-min(b['y']+b['h'],c['y']+c['h'])
            if ov>0.6*min(b['w'],c['w']) and gap<6 and max(b['y']+b['h'],c['y']+c['h'])-min(b['y'],c['y'])<=40:
                x0=min(b['x'],c['x']);y0=min(b['y'],c['y']);x1=max(b['x']+b['w'],c['x']+c['w']);y1=max(b['y']+b['h'],c['y']+c['h'])
                b.update(x=x0,y=y0,w=x1-x0,h=y1-y0,ids=b['ids']+[c['id']],a=b['a']+c['a']); break
        else: out.append(dict(c,ids=[c['id']]))
    out=[b for b in out if b['h']>=8 and b['a']>=25]                      # drop specks
    feats=[]
    for b in out:
        crop=np.isin(lab[b['y']:b['y']+b['h'],b['x']:b['x']+b['w']],b['ids']).astype(np.uint8)*255
        s=max(b['w'],b['h'])+4; pad=np.zeros((s,s),np.uint8); oy=(s-b['h'])//2; ox=(s-b['w'])//2
        pad[oy:oy+b['h'],ox:ox+b['w']]=crop
        b['img']=cv2.resize(pad,(32,32),interpolation=cv2.INTER_AREA)
    return im,out
if __name__=='__main__':
    im,B=page_blobs('/home/claude/rohonc/pages/p-050.jpg'); print("signs found",len(B))
    vis=im.copy()
    for b in B: cv2.rectangle(vis,(int(b['x']),int(b['y'])),(int(b['x']+b['w']),int(b['y']+b['h'])),(0,0,255),1)
    cv2.imwrite('/home/claude/rohonc/work/check050.jpg',vis)
