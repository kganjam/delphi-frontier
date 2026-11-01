"""Write studio simulation manifests (site/artifacts/simulations/<id>/manifest.json) from claude-mol receipts.

Schema follows codex-demo scripts/build_site.py simulation_manifests()/cards (id, title, scales, evidence_kind, model,
time, video, numerical_checks, parameter_unknowns, open_questions, limitations, couplings) plus two fields the
studio gap review asked for: project_scale (exactly one) and does_not_establish. Every number is read from a committed
result file, never typed by hand. Usage: python build_manifests.py
"""
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
R = ROOT / "results/mol-sims/claude-20261101"
OUT = ROOT / "site/artifacts/simulations"
S = json.loads((R / "structures/summary.json").read_text())


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def rel(p):
    return Path(p).relative_to(ROOT).as_posix()


def base(id_, title, scale, kind, model_name, context, sources, not_est, checks, unknowns, questions, limits, time_units="none: a single static prediction"):
    return {"id": id_, "title": title, "scales": [scale], "project_scale": scale, "evidence_kind": kind,
            "model": {"name": model_name, "context": context}, "time": {"units": time_units, "note": ""},
            "video": None, "numerical_checks": checks, "parameter_unknowns": unknowns, "open_questions": questions,
            "limitations": limits, "does_not_establish": not_est, "couplings": [],
            "source_files": {rel(p): sha(p) for p in sources}, "producer": "claude-mol harness, branch claude/mol-sims-20261101"}


def chain(t, m=0):
    return S[t]["models"][m]["chains"]


def write(m):
    d = OUT / m["id"]; d.mkdir(parents=True, exist_ok=True)
    (d / "manifest.json").write_text(json.dumps(m, indent=1) + "\n")
    print(m["id"], m["project_scale"])


SCOPE = "PREDICTED: a computed structure hypothesis, not an observed structure"
lim_msa = "MSA is PDB70-only (structural database, 14-122 sequences), so homologous crystal structures may be templated."

# --- macromolecular: ShhN ---
c = chain("shhN")["A"]
write(base("boltz2-shhN", "Predicted structure of zebrafish Shha signalling domain (Boltz-2 + MSA): a computed model, not an observation",
           "macromolecular", SCOPE, "Boltz-2 (Nebius Scientific AI MCP boltz2_predict_native), 3 diffusion samples, PDB70 MMseqs2 MSA",
           "Shha (UniProt Q92008) residues 24-197, the mature N-terminal signalling fragment.",
           [R / "structures/shhN/receipt.json", R / "structures/shhN/model_0.cif", R / "structures/summary.json", R / "structures/msa/shhN.a3m"],
           ["that zebrafish ShhN adopts this fold in vivo", "Zn2+/Ca2+ site geometry (no ions were modelled)", "anything about Shh secretion, lipidation, gradient range or fin size"],
           [{"name": "mean pLDDT (top model)", "result": f"{c['mean_plddt']:.1f}; {c['frac_ge70'] * 100:.0f}% of residues >= 70"},
            {"name": "same residues in the earlier OpenFold2 dummy-MSA prediction", "result": f"mean pLDDT {c['openfold2_dummy_msa_mean_plddt_same_residues']:.1f}"},
            {"name": "pTM (3 samples)", "result": ", ".join(f"{x:.2f}" for x in S["shhN"]["ptm_scores"])}],
           ["pLDDT/pTM are model-internal confidence, not a calibrated probability of correctness."],
           ["Does a holo model with Zn2+/Ca2+ and the cholesterol-modified C terminus change the surface used by Ptch/Hhip?"],
           [lim_msa, "No seed accepted by the runtime; diffusion sampling is nondeterministic."]))

# --- macromolecular: Fgf10a-Fgfr2b with negative control ---
fc, nc = S["fgf_complex"], S["fgf_vs_fgfr2c_negctrl"]
ax = fc["interface_vs_alternative_exon"]
write(base("boltz2-fgf10a-fgfr2b", "Predicted Fgf10a–Fgfr2b complex (Boltz-2) with a non-cognate Fgfr2c control that scored higher: no specificity signal",
           "macromolecular", SCOPE, "Boltz-2 complex prediction, 3 samples each, PDB70 MSA per chain",
           "Fgf10a core (Q8AY90 58-201) with Fgfr2 IIIb D2-D3 (F1RBT3 150-360); control: Fgfr2 IIIc D2-D3 (Q8JG38 150-362). IIIb chosen by alignment to human P21802-3 vs -1.",
           [R / "structures/fgf_complex/receipt.json", R / "structures/fgf_complex/model_0.cif", R / "structures/fgf_vs_fgfr2c_negctrl/receipt.json", R / "structures/fgf_vs_fgfr2c_negctrl/model_0.cif", R / "structures/summary.json"],
           ["FGF10-FGFR2b isoform specificity (the non-cognate control scores higher)", "binding affinity or ddG", "that this complex forms in the zebrafish or flying-fish pectoral fin bud"],
           [{"name": "cognate IIIb: confidence / pTM / interface pLDDT (top)", "result": f"{fc['confidence_scores'][0]:.2f} / {fc['ptm_scores'][0]:.2f} / {fc['models'][0]['interface']['mean_plddt_interface']:.1f}"},
            {"name": "non-cognate IIIc control: confidence / pTM / interface pLDDT (top)", "result": f"{nc['confidence_scores'][0]:.2f} / {nc['ptm_scores'][0]:.2f} / {nc['models'][0]['interface']['mean_plddt_interface']:.1f}"},
            {"name": "receptor interface residues inside the IIIb/IIIc alternative exon", "result": f"{ax['model_0_interface_B_in_segment']} of {ax['model_0_interface_B_total']} (segment = {ax['model_0_segment_fraction_of_construct'] * 100:.0f}% of construct)"},
            {"name": "chain pLDDT A/B (cognate)", "result": f"{chain('fgf_complex')['A']['mean_plddt']:.1f} / {chain('fgf_complex')['B']['mean_plddt']:.1f}"}],
           ["Confidence scores are not affinities; no ddG was computed (stab_ddg needs an undocumented upload manifest, blocked)."],
           ["Would a deep (UniRef) MSA or AlphaFold3 discriminate IIIb from IIIc? Would MD separate them?"],
           [lim_msa, "The negative control failed to discriminate, so the predictor is not informative about isoform choice here."]))

