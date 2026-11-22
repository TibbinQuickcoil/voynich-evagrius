import random,re
CHUNKS=['cth','ckh','cph','cfh','aiin','ain','iin','qo','ch','sh','ee','dy','ol','or','al','ar','am']
CLASSES=[['k','t','p','f'],['ch','sh','cth','ckh','cph','cfh'],['o','a','y'],['e','ee'],['d','l','r','s'],
         ['aiin','ain','iin','ar','or','al','ol','dy','y','am']]
CLS={t:c for c in CLASSES for t in c}
ENDS=['aiin','ain','dy','y','ol','or','al','ar']; PREF=['qo','o','ch','d','sh']
def tok(w):
    out=[];i=0
    while i<len(w):
        for u in CHUNKS:
            if w.startswith(u,i): out.append(u); i+=len(u); break
        else: out.append(w[i]); i+=1
    return out
def mutate(w,R,P):
    for _ in range(12):
        s=_mutate(w,R,P)
        if legal(s): return s
    return w
def _mutate(w,R,P):
    t=tok(w)
    n=1 if R.random()<P['one'] else 2
    for _ in range(n):
        r=R.random()
        if r<P['sub'] and t:
            j=R.randrange(len(t)); c=CLS.get(t[j])
            if c: t[j]=R.choice(c)
        elif r<P['sub']+P['pre']:
            if len(t)>2 and R.random()<.5: t=t[1:]
            else: t=[R.choice(PREF)]+t
        else:
            if len(t)>2 and t[-1] in ENDS and R.random()<.5: t=t[:-1]
            else: t=t+[R.choice(ENDS)] if t and t[-1] not in ENDS else t[:-1]+[R.choice(ENDS)]
    s=''.join(t)
    if len(s)>8 and R.random()<P.get('shrink',.6): s=''.join(tok(s)[1:]) if R.random()<.5 else ''.join(tok(s)[:-1])
    return s if 1<=len(s)<=11 else ''.join(tok(w)[:3])
import collections as _c
def _legal_model(th=8):
    import sys; sys.path.insert(0,'/home/claude'); from metrics import load_voynich
    W=[w for p in load_voynich() for l in p for w in l[1:-1]]
    tg=_c.Counter(t for w in W for t in zip('^^'+w,'^'+w+'$',w+'$$'))
    return {t for t,c in tg.items() if c>=th}
LEGAL=_legal_model()
def set_legal(th):
    global LEGAL; LEGAL=_legal_model(th)
BENCH={'ch','sh','cth','ckh','cph','cfh'}
def legal(w): return 1<=len(w)<=10 and all(t in LEGAL for t in zip('^^'+w,'^'+w+'$',w+'$$')) and sum(x in BENCH for x in tok(w))<=2
SEED=['daiin','ol','chedy','aiin','shedy','chol','or','ar','qokeey','dar','okaiin','shey']
def scribe(P,pages=211,lines_per=18,words_per=8.5,seed=1):
    R=random.Random(seed); book=[]; prev_line=list(SEED); memory=[]
    for _ in range(pages):
        page=[]
        for li in range(lines_per):
            n=max(3,int(R.gauss(words_per,2))); line=[]
            for j in range(n):
                r=R.random()
                if line and r<P['p_line']:            # copy from recent words on this line
                    src=line[-min(len(line),R.randint(1,P['win']))]
                elif R.random()<P.get('p_far',.1) and len(memory)>50:
                    src=R.choice(memory)                # flips back through the book
                else:                                   # copy from line above, near same position
                    k=min(len(prev_line)-1,max(0,j+R.randint(-2,2))); src=prev_line[k]
                if R.random()<P.get('p_combo',0) and len(memory)>50:
                    other=R.choice(line[-3:]+prev_line) if R.random()<.7 else R.choice(memory)
                    a,b=tok(src),tok(other); cand=''.join(a[:max(1,len(a)//2)]+b[len(b)//2:])
                    w=cand if legal(cand) else mutate(src,R,P)
                else:
                    w=src if R.random()<P['p_exact'] else mutate(src,R,P)
                line.append(w)
            core=list(line)                              # memory keeps bare words
            # line habits are surface flourishes only
            if R.random()<P['open']: line[0]=R.choice('pt')+line[0].lstrip('ktpfcsh')
            if R.random()<P['close']: line[-1]=re.sub(r'(aiin|ain|iin|dy|y|ol|or|al|ar)$','',line[-1])+'am'
            page.append(line); prev_line=core; memory.extend(core)
        book.append(page)
    return book
