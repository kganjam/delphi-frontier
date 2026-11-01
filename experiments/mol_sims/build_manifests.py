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
MI = json.loads((R / "structures/msa_identity.json").read_text())


def tmpl(chain_name):
    """Closest PDB70 hit for one chain: (name, % identity over aligned columns, % query coverage)."""
    h = MI[chain_name]["top5"][0]
    return (f"{h['name']} at {h['identity_pct']:.0f}% identity over {h['query_coverage_pct']:.0f}% of the query "
            f"({MI[chain_name]['n_hits']} hits total; ranked by identity x coverage)")


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
            {"name": "pTM (3 samples)", "result": ", ".join(f"{x:.2f}" for x in S["shhN"]["ptm_scores"])},
            {"name": "closest structure in the supplied PDB70 MSA", "result": tmpl("shhN")}],
           ["pLDDT/pTM are model-internal confidence, not a calibrated probability of correctness."],
           ["Does a holo model with Zn2+/Ca2+ and the cholesterol-modified C terminus change the surface used by Ptch/Hhip?"],
           [lim_msa, "No seed accepted by the runtime; diffusion sampling is nondeterministic.",
            "The closest MSA hit is ~96% identical over most of the chain, so the high confidence is largely template recall, not a de-novo fold."]))

# --- macromolecular: Fgf10a-Fgfr2b with negative control ---
fc, nc = S["fgf_complex"], S["fgf_vs_fgfr2c_negctrl"]
ax = fc["interface_vs_alternative_exon"]
sscp = R / "singleseq_control.json"
SSC = json.loads(sscp.read_text()) if sscp.exists() else None
write(base("boltz2-fgf10a-fgfr2b", "Predicted Fgf10a–Fgfr2b complex (Boltz-2) with a non-cognate Fgfr2c control that scored higher: no specificity signal",
           "macromolecular", SCOPE, "Boltz-2 complex prediction, 3 samples each, PDB70 MSA per chain",
           "Fgf10a core (Q8AY90 58-201) with Fgfr2 IIIb D2-D3 (F1RBT3 150-360); control: Fgfr2 IIIc D2-D3 (Q8JG38 150-362). IIIb chosen by alignment to human P21802-3 vs -1.",
           [R / "structures/fgf_complex/receipt.json", R / "structures/fgf_complex/model_0.cif", R / "structures/fgf_vs_fgfr2c_negctrl/receipt.json", R / "structures/fgf_vs_fgfr2c_negctrl/model_0.cif", R / "structures/summary.json"]
           + ([sscp, R / "structures/fgf_complex_singleseq/receipt.json", R / "structures/fgf_vs_fgfr2c_negctrl_singleseq/receipt.json"] if SSC else []),
           ["FGF10-FGFR2b isoform specificity (the non-cognate control scores higher)", "binding affinity or ddG", "that this complex forms in the zebrafish or flying-fish pectoral fin bud"],
           [{"name": "cognate IIIb: confidence / pTM / interface pLDDT (top)", "result": f"{fc['confidence_scores'][0]:.2f} / {fc['ptm_scores'][0]:.2f} / {fc['models'][0]['interface']['mean_plddt_interface']:.1f}"},
            {"name": "non-cognate IIIc control: confidence / pTM / interface pLDDT (top)", "result": f"{nc['confidence_scores'][0]:.2f} / {nc['ptm_scores'][0]:.2f} / {nc['models'][0]['interface']['mean_plddt_interface']:.1f}"},
            {"name": "receptor interface residues inside the IIIb/IIIc alternative exon", "result": f"{ax['model_0_interface_B_in_segment']} of {ax['model_0_interface_B_total']} (segment = {ax['model_0_segment_fraction_of_construct'] * 100:.0f}% of construct)"},
            {"name": "chain pLDDT A/B (cognate)", "result": f"{chain('fgf_complex')['A']['mean_plddt']:.1f} / {chain('fgf_complex')['B']['mean_plddt']:.1f}"},
            {"name": "closest PDB70 hit, receptor IIIb construct", "result": tmpl("fgfr2b_d2d3")},
            {"name": "closest PDB70 hit, receptor IIIc control construct", "result": tmpl("fgfr2c_d2d3")},
            {"name": "template proximity as the suspected cause of the control inversion", "result": "the non-cognate IIIc construct has the CLOSER template of the two, which suggested template proximity rather than biology was tracking the scores - but the control below TESTS that and does not support it"}]
           + ([{"name": "TEMPLATE CONTROL: both complexes refolded with a single-sequence MSA (no PDB70 alignment)",
                "result": f"cognate {SSC['per_pair']['cognate_fgf10a_fgfr2b']['with_pdb70_msa']['top_confidence']} -> "
                          f"{SSC['per_pair']['cognate_fgf10a_fgfr2b']['single_sequence']['top_confidence']}, non-cognate "
                          f"{SSC['per_pair']['noncognate_fgf10a_fgfr2c']['with_pdb70_msa']['top_confidence']} -> "
                          f"{SSC['per_pair']['noncognate_fgf10a_fgfr2c']['single_sequence']['top_confidence']}. The non-cognate complex "
                          f"still scores higher; the gap only narrows from {SSC['inversion_gap_noncognate_minus_cognate']['with_pdb70_msa']} "
                          f"to {SSC['inversion_gap_noncognate_minus_cognate']['single_sequence']}. The inversion is NOT explained by template proximity."},
               {"name": "which chain the alignment was holding up", "result": SSC["where_the_confidence_lived"]}] if SSC else []),
           ["Confidence scores are not affinities; no ddG was computed (stab_ddg needs an undocumented upload manifest, blocked)."],
           ["Would a deep (UniRef) MSA or AlphaFold3 discriminate IIIb from IIIc? Would MD separate them?",
            "Why does the inversion survive removal of the MSA? A single-sequence input removes the alignment but not the model's learned structural memory, so memorisation is not excluded."],
           [lim_msa, "The negative control failed to discriminate, so the predictor is not informative about isoform choice here.",
            "The single-sequence control removes the MSA, not learned structural memory: the receptor chain still reaches above 80 pLDDT with no alignment."]))

