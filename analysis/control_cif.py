#!/usr/bin/env python3
"""Controls for analysis/cif.py. Both historical misreads are must-flag arms."""
from __future__ import annotations

import os
import pathlib
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cif import CifError, atom_columns, ca_atoms, check_protein_like, span  # noqa: E402

D = pathlib.Path(os.path.dirname(os.path.abspath(__file__))) / ".." / "results" / "fish-proteins" / "structures"
FILES = {"kcnk5b_boltz2.cif": 10, "kcnk5b_esmfold2.cif": 15}


def arms():
    out = []
    for name, want_x in FILES.items():
        p = D / name
        cols = atom_columns(p.read_text())
        out.append((f"{name}: Cartn_x column read from the header is {want_x}",
                    cols["Cartn_x"] == want_x, f"got {cols['Cartn_x']}"))
        ats = ca_atoms(p)
        out.append((f"{name}: 448 CA atoms", len(ats) == 448, f"got {len(ats)}"))
        sx, sy, sz = span(ats)
        out.append((f"{name}: coordinate span is protein-sized", min(sx, sy, sz) > 30,
                    f"{sx:.1f} / {sy:.1f} / {sz:.1f} A"))

    # The two files order their columns DIFFERENTLY. If they ever agreed, a hard-coded index
    # would work and this module would be pointless -- so assert the disagreement.
    xs = {n: atom_columns((D / n).read_text())["Cartn_x"] for n in FILES}
    out.append(("the two files really do put Cartn_x in different columns",
                len(set(xs.values())) == 2, str(xs)))

    # MUST FLAG 1: attempt 1's columns (occupancy / label_entity_id) on the ESMFold file.
    text = (D / "kcnk5b_esmfold2.cif").read_text()
    rows = [ln.split() for ln in text.splitlines() if ln.startswith("ATOM")]
    ats = [{"x": float(r[13]), "y": float(r[14]), "z": float(r[15])}
           for r in rows if r[2] == "CA"]
    try:
        check_protein_like(ats, "attempt-1 columns 13/14/15")
        ok, why = False, "check_protein_like ACCEPTED the occupancy columns"
    except CifError as e:
        ok, why = True, str(e)[:90]
    out.append(("MUST FLAG attempt 1 (occupancy columns) is refused", ok, why))

    # MUST FLAG 2: attempt 2's detected column 12 = B_iso_or_equiv (pLDDT).
    ats = [{"x": float(r[12]), "y": float(r[13]), "z": float(r[14])}
           for r in rows if r[2] == "CA"]
    try:
        check_protein_like(ats, "attempt-2 column 12")
        ok, why = False, "check_protein_like ACCEPTED the B-factor column"
    except CifError as e:
        ok, why = True, str(e)[:90]
    out.append(("MUST FLAG attempt 2 (B_iso/pLDDT column) is refused", ok, why))

    # MUST NOT FLAG: the correct columns pass the same guard, for both files.
    for name in FILES:
        try:
            check_protein_like(ca_atoms(D / name), name)
            ok, why = True, "accepted"
        except CifError as e:
            ok, why = False, str(e)[:90]
        out.append((f"must not flag: {name} read correctly is accepted", ok, why))
    return out


def main() -> int:
    bad = 0
    for name, ok, detail in arms() + pdb_arms():
        print(f"  [{'ok' if ok else 'FAIL'}] {name}\n           {detail}")
        bad += not ok
    print(f"  -> controls {'PASS' if not bad else f'FAIL ({bad})'}")
    return 1 if bad else 0




def pdb_arms():
    """Round-trip control: the PDB must carry the same CA coordinates as the mmCIF."""
    import tempfile
    from cif import all_atoms, to_pdb
    out = []
    src = D / "kcnk5b-homodimer-msa" / "model.cif"
    if not src.exists():
        return [("pdb round trip: source absent", False, str(src))]
    with tempfile.TemporaryDirectory() as td:
        dst = pathlib.Path(td) / "m.pdb"
        n = to_pdb(src, dst)
        text = dst.read_text()
        # re-read the PDB BY COLUMN, which is how a real parser reads it
        got = []
        for ln in text.splitlines():
            if ln.startswith("ATOM") and ln[12:16].strip() == "CA":
                got.append((ln[21], int(ln[22:26]),
                            float(ln[30:38]), float(ln[38:46]), float(ln[46:54])))
        want = [(a["chain"], a["resi"], a["x"], a["y"], a["z"])
                for a in all_atoms(src) if a["name"] == "CA"]
        out.append((f"pdb has the same CA count as the cif ({len(want)})",
                    len(got) == len(want), f"pdb {len(got)} vs cif {len(want)}"))
        worst = max((max(abs(g[i] - w[i]) for i in (2, 3, 4))
                     for g, w in zip(got, want)), default=9.9)
        out.append(("CA coordinates survive the round trip to 0.001 A",
                    worst <= 0.0011, f"worst {worst:.4f} A"))
        out.append((f"both chains present and single-character ({len(set(g[0] for g in got))})",
                    len({g[0] for g in got}) == 2, str(sorted({g[0] for g in got}))))
        # MUST FLAG: a CA written one column left reads as calcium to a column parser
        out.append(("the atom name is column-correct: 'CA' at 13-16 reads as ' CA '",
                    any(ln[12:16] == " CA " for ln in text.splitlines()
                        if ln.startswith("ATOM")),
                    "found ' CA '" if any(ln[12:16] == " CA " for ln in text.splitlines()
                                          if ln.startswith("ATOM")) else "MISPLACED"))
        out.append(("atom count is nonzero and matches the writer's return",
                    n == len(all_atoms(src)), f"{n}"))
    return out


if __name__ == "__main__":
    raise SystemExit(main())
