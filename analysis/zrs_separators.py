#!/usr/bin/env python3
"""S930/S931: is E1 ETS loss the ONLY feature that perfectly separates snakes from non-snakes?

Kvon et al. 2016 showed that replacing the mouse ZRS with a snake ortholog causes severe limb
reduction, and that restoring a single lost ETS binding site reinstates function. The
limbless-mouse project's own analysis records, per taxon, whether that E1 site is present along
with several other alignment features.

The claim worth testing is not "E1 differs between snakes and non-snakes" -- that is how it was
found -- but "E1 is the ONLY such feature". A feature that perfectly separates 5 snakes from 6
non-snakes is not rare by chance: with 11 taxa there are only C(11,5) = 462 ways to split them,
so ANY binary feature has a 1-in-231 chance of separating perfectly, and a threshold chosen on
a continuous feature has a much better chance than that. This computes the exact permutation
probability rather than asserting that a perfect separation is impressive.

NOTHING HERE IS A NEW MEASUREMENT. It reads the project's own zrs-analysis.json, which records
a JASPAR MA0098.3 ETS1 scan at the p<0.0032 threshold Kvon et al. used. The limitation that file
states -- different software, and the E0-E4 site numbering of that paper NOT reproduced -- is
inherited by anything computed here.
"""
from __future__ import annotations

import itertools
import json
import os
import pathlib

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = pathlib.Path(HERE) / ".." / "results" / "limbless-mouse" / "zrs-analysis.json"


def separates(values, is_snake) -> bool:
    """True if some threshold (or the boolean itself) splits snakes from the rest exactly."""
    sn = {v for v, s in zip(values, is_snake) if s}
    ns = {v for v, s in zip(values, is_snake) if not s}
    if isinstance(next(iter(sn | ns)), bool):
        return not (sn & ns)
    return max(sn) < min(ns) or max(ns) < min(sn)


def main() -> int:
    d = json.loads(SRC.read_text())
    raw = d["summary_table"]
    # Pantherophis guttatus is in the table with every feature null -- it was aligned but not
    # scanned. The subproblems say "11 ZRS orthologs already aligned (5 snake, 6 non-snake)",
    # which is this table minus that row. Dropping it SILENTLY would be the wrong kind of
    # tidy, so it is named.
    dropped = [r["species"] for r in raw if r.get("n_ets_motifs") is None]
    tab = [r for r in raw if r.get("n_ets_motifs") is not None]
    print(f"  {len(raw)} rows in {SRC.name}; {len(tab)} usable")
    if dropped:
        print(f"  EXCLUDED for having no scan data: {', '.join(dropped)}")
    print()
    print(f"  {'species':26}{'group':18}{'ETS':>5}{'E1':>6}{'%id':>8}{'core bp':>9}")
    for r in tab:
        print(f"  {r['species'][:25]:26}{r['group'][:17]:18}{r['n_ets_motifs']:>5}"
              f"{str(r['has_e1_ets_site']):>6}{r['pct_identity_to_mouse']:>8.1f}"
              f"{r['core_length_bp']:>9}")

    # The groups are `snake-basal` and `snake-advanced`, NOT `snake`. Testing equality with
    # "snake" makes every taxon a non-snake, and the separation questions below would then all
    # answer against an empty snake set -- a silent wrong answer, not an error.
    is_snake = [str(r["group"]).startswith("snake") for r in tab]
    assert sum(is_snake) == 5, f"expected 5 snakes, got {sum(is_snake)}"
    assert len(tab) - sum(is_snake) == 6, "expected 6 non-snakes"
    n_s, n_n = sum(is_snake), len(tab) - sum(is_snake)
    print(f"\n  {n_s} snakes, {n_n} non-snakes")

    FEATURES = {
        "has_e1_ets_site": [r["has_e1_ets_site"] for r in tab],
        "n_ets_motifs": [r["n_ets_motifs"] for r in tab],
        "pct_identity_to_mouse": [r["pct_identity_to_mouse"] for r in tab],
        "core_length_bp": [r["core_length_bp"] for r in tab],
    }
    print("\n  does each feature separate snakes from non-snakes EXACTLY?")
    perfect = []
    for name, vals in FEATURES.items():
        ok = separates(vals, is_snake)
        perfect.append(name) if ok else None
        sn = sorted({v for v, s in zip(vals, is_snake) if s})
        ns = sorted({v for v, s in zip(vals, is_snake) if not s})
        print(f"    {name:24} {'YES' if ok else 'no ':4}  snakes {str(sn)[:34]:36} "
              f"others {str(ns)[:34]}")

    # The permutation baseline: how surprising is ONE perfect separation?
    total = len(list(itertools.combinations(range(len(tab)), n_s)))
    print(f"\n  PERMUTATION BASELINE. With {len(tab)} taxa there are C({len(tab)},{n_s}) = "
          f"{total} ways to choose which are 'snakes'.")
    for name, vals in FEATURES.items():
        hits = sum(1 for idx in itertools.combinations(range(len(tab)), n_s)
                   if separates(vals, [i in idx for i in range(len(tab))]))
        print(f"    {name:24} separates {hits:>4} of {total} labellings "
              f"(p = {hits/total:.4f} for a random split)")

    print("\n  ANSWER")
    if len(perfect) == 1:
        print(f"    {perfect[0]} is the ONLY feature here that separates perfectly -- "
              f"S930/S931 answered YES on the data this project holds.")
    else:
        print(f"    {len(perfect)} features separate perfectly: {perfect}")
        print("    So E1 is NOT the only separator in this data, and S930/S931 answer NO.")
        print("    That does not refute Kvon et al. -- they showed E1 is CAUSAL by restoring")
        print("    it -- but it does mean the alignment alone cannot single E1 out.")

    print("\n  CONTROLS")
    # must-not-separate: a constant feature cannot separate anything
    const = [1] * len(tab)
    print(f"    a constant feature separates: {separates(const, is_snake)} (must be False)")
    # must-separate: the group label itself, by construction
    print(f"    the group label itself separates: {separates(is_snake, is_snake)} (must be True)")
    # and the permutation count for a perfect-by-construction feature must be small
    hits = sum(1 for idx in itertools.combinations(range(len(tab)), n_s)
               if separates(is_snake, [i in idx for i in range(len(tab))]))
    print(f"    the group label separates {hits} of {total} labellings "
          f"(a lower bound on how special ANY perfect separator is)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
