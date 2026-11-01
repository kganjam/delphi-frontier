"""Turn a collected Nebius job (artifacts/neuro/jobs/<name>/collected/) into a repo-format run: manifest.json, run_receipt.json,
figure.png and the raw result file, under artifacts/neuro/<rid>/. Numbers are read from the returned files only.

    python -m engineering.neuro.postprocess j1|j2|j3
"""
from __future__ import annotations
import gzip, json, shutil, sys, time
from pathlib import Path
import numpy as np

from engineering.neuro import common as C

JOBS = {"j8": ("claude-neuro-j8-m5-design-fair-a1", "j8-m5-design-fair", "out/m5_design_fair.json.gz"),
        "j7": ("claude-neuro-j7-m3-atlas-refined-a1", "j7-m3-atlas-refined", "out/m3_atlas.json.gz"),
        "j5": ("claude-neuro-j5-m1-m5prior-a1", "m1-fast-start-m5prior", "out/m1-fast-start-m5prior/manifest.json"),
        "j6": ("claude-neuro-j6-m5-design-a1", "j6-m5-design", "out/m5_design.json.gz"),
        "j4": ("claude-neuro-j4-m3-sobol-a1", "j4-m3-sobol", "out/sobol_m3.json.gz"),
        "j1": ("claude-neuro-j1-m1-sobol-a1", "j1-m1-sobol", "out/sobol_m1.json"),
        "j2": ("claude-neuro-j2-m3-atlas-a2", "j2-m3-atlas", "out/m3_atlas.json.gz"),
        "j3": ("claude-neuro-j3-m5-mcell-a2", "j3-m5-mcell", "out/m5_mcell.json.gz")}


def load(p):
    return json.load(gzip.open(p, "rt")) if str(p).endswith(".gz") else json.load(open(p))


def receipt_and_dirs(key):
    name, rid, res = JOBS[key]
    col = C.OUT / "jobs" / name / "collected"; cr = json.loads((col / "collection_receipt.json").read_text())
    dst = C.OUT / rid; dst.mkdir(parents=True, exist_ok=True)
    shutil.copy(col / res, dst / Path(res).name)
    for f in ("stdout.log", "stderr.log"):
        if (col / "out" / f).exists():
            shutil.copy(col / "out" / f, dst / f"job_{f}")
    return name, rid, cr, col, dst, load(col / res)


def write(dst, rid, manifest, cr, name):
    manifest["outputs"] = {f.name: C.sha(f) for f in sorted(dst.glob("*")) if f.suffix in (".json", ".gz", ".png", ".log") and f.name not in ("manifest.json", "run_receipt.json")}
    C.dump(dst / "manifest.json", manifest)
    rr = {"command": manifest["command"], "python_module": manifest["python_module"], "exit_code": int(cr["container_rc"]), "where": "Nebius AI job " + name + " (" + cr["job_id"] + ")",
          "platform": cr["submission"]["spec"]["platform"] + " " + cr["submission"]["spec"]["preset"], "archive_sha256": cr["archive_sha256"],
          "collected_utc": cr["collected_utc"], "submitted_utc": cr["submission"]["submitted_utc"], "manifest_sha256": C.sha(dst / "manifest.json"),
          "collection_receipt": f"artifacts/neuro/jobs/{name}/collected/collection_receipt.json"}
    (dst / "run_receipt.json").write_text(json.dumps(rr, indent=1))
    print(json.dumps({"rid": rid, "exit_code": rr["exit_code"], "all_checks_pass": manifest["all_checks_pass"]}))


def base_manifest(rid, name, cr, R, title, also, mod, cmd):
    return {"schema": "frontier.neuro.manifest/1", "id": rid, "project": "flying-fish", "project_scale": "neural", "also_scales": also, "evidence_kind": "simulated, not observed",
            "title": title, "command": cmd, "python_module": mod, "seed": 20261101, "nebius_job": {"name": name, "id": cr["job_id"], "spec": cr["submission"]["spec"]},
            "injected_sources": cr["submission"]["injected"], "bundle_sha256": cr["submission"].get("bundle_tar_xz_sha256"), "git_head_at_submit": cr["submission"]["git_head"],
            "env": R.get("env"), "elapsed_s": R.get("elapsed_s"), "checks": R["checks"], "all_checks_pass": R["all_checks_pass"], "ran": {"utc": cr["collected_utc"]}}


