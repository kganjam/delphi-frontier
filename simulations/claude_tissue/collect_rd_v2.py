"""Collect Sim A v2 (Nebius job log -> sweep-v2.json, figure, receipt).
Usage: python3 collect_rd_v2.py <job_id> <saved_log_path> <job_exit_state>
The log is the job's stdout as returned by `nebius ai job logs`; it is hashed and kept."""
import json, sys, time, base64, pathlib, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from claude_tissue.common import ROOT, sha

OUT = ROOT/"artifacts/simulations/claude-tissue-rd-wavelength"
job, logp, state = sys.argv[1], pathlib.Path(sys.argv[2]), sys.argv[3]
meta, rows, snaps, done = None, [], {}, None
for line in logp.read_text().splitlines():
    i = line.find("META "); j = line.find("RESULT "); k = line.find("SNAP "); m = line.find("DONE ")
    if i >= 0: meta = json.loads(line[i+5:])
    elif j >= 0: rows.append(json.loads(line[j+7:]))
    elif k >= 0: s = json.loads(line[k+5:]); snaps[(s["d"], s["gamma"])] = s
    elif m >= 0: done = json.loads(line[m+5:])
assert meta is not None, "no META line"
for r in rows:
    r["wavelength_obs"] = 2*np.pi/r["k_peak"] if r["patterned"] else None
    r["wavelength_theory"] = 2*np.pi/r["k_theory"] if r["k_theory"] else None
# elasticities from patterned means (log-log slope over d at each gamma; over gamma at each d)
el = {}
for g in meta["gammas"]:
    rs = [r for r in rows if r["gamma"] == g and r["patterned"]]
    ds = sorted({r["d"] for r in rs})
    if len(ds) >= 3:
        lam = [np.mean([r["wavelength_obs"] for r in rs if r["d"] == x]) for x in ds]
        el[f"dlogLambda_dlogd_gamma{g}"] = float(np.polyfit(np.log(ds), np.log(lam), 1)[0])
        lt = [2*np.pi/r["k_theory"] for x in ds for r in rs if r["d"] == x][::3]
        el[f"theory_dlogLambda_dlogd_gamma{g}"] = float(np.polyfit(np.log(ds), np.log(lt), 1)[0])
gs = []
for d in meta["ds"]:
    rs = [r for r in rows if r["d"] == d and r["patterned"]]
    gg = sorted({r["gamma"] for r in rs})
    if len(gg) == 3:
        lam = [np.mean([r["wavelength_obs"] for r in rs if r["gamma"] == x]) for x in gg]
        gs.append(float(np.polyfit(np.log(gg), np.log(lam), 1)[0]))
el["dlogLambda_dloggamma_mean_over_d"] = float(np.mean(gs)) if gs else None
el["dlogLambda_dloggamma_range"] = [float(min(gs)), float(max(gs))] if gs else None
conv = dict(n=len(rows), shell_converged=int(sum(r["converged_shell"] for r in rows)),
            max_rel_k_change_half_to_end=float(max(abs(r["k_peak"] - r["k_peak_half_time"])/r["k_peak"] for r in rows if r["patterned"])))
summary = dict(version=2, job=job, job_state=state, meta=meta, done=done, n_rows=len(rows), elasticities=el, convergence=conv,
               rows=rows, mapping_caveat="Wavelength is in dimensionless length units sqrt(D_u/k_u); converting to fin-ray spacing needs a measured activator diffusivity and turnover rate, which the repo does not have.")
(OUT/"sweep-v2.json").write_text(json.dumps(summary, indent=1))
fig = plt.figure(figsize=(14, 7.5))
ax = fig.add_subplot(2, 1, 1); cols = {0.5: "tab:blue", 1.0: "tab:green", 2.0: "tab:red"}
for g in meta["gammas"]:
    rs = [r for r in rows if r["gamma"] == g and r["patterned"]]; ds = sorted({r["d"] for r in rs})
    m = [np.mean([r["wavelength_obs"] for r in rs if r["d"] == x]) for x in ds]; sd = [np.std([r["wavelength_obs"] for r in rs if r["d"] == x]) for x in ds]
    ax.errorbar(ds, m, sd, marker="o", color=cols[g], label=f"simulated, gamma={g}")
    th = [[2*np.pi/r["k_theory"] for r in rs if r["d"] == x][0] for x in ds]; ax.plot(ds, th, "--", color=cols[g], lw=1, alpha=0.6)
    unp = [r["d"] for r in rows if r["gamma"] == g and not r["patterned"]]
    if unp: ax.scatter(sorted(set(unp)), [ax.get_ylim()[0]]*len(set(unp)), marker="x", color=cols[g])
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlabel("diffusion ratio d (log)"); ax.set_ylabel("wavelength (nondim, log)")
ax.set_title(f"SIMULATED Schnakenberg wavelength, L={meta['L']:g}, N={meta['N']}, t={meta['t_end']:g}, 3 seeds; dashed = linear-theory fastest mode; x = no pattern")
ax.legend(fontsize=8)
pick = [k for k in [(10, 1.0), (20, 1.0), (55, 1.0), (20, 0.5), (20, 2.0)] if k in snaps]
for i, key in enumerate(pick):
    s = snaps[key]; a = np.frombuffer(base64.b64decode(s["u8"]), dtype=np.uint8).reshape(s["n"], s["n"])
    a2 = fig.add_subplot(2, 5, 6+i); a2.imshow(a, cmap="magma"); a2.axis("off"); a2.set_title(f"d={key[0]} gamma={key[1]} (64x64 downsample)", fontsize=8)
fig.tight_layout(); fig.savefig(OUT/"wavelength-sweep-v2.png", dpi=110)
rec = dict(name="claude-tissue-rd-wavelength-v2", command=f"python3 /work/rdwl.py {meta['N']} {meta['L']:g} {meta['t_end']:g}",
           compute=f"Nebius {job} ({meta.get('gpu')}), image nvcr.io/nvidia/pytorch@sha256:11e99763...", job_state=state,
           exit_code=0 if (state == "COMPLETED" and done) else 1, seed=meta["seeds"], wall_s=(done or {}).get("wall_s"),
           code_sha256={"simulations/claude_tissue/rd_wavelength_v2_gpu.py": meta["script_sha256"]},
           code_matches_repo=bool(meta["script_sha256"] == sha(ROOT/"simulations/claude_tissue/rd_wavelength_v2_gpu.py")),
           collector_sha256={"simulations/claude_tissue/collect_rd_v2.py": sha(ROOT/"simulations/claude_tissue/collect_rd_v2.py")},
           input_sha256={}, output_sha256={str(p.relative_to(ROOT)): sha(p) for p in [OUT/"sweep-v2.json", OUT/"wavelength-sweep-v2.png", logp.resolve()]},
           environment=dict(torch=meta["torch"], numpy=meta["numpy"], device=meta["device"]),
           evidence_kind="simulated; not observed", collected_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
(OUT/"receipt-claude-tissue-rd-wavelength-v2.json").write_text(json.dumps(rec, indent=1, sort_keys=True))
print(json.dumps(dict(el=el, conv=conv, n=len(rows), done=done), indent=1))
