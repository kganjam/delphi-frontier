"""Replicate 29: tandem-repeat test vs a composition-preserving shuffle null.

Independent re-derivation. Inputs: UniProt FASTA for A0ACM8QEN9 (and2), E7F5V5 (and1),
Q6PFU3 (kcnk5b), Danio rerio. Usage: python3 -I replicate-29_shuffle_null.py <dir with *.fasta>

Statistics (all computed, none observed):
  T_all : max over periods L=1..100 of the best ungapped BLOSUM62 local score on self-diagonal
          offset L, counting only segments of length >= L (copies abut/overlap = tandem).
  T_ge5 : same, periods L=5..100 (excludes homopolymer / di-, tri-, tetra-peptide runs).
  G_ge5 : gapped Smith-Waterman self-alignment score, linear gap 8, cells with j-i >= 5 only
          (internal repeats, tandem or not, allowing indels).
Null: 200 uniform random permutations of each sequence (exact composition preserved), seed 29.
Empirical p = (1 + #null >= observed) / (1 + 200).
"""
import sys, glob, os, json
import numpy as np

B62_TXT = """
   A  R  N  D  C  Q  E  G  H  I  L  K  M  F  P  S  T  W  Y  V  B  Z  X  *
A  4 -1 -2 -2  0 -1 -1  0 -2 -1 -1 -1 -1 -2 -1  1  0 -3 -2  0 -2 -1  0 -4
R -1  5  0 -2 -3  1  0 -2  0 -3 -2  2 -1 -3 -2 -1 -1 -3 -2 -3 -1  0 -1 -4
N -2  0  6  1 -3  0  0  0  1 -3 -3  0 -2 -3 -2  1  0 -4 -2 -3  3  0 -1 -4
D -2 -2  1  6 -3  0  2 -1 -1 -3 -4 -1 -3 -3 -1  0 -1 -4 -3 -3  4  1 -1 -4
C  0 -3 -3 -3  9 -3 -4 -3 -3 -1 -1 -3 -1 -2 -3 -1 -1 -2 -2 -1 -3 -3 -2 -4
Q -1  1  0  0 -3  5  2 -2  0 -3 -2  1  0 -3 -1  0 -1 -2 -1 -2  0  3 -1 -4
E -1  0  0  2 -4  2  5 -2  0 -3 -3  1 -2 -3 -1  0 -1 -3 -2 -2  1  4 -1 -4
G  0 -2  0 -1 -3 -2 -2  6 -2 -4 -4 -2 -3 -3 -2  0 -2 -2 -3 -3 -1 -2 -1 -4
H -2  0  1 -1 -3  0  0 -2  8 -3 -3 -1 -2 -1 -2 -1 -2 -2  2 -3  0  0 -1 -4
I -1 -3 -3 -3 -1 -3 -3 -4 -3  4  2 -3  1  0 -3 -2 -1 -3 -1  3 -3 -3 -1 -4
L -1 -2 -3 -4 -1 -2 -3 -4 -3  2  4 -2  2  0 -3 -2 -1 -2 -1  1 -4 -3 -1 -4
K -1  2  0 -1 -3  1  1 -2 -1 -3 -2  5 -1 -3 -1  0 -1 -3 -2 -2  0  1 -1 -4
M -1 -1 -2 -3 -1  0 -2 -3 -2  1  2 -1  5  0 -2 -1 -1 -1 -1  1 -3 -1 -1 -4
F -2 -3 -3 -3 -2 -3 -3 -3 -1  0  0 -3  0  6 -4 -2 -2  1  3 -1 -3 -3 -1 -4
P -1 -2 -2 -1 -3 -1 -1 -2 -2 -3 -3 -1 -2 -4  7 -1 -1 -4 -3 -2 -2 -1 -2 -4
S  1 -1  1  0 -1  0  0  0 -1 -2 -2  0 -1 -2 -1  4  1 -3 -2 -2  0  0  0 -4
T  0 -1  0 -1 -1 -1 -1 -2 -2 -1 -1 -1 -1 -2 -1  1  5 -2 -2  0 -1 -1  0 -4
W -3 -3 -4 -4 -2 -2 -3 -2 -2 -3 -2 -3 -1  1 -4 -3 -2 11  2 -3 -4 -3 -2 -4
Y -2 -2 -2 -3 -2 -1 -2 -3  2 -1 -1 -2 -1  3 -3 -2 -2  2  7 -1 -3 -2 -1 -4
V  0 -3 -3 -3 -1 -2 -2 -3 -3  3  1 -2  1 -1 -2 -2  0 -3 -1  4 -3 -2 -1 -4
B -2 -1  3  4 -3  0  1 -1  0 -3 -4  0 -3 -3 -2  0 -1 -4 -3 -3  4  1 -1 -4
Z -1  0  0  1 -3  3  4 -2  0 -3 -3  1 -1 -3 -1  0 -1 -3 -2 -2  1  4 -1 -4
X  0 -1 -1 -1 -2 -1 -1 -1 -1 -1 -1 -1 -1 -1 -2  0  0 -2 -1 -1 -1 -1 -1 -4
* -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4  1
"""
rows = [r.split() for r in B62_TXT.strip().splitlines()]
ALPH = rows[0]
IDX = {a: i for i, a in enumerate(ALPH)}
B62 = np.array([[int(x) for x in r[1:]] for r in rows[1:]], dtype=np.int32)
GAP = 8
N_SHUF = 200
MAXP = 100


