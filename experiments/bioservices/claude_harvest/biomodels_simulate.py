"""Run fetched BioModels SBML on CPU with libRoadRunner at the model's own defaults.

Output is SIMULATION of a published model (as curated), not observation, and
nothing is fit to fin data. Model species/params are untouched.
"""
import hashlib, json, sys, time
from pathlib import Path
import numpy as np, roadrunner
OUT = Path(sys.argv[1]); IDS = sys.argv[2:]
res = []
for i in IDS:
    p = OUT / f"biomodels/{i}.xml"; raw = p.read_bytes()
    rr = roadrunner.RoadRunner(raw.decode()); t0 = time.time()
    meta = json.load(open(OUT / f"biomodels/{i}_meta.json"))
    for T, N in ((200, 2001), (1000, 4001)):
        rec = {"model": i, "name": meta.get("name"), "publication": (meta.get("publication") or {}).get("link"),
               "sbml_sha256": hashlib.sha256(raw).hexdigest(), "roadrunner": roadrunner.__version__, "integrator": rr.integrator.getName(),
               "t_end": T, "points": N, "evidence_kind": "simulated",
               "epistemic_status": "simulation of a published model at curated defaults; not observed, not fit to fish data"}
        try:
            rr.resetAll(); r = rr.simulate(0, T, N)
            cols = r.colnames; fin = np.isfinite(r).all()
            rec.update(ok=True, finite=bool(fin), n_species=len([c for c in cols if c.startswith("[")]), wall_s=round(time.time() - t0, 2))
            stats = {}
            for k, c in enumerate(cols[1:], 1):
                y = r[:, k]
                if y.size and np.ptp(y) > 1e-9:
                    # peaks in latter half indicate sustained oscillation
                    h = y[len(y) // 2:]; pk = [j for j in range(1, len(h) - 1) if h[j] > h[j - 1] and h[j] >= h[j + 1] and h[j] - h.min() > 0.05 * max(np.ptp(h), 1e-12)]
                    per = float(np.mean(np.diff(pk)) * (T / (N - 1))) if len(pk) >= 3 else None
                    stats[c] = {"final": float(y[-1]), "min": float(y.min()), "max": float(y.max()), "late_peaks": len(pk), "mean_peak_period": per}
            rec["species_stats_first40"] = dict(list(stats.items())[:40]); rec["n_varying"] = len(stats)
            rec["n_oscillating_late"] = sum(1 for v in stats.values() if v["late_peaks"] >= 3)
        except Exception as e:
            rec.update(ok=False, error=f"{type(e).__name__}: {str(e)[:300]}")
        res.append(rec)
        break_after = rec.get("ok")
        if break_after: break
(OUT / "biomodels/simulation_receipts.json").write_text(json.dumps(res, indent=1, sort_keys=True) + "\n")
for r in res: print(r["model"], r["ok"], r.get("n_varying"), r.get("n_oscillating_late"), r.get("error", ""))
