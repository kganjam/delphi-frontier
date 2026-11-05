#!/usr/bin/env python3
"""Convert an ESMFold2/OpenFold mmCIF to PDB, for tools that only accept ATOM records.

THE HEADER MUST BE READ, NOT ASSUMED -- the same warning `plddt_from_cif.py` carries, for the same
writer. This file orders B_iso_or_equiv at field 12 and occupancy at 13, the reverse of the usual
PDB-derived order, and every occupancy is exactly 1.0. A positional parse written against a
standard mmCIF therefore produces a structurally valid PDB whose B-factors are all 1.00 and whose
occupancies are the pLDDT values, and nothing downstream complains.

    python3 cif_to_pdb.py in.cif out.pdb
"""
from __future__ import annotations

import sys

AA3 = {"ALA", "ARG", "ASN", "ASP", "CYS", "GLN", "GLU", "GLY", "HIS", "ILE", "LEU", "LYS",
       "MET", "PHE", "PRO", "SER", "THR", "TRP", "TYR", "VAL"}


def read_cif(path: str) -> tuple[list[str], list[list[str]]]:
    cols, rows, inloop = [], [], False
    for line in open(path):
        s = line.strip()
        if s.startswith("_atom_site."):
            cols.append(s.split(".", 1)[1].strip())
            inloop = True
            continue
        if inloop:
            if s.startswith(("ATOM", "HETATM")):
                rows.append(s.split())
            elif s.startswith("#") and rows:
                break
    if not cols or not rows:
        raise SystemExit(f"{path}: no _atom_site loop found")
    return cols, rows


def to_pdb(path: str) -> str:
    cols, rows = read_cif(path)
    i = {name: cols.index(name) for name in
         ("group_PDB", "type_symbol", "label_atom_id", "label_comp_id", "label_asym_id",
          "label_seq_id", "Cartn_x", "Cartn_y", "Cartn_z", "B_iso_or_equiv")}
    # `occupancy` is OPTIONAL. ESMFold2's writer emits it; OpenFold3's does not, and a required
    # lookup turned a perfectly readable dimer into ValueError: 'occupancy' is not in list.
    # Where it is absent every atom is fully occupied by construction -- these are predictions,
    # not crystallographic refinements with partial occupancy -- so 1.00 is the right default
    # rather than a guess.
    i_occ = i.get("occupancy")
    out = []
    for n, r in enumerate(rows, 1):
        name, elem = r[i["label_atom_id"]], r[i["type_symbol"]]
        # PDB atom-name justification: a one-letter element starts in column 14, not 13.
        an = f" {name:<3s}" if len(name) < 4 and len(elem) == 1 else f"{name:<4s}"
        out.append(
            f"{'ATOM  ' if r[i['group_PDB']] == 'ATOM' else 'HETATM'}"
            f"{n:5d} {an}{'':1s}{r[i['label_comp_id']]:>3s} {r[i['label_asym_id']][:1]:1s}"
            f"{int(r[i['label_seq_id']]):4d}{'':1s}   "
            f"{float(r[i['Cartn_x']]):8.3f}{float(r[i['Cartn_y']]):8.3f}{float(r[i['Cartn_z']]):8.3f}"
            f"{(float(r[i_occ]) if i_occ is not None else 1.0):6.2f}"
            f"{float(r[i['B_iso_or_equiv']]):6.2f}"
            f"{'':10s}{elem:>2s}")
    out.append("TER")
    out.append("END")
    return "\n".join(out) + "\n"


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    src, dst = sys.argv[1], sys.argv[2]
    text = to_pdb(src)
    with open(dst, "w") as f:
        f.write(text)

    # CONTROL: read the PDB back and require that it reproduces the mmCIF's own residue sequence
    # and atom count. A converter that drops a chain or mangles a column still writes a file.
    cols, rows = read_cif(src)
    ic = {n: cols.index(n) for n in ("label_atom_id", "label_comp_id", "label_seq_id")}
    want = {int(r[ic["label_seq_id"]]): r[ic["label_comp_id"]]
            for r in rows if r[ic["label_atom_id"]] == "CA"}
    got = {}
    for line in text.splitlines():
        if line.startswith("ATOM") and line[12:16].strip() == "CA":
            got[int(line[22:26])] = line[17:20].strip()
    n_atoms = sum(1 for line in text.splitlines() if line.startswith(("ATOM", "HETATM")))
    ok = (want == got) and n_atoms == len(rows)
    print(f"  {src} -> {dst}")
    print(f"  atoms {n_atoms} (mmCIF {len(rows)}), CA residues {len(got)} (mmCIF {len(want)})")
    print(f"  CONTROL round-trip residue identity: {'MATCH' if want == got else '*** MISMATCH ***'}")
    nonstd = {v for v in got.values()} - AA3
    if nonstd:
        print(f"  non-standard residues present: {sorted(nonstd)}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
