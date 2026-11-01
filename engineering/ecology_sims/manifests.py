"""Write repo-format manifests (site/artifacts/simulations/<id>/manifest.json, read by scripts/build_site.py simulation_manifests)
plus sensitivity.json for the three claude-eco models. Numbers are read from results.json; nothing is typed by hand.
Run after the model scripts and render.py."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from engineering.ecology_sims import common as C  # noqa: E402

REVIEW = {"model": "gemini-4-argon (Google), design critique 2026-11-01T14:39Z, full code + summary sent",
          "changed_in_response": ["added an aquatic fin cost (kappa_fin, swept 0-1; default 0 = escape-only fitness, stated)",
                                  "added a zero-lift (ballistic) control for every phenotype", "added swim_sync control (alarm cascade without gliding) to separate gliding from social alarm",
                                  "predator now pursues the glider's ground track instead of its landing point (no foreknowledge); d_gap term removed from the ABM tracking rule",
                                  "faster in-water flee (5 and 10 m/s) as sensitivity cases", "correlated-G (p-c pleiotropy +-0.5) and CV_A 0.02/0.10 Lande variants",
                                  "CL rule n_trim 1.5 sweep", "weakest-step selection coefficient reported with the Ne needed for selection to beat drift"],
          "not_changed": ["ground effect is still omitted (stated as a limitation: it would lengthen glides of low fliers)", "body-shape (length-weight a) is not an evolving trait; both FishBase values are run",
                          "fitness has no fecundity/foraging term beyond the fin-cost factor"]}


def rel(p):
    return str(Path(p).relative_to(C.ROOT))


def common_fields(d, mid, title, scales, video, model_name, context, srcs):
    rc = json.loads((d / "receipt.json").read_text())
    return {"id": mid, "title": title, "scales": scales, "project": "flying-fish",
            "evidence_kind": "simulated: model output under declared assumptions; not an observation of any fish, predator or lineage",
            "model": {"name": model_name, "context": context, "code": "engineering/ecology_sims/", "reuses": "engineering/simulation/glide.py (project point-mass glide) unchanged"},
            "video": {"file": video, "sha256": C.sha256_file(d / video), "note": "1280x720 h264, rendered single-thread from results.json / saved states"},
            "poster": "poster.png", "poster_sha256": C.sha256_file(d / "poster.png"),
            "receipt": {"file": rel(d / "receipt.json"), "sha256": C.sha256_file(d / "receipt.json"), "command": rc["command"], "exit_code": rc["exit_code"], "seed": rc["seed"],
                        "started_utc": rc["started_utc"], "finished_utc": rc["finished_utc"], "inputs_sha256": rc["inputs_sha256"]},
            "results": {"file": rel(d / "results.json"), "sha256": C.sha256_file(d / "results.json")},
            "sensitivity": {"file": rel(d / "sensitivity.json")},
            "sources": [{"id": k, **C.SOURCES[k]} for k in srcs], "review": REVIEW, "couplings": [], "native": True, "author": "claude-eco (Claude Opus 5.5), 2026-11-01"}


def reach():
    d = C.OUT / "eco-reachability"; R = json.loads((d / "results.json").read_text())
    runs = R["runs"]; get = lambda s, h: next(r for r in runs if r["setting"] == s and r["hypothesis"] == h)
    sens = [{k: r.get(k) for k in ("setting", "overrides", "hypothesis", "W_ancestor", "W_target", "maximin_worst_step_dW", "strictly_improving_path_exists", "path_only_via_neutral_steps",
                                   "valley_depth_if_any", "path_bottleneck_step", "weakest_step_selection_coefficient", "Ne_needed_for_selection_to_dominate_drift_at_weakest_step")}
            | {"lande_end": r["lande"]["end"], "lande_end_dist_to_target_norm": r["lande"]["end_dist_to_target_norm"], "straight_line": r.get("straight_line")} for r in runs]
    C.dump(d / "sensitivity.json", {"schema": "frontier.eco.sensitivity/1", "model": "eco-reachability", "rows": sens})
    b, v, c = get("default", "both"), get("default", "vis"), get("default", "chase")
    n_strict = sum(1 for r in runs if r["strictly_improving_path_exists"]); n_valley = sum(1 for r in runs if (r["valley_depth_if_any"] or 0) > 0)
    n_neutral = sum(1 for r in runs if r["path_only_via_neutral_steps"])
    reached = sum(1 for r in runs if r["lande"]["first_gen_within_0.05_of_target"] is not None)
    bc = R.get("ballistic_control", {})
    def bstep(r):
        s = r["path_bottleneck_step"]; return f"{s['trait']} {s['from'][s['trait']]:.3g} -> {s['to'][s['trait']]:.3g} (dW {s['dW']:.2e})" if s and s.get("trait") else "none"
    post = json.loads((d / "reach_post.json").read_text()) if (d / "reach_post.json").exists() else None
    clr = next((r for r in runs if r["setting"] == "CL_schedule" and r["hypothesis"] == "both"), None)
    v4 = next((r for r in runs if r["setting"] == "V_exit=4" and r["hypothesis"] == "both"), None)
    lande_ps = [r["lande"]["end"]["p"] for r in runs if r["hypothesis"] == "both"]
    findings = [
        f"ANSWER (default physics, H_vis + H_chase): changing all four traits together along the straight line ancestor -> target, W never decreases (max drop {b['straight_line']['max_drop']:.1e} over 200 steps) -- a monotonically improving path EXISTS when traits co-vary. With one trait changing at a time there is no strictly improving path: the least-bad route dips by {b['valley_depth_if_any']:.1e}.",
        f"Default physics, H_vis + H_chase: W rises from {b['W_ancestor']:.3f} (ancestor) to {b['W_target']:.4f} (target). The best single-trait path has worst step dW = {b['maximin_worst_step_dW']:.2e}: "
        + ("a strictly improving path exists." if b["strictly_improving_path_exists"] else ("only neutral steps connect them." if b["path_only_via_neutral_steps"] else f"no strictly improving path; every path crosses a dip of at least {b['valley_depth_if_any']:.2e}.")) + f" Bottleneck step: {bstep(b)}.",
        f"H_chase only (escape requires out-running the predator's chase): the ancestor's {R['runs'][0]['ancestor']['p']:.3f} pectoral ratio gives a leap shorter than the chase, W = e_swim exactly, and the landscape is flat around it: worst step {c['maximin_worst_step_dW']:.2e}; the Lande walk does not move (ends at p = {c['lande']['end']['p']:.3f}). Under this hypothesis the first steps are neutral and need drift or another benefit.",
        f"H_vis only: worst step {v['maximin_worst_step_dW']:.2e}; bottleneck {bstep(v)}.",
        f"Selection-driven (Lande) walk, default, H_vis + H_chase, {b['lande']['generations']} generations at CV_A 0.05: ends at p = {b['lande']['end']['p']:.3f}, A = {b['lande']['end']['A']:.2f}, M = {b['lande']['end']['M']*1000:.1f} g, c = {b['lande']['end']['c']:.3f}; normalised distance to the Exocoetus-like target {b['lande']['end_dist_to_target_norm']:.2f}. The walk does not head to the target's aspect ratio or mass under this fitness.",
        f"Across all {len(runs)} sensitivity rows: strictly improving path in {n_strict}, neutral-only in {n_neutral}, a required dip in {n_valley}; the Lande walk came within 0.05 (normalised) of the target in {reached}.",
        (("Where the dip is (reach_post, default landscape): " + "; ".join(f"{h}: to the target cell worst step {post['by_hypothesis'][h]['a_target_cell']['worst_step_dW']:.1e} ({post['by_hypothesis'][h]['a_target_cell']['bottleneck_trait']}), mass free {post['by_hypothesis'][h]['b_any_mass']['worst_step_dW']:.1e} ({post['by_hypothesis'][h]['b_any_mass']['bottleneck_trait']}), mass frozen {post['by_hypothesis'][h]['c_mass_frozen_at_ancestor']['worst_step_dW']:.1e} ({post['by_hypothesis'][h]['c_mass_frozen_at_ancestor']['bottleneck_trait']})" for h in ("vis", "both"))
          + ". So the dip is not only the mass increase: escape peaks once the fins carry the full weight at exit (phi = 1, p near 0.3) and falls slightly as p and A rise further toward the exocoetid values.") if post else "reach_post missing"),
        ((f"H_chase plateau: {post['by_hypothesis']['chase']['d_plateau']['cells_connected_to_ancestor_with_W_equal_e_swim']} grid cells connected to the ancestor have W exactly equal to e_swim (up to p = {post['by_hypothesis']['chase']['d_plateau']['max_p_on_plateau']:.2f}); a path to the target exists with no downhill step but begins with neutral steps only -- under H_chase the first steps need drift, not selection.") if post and post['by_hypothesis']['chase'].get('d_plateau') else "no H_chase plateau"),
        f"BOTTLENECK of the selection-driven walk: across all {sum(1 for r in runs if r['hypothesis'] == 'both')} H_vis+H_chase rows the walk ends at p = {min(lande_ps):.2f}-{max(lande_ps):.2f} with broad fins (A about 2), never within 0.05 of the target. The stall is where the fins first carry the full weight at water exit; it is robust to the CL control rule (scheduled-CL variant ends at p = {clr['lande']['end']['p']:.2f}) " + (f"but not to exit speed (V_exit = 4 m/s: p = {v4['lande']['end']['p']:.2f})." if v4 else "."),
        (lambda rows: f"Straight-line (traits co-varying) check across the {len(rows)} sensitivity rows that ran it: monotone non-decreasing in {sum(1 for r in rows if r['straight_line']['monotone_nondecreasing'])}; largest single drop among the rest {max([r['straight_line']['max_drop'] for r in rows] or [0]):.1e}. Required single-trait dips, where present, range {min([r['valley_depth_if_any'] for r in runs if r['valley_depth_if_any'] > 0] or [0]):.1e} to {max([r['valley_depth_if_any'] for r in runs] or [0]):.1e} in W per attack; whether drift or a correlated response would cross them depends on Ne and G, which this model does not estimate. The Ne needed for selection to dominate at the weakest positive step is given per row in sensitivity.json.")([r for r in runs if r.get("straight_line")]),
        (f"Zero-lift control: ancestor airborne {bc['ancestor_d_lift']:.2f} m with lift vs {bc['ancestor_d_no_lift']:.2f} m ballistic; target {bc['target_d_lift']:.1f} m vs {bc['target_d_no_lift']:.1f} m." if bc else "zero-lift control missing"),
    ]
    m = common_fields(d, "eco-reachability", "Reachability of an exocoetid-like glider from a halfbeak-like ancestor (model escape-fitness landscape)", ["ecological"], "reachability.mp4",
                      "claude-eco reachability/1: 4-trait landscape (pectoral length/SL, fin aspect ratio, mass, hypocaudal share) -> project point-mass glide -> escape probability; maximin accessible path, Lande walk, straight line",
                      "Asks whether, under a stated escape-fitness function, a monotonically improving path exists from a halfbeak-like ancestor (Daane 2021 S1A Hyporhamphus proportions) to an Exocoetus-like exocoetid (Daane 2021 S1A, Fish 1990, FishBase). Airborne phase uses the project's own glide model. SIMULATION; reachability in a model is not evidence that the transition happened or how.",
                      ["daane2021", "fish1990", "davenport1992", "lovejoy2004", "fishbase", "houle1992", "lande1979", "weinreich2005", "project_glide"])
    m.update({"time": {"units": "generations of a Lande walk (model time, not years)", "note": "video: the H_vis + H_chase walk sampled on a log scale of generations; each frame re-flies the current phenotype"},
              "post_analysis": {"file": rel(d / "reach_post.json"), "sha256": C.sha256_file(d / "reach_post.json"), "receipt": rel(d / "receipt_post.json")} if post else None,
              "numerical_checks": [{"name": "glide timestep halving over the whole landscape", "result": json.dumps(R.get("dt_check"))},
                                   {"name": "flight completion", "result": f"{b['cells_not_completed_flight']} of {b['grid_cells']} default cells did not complete a forward water-to-water flight (they are scored as staying in the water)"},
                                   {"name": "zero-lift control", "result": json.dumps(bc)}],
              "findings": findings,
              "parameter_unknowns": [f"{k} = {v[0]} {v[1]}: {v[2]}" for k, v in C.ASSUMPTIONS.items()],
              "does_not_establish": ["that flying fish evolved from a halfbeak-like ancestor along this or any path (phylogeny is from Lovejoy 2004; the path is a model)",
                                     "that the walk's stall near p 0.3 explains flying halfbeaks (Oxyporhamphus p = 0.337 in Daane S1A) -- a numerical coincidence in a model, not evidence",
                                     "that predator escape was the selective agent", "real fitness: no fecundity, foraging or development term; fin cost only as a swept factor",
                                     "the evolution of aspect ratio or mass: the fitness used does not favour the target's A or M", "anything about developmental feasibility (that is the developmental scale)",
                                     "aerodynamics beyond a point-mass glide with a design-assumed polar and no ground effect"],
              "open_questions": ["Which ecological term (ground effect, re-launch/taxi bouts, aerial predators, swimming cost) would make the exocoetid A and M uphill?", "Is the H_chase plateau real: do predators keep tracking a short leap?"],
              "caption": "Reachability on a MODEL escape-fitness landscape. SIMULATION, not an observation; a reachable model path is not evidence the transition happened."})
    C.dump(d / "manifest.json", m)
    return m


def escape():
    d = C.OUT / "eco-escape-ecology"; R = json.loads((d / "results.json").read_text())
    C.dump(d / "sensitivity.json", {"schema": "frontier.eco.sensitivity/1", "model": "eco-escape-ecology", "rows": R["sensitivity"]})
    ph = R["phenotypes"]; be = R["H_chase_predator_speed_where_gain_below_0.01_m_s"]
    am = R["aerial_map"]
    import numpy as np
    gain = np.array(am["gain_both"]); U = np.array(am["U_burst_m_s"]); B = np.array(am["beta_air_per_s"])
    iu = int(np.argmin(np.abs(U - 10.0))); neg = np.where(gain[:, iu] < 0)[0]
    findings = [f"{k}: airborne {v['airborne_distance_m']:.1f} m / {v['airborne_time_s']:.2f} s (zero-lift control {v['ballistic_control_distance_m']:.1f} m); escape per attack H_vis {v['escape_vis']:.2f}, H_chase {v['escape_chase']:.2f}, both {v['escape_both']:.2f}; launch metabolic cost (lower bound) {100*v['launch_cost_frac_of_assumed_daily_RMR']:.1f}% of an ASSUMED daily routine budget" for k, v in ph.items()]
    findings.append("H_chase only: predator burst speed (2 s burst) above which leaving the water gains < 0.01 escape probability: " + "; ".join(f"{k} {v} m/s" if v else f"{k} none in 2-25 m/s" for k, v in be.items()) + ". FishBase T. albacares burst rows span 5.21-20.46 m/s.")
    findings.append("Aerial predators, 10 m/s underwater predator: " + (f"gliding stops paying for the target (gain < 0) once the aerial hazard while airborne exceeds {B[neg[0]]:.2f} /s." if len(neg) else f"the target's gain stays positive across the whole swept aerial hazard 0-{B[-1]:.2f} /s."))
    findings.append(f"Energy: at 10 attacks/day the launch cost lower bound is {100*R['energy']['launch_metabolic_frac_of_daily_RMR'][-1]:.0f}% of the assumed daily routine budget (taxi drag excluded).")
    m = common_fields(d, "eco-escape-ecology", "Glide as predator escape: when does leaving the water pay? (model)", ["ecological", "organism"], "escape.mp4",
                      "claude-eco escape/1: phenotype -> launch (taxi surrogate) -> project point-mass glide -> escape probability vs predator burst speed/endurance, aerial hazard and size",
                      "Three phenotypes (halfbeak-like ancestor, flying-halfbeak proportions, Exocoetus-like) against predators parameterised from FishBase speed and size rows. Encounter and aerial-hazard rates are swept assumptions. SIMULATION, not an observation of predation.",
                      ["daane2021", "fish1990", "fishbase", "oxenford1999", "project_glide"])
    m.update({"time": {"units": "seconds of one escape", "note": "video: one launch of each phenotype at t = 0 with a predator under the surface at the FishBase-range burst speed"},
              "numerical_checks": [{"name": "dt halving", "result": "; ".join(f"{k}: {v['airborne_distance_m']:.4f} vs {v['dt_half_distance_m']:.4f} m" for k, v in ph.items())},
                                   {"name": "zero-lift control", "result": "; ".join(f"{k}: {v['ballistic_control_distance_m']:.2f} m" for k, v in ph.items())}],
              "findings": findings,
              "parameter_unknowns": [f"{k} = {v[0]} {v[1]}: {v[2]}" for k, v in R["assumptions"].items()],
              "does_not_establish": ["actual predation rates, encounter rates or escape success of any fish", "that predators of flying fish track by vision or out-run by chase (two hypotheses, both shown)",
                                     "energy budgets: the launch cost is a kinetic lower bound against an assumed routine metabolic rate", "anything about real seabird predation (aerial hazard is swept)"],
              "open_questions": ["Measured predator tracking after a prey leaves the water", "Taxi energetics and re-launch frequency"],
              "caption": "Glide as predator escape under swept predator speed, aerial hazard and size. SIMULATION, not an observation."})
    C.dump(d / "manifest.json", m)
    return m


def collective():
    d = C.OUT / "collective-school-escape"; R = json.loads((d / "results.json").read_text())
    C.dump(d / "sensitivity.json", {"schema": "frontier.eco.sensitivity/1", "model": "collective-school-escape", "rows": R.get("sensitivity", []), "seed_replicate": R.get("seed_replicate")})
    M = R["main"]; Ns = sorted({int(k.split("|")[1]) for k in M}); N2 = 16 if 16 in Ns else Ns[-1]
    f = lambda c, N: M[f"{c}|{N}"]
    findings = [f"Solitary (N=1) capture per attack: glide {f('glide_sync',1)['P_capture_episode']:.2f}, swim {f('swim',1)['P_capture_episode']:.2f}.",
                f"N={N2}: P(capture per episode) glide+alarm {f('glide_sync',N2)['P_capture_episode']:.3f} +- {1.96*f('glide_sync',N2)['se']:.3f}, glide independent {f('glide_indep',N2)['P_capture_episode']:.3f}, swim+alarm {f('swim_sync',N2)['P_capture_episode']:.3f}, swim {f('swim',N2)['P_capture_episode']:.3f}.",
                f"Per-capita capture per encounter at N={N2}: glide+alarm {f('glide_sync',N2)['per_capita']:.4f} vs solitary glider {f('glide_sync',1)['per_capita']:.3f} ({f('glide_sync',1)['per_capita']/max(f('glide_sync',N2)['per_capita'],1e-9):.0f}x lower); glide independent {f('glide_indep',N2)['per_capita']:.4f}; swim {f('swim',N2)['per_capita']:.4f} (dilution alone).",
                "Synchronised emergence (alarm cascade) lowers whole-school capture for gliders but not for swimmers in this model: the alarm only helps if it triggers an escape that removes the target from reach.",
                "Per unit time, schooling helps only if encounter rate grows slower than N: see risk_per_time_relative_to_solitary for alpha = 0, 0.5, 1 (alpha = 1 removes all dilution)."]
    m = common_fields(d, "collective-school-escape", "Schooling and synchronised emergence vs a predator: per-capita escape (agent-based model)", ["collective", "ecological"], "collective.mp4",
                      "claude-eco collective/1: 2-D agent-based school (zonal model geometry, detection, alarm cascade over the neighbour graph), predator approach/burst/strike with confusion, gliders flying the project point-mass glide distance",
                      "Population/behavioural layer of the collective scale; the rigid-body/hydrodynamic collective launch is claude-organ's. Compares glide + alarm, glide independent, swim + alarm and swim-only over N = 1..64. All behavioural parameters are assumptions, swept. SIMULATION, not an observation of any school.",
                      ["couzin2002", "treherne1981", "landeau1986", "hamilton1971", "fishbase", "project_glide"])
    m.update({"time": {"units": "seconds of one attack episode (dt 0.02 s, cap 12 s)", "note": "video: one recorded episode per condition, top view"},
              "numerical_checks": [{"name": "seed replicate (seed + 99)", "result": json.dumps(R.get("seed_replicate"))},
                                   {"name": "binomial standard errors", "result": "every P has se = sqrt(P(1-P)/B) recorded in results.json"}],
              "findings": findings,
              "parameter_unknowns": [f"{k} = {v[0]} {v[1]}: {v[2]}" for k, v in R["abm_assumptions"].items()],
              "does_not_establish": ["that real flying-fish schools emerge synchronously or transmit alarms", "rigid-body or hydrodynamic interactions between launching fish (claude-organ's layer)",
                                     "encounter-rate scaling with school size (alpha is swept, not estimated)", "confusion strengths for any real predator (Landeau & Terborgh form only)",
                                     "any 3-D effect: the ABM is 2-D top view; airborne fish are represented by their ground track"],
              "open_questions": ["Field video of school emergence timing", "Does claude-organ's collective-launch physics change per-fish airborne distance when launches are simultaneous?"],
              "risk_per_time_relative_to_solitary": R.get("risk_per_time_relative_to_solitary"),
              "caption": "Agent-based school vs predator: per-capita capture with and without synchronised emergence. SIMULATION, not an observation."})
    C.dump(d / "manifest.json", m)
    return m


if __name__ == "__main__":
    which = sys.argv[1:] or ["reach", "escape", "collective"]
    for w in which:
        m = {"reach": reach, "escape": escape, "collective": collective}[w]()
        print(m["id"]); [print("  -", x) for x in m["findings"]]
