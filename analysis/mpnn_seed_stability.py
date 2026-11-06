#!/usr/bin/env python3
"""Is the failed calibration's MISSED verdict a stable fact, or decoding-order noise?

Claim 1079 registered positional-entropy rank as `untrusted`: the selectivity-filter glycines
land inside the most-constrained quartile in the homodimer and OUTSIDE it in the monomer, where
G100 ranks 385 of 448. All three runs behind that verdict used `random_seed=42` and 8 samples.

ProteinMPNN is autoregressive, so a position's entropy depends on where it falls in a random
decoding order. Averaging 8 orders controls that only partly. If the glycine ranks move a long
way under a different seed, the 1-of-3 result is sampling noise and claim 1079 is measuring the
estimator rather than the protein. If they stay put, the metric really does fail to see the
filter in the monomer, and the dimer/monomer difference is structural.

RULED OUT FIRST, cheaply, because it would have explained everything: a mis-indexed slice. The
native sequence in each run's `mfasta` was checked position by position -- GYG sits at 100-102
and GFG at 205-207 in all three, chain B's copies at the expected +448/+240 offsets, and every
position the calibration calls a glycine is a G. The indexing is sound.

This re-runs the MONOMER, the surprising arm, at a different seed and nothing else changed.
"""
from __future__ import annotations

import json
import math
import os
import pathlib
import statistics as st
import sys

HERE = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, str(HERE / ".." / "swarm"))
D = HERE / ".." / "results" / "fish-proteins" / "structures"
GLY = [100, 102, 205, 207]
QUARTILE = 0.25
RUN = "kcnk5b-monomer-msa"


def entropy(p):
    tot = sum(p) or 1.0
    return -sum((x / tot) * math.log2(x / tot) for x in p if x > 0)


def ranks_from_probs(probs, per):
    ent = [st.fmean(entropy(probs[s][i]) for s in range(len(probs))) for i in range(per)]
    order = sorted(range(per), key=lambda i: ent[i])
    rank = {r: i for i, r in enumerate(order)}
    return [rank[g - 1] for g in GLY if g <= per], int(QUARTILE * per)


def main() -> int:
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    import nebius

    pdb = (D / RUN / "model.pdb").read_bytes()
    print(f"  structure {RUN}  ({len(pdb)} bytes)   seed {seed}")

    # baseline, seed 42, already on disk
    base = json.loads((D / RUN / "mpnn" / "result.json").read_text())
    per = len(base["probs"][0])
    b_ranks, cut = ranks_from_probs(base["probs"], per)
    print(f"  baseline seed 42 : glycine ranks {b_ranks}  (quartile cut {cut} of {per})")

    idem = f"ms-{RUN}-mpnn-seed{seed}-v1"
    op, _ = nebius.submit(
        "infer_proteinmpnn_native",
        {"input_pdb": pdb.decode(), "num_seq_per_target": 8, "sampling_temp": 0.1,
         "random_seed": seed, "idempotency_key": idem},
        f"mpnn-seed-stability:{RUN} seed={seed} -- is claim 1079's MISSED verdict seed-stable?")
    print(f"  submitted {op}; waiting")
    nebius.wait(op)
    # get_operation_result returns an ARTIFACT REFERENCE, not the payload: a native
    # proteinmpnn result is ~1.6 MB and is delivered out of band. Reading res["probs"]
    # off the operation reply raises KeyError on a job that SUCCEEDED, which reads like a
    # failed run. fetch_results.py resolves the reference and verifies its sha256.
    out = D / RUN / f"mpnn-seed{seed}"
    out.mkdir(parents=True, exist_ok=True)
    os.system(f"python3 {HERE}/../swarm/fetch_results.py {op} {out}")
    res = json.loads((out / "result.json").read_text())
    n_ranks, _ = ranks_from_probs(res["probs"], per)
    print(f"  seed {seed:>5}        : glycine ranks {n_ranks}")
    moved = [abs(a - b) for a, b in zip(b_ranks, n_ranks)]
    # A movement means nothing without the floor: how far does a TYPICAL position move
    # between two seeds? Without this the glycine numbers are unreadable in either direction.
    def order_of(probs):
        e = [st.fmean(entropy(probs[s][i]) for s in range(len(probs))) for i in range(per)]
        o = sorted(range(per), key=lambda i: e[i])
        return [o.index(i) for i in range(per)]
    floor = [abs(x - y) for x, y in zip(order_of(base["probs"]), order_of(res["probs"]))]
    print(f"\n  rank movement per glycine: {moved}   max {max(moved)}")
    print(f"  FLOOR across all {per} positions: median {st.median(floor):.0f}, "
          f"90th {sorted(floor)[int(0.9 * per)]}, max {max(floor)}")
    print(f"  seed 42 verdict {'CAUGHT' if all(r < cut for r in b_ranks) else 'MISSED'}; "
          f"seed {seed} verdict {'CAUGHT' if all(r < cut for r in n_ranks) else 'MISSED'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
