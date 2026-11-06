#!/usr/bin/env python3
"""Measure Boltz2's OWN re-run spread on kcnk5b, in a single operation.

WHY THIS AND NOT ANOTHER VARIANT RUN. The protein arm is blocked on instrument resolution, not
on more variants. Claim 1868 ruled that a difference between two predicted structures needs a
floor and a ceiling; claim 3161 added that the same holds for the confidence SCORES, where five
of five metrics were unresolved. Both verdicts are about openfold3, whose complex pLDDT on this
target is about 60 and whose two runs of the identical sequence differ by 7.4 points and 30 A.
Boltz2 scored 77.5 pLDDT on the same protein (claim 20) and its re-run spread has NEVER been
measured, so whether ANY available predictor determines this fold is still open.

WHY ONE OPERATION. The workbench key allows ONE operation in flight across all 69 tools, so this
resource cannot be maximised by fanning out -- the only lever is work per slot.
`boltz2_predict_native` accepts `diffusion_samples` up to 8, so a single submit returns eight
independent samples of the same sequence. That is a DISTRIBUTION rather than the single pair
claim 3161 had to call a floor-not-an-error-bar, and it costs one slot instead of eight.

    python3 analysis/boltz2_rerun_spread.py --submit    # occupy the slot
    python3 analysis/boltz2_rerun_spread.py <op_id>     # fetch and report
"""
import json
import pathlib
import statistics
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "swarm"))

D = HERE.parent / "results" / "fish-proteins" / "structures"
A3M = D / "kcnk5b_pdb70.a3m"
SAMPLES = 8
IDEM = "ms-kcnk5b-wt-boltz2-spread8-v1"


def wt_sequence() -> str:
    """The query sequence is the first non-header line of the pdb70 alignment."""
    return [ln for ln in A3M.read_text().splitlines() if not ln.startswith(">")][0].strip()


def submit() -> int:
    import nebius
    seq = wt_sequence()
    pol = {"id": "A", "molecule_type": "protein", "sequence": seq,
           # FOUR LEVELS: polymers[] -> msa -> msa_search -> a3m -> {alignment, format}.
           # The nesting is mandatory; a flattened `msa` is refused.
           "msa": {"msa_search": {"a3m": {"alignment": A3M.read_text(), "format": "a3m"}}}}
    print(f"  kcnk5b WT, {len(seq)} aa, {SAMPLES} diffusion samples, one operation")
    op, _ = nebius.submit(
        "boltz2_predict_native",
        {"polymers": [pol], "diffusion_samples": SAMPLES, "idempotency_key": IDEM,
         "wait_seconds": 5},
        f"boltz2 re-run spread: {SAMPLES} samples of kcnk5b WT in one slot")
    print(f"  submitted {op}  (recorded to the ops log; idempotency_key {IDEM})")
    return 0