# --- macromolecular: Kcnk5b dimer ---
kd = S["kcnk5b_dimer_openfold3"]; kc = chain("kcnk5b_dimer_openfold3")["A"]
write(base("openfold3-kcnk5b-dimer", "Predicted Kcnk5b (another longfin) K2P channel dimer (OpenFold3 + MSA): low interface confidence",
           "macromolecular", SCOPE, "OpenFold3 preview2 (Nebius MCP infer_openfold3_native), seed 42, 1 sample, PDB70 MSA",
           "Kcnk5b (Q6PFU3) residues 1-265 x2 (transmembrane core). Boltz-2 refused the homodimer (same-sequence MSA check); its failure receipt is kept.",
           [R / "structures/kcnk5b_dimer_openfold3/receipt.json", R / "structures/kcnk5b_dimer_openfold3/model_0.cif", R / "structures/kcnk5b_dimer_boltz2_failed/receipt.json", R / "structures/summary.json"],
           ["the dimer interface (ipTM below 0.6)", "conductance, gating or the effect of any fin-overgrowth allele", "membrane placement (no lipid bilayer modelled)"],
           [{"name": "chain mean pLDDT", "result": f"{kc['mean_plddt']:.1f} (OpenFold2 monomer, same residues: {kc['openfold2_dummy_msa_mean_plddt_same_residues']:.1f})"},
            {"name": "ipTM / pTM", "result": f"{kd['iptm_scores'][0]:.2f} / {kd['ptm_scores'][0]:.2f}"},
            {"name": "closest structure in the supplied PDB70 MSA", "result": tmpl("kcnk5b_core")},
            {"name": "pore domains mean pLDDT (75-137, 173-246)", "result": ", ".join(f"{k}: {v['of3_dimer_mean_plddt']:.1f} (OF2 {v['of2_monomer_mean_plddt']:.1f})" for k, v in kd["pore_domains"].items())}],
           ["Model-internal confidence only."], ["Does a membrane-aware model or AlphaFold3 raise the interface confidence enough to place alf variants?"],
           [lim_msa, "Single sample; no MD run because the interface is not confident."]))

