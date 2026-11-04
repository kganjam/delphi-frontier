#!/usr/bin/env python3
"""Minimum nucleotide substitutions between two amino acids under the standard genetic code.

Re-derives the quantity behind Delphi law `genotype-genetic-code`
(Delphi.Genotype.claimed_substitutions_rules_out). Ships with the three instances that law's own
statement commits to as controls: a table that disagrees with them is wrong.

    python3 codon_distance.py            # run the controls and report T200K
"""
import sys

B = "UCAG"
AAS = "FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"
CODE = {}
_i = 0
for _a in B:
    for _b in B:
        for _c in B:
            CODE[_a + _b + _c] = AAS[_i]; _i += 1


def codons(aa):
    return [c for c, x in CODE.items() if x == aa]


def hamming(c, d):
    return sum(1 for p, q in zip(c, d) if p != q)


def min_subst(a, b):
    return min(hamming(c, d) for c in codons(a) for d in codons(b))


def main():
    assert len(CODE) == 64 and CODE["AUG"] == "M" and CODE["UGG"] == "W"
    controls = [("F", "L", 1), ("W", "*", 1), ("M", "W", 2)]
    for a, b, n in controls:
        got = min_subst(a, b)
        print(f"control {a}->{b}: expected {n}, got {got}")
        if got != n:
            print("CONTROL FAILED: this code table disagrees with the law"); return 1
    print(f"\nThr->Lys minimum substitutions: {min_subst('T','K')}")
    pairs = [(c, d) for c in codons("T") for d in codons("K")
             if hamming(c, d) == min_subst("T", "K")]
    print(f"realising codon pairs: {pairs}")
    print("codon 200 of ENSDART00000168453 is ACA -> AAA is one C->A at position 2")
    return 0


if __name__ == "__main__":
    sys.exit(main())
