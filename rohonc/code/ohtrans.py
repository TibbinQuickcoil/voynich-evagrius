import sys,pickle,re,unicodedata,collections,numpy as np; sys.path.insert(0,'.')
from refs import norm
from wordfreq import top_n_list, word_frequency
D=pickle.load(open('rohonc_signs.pkl','rb')); R=pickle.load(open('refs.pkl','rb'))
SOUND={'A':'a','AA':'á','EB':'b','AMB':'mb','EC':'c','ENC':'nc','ECS':'cs','ED':'d','AND':'nd','E':'e','CLOSE E':'e','EE':'é','EF':'f','EG':'g','EGY':'gy','EH':'h','I':'i','II':'í','EJ':'j','EK':'k','AK':'k','UNK':'nk','EL':'l','ELY':'ly','EM':'m','EN':'n','ENY':'ny','O':'o','OO':'ó','NIKOLSBURG OE':'ö','RUDIMENTA OE':'ö','OEE':'ő','EP':'p','EMP':'mp','ER':'r','SHORT ER':'r','ES':'s','ESZ':'sz','ET':'t','ENT':'nt','ETY':'ty','ECH':'ch','U':'u','UU':'ú','NIKOLSBURG UE':'ü','RUDIMENTA UE':'ü','EV':'v','EZ':'z','EZS':'zs','ENT-SHAPED SIGN':'nt','US':'us'}
OH=[(cp,v) for cp,_,v in R['Old Hungarian']]
snd={cp:SOUND[unicodedata.name(chr(cp)).replace('OLD HUNGARIAN CAPITAL LETTER ','')] for cp,_ in OH}
# 1) nearest Old Hungarian letter for every invented sign code, by shape
P=D['proto']; MAP={}
for c,img in P.items():
    v=norm(img>127)
    if v is None: continue
    s=[(float(v@x),cp) for cp,x in OH]; best=max(s); MAP[c]=(best[1],best[0])
# 2) reading order: per spread split at gutter, lines by y, right to left
B=D['B']; pages=collections.defaultdict(list)
for b in B:
    if b['code'] in MAP: pages[b['page']].append(b)
lines=[]
for p in sorted(pages):
    bl=pages[p]; mid=np.median([b['x']+b['w']/2 for b in bl])
    for side,sel in (('L',[b for b in bl if b['x']+b['w']/2<mid]),('R',[b for b in bl if b['x']+b['w']/2>=mid])):
        sel=sorted(sel,key=lambda b:b['y']+b['h']/2); cur=[]; last=None
        for b in sel:
            cy=b['y']+b['h']/2
            if last is not None and cy-last>18: lines.append((p,side,cur)); cur=[]
            cur.append(b); last=cy if last is None else 0.7*last+0.3*cy
        if cur: lines.append((p,side,cur))
def render(L):
    L=sorted(L,key=lambda b:-(b['x']+b['w']))                     # right to left
    out_oh=[];out_lat=[];units=[]
    for i,b in enumerate(L):
        if i and (L[i-1]['x']-(b['x']+b['w']))>14: out_oh.append(' '); out_lat.append(' ')
        cp=MAP[b['code']][0]; out_oh.append(chr(cp)); out_lat.append(snd[cp]); units.append(b['code'])
    return ''.join(out_oh),''.join(out_lat),units
T=[(p,s,*render(L)) for p,s,L in lines if len(L)>=4]
print("lines",len(T),"signs",sum(len(t[4]) for t in T))
pickle.dump(dict(MAP=MAP,snd=snd,T=T),open('oh_trans.pkl','wb'))
with open('rohonc_old_hungarian.txt','w') as o:
    o.write("# Rohonc Codex, shape-mapped to the nearest Old Hungarian letter (NOT a reading).\n# spread/side | Old Hungarian letters (read right to left) | sound values of those letters\n")
    for p,s,oh,lat,_ in T: o.write(f"{p}{s}\t{oh}\t{lat}\n")
print(open('rohonc_old_hungarian.txt').read().splitlines()[2:10])
