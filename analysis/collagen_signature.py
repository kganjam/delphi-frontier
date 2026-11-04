#!/usr/bin/env python3
"""Does a protein carry a collagen triple-helix signature? Glycine fraction and in-frame Gly-X-Y runs.

Collagen's defining sequence feature is a long (Gly-X-Y)n repeat, which shows up as a high glycine
fraction and a long run of in-frame glycines. This measures both.

SHIPS WITH A POSITIVE CONTROL and will not report a negative without it: a real collagen must be
passed alongside the test proteins. An assay that cannot separate col1a1a from a non-collagen is
not evidence that anything lacks the signature.

    python3 collagen_signature.py CONTROL.faa TEST.faa [TEST2.faa ...]
"""
import sys


def read_fasta(path):
    lines = open(path).read().split("\n")
    return "".join(l.strip() for l in lines[1:] if l and not l.startswith(">"))


def stats(seq):
    n = len(seq)
    gly = seq.count("G") / n
    pro = seq.count("P") / n
    best = 0
    for frame in range(3):
        run = 0
        for i in range(frame, n - 2, 3):
            if seq[i] == "G":
                run += 1; best = max(best, run)
            else:
                run = 0
    return n, gly, pro, best


def main():
    if len(sys.argv) < 3:
        print(__doc__); return 2
    ctrl_path, tests = sys.argv[1], sys.argv[2:]
    cn, cg, cp, cb = stats(read_fasta(ctrl_path))
    print(f"CONTROL  {ctrl_path:28} len={cn:5}  Gly={cg*100:5.1f}%  "
          f"Pro={cp*100:5.1f}%  longest in-frame GXY run={cb:4}")
    if cg < 0.15 or cb < 50:
        print("  CONTROL FAILED: the positive control does not look collagen-like. "
              "No negative result below is interpretable.")
        return 1
    print("  control passed: the assay separates a real collagen.\n")
    for t in tests:
        n, g, p, b = stats(read_fasta(t))
        verdict = "COLLAGEN-LIKE" if (g >= 0.15 and b >= 50) else "no collagen signature"
        print(f"TEST     {t:28} len={n:5}  Gly={g*100:5.1f}%  "
              f"Pro={p*100:5.1f}%  longest run={b:4}   {verdict}")
    print(f"\n  separation on run length: control {cb} vs tests — "
          f"the margin is what makes a negative informative.")
    print("  SCOPE: this tests for the collagen TRIPLE HELIX only. A protein can be stiff "
          "without being collagen; nothing here measures a modulus.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
