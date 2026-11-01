"""Species-level version of the developmental-programme fit (answers the gemini-4-argon pseudoreplication point).
Per species: L = a + c*SL (OLS) on observed specimens.  Group effect on c via a TWO-STAGE bootstrap: resample species
within group, then specimens within species, refit, average c over the resampled species.  With only 2-3 species per
group this interval reflects between-species spread honestly (it widens), and the flying-fish vs other contrasts are
re-tested at the species level.  No phylogenetic covariance is modelled (no tree in the repo): stated, not fixed.
Observed specimens; fitted lines are computed."""
import json, sys, time, csv, pathlib, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from claude_tissue.common import ROOT, write_receipt

OUT = ROOT/"artifacts/simulations/claude-tissue-dev-programme"
DATA = "artifacts/observed-allometry/source-observations.csv"
GROUPS = ["flying fish", "flying halfbeak", "halfbeak", "needlefish"]
NBOOT, SEED = 4000, 20261102

def fit(x, y):
    A = np.c_[np.ones_like(x), x]; return np.linalg.lstsq(A, y, rcond=None)[0]

if __name__ == "__main__":
    t0 = time.time(); rows = list(csv.DictReader(open(ROOT/DATA))); rng = np.random.default_rng(SEED)
    sp = {}
    for r in rows:
        if r["group"] in GROUPS and r["pectoral_cm"]:
            sp.setdefault((r["group"], r["species"]), []).append((float(r["sl_cm"]), float(r["pectoral_cm"])))
    sp = {k: np.array(v) for k, v in sp.items()}
    per = {}
    for (g, s), a in sp.items():
        a_, c_ = fit(a[:, 0], a[:, 1]); per[s] = dict(group=g, n=int(len(a)), a_cm=float(a_), c=float(c_), sl_range=[float(a[:, 0].min()), float(a[:, 0].max())])
        print(g, s, per[s], flush=True)
    boot = {g: [] for g in GROUPS}
    for g in GROUPS:
        names = [k for k in sp if k[0] == g]
        for _ in range(NBOOT):
            pick = [names[i] for i in rng.integers(0, len(names), len(names))]; cs = []
            for k in pick:
                a = sp[k]; i = rng.integers(0, len(a), len(a))
                if len(np.unique(a[i, 0])) < 2: continue
                cs.append(fit(a[i, 0], a[i, 1])[1])
            if cs: boot[g].append(np.mean(cs))
        boot[g] = np.array(boot[g])
    q = lambda v: [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]
    grp = {g: dict(n_species=len([k for k in sp if k[0] == g]), c_species_mean=float(np.mean([per[k[1]]["c"] for k in sp if k[0] == g])),
                   c_ci95_two_stage=q(boot[g])) for g in GROUPS}
    contr = {}
    for o in GROUPS[1:]:
        n = min(len(boot["flying fish"]), len(boot[o])); dlt = boot["flying fish"][:n] - boot[o][:n]
        contr[f"flying fish - {o}"] = dict(delta_c=float(np.mean(dlt)), ci95=q(dlt), fraction_boot_le_0=float(np.mean(dlt <= 0)))
    out = dict(model="per-species L = a + c*SL; group c by two-stage bootstrap (species, then specimens)", data=DATA, bootstrap=dict(n=NBOOT, seed=SEED),
               species=per, groups=grp, contrasts=contr,
               caveats=["2-3 species per group: the species-level resampling has very few distinct draws; intervals are coarse.",
                        "No phylogenetic covariance (no tree in repo).", "Cross-sectional specimens; not growth trajectories."])
    (OUT/"programme-species.json").write_text(json.dumps(out, indent=1))
    fig, ax = plt.subplots(figsize=(8, 4.4)); cols = {"flying fish": "tab:blue", "flying halfbeak": "tab:purple", "halfbeak": "tab:orange", "needlefish": "tab:gray"}
    for i, g in enumerate(GROUPS):
        ss = [k[1] for k in sp if k[0] == g]
        ax.scatter([i + 0.12*(j - (len(ss)-1)/2) for j in range(len(ss))], [per[s]["c"] for s in ss], color=cols[g], s=30, zorder=3)
        for j, s in enumerate(ss): ax.annotate(s.split()[0][:4] + ". " + s.split()[1], (i + 0.12*(j - (len(ss)-1)/2), per[s]["c"]), fontsize=6, xytext=(4, 2), textcoords="offset points")
        lo, hi = grp[g]["c_ci95_two_stage"]; ax.plot([i, i], [lo, hi], color=cols[g], lw=6, alpha=0.25)
    ax.set_xticks(range(len(GROUPS))); ax.set_xticklabels(GROUPS); ax.set_ylabel("c = dL/dSL (fitted per species)")
    ax.set_title("Species-level growth-zone coefficient; bars = two-stage bootstrap 95% (observed specimens, fitted lines)", fontsize=8)
    fig.tight_layout(); fig.savefig(OUT/"programme-species.png", dpi=110); plt.close(fig)
    write_receipt(OUT, "claude-tissue-dev-programme-species", "python3 simulations/claude_tissue/dev_programme_species.py", SEED, [DATA],
                  [OUT/"programme-species.json", OUT/"programme-species.png"], t0)