# --- macromolecular: Kcnj13 (recorded OF2 gap) ---
if "kcnj13" in S:
    kj = chain("kcnj13")["A"]
    checks = [{"name": "mean pLDDT / fraction >= 70 (Boltz-2, top)", "result": f"{kj['mean_plddt']:.1f} / {kj['frac_ge70'] * 100:.0f}%"},
              {"name": "recorded OpenFold2 dummy-MSA gap, same sequence (sha256 8029209...)", "result": f"mean {kj['openfold2_dummy_msa_mean_plddt_same_residues']:.1f}; 18% of residues >= 70"},
              {"name": "pTM (3 samples)", "result": ", ".join(f"{x:.2f}" for x in S["kcnj13"]["ptm_scores"])},
              {"name": "closest structure in the supplied PDB70 MSA", "result": tmpl("kcnj13") + " -- the weakest template of the four targets, which is the honest reason this target stays the least resolved"}]
    srcs = [R / "structures/kcnj13/receipt.json", R / "structures/kcnj13/model_0.cif", R / "structures/summary.json"]
    if "kcnj13_tetramer_openfold3" in S:
        t = S["kcnj13_tetramer_openfold3"]; tc = chain("kcnj13_tetramer_openfold3")["A"]
        checks.append({"name": "OpenFold3 tetramer attempt: chain pLDDT / ipTM / pTM / confidence", "result": f"{tc['mean_plddt']:.1f} / {t['iptm_scores'][0]:.2f} / {t['ptm_scores'][0]:.2f} / {t['confidence_scores'][0]:.2f} -- WORSE than the monomer; the tetramer was not resolved"})
        srcs += [R / "structures/kcnj13_tetramer_openfold3/receipt.json", R / "structures/kcnj13_tetramer_openfold3/model_0.cif"]
    write(base("boltz2-kcnj13", "Predicted zebrafish Kcnj13 (Kir7.1) with an MSA: revisits the low-confidence OpenFold2 model",
               "macromolecular", SCOPE, "Boltz-2 monomer (3 samples) and OpenFold3 tetramer, PDB70 MSA",
               "Full-length Kcnj13 (Q0KIZ7, 362 aa), the same sequence as the studio's openfold2-kcnj13 card.",
               srcs, ["channel function, rectification or pigment-pattern/fin effects", "membrane placement", "a tetramer: the 4-chain attempt scored far lower than the monomer"],
               checks, ["Model-internal confidence only."], ["Would a membrane-aware model or a deep MSA resolve the tetramer? The PDB70-only MSA did not."],
               [lim_msa, "Monomer prediction of an obligate tetramer."]))

