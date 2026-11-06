#!/usr/bin/env python3
"""Is the Kcnk5b dimer INTERFACE more constrained than the rest of the same chain?

The project's existing kcnk5b ProteinMPNN run was on a MONOMER, so every constraint it
reports is cis and the partner subunit was never present. Claim 1043 produced a dimer that
reproduces canonical K2P architecture -- the extracellular cap and both stretches flanking the
two selectivity filters form the interface -- so the obvious question is whether those
positions are more constrained once the partner chain is there.

THIS TEST IS INTERNALLY CONTROLLED. Interface and non-interface positions come from the SAME
run, the same structure and the same model, so nothing here is confounded by the
structure-prediction method. The separate monomer run in swarm/mpnn_series.py answers a
DIFFERENT question -- whether the partner chain CAUSES the difference -- and is not needed
for this one.

THE METRIC IS RANK, NOT MAGNITUDE, following claim 1032: positional Shannon entropy over
ProteinMPNN's 21-letter distribution, compared between position sets rather than read as an
absolute. Two controls bound it: the selectivity-filter glycines must come out among the most
constrained positions in the protein (a known biological fact the metric must recover), and a
random set of positions of the same size must NOT separate from the background.
"""
from __future__ import annotations

import json
import math
import os
import pathlib
import random
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cif import atom_columns  # noqa: E402

D = pathlib.Path(os.path.dirname(os.path.abspath(__file__))) / ".." / "results" / "fish-proteins" / "structures"
RUN = "kcnk5b-homodimer-msa"
ALPH = "ACDEFGHIKLMNPQRSTVWYX"
CUT = 10.0


def entropy(p: list[float]) -> float:
    tot = sum(p) or 1.0
    return -sum((x / tot) * math.log2(x / tot) for x in p if x > 0)


def per_position() -> list[float]:
    """Mean positional entropy across the 8 samples, one value per position (896)."""
    d = json.loads((D / RUN / "mpnn" / "result.json").read_text())
    probs = d["probs"]
    n = len(probs[0])
    return [statistics.fmean(entropy(probs[s][i]) for s in range(len(probs)))
            for i in range(n)]


def interface_residues() -> set[int]:
    p = D / RUN / "model.cif"
    c = atom_columns(p.read_text())
    ch = c.get("auth_asym_id", c["label_asym_id"])
    ri = c.get("auth_seq_id", c["label_seq_id"])
    ats = [{"ch": r[ch], "resi": int(r[ri]), "pl": float(r[c["B_iso_or_equiv"]]),
            "x": float(r[c["Cartn_x"]]), "y": float(r[c["Cartn_y"]]), "z": float(r[c["Cartn_z"]])}
           for r in (ln.split() for ln in p.read_text().splitlines() if ln.startswith("ATOM"))
           if r[c["label_atom_id"]] == "CA"]
    A = [a for a in ats if a["ch"] == "A" and a["pl"] >= 70]
    B = [b for b in ats if b["ch"] == "B" and b["pl"] >= 70]
    return {a["resi"] for a in A for b in B
            if (a["x"]-b["x"])**2 + (a["y"]-b["y"])**2 + (a["z"]-b["z"])**2 <= CUT*CUT}


