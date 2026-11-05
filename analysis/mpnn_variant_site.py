#!/usr/bin/env python3
"""Does the fold still want the wild-type residue once the variant is built into the backbone?

WHY NOT pLDDT. This project spent thirteen substitutions at one site establishing that a pLDDT
delta at the substituted position tracks a property of the SUBSTITUTED RESIDUE -- side-chain
heavy-atom count -- and not how damaging the substitution is (docs/FINDINGS.md, claims 460/462/
517/521). It gave its largest response to the milder substitution and nothing to the severe one.
So the structure-confidence route is closed here by measurement, not by preference. ProteinMPNN
is a different model on a different principle: it reads a backbone and returns, per position, a
distribution over the twenty residues that backbone would accept.

THE QUESTION, stated so it can come out either way. Fold the variant, then ask the designer what
belongs at that site. If it still prefers the wild-type residue over the one actually present,
the mutant backbone has not made room for the substitution. If it prefers the variant residue,
the backbone accommodates it. Neither answer is the "good" one in advance.

THE CONTROL THAT DECIDES WHETHER ANY OF IT IS READABLE. Two ProteinMPNN runs on two separately
predicted structures differ for two reasons: the substitution, and everything else that moves
between two runs. Claim 1096 measured that run-to-run term on this project and found it large
enough to erase a causal attribution. So this script reports the shift at the mutated site
BESIDE the distribution of shifts at every other position. If the site's shift is ordinary
against that background, the comparison is noise and the script says so. That is a must-not-flag
control: a null result here must be reachable, or the measurement cannot support a conclusion.

    python3 analysis/mpnn_variant_site.py --wt-probs ... --var-probs ... \
        --wt-fasta ... --var-fasta ... --site 583
"""
from __future__ import annotations

import argparse
import json
import math

ALPHABET = "ACDEFGHIKLMNPQRSTVWYX"   # verified by recovery: 37.2% native vs 11.6% shuffled


def read_seq(path: str) -> str:
    return "".join(ln.strip() for ln in open(path) if not ln.startswith(">"))


def mean_sd(xs: list[float]) -> tuple[float, float]:
    n = len(xs)
    m = sum(xs) / n
    if n < 2:
        return m, float("nan")
    return m, math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1))


def site_profile(probs: list, pos0: int) -> dict[str, tuple[float, float]]:
    """mean and sd across the replicate decoding orders, per amino acid, at one position."""
    return {ALPHABET[j]: mean_sd([s[pos0][j] for s in probs]) for j in range(20)}


def jsd(p: list[float], q: list[float]) -> float:
    """Jensen-Shannon divergence, base 2, between two residue distributions at one position.

    The first version of this script used |P(native, variant run) - P(native, WT run)| as the
    shift statistic and it went DEGENERATE on the very first site it was pointed at: ProteinMPNN
    gives both cysteine and tyrosine ~0 at slc12a7a 583, so their difference is ~0 and the site
    scored at the 29th percentile of background -- a number that says nothing about whether the
    distribution moved, only that two small numbers are both small. JSD reads the whole
    distribution, so a position cannot score low merely because the residue of interest is
    unlikely under both.
    """
    tot = 0.0
    for a, b in zip(p, q):
        m = 0.5 * (a + b)
        if a > 0:
            tot += 0.5 * a * math.log2(a / m)
        if b > 0:
            tot += 0.5 * b * math.log2(b / m)
    return tot


def mean_dist(probs: list, pos0: int) -> list[float]:
    return [sum(s[pos0][j] for s in probs) / len(probs) for j in range(21)]


