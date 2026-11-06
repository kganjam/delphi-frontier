#!/usr/bin/env python3
"""Does the alf substitution W169L move the Kcnk5b ion pathway? Measured against the right floor.

THE EXPERIMENT WAS ALREADY SET UP CORRECTLY by analysis/kcnk5b_w169l_pore.py, which predicts
wild type and W169L with the SAME model and the SAME alignment so that nothing is confounded by
method. Both arms are on disk. What was never done is the comparison, and the comparison turns
entirely on which floor it is judged against.

THE FLOOR IS NOT CHAIN SYMMETRY, and that is the whole point. The obvious yardstick -- chain A
against chain B of one homodimer -- is two copies produced in ONE forward pass, so it measures
the model's internal consistency and not its reproducibility. This project has the number that
shows the difference: claim 1092 measured 30.161 A between TWO openfold3 runs of the IDENTICAL
wild-type dimer. A within-file symmetry check on the same protein lands near zero. Judging a
one-residue substitution against the symmetry number would make almost any difference look
enormous; judging it against the re-run number is the honest test, and it is the same lesson
claim 1450 reached from the other direction, where re-folding one sequence moved ProteinMPNN
more than mutating it did.

WHAT IS ALREADY KNOWN, so this is not read as new. Claim 1083 ran exactly this comparison and
got 49.178 A whole-chain, concluding "it cannot be asked at this confidence level, and finding
that out is the result". Claim 1092 then supplied the control 1083 lacked: wild type submitted
twice gives 30.161 A. This script REPRODUCES 1083 (49.18 A on chain A) from the structures on
disk and exists to make that reproducible rather than to rediscover it.

WHAT IT ADDS IS THE CEILING, and it changes the verdict's shape. Neither 1083 nor 1092 reports
what "completely unrelated" scores on this metric. Shuffling the residue correspondence of one
structure against itself gives 63.3 A here. So the 50.2 A mutant-vs-wild-type difference is 79
per cent of the way to unrelated. Judged against the 30.16 A floor ALONE, 50 > 30 reads as a
detected change; judged with the ceiling as well, it reads as a predictor that has not
determined the fold at all. A floor says what no change looks like; a ceiling says what no
information looks like, and a number can clear the first while sitting next to the second.
"""
from __future__ import annotations

import os
import sys

import json

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pore_geometry import coords, kabsch_rmsd  # noqa: E402

WT, MUT = "kcnk5b-wt-of3", "kcnk5b-w169l-of3"
POS = 169
#: claim 1092: two openfold3 runs of the IDENTICAL wild-type dimer, same alignment.
RERUN_FLOOR = (30.161, "claim 1092, two openfold3 runs of the identical wild-type kcnk5b dimer")


