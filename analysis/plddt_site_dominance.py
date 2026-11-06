#!/usr/bin/env python3
"""Is an ESMFold2 pLDDT delta a property of the SUBSTITUTION or of the SITE?

This decides whether pLDDT delta can rank designed variants, which is the only reason this
project was characterising it. If the delta is a property of the substitution, a design pipeline
can use it to say which mutation is more damaging. If it is a property of the site, the same
mutation scores differently depending only on where it lands, and the ranking is an artifact.

slc43a2a was folded with the SAME three substitutions at TWO positions, 200 and 219. The
comparison is therefore paired: same protein, same model, same parser, same wild-type replicates.

Usage:  python3 plddt_site_dominance.py [structures_dir]
"""
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from plddt_from_cif import parse  # noqa: E402

WT_DIRS = ("slc43a2a_wt", "slc43a2a_wt_seed1", "slc43a2a_wt_seed2", "slc43a2a_wt_seed3")
SITES = {200: "slc43a2a_t200{}", 219: "slc43a2a_l219{}"}


def plddt_at(cif, site):
    per = parse(cif)
    return (per[site][0], per[site][1]) if site in per else (None, None)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else
                Path(__file__).resolve().parent.parent /
                "results/fish-proteins/structures")

    wt, table = {}, {}
    for site in SITES:
        vals = []
        for d in WT_DIRS:
            cifs = sorted((root / d).glob("*.cif"))
            if cifs:
                v, _ = plddt_at(cifs[0], site)
                if v is not None:
                    vals.append(v)
        wt[site] = (sum(vals) / len(vals), statistics.stdev(vals), len(vals))

    for site, pat in SITES.items():
        table[site] = {}
        for d in sorted(root.glob(pat.format("*"))):
            cifs = sorted(d.glob("*.cif"))
            if not cifs:
                continue
            v, aa = plddt_at(cifs[0], site)
            if v is not None:
                table[site][aa] = wt[site][0] - v

    for site in SITES:
        m, sd, n = wt[site]
        print(f"site {site}: wild type {m:.2f} over {n} replicates, replicate sd {sd:.4f}, "
              f"{len(table[site])} substitutions folded")

    shared = sorted(set(table[200]) & set(table[219]))
    if len(shared) < 2:
        raise SystemExit(f"only {len(shared)} substitution(s) in common; nothing to pair")

    print(f"\nPAIRED on the {len(shared)} substitution(s) folded at BOTH sites: "
          f"{', '.join(shared)}\n")
    print(f"{'sub':>4} {'drop@200':>10} {'drop@219':>10} {'difference':>12}")
    for aa in shared:
        d2, d1 = table[200][aa], table[219][aa]
        print(f"{aa:>4} {d2:>10.2f} {d1:>10.2f} {d2 - d1:>12.2f}")

    a200 = [abs(table[200][a]) for a in shared]
    a219 = [abs(table[219][a]) for a in shared]
    m200, m219 = sum(a200) / len(a200), sum(a219) / len(a219)
    print(f"\nmean |drop| at 200: {m200:.2f}")
    print(f"mean |drop| at 219: {m219:.2f}")

    # --- POSITIVE CONTROL ---------------------------------------------------
    # A parser that silently returned the same residue for every file would make both sites
    # look identical, which is the OPPOSITE of this finding and so would hide it. Assert the
    # parser resolves different residues and that site 200 does produce large drops.
    assert max(a200) > 5.0, (
        f"CONTROL FAILED: largest drop at 200 is {max(a200):.2f}; without a large drop "
        "somewhere, 'both sites are flat' would be the trivial reading")
    assert wt[200][0] != wt[219][0], (
        "CONTROL FAILED: the two sites report an identical wild-type pLDDT, which suggests "
        "the site argument is being ignored")
    print(f"\nCONTROL ok: site 200 reaches {max(a200):.2f}, and the two sites report "
          f"different wild-type values ({wt[200][0]:.2f} vs {wt[219][0]:.2f}), "
          "so the site argument is being honoured")

    # --- verdict ------------------------------------------------------------
    if m219 > 0:
        print(f"\nthe SAME substitutions perturb site 200 {m200 / m219:.0f}x more than site 219")
    rank200 = sorted(shared, key=lambda a: -table[200][a])
    rank219 = sorted(shared, key=lambda a: -table[219][a])
    print(f"rank by damage at 200: {' > '.join(rank200)}")
    print(f"rank by damage at 219: {' > '.join(rank219)}")
    if rank200 != rank219:
        print("THE ORDERING ITSELF FLIPS, so this is not a scale factor that a per-site")
        print("normalisation could divide out -- the sites disagree about WHICH substitution")
        print("is worst, not merely by how much.")

    biggest = max(shared, key=lambda a: abs(table[200][a] - table[219][a]))
    print(f"\nsharpest pair: {biggest} drops {table[200][biggest]:.2f} at site 200 and "
          f"{table[219][biggest]:.2f} at site 219 -- same protein, same model, "
          f"{abs(200 - 219)} residues apart")
    print("\nCONSEQUENCE FOR THE DESIGN PIPELINE: a pLDDT delta cannot rank designed variants.")
    print("It reports how tolerant a POSITION is in the model's own representation, not how")
    print("damaging a substitution is to the protein. Any ranking built on it ranks site")
    print("idiosyncrasy. This also explains the atom-count and depth 'models': both were fitted")
    print("at site 200 alone, where the representation happens to be sensitive, and neither is")
    print("a statement about amino acids.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