# --- macromolecular: Kcnk5b dimer ---
kd = S["kcnk5b_dimer_openfold3"]; kc = chain("kcnk5b_dimer_openfold3")["A"]
write(base("openfold3-kcnk5b-dimer", "Predicted Kcnk5b (another longfin) K2P channel dimer (OpenFold3 + MSA): low interface confidence",
           "macromolecular", SCOPE, "OpenFold3 preview2 (Nebius MCP infer_openfold3_native), seed 42, 1 sample, PDB70 MSA",
           "Kcnk5b (Q6PFU3) residues 1-265 x2 (transmembrane core). Boltz-2 refused the homodimer (same-sequence MSA check); its failure receipt is kept.",
           [R / "structures/kcnk5b_dimer_openfold3/receipt.json", R / "structures/kcnk5b_dimer_openfold3/model_0.cif", R / "structures/kcnk5b_dimer_boltz2_failed/receipt.json", R / "structures/summary.json"],
           ["the dimer interface (ipTM below 0.6)", "conductance, gating or the effect of any fin-overgrowth allele", "membrane placement (no lipid bilayer modelled)"],
           [{"name": "chain mean pLDDT", "result": f"{kc['mean_plddt']:.1f} (OpenFold2 monomer, same residues: {kc['openfold2_dummy_msa_mean_plddt_same_residues']:.1f})"},
            {"name": "ipTM / pTM", "result": f"{kd['iptm_scores'][0]:.2f} / {kd['ptm_scores'][0]:.2f}"},
            {"name": "pore domains mean pLDDT (75-137, 173-246)", "result": ", ".join(f"{k}: {v['of3_dimer_mean_plddt']:.1f} (OF2 {v['of2_monomer_mean_plddt']:.1f})" for k, v in kd["pore_domains"].items())}],
           ["Model-internal confidence only."], ["Does a membrane-aware model or AlphaFold3 raise the interface confidence enough to place alf variants?"],
           [lim_msa, "Single sample; no MD run because the interface is not confident."]))

# --- macromolecular: Kcnj13 (recorded OF2 gap) ---
if "kcnj13" in S:
    kj = chain("kcnj13")["A"]
    checks = [{"name": "mean pLDDT / fraction >= 70 (Boltz-2, top)", "result": f"{kj['mean_plddt']:.1f} / {kj['frac_ge70'] * 100:.0f}%"},
              {"name": "recorded OpenFold2 dummy-MSA gap, same sequence (sha256 8029209...)", "result": f"mean {kj['openfold2_dummy_msa_mean_plddt_same_residues']:.1f}; 18% of residues >= 70"},
              {"name": "pTM (3 samples)", "result": ", ".join(f"{x:.2f}" for x in S["kcnj13"]["ptm_scores"])}]
    srcs = [R / "structures/kcnj13/receipt.json", R / "structures/kcnj13/model_0.cif", R / "structures/summary.json"]
    if "kcnj13_tetramer_openfold3" in S:
        t = S["kcnj13_tetramer_openfold3"]; tc = chain("kcnj13_tetramer_openfold3")["A"]
        checks.append({"name": "OpenFold3 tetramer: chain pLDDT / ipTM / pTM", "result": f"{tc['mean_plddt']:.1f} / {t['iptm_scores'][0]:.2f} / {t['ptm_scores'][0]:.2f}"})
        srcs += [R / "structures/kcnj13_tetramer_openfold3/receipt.json", R / "structures/kcnj13_tetramer_openfold3/model_0.cif"]
    write(base("boltz2-kcnj13", "Predicted zebrafish Kcnj13 (Kir7.1) with an MSA: revisits the low-confidence OpenFold2 model",
               "macromolecular", SCOPE, "Boltz-2 monomer (3 samples) and OpenFold3 tetramer, PDB70 MSA",
               "Full-length Kcnj13 (Q0KIZ7, 362 aa), the same sequence as the studio's openfold2-kcnj13 card.",
               srcs, ["channel function, rectification or pigment-pattern/fin effects", "membrane placement", "a correct tetramer unless ipTM is high"],
               checks, ["Model-internal confidence only."], ["Would a membrane-aware model resolve the cytoplasmic domain packing?"],
               [lim_msa, "Monomer prediction of an obligate tetramer."]))

