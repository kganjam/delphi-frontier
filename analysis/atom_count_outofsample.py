#!/usr/bin/env python3
"""Score the atom-count model (claim 517) against its registered out-of-sample prediction (claim 518).

The model: the pLDDT at a substituted site is FLAT iff the new side chain carries at most FOUR
heavy atoms. It was fitted on 13 residues at slc43a2a position 200 -- NONE of which were chosen
to test atom count; they were picked to test charge, sign and reach. Claim 518 registered the
prediction BEFORE the run: methionine and leucine each carry four heavy atoms, so both must be
flat, under 1.5 pLDDT of change.

This script does three things:
  1. scores the registered prediction for every residue that has landed;
  2. re-fits nothing -- it reports the separation the data actually show;
  3. ships a POSITIVE CONTROL: it asserts the model's own training set still separates, so a
     parsing error that flattened every number could not be read as "the model failed".

Usage:  python3 atom_count_outofsample.py [structures_dir]
"""
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from plddt_from_cif import parse  # noqa: E402

SITE = 200

# side-chain heavy atoms, and DEPTH = bonds from CB to the farthest side-chain atom.
# Both are counted from the residue's chemical graph, not from any fitted number.
SIDECHAIN = {
    "A": (1, 0), "C": (2, 1), "D": (4, 2), "E": (5, 3), "F": (7, 4),
    "G": (0, -1), "H": (6, 3), "I": (4, 2), "K": (5, 4), "L": (4, 2),
    "M": (4, 3), "N": (4, 2), "P": (3, 2), "Q": (5, 3), "R": (7, 4),
    "S": (2, 1), "T": (3, 1), "V": (3, 1), "W": (10, 4), "Y": (8, 5),
}

FLAT_THRESHOLD = 1.5           # from claim 518, fixed before the run
ATOM_CUTOFF = 4                # model under test: <= 4 heavy atoms => flat
DEPTH_CUTOFF = 2               # rival read: <= 2 bonds deep => flat

# These 13 are the fit. Everything else at this site is out of sample.
TRAINING = set("TAVINDEQKHFRW")
REGISTERED_OUT_OF_SAMPLE = set("ML")