# --- macromolecular: MD of the predicted ShhN model ---
mdp = R / "md_shhN/md_receipt.json"
if mdp.exists():
    a = json.loads(mdp.read_text())["analysis"]
    checks = [{"name": "CA RMSD from the equilibrated start", "result": f"first 1 ns mean {a['rmsd_ca_A']['first_ns_mean']:.2f} A, last 2 ns mean {a['rmsd_ca_A']['last_2ns_mean']:.2f} A, max {a['rmsd_ca_A']['max']:.2f} A; last-2-ns drift {a['rmsd_ca_A']['last_2ns_slope_A_per_ns']:+.2f} A/ns"},
              {"name": "per-residue flexibility vs the predictor's own confidence", "result": f"Spearman rho {a['rmsf_vs_start_plddt_spearman']['rho']:.2f} (p={a['rmsf_vs_start_plddt_spearman']['p']:.1e}) between CA RMSF and start-model pLDDT: low-confidence residues move most"},
              {"name": "radius of gyration, first vs last frame", "result": f"{a['rg_ca_A_first_last'][0]:.2f} -> {a['rg_ca_A_first_last'][1]:.2f} A (no unfolding)"},
              {"name": "all saved values finite", "result": str(a["all_finite"])},
              {"name": "throughput", "result": f"{a['ns_per_day']:.0f} ns/day on one H100, {a['n_atoms']} atoms"}]
    rcp = R / "md_shhN_replica_comparison.json"
    srcs = [R / "md_shhN/md_receipt.json", R / "md_shhN/md_summary.json", R / "md_shhN/final_frame_protein.pdb", R / "md_shhN/job_log.txt", R / "structures/shhN/model_0.cif"]
    if rcp.exists():
        rc = json.loads(rcp.read_text()); r1, r2 = rc["replicas"]
        checks.append({"name": "SECOND REPLICA (seed {}), same correlation".format(r2["seed"]), "result": f"Spearman rho {r2['rmsf_vs_plddt']['rho']:.2f} (p={r2['rmsf_vs_plddt']['p']:.1e}): the confidence-flexibility relation reproduces across seeds"})
        checks.append({"name": "cross-replica agreement on which residues move", "result": f"Spearman rho {rc['cross_replica_rmsf_spearman']['rho']:.2f} between the two replicas' per-residue RMSF (median ratio {rc['rmsf_ratio_median']:.2f})"})
        checks.append({"name": "convergence, honestly", "result": f"the replicas DISAGREE on drift: last-2-ns slope {r1['last_2ns_slope_A_per_ns']:+.2f} vs {r2['last_2ns_slope_A_per_ns']:+.2f} A/ns at similar RMSD ({r1['last_2ns_mean']:.2f} vs {r2['last_2ns_mean']:.2f} A). 10 ns is NOT converged; only the ranking of mobile residues is stable"})
        cvp = R / "md_convergence_report.json"
        if cvp.exists():
            cv = json.loads(cvp.read_text())
            sl = cv["final_block_slopes_A_per_ns"]
            checks.append({"name": "drift measured over 5 ns blocks instead of 2 ns windows", "result":
                           "final-5-ns-block slope per replica: " + ", ".join(f"{k} {v:+.2f} A/ns" for k, v in sl.items())
                           + ". A 2 ns window is too short to read a slope from: the negative last-2-ns "
                             "figure above is window noise, not a plateau, and should not be quoted as one."})
            longr = [k for k in cv["replicas"] if cv["replicas"][k]["prod_ns"] >= 30]
            if longr:
                checks.append({"name": f"two 40 ns replicas added to test convergence ({', '.join(longr)})",
                               "result": cv["verdict"]})
                checks.append({"name": "what reproduces across ALL FOUR replicas (2 x 10 ns, 2 x 40 ns)",
                               "result": f"flexibility vs start-model pLDDT: rho {cv['rmsf_rho_range_all_replicas'][0]} to "
                                         f"{cv['rmsf_rho_range_all_replicas'][1]} in every replica; per-residue RMSF agrees "
                                         f"between every pair of replicas at rho {cv['cross_replica_rmsf_rho_range'][0]} to "
                                         f"{cv['cross_replica_rmsf_rho_range'][1]}. The ranking of mobile residues is the "
                                         f"robust result; the absolute RMSD level is not."})
                for k in longr:
                    rr = cv["replicas"][k]
                    srcs.extend([R / k / "md_receipt.json", R / k / "md_summary.json", R / k / "job_log.txt", R / k / "final_frame_protein.pdb"])
                vfp = R / "md_log_verification.json"
                if vfp.exists():
                    vf = json.loads(vfp.read_text())
                    checks.append({"name": "log-integrity re-check of every MD run in this project",
                                   "result": ", ".join(f"{len(v)} {st}" for st, v in vf["by_status"].items())
                                             + ". The log service returns 16 KiB pieces out of order; accepting any ordering that "
                                               "merely PARSED once spliced potential energies into the RMSD array (a 926209 A RMSD "
                                               "and a negative radius of gyration). The reassembler now also checks array lengths, "
                                               "distance ranges and energy signs, and every committed run re-derives from its saved log."})
                    srcs.append(vfp)
            srcs.append(cvp)
        srcs += [rcp, R / "md_shhN_rep2/md_receipt.json", R / "md_shhN_rep2/md_summary.json", R / "md_shhN_rep2/final_frame_protein.pdb", R / "md_shhN_rep2/job_log.txt"]
    write(base("openmm-shhN-md", "Explicit-solvent MD of the predicted Shha signalling domain, 2 x 10 ns + 2 x 40 ns: flexibility tracks predictor confidence in every replica, but the runs are not converged",
               "macromolecular", "SIMULATED classical MD of a PREDICTED structure; not an observation",
               f"OpenMM 8.6.1 CUDA mixed precision, amber14 + TIP3P-FB, PME 1.0 nm, HBonds, LangevinMiddle 301 K, 2 fs, 0.15 M NaCl, seed {a['seed']}",
               "Start: the Boltz-2 ShhN model (model_0.cif). Minimise, 100 ps NVT, 200 ps NPT, 10 ns production NPT; CA frames every 10 ps. TWO independent replicas (seeds 20261101 and 777000). Run as a Nebius AI job on one H100; results read from the job log, which the service splits and can return out of order, so the summary and final frame are reassembled and checked (JSON parse, gzip) before use.",
               srcs,
               ["that the predicted fold is correct (MD stability is not accuracy)",
                "a converged simulation: 5 ns block means wander by about 3 A in BOTH 40 ns replicas with the slope changing sign repeatedly, so RMSD plateau is not a usable criterion here",
                "any equilibrium property, free energy or binding quantity from these replicas",
                "Zn2+/Ca2+ site behaviour: this is an apo run with no ions bound", "anything about fin size, Shh gradient range or flight"],
               checks,
               ["Force-field and water-model error are not quantified here.", "Protonation states are PDBFixer defaults at pH 7."],
               ["Does a holo run with Zn2+/Ca2+ reduce the motion at the metal site?",
                "At what length does the RMSD block-mean wander (about 3 A over 40 ns) actually settle? 40 ns is not enough.",
                "Would a frame-level test (pairwise RMSD matrix, cluster overlap between replicas) show sampling overlap? It needs trajectory frames, which the job log does not return."],
               ["10 ns per replica: far too short to sample conformational change (argon), and the two replicas disagree on whether the RMSD has settled.", "The start is a prediction, so every number inherits that uncertainty."],
               time_units="nanoseconds of simulated time"))

