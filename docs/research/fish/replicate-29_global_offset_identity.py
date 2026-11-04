"""Replicate 29, comparison step: the whole-sequence statistic the recorded claim used,
implemented here independently. max over offsets k=1..80 of mean(s[i]==s[i+k]),
vs composition-preserving permutations. Usage: python3 -I this.py <dir with *.fasta>"""
import sys, os, numpy as np
def rd(p):
    L = open(p).read().splitlines(); return "".join(L[1:])
f = lambda x: max((x[:-k] == x[k:]).mean() for k in range(1, 81))
for a, n in [("Q6PFU3", "kcnk5b"), ("E7F5V5", "and1"), ("A0ACM8QEN9", "and2")]:
    s = np.array(list(rd(os.path.join(sys.argv[1], a + ".fasta")))); o = f(s)
    for seed, N in [(29, 200), (7, 2000)]:
        rng = np.random.default_rng(seed); nl = np.array([f(rng.permutation(s)) for _ in range(N)])
        print(n, seed, N, "obs=%.4f null_mean=%.4f null_max=%.4f p=%.4f" % (o, nl.mean(), nl.max(), (1 + (nl >= o).sum()) / (N + 1)))
