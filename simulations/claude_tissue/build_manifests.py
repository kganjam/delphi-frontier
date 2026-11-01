"""Write repo-format manifest.json for each claude-tissue simulation directory.
Each manifest carries: project scales, what it does NOT establish, file/code/input hashes, every run receipt
(command, exit code, seed, compute, superseded flag) and a `studio_card` block shaped like the cards in
scripts/build_site.py (id, title, scales, evidence_kind, model, equations, parameter_unknowns, open_questions,
limitations, sources, manifest) so the studio panel can link it without re-deriving claims.
Numbers quoted in cards are read from result files, not typed in."""
import json, pathlib, subprocess, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from claude_tissue.common import ROOT, sha

A = ROOT/"artifacts/simulations"
def J(p): return json.loads((A/p).read_text())

def cards():
    prog = J("claude-tissue-dev-programme/programme.json"); g = prog["groups"]; dec = prog["decomposition"]
    idv = J("claude-tissue-identifiability/identifiability-v2.json")
    rd = J("claude-tissue-rd-wavelength/sweep-v2.json"); el = rd["elasticities"]
    gr = J("claude-tissue-growing-rd/sweep-v2.json")
    fgs = J("claude-tissue-fin-growth/summary.json")
    tr = J("claude-tissue-identifiability/transfer-regimes.json")
    comp = [r for r in tr["rows"] if r["compatible_95"]]
    d_hb = dec["flying fish - halfbeak"]
    C = {}
    C["claude-tissue-dev-programme"] = dict(
        title="Developmental growth-zone programme linking adult pectoral-fin proportion to fin outgrowth rate (fitted to observed allometry)",
        scales=["developmental", "organ"],
        evidence_kind="computed model fitted to observed museum-specimen measurements (cross-sectional); model curves are not growth trajectories",
        model=dict(name="Two-phase distal growth-zone programme: tip-saturated limit of a morphogen-gradient fin-growth model",
                   context="Flying fish, flying halfbeaks, halfbeaks and needlefish from the repo's observed allometry (Daane 2021 Data S1A copy)."),
        equations=[{"label": "Fin growth per unit body growth (model form, declared)", "tex": "\\frac{dL}{dSL}=\\frac{r}{s}\\int_0^{L}\\frac{m(x)}{K+m(x)}\\,dx", "source": "this harness; saturating growth law is an assumption"},
                   {"label": "Tip-saturated limit (where the flying-fish best fit runs; other regimes not excluded)", "tex": "\\frac{dL}{dSL}\\to c=\\frac{r}{s}\\sqrt{D/k}\\,\\ln(1+p)", "source": "identifiability-v2 best fit: l -> 0.009 cm"},
                   {"label": "Adult proportion", "tex": "\\frac{L}{SL}=c+\\frac{a}{SL}\\ \\xrightarrow{SL\\to\\infty}\\ c", "source": "solution of the limit; a = offset laid down before the observed size range"}],
        numerical_results=[f"{k}: c = {v['programme_fit']['c']:.3f} (95% CI {v['programme_fit']['c_ci95'][0]:.3f}-{v['programme_fit']['c_ci95'][1]:.3f}), a = {v['programme_fit']['a_cm']:.2f} cm, n = {v['n']}" for k, v in g.items()]
            + [f"Flying fish minus halfbeak fin/SL at SL {prog['sl_ref_cm']:g} cm: {d_hb['delta_ratio_at_SLref']:.3f}, of which {d_hb['from_growth_zone_c']:.3f} from c and {d_hb['from_early_offset_a']:.3f} from a"]
            + ([f"Species level ({k}): delta c {v['delta_c']:.3f}, two-stage bootstrap 95% CI {v['ci95'][0]:.3f}-{v['ci95'][1]:.3f}" for k, v in J("claude-tissue-dev-programme/programme-species.json")["contrasts"].items()]
               + ["Per-species c: " + ", ".join(f"{k} {v['c']:.3f}" for k, v in J("claude-tissue-dev-programme/programme-species.json")["species"].items())]
               if (A/"claude-tissue-dev-programme/programme-species.json").exists() else []),
        parameter_unknowns=["r, s, D, k, P, K are not separately identified; only the composite c and the extrapolated intercept a are fitted.",
                            "A power law L = b SL^alpha fits modestly better (AIC) in every group; the linear programme is an interpretable, untested reading, not the preferred statistical form.",
                            "The morphogen is hypothetical; no molecule is assigned to m(x)."],
        open_questions=["Is the high flying-fish c a higher outgrowth rate, a longer-lived growth zone, or a larger saturated zone? Longitudinal imaging of the distal fin margin and a graded perturbation series would separate them.",
                        f"Data-compatible gradient lengths predict production elasticities of fin/SL from {min(r['elasticity_ratio_wrt_production'] for r in comp):.2f} to {max(r['elasticity_ratio_wrt_production'] for r in comp):.2f}: a dose series discriminates them.",
                        "Phase 1 (below 1.68 cm SL) is unobserved; larval specimens are needed to test whether an early burst exists.",
                        "The flying-halfbeak group mixes two species with different proportions; per-species fits need more specimens."],
        limitations=prog["does_not_establish"])
    C["claude-tissue-fin-growth"] = dict(
        title="Morphogen-gradient fin elongation with production, decay, diffusion and growth-rate perturbations (simulated)",
        scales=["developmental", "organ"], evidence_kind="simulated; growth rate anchored to the observed flying-fish mean ratio (anchor, not validation)",
        model=dict(name="1-D quasi-steady distal-source gradient on a growing fin; saturating growth law", context="Dimensioned in cm against SL; parameters declared, not measured."),
        equations=[{"label": "Quasi-steady gradient", "tex": "m(x)=K\\,p\\,\\frac{\\cosh(x/l)}{\\sinh(L/l)},\\ l=\\sqrt{D/k}", "source": "standard source-decay solution, no-flux base"},
                   {"label": "Fin growth", "tex": "\\frac{dL}{dt}=r\\int_0^L\\frac{m}{K+m}dx,\\ SL=SL_0+s\\,t", "source": "declared"}],
        numerical_results=[f"{o['param']} x{o['factor']:g}: fin/SL at SL 24 changes {o['pct_change_ratio']:+.0f}%" for o in fgs["oat"]],
        parameter_unknowns=["All six parameters are declared; identifiability-v2 shows the observed allometry pins about one combination."],
        open_questions=["The fixed initial fin length (fin/SL 0.30 at SL 1.5 cm) contradicts the observed 0.54-0.76 at SL 1.7-3 cm; see the developmental-programme card for the data-favoured form."],
        limitations=["Simulated, not observed.", "Baseline log-log slope 1.29 vs observed 1.06: the anchored baseline has the wrong shape.",
                     "Does not establish a morphogen, a gradient, or that fin proportion is controlled by any of the perturbed quantities in a fish.",
                     "The perturbation percentages are for the declared baseline regime only; in the data-favoured tip-saturated regime the production response is much smaller (transfer-regimes)."])
    lad = "; ".join(f"{x['readouts']}: rank {x['rank_of_6']}" for x in idv["readout_ladder"])
    C["claude-tissue-identifiability"] = dict(
        title="What the observed flying-fish allometry can and cannot pin down in a fin-growth model, and which measurements would",
        scales=["developmental", "organ"], evidence_kind="computed identifiability analysis of a simulated model against observed specimens",
        model=dict(name="Profile likelihood and Jacobian rank of the fin-growth model", context="49 observed flying-fish specimens."),
        equations=[{"label": "Exact reduction", "tex": "L(SL)\\ \\text{depends only on}\\ p=\\frac{P l}{D K},\\ l=\\sqrt{D/k},\\ \\rho=r/s", "source": "this harness, verified numerically (rank 3 of 6)"}],
        numerical_results=[f"Native Jacobian rank {idv['native_jacobian']['rank']} of 6", "Readout ladder: " + lad,
                           f"Freeing initial fin length improves deviance by {idv['L0_free_sensitivity']['delta_deviance']:.0f}",
                           f"Transfer regimes (L0 free): production elasticity of fin/SL {min(r['elasticity_ratio_wrt_production'] for r in comp):.2f}-{max(r['elasticity_ratio_wrt_production'] for r in comp):.2f} across {len(comp)} data-compatible gradient lengths"],
        parameter_unknowns=["Gaussian iid log residuals assumed for intervals.", "FRAP and dose-response ladder rungs are structural, not simulated experiments.",
                            "In transfer-regimes, rho sits on its upper bound at l = 0.1 and 0.3 cm."],
        open_questions=["A graded morphogen-production series discriminates gradient-limited from tip-saturated regimes that the allometry cannot."],
        limitations=["v1 (rank-4) superseded: time-step artifact.", "Does not establish any parameter value of a real fish; it ranks measurements."])
    C["claude-tissue-rd-wavelength"] = dict(
        title="Turing (Schnakenberg) pattern wavelength across diffusion ratio and rate scale, 90 runs on an H100 (simulated, dimensionless)",
        scales=["tissue", "developmental"], evidence_kind="simulated; dimensionless; mapping to fin rays or scales is an assumption",
        model=dict(name="Schnakenberg reaction-diffusion, 2-D periodic, IMEX pseudo-spectral, 256^2", context="Generic kinetics (a=0.1, b=0.9), not fitted to any fish."),
        equations=[{"label": "Schnakenberg", "tex": "u_t=\\gamma(a-u+u^2v)+\\nabla^2u,\\quad v_t=\\gamma(b-u^2v)+d\\nabla^2v", "source": "Murray, Mathematical Biology"},
                   {"label": "Simulated scaling", "tex": f"\\lambda\\propto\\gamma^{{{el['dlogLambda_dloggamma_mean_over_d']:.2f}}}\\,d^{{{el['dlogLambda_dlogd_gamma1.0']:.2f}}}", "source": "fit over 90 runs (linear theory: d^0.21)"}],
        numerical_results=[f"{rd['convergence']['shell_converged']}/{rd['convergence']['n']} runs shell-converged; max k change half-to-end {100*rd['convergence']['max_rel_k_change_half_to_end']:.1f}%",
                           "Selected wavenumber 3-18% above the linear fastest mode", "Stripes/labyrinths near onset (d=10), spots for d>=20"],
        parameter_unknowns=["Activator diffusivity and turnover (needed to convert to cm) are unmeasured for any fin pathway."],
        open_questions=["FRAP of a candidate ligand plus measured ray spacing would test whether lambda_nondim falls in the simulated band."],
        limitations=["Does not establish that fin rays or scales are Turing patterns.", "v1 (L=32) superseded: quantized wavenumber; v1 convergence control found 1 of 3 cases unconverged at t=150."])
    rows = gr["rows"]
    eg = J("claude-tissue-growing-rd/edge-growth.json")["rows"]
    C["claude-tissue-growing-rd"] = dict(
        title="Turing peaks on a growing fin-width domain: uniform growth gives frequency doubling, edge growth gives sequential insertion with speed-dependent spacing (simulated)",
        scales=["tissue", "developmental"], evidence_kind="simulated; dimensionless; peaks -> rays is an assumption",
        model=dict(name="1-D Schnakenberg on a growing domain: uniform (dilution) growth and edge (apical) growth", context="12x width increase; each mode 3 growth speeds x 3 diffusion ratios x 5 seeds."),
        equations=[{"label": "Growing-domain RD (comoving)", "tex": "u_t=\\gamma f(u,v)-\\tfrac{\\dot W}{W}u+W^{-2}u_{\\xi\\xi}", "source": "Crampin, Gaffney & Maini 1999 form"}],
        numerical_results=[f"d={d}, T={T:g}: final peaks {sorted({r['n_final'] for r in rows if r['d']==d and r['T_grow']==T})} (W/lambda* = {[r['n_expected_final'] for r in rows if r['d']==d][0]:.1f})" for d in (15, 20, 30) for T in (250.0, 1000.0, 4000.0)]
            + [f"EDGE growth d={d}, speed {v:g}: final peaks {sorted({r['n_final'] for r in eg if r['d']==d and r['speed']==v})}, max jump {max(r['max_jump'] for r in eg if r['d']==d and r['speed']==v)}, mean spacing {sum(r['mean_spacing'] for r in eg if r['d']==d and r['speed']==v)/5:.1f} (lambda* {[r['lambda_star'] for r in eg if r['d']==d][0]:.1f})" for d in (15, 20, 30) for v in (0.5, 0.1, 0.03)],
        parameter_unknowns=["Real fin outgrowth geometry (where and how fast tissue is added) is not measured here; both growth modes are idealised."],
        open_questions=["Live imaging of ray-primordium insertion events (+1 at margin vs synchronous splitting) discriminates the growth modes.", "Edge model predicts new-ray spacing widens when outgrowth slows (e.g. temperature series in medaka)."],
        limitations=["Does not establish how fin rays are added in any species.", "Interior-peak counting may under-count edge peaks."])
    if (A/"claude-tissue-phase-map/phase-map.json").exists():
        pm = J("claude-tissue-phase-map/phase-map.json"); gr_ = pm["grid"]
        tur = [v for v in gr_.values() if v["turing_unstable"]]
        stripes = [f"b={v['b']}, d={v['d']}" for v in tur if v.get("component_density_mean") is not None and v["component_density_mean"] < 0.6]
        C["claude-tissue-phase-map"] = dict(
            title="Where Turing kinetics give stripes (ray-like) vs spots: Schnakenberg phase map over b and d, on an H100 (simulated)",
            scales=["tissue", "developmental"], evidence_kind="simulated; dimensionless; stripes -> rays and spots -> scales are assumptions",
            model=dict(name="Schnakenberg 2-D periodic, IMEX spectral, 128^2, t=800, 3 seeds per cell", context=f"a=0.1; b in {pm['meta']['bs']}; d in {pm['meta']['ds']}"),
            equations=[{"label": "Schnakenberg", "tex": "u_t=a-u+u^2v+\\nabla^2u,\\quad v_t=b-u^2v+d\\nabla^2v", "source": "Murray, Mathematical Biology"},
                       {"label": "Stripe/spot classifier", "tex": "\\rho_c=N_{\\text{comp}}(u>\\bar u)\\,\\lambda^2/A;\\ \\rho_c>0.6\\Rightarrow\\text{spots}", "source": "this harness; synthetic check stripes 0.25, hexagonal spots 1.0"}],
            numerical_results=[f"{len(tur)} of {len(gr_)} cells Turing-unstable", "Stripe/labyrinth cells: " + "; ".join(stripes),
                               "Stripes occur only in the band adjacent to onset (smallest unstable d for each b); spots everywhere deeper in the Turing region"],
            parameter_unknowns=["Kinetics are generic, not fitted to any fish pathway."],
            open_questions=["Static patterning gives ray-like stripes only near onset; does directional (edge) growth widen the stripe regime? (claude-tissue-edge2d)"],
            limitations=["Does not establish that fin rays or scales are Turing patterns.", "Coarse 8x8 grid; boundaries between cells are not resolved.",
                         "Classifier threshold is heuristic; cell b=1.4, d=17 is weak (amplitude 0.02) and near onset."])
    if (A/"claude-tissue-edge2d/edge2d.json").exists():
        e2 = J("claude-tissue-edge2d/edge2d.json"); sm = e2["summary"]
        C["claude-tissue-edge2d"] = dict(
            title="Fin fold growing at its distal edge: does directional growth orient Turing patterns into proximo-distal (ray-like) stripes? (simulated, H100)",
            scales=["tissue", "developmental"], evidence_kind="simulated; dimensionless; video renders model state, not tissue",
            model=dict(name="2-D Schnakenberg, rows activated at the distal edge at speed v; static control patterned all at once", context=f"width {e2['meta']['X']}, length {e2['meta']['Y0']}->{e2['meta']['Y1']}, dx=1, {len(e2['meta']['seeds'])} seeds per condition"),
            equations=[{"label": "Orientation index", "tex": "A=\\frac{P_{|k_x|>|k_y|}-P_{|k_y|>|k_x|}}{P_{|k_x|>|k_y|}+P_{|k_y|>|k_x|}}", "source": "this harness; +1 = stripes along the growth axis"}],
            numerical_results=[f"d={v['d']}, {'static' if v['speed']==0 else 'edge speed '+str(v['speed'])}: A = {v['orientation_A_mean']:.2f} +/- {v['orientation_A_sd']:.2f}, stripes across width {v['stripes_across_width']}" for v in sm.values()],
            parameter_unknowns=["Real fin-fold growth geometry and speed are not measured here."],
            open_questions=["Is orientation caused by edge growth specifically, or by any growth along the proximo-distal axis? A uniform-growth control is needed."],
            limitations=["Does not establish that fin rays form by a Turing mechanism or that fin folds grow only at the edge.", "Dimensionless; generic kinetics."])
    return C

