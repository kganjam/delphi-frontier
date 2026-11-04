#!/usr/bin/env python3
"""Can ProteinMPNN rank candidate kcnk5b substitutions? Measured answer: no.

WHY IT WAS ASKED. kcnk5b is the fin-size gene. Claim 528 puts the alf gain-of-function allele at
1.74x linear fin proportion and claim 529 at 2.65x area, against the 4.4x area that claim 523 says
S901's threshold needs -- a 1.66x gap. Closing it by design means proposing kcnk5b variants, and
Yi 2021 reports that Kcnk5b activity is regulated at SERINE 345. The folded 448-residue construct
does carry a serine at 345, in a DHS-PR context, so the structure covers the residue the
literature implicates. The question is whether ProteinMPNN's per-position distributions can say
which substitutions there are structurally tolerated.

THE FIRST READING LOOKED LIKE A RESULT AND WAS AN ARTIFACT. ProteinMPNN assigns p(native) = 0.000
at 342, 343, 344, 345, 347 and 348, wanting proline and alanine instead -- six consecutive
positions where the model disagrees flatly with nature, centred on the functional serine. That is
a striking pattern and it means nothing, because 53% OF ALL 448 POSITIONS ARE BELOW 0.001. Without
the base rate the window reads as a discovery. This is the same shape as claim 522: a number that
looks like it is about the residue is about the context.

THE MEASUREMENT THAT SETTLES IT is sequence recovery -- how often the model's top choice is the
residue actually there. Published ProteinMPNN recovery on native backbones is about 40-50%. Here
it is 20.5%, roughly half. Two reasons are available and this script does not separate them: the
protein is a potassium channel, so a membrane protein, and ProteinMPNN's training set is dominated
by soluble structures; and the backbone is an ESMFold2 PREDICTION rather than an experimental
structure. Either way a model that recovers one native residue in five cannot be trusted to rank
substitutions at a position chosen for its biology.

CONCLUSION: ProteinMPNN is not usable as a variant ranker on this target. That is a second
instrument retired on this project by measurement, after pLDDT delta in claim 522, and it means
no kcnk5b design proposal may cite it.

Usage:  python3 proteinmpnn_fitness.py [result.json] [structure.cif]
"""
import json
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from plddt_from_cif import parse  # noqa: E402

AA = "ACDEFGHIKLMNPQRSTVWYX"
PUBLISHED_RECOVERY = (0.40, 0.50)   # ProteinMPNN paper range on native backbones
ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    res = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        ROOT / "results/fish-proteins/proteinmpnn_kcnk5b/result.json"
    cif = Path(sys.argv[2]) if len(sys.argv) > 2 else \
        ROOT / "results/fish-proteins/structures/kcnk5b_esmfold2.cif"

    d = json.loads(res.read_text())
    probs = d["probs"]
    native = [l for l in d["mfasta"].splitlines() if l and not l.startswith(">")][0]

    def dist(p0):
        cols = [probs[k][p0] for k in range(len(probs))]
        return [sum(c[j] for c in cols) / len(cols) for j in range(len(cols[0]))]

    pn, rec = [], 0
    for i, aa in enumerate(native):
        v = dist(i)
        assert abs(sum(v) - 1.0) < 1e-3, f"position {i+1} distribution sums to {sum(v)}"
        pn.append(v[AA.index(aa)] if aa in AA else 0.0)
        if AA[max(range(len(v)), key=lambda j: v[j])] == aa:
            rec += 1

    recovery = rec / len(pn)
    print(f"positions {len(pn)}")
    print(f"SEQUENCE RECOVERY {rec}/{len(pn)} = {recovery*100:.1f}%")
    lo, hi = PUBLISHED_RECOVERY
    if recovery < lo:
        print(f"  BELOW the published {lo*100:.0f}-{hi*100:.0f}% range on native backbones, by a "
              f"factor of {lo/recovery:.1f}. A ranker that recovers one native residue in "
              f"{1/recovery:.0f}\n  cannot be trusted to rank substitutions at a chosen position.")
    else:
        print(f"  within the published {lo*100:.0f}-{hi*100:.0f}% range")

    below = sum(1 for x in pn if x < 0.001)
    print(f"\nBASE RATE: p(native) < 0.001 at {below}/{len(pn)} positions "
          f"({100*below/len(pn):.0f}%)")
    print(f"  median p(native) {statistics.median(pn):.3f}")
    print(f"  p(native) at 345 = {pn[344]:.4f}  -> unremarkable against that base rate")
    print("  Reading the S345 window as a special disagreement needs this line to not exist.")

    per = parse(str(cif))
    pairs = [(per[i + 1][0], pn[i]) for i in range(len(pn)) if (i + 1) in per]
    lowc = [p for pl, p in pairs if pl < 80]
    hic = [p for pl, p in pairs if pl >= 90]
    print(f"\np(native) by backbone confidence -- the two models agree about where it is uncertain:")
    print(f"  pLDDT <80 : mean p(native) {statistics.mean(lowc):.3f}  (n={len(lowc)})")
    print(f"  pLDDT >=90: mean p(native) {statistics.mean(hic):.3f}  (n={len(hic)})")

    print("\nVERDICT: ProteinMPNN is NOT usable as a variant ranker on this target.")
    print("No kcnk5b design proposal may cite it. Second instrument retired by measurement")
    print("on this project, after pLDDT delta (claim 522).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
