import sys,re,pickle; sys.path.insert(0,'/home/claude/v2')
from feats2 import process
from common2 import ZL
H=open('herbal.txt').read().split()
def zl_count(p):
    n=0
    for l in open(ZL,errors='ignore'):
        m=re.match(r'<(f\d+[rv]\d*)\.\d+,.(\w+)>\s*(.*)',l)
        if m and m.group(1)==p:
            t=re.sub(r'<[^>]*>','',m.group(3)); n+=len([w for w in re.split(r'[.,\s]+',t) if re.search('[a-z?]',w)])
    return n
d=process(H,'herbal_all.pkl')
keep=[]
for p in H:
    z=zl_count(p); r=d[p]['nwords']/max(1,z)
    if 0.8<=r<=1.25 and z>=40: keep.append(p)
print(f"pages passing QC: {len(keep)}/{len(H)}")
pickle.dump({p:d[p] for p in keep},open('herbal_qc.pkl','wb'))