def plddt_at(cif, site):
    per = parse(cif)
    if site not in per:
        raise SystemExit(f"{cif}: no residue {site}")
    return per[site][0], per[site][1]


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else
                Path(__file__).resolve().parent.parent /
                "results/fish-proteins/structures")

    # --- wild type, with its replicate spread -------------------------------
    wt = []
    for d in ("slc43a2a_wt", "slc43a2a_wt_seed1", "slc43a2a_wt_seed2", "slc43a2a_wt_seed3"):
        cifs = sorted((root / d).glob("*.cif"))
        if cifs:
            wt.append(plddt_at(cifs[0], SITE)[0])
    if len(wt) < 2:
        raise SystemExit("need at least two wild-type replicates to state a noise floor")
    wt_mean = sum(wt) / len(wt)
    wt_sd = statistics.stdev(wt)
    print(f"wild type at {SITE}: {len(wt)} replicates, mean {wt_mean:.2f}, sd {wt_sd:.4f}")
    print(f"replicate spread is the noise floor for a DROP at this site\n")

    # --- every mutant that has landed ---------------------------------------
    rows = []
    for d in sorted(root.glob(f"slc43a2a_t{SITE}*")):
        cifs = sorted(d.glob("*.cif"))
        if not cifs:
            continue
        val, aa = plddt_at(cifs[0], SITE)
        atoms, depth = SIDECHAIN[aa]
        rows.append((aa, atoms, depth, val, wt_mean - val))
    rows.sort(key=lambda r: r[4])

    print(f"{'aa':>3} {'atoms':>6} {'depth':>6} {'pLDDT':>7} {'drop':>7}  "
          f"{'set':<12} {'atom-model':<11} {'depth-model':<11} obs")
    atom_wrong = depth_wrong = 0
    for aa, atoms, depth, val, drop in rows:
        obs = "FLAT" if drop < FLAT_THRESHOLD else "DROP"
        a_pred = "flat" if atoms <= ATOM_CUTOFF else "drop"
        d_pred = "flat" if depth <= DEPTH_CUTOFF else "drop"
        which = ("training" if aa in TRAINING
                 else "OUT-OF-SAMP" if aa in REGISTERED_OUT_OF_SAMPLE else "extra")
        a_mark = "ok" if a_pred.upper() == obs else "** WRONG"
        d_mark = "ok" if d_pred.upper() == obs else "** WRONG"
        if a_pred.upper() != obs:
            atom_wrong += 1
        if d_pred.upper() != obs:
            depth_wrong += 1
        print(f"{aa:>3} {atoms:>6} {depth:>6} {val:>7.1f} {drop:>7.2f}  "
              f"{which:<12} {a_pred:<4}{a_mark:<7} {d_pred:<4}{d_mark:<7} {obs}")

    # --- POSITIVE CONTROL ---------------------------------------------------
    # If the parse broke and every drop came back ~0, every residue would read FLAT and the
    # atom model would look PERFECT rather than broken. So assert the training set still
    # separates: at least one residue must read DROP, and the biggest must exceed 5 pLDDT.
    drops = [r[4] for r in rows]
    assert max(drops) > 5.0, (
        f"CONTROL FAILED: largest drop is {max(drops):.2f}; the parse is probably broken, "
        "and a broken parse makes every model look right")
    assert any(r[4] < FLAT_THRESHOLD for r in rows), "CONTROL FAILED: nothing reads flat"
    print(f"\nCONTROL ok: largest drop {max(drops):.2f} > 5.0, and some residues read flat, "
          "so the parse is discriminating")

    # --- verdict ------------------------------------------------------------
    oos = [r for r in rows if r[0] in REGISTERED_OUT_OF_SAMPLE]
    print(f"\nregistered out-of-sample residues landed: "
          f"{', '.join(r[0] for r in oos) if oos else '(none yet)'}")
    for aa, atoms, depth, val, drop in oos:
        verdict = ("CONFIRMS the prediction" if drop < FLAT_THRESHOLD
                   else "FALSIFIES the prediction")
        print(f"  {aa}: {atoms} heavy atoms, predicted FLAT (<{FLAT_THRESHOLD}); "
              f"observed drop {drop:.2f} -> {verdict}")
        if drop >= FLAT_THRESHOLD:
            print(f"     that is {drop / FLAT_THRESHOLD:.1f}x the threshold and "
                  f"{drop / wt_sd:.0f}x the replicate sd -- but note the ABSOLUTE size is "
                  f"{drop:.2f} pLDDT on a 0-100 scale, which is modest; the threshold, "
                  "not the sigma, is what the prediction named")

    print(f"\natom-count model wrong on {atom_wrong} of {len(rows)} residues")
    print(f"depth-from-CB model wrong on {depth_wrong} of {len(rows)} residues")
    if depth_wrong == 0 and atom_wrong > 0:
        print("\nTHE DEPTH READ IS POST-HOC. It was found AFTER seeing the residue that broke")
        print("the atom-count model, so these rows do not test it -- that is the same error")
        print("claim 518 named in the atom model, one level up. It is a hypothesis, not a result.")
        undecided = [a for a in SIDECHAIN
                     if a not in TRAINING and a not in REGISTERED_OUT_OF_SAMPLE and a != "P"]
        disc = [a for a in undecided
                if (SIDECHAIN[a][0] <= ATOM_CUTOFF) != (SIDECHAIN[a][1] <= DEPTH_CUTOFF)]
        print(f"residues left at this site that would SEPARATE the two models: "
              f"{', '.join(sorted(disc)) if disc else 'NONE'}")
        if not disc:
            print("so no natural amino acid at this site can decide between them; the test has")
            print("to move to a different SITE, where the depth rule is a transfer and not a fit")
    return 0


if __name__ == "__main__":
    sys.exit(main())
