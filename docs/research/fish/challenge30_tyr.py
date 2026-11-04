"""Challenge 30: re-run of the Tyr spatial-clustering shuffle test (computed, not observed).
Usage: python3 -I challenge30_tyr.py and1.fasta and2.fasta kcnk5b.fasta
FASTA from rest.uniprot.org/uniprotkb/{E7F5V5,A0ACM8QEN9,Q6PFU3}.fasta (fetched 2026-11-04).
Statistic (reconstructed): fraction of consecutive-Tyr gaps <= t residues; null = shuffled sequence."""
import random, re, sys
def read(f): return ''.join(l.strip() for l in open(f) if not l.startswith('>'))
def stat(s, t=4, collapse=False):
    if collapse: s = re.sub('Y+', 'Y', s)
    p = [i for i, c in enumerate(s) if c == 'Y']; g = [b - a for a, b in zip(p, p[1:])]
    return sum(x <= t for x in g) / len(g)
def block(s, r, w):
    out = []
    for i in range(0, len(s), w):
        b = list(s[i:i+w]); r.shuffle(b); out += b
    return ''.join(out)
def test(s, n=20000, t=4, seed=1, w=None, collapse=False):
    r = random.Random(seed); o = stat(s, t, collapse)
    v = [stat(block(s, r, w) if w else ''.join(r.sample(s, len(s))), t, collapse) for _ in range(n)]
    m = sum(v)/n; sd = (sum((x-m)**2 for x in v)/(n-1))**.5
    return o, m, (o-m)/sd, (1 + sum(x >= o for x in v))/(n + 1)
if __name__ == '__main__':
    for f in sys.argv[1:]:
        s = read(f)
        for t in (2, 3, 4, 5, 6): print(f, 'full t=%d' % t, *('%.4f' % x for x in test(s, t=t)))
        for w in (100, 50, 20): print(f, 'block%d t=4' % w, *('%.4f' % x for x in test(s, w=w)))
        print(f, 'collapse-runs t=4', *('%.4f' % x for x in test(s, collapse=True)))
