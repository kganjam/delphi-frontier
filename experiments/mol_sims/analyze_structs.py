"""Unpack Boltz-2 results and score them (claude-mol, 2026-11-01). COMPUTED from predictions; nothing observed.

For each target in results/mol-sims/claude-20261101/structures/<target>/: dedupe the delivered JSON artifacts by
content, write model_<i>.cif, and report per-chain pLDDT (mmCIF B-factor column), pTM/confidence, inter-chain
contacts (heavy atoms < 5 A) and interface pLDDT, plus the OpenFold2 (dummy MSA) pLDDT on the same residues.
Usage: python analyze_structs.py   -> structures/summary.json
"""
import hashlib, json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SD = ROOT / "results/mol-sims/claude-20261101/structures"
OF2 = ROOT / "results/bioservices/claude-20261101/openfold2"
KCNJ13_OF2 = "/data/worktrees/delphi-frontier/codex-demo/artifacts/bio-services/kcnj13_openfold2/rank1.pdb"  # recorded gap, sha 3200f588...
OF2_MAP = {("shhN", "A"): ("shha_Q92008_rank1.pdb", 23), ("fgf_complex", "A"): ("fgf10a_Q8AY90_rank1.pdb", 57),
           ("kcnk5b_dimer_openfold3", "A"): ("kcnk5b_Q6PFU3_rank1.pdb", 0), ("kcnk5b_dimer_openfold3", "B"): ("kcnk5b_Q6PFU3_rank1.pdb", 0),
           ("fgf_vs_fgfr2c_negctrl", "A"): ("fgf10a_Q8AY90_rank1.pdb", 57), ("kcnj13", "A"): (KCNJ13_OF2, 0),
           **{("kcnj13_tetramer_openfold3", c): (KCNJ13_OF2, 0) for c in "ABCD"}}


def parse_cif(txt):
    cols, atoms = [], []
    for l in txt.splitlines():
        if l.startswith("_atom_site."):
            cols.append(l.split(".", 1)[1].strip())
        elif l.startswith("ATOM") or l.startswith("HETATM"):
            f = l.split()
            atoms.append(dict(zip(cols, f)))
    return atoms


def of2_plddt(fn):
    return np.array([float(l[60:66]) for l in (Path(fn) if fn.startswith("/") else OF2 / fn).read_text().splitlines() if l.startswith("ATOM") and l[12:16].strip() == "CA"])


def analyze(target):
    d = SD / target
    seen, models = {}, []
    for a in sorted(d.glob("artifact_*")):
        j = json.loads(a.read_text())
        key = hashlib.sha256(json.dumps(j, sort_keys=True).encode()).hexdigest()
        seen.setdefault(key, (a.name, j))
    (src_name, j), = list(seen.values())[:1]
    if "outputs" in j:   # OpenFold3 layout -> Boltz-like
        sw = j["outputs"][0]["structures_with_scores"]
        j = {"structures": [{"structure": x["structure"]} for x in sw], "confidence_scores": [x["confidence_score"] for x in sw],
             "ptm_scores": [x["ptm_score"] for x in sw], "iptm_scores": [x.get("iptm_score") for x in sw],
             "complex_plddt": [x.get("complex_plddt_score") for x in sw]}
    out = {"iptm_scores": j.get("iptm_scores"), "complex_plddt": j.get("complex_plddt"),"target": target, "artifact_used": src_name, "distinct_artifact_contents": len(seen),
           "confidence_scores": j.get("confidence_scores"), "ptm_scores": j.get("ptm_scores"), "models": []}
    for i, s in enumerate(j["structures"]):
        cif = s["structure"]
        (d / f"model_{i}.cif").write_text(cif)
        at = parse_cif(cif)
        ca = [a for a in at if a["label_atom_id"] == "CA"]
        chains = sorted({a["label_asym_id"] for a in ca})
        m = {"model": i, "cif_sha256": hashlib.sha256(cif.encode()).hexdigest(), "chains": {}}
        for c in chains:
            pl = np.array([float(a["B_iso_or_equiv"]) for a in ca if a["label_asym_id"] == c])
            cm = {"n": int(len(pl)), "mean_plddt": float(pl.mean()), "frac_ge70": float((pl >= 70).mean()), "frac_ge90": float((pl >= 90).mean())}
            if (target, c) in OF2_MAP:
                fn, off = OF2_MAP[(target, c)]
                o = of2_plddt(fn)[off:off + len(pl)]
                cm["openfold2_dummy_msa_mean_plddt_same_residues"] = float(o.mean())
            m["chains"][c] = cm
        if len(chains) > 1:
            heavy = [a for a in at if not a["type_symbol"].startswith("H")]
            xyz = np.array([[float(a["Cartn_x"]), float(a["Cartn_y"]), float(a["Cartn_z"])] for a in heavy])
            ch = np.array([a["label_asym_id"] for a in heavy]); rn = np.array([int(a["label_seq_id"]) for a in heavy])
            bf = {(a["label_asym_id"], int(a["label_seq_id"])): float(a["B_iso_or_equiv"]) for a in ca}
            A, B = chains[0], chains[1]
            ia, ib = np.where(ch == A)[0], np.where(ch == B)[0]
            dd = np.linalg.norm(xyz[ia][:, None, :] - xyz[ib][None, :, :], axis=-1)
            pa, pb = np.where(dd < 5.0)
            ra, rb = sorted(set(rn[ia][pa].tolist())), sorted(set(rn[ib][pb].tolist()))
            m["interface"] = {"chains": [A, B], "n_residues_A": len(ra), "n_residues_B": len(rb), "residues_A": ra, "residues_B": rb,
                              "mean_plddt_interface": float(np.mean([bf[(A, r)] for r in ra] + [bf[(B, r)] for r in rb])) if ra else None}
        out["models"].append(m)
    return out