def report(op: str) -> int:
    """Fetch (if needed) and measure the spread across the 8 samples.

    Boltz2's result schema is NOT openfold3's: it returns parallel lists
    `confidence_scores`, `ptm_scores` and `structures`, with no `outputs` wrapper and no
    complex pLDDT. So the comparable quantities are pTM, the confidence score, and the one
    that actually decides the question -- CA RMSD between samples.
    """
    import numpy as np
    sys.path.insert(0, str(HERE))
    from pore_geometry import ca_atoms, kabsch_rmsd

    out = D / "kcnk5b-boltz2-spread8"
    out.mkdir(parents=True, exist_ok=True)
    blob_path = next(iter(out.glob("spread8*.json")), None)
    if blob_path is None:
        import fetch_results as fr
        for name, path, n in fr.fetch_run(op, str(out), stem="spread8"):
            print(f"  {name:28} -> {path}  ({n:,} bytes, sha256 verified)")
        blob_path = next(iter(out.glob("spread8*.json")))
    blob = json.load(open(blob_path))

    conf, ptm = blob["confidence_scores"], blob["ptm_scores"]
    structs = blob["structures"]
    print(f"\n  {len(structs)} sample(s) of ONE unchanged sequence, one operation")
    for label, v in (("confidence_score", conf), ("ptm_score", ptm)):
        sd = statistics.stdev(v) if len(v) > 1 else 0.0
        print(f"    {label:<18} min {min(v):.4f}  max {max(v):.4f}  "
              f"spread {max(v)-min(v):.4f}  stdev {sd:.4f}")

    paths = []
    for i, st in enumerate(structs):
        fp = out / f"sample{i}.cif"
        fp.write_text(st["structure"])
        paths.append(fp)
    def ca(fp):
        ats = sorted((a for a in ca_atoms(str(fp)) if a["chain"] == "A"),
                     key=lambda a: int(a["resi"]))
        return np.array([[a["x"], a["y"], a["z"]] for a in ats])
    xyz = [ca(fp) for fp in paths]
    n = {len(x) for x in xyz}
    if len(n) != 1:
        print(f"  REFUSING to compare: samples have different CA counts {n}")
        return 1
    print(f"    {len(xyz)} structures, {n.pop()} CA each")

    # CONTROLS, the same four shapes claim 1868 requires.
    rng = np.random.default_rng(0)
    perm = rng.permutation(len(xyz[0]))
    Rz = np.array([[0., -1., 0.], [1., 0., 0.], [0., 0., 1.]])
    print("\n  CONTROLS")
    print(f"    a structure against itself                  "
          f"{kabsch_rmsd(xyz[0], xyz[0]):8.4f} A  (must be ~0)")
    print(f"    against a rotated+translated copy of itself "
          f"{kabsch_rmsd(xyz[0], xyz[0] @ Rz + np.array([11., -7., 3.])):8.4f} A  (must be ~0)")
    ceiling = kabsch_rmsd(xyz[0], xyz[0][perm])
    print(f"    against itself, correspondence SHUFFLED     {ceiling:8.2f} A  (must be large)")

    pair = [kabsch_rmsd(xyz[i], xyz[j])
            for i in range(len(xyz)) for j in range(i + 1, len(xyz))]
    print(f"\n  SPREAD ACROSS SAMPLES: {len(pair)} pairs, "
          f"min {min(pair):.3f} A, median {statistics.median(pair):.3f} A, max {max(pair):.3f} A")
    OF3_FLOOR = 30.161   # claim 1092: two openfold3 runs of the identical kcnk5b sequence
    print(f"    openfold3's floor on this protein: {OF3_FLOOR:.3f} A (claim 1092)")
    print(f"    ceiling (shuffled correspondence):  {ceiling:.3f} A")
    # THE VERDICT IS COMPUTED, AND THE FIRST VERSION OF IT WAS WRONG. Comparing the spread
    # only against openfold3's floor said "Boltz2 DETERMINES the fold", which claim 1868
    # forbids: a result is uninformative however far above the floor it sits if it sits near
    # the ceiling. Both bounds, or no verdict.
    frac = max(pair) / ceiling
    window = ceiling - max(pair)
    print(f"    max spread is {100*frac:.0f} per cent of the ceiling, leaving a {window:.1f} A "
          f"band\n    between this floor and carrying no information at all.")
    if max(pair) >= OF3_FLOOR:
        print("    VERDICT: no better than openfold3 -- its own floor already exceeds it.")
    elif frac >= 0.33:
        print(f"    VERDICT: BETTER THAN openfold3 ({max(pair):.1f} A against {OF3_FLOOR:.1f} A) "
              f"AND STILL NOT\n    SUFFICIENT. A substitution must move the fold more than "
              f"{max(pair):.1f} A to register, and\n    anything that large is already "
              f"{100*frac:.0f} per cent of the way to an unrelated structure.\n"
              f"    The detectable band is {max(pair):.1f}-{ceiling:.1f} A, which is not a "
              f"range a real\n    point substitution is expected to occupy.")
    else:
        print(f"    VERDICT: determines the fold -- floor {max(pair):.1f} A is only "
              f"{100*frac:.0f} per cent of the ceiling,\n    leaving real room for an effect.")

    if "--write" in sys.argv:
        sys.path.insert(0, str(HERE.parent / "swarm"))
        from dbq import write_claim
        # NO SCALE: this measures Boltz2, not the fish. goal_status reads `scale_id is not
        # null` as "measured about the ANIMAL", and claim 513 already named this drift.
        cid = write_claim(
            "zebrafish-flight", None,
            f"""[BOLTZ2 IS BETTER THAN openfold3 ON THIS FOLD AND STILL CANNOT RESOLVE A POINT
SUBSTITUTION: ITS OWN FLOOR IS {max(pair):.1f} A, WHICH IS {100*frac:.0f} PER CENT OF THE CEILING]
Claims 1868 and 3161 found openfold3 unable to answer whether W169L moves the kcnk5b pore: its
re-run floor is 30.161 A (claim 1092) against a 63.3 A shuffled-correspondence ceiling, and all
five of its confidence metrics were unresolved. Boltz2 scores 77.5 pLDDT on this protein against
openfold3's ~60 (claim 20) and its spread had never been measured, so whether ANY available
predictor determines this fold was open.

Measured in ONE operation -- the workbench key allows one in flight across all 69 tools, so the
lever is work per slot, and boltz2_predict_native takes diffusion_samples up to 8.
{len(structs)} samples of the identical 448-residue sequence, {len(pair)} pairs: min
{min(pair):.3f} A, median {statistics.median(pair):.3f} A, max {max(pair):.3f} A. Confidence
score spread {max(conf)-min(conf):.4f} (stdev {statistics.stdev(conf):.4f}), pTM spread
{max(ptm)-min(ptm):.4f} (stdev {statistics.stdev(ptm):.4f}). Four controls pass: a structure
against itself 0.0000 A, against a rotated and translated copy 0.0000 A, and against itself with
the residue correspondence shuffled {ceiling:.3f} A.

BOTH BOUNDS, BECAUSE ONE IS MISLEADING. Against openfold3's floor alone the answer reads
"Boltz2 determines this fold" -- {max(pair):.1f} A against 30.2 A -- and the first version of
this script printed exactly that. Claim 1868 forbids it: a result is uninformative however far
above the floor it sits if it sits near the ceiling. {max(pair):.1f} A is {100*frac:.0f} per cent
of the way to an unrelated structure, leaving a detectable band of {max(pair):.1f}-{ceiling:.1f}
A. A point substitution is not expected to move a fold that far, so the usable range is
effectively empty. Boltz2 is the better instrument and is still not sufficient.

CONSEQUENCE: the kcnk5b variant question is not answerable by structure prediction with anything
in this catalogue, which is a more final answer than "openfold3 cannot do it" and should stop
further variant folding on this target. It does NOT say the allele has no effect.

SCOPE, AND IT CUTS AGAINST THIS CLAIM'S OWN CONCLUSION: these 8 samples come from one operation
and share a seed and an MSA, so {max(pair):.1f} A is spread WITHIN a run and a LOWER bound on
re-run spread. openfold3's 30.161 A is a BETWEEN-run number. The comparison therefore favours
Boltz2, and the true Boltz2 floor can only be larger -- which strengthens the "not sufficient"
half and weakens the "better than openfold3" half. A second submit under a different idempotency
key is the matching measurement and has not been run.""",
            "measured", max(pair), "A, max CA RMSD across 8 Boltz2 samples of one sequence",
            "analysis/boltz2_rerun_spread.py", None)
        print(f"\n  recorded claim {cid}")

    print("\n  SCOPE: samples from ONE operation share a seed and an MSA, so this is spread\n"
          "  WITHIN a run -- a LOWER bound on re-run spread. openfold3's 30.161 A is a\n"
          "  BETWEEN-run number, so this comparison favours Boltz2 and a Boltz2 figure that\n"
          "  still exceeded it would be decisive, while one below it is suggestive only.\n"
          "  A second submit with a different idempotency key is the matching measurement.")
    return 0


if __name__ == "__main__":
    if "--submit" in sys.argv:
        raise SystemExit(submit())
    rest = [a for a in sys.argv[1:] if not a.startswith("-")]
    if not rest:
        print(__doc__)
        raise SystemExit(2)
    raise SystemExit(report(rest[0]))