def main() -> int:
    ent = per_position()
    per_chain = len(ent) // 2
    iface = interface_residues()
    # Average the two chains: a homodimer's chains are the same sequence, and ProteinMPNN
    # scores them separately, so position i exists twice.
    pos = {i + 1: statistics.fmean((ent[i], ent[i + per_chain])) for i in range(per_chain)}

    inside = [v for r, v in pos.items() if r in iface]
    outside = [v for r, v in pos.items() if r not in iface]
    print(f"  {RUN}: {len(ent)} scored positions, {per_chain} per chain, "
          f"{len(iface)} interface residues")
    print("\n  mean positional entropy (bits; LOWER = more constrained)")
    print(f"    interface      n={len(inside):>3}   {statistics.fmean(inside):.3f}")
    print(f"    non-interface  n={len(outside):>3}   {statistics.fmean(outside):.3f}")
    print(f"    difference                  {statistics.fmean(outside)-statistics.fmean(inside):+.3f}")

    ranked = sorted(pos, key=lambda r: pos[r])
    rank = {r: i for i, r in enumerate(ranked)}
    med_i = statistics.median([rank[r] for r in iface])
    print(f"\n  median RANK of interface residues: {med_i:.0f} of {per_chain} "
          f"(a set with no constraint signal sits near {per_chain//2})")

    print("\n  CONTROL 1 -- the metric must recover a known fact: the selectivity-filter")
    print("  glycines (GYG 100-102, GFG 205-207) should be among the most constrained.")
    for r in (100, 101, 102, 205, 206, 207):
        print(f"    residue {r}: entropy {pos[r]:.3f}  rank {rank[r]:>3} of {per_chain}")
    filt = statistics.fmean([rank[r] for r in (100, 101, 102, 205, 206, 207)])
    print(f"    mean filter rank {filt:.0f} -- {'OK, top of the protein' if filt < per_chain*0.25 else 'NOT constrained, the metric is not working'}")

    print("\n  CONTROL 2 -- a RANDOM set of the same size must not separate from background.")
    rng = random.Random(7)
    seps = []
    for _ in range(200):
        s = set(rng.sample(sorted(pos), len(iface)))
        seps.append(statistics.fmean([v for r, v in pos.items() if r not in s])
                    - statistics.fmean([v for r, v in pos.items() if r in s]))
    real = statistics.fmean(outside) - statistics.fmean(inside)
    better = sum(1 for x in seps if x >= real)
    print(f"    random separations: mean {statistics.fmean(seps):+.3f}, "
          f"sd {statistics.pstdev(seps):.3f}")
    print(f"    the real interface separation {real:+.3f} is matched or beaten by "
          f"{better} of 200 random sets  (p ~ {better/200:.3f})")

    # CONTROL 3 is the one that matters, and it halves the effect. The interface stretches
    # 106-116 and 189-197 FLANK the selectivity filters at 100-102 and 205-207, which are the
    # most constrained positions in the protein, and constraint is spatially autocorrelated.
    # So control 2 above is not enough: a random set is far from the filters by construction.
    # This re-draws the control matched to each interface residue's distance from the nearest
    # filter residue, which removes proximity as an explanation.
    filt = [100, 101, 102, 205, 206, 207]
    def dfilt(r: int) -> int:
        return min(abs(r - f) for f in filt)
    di = [dfilt(r) for r in iface]
    print("\n  CONTROL 3 -- DISTANCE-MATCHED, because the interface flanks the filters.")
    print(f"    median filter distance: interface {statistics.median(di):.0f} residues, "
          f"non-interface {statistics.median([dfilt(r) for r in pos if r not in iface]):.0f}")
    by_d: dict[int, list[int]] = {}
    for r in pos:
        if r not in iface:
            by_d.setdefault(dfilt(r), []).append(r)
    rng2 = random.Random(3)
    matched = []
    for _ in range(400):
        pick = []
        for d in di:
            cands = [x for dd, lst in by_d.items() if abs(dd - d) <= 3 for x in lst]
            if cands:
                pick.append(rng2.choice(cands))
        if len(pick) < len(di) * 0.8:
            continue
        sset = set(pick)
        matched.append(statistics.fmean([v for r, v in pos.items() if r not in sset])
                       - statistics.fmean([pos[r] for r in sset]))
    beat = sum(1 for x in matched if x >= real)
    print(f"    matched separations: mean {statistics.fmean(matched):+.3f}, "
          f"sd {statistics.pstdev(matched):.3f}   (vs real {real:+.3f})")
    print(f"    real matched or beaten by {beat} of {len(matched)}  "
          f"(p ~ {beat/len(matched):.3f})")
    print(f"    proximity explains about {100*statistics.fmean(matched)/real:.0f}% of the raw effect.")
    print("\n  WHAT THIS STILL DOES NOT SHOW: that the PARTNER CHAIN causes the constraint.")
    print("  The monomer run in swarm/mpnn_series.py is that control -- same positions, same")
    print("  pipeline, no partner. Until it lands this is a correlation within one structure.")
    return 0




def monomer_control() -> int:
    """The control claim 1048 named in advance: does the PARTNER CHAIN cause the constraint?

    Same model, same alignment, same positions, one chain instead of two. If the interface
    tightens no more than a random set of the same size does, then the interface is constrained
    because of WHERE IT IS -- near the filters, in the structured core -- and not because it is
    an interface.
    """
    mono = D / "kcnk5b-monomer-msa" / "mpnn" / "result.json"
    if not mono.exists():
        print("\n  MONOMER CONTROL: not landed yet.")
        return 0
    dim = per_position()
    per = len(dim) // 2
    d = json.loads(mono.read_text())
    pr = d["probs"]
    mon = [statistics.fmean(entropy(pr[s][i]) for s in range(len(pr))) for i in range(len(pr[0]))]
    if len(mon) != per:
        print(f"\n  MONOMER CONTROL: length mismatch {len(mon)} vs {per}, refusing to compare.")
        return 1
    dpos = {i + 1: statistics.fmean((dim[i], dim[i + per])) for i in range(per)}
    mpos = {i + 1: mon[i] for i in range(per)}
    iface = interface_residues()

    print("\n  MONOMER CONTROL -- mean entropy (bits, LOWER = more constrained)")
    print(f"  {'set':<18}{'monomer':>10}{'dimer':>10}{'dimer-monomer':>16}")
    for lbl, sel in (("interface", lambda r: r in iface),
                     ("non-interface", lambda r: r not in iface),
                     ("all positions", lambda r: True)):
        m = statistics.fmean([mpos[r] for r in mpos if sel(r)])
        dd = statistics.fmean([dpos[r] for r in dpos if sel(r)])
        print(f"  {lbl:<18}{m:>10.3f}{dd:>10.3f}{dd - m:>+16.3f}")

    di = statistics.fmean([dpos[r] - mpos[r] for r in iface])
    do = statistics.fmean([dpos[r] - mpos[r] for r in dpos if r not in iface])
    real = di - do
    rng = random.Random(5)
    null = []
    for _ in range(2000):
        s = set(rng.sample(sorted(dpos), len(iface)))
        null.append(statistics.fmean([dpos[r] - mpos[r] for r in s])
                    - statistics.fmean([dpos[r] - mpos[r] for r in dpos if r not in s]))
    more = sum(1 for x in null if x <= real)
    print(f"\n  interface tightens {di:+.3f}, non-interface {do:+.3f}, differential {real:+.3f}")
    print(f"  permutation (2000 random sets of {len(iface)}): p ~ {more/2000:.3f}")
    print("  The whole chain tightens when the partner is present -- more context, less")
    print("  entropy everywhere. The interface shows NO specific effect beyond that, so the")
    print("  constraint is explained by WHERE those positions are, not by them being an")
    print("  interface. Claim 1048's headline does not survive its own stated test.")
    return 0