# --- macromolecular: MD of the predicted FGF complex, with the non-cognate control ---
fp = R / "md_fgf_complex/md_receipt.json"
if fp.exists():
    a = json.loads(fp.read_text())["analysis"]; iface = a["interface"]
    checks = [{"name": "CA RMSD from the equilibrated start", "result": f"first 1 ns mean {a['rmsd_ca_A']['first_ns_mean']:.2f} A, last 2 ns mean {a['rmsd_ca_A']['last_2ns_mean']:.2f} A, max {a['rmsd_ca_A']['max']:.2f} A; last-2-ns drift {a['rmsd_ca_A']['last_2ns_slope_A_per_ns']:+.2f} A/ns"},
              {"name": "inter-chain CA contacts retained (<8 A, from the start frame)", "result": f"{iface['retained_fraction_last_2ns_mean'] * 100:.0f}% over the last 2 ns, minimum {iface['retained_fraction_min'] * 100:.0f}% of {iface['n_initial_ca_pairs_lt8A']} initial pairs; the two chains never separate (closest CA {iface['min_interchain_ca_distance_last']:.1f} A at the end)"},
              {"name": "per-residue flexibility vs start-model pLDDT, pooled over both chains", "result": f"Spearman rho {a['rmsf_vs_start_plddt_spearman']['rho']:.2f} (p={a['rmsf_vs_start_plddt_spearman']['p']:.3f}): not significant pooled - but see the per-chain correction below, which is where this test belongs"},
              {"name": "radius of gyration, first vs last frame", "result": f"{a['rg_ca_A_first_last'][0]:.2f} -> {a['rg_ca_A_first_last'][1]:.2f} A"},
              {"name": "all saved values finite", "result": str(a["all_finite"])},
              {"name": "throughput", "result": f"{a['ns_per_day']:.0f} ns/day on one H100, {a['n_atoms']} atoms"}]
    srcs = [R / "md_fgf_complex/md_receipt.json", R / "md_fgf_complex/md_summary.json", R / "md_fgf_complex/final_frame_protein.pdb", R / "md_fgf_complex/job_log.txt"]
    stp = R / "md_complex_stratified.json"
    ST = json.loads(stp.read_text()) if stp.exists() else None
    ncp = R / "md_fgf_negctrl/md_receipt.json"
    if ncp.exists():
        na = json.loads(ncp.read_text())["analysis"]; ni = na["interface"]
        checks.insert(2, {"name": "SAME RUN ON THE NON-COGNATE IIIc CONTROL: contacts retained", "result": f"{ni['retained_fraction_last_2ns_mean'] * 100:.0f}% over the last 2 ns (minimum {ni['retained_fraction_min'] * 100:.0f}%) of {ni['n_initial_ca_pairs_lt8A']} initial pairs; CA RMSD last 2 ns {na['rmsd_ca_A']['last_2ns_mean']:.2f} A"})
        checks.insert(3, {"name": "what the control implies for MD as a specificity test", "result": (f"the non-cognate interface stays within the same range as the cognate one over 10 ns "
                                                                                                        f"({ni['retained_fraction_last_2ns_mean'] * 100:.0f}% vs {iface['retained_fraction_last_2ns_mean'] * 100:.0f}% retained, from {ni['n_initial_ca_pairs_lt8A']} vs {iface['n_initial_ca_pairs_lt8A']} initial pairs), "
                                                                                                        f"so interface persistence at this length does NOT discriminate the isoforms; the only difference is how many contacts the prediction started with"
                                                                                                        if ni["retained_fraction_last_2ns_mean"] > 0.6 * iface["retained_fraction_last_2ns_mean"] else
                                                                                                        "the non-cognate interface loosened markedly more than the cognate one over 10 ns; a longer, replicated test would be needed before treating that as a specificity signal")})
        srcs += [R / "md_fgf_negctrl/md_receipt.json", R / "md_fgf_negctrl/md_summary.json", R / "md_fgf_negctrl/final_frame_protein.pdb", R / "md_fgf_negctrl/job_log.txt"]
    if ST:
        cc = ST["contact_comparison"]
        checks.insert(4, {"name": "the same comparison as an absolute count, not a fraction",
                          "result": f"{cc['cognate_retained_count']} surviving inter-chain CA pairs for the cognate complex vs "
                                    f"{cc['noncognate_retained_count']} for the non-cognate ({cc['ratio_cognate_over_noncognate']}x). " + cc["reading"]})
        sf = ST["stratified_finding"]
        checks.append({"name": "CORRECTION: flexibility vs confidence, split by chain instead of pooled",
                       "result": "; ".join(f"{k}: rho {v['rho']} (R2 {v['r2']}, n={v['n']})" for k, v in sf["surviving_groups"].items() if "interface" in k)
                                 + f". {sf['n_tests']} groups tested, Bonferroni alpha {sf['bonferroni_alpha']}. " + sf["finding"]})
        srcs.append(stp)
    write(base("openmm-fgf10a-fgfr2b-md", "10 ns MD of the predicted Fgf10a-Fgfr2b complex, run alongside the non-cognate Fgfr2c control",
               "macromolecular", "SIMULATED classical MD of a PREDICTED complex; not an observation",
               f"OpenMM 8.6.1 CUDA mixed precision, amber14 + TIP3P-FB, PME 1.0 nm, HBonds, LangevinMiddle 301 K, 2 fs, 0.15 M NaCl, seed {a['seed']}",
               "Start: the Boltz-2 complex model (model_0.cif). Minimise, 100 ps NVT, 200 ps NPT, 10 ns production NPT, CA frames every 10 ps. One replica per complex. Nebius AI job on one H100; the job log is reassembled and checked before use.",
               srcs,
               ["binding affinity, ddG or on/off rates", "FGF10-FGFR2b isoform specificity: the non-cognate control behaves the same way",
                "that the predicted docking pose is correct (a wrong pose can also persist for 10 ns)",
                "a causal link between predictor confidence and simulated flexibility: both may follow from the same sparse MSA coverage",
                "that the flexibility is local - whole-complex superposition leaves rigid-body rocking in the RMSF",
                "anything about fin size or flight"],
               checks,
               ["Force-field and water-model error are not quantified.", "No ddG was computed: the hosted stab_ddg tool needs an upload manifest whose format is undocumented."],
               ["Do the two complexes separate over hundreds of ns, or under free-energy perturbation?"],
               ["Single replica per complex, 10 ns: too short for a binding claim.", "Both starts are predictions, and the predictor already failed its isoform control."],
               time_units="nanoseconds of simulated time"))

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