def alt_exon_check(fc):
    """Which receptor interface residues fall in the IIIb/IIIc alternatively spliced D3 segment? The segment is the
    contiguous block where zebrafish F1RBT3 (IIIb) and Q8JG38 (IIIc) differ after global alignment. Known biology
    (FGF10 binds FGFR2b, not 2c; specificity set by this exon) predicts the interface should use it."""
    from Bio.Align import PairwiseAligner, substitution_matrices
    inp = ROOT / "results/mol-sims/claude-20261101/inputs"
    rd = lambda a: "".join(l.strip() for l in (inp / f"{a}.fasta").read_text().splitlines()[1:])
    b3, c3 = rd("F1RBT3"), rd("Q8JG38")
    al = PairwiseAligner(); al.substitution_matrix = substitution_matrices.load("BLOSUM62"); al.open_gap_score = -10; al.extend_gap_score = -0.5
    a = al.align(b3, c3)[0]
    same = set()
    for (s1, e1), (s2, e2) in zip(*a.aligned):
        for k in range(e1 - s1):
            if b3[s1 + k] == c3[s2 + k]:
                same.add(s1 + k + 1)
    # D3 region of the construct (F1RBT3 250-360): longest run of non-identical/unaligned positions
    diff = [p for p in range(250, 361) if p not in same]
    runs, cur = [], [diff[0]]
    for p in diff[1:]:
        if p - cur[-1] <= 6: cur.append(p)
        else: runs.append(cur); cur = [p]
    runs.append(cur)
    seg = max(runs, key=lambda r: r[-1] - r[0])
    lo, hi = seg[0], seg[-1]
    out = {"alt_exon_segment_F1RBT3": [lo, hi], "construct_offset": 149}
    for m in fc["models"]:
        rb = [r + 149 for r in m["interface"]["residues_B"]]
        inside = [r for r in rb if lo <= r <= hi]
        out[f"model_{m['model']}_interface_B_in_segment"] = len(inside)
        out[f"model_{m['model']}_interface_B_total"] = len(rb)
        out[f"model_{m['model']}_segment_fraction_of_construct"] = (hi - lo + 1) / 211
    out["residues_B_model0_F1RBT3_numbering"] = [r + 149 for r in fc["models"][0]["interface"]["residues_B"]]
    return out


def main():
    res = {}
    for t in ["shhN", "fgf_complex", "fgf_vs_fgfr2c_negctrl", "kcnk5b_dimer_openfold3", "kcnj13", "kcnj13_tetramer_openfold3"]:
        if (SD / t / "receipt.json").exists() and json.loads((SD / t / "receipt.json").read_text()).get("final_status") == "SUCCEEDED":
            res[t] = analyze(t)
            m0 = res[t]["models"][0]
            print(t, res[t]["confidence_scores"], {c: (round(v["mean_plddt"], 1), round(v.get("openfold2_dummy_msa_mean_plddt_same_residues", float("nan")), 1)) for c, v in m0["chains"].items()},
                  {k: v for k, v in m0.get("interface", {}).items() if k.startswith("n_") or k.startswith("mean")})
    if "fgf_complex" in res:
        res["fgf_complex"]["interface_vs_alternative_exon"] = alt_exon_check(res["fgf_complex"])
        print("alt exon check", {k: v for k, v in res["fgf_complex"]["interface_vs_alternative_exon"].items() if not isinstance(v, list)})
    if "kcnk5b_dimer_openfold3" in res:   # pLDDT inside the UniProt pore domains (Q6PFU3 75-137, 173-246)
        at = parse_cif((SD / "kcnk5b_dimer_openfold3" / "model_0.cif").read_text())
        ca = [a for a in at if a["label_atom_id"] == "CA" and a["label_asym_id"] == "A"]
        pl = np.array([float(a["B_iso_or_equiv"]) for a in ca]); o = of2_plddt("kcnk5b_Q6PFU3_rank1.pdb")
        res["kcnk5b_dimer_openfold3"]["pore_domains"] = {f"{s}-{e}": {"of3_dimer_mean_plddt": float(pl[s - 1:e].mean()), "of2_monomer_mean_plddt": float(o[s - 1:e].mean())}
                                                         for s, e in [(75, 137), (173, 246)]}
        print("kcnk5b pore", res["kcnk5b_dimer_openfold3"]["pore_domains"])
    res["_scope"] = "COMPUTED structure hypotheses (Boltz-2, PDB70 MSA); confidence is model self-assessment, not accuracy; nothing observed"
    (SD / "summary.json").write_text(json.dumps(res, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