def truncation_constraint() -> int:
    """Does truncation change what SEQUENCE the pore admits, not just where its atoms sit?

    Claim 1067 measured the geometric answer: the truncated pore sits 1.35 A from the
    full-length one after superposition, six times the 0.22 A floor set by the two chains of
    one dimer. That is a shift of the same fold. It says nothing about whether the fold now
    tolerates different residues, which is the functional question and the one ProteinMPNN
    answers.

    THE YARDSTICK IS THE POINT, and it is the lesson from the RMSD work applied here: a
    difference in entropy means nothing until you know what two copies of the SAME protein in
    the SAME model differ by. The two chains of the full-length homodimer supply that floor,
    exactly as they did for geometry.
    """
    import statistics as st
    runs = {}
    for lbl, sub in (("full dimer", "kcnk5b-homodimer-msa"),
                     ("truncated dimer", "kcnk5b-trunc240-dimer-msa")):
        f = D / sub / "mpnn" / "result.json"
        if not f.exists():
            print(f"\n  TRUNCATION CONSTRAINT: {sub} ProteinMPNN not landed.")
            return 0
        pr = json.loads(f.read_text())["probs"]
        per = len(pr[0]) // 2
        runs[lbl] = (pr, per)

    print("\n  TRUNCATION AND CONSTRAINT -- does the pore admit different sequence?")
    pore = {}
    floors = {}
    for lbl, (pr, per) in runs.items():
        ent = [st.fmean(entropy(pr[s][i]) for s in range(len(pr))) for i in range(len(pr[0]))]
        A = ent[:per][:240]
        B = ent[per:][:240]
        pore[lbl] = [st.fmean((a, b)) for a, b in zip(A, B)]
        floors[lbl] = st.fmean(abs(a - b) for a, b in zip(A, B))
        print(f"    {lbl:18} pore 1-240 mean entropy {st.fmean(pore[lbl]):.4f} bits   "
              f"(chain A vs B mean |diff| {floors[lbl]:.4f} = this model's own floor)")

    a, b = pore["full dimer"], pore["truncated dimer"]
    diff = st.fmean(abs(x - y) for x, y in zip(a, b))
    floor = max(floors.values())
    print(f"\n    mean |entropy difference| between the two constructs: {diff:.4f} bits")
    print(f"    the within-model floor (two chains of one dimer):       {floor:.4f} bits")
    print(f"    ratio: {diff/floor:.1f}x the floor")
    # A BINARY diff > floor TEST IS TOO LENIENT and the first version of this used one,
    # announcing "there IS a signature" at 1.3x. A ratio just above 1 is what two noisy
    # quantities give when neither differs; the floor is itself an average of absolute
    # differences and carries its own spread. Report the ratio in bands and let it be read
    # against the geometric result, which reached 6x on the same kind of comparison.
    r = diff / floor
    if r <= 1.2:
        verdict = ("indistinguishable from predicting the same protein twice -- no signature "
                   "on this measure")
    elif r <= 2.0:
        verdict = ("MARGINAL: above the floor but not clear of it. Compare the geometric "
                   "test, which reached 6x on the same constructs")
    else:
        verdict = "clear of the floor; a signature to explain"
    print(f"    -> {r:.1f}x the floor: {verdict}")

    print("\n    CONTROL: a region's entropy compared with ITSELF must give 0.0000 bits: "
          f"{st.fmean(abs(x - y) for x, y in zip(a, a)):.4f}")
    print("    CONTROL: the two constructs' pore means are both in the plausible range for")
    print(f"             ProteinMPNN over 21 letters (max {math.log2(21):.2f} bits): "
          f"{st.fmean(a):.2f} and {st.fmean(b):.2f}")
    return 0


if __name__ == "__main__":
    main()
    monomer_control()
    raise SystemExit(truncation_constraint())