def native_prob_vector(probs: list, seq: str) -> list[float]:
    """P(the residue that is actually there), averaged over replicates, at every position."""
    out = []
    for i, aa in enumerate(seq):
        j = ALPHABET.index(aa) if aa in ALPHABET else 20
        out.append(sum(s[i][j] for s in probs) / len(probs))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--wt-probs", required=True)
    ap.add_argument("--var-probs", required=True)
    ap.add_argument("--wt-fasta", required=True)
    ap.add_argument("--var-fasta", required=True)
    ap.add_argument("--site", type=int, required=True, help="1-indexed")
    ap.add_argument("--null", action="store_true",
                    help="the two runs are REPLICATES of the same sequence, not a variant pair. "
                         "This is the control the variant comparison needs: it measures how much "
                         "two independent structure predictions of the SAME genotype disagree, "
                         "which is the background a real substitution has to beat.")
    a = ap.parse_args()

    wt_seq, var_seq = read_seq(a.wt_fasta), read_seq(a.var_fasta)
    if len(wt_seq) != len(var_seq):
        print(f"REFUSED: sequences differ in length ({len(wt_seq)} vs {len(var_seq)}); "
              f"this script assumes a substitution, not an indel.")
        return 2
    diffs = [(i + 1, x, y) for i, (x, y) in enumerate(zip(wt_seq, var_seq)) if x != y]
    if a.null and diffs:
        print(f"REFUSED: --null says these are replicates of one sequence, but they differ "
              f"at {diffs}.")
        return 2
    if not a.null and diffs != [(a.site, wt_seq[a.site - 1], var_seq[a.site - 1])]:
        print(f"REFUSED: the two sequences differ at {diffs}, not only at the named site {a.site}.")
        return 2

    i0 = a.site - 1
    wt_aa, var_aa = wt_seq[i0], var_seq[i0]
    WT = json.load(open(a.wt_probs))["probs"]
    VR = json.load(open(a.var_probs))["probs"]
    kind = "REPLICATE PAIR (null control)" if a.null else f"{wt_aa} -> {var_aa}"
    print(f"site {a.site}: {kind}   "
          f"({len(WT)} and {len(VR)} replicate decoding orders)\n")

    pw, pv = site_profile(WT, i0), site_profile(VR, i0)
    print("  what the designer wants AT THE SITE (mean +- sd over replicates)")
    print(f"  {'':12s} {'on WT backbone':>22s}   {'on variant backbone':>22s}")
    for aa, lab in ((wt_aa, "wild-type"), (var_aa, "variant")):
        mw, sw = pw[aa]
        mv, sv = pv[aa]
        print(f"  {aa} ({lab:9s}) {mw:>11.4f} +- {sw:.4f}   {mv:>11.4f} +- {sv:.4f}")
    for lab, prof in (("WT backbone", pw), ("variant backbone", pv)):
        rank = sorted(prof, key=lambda k: -prof[k][0])
        print(f"  top-5 on the {lab:17s}: "
              + ", ".join(f"{k} {prof[k][0]:.3f}" for k in rank[:5])
              + f"   | {wt_aa} rank {rank.index(wt_aa)+1}, {var_aa} rank {rank.index(var_aa)+1}")

    # ---- the control: is the site's shift unusual against every other position? ----
    shifts = [jsd(mean_dist(WT, i), mean_dist(VR, i)) for i in range(len(wt_seq))]
    site_shift = shifts[i0]
    others = sorted(shifts[:i0] + shifts[i0 + 1:])
    bigger = sum(1 for s in others if s >= site_shift)
    pct = 100.0 * (len(others) - bigger) / len(others)
    med = others[len(others) // 2]
    print("\n  CONTROL -- run-to-run background, Jensen-Shannon divergence per position")
    print(f"    at the mutated site      {site_shift:.4f}")
    print(f"    median over {len(others)} others  {med:.4f}")
    print(f"    90th pct / max           {others[int(.9*len(others))]:.4f} / {others[-1]:.4f}")
    print(f"    the site sits at the {pct:.1f}th percentile of background shift "
          f"({bigger} positions moved at least as much)")
    if a.null:
        print("\n  READING (null control): the same genotype folded twice, so every number above\n"
              "  is structure-prediction background with NO substitution in it. Compare this\n"
              "  distribution against the variant pair's -- if they match, the variant\n"
              "  comparison was measuring the predictor and not the mutation.")
        return 0
    if pct < 95.0:
        print("\n  READING: the mutated site's shift is NOT distinguishable from the background\n"
              "  two independent structure predictions produce anyway. This comparison does not\n"
              "  support a conclusion about the substitution. Replicate structures, not just\n"
              "  replicate decoding orders, would be needed to separate the two.")
    else:
        print(f"\n  READING: the mutated site moved more than {pct:.1f}% of all other positions,\n"
              f"  so the shift is larger than the run-to-run background -- though a background\n"
              f"  built from ONE structure pair still cannot rule out a single unlucky draw.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
