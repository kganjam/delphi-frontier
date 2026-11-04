#!/usr/bin/env python3
"""BLAST-lite tblastn: query protein vs 6-frame translation of a DNA locus.

Seed (4-mer exact) + ungapped BLOSUM62 extension. Written because no
blast/biopython is available in this container.
"""
import sys, random
from itertools import product

B62_RAW = """A R N D C Q E G H I L K M F P S T W Y V B Z X *
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
* -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4  1"""


def load_b62():
    lines = B62_RAW.strip().split("\n")
    cols = lines[0].split()
    m = {}
    for ln in lines[1:]:
        p = ln.split()
        r = p[0]
        for c, v in zip(cols, p[1:]):
            m[(r, c)] = int(v)
    return m


B62 = load_b62()
AAS = "FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"
CODON = {}
for i, (a, b, c) in enumerate(product("TCAG", repeat=3)):
    CODON[a + b + c] = AAS[i]


def sc(a, b):
    return B62.get((a, b), B62.get((b, a), -4))


def revcomp(s):
    return s.translate(str.maketrans("ACGTN", "TGCAN"))[::-1]


def translate(s):
    return "".join(CODON.get(s[i:i + 3], "X") for i in range(0, len(s) - 2, 3))


def frames(dna):
    """Yield (label, aa_seq, fn mapping aa index -> 1-based locus offset)."""
    n = len(dna)
    for off in range(3):
        yield (f"+{off+1}", translate(dna[off:]), lambda i, off=off: off + 3 * i + 1)
    rc = revcomp(dna)
    for off in range(3):
        yield (f"-{off+1}", translate(rc[off:]),
               lambda i, off=off: n - (off + 3 * i))


def hsps(query, dna, k=4, min_score=40, drop=12):
    """Seeded ungapped extension. Returns list of HSP dicts."""
    out = []
    qidx = {}
    for i in range(len(query) - k + 1):
        qidx.setdefault(query[i:i + k], []).append(i)
    for label, sub, mapper in frames(dna):
        seen = set()
        for j in range(len(sub) - k + 1):
            seed = sub[j:j + k]
            if "*" in seed or "X" in seed:
                continue
            for i in qidx.get(seed, ()):
                diag = (label, i - j)
                if diag in seen:
                    continue
                # ungapped extend both ways with X-drop
                s = sum(sc(query[i + t], sub[j + t]) for t in range(k))
                best = s
                # right
                cur, a, b = s, i + k, j + k
                bi, bj = i + k, j + k
                while a < len(query) and b < len(sub) and sub[b] != "*":
                    cur += sc(query[a], sub[b])
                    if cur > best:
                        best, bi, bj = cur, a + 1, b + 1
                    if best - cur > drop:
                        break
                    a += 1
                    b += 1
                # left
                cur, a, b = best, i - 1, j - 1
                si, sj = i, j
                peak = best
                while a >= 0 and b >= 0 and sub[b] != "*":
                    cur += sc(query[a], sub[b])
                    if cur > peak:
                        peak, si, sj = cur, a, b
                    if peak - cur > drop:
                        break
                    a -= 1
                    b -= 1
                if peak >= min_score:
                    seen.add(diag)
                    qs, qe = si, bi
                    ident = sum(1 for t in range(qe - qs)
                                if query[qs + t] == sub[sj + t])
                    out.append(dict(frame=label, score=peak, q_start=qs + 1,
                                    q_end=qe, locus=mapper(sj),
                                    ident=round(100.0 * ident / max(1, qe - qs), 1),
                                    alen=qe - qs,
                                    subj=sub[sj:sj + (qe - qs)]))
    out.sort(key=lambda h: -h["score"])
    # dedupe overlapping query ranges keeping best
    keep = []
    for h in out:
        if any(not (h["q_end"] <= g["q_start"] or h["q_start"] >= g["q_end"])
               and h["frame"] == g["frame"] for g in keep):
            continue
        keep.append(h)
    return keep


def nw(a, b, gap=-8):
    """Global alignment, returns map from a-index(0based) -> b-index(0based)."""
    n, m = len(a), len(b)
    f = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        f[i][0] = gap * i
    for j in range(1, m + 1):
        f[0][j] = gap * j
    for i in range(1, n + 1):
        ai = a[i - 1]
        fi, fp = f[i], f[i - 1]
        for j in range(1, m + 1):
            fi[j] = max(fp[j - 1] + sc(ai, b[j - 1]), fp[j] + gap, fi[j - 1] + gap)
    i, j = n, m
    mp = {}
    while i > 0 and j > 0:
        if f[i][j] == f[i - 1][j - 1] + sc(a[i - 1], b[j - 1]):
            mp[i - 1] = j - 1
            i, j = i - 1, j - 1
        elif f[i][j] == f[i - 1][j] + gap:
            i -= 1
        else:
            j -= 1
    return mp


def rdfa(p):
    return "".join(l.strip() for l in open(p) if not l.startswith(">")).upper()


if __name__ == "__main__":
    locus = rdfa(sys.argv[1])
    a153 = rdfa(sys.argv[2])   # slc43a2a 153 aa
    b592 = rdfa(sys.argv[3])   # slc43a2b 592 aa

    print(f"locus {len(locus)} bp | slc43a2a {len(a153)} aa | slc43a2b {len(b592)} aa")

    mp = nw(a153, b592)
    last = max(mp.values())
    print(f"\n[map] slc43a2a residue 153 aligns to slc43a2b residue {mp.get(152, '?')}")
    print(f"[map] a-residue 200 would correspond to ~b-residue "
          f"{(mp.get(152) or 0) + 1 + 47}")

    print("\n=== POSITIVE CONTROL: slc43a2a 153aa vs locus (must be found, ~100% id) ===")
    for h in hsps(a153, locus)[:8]:
        print(f"  q{h['q_start']}-{h['q_end']} frame {h['frame']} "
              f"locus~{h['locus']} score {h['score']} id {h['ident']}%")

    print("\n=== TEST: slc43a2b 592aa vs locus (do exons past a-153 exist?) ===")
    for h in hsps(b592, locus):
        flag = "  <-- PAST a-153" if h["q_start"] > last + 1 else ""
        print(f"  q{h['q_start']}-{h['q_end']} frame {h['frame']} "
              f"locus~{h['locus']} score {h['score']} id {h['ident']}% "
              f"len {h['alen']}{flag}")

    print("\n=== MUST-FAIL 1: shuffled slc43a2b (composition-matched) ===")
    random.seed(11)
    sh = list(b592)
    random.shuffle(sh)
    r = hsps("".join(sh), locus)
    print(f"  HSPs >= 40: {len(r)}" + ("" if not r else f"  top score {r[0]['score']}"))

    print("=== MUST-FAIL 2: unrelated protein (human HBB) ===")
    HBB = ("MVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFESFGDLSTPDAVMGNPKV"
           "KAHGKKVLGAFSDGLAHLDNLKGTFATLSELHCDKLHVDPENFRLLGNVLVCVLAHHFGKE"
           "FTPPVQAAYQKVVAGVANALAHKYH")
    r2 = hsps(HBB, locus)
    print(f"  HSPs >= 40: {len(r2)}" + ("" if not r2 else f"  top score {r2[0]['score']}"))
