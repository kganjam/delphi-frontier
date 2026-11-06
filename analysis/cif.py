#!/usr/bin/env python3
"""Read an mmCIF atom table by its DECLARED column header, never by guessing.

WHY THIS EXISTS, measured twice on the same two files within one session.

The project holds two Kcnk5b predictions written by different programs, and their atom tables
have different column orders:

    kcnk5b_boltz2.cif    Cartn_x at 0-indexed field 10
    kcnk5b_esmfold2.cif  Cartn_x at 0-indexed field 15

ATTEMPT 1 hard-coded 13..16 for the ESMFold file and read `occupancy` and `B_iso_or_equiv` as
coordinates. It produced an 18.28% inter-region contact fraction -- a dramatic result that
would have supported the hypothesis under test. It was caught only because the coordinate
SPANS were printed: x and y both ran "1.0 to 1.0", which is an occupancy column, not a protein.

ATTEMPT 2 tried to be safe by DETECTING the columns: take the first run of three consecutive
float fields whose span exceeds 15 Angstrom. That picked field 12 for the ESMFold file --
`B_iso_or_equiv`, whose pLDDT values span 30..95 and so clear any such threshold. The contact
fraction came back 38.4% instead of 0.12%, a factor of 300, and this time it would have been
written into a correlation rather than a headline. The heuristic written to prevent the error
reproduced it.

The header is right there in the file. `_atom_site.*` loop tags are declared in order, so the
column index is a lookup, not an inference. Anything else is guessing with extra steps.
"""
from __future__ import annotations

import pathlib


class CifError(ValueError):
    pass


def atom_columns(text: str) -> dict[str, int]:
    """Map each `_atom_site.<name>` tag to its 0-indexed column in the ATOM/HETATM rows."""
    cols: dict[str, int] = {}
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("_atom_site."):
            cols[s.split(".", 1)[1].split()[0]] = len(cols)
        elif cols and (s.startswith("ATOM") or s.startswith("HETATM")):
            break
    for need in ("Cartn_x", "Cartn_y", "Cartn_z", "label_atom_id", "label_comp_id"):
        if need not in cols:
            raise CifError(f"no _atom_site.{need} in the header; got {sorted(cols)}")
    return cols


def ca_atoms(path: str | pathlib.Path) -> list[dict]:
    """Every CA atom as {chain, resi, resn, x, y, z}, read through the declared header."""
    text = pathlib.Path(path).read_text()
    c = atom_columns(text)
    chain = c.get("auth_asym_id", c.get("label_asym_id"))
    resi = c.get("auth_seq_id", c.get("label_seq_id"))
    out = []
    for line in text.splitlines():
        if not (line.startswith("ATOM") or line.startswith("HETATM")):
            continue
        f = line.split()
        if len(f) <= max(c.values()) or f[c["label_atom_id"]] != "CA":
            continue
        out.append({"chain": f[chain], "resi": f[resi], "resn": f[c["label_comp_id"]],
                    "x": float(f[c["Cartn_x"]]), "y": float(f[c["Cartn_y"]]),
                    "z": float(f[c["Cartn_z"]])})
    if not out:
        raise CifError(f"{path}: no CA atoms")
    return out


def span(atoms: list[dict]) -> tuple[float, float, float]:
    return tuple(max(a[k] for a in atoms) - min(a[k] for a in atoms) for k in "xyz")


def check_protein_like(atoms: list[dict], path: str = "") -> None:
    """Refuse an obviously non-coordinate column. A real protein is tens of Angstrom across;
    an occupancy column has span 0 and a pLDDT column is positive-only and under ~100."""
    sx, sy, sz = span(atoms)
    if min(sx, sy, sz) < 5.0:
        raise CifError(f"{path}: coordinate span {sx:.1f}/{sy:.1f}/{sz:.1f} A is too small to "
                       f"be a protein -- this is almost certainly an occupancy or B-factor column")
    if all(a[k] >= 0 for a in atoms for k in "xyz"):
        raise CifError(f"{path}: every x/y/z is non-negative, which a centred structure is not -- "
                       f"suspect a B-factor/pLDDT column")


def all_atoms(path: str | pathlib.Path) -> list[dict]:
    """Every ATOM record, read through the declared header (not just CA)."""
    text = pathlib.Path(path).read_text()
    c = atom_columns(text)
    chain = c.get("auth_asym_id", c.get("label_asym_id"))
    resi = c.get("auth_seq_id", c.get("label_seq_id"))
    elem = c.get("type_symbol")
    out = []
    for line in text.splitlines():
        if not line.startswith("ATOM"):
            continue
        f = line.split()
        if len(f) <= max(c.values()):
            continue
        out.append({"name": f[c["label_atom_id"]], "resn": f[c["label_comp_id"]],
                    "chain": f[chain], "resi": int(f[resi]),
                    "x": float(f[c["Cartn_x"]]), "y": float(f[c["Cartn_y"]]),
                    "z": float(f[c["Cartn_z"]]),
                    "b": float(f[c["B_iso_or_equiv"]]) if "B_iso_or_equiv" in c else 0.0,
                    "elem": f[elem] if elem is not None else ""})
    if not out:
        raise CifError(f"{path}: no ATOM records")
    return out


def to_pdb(src: str | pathlib.Path, dst: str | pathlib.Path) -> int:
    """Write an mmCIF's atoms as a PDB file. Returns the atom count.

    PDB is COLUMN-FIXED, not whitespace-separated, and the two traps are the atom-name field
    and the chain id. A one-character element is right-justified into columns 13-14 so the
    name begins at column 14; writing it at 13 makes `CA` (alpha carbon) read as `CA` the
    calcium ion to anything that parses by column. And the chain id is a SINGLE character, so
    an mmCIF label longer than one character has to be mapped rather than truncated silently.
    """
    atoms = all_atoms(src)
    check_protein_like([a for a in atoms if a["name"] == "CA"], str(src))
    chains = sorted({a["chain"] for a in atoms})
    if len(chains) > 62:
        raise CifError(f"{src}: {len(chains)} chains, more than PDB single-character ids allow")
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    cmap = {c: (c if len(c) == 1 else alphabet[i]) for i, c in enumerate(chains)}
    lines = []
    for i, a in enumerate(atoms, start=1):
        nm = a["name"]
        el = (a["elem"] or nm[0]).strip()
        name = f" {nm:<3}" if len(el) == 1 and len(nm) < 4 else f"{nm:<4}"
        lines.append(
            f"ATOM  {i:>5} {name}{'':1}{a['resn']:>3} {cmap[a['chain']]:1}{a['resi']:>4}    "
            f"{a['x']:>8.3f}{a['y']:>8.3f}{a['z']:>8.3f}{1.00:>6.2f}{a['b']:>6.2f}"
            f"{'':10}{el:>2}")
    lines.append("END")
    pathlib.Path(dst).write_text("\n".join(lines) + "\n")
    return len(atoms)
