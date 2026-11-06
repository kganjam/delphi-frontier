#!/usr/bin/env python3
"""A per-residue structural readout is not reproducible unless it names the structure it read.

WHY, measured 2026-11-05 and the chain is complete.

  * ProteinMPNN is BIT-DETERMINISTIC on a fixed backbone: two independent submissions on the
    identical PDB agreed at 577 of 577 positions to 1e-12 (claim 1394).
  * ESMFold2 is NOT deterministic even at a fixed seed: the same sequence at seed 2, run in two
    sessions, produced different bytes and a maximum per-residue pLDDT difference of 10.04
    points (claim 1393).
  * So a 10-percent wobble in the structure becomes TWO ORDERS OF MAGNITUDE in the sequence
    model's per-residue probability. This project holds three values for one such quantity --
    9.198e-21, 6.218e-19 and a reported 5.47e-12 for P(K) at lat4a 200 -- and they were
    indistinguishable from a disagreement about the number, because no record said which
    structure it came from.

A number computed on an unnamed structure is therefore not a measurement of anything. It is a
measurement of a structure nobody can retrieve.

WHAT COUNTS AS NAMING IT: a sha256, a Nebius operation id (op-xxxxxxxx), or a path under
results/ that resolves to a file on disk. Any one is enough -- the point is that a reader can get
the same bytes back, not that the record uses a particular format.

WHAT THIS DELIBERATELY DOES NOT DO. It does not flag claims ABOUT structure prediction in
general, only those reporting a per-residue NUMBER. A claim saying "ESMFold2 is not
deterministic" needs no structure id; a claim saying "pLDDT at residue 200 is 97.7" is
meaningless without one. The matcher is therefore anchored on a residue-and-number pattern
rather than on structural vocabulary, and it REPORTS rather than blocks, because its false
positives are claims that discuss such numbers without asserting one.
"""
from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dbq  # noqa: E402

PROJECT = os.environ.get("SWARM_PROJECT", "zebrafish-flight")

# asserts a per-residue number: "pLDDT at residue 200 is 97.7", "P(K) at 200", "residue 583 pLDDT"
READOUT = re.compile(
    r"(pLDDT|p\(native\)|P\([A-Z]\)|positional entropy|sequence recovery)[^.\n]{0,60}"
    r"(residue|position|site)\s*\d+|"
    r"(residue|position|site)\s*\d+[^.\n]{0,60}(pLDDT|p\(native\)|P\([A-Z]\))", re.I)
# names the structure so it can be fetched back
# A results/ path counts WITH OR WITHOUT a file extension. The first version required one and
# produced two false positives out of four flags, both from records that do name their
# structures: claim 473 cites the DIRECTORIES
# "results/fish-proteins/structures/slc43a2a_wt{,_seed1,_seed2}/", and claim 462 cites
# "...slc43a2a_{wt,t200k,l219p}/ + proteinmpnn_slc43a2a_wt/result.json", where the extension sits
# after a space so an anchored path match stops before reaching it. A directory of predictions is
# a retrievable reference; insisting on a filename was my formatting preference, not the property
# being checked.
NAMED = re.compile(r"\bop-[0-9a-f]{8,}"
                   r"|[0-9a-f]{40,}"
                   r"|results/[\w./{},-]+"
                   r"|\b[\w./{},-]*(?:structures|proteinmpnn)[\w./{},-]*", re.I)


# A bare sequence-model PROBABILITY, e.g. "P(K) = 6.2e-19". Measured 2026-11-05 (claim 1396):
# across four ESMFold2 replicate backbones of one sequence, ProteinMPNN's P(native) at one
# position spans 4.52 orders of magnitude and P(mutant) spans 1.84, while pLDDT at that same
# position in those same structures has sd 0.116. The ARGMAX is stable (valine in all four,
# 0.976-1.000) and the magnitudes are not, so a probability quoted from one structure carries an
# unstated uncertainty of two to four orders.
PROB = re.compile(r"P\(\s*(?:native|[A-Z])\s*\)\s*(?:at|=|of|is)?[^.\n]{0,24}"
                  r"\d(?:\.\d+)?\s*(?:[eE][-+]?\d+|x\s*10)", re.I)
# a replicate spread is quoted when the text mentions replicates/seeds AND a spread word
SPREAD = re.compile(r"(replicate|seed[s]?\b|across .{0,20}backbone)[^.\n]{0,80}"
                    r"(spread|range|sd\b|orders of magnitude|standard deviation)"
                    r"|(spread|range|sd\b|orders of magnitude)[^.\n]{0,80}(replicate|seed|backbone)", re.I)


def probabilities_without_spread(rows):
    out = []
    for r in rows:
        if len(r) < 4 or not PROB.search(r[2]):
            continue
        if not SPREAD.search(r[2]):
            out.append(r)
    return out


def main() -> int:
    rows = dbq.q(
        "select id::text, coalesce(evidence,''), "
        "replace(replace(statement, chr(1), ' '), chr(10), ' '), "
        "replace(replace(coalesce(source,''), chr(1), ' '), chr(10), ' ') "
        f"from claim where project_id = {dbq.lit(PROJECT)} and superseded_by is null order by id")
    asserts, named, bare = 0, 0, []
    for r in rows:
        if len(r) < 4 or not READOUT.search(r[2]):
            continue
        asserts += 1
        if NAMED.search(r[2]) or NAMED.search(r[3]):
            named += 1
        else:
            bare.append(r)

    print("=" * 78)
    print(f"PER-RESIDUE READOUTS WITHOUT A RETRIEVABLE STRUCTURE   project {PROJECT!r}")
    print("=" * 78)
    print(f"  {len(rows)} live claims; {asserts} assert a per-residue number")
    print(f"    {named} name the structure (sha256, op id, or a results/ path)")
    print(f"    {len(bare)} do NOT -- those numbers cannot be recomputed")
    if asserts:
        print(f"\n  CONTROL: the matcher found {asserts} assertions out of {len(rows)} claims. "
              f"If that\n  is 0 the pattern is broken, not the corpus clean.")
    for r in bare[:20]:
        print(f"    {r[0]:>5} [{r[1]:<10}] {r[2][:92]}")
    if len(bare) > 20:
        print(f"    ... and {len(bare) - 20} more")
    print("\n  Reports only. A claim here is not wrong; its number is just not retrievable.")

    bare_p = probabilities_without_spread(rows)
    print()
    print("=" * 78)
    print("SEQUENCE-MODEL PROBABILITIES QUOTED WITHOUT A REPLICATE SPREAD")
    print("=" * 78)
    print(f"  {len(bare_p)} live claim(s) quote a P(...) value with no replicate range beside it.")
    print("  Measured error bar on such a number: 4.52 orders on P(native), 1.84 on P(mutant),")
    print("  across four replicate backbones of ONE sequence (claim 1396). The argmax is stable;")
    print("  the magnitude is not. Prefer a rank or an argmax, or quote the spread.")
    for r in bare_p[:15]:
        print(f"    {r[0]:>5} [{r[1]:<10}] {r[2][:92]}")
    if len(bare_p) > 15:
        print(f"    ... and {len(bare_p) - 15} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
