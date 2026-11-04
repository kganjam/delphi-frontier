"""Replication 30: Tyr spatial clustering in zebrafish actinodin and1/and2.
Metric (inferred, see replicate-30.md): fraction of consecutive Tyr-Tyr gaps <= d residues.
Null: composition-preserving full-sequence shuffles. p = (#null >= obs + 1)/(N + 1).
Usage: python3 -I replicate-30-tyr.py E7F5V5.fasta A0ACM8QEN9.fasta
"""
import random, statistics as st, sys

def load(f): return ''.join(open(f).read().split('\n')[1:])

def gap_metric(s, d=4):
    ys = [i for i, c in enumerate(s) if c == 'Y']
    g = [b - a for a, b in zip(ys, ys[1:])]
    return sum(x <= d for x in g) / len(g)

for name, f in zip(('and1', 'and2'), sys.argv[1:3]):
    s = load(f); obs = gap_metric(s)
    for seed, n in ((99, 2000), (99, 100000)):
        rng = random.Random(seed); L = list(s); null = []
        for _ in range(n):
            rng.shuffle(L); null.append(gap_metric(L))
        mu, sd = st.mean(null), st.pstdev(null)
        p = (sum(x >= obs for x in null) + 1) / (n + 1)
        print(f"{name} N={n} obs={obs:.4f} null={mu:.4f} sd={sd:.4f} z={(obs-mu)/sd:.2f} p={p:.4f}")