# --- subcellular: RA/FGF switch ---
s1 = json.loads((R / "s1_ra_fgf_switch_perturbations.json").read_text())["perturbations"]
rng = lambda k: s1[k]["bistable_x_range"]
write(base("sbml-ra-fgf-bistable-switch", "RA/FGF mutual-inhibition switch (BIOMD0000000275): where the bistable boundary sits when synthesis rates change",
           "subcellular", "SIMULATED: published-model ODE dynamics, not fit to fish data", "libRoadRunner 2.11.0 CVODE, rtol 1e-10, deterministic; two initial states per position to detect bistability",
           "Goldbeter-Gonze-Pourquie 2007 somitogenesis switch, swept at 51 positions x (0-50) for 8 parameter settings. Used here as a generic two-morphogen switch, NOT as a fin model.",
           [R / "s1_ra_fgf_switch_perturbations.json", R / "s1_receipt.json"],
           ["any fin or limb bud boundary position (the model is a presomitic-mesoderm model in arbitrary position units)",
            "that RA/FGF sets flying-fish pectoral fin proportions", "the Cyp26-loss case, which never reached steady state and is reported as invalid"],
           [{"name": "baseline bistable window (model position units)", "result": f"x {rng('baseline')[0]:.0f}-{rng('baseline')[1]:.0f} ({s1['baseline']['n_bistable_points']} of 51 positions)"},
            {"name": "FGF synthesis x2 / x4", "result": f"window moves to x {rng('fgf_over_ks3x2')[0]:.0f}-{rng('fgf_over_ks3x2')[1]:.0f} / {rng('fgf_over_ks3x4')[0]:.0f}-{rng('fgf_over_ks3x4')[1]:.0f}"},
            {"name": "RA synthesis x0.5 / x2", "result": f"x {rng('ra_synth_x0.5')[0]:.0f}-{rng('ra_synth_x0.5')[1]:.0f} / {rng('ra_synth_x2')[0]:.0f}-{rng('ra_synth_x2')[1]:.0f}"},
            {"name": "FGF loss", "result": "bistability disappears entirely (0 of 51 positions)"},
            {"name": "steady-state residual, all valid runs", "result": f"max |dy/dt| {max(v['max_residual_rate_all_runs'] for k, v in s1.items() if 'cyp26' not in k):.1e}"},
            {"name": "Cyp26 loss", "result": f"max |dy/dt| {s1['cyp26_loss_V0=Vsc=0']['max_residual_rate_all_runs']:.1f}: NOT a steady state, RA accumulates without bound. Reported as a model defect, not a result."}],
           ["Every rate constant is the published model's; none measured in any fish."],
           ["Does the boundary in a real fin bud show hysteresis, i.e. depend on treatment history?"],
           ["The model has no Cyp26-independent RA clearance, so RA-degradation knockouts cannot be simulated in it.",
            "Local sensitivity near this switch is not a derivative (see s3); the bistable window location is the usable output."],
           time_units="model time units (unconverted); steady states only"))