def j1():
    name, rid, cr, col, dst, R = receipt_and_dirs("j1")
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    outs = [("predator", "caught"), ("kinematic", "U_emerge"), ("kinematic", "t_emerge_after_command"), ("kinematic", "V_taxi_end"), ("kinematic", "takeoff"), ("kinematic", "gamma_emerge")]
    fig, ax = plt.subplots(2, 3, figsize=(17, 9)); summ = {}
    for a_, (sc, o) in zip(ax.ravel(), outs):
        d = R["scenarios"][sc]["outputs"][o]; ST = d["ST"]; S1 = d["S1"]; top = sorted(ST, key=lambda k: -ST[k])[:10]
        ci = np.array([d["ST_ci95"][k] for k in top]); y = np.arange(len(top))[::-1]
        a_.barh(y, [ST[k] for k in top], xerr=[np.array([ST[k] for k in top]) - ci[:, 0], ci[:, 1] - np.array([ST[k] for k in top])], color="C0", alpha=.7, label="total ST (95% bootstrap)")
        a_.barh(y, [max(S1[k], 0) for k in top], height=.4, color="C3", label="first order S1")
        a_.set_yticks(y, top, fontsize=8); a_.set_xlim(0, 1.05); a_.set_title(f"{sc}: {o} (mean {d['mean']:.3g})", fontsize=9); a_.legend(fontsize=7)
        summ[f"{sc}:{o}"] = {"mean": d["mean"], "top_ST": [[k, round(ST[k], 4), [round(x, 4) for x in d["ST_ci95"][k]], round(S1[k], 4)] for k in top[:6]], "nonfinite_rows_set_to_0": d["nonfinite_rows_set_to_0"]}
    fig.suptitle(f"J1 Sobol sensitivity of M1 (N {R['N']}, {R['runs_per_scenario']} runs per scenario; SIMULATED: ranks model priors, measures nothing)", fontsize=11)
    fig.tight_layout(); fig.savefig(dst / "figure.png", dpi=100); plt.close(fig)
    m = base_manifest(rid, name, cr, R, "Global (Sobol) sensitivity of the escape-to-launch model: which unknowns to measure first", ["organism"], "engineering.neuro.sobol_m1",
                      cr["submission"]["spec"]["command"])
    m["summary"] = summ | {"kinematic_emerged_fraction": R["scenarios"]["kinematic"].get("emerged_fraction"), "runs_per_scenario": R["runs_per_scenario"], "N": R["N"], "d": R["d"]}
    write(dst, rid, m, cr, name)


