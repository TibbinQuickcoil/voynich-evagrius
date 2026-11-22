import re, math, collections, glob
B='/home/claude/vdata/base'
def norm(t): return re.sub(r'\s+',' ',re.sub(r'[^a-z]+',' ',t.lower())).strip()
def voy_words(path='/home/claude/vdata/voynich/analysis/takahashi_clean.txt'):
    t=open(path).read().replace('*',' ')
    return [w.lower() for w in t.split() if re.fullmatch(r'[A-Za-z]+',w)]
def baselines(n):
    src={'Latin: Vulgate':glob.glob(B+'/lat/bible/*.txt'),
         'Latin: Pliny NH':sorted(glob.glob(B+'/lat/pliny.nh*.txt')),
         'Latin: Varro+Vitruvius':sorted(glob.glob(B+'/lat/varro.rr*.txt')+glob.glob(B+'/lat/vitruvius*.txt')),
         'English: KJV':[B+'/gutenberg/bible-kjv.txt'],
         'English: Moby Dick':[B+'/gutenberg/melville-moby_dick.txt'],
         'English: Austen':[B+'/gutenberg/austen-emma.txt']}
    out={}
    for k,fs in src.items():
        s=norm(' '.join(open(f,errors='ignore').read() for f in sorted(fs)))
        out[k]=s[:n]
    return out
def h_cond(seq):
    c1=collections.Counter(seq); n=len(seq)
    H1=-sum(v/n*math.log2(v/n) for v in c1.values())
    c2=collections.Counter(zip(seq,seq[1:])); n2=n-1
    H2=-sum(v/n2*math.log2(v/n2) for v in c2.values())
    return len(c1),H1,H2-H1
def bpe(seq,k):
    seq=list(seq)
    for _ in range(k):
        c=collections.Counter((a,b) for a,b in zip(seq,seq[1:]) if a!=' ' and b!=' ')
        if not c: break
        (a,b),_=c.most_common(1)[0]; new=a+b; out=[]; i=0
        while i<len(seq):
            if i<len(seq)-1 and seq[i]==a and seq[i+1]==b: out.append(new); i+=2
            else: out.append(seq[i]); i+=1
        seq=out
    return seq