def read_fasta(p):
    with open(p) as f:
        lines = f.read().splitlines()
    return lines[0], "".join(l.strip() for l in lines[1:] if not l.startswith(">"))


def enc(s):
    return np.array([IDX.get(c, IDX["X"]) for c in s], dtype=np.int64)


def tandem_scores(x):
    """Return (T_all, best_L_all, T_ge5, best_L_ge5, best segment info)."""
    n = len(x)
    best = {}  # L -> (score, start, length)
    for L in range(1, min(MAXP, n - 1) + 1):
        d = B62[x[:-L], x[L:]]
        # Kadane with length tracking; keep only segments of length >= L
        bs, bstart, blen = 0, -1, 0
        cur, cstart = 0, 0
        # need best segment with length >= L: track max over ends of (cur) where length >= L
        # simple O(n) approach: prefix sums, for each end e best start s<=e-L+1 minimizing prefix
        P = np.concatenate([[0], np.cumsum(d)])
        m = len(d)
        if m < L:
            best[L] = (0, -1, 0)
            continue
        # min prefix over starts 0..e-L+1 for end e (segment d[s:e+1])
        ends = np.arange(L - 1, m)
        minpref = np.minimum.accumulate(P[: m - L + 1])
        ar = np.arange(m - L + 1)
        argpref = np.maximum.accumulate(np.where(P[: m - L + 1] == minpref, ar, 0))
        sc = P[ends + 1] - minpref
        k = int(np.argmax(sc))
        s = int(sc[k])
        if s > 0:
            st = int(argpref[k]); en = int(ends[k])
            best[L] = (s, st, en - st + 1)
        else:
            best[L] = (0, -1, 0)
    Lall = max(best, key=lambda L: best[L][0])
    L5 = max((L for L in best if L >= 5), key=lambda L: best[L][0])
    return best[Lall][0], Lall, best[L5][0], L5, best


def gapped_internal(x, minoff=5):
    n = len(x)
    S = B62[x[:, None], x[None, :]].astype(np.int64)
    j = np.arange(n)
    prev = np.zeros(n, dtype=np.int64)
    best = 0
    for i in range(n):
        diag = np.zeros(n, dtype=np.int64)
        diag[1:] = prev[:-1] + S[i, 1:]
        diag[0] = S[i, 0]
        up = prev - GAP
        h = np.maximum(0, np.maximum(diag, up))
        h[j - i < minoff] = 0
        h = np.maximum(h, np.maximum.accumulate(h + GAP * j) - GAP * j)
        h[j - i < minoff] = 0
        best = max(best, int(h.max()))
        prev = h
    return best


def main(d):
    rng = np.random.default_rng(29)
    out = {}
    for p in sorted(glob.glob(os.path.join(d, "*.fasta"))):
        hdr, s = read_fasta(p)
        acc = hdr.split("|")[1]
        x = enc(s)
        Ta, La, T5, L5, best = tandem_scores(x)
        G5 = gapped_internal(x)
        nT, n5, nG = [], [], []
        for _ in range(N_SHUF):
            y = rng.permutation(x)
            a, _, b, _, _ = tandem_scores(y)
            nT.append(a); n5.append(b); nG.append(gapped_internal(y))
        def summ(obs, null):
            null = np.array(null)
            return {"obs": obs, "null_mean": round(float(null.mean()), 2),
                    "null_sd": round(float(null.std(ddof=1)), 2),
                    "null_max": int(null.max()), "null_q95": float(np.quantile(null, 0.95)),
                    "z": round(float((obs - null.mean()) / null.std(ddof=1)), 2),
                    "p_emp": round((1 + int((null >= obs).sum())) / (1 + N_SHUF), 4)}
        segA = best[La]; seg5 = best[L5]
        out[acc] = {"len": len(s),
                    "T_all": summ(Ta, nT), "T_all_period": La,
                    "T_all_segment": s[segA[1]: segA[1] + segA[2] + La] if segA[1] >= 0 else "",
                    "T_ge5": summ(T5, n5), "T_ge5_period": L5,
                    "T_ge5_segment": s[seg5[1]: seg5[1] + seg5[2] + L5] if seg5[1] >= 0 else "",
                    "G_ge5": summ(G5, nG)}
        print(acc, json.dumps(out[acc], indent=1), flush=True)
    return out


if __name__ == "__main__":
    main(sys.argv[1])
