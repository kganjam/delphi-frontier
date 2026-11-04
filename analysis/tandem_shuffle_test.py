#!/usr/bin/env python3
"""Is a protein's internal self-similarity above a composition-preserving shuffle null?

Settles an open disagreement: claim 29 reports "no tandem repeats in any of the three proteins
against a null of 200 composition-preserving shuffles"; two independent replications report that
and1 departs from that null at p about 0.005, naming a period-10 repeat around residues 170-197.

METHOD. For each lag k, count exact matches between seq[i] and seq[i+k] and take the best lag's
match fraction as the statistic. The null permutes the sequence, which preserves composition
EXACTLY -- so any excess is positional structure, not amino-acid bias. Empirical p is the fraction
of shuffles reaching the observed statistic.

SHIPS WITH BOTH CONTROLS, because a shuffle test that cannot separate a planted repeat from noise
proves nothing either way:
  POSITIVE  a synthetic tandem repeat must come back significant
  NEGATIVE  a shuffled copy of the real sequence must NOT

    python3 tandem_shuffle_test.py seq.faa [n_shuffles]
"""
import random
import sys


def read_fasta(path):
    return "".join(l.strip() for l in open(path).read().split("\n")[1:]
                   if l and not l.startswith(">"))


def best_lag_identity(seq, kmin=2, kmax=60):
    """Highest fraction of matching residues over all lags in [kmin, kmax]."""
    best, best_k = 0.0, None
    n = len(seq)
    for k in range(kmin, min(kmax, n - 1) + 1):
        m = sum(1 for i in range(n - k) if seq[i] == seq[i + k])
        f = m / (n - k)
        if f > best:
            best, best_k = f, k
    return best, best_k


def test(seq, n_shuffles, rng):
    obs, k = best_lag_identity(seq)
    chars = list(seq)
    ge = 0
    null = []
    for _ in range(n_shuffles):
        rng.shuffle(chars)
        s, _ = best_lag_identity("".join(chars))
        null.append(s)
        if s >= obs:
            ge += 1
    p = (ge + 1) / (n_shuffles + 1)        # add-one, so p is never reported as exactly 0
    return obs, k, p, max(null)


def main():
    path = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    rng = random.Random(29)

    print("CONTROLS FIRST — a test that cannot separate these proves nothing.\n")
    planted = ("ACDEFGHIKL" * 6) + "".join(rng.choice("ACDEFGHIKLMNPQRSTVWY") for _ in range(120))
    o, k, p, mx = test(planted, n, rng)
    print(f"  POSITIVE (planted period-10 repeat): best lag {k}, identity {o:.4f}, "
          f"shuffle max {mx:.4f}, p = {p:.4f}  {'PASS' if p <= 0.05 else 'FAIL'}")
    if p > 0.05:
        print("  CONTROL FAILED: the test cannot see a planted repeat."); return 1

    seq = read_fasta(path)
    shuf = list(seq); rng.shuffle(shuf)
    o2, k2, p2, _ = test("".join(shuf), n, rng)
    print(f"  NEGATIVE (this sequence, shuffled):  best lag {k2}, identity {o2:.4f}, "
          f"p = {p2:.4f}  {'PASS' if p2 > 0.05 else 'FAIL'}")
    if p2 <= 0.05:
        print("  CONTROL FAILED: the test calls shuffled input significant."); return 1

    print(f"\nTEST — {path}, {len(seq)} residues, {n} composition-preserving shuffles")
    obs, k, p, mx = test(seq, n, rng)
    print(f"  best lag {k}, self-identity {obs:.4f}, shuffle maximum {mx:.4f}")
    print(f"  empirical p = {p:.4f}   -> {'DEPARTS from the shuffle null' if p <= 0.05 else 'at the null'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