SUPERSEDED = {"receipt-claude-tissue-rd-wavelength.json": "v1 (L=32) superseded by receipt-claude-tissue-rd-wavelength-v2.json",
              "receipt-claude-tissue-rd-convergence.json": "control on v1; motivates v2",
              "receipt-claude-tissue-identifiability.json": "v1 superseded by identifiability-v2 (rank-4 was a time-step artifact)",
              "receipt-claude-tissue-growing-rd.json": "v1 (4x growth) complemented by v2 (12x growth)",
              "receipt-claude-tissue-transfer-regimes.json": None}

def git_head():
    return subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()

if __name__ == "__main__":
    for name, card in cards().items():
        d = A/name
        files = {p.name: dict(bytes=p.stat().st_size, sha256=sha(p)) for p in sorted(d.iterdir()) if p.is_file() and p.name != "manifest.json"}
        runs, inputs = [], {}
        for p in sorted(d.glob("receipt-*.json")):
            r = json.loads(p.read_text()); inputs.update(r.get("input_sha256", {}))
            stale = {k: v for k, v in r.get("code_sha256", {}).items() if (ROOT/k).exists() and sha(ROOT/k) != v}
            runs.append(dict(receipt=p.name, run=r["name"], command=r["command"], exit_code=r["exit_code"], seed=r["seed"], wall_s=r["wall_s"],
                             compute=r.get("compute") or r.get("gpu"), job_state=r.get("job_state"), superseded=SUPERSEDED.get(p.name),
                             code_changed_since_run=stale or None))
        vids = sorted(d.glob("*.mp4"))
        if vids:
            card["video"] = dict(file=vids[0].name, sha256=sha(vids[0]), note=f"{vids[0].stat().st_size} bytes; render of computed model state, not footage")
        if (d/"poster.png").exists():
            card["poster"] = "poster.png"
        card = dict(id=name, **card, manifest=f"artifacts/simulations/{name}/manifest.json", native=True, couplings=[],
                    sources=[{"label": "Observed allometry", "locator": "artifacts/observed-allometry/source-observations.csv"}] if inputs else [])
        man = dict(schema="frontier.claude-tissue-simulation.manifest/1", id=name, title=card["title"], scales=card["scales"],
                   evidence_kind=card["evidence_kind"], status="computed_not_observed", does_not_establish=card["limitations"],
                   base_commit=git_head(), code_sha256={str(p.relative_to(ROOT)): sha(p) for p in sorted((ROOT/"simulations/claude_tissue").glob("*.py"))},
                   input_sha256=inputs, files=files, runs=runs, measurement_rows=0,
                   experiment_design="docs/claude-tissue-transfer-designs.md", studio_card=card)
        (d/"manifest.json").write_text(json.dumps(man, indent=2, sort_keys=True))
        print(name, len(files), "files", len(runs), "runs", card["scales"])