def j2(key="j2"):
    name, rid, cr, col, dst, R = receipt_and_dirs(key)
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    gr = R["grids"]; lat = R["airframes"]["lateral"]; lon = R["airframes"]["longitudinal"]; mc = R["mc"]
    def F(kind, pred):
        return [r for r in mc[kind] if pred(r)]
    fig, ax = plt.subplots(2, 3, figsize=(17, 9.5)); summ = {}
    for col_i, (gust, sens, ta, trr) in enumerate(((1.0, "vision", 0.06, 0.01), (2.0, "vision", 0.06, 0.01), (2.0, "rate_only", 0.0, 0.01))):
        Z = np.full((len(gr["k_v"]), len(gr["dihedral"])), np.nan)
        for r in F("lateral", lambda r: r["sensor"] == sens and r["gust_sd_ms"] == gust and abs(r["delay_att_s"] - ta) < 1e-9 and abs(r["delay_rate_s"] - trr) < 1e-9):
            f = lat[r["airframe"]]
            if f["m"] == 0.025:
                Z[gr["k_v"].index(f["k_v"]), gr["dihedral"].index(f["dihedral"])] = r["fail_frac"]
        im = ax[0, col_i].imshow(Z, origin="lower", aspect="auto", vmin=0, vmax=1, cmap="magma_r"); plt.colorbar(im, ax=ax[0, col_i], label="P(|bank| > 45 deg in 5 s)")
        ax[0, col_i].set_xticks(range(len(gr["dihedral"])), gr["dihedral"]); ax[0, col_i].set_yticks(range(len(gr["k_v"])), gr["k_v"])
        ax[0, col_i].set_xlabel("pectoral dihedral (deg)"); ax[0, col_i].set_ylabel("caudal vertical-surface fraction k_v")
        ax[0, col_i].set_title(f"25 g, {sens}, gust {gust} m/s, delays {int(ta*1e3)}/{int(trr*1e3)} ms", fontsize=9)
        summ[f"lat_25g_{sens}_g{gust}"] = {"min_fail": float(np.nanmin(Z)), "argmin": [gr["k_v"][int(np.nanargmin(Z) // Z.shape[1])], gr["dihedral"][int(np.nanargmin(Z) % Z.shape[1])]], "max_fail": float(np.nanmax(Z)), "baseline_kv0.15_G7": float(Z[gr["k_v"].index(0.15), gr["dihedral"].index(7)])}
    # failure vs vision delay at baseline and at the best airframe, gust 2
    base = next(i for i, f in enumerate(lat) if f["m"] == 0.025 and f["dihedral"] == 7 and f["k_v"] == 0.15)
    for tc, ls in ((0.0, "-"), (0.01, "--"), (0.03, ":"), (0.06, "-.")):
        rows = sorted(F("lateral", lambda r: r["airframe"] == base and r["sensor"] == "vision" and r["gust_sd_ms"] == 2.0 and abs(r["delay_rate_s"] - tc) < 1e-9), key=lambda r: r["delay_att_s"])
        ax[1, 0].plot([r["delay_att_s"] * 1e3 for r in rows], [r["fail_frac"] for r in rows], ls, marker="o", label=f"canal delay {int(tc*1e3)} ms")
    ax[1, 0].set_xlabel("vision bank delay (ms)"); ax[1, 0].set_ylabel("P(fail), gust 2 m/s"); ax[1, 0].legend(fontsize=8); ax[1, 0].set_title("baseline airframe (25 g, 7 deg, k_v 0.15)", fontsize=9)
    # longitudinal: fail vs SM for passive and vision
    for sens, mk in (("passive", "x-"), ("vision", "o-"), ("otolith", "s--")):
        for gust in (1.0, 2.0):
            rows = [r for r in F("longitudinal", lambda r: r["sensor"] == sens and r["gust_sd_ms"] == gust and (sens == "passive" or (abs(r["delay_rate_s"] - 0.01) < 1e-9 and (sens == "otolith" or abs(r["delay_att_s"] - 0.06) < 1e-9)))) if lon[r["airframe"]]["m"] == 0.025]
            rows.sort(key=lambda r: lon[r["airframe"]]["sm"])
            ax[1, 1].plot([lon[r["airframe"]]["sm"] * 100 for r in rows], [r["fail_frac"] for r in rows], mk, label=f"{sens} gust {gust}")
    ax[1, 1].axvline(8, color="g", ls=":"); ax[1, 1].set_xlabel("static margin (% MAC)"); ax[1, 1].set_ylabel("P(|pitch| > 30 deg in 5 s)"); ax[1, 1].legend(fontsize=7); ax[1, 1].set_title("pitch, 25 g", fontsize=9)
    # linear: fraction of lateral airframes stable vs canal delay (vision 60 ms, gain 1) and otolith
    lin = R["linear"]
    for sens, mk in (("vis", "o-"), ("oto", "s--")):
        fr = []
        for tc in gr["lin_tc"]:
            rr = [x for x in lin if x["kind"] == "lateral" and x["sensor"] == sens and x["gain"] == 1.0 and abs(x["tc"] - tc) < 1e-9 and (sens == "oto" or abs(x["tv"] - 0.06) < 1e-9)]
            fr.append(np.mean([x["radius"] < 1 for x in rr]) if rr else np.nan)
        ax[1, 2].plot(np.array(gr["lin_tc"]) * 1e3, fr, mk, label={"vis": "vision 60 ms + canal", "oto": "otolith + canal"}[sens])
        summ[f"lin_lateral_stable_fraction_{sens}"] = dict(zip([str(t) for t in gr["lin_tc"]], [None if not np.isfinite(v) else float(v) for v in fr]))
    ax[1, 2].set_xlabel("canal (vestibular) delay (ms)"); ax[1, 2].set_ylabel("fraction of 112 lateral airframes stable (exact linear)"); ax[1, 2].legend(fontsize=8); ax[1, 2].set_title("linear atlas, gain 1", fontsize=9)
    fig.suptitle(f"J2 M3 design-space atlas: {R['mc_trajectories']:,} saturation Monte Carlo trajectories ({R.get('gpu')}) + {len(lin):,} exact linear radii; SIMULATED", fontsize=11)
    fig.tight_layout(); fig.savefig(dst / "figure.png", dpi=100); plt.close(fig)
    title = ("Glide stabiliser design-space atlas: failure probability and exact delayed stability over every r3-daane variant" if key == "j2" else
             "Refined print-tolerance atlas around the recommended r3-daane change (dihedral 0-7 deg, caudal fraction 0.10-0.25, 25-35 g, gusts to 3 m/s)")
    m = base_manifest(rid, name, cr, R, title, ["organ", "organism"],
                      "engineering.neuro.m3_atlas", cr["submission"]["spec"]["command"])
    m["integration_note"] = ("The Monte Carlo loop applies the actuator state updated in the same 2 ms step (the same order as glide_stab.mc, which the committed "
                             "CPU rows used and which control 3 compares against statistically). The exact linear radius applies the previous step's actuator state. "
                             "The MC therefore has one step (2 ms) less effective fin lag than the linear atlas. Control 1 checks the linear ordering only.")
    m["summary"] = summ | {"mc_trajectories": R["mc_trajectories"], "mc_elapsed_s": R["mc_elapsed_s"], "linear_radii": len(lin), "linear_elapsed_s": R["linear_elapsed_s"], "gpu": R.get("gpu"), "n_mc": R["n_mc"]}
    write(dst, rid, m, cr, name)


def j3():
    name, rid, cr, col, dst, R = receipt_and_dirs("j3")
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(2, 3, figsize=(17, 9)); summ = {}
    encs = list(R["encoders"])
    x = np.arange(4); w = 0.25
    for i, e in enumerate(encs):
        fr = R["encoders"][e]["fraction"]; ax[0, 0].bar(x + (i - 1) * w, [fr["C1"], fr["C2"], fr["C3"], fr["C123"]], w, label=e)
        summ[e] = {"fraction": fr, "n_C123": R["encoders"][e]["n_consistent_C123"], "n_C1234": R["encoders"][e]["n_consistent_C1234"],
                   "response_angle_deg": R["encoders"][e]["consistent_response_angle_deg"], "latency_s_by_lv": R["encoders"][e]["consistent_latency_s_by_lv"]}
    ax[0, 0].set_xticks(x, ["C1 p", "C2 angle-invariant", "C3 latency rises", "C1&C2&C3"]); ax[0, 0].set_yscale("log"); ax[0, 0].legend(); ax[0, 0].set_title("fraction of parameter space meeting each criterion", fontsize=9)
    for i, e in enumerate(encs):
        ps = R["encoders"][e]["per_set"]; a1 = np.array(ps["ang_lv10"], float); a2 = np.array(ps["ang_lv240"], float)
        ax[0, 1].scatter(a1, a2, s=2, alpha=.3, label=e)
    ax[0, 1].plot([0, 90], [0, 90], "k-"); ax[0, 1].set_xlabel("response angle at l/v 10 ms (deg)"); ax[0, 1].set_ylabel("at l/v 240 ms (deg)"); ax[0, 1].legend(markerscale=5); ax[0, 1].set_title("angle invariance (C2: within 10 deg of the diagonal)", fontsize=9)
    for i, e in enumerate(encs):
        L = R["encoders"][e]["consistent_latency_s_by_lv"]
        if all(L[str(lv)].get("n") for lv in R["lv_s"]):
            ax[0, 2].errorbar(np.array(R["lv_s"]) * 1e3, [L[str(lv)]["q50"] for lv in R["lv_s"]], yerr=[[L[str(lv)]["q50"] - L[str(lv)]["q25"] for lv in R["lv_s"]], [L[str(lv)]["q75"] - L[str(lv)]["q50"] for lv in R["lv_s"]]], marker="o", label=e)
    ax[0, 2].axhspan(0.142, 0.716, color="g", alpha=.1, label="Preuss 2006 mean latencies"); ax[0, 2].set_xlabel("l/v (ms)"); ax[0, 2].set_ylabel("latency from onset (s), consistent sets"); ax[0, 2].legend(fontsize=8)
    for k_i, k in enumerate(["gI_over_gE", "sigma", "beta_per_rad"]):
        for e in encs:
            mp = R["encoders"][e]["all_params_marginal_pass_rate"][k]; ed = np.array(mp["bin_edges"]); c = 0.5 * (ed[1:] + ed[:-1])
            ax[1, k_i].plot(c, [np.nan if v is None else v for v in mp["C123_rate"]], "o-", label=e)
        ax[1, k_i].set_xlabel(k); ax[1, k_i].set_ylabel("P(C1&C2&C3) in bin"); ax[1, k_i].legend(fontsize=8)
    fig.suptitle(f"J3 M5 LIF Mauthner cell x looming encoders ({R['sets']} sets x 7 l/v x {R['trials']} trials per encoder, {R.get('gpu')}); SIMULATED", fontsize=11)
    fig.tight_layout(); fig.savefig(dst / "figure.png", dpi=100); plt.close(fig)
    m = base_manifest(rid, name, cr, R, "Spiking Mauthner-cell decision model: which looming encoding with feedforward inhibition reproduces measured escape signatures", ["organism"],
                      "engineering.neuro.m5_mcell", cr["submission"]["spec"]["command"])
    m["summary"] = summ | {"sweep_elapsed_s": R["sweep_elapsed_s"], "gpu": R.get("gpu"), "criteria": "C1 p in [0.70,0.91]; C2 |angle(240)-angle(10)| <= 10 deg; C3 Spearman(latency, l/v) >= 0.9; C4 loose mean latency in [142,716] ms"}
    write(dst, rid, m, cr, name)


def j4():
    name, rid, cr, col, dst, R = receipt_and_dirs("j4")
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 3, figsize=(18, 6)); summ = {}
    for a_, o in zip(ax, ("fail_prob", "linear_unstable", "log_radius")):
        d = R["outputs"][o]; ST, S1 = d["ST"], d["S1"]; top = sorted(ST, key=lambda k: -ST[k]); y = np.arange(len(top))[::-1]
        ci = np.array([d["ST_ci95"][k] for k in top]); st = np.array([ST[k] for k in top])
        a_.barh(y, st, xerr=[st - ci[:, 0], ci[:, 1] - st], color="C0", alpha=.7, label="total ST (95% bootstrap)")
        a_.barh(y, [max(S1[k], 0) for k in top], height=.4, color="C3", label="first order S1"); a_.set_yticks(y, top, fontsize=8); a_.set_xlim(0, 1.05)
        a_.set_title(f"{o} (mean {d['mean']:.3g})" + (f"; MC noise share {d['mc_noise_share_of_variance']:.3f}" if "mc_noise_share_of_variance" in d else ""), fontsize=9); a_.legend(fontsize=7)
        summ[o] = {"mean": d["mean"], "top_ST": [[k, round(ST[k], 4), [round(x, 4) for x in d["ST_ci95"][k]], round(S1[k], 4)] for k in top[:6]]} | ({"mc_noise_share_of_variance": d["mc_noise_share_of_variance"]} if "mc_noise_share_of_variance" in d else {})
    fig.suptitle(f"J4 Sobol sensitivity of glide roll stabilisation ({R['points']:,} points x {R['trials']} trajectories, {R.get('gpu')}); SIMULATED", fontsize=11)
    fig.tight_layout(); fig.savefig(dst / "figure.png", dpi=100); plt.close(fig)
    m = base_manifest(rid, name, cr, R, "Global sensitivity of glide roll stabilisation: design vs neural vs fin-muscle vs environment parameters", ["organ", "organism"],
                      "engineering.neuro.sobol_m3", cr["submission"]["spec"]["command"])
    m["summary"] = summ | {"linear_vs_mc_agreement": R["linear_vs_mc_agreement"], "points": R["points"], "trials": R["trials"], "elapsed": R["elapsed"], "gpu": R.get("gpu")}
    write(dst, rid, m, cr, name)


def j5():
    """M1 rerun inside the job: its own manifest/results/figure are copied unchanged; run_receipt wraps the job; a comparison file is added."""
    name, rid, res = JOBS["j5"]; col = C.OUT / "jobs" / name / "collected"; cr = json.loads((col / "collection_receipt.json").read_text())
    src = col / "out" / rid; dst = C.OUT / rid; dst.mkdir(parents=True, exist_ok=True)
    for f in src.iterdir():
        shutil.copy(f, dst / f.name)
    for f in ("stdout.log", "stderr.log"):
        if (col / "out" / f).exists():
            shutil.copy(col / "out" / f, dst / f"job_{f}")
    m = json.loads((dst / "manifest.json").read_text()); b = json.loads((C.OUT / "m1-fast-start" / "manifest.json").read_text())["summary"]; s_ = m["summary"]
    keys = ["P_caught", "P_emerge"]; cmp = {k: {"baseline_assumed_priors": b[k], "m5_priors": s_[k]} for k in keys}
    cmp["U_emerge_median"] = {"baseline_assumed_priors": b["U_emerge_ms"]["q50"], "m5_priors": s_["U_emerge_ms"]["q50"]}
    cmp["t_go_median_s"] = {"baseline_assumed_priors": b["t_go_s"]["q50"], "m5_priors": s_["t_go_s"]["q50"]}
    for t in ("taxi_pes", "taxi_opt"):
        cmp[f"{t}_P_takeoff"] = {"baseline_assumed_priors": b[t]["P_takeoff"], "m5_priors": s_[t]["P_takeoff"]}
    (dst / "comparison_with_assumed_priors.json").write_text(json.dumps({"note": "Same seed and code; only theta_thr_deg and lat_M_ms priors differ (from M5/J3). Simulated.", "comparison": cmp, "prior_overrides": m.get("prior_overrides")}, indent=1))
    rr = {"command": cr["submission"]["spec"]["command"], "python_module": "engineering.neuro.fast_start", "exit_code": int(cr["container_rc"]), "where": f"Nebius AI job {name} ({cr['job_id']})",
          "platform": cr["submission"]["spec"]["platform"] + " " + cr["submission"]["spec"]["preset"], "archive_sha256": cr["archive_sha256"], "collected_utc": cr["collected_utc"],
          "manifest_sha256": C.sha(dst / "manifest.json"), "collection_receipt": f"artifacts/neuro/jobs/{name}/collected/collection_receipt.json"}
    (dst / "run_receipt.json").write_text(json.dumps(rr, indent=1)); print(json.dumps({"rid": rid, "exit_code": rr["exit_code"], "all_checks_pass": m["all_checks_pass"], "comparison": cmp}, default=str))


def j6():
    name, rid, cr, col, dst, R = receipt_and_dirs("j6")
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 3, figsize=(17, 5.5)); summ = {"discrimination_accuracy": R["discrimination_accuracy"]}
    for pk, acc in R["discrimination_accuracy"].items():
        ns = sorted(int(n) for n in acc); ax[0].plot(ns, [acc[str(n)] for n in ns], "o-", label=pk)
    ax[0].axhline(1 / 3, color="k", ls=":", label="chance"); ax[0].set_xscale("log", base=2); ax[0].set_xlabel("fish per encoder hypothesis (one parameter set each)"); ax[0].set_ylabel("encoder classification accuracy")
    ax[0].legend(fontsize=8); ax[0].set_title("discriminability by protocol", fontsize=9)
    for k_i, (pk, key, lab) in enumerate((("P_wide", "angle_deg_q10_50_90", "response angle (deg)"), ("P_wide", "latency_s_q10_50_90", "latency from onset (s)"))):
        lv = np.array(R["protocols"][pk]["lv_s"]) * 1e3
        for e, v in R["encoders"].items():
            Q = np.array([[np.nan if x is None else x for x in row] for row in v["protocols"][pk][key]], float)
            ax[k_i + 1].plot(lv, Q[:, 1], "o-", label=e); ax[k_i + 1].fill_between(lv, Q[:, 0], Q[:, 2], alpha=.15)
        ax[k_i + 1].set_xscale("log"); ax[k_i + 1].set_xlabel("l/v (ms)"); ax[k_i + 1].set_ylabel(lab); ax[k_i + 1].legend(fontsize=8)
        ax[k_i + 1].set_title(f"{pk}: median and 10-90% over consistent sets", fontsize=9)
    for e, v in R["encoders"].items():
        summ[e] = {"n_consistent_sets": v["n_consistent_sets"], "angle_slope_deg_per_log2_lv": {pk: v["protocols"][pk]["angle_slope_deg_per_log2_lv"] for pk in v["protocols"]}}
    fig.suptitle(f"J6 M5 experiment design: protocols x encoders ({R.get('gpu')}); SIMULATED sizing of a real experiment", fontsize=11)
    fig.tight_layout(); fig.savefig(dst / "figure.png", dpi=100); plt.close(fig)
    m = base_manifest(rid, name, cr, R, "Looming-protocol design: how many fish and which l/v range would discriminate Mauthner-cell encoding hypotheses", ["organism"],
                      "engineering.neuro.m5_design", cr["submission"]["spec"]["command"])
    m["summary"] = summ; write(dst, rid, m, cr, name)


def j8():
    name, rid, cr, col, dst, R = receipt_and_dirs("j8")
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(7.5, 5))
    for pk, v in R["by_protocol"].items():
        if v["accuracy"]:
            ns = sorted(int(n) for n in v["accuracy"]); ax.plot(ns, [v["accuracy"][str(n)] for n in ns], "o-", label=f"{pk} (selected {v['n_selected']})")
    ax.axhline(1 / 3, color="k", ls=":", label="chance"); ax.set_xscale("log", base=2); ax.set_xlabel("fish per encoder hypothesis"); ax.set_ylabel("held-out classification accuracy")
    ax.legend(fontsize=7); ax.set_title("J8 protocol-fair encoder discrimination (selection and features on disjoint trials); SIMULATED", fontsize=9)
    fig.tight_layout(); fig.savefig(dst / "figure.png", dpi=110); plt.close(fig)
    m = base_manifest(rid, name, cr, R, "Protocol-fair looming-experiment design: encoder discrimination with selection and features on disjoint trials", ["organism"],
                      "engineering.neuro.m5_design fair", cr["submission"]["spec"]["command"])
    m["summary"] = {pk: v for pk, v in R["by_protocol"].items()}; write(dst, rid, m, cr, name)


if __name__ == "__main__":
    {"j8": j8, "j1": j1, "j2": j2, "j3": j3, "j4": j4, "j5": j5, "j6": j6, "j7": lambda: j2("j7")}[sys.argv[1]]()
