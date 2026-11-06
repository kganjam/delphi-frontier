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
    import fetch_results as fr
    out = D / "kcnk5b-boltz2-spread8"
    out.mkdir(parents=True, exist_ok=True)
    for name, path, n in fr.fetch_run(op, str(out), stem="spread8"):
        print(f"  {name:28} -> {path}  ({n:,} bytes, sha256 verified)")
    blob = json.load(open(next(iter(out.glob("spread8*.json")))))
    scored = blob["outputs"][0]["structures_with_scores"]
    print(f"\n  {len(scored)} sample(s) of ONE unchanged sequence")
    keys = [k for k in scored[0] if k.endswith("_score")]
    print(f"    {'metric':<24}{'min':>10}{'max':>10}{'spread':>10}{'stdev':>10}")
    for k in keys:
        v = [s[k] for s in scored]
        sd = statistics.stdev(v) if len(v) > 1 else 0.0
        print(f"    {k:<24}{min(v):>10.4f}{max(v):>10.4f}{max(v)-min(v):>10.4f}{sd:>10.4f}")
    print("\n  READ THIS AGAINST openfold3's 7.4365 complex pLDDT between two runs of the same\n"
          "  sequence (claim 3161). A SMALLER spread here means Boltz2 determines this fold\n"
          "  where openfold3 does not, and the variant questions become askable on Boltz2.\n"
          "  A comparable spread means the fold is not determined by any predictor on hand,\n"
          "  which is a different and more final answer than 'openfold3 cannot do it'.")
    print("\n  SCOPE: diffusion samples from ONE operation share a seed and an MSA, so this is\n"
          "  the spread WITHIN a run, not between runs. It is a LOWER bound on re-run spread,\n"
          "  and a separate submit is needed before calling it reproducibility.")
    return 0


if __name__ == "__main__":
    if "--submit" in sys.argv:
        raise SystemExit(submit())
    rest = [a for a in sys.argv[1:] if not a.startswith("-")]
    if not rest:
        print(__doc__)
        raise SystemExit(2)
    raise SystemExit(report(rest[0]))