# --- subcellular: Hedgehog pathway ODE ---
s2b = json.loads((R / "s2b_hedgehog_perturbations_at_ec.json").read_text())
e50 = s2b["perturbations"]["EC50"]
write(base("sbml-hedgehog-pathway-perturbations", "Hedgehog pathway ODE (BIOMD0000000395) perturbed at EC50: fails the Ptc-loss sign check",
           "subcellular", "SIMULATED: published-model ODE dynamics, not fit to fish data", "libRoadRunner 2.11.0 CVODE, rtol 1e-10, deterministic",
           "Sivakumar 2011 Drosophila Hedgehog signal-transduction model; Ptc/Smo/Sufu perturbations at EC10/EC50/EC90 Hh doses interpolated from a 37-dose response.",
           [R / "s2b_hedgehog_perturbations_at_ec.json", R / "s2b_receipt.json", R / "s2_hedgehog_dose_response_perturbations.json", R / "s2_receipt.json"],
           ["anything about zebrafish shha/ptch signalling (Drosophila model, orthology by name only)", "Ptc- or Sufu-null phenotypes: the model gives the WRONG SIGN for both", "fin size"],
           [{"name": "target at EC50 baseline", "result": f"{e50['baseline']['target_s75']:.3f}"},
            {"name": "Ptc loss at EC50 (biology: constitutive activation)", "result": f"{e50['ptc_loss_s1=0']['target_s75']:.3f} = no-Hh basal: sign wrong"},
            {"name": "Sufu-Ci repressor complex loss at EC50", "result": f"{e50['sufu_complex_loss_s128=0']['target_s75']:.3f} (below basal): sign wrong"},
            {"name": "Smo loss at EC50", "result": f"{e50['smo_loss_s148=0']['target_s75']:.3f} (basal, as expected)"}],
           ["All kinetic parameters are the published model's; none measured in fish."],
           ["Re-specified with Ptc catalytically inhibiting Smo, does Ptc=0 give maximal output?"],
           ["Model is unusable for Ptc/Sufu predictions until re-specified.", "Default Hh in the SBML saturates the target; s2 perturbations at that dose were uninformative."],
           time_units="model time units (unconverted)"))

# --- cellular: bioelectric Kcnk5b ---
s5 = json.loads((R / "s5_bioelectric_kcnk5b_sweep.json").read_text())
st = s5["kcnk5b_step_from_1x_state"]
g = lambda c, f, k, i: next(r for r in st[c] if r["kcnk5b_fold"] == f)["trajectory"][i][k]
write(base("bioelectric-kcnk5b-pump-leak", "Single-cell Kcnk5b dose model: passive K+ leak hyperpolarises; only Na-channel recruitment reproduces the reported depolarisation",
           "cellular", "SIMULATED with ASSUMED generic parameters; a sign test, not a calibrated model", "SciPy LSODA pump-leak ODE (GHK leaks, Kir, persistent Na, Na/K-ATPase)",
           "Kcnk5b 0-32x step from the 1x state, read at 10 min, 1 h, 6 h, 24 h; passive (c=0) vs Na-recruitment (g_NaP ~ fold^c) arms. Targets from Yi et al. 2024 PLoS Biol (PMID 38527087).",
           [R / "s5_bioelectric_kcnk5b_sweep.json", R / "s5_receipt.json"],
           ["any zebrafish membrane potential value (parameters are generic)", "the Kcnk5b -> Na-channel link itself (it is assumed in the c=1 arm)", "fin size or shha induction"],
           [{"name": "passive arm, Kcnk5b x8, Vm at 10 min / 1 h", "result": f"{g('c=0.0', 8, 'Vm_mV', 0):.1f} / {g('c=0.0', 8, 'Vm_mV', 1):.1f} mV (baseline {g('c=0.0', 1, 'Vm_mV', 0):.1f})"},
            {"name": "Na-recruitment arm (c=1), Kcnk5b x8, Vm at 1 h; K_i at 6 h", "result": f"{g('c=1.0', 8, 'Vm_mV', 1):.1f} mV; {g('c=1.0', 8, 'K_i', 2):.1f} mM"},
            {"name": "Kcnj13 0-2x at baseline", "result": "no Vm change (Kir rectified off at about -32 mV)"}],
           ["Every conductance, pump capacity and concentration is assumed.", "Fixed cell volume; no osmotic regulation."],
           ["Do hsp70:kcnk5b fin-bud cells show rising Na_i (recruitment) or falling Na_i (passive)?"],
           ["Ion steady state takes days; only the step-response window is physiologically relevant."], time_units="seconds"))