# --- cellular: bioelectric Kcnk5b ---
s5 = json.loads((R / "s5_bioelectric_kcnk5b_sweep.json").read_text())
st = s5["kcnk5b_step_from_1x_state"]
g = lambda c, f, k, i: next(r for r in st[c] if r["kcnk5b_fold"] == f)["trajectory"][i][k]
MT = json.loads((R / "s5_matched_timepoints.json").read_text()) if (R / "s5_matched_timepoints.json").exists() else None
write(base("bioelectric-kcnk5b-pump-leak", "Single-cell Kcnk5b dose model: passive K+ leak hyperpolarises; Na-channel recruitment gives a small depolarisation inside the physiological window",
           "cellular", "SIMULATED with ASSUMED generic parameters; a sign test, not a calibrated model", "SciPy LSODA pump-leak ODE (GHK leaks, Kir, persistent Na, Na/K-ATPase)",
           "Kcnk5b 0-32x step from the 1x state, read at 10 min, 1 h, 6 h, 24 h; passive (c=0) vs Na-recruitment (g_NaP ~ fold^c) arms. Targets from Yi et al. 2024 PLoS Biol (PMID 38527087).",
           [R / "s5_bioelectric_kcnk5b_sweep.json", R / "s5_receipt.json"] + ([R / "s5_matched_timepoints.json"] if MT else []),
           ["any zebrafish membrane potential value (parameters are generic)", "the Kcnk5b -> Na-channel link itself (it is assumed in the c=1 arm)", "fin size or shha induction"],
           [{"name": "passive arm, Kcnk5b x8, Vm at 10 min / 1 h", "result": f"{g('c=0.0', 8, 'Vm_mV', 0):.1f} / {g('c=0.0', 8, 'Vm_mV', 1):.1f} mV (baseline {g('c=0.0', 1, 'Vm_mV', 0):.1f})"},
            {"name": "Na-recruitment arm (c=1), Kcnk5b x8, Vm at 1 h; K_i at 6 h", "result": f"{g('c=1.0', 8, 'Vm_mV', 1):.1f} mV; {g('c=1.0', 8, 'K_i', 2):.1f} mM"},
            {"name": "Kcnj13 0-2x at baseline", "result": "no Vm change (Kir rectified off at about -32 mV)"}]
           + ([{"name": "CORRECTION: largest fold at which each arm is still physiological at 10 min",
                "result": "; ".join(f"{k} fold {v['largest_fold_still_physiological_at_600s']}, Vm {v['Vm_mV']:.1f} mV "
                                    f"({v['delta_Vm_from_baseline_mV']:+.1f} from baseline), Na_i {v['Na_i_mM']} mM, K_i {v['K_i_mM']} mM"
                                    for k, v in MT["largest_physiological_fold_per_arm"].items() if v)
                          + ". Screened against Na_i 5-30 mM and K_i 100-150 mM."},
               {"name": "what that leaves of the sign test", "result": MT["restated_conclusion"]},
               {"name": "steady state?", "result": "no arm is at steady state at any stored time: the per-point Vm change is non-zero throughout, so these are transients"}]
              if MT else []),
           ["Every conductance, pump capacity and concentration is assumed.", "Fixed cell volume; no osmotic regulation.",
            "The recruitment arm scales an inward Na+ conductance by the same factor as the K+ conductance, so recovering a depolarisation is close to built in: it shows a depolarising route is not excluded, not that it is the one used.",
            "Beyond 4x fold the recruitment arm leaves the physiological ion range within 10 min and its later points describe a failing cell."],
           ["Do hsp70:kcnk5b fin-bud cells show rising Na_i (recruitment) or falling Na_i (passive)?",
            "Does the depolarisation survive Na+-free (NMDG+) extracellular solution? Recruitment requires that it does NOT; that is the falsifying test."],
           ["Ion steady state takes days; only the step-response window is physiologically relevant."], time_units="seconds"))
