#!/usr/bin/env python3
"""Does Kcnk5b's C-terminus contact the PARTNER subunit? Measured under a confidence filter.

Claim 1039 established that the project's two monomer predictions cannot address this, because
the functional channel homodimerises (UniProt O95279, experimental) and a monomer forbids the
trans arrangement. Claim 1042 ran the dimer and REFUSED to read it: with no supplied alignment
nothing in it reached pLDDT 70. This reads the alignment-supplied run.

THE FILTER IS THE WHOLE POINT. With no confidence filter, 79 of 208 C-terminal residues appear
to contact the partner. Restricted to residues the model places confidently, 8 of 208 qualify
and 0 of those contact anything. The unfiltered number is noise from residues at pLDDT below
50, and reporting it would have inverted the conclusion.
"""
from __future__ import annotations

import collections
import json
import os
import pathlib
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cif import atom_columns  # noqa: E402

D = pathlib.Path(os.path.dirname(os.path.abspath(__file__))) / ".." / "results" / "fish-proteins" / "structures"
RUNS = (("dimer   no-MSA", "kcnk5b-homodimer-full"),
        ("monomer no-MSA", "kcnk5b-monomer-of3"),
        ("dimer   +MSA", "kcnk5b-homodimer-msa"))
BOUNDARY = 240          # the truncation cut: F241 opens the region Daane 2018 says is removed
CUT = 10.0              # CA-CA contact distance, Angstrom


def load(sub: str):
    d = json.loads((D / sub / "result.json").read_text())
    s = d["outputs"][0]["structures_with_scores"][0]
    p = D / sub / "model.cif"
    if not p.exists():
        p.write_text(s["structure"])
    c = atom_columns(p.read_text())
    ch = c.get("auth_asym_id", c["label_asym_id"])
    ri = c.get("auth_seq_id", c["label_seq_id"])
    ats = [{"ch": r[ch], "resi": int(r[ri]), "pl": float(r[c["B_iso_or_equiv"]]),
            "x": float(r[c["Cartn_x"]]), "y": float(r[c["Cartn_y"]]), "z": float(r[c["Cartn_z"]])}
           for r in (ln.split() for ln in p.read_text().splitlines() if ln.startswith("ATOM"))
           if r[c["label_atom_id"]] == "CA"]
    return s, ats


def main() -> int:
    print(f"  {'run':18}{'cplDDT':>8}{'iPTM':>8}{'pTM':>8}{'>70':>8}{'pore':>8}{'tail':>8}")
    for lbl, sub in RUNS:
        if not (D / sub / "result.json").exists():
            print(f"  {lbl:18}  (absent)")
            continue
        s, ats = load(sub)
        pl = [a["pl"] for a in ats]
        pore = [a["pl"] for a in ats if a["resi"] <= BOUNDARY]
        tail = [a["pl"] for a in ats if a["resi"] > BOUNDARY]
        print(f"  {lbl:18}{s['complex_plddt_score']:8.2f}{s['iptm_score']:8.3f}{s['ptm_score']:8.3f}"
              f"{100*sum(1 for x in pl if x > 70)/len(pl):7.1f}%{sum(pore)/len(pore):8.1f}"
              f"{sum(tail)/len(tail):8.1f}")

    s, ats = load("kcnk5b-homodimer-msa")
    A = [a for a in ats if a["ch"] == "A"]
    B = [a for a in ats if a["ch"] == "B"]
    print(f"\n  INTER-SUBUNIT CONTACTS, chain A -> chain B, CA-CA within {CUT:.0f} A")
    print(f"  {'pLDDT filter':>13}{'A kept':>9}{'pore pairs':>12}{'tail pairs':>12}"
          f"{'tail res w/ contact':>22}")
    for cut in (0, 50, 70):
        Af = [a for a in A if a["pl"] >= cut]
        Bf = [b for b in B if b["pl"] >= cut]
        n = collections.Counter()
        for a in Af:
            reg = "pore" if a["resi"] <= BOUNDARY else "tail"
            for b in Bf:
                if (a["x"]-b["x"])**2 + (a["y"]-b["y"])**2 + (a["z"]-b["z"])**2 <= CUT*CUT:
                    n[reg] += 1
        hits = sum(1 for a in Af if a["resi"] > BOUNDARY and any(
            (a["x"]-b["x"])**2 + (a["y"]-b["y"])**2 + (a["z"]-b["z"])**2 <= CUT*CUT for b in Bf))
        nt = sum(1 for a in Af if a["resi"] > BOUNDARY)
        print(f"  {'>= ' + str(cut):>13}{len(Af):>9}{n['pore']:>12}{n['tail']:>12}"
              f"{f'{hits} of {nt}':>22}")

    Af = [a for a in A if a["pl"] >= 70]
    Bf = [b for b in B if b["pl"] >= 70]
    iface = sorted({a["resi"] for a in Af for b in Bf
                    if (a["x"]-b["x"])**2 + (a["y"]-b["y"])**2 + (a["z"]-b["z"])**2 <= CUT*CUT})
    runs, st, pv = [], iface[0], iface[0]
    for x in iface[1:]:
        if x != pv + 1:
            runs.append((st, pv))
            st = x
        pv = x
    runs.append((st, pv))
    print(f"\n  CONFIDENT INTERFACE (pLDDT>=70): {len(iface)} chain-A residues at "
          + ", ".join(f"{a}-{b}" if a != b else str(a) for a, b in runs))
    print("  A K2P subunit has TWO pore domains, each with a selectivity filter, and the family's")
    print("  dimerisation element is the extracellular cap between M1 and P1. The filters in this")
    print("  sequence are GYG at 100-102 and GFG at 205-207; the interface stretches flank them.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
