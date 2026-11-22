import re,glob,random,collections,json,sys,numpy as np; sys.path.insert(0,'/home/claude')
import xml.etree.ElementTree as ET
from metrics import lev1
rnd=random.Random(0)
def lev1s(a,b):  # one unit different, for tuple sequences
    if a==b: return False
    if len(a)==len(b): return sum(x!=y for x,y in zip(a,b))==1
    if abs(len(a)-len(b))!=1: return False
    if len(a)>len(b): a,b=b,a
    return any(b[:i]+b[i+1:]==a for i in range(len(b)))
def test(groups,near=False,n=500):
    """groups: list of sequences (units are hashable). adjacency within group; null = shuffle within group."""
    groups=[g for g in groups if len(g)>=3]
    def cnt(G):
        e=nr=t=0
        for g in G:
            for a,b in zip(g,g[1:]): t+=1; e+=a==b; nr+=(lev1s(a,b) if near else 0)
        return e,nr,t
    e,nr,t=cnt(groups); E=[];N=[]
    for _ in range(n):
        G=[rnd.sample(g,len(g)) for g in groups]; x=cnt(G); E.append(x[0]); N.append(x[1])
    E=np.array(E);N=np.array(N)
    out=dict(pairs=t,units=sum(map(len,groups)),exact=e/E.mean() if E.mean() else float('nan'),p_hi=(1+(E>=e).sum())/(n+1),p_lo=(1+(E<=e).sum())/(n+1))
    if near: out.update(near=nr/N.mean(),pn_hi=(1+(N>=nr).sum())/(n+1),pn_lo=(1+(N<=nr).sum())/(n+1))
    return out
R={}
def run():
    # --- rongorongo: glyph sequences per line, split at unreadable glyphs
    rr_full=[];rr_base=[]
    for f in sorted(glob.glob('/home/claude/arch/rr/*.xml')):
        for line in ET.parse(f).getroot().iter('line'):
            seq=[g.findtext('code') or '_' for g in line.iter('glyph')]; cur=[]
            for c in seq+['_']:
                c=c.replace('!','').replace('?','')
                if c in('_','') or not re.match(r'\d',c):
                    if cur: rr_full.append(cur); rr_base.append([x[:3] for x in cur]); cur=[]
                else: cur.append(c)
    R['Rongorongo, glyphs (full codes)']=test(rr_full)
    R['Rongorongo, glyphs (base codes)']=test(rr_base)
    # --- Linear A / B: multi-sign syllabic words per inscription; and their signs
    def linear(path,lower):
        s=open(path).read(); out_w=[];out_s=[]
        for block in re.findall(r'"transliteratedWords": \[(.*?)\]',s,flags=re.S):
            items=re.findall(r'"((?:[^"\\]|\\.)*)"',block)
            pat=r'^[a-z0-9₂₃]+(-[a-z0-9₂₃]+)+$' if lower else r'^[A-Z0-9₂₃]+(-[A-Z0-9₂₃]+)+$'
            ws=[tuple(w.split('-')) for w in items if re.match(pat,w)]
            if ws: out_w.append(ws); out_s.append([x for w in ws for x in w])
        return out_w,out_s
    LAw,LAs=linear('/home/claude/arch/lineara.xyz/LinearAInscriptions.js',False)
    LBw,LBs=linear('/home/claude/arch/linearb.xyz/LinearBInscriptions.js',True)
    R['Linear A, words']=test(LAw,near=True); R['Linear A, signs']=test(LAs)
    R['Linear B (Greek), words']=test(LBw,near=True); R['Linear B (Greek), signs']=test(LBs)
    # --- Maori: syllables and words per sentence
    sents=[l.strip().lower() for f in glob.glob('/home/claude/arch/maori/lists/prompts-tri-*-n-5.txt') for l in open(f) if l.strip()]
    sents=list(dict.fromkeys(sents))
    syl=re.compile(r'(?:ng|wh|[hkmnprtw])?[aeiouāēīōū]')
    MW=[];MS=[]
    for s_ in sents:
        ws=re.findall(r"[a-zāēīōū]+",s_)
        MW.append([tuple(syl.findall(w)) for w in ws]); MS.append([x for w in ws for x in syl.findall(w)])
    R['Maori (Polynesian), words']=test(MW,near=True); R['Maori (Polynesian), syllables']=test(MS)
    for k,v in R.items():
        extra=f"  near {v['near']:.2f}x (p_hi {v['pn_hi']:.3f}, p_lo {v['pn_lo']:.3f})" if 'near' in v else ''
        print(f"{k:34s} units {v['units']:6d} pairs {v['pairs']:6d}  same-twice {v['exact']:.2f}x (p_hi {v['p_hi']:.3f}, p_lo {v['p_lo']:.3f}){extra}")
    json.dump(R,open('scripts_results.json','w'),indent=1)
if __name__=='__main__': run()
