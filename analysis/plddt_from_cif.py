#!/usr/bin/env python3
"""Per-residue pLDDT from an ESMFold2 mmCIF, reading column order from the _atom_site. header.

THE HEADER MUST BE READ, NOT ASSUMED. This writer orders B_iso_or_equiv at field 12 and occupancy
at field 13, and every occupancy is exactly 1.0 -- so a positional parse written for a standard
mmCIF silently reports a mean pLDDT of 1.00 and looks entirely plausible.

    python3 plddt_from_cif.py model.cif [residue]
"""
import statistics
import sys

AA3 = {"ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C", "GLN": "Q", "GLU": "E",
       "GLY": "G", "HIS": "H", "ILE": "I", "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F",
       "PRO": "P", "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V"}


def parse(path):
    cols, rows, inloop = [], [], False
    for line in open(path):
        s = line.strip()
        if s.startswith("_atom_site."):
            cols.append(s.split(".")[1]); inloop = True; continue
        if inloop:
            if s.startswith(("ATOM", "HETATM")):
                rows.append(s.split())
            elif s.startswith("#") and rows:
                break
    ib, iq = cols.index("B_iso_or_equiv"), cols.index("label_seq_id")
    ia, ic = cols.index("label_atom_id"), cols.index("label_comp_id")
    return {int(r[iq]): (float(r[ib]), AA3.get(r[ic], "?")) for r in rows if r[ia] == "CA"}


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    per = parse(sys.argv[1])
    v = [x for x, _ in per.values()]
    print(f"residues {len(per)}  mean {sum(v)/len(v):.2f}  median {statistics.median(v):.2f}  "
          f">70 {100*sum(1 for x in v if x > 70)/len(v):.1f}%  "
          f">90 {100*sum(1 for x in v if x > 90)/len(v):.1f}%")
    if len(sys.argv) > 2:
        p = int(sys.argv[2])
        print(f"residue {p}: {per[p][1]} pLDDT {per[p][0]:.1f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