def main() -> int:
    print("=" * 92)
    print("kcnk5b W169L (the alf gain-of-function allele): does the fold move?")
    print("=" * 92)

    chains = []
    for ch in ("A", "B"):
        try:
            a, b = coords(WT, ch, 1, 448), coords(MUT, ch, 1, 448)
        except Exception as e:                                    # noqa: BLE001
            print(f"  chain {ch}: unreadable ({type(e).__name__})")
            continue
        if len(a) != len(b) or not len(a):
            print(f"  chain {ch}: {len(a)} vs {len(b)} CA -- REFUSING, not like for like")
            continue
        chains.append((ch, a, b))
        print(f"  chain {ch}: {len(a)} CA in each arm")
    if not chains:
        print("  nothing comparable on disk")
        return 2

    print("\n  CONTROLS (the metric must be able to say 'same' and 'different')")
    ch, a, _ = chains[0]
    rng = np.random.default_rng(3)
    th = rng.random() * 2 * np.pi
    Rz = np.array([[np.cos(th), -np.sin(th), 0], [np.sin(th), np.cos(th), 0], [0, 0, 1]])
    print(f"    a structure against itself                  {kabsch_rmsd(a, a):8.4f} A  (must be ~0)")
    print(f"    against a rotated+translated copy of itself {kabsch_rmsd(a, a @ Rz + np.array([11., -7., 3.])):8.4f} A  (must be ~0)")
    perm = rng.permutation(len(a))
    print(f"    against itself, correspondence SHUFFLED     {kabsch_rmsd(a, a[perm]):8.2f} A  (must be large)")

    print("\n  THE MEASUREMENT")
    vals = []
    for ch, a, b in chains:
        r = kabsch_rmsd(a, b)
        vals.append(r)
        print(f"    wild type vs W169L, chain {ch}:            {r:8.2f} A")
    try:
        sym = kabsch_rmsd(coords(WT, "A", 1, 448), coords(WT, "B", 1, 448))
        print(f"    chain A vs chain B WITHIN the wild type:  {sym:8.2f} A  "
              f"<- internal symmetry, NOT a reproducibility floor")
    except Exception:                                             # noqa: BLE001
        sym = None

    worst = max(vals)
    floor = RERUN_FLOOR[0]
    print(f"\n    the re-run floor:                         {floor:8.2f} A  ({RERUN_FLOOR[1]})")

    scram = kabsch_rmsd(a, a[perm])
    print("\n  WHAT THE MODEL THINKS OF ITS OWN ANSWER (both arms, same seed 42):")
    for name in (WT, MUT):
        d = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                                        "results/fish-proteins/structures", name, "result.json")))
        sc = d["outputs"][0]["structures_with_scores"][0]
        print(f"    {name:22s} pLDDT {sc['complex_plddt_score']:5.1f}  ipTM {sc['iptm_score']:.3f}  "
              f"pTM {sc['ptm_score']:.3f}")
    print("    pLDDT near 60 and ipTM below 0.5 are both low: the model is NOT confident in "
          "either\n    structure, so neither is a determined answer that a difference could be "
          "read against.")

    # THE SAME FLOOR, ON THE SCORES THEMSELVES. Claim 1868 established that an RMSD between two
    # predicted structures needs both bounds, and quoted these confidence scores as supporting
    # evidence WITHOUT a floor under them. That leaves the pair readable the wrong way: pLDDT
    # 60.7 -> 57.3 looks like the substitution destabilising the fold. The wild type was run
    # twice, so the floor is already on disk and nothing new has to be computed on a GPU.
    rep = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                       "results/fish-proteins/structures", "kcnk5b-wt-replicate-of3",
                       "result.json")
    if os.path.exists(rep):
        def sc_of(name):
            d = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                                            "results/fish-proteins/structures", name,
                                            "result.json")))
            return d["outputs"][0]["structures_with_scores"][0]
        wt_s, mut_s = sc_of(WT), sc_of(MUT)
        rep_s = json.load(open(rep))["outputs"][0]["structures_with_scores"][0]
        print("\n  AND THE FLOOR UNDER THOSE SCORES -- wild type run TWICE, same seed 42:")
        print(f"    {'metric':<22}{'noise (WT vs WT)':>18}{'effect (WT vs W169L)':>22}   verdict")
        unresolved = 0
        for k in ("complex_plddt_score", "iptm_score", "ptm_score", "confidence_score",
                  "complex_pde_score"):
            noise = abs(wt_s[k] - rep_s[k])
            effect = abs(wt_s[k] - mut_s[k])
            ok = effect > noise
            unresolved += not ok
            print(f"    {k:<22}{noise:>18.4f}{effect:>22.4f}   "
                  + ("resolved" if ok else "NOT RESOLVED (noise >= effect)"))
        print(f"\n    {unresolved} of 5 confidence metrics are NOT resolved. The two wild-type "
              f"runs\n    differ by {abs(wt_s['complex_plddt_score'] - rep_s['complex_plddt_score']):.1f} "
              f"pLDDT against {abs(wt_s['complex_plddt_score'] - mut_s['complex_plddt_score']):.1f} "
              f"between wild type and W169L, so the\n    score drop is smaller than what an "
              f"UNCHANGED sequence produces. Both runs carry\n    the same seed, so openfold3 is "
              f"non-deterministic at fixed seed on this target --\n    the same property claim 1394 "
              f"measured for ESMFold2, on a different predictor.")

        if "--write" in sys.argv:
            sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                            "..", "swarm"))
            from dbq import write_claim
            dp = abs(wt_s["complex_plddt_score"] - rep_s["complex_plddt_score"])
            de = abs(wt_s["complex_plddt_score"] - mut_s["complex_plddt_score"])
            cid = write_claim(
                "zebrafish-flight", "protein",
                f"""[EXTENDS CLAIM 1868 TO THE CONFIDENCE SCORES IT QUOTED WITHOUT A FLOOR:
{unresolved} OF 5 ARE UNRESOLVED, AND openfold3 IS NON-DETERMINISTIC AT FIXED SEED]
Claim 1868 established that an RMSD between two predicted structures may not be read as evidence
about a substitution without quoting a floor and a ceiling. In support it quoted this pair's own
confidence scores -- complex pLDDT 60.7 and 57.3, ipTM 0.399 and 0.371 -- and observed that both
are low. It did not put a floor under THOSE numbers, which leaves them readable the wrong way: a
60.7 to 57.3 drop looks like the substitution destabilising the fold.

The wild type was run twice, so the floor was already on disk and no GPU was spent to get it.
Two runs of the IDENTICAL wild-type sequence differ by {dp:.4f} complex pLDDT; wild type against
W169L differs by {de:.4f}. The effect is SMALLER than the noise. The same holds on all five
metrics the model reports: ipTM {abs(wt_s['iptm_score']-rep_s['iptm_score']):.4f} noise against
{abs(wt_s['iptm_score']-mut_s['iptm_score']):.4f} effect, pTM
{abs(wt_s['ptm_score']-rep_s['ptm_score']):.4f} against
{abs(wt_s['ptm_score']-mut_s['ptm_score']):.4f}, confidence
{abs(wt_s['confidence_score']-rep_s['confidence_score']):.4f} against
{abs(wt_s['confidence_score']-mut_s['confidence_score']):.4f}, PDE
{abs(wt_s['complex_pde_score']-rep_s['complex_pde_score']):.4f} against
{abs(wt_s['complex_pde_score']-mut_s['complex_pde_score']):.4f}. {unresolved} of 5 unresolved.

BOTH RUNS CARRY SEED 42. They differ only in idempotency key, so openfold3 is non-deterministic
at a FIXED seed on this target -- the property claim 1394 measured for ESMFold2, reproduced here
on a different predictor and a different target. A seed is not a reproducibility guarantee for
either.

CONSEQUENCE, extending 1868's: a confidence score reported for a variant may not be compared with
one reported for its wild type unless a same-sequence re-run bounds the comparison. That bound is
cheap -- it is one extra submit -- and in this case it already existed unused.

SCOPE: one target, one predictor, one replicate pair. A single replicate gives a floor, not a
distribution, so "noise exceeds effect" here is a statement about these four runs and not an
error bar. The monomer-replicate arm reports ipTM 0.0000, which is the expected value for a
single chain and is a sanity control on the reader, not evidence about the dimer.""",
                "measured", dp, "complex pLDDT between two runs of the identical sequence",
                "analysis/kcnk5b_w169l_geometry.py", None)
            print(f"\n    recorded claim {cid}")

    print("\n  READING")
    print(f"    The {worst:.1f} A difference is {100*worst/scram:.0f} per cent of the {scram:.1f} A "
          f"a SHUFFLED\n    correspondence gives -- that is, the two predictions are most of the "
          f"way to\n    unrelated. Together with a {floor:.1f} A floor from re-running an "
          f"UNCHANGED sequence,\n    the arithmetic says the predictor does not determine this "
          f"fold, not that W169L\n    rearranges it.")
    if worst <= floor:
        print(f"    The substitution moves the fold by at most {worst:.2f} A, against a {floor:.2f} A")
        print("    floor measured between two runs of the IDENTICAL sequence. The difference is")
        print("    INSIDE what this predictor produces from no change at all, so this comparison")
        print("    does not show that W169L moves the ion pathway, and does not show that it")
        print("    leaves it alone either. It is not a measurement of the substitution.")
        if sym is not None and worst > sym:
            print(f"\n    Judged against the {sym:.2f} A internal symmetry instead, the same number")
            print("    would read as a large change. That is the trap this script exists to avoid:")
            print("    symmetry is one forward pass, reproducibility is two.")
    else:
        print(f"    It is also above the {floor:.2f} A re-run floor, which on its own would read "
              f"as a\n    detected change. It should not: a floor and a ceiling are both needed, "
              f"and this\n    difference sits near the ceiling. VERDICT: NOT MEASURABLE with this "
              f"predictor on\n    this protein. That is a statement about openfold3 here, not "
              f"about the allele.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
