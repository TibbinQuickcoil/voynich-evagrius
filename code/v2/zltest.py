from common2 import *
REC=[f"f{n}{s}" for n in range(103,117) for s in 'rv' if f"f{n}{s}" not in ('f111r','f111v','f116v')]
print(fmt("Takahashi, recipe pages",perm(tak_pages(REC))))
print(fmt("Zandbergen-Landini, recipe pages",perm(zl_pages(REC))))
print(fmt("Takahashi, whole book",perm(tak_pages(),n=200)))
print(fmt("Zandbergen-Landini, whole book",perm(zl_pages(),n=200)))
M=zl_meta(); Z=zl_pages()
for L in 'AB':
    print(fmt(f"ZL, Currier {L} pages",perm({k:v for k,v in Z.items() if M.get(k,{}).get('L')==L},n=200)))
