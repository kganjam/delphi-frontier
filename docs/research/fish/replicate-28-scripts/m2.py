def rd(f): return ''.join(l.strip() for l in open(f) if not l.startswith('>'))
k=rd('dl/Q6PFU3.fasta'); a=rd('dl/A0ACM8QEN9.fasta')
D='ARGQSPEK'; O='WCFIYVLN'
def f(s): n=len(s); d=sum(c in D for c in s)/n; o=sum(c in O for c in s)/n; return d,o,d-o
for lab,s in (('kcnk5b',k),('and2',a),('and2 24-end',a[23:]),('kcnk5b 251-end',k[250:]),('kcnk5b 262-end',k[261:])):
    d,o,x=f(s); print(f"{lab:16s} n={len(s)} fD={d:.4f} fO={o:.4f} fD-fO={x:+.4f}")
